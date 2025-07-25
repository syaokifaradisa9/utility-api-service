import fitz
from PIL import Image
from typing import List, Optional
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
        
async def replace_template_with_image(pdf_data: bytes, template_text: str, image_data: bytes, image_width: float = None, image_height: float = None) -> bytes:
    try:
        # Open the PDF
        pdf = fitz.open(stream=pdf_data, filetype="pdf")
        
        # Load image
        img_temp = tempfile.NamedTemporaryFile(delete=False)
        img_temp.write(image_data)
        img_temp.close()
        
        # Track if we found and replaced any instances
        replacements_made = False
        
        # Process each page
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            
            # Search for the template text in the page
            text_instances = page.search_for(template_text)
            
            for inst in text_instances:
                replacements_made = True
                
                # Calculate dimensions for the image
                rect = inst
                
                # If custom dimensions are provided, adjust the rectangle
                if image_width and image_height:
                    # Center the image at the midpoint of the found text
                    mid_x = (rect.x0 + rect.x1) / 2
                    mid_y = (rect.y0 + rect.y1) / 2
                    rect.x0 = mid_x - (image_width / 2)
                    rect.x1 = mid_x + (image_width / 2)
                    rect.y0 = mid_y - (image_height / 2)
                    rect.y1 = mid_y + (image_height / 2)
                
                # Remove the template text by adding white rectangle
                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                
                # Insert the image
                page.insert_image(rect, filename=img_temp.name)
        
        # Clean up the temporary file
        os.unlink(img_temp.name)
        
        if not replacements_made:
            return {
                "success": False,
                "error": f"Template text '{template_text}' not found in the document.",
                "pdf_data": None
            }
        
        # Save the modified PDF
        output_buffer = io.BytesIO()
        pdf.save(output_buffer)
        pdf.close()
        
        return {
            "success": True,
            "error": None,
            "pdf_data": output_buffer.getvalue()
        }
        
    except Exception as e:
        # Clean up the temporary file if it exists
        try:
            if 'img_temp' in locals() and os.path.exists(img_temp.name):
                os.unlink(img_temp.name)
        except:
            pass
        
        return {
            "success": False,
            "error": f"Error replacing template with image: {str(e)}",
            "pdf_data": None
        }
        
async def is_page_body_empty(page: fitz.Page, header_margin: float = 0.15, footer_margin: float = 0.15, text_threshold: int = 20) -> bool:
    """
    Check if a page body is empty, ignoring headers and footers.
    A page is considered empty if its body has very little text, no significant images, and no vector graphics.
    The body is the area of the page excluding the top and bottom margins.
    """
    page_rect = page.rect
    page_height = page_rect.height
    
    # Define the body area, excluding header and footer
    body_rect = fitz.Rect(
        page_rect.x0,
        page_rect.y0 + page_height * header_margin,
        page_rect.x1,
        page_rect.y1 - page_height * footer_margin
    )

    # 1. Check for text content within the body
    text = page.get_text("text", clip=body_rect)
    if len(text.strip()) > text_threshold:
        return False

    # 2. Check for images within the body
    images = page.get_images(full=True)
    for img_info in images:
        img_rects = page.get_image_rects(img_info[0])
        for rect in img_rects:
            if rect.intersects(body_rect):
                # Check if the intersection area is significant
                if rect.intersect(body_rect).get_area() > 100: # ignore very small images/logos
                    return False

    # 3. Check for vector graphics (drawings) within the body
    drawings = page.get_drawings()
    for path in drawings:
        if path["rect"].intersects(body_rect):
            # If any drawing is in the body, it's not empty
            return False

    return True

async def split_pdf_by_pages(data: bytes, start_page: int = 1, end_page: Optional[int] = None) -> bytes:
    try:
        # Open the PDF
        pdf = fitz.open(stream=data, filetype="pdf")
        
        # Validate page numbers
        total_pages = len(pdf)
        if start_page < 1 or start_page > total_pages:
            raise ValueError(f"Start page must be between 1 and {total_pages}")
        
        if end_page is None:
            end_page = total_pages
        elif end_page < start_page or end_page > total_pages:
            raise ValueError(f"End page must be between {start_page} and {total_pages}")
        
        # Create new PDF with selected pages
        new_pdf = fitz.open()  # Create empty PDF
        
        # Copy pages (convert to 0-based indexing)
        new_pdf.insert_pdf(pdf, from_page=start_page-1, to_page=end_page-1)
        
        # Save to bytes
        output_buffer = io.BytesIO()
        new_pdf.save(output_buffer)
        new_pdf.close()
        pdf.close()
        
        return output_buffer.getvalue()
        
    except Exception as e:
        raise Exception(f"Error splitting PDF: {str(e)}")

async def remove_empty_pages(data: bytes) -> bytes:
    """
    Removes empty pages from a PDF document.
    An empty page is defined by the 'is_page_body_empty' function.
    """
    try:
        # Open the original PDF
        pdf = fitz.open(stream=data, filetype="pdf")
        
        # Create a new PDF to store non-empty pages
        new_pdf = fitz.open()
        
        # Iterate through all pages and add non-empty ones to the new PDF
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            if not await is_page_body_empty(page):
                new_pdf.insert_pdf(pdf, from_page=page_num, to_page=page_num)
        
        if len(new_pdf) == 0:
            raise ValueError("All pages in the document were considered empty.")

        # Save the new PDF to a buffer
        output_buffer = io.BytesIO()
        new_pdf.save(output_buffer)
        new_pdf.close()
        pdf.close()
        
        return output_buffer.getvalue()
        
    except Exception as e:
        raise Exception(f"Error removing empty pages: {str(e)}")
