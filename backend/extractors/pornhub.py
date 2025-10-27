import re
import json
from typing import Dict, List
from .base import BaseExtractor

class PornhubExtractor(BaseExtractor):
    """Custom extractor for Pornhub videos"""
    
    @staticmethod
    def is_supported(url: str) -> bool:
        return 'pornhub.com' in url.lower() and '/view_video.php' in url.lower()
    
    def extract(self) -> Dict:
        """Extract video info from Pornhub"""
        soup = self.fetch_page(self.url)
        
        # Extract title
        title = self._extract_title(soup)
        
        # Extract thumbnail
        thumbnail = self._extract_thumbnail(soup)
        
        # Extract video formats
        formats = self._extract_formats(soup)
        
        # Extract metadata
        duration = self._extract_duration(soup)
        uploader = self._extract_uploader(soup)
        view_count = self._extract_views(soup)
        
        return {
            'title': title,
            'thumbnail': thumbnail,
            'duration': duration,
            'uploader': uploader,
            'view_count': view_count,
            'formats': formats,
            'extractor': 'pornhub'
        }
    
    def _extract_title(self, soup) -> str:
        title_tag = soup.find('h1', class_='title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        # Fallback to meta tag
        meta_title = soup.find('meta', property='og:title')
        if meta_title:
            return meta_title.get('content', 'Unknown')
        
        return 'Unknown Title'
    
    def _extract_thumbnail(self, soup) -> str:
        meta_image = soup.find('meta', property='og:image')
        if meta_image:
            return meta_image.get('content')
        return None
    
    def _extract_formats(self, soup) -> List[Dict]:
        formats = []
        scripts = soup.find_all('script')
        
        for script in scripts:
            script_text = script.string
            if not script_text:
                continue
            
            # Method 1: flashvars mediaDefinitions
            if 'flashvars' in script_text and 'mediaDefinitions' in script_text:
                match = re.search(r'mediaDefinitions"\s*:\s*(\[.*?\])', script_text, re.DOTALL)
                if match:
                    try:
                        media_defs = json.loads(match.group(1))
                        for media in media_defs:
                            if media.get('videoUrl'):
                                formats.append({
                                    'format_id': media.get('quality', 'unknown'),
                                    'quality': media.get('quality', 'unknown'),
                                    'url': media['videoUrl'],
                                    'ext': media.get('format', 'mp4')
                                })
                    except json.JSONDecodeError:
                        pass
            
            # Method 2: Direct video URLs
            video_urls = re.findall(r'"(https://[^"]*\.mp4[^"]*)"', script_text)
            for url in video_urls:
                quality = self._guess_quality_from_url(url)
                formats.append({
                    'format_id': quality,
                    'quality': quality,
                    'url': url,
                    'ext': 'mp4'
                })
        
        return formats
    
    def _extract_duration(self, soup) -> Optional[int]:
        duration_tag = soup.find('meta', property='video:duration')
        if duration_tag:
            try:
                return int(duration_tag.get('content'))
            except (ValueError, TypeError):
                pass
        return None
    
    def _extract_uploader(self, soup) -> str:
        uploader_tag = soup.find('div', class_='usernameBadgesWrapper')
        if uploader_tag:
            username = uploader_tag.find('a')
            if username:
                return username.get_text(strip=True)
        return 'Unknown'
    
    def _extract_views(self, soup) -> Optional[int]:
        views_tag = soup.find('span', class_='count')
        if views_tag:
            views_text = views_tag.get_text(strip=True)
            # Remove commas and convert to int
            try:
                return int(views_text.replace(',', ''))
            except ValueError:
                pass
        return None
    
    @staticmethod
    def _guess_quality_from_url(url: str) -> str:
        """Guess quality from URL pattern"""
        if '1080P' in url.upper():
            return '1080p'
        elif '720P' in url.upper():
            return '720p'
        elif '480P' in url.upper():
            return '480p'
        elif '360P' in url.upper():
            return '360p'
        return 'unknown'
