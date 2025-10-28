// Use a relative API base by default so requests are sent to the same origin
// (e.g. when frontend is served by nginx at http://localhost that proxies /api/ to backend).
// This avoids cross-origin requests which often lead to "NetworkError when attempting to fetch resource." in the browser.
const API_BASE_URL = (window.__API_BASE_URL__ && typeof window.__API_BASE_URL__ === 'string') ? window.__API_BASE_URL__ : '/api';

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
                // try to include server error details if available
                let errText = `HTTP ${response.status}`;
                try {
                    const errBody = await response.json();
                    errText = errBody.detail || errBody.message || JSON.stringify(errBody);
                } catch (e) {
                    try {
                        const txt = await response.text();
                        if (txt) errText = txt;
                    } catch(_){}
                }
                throw new Error(errText || 'Extraction failed');
            }

            return await response.json();
        } catch (error) {
            // NetworkErrors (CORS, no backend) will show up here — include helpful hint
            console.error('API Error:', error);
            if (error instanceof TypeError) {
                console.error('TypeError likely indicates network/CORS issue or backend not reachable. Ensure backend is running and /api is proxied by nginx or API_BASE_URL is reachable.');
            }
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
