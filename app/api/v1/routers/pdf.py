import io
from app.core.config import settings
from app.api.v1.rate_limiter import limiter
from fastapi.responses import PlainTextResponse
from app.api.v1.dependencies import verify_api_key
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Request
from app.services.pdf_service import convert_pdf_to_single_image, convert_pdf_to_text

router = APIRouter(prefix="/v1/pdf", tags=["pdf"])

@router.post("/convert-to-image")
@limiter.limit(settings.RATE_LIMIT)
async def pdf_to_image(
    request: Request,
    file: UploadFile = File(...),
    x_api_key: str = Depends(verify_api_key)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    data = await file.read()
    
    image_bytes = await convert_pdf_to_single_image(data, dpi=150)
    return StreamingResponse(
        io.BytesIO(image_bytes),
        media_type="image/png",
        headers={"Content-Disposition": "inline; filename=combined.png"}
    )
    
@router.post("/convert-to-text")
@limiter.limit(settings.RATE_LIMIT)
async def convert_to_text(
    request: Request,
    file: UploadFile = File(...),
    dpi: int = 300,
    language: str = "en",
    x_api_key: str = Depends(verify_api_key)
):
    """Extract text from PDF with automatic fallback to OCR if needed"""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Parse language parameter
    lang_list = language.split(',')
    
    data = await file.read()
    
    # First try regular text extraction
    result = await convert_pdf_to_text(data)
    
    if not result["success"]:
        return JSONResponse(
            status_code=422,
            content={
                "detail": result["error"],
                "page_count": result["page_count"],
            }
        )
    
    # Return successful text response
    return JSONResponse(
        content={
            "text": result["text"],
            "page_count": result["page_count"]
        },
        headers={"Content-Disposition": "attachment; filename=extracted_text.json"}
    )