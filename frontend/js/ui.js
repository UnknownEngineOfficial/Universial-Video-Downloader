/**
 * UI Helper Functions
 */

/**
 * Show loader with message
 */
function showLoader(message = 'Laden...') {
    const loader = document.getElementById('loader');
    const loaderText = document.getElementById('loaderText');
    loaderText.textContent = message;
    loader.style.display = 'block';
}

/**
 * Hide loader
 */
function hideLoader() {
    const loader = document.getElementById('loader');
    loader.style.display = 'none';
}

/**
 * Show error message
 */
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

/**
 * Hide error message
 */
function hideError() {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.style.display = 'none';
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.style.display = 'block';
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

/**
 * Clear video info display
 */
function clearVideoInfo() {
    const container = document.getElementById('videoInfo');
    container.innerHTML = '';
    hideError();
}