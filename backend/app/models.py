from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List

class ExtractRequest(BaseModel):
    """Request model for video extraction"""
    url: HttpUrl = Field(..., description="Video URL to extract")

class VideoFormat(BaseModel):
    """Video format information"""
    format_id: str
    quality: str
    ext: str
    filesize: Optional[int] = None
    url: str
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[int] = None
    vcodec: Optional[str] = None
    acodec: Optional[str] = None

class VideoInfo(BaseModel):
    """Video information response"""
    title: str
    thumbnail: Optional[str] = None
    duration: Optional[int] = None
    description: Optional[str] = None
    uploader: Optional[str] = None
    upload_date: Optional[str] = None
    view_count: Optional[int] = None
    formats: List[VideoFormat]
    webpage_url: str
    extractor: str

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str = "1.0.0"
    yt_dlp_version: str

class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    message: str
    detail: Optional[str] = None