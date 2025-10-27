from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup

class BaseExtractor(ABC):
    """Base class for custom video extractors"""
    
    def __init__(self, url: str):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    @abstractmethod
    def extract(self) -> Dict:
        """Extract video information"""
        pass
    
    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse HTML page"""
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'lxml')
    
    @staticmethod
    def is_supported(url: str) -> bool:
        """Check if URL is supported by this extractor"""
        return False
