let currentVideoInfo = null;

async function handleExtract() {
    const urlInput = document.getElementById('videoUrl');
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('Bitte geben Sie eine URL ein');
        return;
    }
    
    try {
        showLoader('Video wird analysiert...');
        currentVideoInfo = await VideoAPI.extractVideo(url);
        displayVideoInfo(currentVideoInfo);
        hideLoader();
    } catch (error) {
        hideLoader();
        showError(error.message);
    }
}

function displayVideoInfo(info) {
    const container = document.getElementById('videoInfo');
    
    let html = `
        <div class="video-card">
            <img src="${info.thumbnail}" alt="${info.title}" class="thumbnail">
            <h2>${info.title}</h2>
            <p>Uploader: ${info.uploader || 'Unknown'}</p>
            <p>Duration: ${formatDuration(info.duration)}</p>
            <div class="formats">
                <h3>Verfügbare Formate:</h3>
                ${info.formats.map((fmt, idx) => `
                    <button class="quality-btn" onclick="downloadVideo(${idx})">
                        ${fmt.quality} - ${fmt.ext} ${fmt.filesize ? '(' + formatFilesize(fmt.filesize) + ')' : ''}
                    </button>
                `).join('')}
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}

function downloadVideo(formatIndex) {
    const format = currentVideoInfo.formats[formatIndex];
    window.open(format.url, '_blank');
}

function formatDuration(seconds) {
    if (!seconds) return 'Unknown';
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function formatFilesize(bytes) {
    return (bytes / 1024 / 1024).toFixed(2) + ' MB';
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('extractBtn').addEventListener('click', handleExtract);
});
