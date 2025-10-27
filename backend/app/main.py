from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import yt_dlp
import logging
from app.config import settings
from app.models import ExtractRequest, VideoInfo, VideoFormat, HealthResponse, ErrorResponse

# Logging setup
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Universal Video Downloader API",
    description="Backend API for video extraction and downloading",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        yt_dlp_version=yt_dlp.version.__version__
    )

@app.post("/api/extract", response_model=VideoInfo)
async def extract_video_info(request: ExtractRequest):
    """Extract video information from URL"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'format': 'best',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(str(request.url), download=False)
            
            # Parse formats
            formats = []
            if 'formats' in info:
                for fmt in info['formats']:
                    if fmt.get('url'):
                        formats.append(VideoFormat(
                            format_id=fmt.get('format_id', ''),
                            quality=fmt.get('format_note', 'unknown'),
                            ext=fmt.get('ext', 'mp4'),
                            filesize=fmt.get('filesize'),
                            url=fmt.get('url'),
                            width=fmt.get('width'),
                            height=fmt.get('height'),
                            fps=fmt.get('fps'),
                            vcodec=fmt.get('vcodec'),
                            acodec=fmt.get('acodec')
                        ))
            
            return VideoInfo(
                title=info.get('title', 'Unknown'),
                thumbnail=info.get('thumbnail'),
                duration=info.get('duration'),
                description=info.get('description'),
                uploader=info.get('uploader'),
                upload_date=info.get('upload_date'),
                view_count=info.get('view_count'),
                formats=formats,
                webpage_url=info.get('webpage_url', str(request.url)),
                extractor=info.get('extractor', 'generic')
            )
            
    except yt_dlp.utils.DownloadError as e:
        logger.error(f"Download error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to extract video: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
