from typing import Dict, List
from .base import BaseExtractor
import re

class GenericExtractor(BaseExtractor):
    """Generic extractor for common video patterns"""
    
    @staticmethod
    def is_supported(url: str) -> bool:
        # Generic extractor supports all URLs as fallback
        return True
    
    def extract(self) -> Dict:
        """
        Extract video info using generic patterns
        """
        soup = self.fetch_page(self.url)
        
        # Extract title
        title = self._extract_title(soup)
        
        # Extract thumbnail
        thumbnail = self._extract_thumbnail(soup)
        
        # Try to find video URLs
        formats = self._extract_video_urls(soup)
        
        return {
            'title': title,
            'thumbnail': thumbnail,
            'formats': formats,
            'extractor': 'generic'
        }
    
    def _extract_title(self, soup) -> str:
        """Extract title from common meta tags"""
        # Try og:title
        og_title = soup.find('meta', property='og:title')
        if og_title:
            return og_title.get('content', 'Unknown')
        
        # Try title tag
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        return 'Unknown Title'
    
    def _extract_thumbnail(self, soup) -> str:
        """Extract thumbnail from common meta tags"""
        # Try og:image
        og_image = soup.find('meta', property='og:image')
        if og_image:
            return og_image.get('content')
        
        # Try twitter:image
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        if twitter_image:
            return twitter_image.get('content')
        
        return None
    
    def _extract_video_urls(self, soup) -> List[Dict]:
        """Extract video URLs from page"""
        formats = []
        
        # Find video tags
        video_tags = soup.find_all('video')
        for video in video_tags:
            sources = video.find_all('source')
            for source in sources:
                src = source.get('src')
                if src:
                    formats.append({
                        'format_id': 'video',
                        'quality': 'unknown',
                        'url': src,
                        'ext': self._get_extension(src)
                    })
        
        # Find direct video links in scripts
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                # Look for .mp4, .webm, .m3u8 URLs
                video_urls = re.findall(
                    r'["\']((https?://[^"\']*(\.(mp4|webm|m3u8))[^"\']*))["\']',
                    script.string
                )
                for url_match in video_urls:
                    url = url_match[0]
                    formats.append({
                        'format_id': 'direct',
                        'quality': 'unknown',
                        'url': url,
                        'ext': url_match[2]
                    })
        
        return formats
    
    @staticmethod
    def _get_extension(url: str) -> str:
        """Get file extension from URL"""
        match = re.search(r'\.([a-z0-9]{2,4})(?:[\?#]|$)', url, re.IGNORECASE)
        if match:
            return match.group(1)
        return 'mp4'