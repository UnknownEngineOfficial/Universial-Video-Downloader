from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
import yt_dlp
from utils.logger import logger
from utils.validators import validate_url

router = APIRouter()

@router.get("/direct")
async def download_direct(
    url: str = Query(..., description="Video URL to download"),
    format_id: str = Query(None, description="Specific format ID to download")
):
    """
    Get direct download link for video
    
    Args:
        url: Video URL
        format_id: Optional specific format ID
        
    Returns:
        Redirect to direct video URL
    """
    # Validate URL
    is_valid, message = validate_url(url)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    logger.info(f"Getting download link for: {url}")
    
    try:
        # Import settings here to avoid circular imports
        from app.config import settings
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
        }
        
        # Add cookies file if configured
        if settings.youtube_cookies_file:
            ydl_opts['cookiefile'] = settings.youtube_cookies_file
            
        # Add cookies from browser if configured
        if settings.youtube_cookies_from_browser:
            ydl_opts['cookiesfrombrowser'] = (
                settings.youtube_cookies_from_browser,
                settings.youtube_cookies_browser_profile
            ) if settings.youtube_cookies_browser_profile else settings.youtube_cookies_from_browser
            
        # Add proxy if configured
        if settings.youtube_proxy:
            ydl_opts['proxy'] = settings.youtube_proxy
        
        if format_id:
            ydl_opts['format'] = format_id
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Get the best format URL
            if format_id and 'formats' in info:
                # Find specific format
                for fmt in info['formats']:
                    if fmt.get('format_id') == format_id:
                        video_url = fmt.get('url')
                        if video_url:
                            return RedirectResponse(url=video_url)
            
            # Fallback to default URL
            video_url = info.get('url')
            if not video_url and 'formats' in info and info['formats']:
                # Get first available format
                video_url = info['formats'][0].get('url')
            
            if not video_url:
                raise HTTPException(status_code=404, detail="No video URL found")
            
            return RedirectResponse(url=video_url)
            
    except yt_dlp.utils.DownloadError as e:
        logger.error(f"yt-dlp error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to get download link: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")