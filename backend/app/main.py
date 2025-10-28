from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import yt_dlp
from app.config import settings
from app.models import HealthResponse
from utils.logger import logger
from app.routes import api_router

app = FastAPI(
    title="Universal Video Downloader API",
    description="Backend API for video extraction from 1000+ platforms",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "message": str(exc)}
    )

# Include API routes
app.include_router(api_router, prefix="/api")

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        yt_dlp_version=yt_dlp.version.__version__
    )



@app.get("/")
async def root():
    return {
        "message": "Universal Video Downloader API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
