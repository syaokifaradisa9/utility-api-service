import fitz  # PyMuPDF
from PIL import Image
import io

async def convert_pdf_to_single_image(data: bytes, dpi: int = 150) -> bytes:
    # Buka PDF dari bytes
    pdf = fitz.open(stream=data, filetype="pdf")
    images = []
    # Matrix untuk scaling sesuai DPI: 72 * scale = dpi → scale = dpi/72
    scale = dpi / 72
    mat = fitz.Matrix(scale, scale)

    for page in pdf:
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)

    # Gabungkan secara vertikal
    max_width = max(img.width for img in images)
    total_height = sum(img.height for img in images)
    combined = Image.new("RGB", (max_width, total_height), (255, 255, 255))

    y_offset = 0
    for img in images:
        combined.paste(img, (0, y_offset))
        y_offset += img.height

    # Simpan ke buffer PNG
    buf = io.BytesIO()
    combined.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()