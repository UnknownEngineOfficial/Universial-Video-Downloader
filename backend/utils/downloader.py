import yt_dlp
from typing import Dict, Optional
from app.utils.logger import logger
from app.utils.validators import sanitize_filename

class VideoDownloader:
    """
    Video downloader using yt-dlp
    """
    
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
        }
    
    def extract_info(self, url: str, download: bool = False) -> Dict:
        """
        Extract video information
        
        Args:
            url: Video URL
            download: Whether to download the video
            
        Returns:
            Video information dictionary
        """
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=download)
                return info
        except Exception as e:
            logger.error(f"Failed to extract info: {str(e)}")
            raise
    
    def download_video(self, url: str, output_path: Optional[str] = None, format_id: Optional[str] = None) -> str:
        """
        Download video to specified path
        
        Args:
            url: Video URL
            output_path: Output directory path
            format_id: Specific format ID to download
            
        Returns:
            Path to downloaded file
        """
        opts = self.ydl_opts.copy()
        
        if output_path:
            opts['outtmpl'] = f"{output_path}/%(title)s.%(ext)s"
        
        if format_id:
            opts['format'] = format_id
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                logger.info(f"Downloaded: {filename}")
                return filename
        except Exception as e:
            logger.error(f"Failed to download: {str(e)}")
            raise
    
    def get_formats(self, url: str) -> list:
        """
        Get available formats for video
        
        Args:
            url: Video URL
            
        Returns:
            List of available formats
        """
        info = self.extract_info(url, download=False)
        return info.get('formats', [])