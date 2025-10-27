from abc import ABC, abstractmethod
from typing import Dict, Optional
import requests
from bs4 import BeautifulSoup

class BaseExtractor(ABC):
    """Base class for custom video extractors"""
    
    def __init__(self, url: str):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    @abstractmethod
    def extract(self) -> Dict:
        """Extract video information and return dict with title, formats, etc."""
        pass
    
    @staticmethod
    @abstractmethod
    def is_supported(url: str) -> bool:
        """Check if this extractor supports the given URL"""
        pass
    
    def fetch_page(self, url: str, timeout: int = 30) -> BeautifulSoup:
        """Fetch and parse HTML page"""
        response = self.session.get(url, timeout=timeout)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'lxml')
    
    def fetch_json(self, url: str, timeout: int = 30) -> dict:
        """Fetch JSON data"""
        response = self.session.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
