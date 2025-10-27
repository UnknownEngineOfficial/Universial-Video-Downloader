let currentVideoInfo = null;

/**
 * Handle video extraction
 */
async function handleExtract() {
    const urlInput = document.getElementById('videoUrl');
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('Bitte geben Sie eine gültige Video-URL ein');
        return;
    }
    
    // Basic URL validation
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        showError('URL muss mit http:// oder https:// beginnen');
        return;
    }
    
    try {
        clearVideoInfo();
        showLoader('Video wird analysiert... Dies kann einige Sekunden dauern.');
        
        currentVideoInfo = await VideoAPI.extractVideo(url);
        
        hideLoader();
        displayVideoInfo(currentVideoInfo);
        
        showNotification('Video erfolgreich extrahiert!', 'success');
        
    } catch (error) {
        hideLoader();
        showError(`Fehler: ${error.message}`);
        console.error('Extraction error:', error);
    }
}

/**
 * Display video information
 */
function displayVideoInfo(info) {
    const container = document.getElementById('videoInfo');
    
    // Sort formats by quality (highest first)
    const sortedFormats = info.formats.sort((a, b) => {
        const heightA = a.height || 0;
        const heightB = b.height || 0;
        return heightB - heightA;
    });
    
    let html = `
        <div class="video-card">
            ${info.thumbnail ? `<img src="${info.thumbnail}" alt="${info.title}" class="thumbnail">` : ''}
            <h2>${escapeHtml(info.title)}</h2>
            <div class="video-meta">
                ${info.uploader ? `<p><strong>Uploader:</strong> ${escapeHtml(info.uploader)}</p>` : ''}
                ${info.duration ? `<p><strong>Dauer:</strong> ${formatDuration(info.duration)}</p>` : ''}
                ${info.view_count ? `<p><strong>Aufrufe:</strong> ${formatNumber(info.view_count)}</p>` : ''}
                ${info.upload_date ? `<p><strong>Hochgeladen:</strong> ${formatDate(info.upload_date)}</p>` : ''}
                <p><strong>Plattform:</strong> ${escapeHtml(info.extractor)}</p>
            </div>
            
            <div class="formats">
                <h3>📥 Verfügbare Download-Optionen (${sortedFormats.length})</h3>
                <div class="format-grid">
                    ${sortedFormats.map((fmt, idx) => `
                        <button class="quality-btn" onclick="downloadVideo(${idx})" title="${getFormatDetails(fmt)}">
                            <span class="format-quality">${getQualityLabel(fmt)}</span>
                            <span class="format-info">${fmt.ext.toUpperCase()}</span>
                            ${fmt.filesize ? `<span class="format-size">${formatFilesize(fmt.filesize)}</span>` : ''}
                        </button>
                    `).join('')}
                </div>
            </div>
            
            ${info.description ? `
                <div class="video-description">
                    <h3>Beschreibung</h3>
                    <p>${escapeHtml(info.description).substring(0, 300)}${info.description.length > 300 ? '...' : ''}</p>
                </div>
            ` : ''}
        </div>
    `;
    
    container.innerHTML = html;
    container.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Download selected video format
 */
function downloadVideo(formatIndex) {
    if (!currentVideoInfo || !currentVideoInfo.formats[formatIndex]) {
        showError('Ungültiges Format ausgewählt');
        return;
    }
    
    const format = currentVideoInfo.formats[formatIndex];
    const filename = `${sanitizeFilename(currentVideoInfo.title)}.${format.ext}`;
    
    showNotification('Download wird gestartet...', 'info');
    
    // Open in new tab (browser will handle download)
    window.open(format.url, '_blank');
}

/**
 * Format duration in seconds to readable format
 */
function formatDuration(seconds) {
    if (!seconds) return 'Unbekannt';
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Format file size in bytes
 */
function formatFilesize(bytes) {
    if (!bytes) return '';
    const mb = bytes / 1024 / 1024;
    if (mb > 1024) {
        return (mb / 1024).toFixed(2) + ' GB';
    }
    return mb.toFixed(2) + ' MB';
}

/**
 * Format number with thousands separator
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

/**
 * Format upload date (YYYYMMDD to readable format)
 */
function formatDate(dateStr) {
    if (!dateStr || dateStr.length !== 8) return dateStr;
    const year = dateStr.substring(0, 4);
    const month = dateStr.substring(4, 6);
    const day = dateStr.substring(6, 8);
    return `${day}.${month}.${year}`;
}

/**
 * Get quality label for format
 */
function getQualityLabel(fmt) {
    if (fmt.height) {
        return `${fmt.height}p${fmt.fps ? ` ${fmt.fps}fps` : ''}`;
    }
    return fmt.quality || 'Standard';
}

/**
 * Get format details tooltip
 */
function getFormatDetails(fmt) {
    let details = [];
    if (fmt.width && fmt.height) {
        details.push(`Auflösung: ${fmt.width}x${fmt.height}`);
    }
    if (fmt.vcodec && fmt.vcodec !== 'none') {
        details.push(`Video: ${fmt.vcodec}`);
    }
    if (fmt.acodec && fmt.acodec !== 'none') {
        details.push(`Audio: ${fmt.acodec}`);
    }
    return details.join(', ') || 'Keine Details verfügbar';
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Sanitize filename
 */
function sanitizeFilename(filename) {
    return filename.replace(/[<>:"/\\|?*]/g, '_').substring(0, 100);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    const extractBtn = document.getElementById('extractBtn');
    const urlInput = document.getElementById('videoUrl');
    
    extractBtn.addEventListener('click', handleExtract);
    
    // Allow Enter key to submit
    urlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleExtract();
        }
    });
    
    // Check API health on load
    try {
        const health = await VideoAPI.checkHealth();
        console.log('API Status:', health);
    } catch (error) {
        console.warn('API health check failed:', error);
        showError('Backend API ist nicht erreichbar. Stellen Sie sicher, dass der Server läuft auf Port 8000.');
    }
});
