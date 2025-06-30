
import os
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from app.services.barcode_service import barcode_service
from app.api.v1.dependencies import verify_api_key

router = APIRouter(prefix="/v1/barcode", tags=["barcode"])

@router.post("/generate-barcode", tags=["Generate Barcode"])
async def generate_barcode(
    data: str = Form(...),
    barcode_type: str = Form('qr'),
    image_format: str = Form('PNG'),
    width: int = Form(250),
    height: int = Form(250),
    logo_file: UploadFile = None,
    x_api_key: str = Depends(verify_api_key)
):
    """
    Generate a barcode.

    - **data**: The data to encode in the barcode.
    - **barcode_type**: The type of barcode to generate (e.g., 'code128', 'qr').
    - **image_format**: The format of the output image (e.g., PNG, JPEG).
    - **width**: The width of the barcode image.
    - **height**: The height of the barcode image.
    - **logo_file**: Optional. An image file to be placed in the center of the barcode.
    """
    try:
        path = await barcode_service.generate_barcode(data, barcode_type, image_format, width, height, logo_file)
        return FileResponse(path, media_type=f'image/{image_format.lower()}', background=BackgroundTask(os.remove, path))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
