import re
import json
from typing import Dict
from .base import BaseExtractor

class PornhubExtractor(BaseExtractor):
    """Custom extractor for Pornhub videos"""
    
    @staticmethod
    def is_supported(url: str) -> bool:
        return 'pornhub.com' in url.lower()
    
    def extract(self) -> Dict:
        """Extract video info from Pornhub"""
        soup = self.fetch_page(self.url)
        
        # Extract title
        title_tag = soup.find('h1', class_='title')
        title = title_tag.text.strip() if title_tag else 'Unknown'
        
        # Find flashvars script
        formats = []
        scripts = soup.find_all('script')
        
        for script in scripts:
            if 'flashvars' in script.text and 'mediaDefinitions' in script.text:
                # Extract JSON data
                match = re.search(r'mediaDefinitions"\s*:\s*(\[.*?\])', script.text, re.DOTALL)
                if match:
                    try:
                        media_defs = json.loads(match.group(1))
                        for media in media_defs:
                            if media.get('videoUrl'):
                                formats.append({
                                    'quality': media.get('quality', 'unknown'),
                                    'url': media['videoUrl'],
                                    'format': media.get('format', 'mp4')
                                })
                    except json.JSONDecodeError:
                        pass
        
        # Extract thumbnail
        thumbnail = None
        thumb_tag = soup.find('meta', property='og:image')
        if thumb_tag:
            thumbnail = thumb_tag.get('content')
        
        return {
            'title': title,
            'thumbnail': thumbnail,
            'formats': formats,
            'extractor': 'pornhub'
        }
