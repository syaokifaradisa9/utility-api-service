from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.api.v1.dependencies import verify_api_key

router = APIRouter(prefix="/v1", tags=["health"])

@router.get("/health", dependencies=[Depends(verify_api_key)])
async def health_check():
    return JSONResponse(content={"status": "ok", "version": "v1"})