import io
from typing import Optional
from app.core.config import settings
from app.api.v1.rate_limiter import limiter
from app.api.v1.dependencies import verify_api_key
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Request, Form
from app.services.pdf_service import (
    convert_pdf_to_single_image, 
    convert_pdf_to_text,
    replace_template_with_image,
    split_pdf_by_pages
)

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
    
@router.post("/sign")
@limiter.limit(settings.RATE_LIMIT)
async def sign_document_with_image(
    request: Request,
    pdf_file: UploadFile = File(...),
    image_file: UploadFile = File(...),
    template_text: str = Form("${sign}"),
    image_width: Optional[float] = Form(None),
    image_height: Optional[float] = Form(None),
    x_api_key: str = Depends(verify_api_key)
):
    if pdf_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="First file must be a PDF")
    
    # Validate image file
    valid_image_types = ["image/png", "image/jpeg", "image/jpg", "image/gif"]
    if image_file.content_type not in valid_image_types and not image_file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Second file must be an image")
    
    # Read the files
    pdf_data = await pdf_file.read()
    image_data = await image_file.read()
    
    # Replace template with image
    result = await replace_template_with_image(
        pdf_data, 
        template_text, 
        image_data,
        image_width,
        image_height
    )
    
    if not result["success"]:
        raise HTTPException(status_code=422, detail=result["error"])
        
    # Return the modified PDF
    return StreamingResponse(
        io.BytesIO(result["pdf_data"]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=modified_{pdf_file.filename}"}
    )
    
@router.post("/split-by-range")
@limiter.limit(settings.RATE_LIMIT)
async def split_pdf_range(
    request: Request,
    file: UploadFile = File(...),
    start_page: int = Form(1),
    end_page: Optional[int] = Form(None),
    x_api_key: str = Depends(verify_api_key)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        data = await file.read()
        result_pdf = await split_pdf_by_pages(data, start_page, end_page)
        
        filename = f"split_pages_{start_page}_to_{end_page or 'end'}.pdf"
        
        return StreamingResponse(
            io.BytesIO(result_pdf),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")