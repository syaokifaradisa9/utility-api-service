

from fastapi import UploadFile, HTTPException
import os
import uuid
import platform
import subprocess

class DocxService:
    def __init__(self):
        self.upload_dir = "uploads"
        os.makedirs(self.upload_dir, exist_ok=True)

    async def convert_to_pdf(self, file: UploadFile):
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

        pdf_path = os.path.splitext(upload_path)[0] + ".pdf"

        # Try converting with MS Word first on Windows
        if platform.system() == "Windows":
            try:
                from docx2pdf import convert
                convert(upload_path, pdf_path)
                return pdf_path
            except Exception as e:
                print(f"MS Word conversion failed: {e}. Falling back to LibreOffice.")

        # Fallback to LibreOffice if not on Windows or MS Word conversion fails
        try:
            if platform.system() == "Windows":
                libreoffice_path = "C:\\Program Files\\LibreOffice\\program\\soffice.exe"
                if not os.path.exists(libreoffice_path):
                    raise HTTPException(status_code=500, detail="LibreOffice not found. Please install it and ensure the path is correct.")
                command = [libreoffice_path, '--headless', '--convert-to', 'pdf', '--outdir', self.upload_dir, upload_path]
            else:
                command = ['soffice', '--headless', '--convert-to', 'pdf', '--outdir', self.upload_dir, upload_path]

            subprocess.run(command, check=True)
            
            base_name = os.path.splitext(os.path.basename(upload_path))[0]
            converted_pdf_path = os.path.join(self.upload_dir, base_name + '.pdf')
            os.rename(converted_pdf_path, pdf_path)
            
            return pdf_path
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="LibreOffice not found. Please install it and ensure it's in your system's PATH.")
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during PDF conversion: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

docx_service = DocxService()

