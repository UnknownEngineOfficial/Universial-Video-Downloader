import re
from typing import Tuple
from urllib.parse import urlparse

def validate_url(url: str) -> Tuple[bool, str]:
    """
    Validate if URL is valid and accessible
    
    Args:
        url: URL to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not url:
        return False, "URL cannot be empty"
    
    # Check if URL starts with http/https
    if not url.startswith(('http://', 'https://')):
        return False, "URL must start with http:// or https://"
    
    # Parse URL
    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            return False, "Invalid URL format"
    except Exception as e:
        return False, f"Invalid URL: {str(e)}"
    
    return True, "Valid URL"

def is_video_url(url: str) -> bool:
    """
    Check if URL is likely a video URL
    
    Args:
        url: URL to check
        
    Returns:
        True if likely a video URL
    """
    video_patterns = [
        r'youtube\.com/watch',
        r'youtu\.be/',
        r'vimeo\.com/',
        r'dailymotion\.com/',
        r'pornhub\.com/',
        r'xvideos\.com/',
        r'redtube\.com/',
        r'twitter\.com/.*/status/',
        r'tiktok\.com/',
        r'instagram\.com/p/',
    ]
    
    for pattern in video_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return True
    
    return False

def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    Sanitize filename for safe file system usage
    
    Args:
        filename: Original filename
        max_length: Maximum length of filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > max_length:
        filename = filename[:max_length]
    
    return filename or 'video'