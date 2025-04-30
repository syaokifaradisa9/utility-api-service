from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from app.services.pdf_service import convert_pdf_to_single_image
from app.api.v1.dependencies import verify_api_key
from app.api.v1.rate_limiter import limiter
from app.core.config import settings
import io

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
    # DPI bisa diambil dari query param jika diinginkan, contoh tetap pakai default 150
    image_bytes = await convert_pdf_to_single_image(data, dpi=150)
    return StreamingResponse(
        io.BytesIO(image_bytes),
        media_type="image/png",
        headers={"Content-Disposition": "inline; filename=combined.png"}
    )