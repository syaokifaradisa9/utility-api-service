from fastapi import HTTPException, UploadFile
from barcode import get_barcode_class
from barcode.writer import ImageWriter
from PIL import Image
import os
import uuid
import io
import qrcode

class BarcodeService:
    def __init__(self):
        self.upload_dir = "uploads"
        os.makedirs(self.upload_dir, exist_ok=True)

    async def generate_barcode(self, data: str, barcode_type: str, image_format: str, width: int, height: int, logo_file: UploadFile = None):
        try:
            if barcode_type.lower() == 'qr':
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=10,
                    border=4,
                )
                qr.add_data(data)
                qr.make(fit=True)
                barcode_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

                # Resize QR code to desired width and height
                barcode_img = barcode_img.resize((width, height), Image.LANCZOS)

            else:
                # Get the barcode class for 1D barcodes
                barcode_class = get_barcode_class(barcode_type)

                # Generate the barcode
                barcode = barcode_class(data, writer=ImageWriter())

                # Generate the barcode to an in-memory BytesIO object
                temp_barcode_buffer = io.BytesIO()
                options = {'module_width': width, 'module_height': height}
                barcode.write(temp_barcode_buffer, options)
                temp_barcode_buffer.seek(0) # Rewind the buffer to the beginning
                barcode_img = Image.open(temp_barcode_buffer)

            if logo_file:
                logo_img = Image.open(io.BytesIO(await logo_file.read()))
                
                # Calculate logo size to fit within barcode (e.g., 20% of barcode height)
                barcode_width, barcode_height = barcode_img.size
                logo_max_height = int(barcode_height * 0.35)
                logo_max_width = int(barcode_width * 0.35)

                logo_img.thumbnail((logo_max_width, logo_max_height), Image.LANCZOS)

                # Calculate position to center the logo
                logo_width, logo_height = logo_img.size
                position = ((barcode_width - logo_width) // 2, (barcode_height - logo_height) // 2)

                # Ensure barcode_img is RGBA for pasting with alpha channel
                if barcode_img.mode != 'RGBA':
                    barcode_img = barcode_img.convert('RGBA')

                # Create a white background for the logo if it has an alpha channel
                if logo_img.mode == 'RGBA':
                    white_bg = Image.new('RGBA', logo_img.size, (255, 255, 255, 255))
                    white_bg.paste(logo_img, (0, 0), logo_img)
                    logo_to_paste = white_bg
                else:
                    logo_to_paste = logo_img
                
                barcode_img.paste(logo_to_paste, position, logo_to_paste if logo_to_paste.mode == 'RGBA' else None)

            # Save the final barcode image
            filename = f"{uuid.uuid4()}.{image_format.lower()}"
            path = os.path.join(self.upload_dir, filename)
            barcode_img.save(path)
            
            return path
        except Image.DecompressionBombError:
            raise HTTPException(status_code=400, detail="Logo image is too large. Please use a smaller image.")
        except Exception as e:
            import traceback
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

barcode_service = BarcodeService()