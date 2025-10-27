from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import yt_dlp
import logging
from app.config import settings
from app.models import ExtractRequest, VideoInfo, VideoFormat, HealthResponse
from app.utils.logger import logger
from app.utils.validators import validate_url, is_video_url

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

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        yt_dlp_version=yt_dlp.version.__version__
    )

@app.post("/api/extract", response_model=VideoInfo)
async def extract_video_info(request: ExtractRequest):
    """Extract video information from URL"""
    url = str(request.url)
    
    # Validate URL
    is_valid, message = validate_url(url)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    logger.info(f"Extracting info from: {url}")
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'format': 'best',
            'nocheckcertificate': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Parse formats
            formats = []
            if 'formats' in info:
                for fmt in info['formats']:
                    if fmt.get('url'):
                        formats.append(VideoFormat(
                            format_id=fmt.get('format_id', ''),
                            quality=fmt.get('format_note', fmt.get('quality', 'unknown')),
                            ext=fmt.get('ext', 'mp4'),
                            filesize=fmt.get('filesize'),
                            url=fmt.get('url'),
                            width=fmt.get('width'),
                            height=fmt.get('height'),
                            fps=fmt.get('fps'),
                            vcodec=fmt.get('vcodec'),
                            acodec=fmt.get('acodec')
                        ))
            
            # If no formats found, try direct URL
            if not formats and info.get('url'):
                formats.append(VideoFormat(
                    format_id='direct',
                    quality='default',
                    ext=info.get('ext', 'mp4'),
                    url=info.get('url'),
                    filesize=None,
                    width=None,
                    height=None,
                    fps=None,
                    vcodec=None,
                    acodec=None
                ))
            
            return VideoInfo(
                title=info.get('title', 'Unknown Title'),
                thumbnail=info.get('thumbnail'),
                duration=info.get('duration'),
                description=info.get('description', ''),
                uploader=info.get('uploader', info.get('channel', 'Unknown')),
                upload_date=info.get('upload_date'),
                view_count=info.get('view_count'),
                formats=formats,
                webpage_url=info.get('webpage_url', url),
                extractor=info.get('extractor', 'generic')
            )
            
    except yt_dlp.utils.DownloadError as e:
        logger.error(f"yt-dlp error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to extract video: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

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
