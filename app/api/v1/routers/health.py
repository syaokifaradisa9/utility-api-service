from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/v1", tags=["health"])

@router.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok", "version": "v1"})