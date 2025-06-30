
from fastapi import UploadFile, HTTPException
from docx2pdf import convert
import os
import uuid

class DocxService:
    def __init__(self):
        self.upload_dir = "uploads"
        os.makedirs(self.upload_dir, exist_ok=True)

    async def convert_to_pdf(self, file: UploadFile):
        try:
            # Validate file type
            if file.content_type not in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
                raise HTTPException(status_code=400, detail="Invalid file type. Only .docx and .doc are supported.")

            # Validate file size (10MB limit)
            if file.file._file.seekable():
                file.file._file.seek(0, 2)
                size = file.file._file.tell()
                file.file._file.seek(0)
                if size > 10 * 1024 * 1024:
                    raise HTTPException(status_code=413, detail="File size exceeds the 10MB limit.")

            # Save the uploaded file
            file_ext = os.path.splitext(file.filename)[1]
            upload_path = os.path.join(self.upload_dir, f"{uuid.uuid4()}{file_ext}")
            with open(upload_path, "wb") as buffer:
                buffer.write(await file.read())

            # Convert to PDF
            pdf_path = os.path.splitext(upload_path)[0] + ".pdf"
            convert(upload_path, pdf_path)

            return pdf_path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

docx_service = DocxService()
