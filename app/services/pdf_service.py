import fitz
from PIL import Image
import io
import numpy as np
import tempfile
import os

async def convert_pdf_to_single_image(data: bytes, dpi: int = 150) -> bytes:
    pdf = fitz.open(stream=data, filetype="pdf")
    images = []
    
    scale = dpi / 72
    mat = fitz.Matrix(scale, scale)

    for page in pdf:
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)

    max_width = max(img.width for img in images)
    total_height = sum(img.height for img in images)
    combined = Image.new("RGB", (max_width, total_height), (255, 255, 255))

    y_offset = 0
    for img in images:
        combined.paste(img, (0, y_offset))
        y_offset += img.height

    buf = io.BytesIO()
    combined.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()

async def convert_pdf_to_text(data: bytes) -> dict:
    try:
        # Open PDF from bytes
        pdf = fitz.open(stream=data, filetype="pdf")
        
        # Initialize result
        result = {
            "success": True,
            "text": "",
            "page_count": len(pdf),
            "has_text": False,
            "error": None
        }
        
        # Check if any page has text content
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            if page.get_text().strip():
                result["has_text"] = True
                break
        
        # If no text found in any page
        if not result["has_text"]:
            result["success"] = False
            result["error"] = "No text found in PDF. The document might be scanned or image-based."
            return result
        
        # Extract text from each page
        for i, page in enumerate(pdf):
            page_text = page.get_text()
            result["text"] += page_text
            if i < len(pdf) - 1:  # Don't add page break after last page
                result["text"] += "\n\n--- Page Break ---\n\n"
        
        return result
    
    except Exception as e:
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "has_text": False,
            "error": f"Error processing PDF: {str(e)}"
        }
    

    """Extract text from PDF using EasyOCR for scanned documents"""
    try:
        # Initialize reader inside the function
        reader = easyocr.Reader(lang)
        
        # Open PDF from bytes
        pdf = fitz.open(stream=data, filetype="pdf")
        
        # Initialize result
        result = {
            "success": True,
            "text": "",
            "page_count": len(pdf),
            "used_ocr": True,
            "error": None
        }
        
        # Matrix for scaling according to DPI
        scale = dpi / 72
        mat = fitz.Matrix(scale, scale)
        
        for i, page in enumerate(pdf):
            # Render page to image
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Convert to numpy array for EasyOCR
            img_np = np.array(img)
            
            # Apply OCR to extract text
            ocr_result = reader.readtext(img_np)
            
            # Extract text from EasyOCR result
            page_text = ""
            for detection in ocr_result:
                text = detection[1]  # text is in the second position
                page_text += text + " "
            
            result["text"] += page_text.strip()
            
            if i < len(pdf) - 1:
                result["text"] += "\n\n--- Page Break ---\n\n"
        
        return result
    
    except Exception as e:
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "used_ocr": False,
            "error": f"Error processing PDF with EasyOCR: {str(e)}"
        }
        
async def convert_pdf_to_text_with_ocr(data: bytes, dpi: int = 300, lang: list = None) -> dict:
    """Extract text from PDF using Tesseract OCR for scanned documents"""
    try:
        # Open PDF from bytes
        pdf = fitz.open(stream=data, filetype="pdf")
        
        # Initialize result
        result = {
            "success": True,
            "text": "",
            "page_count": len(pdf),
            "used_ocr": True,
            "error": None
        }
        
        # Matrix for scaling according to DPI
        scale = dpi / 72
        mat = fitz.Matrix(scale, scale)
        
        # Use the provided language or default to English
        language = '+'.join(lang) if lang and len(lang) > 0 else 'eng'
        
        for i, page in enumerate(pdf):
            try:
                # Render page to image
                pix = page.get_pixmap(matrix=mat)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # Apply OCR to extract text with language support
                page_text = pytesseract.image_to_string(img, lang=language)
                result["text"] += page_text
                
                if i < len(pdf) - 1:
                    result["text"] += "\n\n--- Page Break ---\n\n"
            except Exception as page_error:
                # If an individual page fails, log the error but continue with other pages
                result["text"] += f"\n\n--- Error processing page {i+1}: {str(page_error)} ---\n\n"
        
        return result
    
    except Exception as e:
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "used_ocr": False,
            "error": f"Error processing PDF with Tesseract OCR: {str(e)}"
        }