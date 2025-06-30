import uvicorn
from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from app.api.v1.rate_limiter import limiter
from app.api.v1.routers import health, pdf, about, docx, barcode
from app.utils.logger import logger

# Create FastAPI app and attach rate limiter
app = FastAPI(title="PDF to Image Service")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application...")

# Include routers
app.include_router(health.router)
app.include_router(pdf.router)
app.include_router(about.router)
app.include_router(docx.router)
app.include_router(barcode.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)