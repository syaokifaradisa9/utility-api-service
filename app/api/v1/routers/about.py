from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["about"])

@router.get("/about")
async def about():
    return {
        "service": "Loka Pengamanan Alat dan Fasilitas Kesehatan API",
        "description": "Endpoint yang berisi beberapa tools melalui API di Loka Pengamanan Alat dan Fasilitas Kesehatan.",
        "created_by": "Muhammad Syaoki Faradisa (syaokifaradisa09)"
    }