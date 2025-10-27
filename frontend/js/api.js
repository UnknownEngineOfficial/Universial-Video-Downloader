const API_BASE_URL = 'http://localhost:8000/api';

class VideoAPI {
    /**
     * Extract video information from URL
     * @param {string} url - Video URL to extract
     * @returns {Promise<Object>} Video information
     */
    static async extractVideo(url) {
        try {
            const response = await fetch(`${API_BASE_URL}/info/extract`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || error.message || 'Extraction failed');
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
    
    /**
     * Check API health status
     * @returns {Promise<Object>} Health status
     */
    static async checkHealth() {
        try {
            const response = await fetch(`${API_BASE_URL}/health`);
            return await response.json();
        } catch (error) {
            console.error('Health check failed:', error);
            throw error;
        }
    }
    
    /**
     * Download video file
     * @param {string} url - Direct video URL
     * @param {string} filename - Filename for download
     */
    static downloadFile(url, filename) {
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.target = '_blank';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
}
