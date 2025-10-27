const API_BASE_URL = 'http://localhost:8000/api';

class VideoAPI {
    static async extractVideo(url) {
        try {
            const response = await fetch(`${API_BASE_URL}/extract`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Extraction failed');
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
    
    static async checkHealth() {
        const response = await fetch(`${API_BASE_URL}/health`);
        return await response.json();
    }
}
