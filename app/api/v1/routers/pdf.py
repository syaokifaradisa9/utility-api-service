from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.services.pdf_service import convert_pdf_to_images
from app.api.v1.dependencies import verify_api_key
from app.api.v1.rate_limiter import limiter
from app.core.config import settings

router = APIRouter(prefix="/v1", tags=["pdf"])

@router.post("/pdf-to-image")
@limiter.limit(settings.RATE_LIMIT)
async def pdf_to_image(
    request: Request,
    file: UploadFile = File(...),
    x_api_key: str = Depends(verify_api_key)
):
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="File must be a PDF")
        data = await file.read()
        images = await convert_pdf_to_images(data)
        paths = []
        for i, img in enumerate(images):
            path = f"output_page_{i + 1}.png"
            img.save(path, "PNG")
            paths.append(path)
        return JSONResponse(content={"pages_converted": len(paths), "paths": paths})
    except RateLimitExceeded as e:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")