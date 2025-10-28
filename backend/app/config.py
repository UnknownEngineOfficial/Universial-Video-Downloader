from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    environment: str = "development"
    
    # CORS Settings
    @property
    def cors_origins(self) -> List[str]:
        return ["https://terrible-apparition-9vqpjp556pqcxgxg-80.app.github.dev"]  # GitHub Codespaces URL
    
    # Logging
    log_level: str = "INFO"
    
    # Download Settings
    max_video_size_mb: int = 1000
    download_timeout_seconds: int = 600
    
    # Rate Limiting
    max_requests_per_minute: int = 60
    
    # YouTube Settings
    youtube_cookies_file: Optional[str] = None
    youtube_cookies_from_browser: Optional[str] = None  # chrome, firefox, etc.
    youtube_cookies_browser_profile: Optional[str] = None  # browser profile path
    youtube_proxy: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()