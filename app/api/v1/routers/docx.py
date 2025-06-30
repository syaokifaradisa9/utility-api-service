
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from app.api.v1.dependencies import verify_api_key
from app.services.docx_service import DocxService, docx_service

router = APIRouter(prefix="/v1/docx", tags=["pdf"])

@router.post("/docx-to-pdf", tags=["DOCX Conversion"])
async def convert_docx_to_pdf(
    file: UploadFile = File(None),
    service: DocxService = Depends(lambda: docx_service),
    x_api_key: str = Depends(verify_api_key)
):
    """
    Convert a DOCX or DOC file to PDF.
    """
    if not file:
        return JSONResponse(status_code=400, content={"message": "File is required"})

    pdf_path = await service.convert_to_pdf(file)
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"{file.filename}.pdf")
