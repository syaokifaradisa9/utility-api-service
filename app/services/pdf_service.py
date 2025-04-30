from pdf2image import convert_from_bytes

async def convert_pdf_to_images(data: bytes):
    return convert_from_bytes(data)