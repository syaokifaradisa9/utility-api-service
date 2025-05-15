from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["about"])

@router.get("/about")
async def about():
    return {
        "service": "Loka Pengamanan Alat dan Fasilitas Kesehatan API",
        "description": "Endpoint yang berisi beberapa tools melalui Rest API",
        "created_by": "Muhammad Syaoki Faradisa (syaokifaradisa09)",
        "notes" : "Mohon tidak menjual atau mencari keuntungan secara pribadi dengan repository ini. Jika anda melanggar silahkan tanggungjawab sendiri di akhirat kelak."
    }