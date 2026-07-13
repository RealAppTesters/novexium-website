// ============================================
// Connect App Flow
// ============================================

let currentStep = 1;
let appData = {};
let loadingInterval = null;

// Open Connect Modal
function openConnectModal() {
    const modal = document.getElementById('connectModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    document.getElementById('connectStep1').style.display = 'block';
    document.getElementById('connectLoading').style.display = 'none';
    document.getElementById('connectPreview').style.display = 'none';
    document.getElementById('connectAnalysis').style.display = 'none';
    document.getElementById('storeUrl').focus();
}

// Close Connect Modal
function closeConnectModal() {
    const modal = document.getElementById('connectModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
    clearInterval(loadingInterval);
}

// Clear URL
function clearUrl() {
    document.getElementById('storeUrl').value = '';
    document.getElementById('storeUrl').focus();
    document.getElementById('connect-input-clear').style.display = 'none';
    document.getElementById('urlError').style.display = 'none';
}

// Set Example URL
function setExampleUrl(type) {
    const url = type === 'google' 
        ? 'https://play.google.com/store/apps/details?id=com.example.app'
        : 'https://apps.apple.com/us/app/example-app/id123456789';
    document.getElementById('storeUrl').value = url;
    document.getElementById('connect-input-clear').style.display = 'block';
}

// URL Validation
document.getElementById('storeUrl').addEventListener('input', function() {
    const value = this.value;
    if (value) {
        document.getElementById('connect-input-clear').style.display = 'block';
    } else {
        document.getElementById('connect-input-clear').style.display = 'none';
    }
    document.getElementById('urlError').style.display = 'none';
});

// ============================================
// Step 2: Fetch App Information
// ============================================

function fetchAppData(event) {
    event.preventDefault();
    
    const url = document.getElementById('storeUrl').value.trim();
    
    // Validate URL
    if (!isValidStoreUrl(url)) {
        showUrlError('Please enter a valid App Store or Google Play URL');
        return;
    }
    
    // Show loading
    document.getElementById('connectStep1').style.display = 'none';
    document.getElementById('connectLoading').style.display = 'block';
    
    // Start loading animation
    startLoadingAnimation();
    
    // Simulate API call
    setTimeout(() => {
        // Mock app data
        appData = {
            app_name: 'My Example App',
            developer: 'Example Developer Inc.',
            store: url.includes('play.google.com') ? 'google_play' : 'app_store',
            category: 'Productivity',
            country: 'US',
            rating: 4.7,
            review_count: 1247,
            package_name: 'com.example.app',
            store_url: url,
            last_updated: '2024-01-15',
            description: 'This is a powerful app that helps users achieve their goals. With intuitive design and advanced features, it\'s the perfect tool for productivity.',
            screenshots: [
                'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="350"><rect width="200" height="350" fill="%234F46E5"/><text x="100" y="175" text-anchor="middle" fill="white" font-size="20">Screenshot 1</text></svg>',
                'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="350"><rect width="200" height="350" fill="%2322C55E"/><text x="100" y="175" text-anchor="middle" fill="white" font-size="20">Screenshot 2</text></svg>',
                'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="350"><rect width="200" height="350" fill="%23F59E0B"/><text x="100" y="175" text-anchor="middle" fill="white" font-size="20">Screenshot 3</text></svg>',
                'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="350"><rect width="200" height="350" fill="%23EF4444"/><text x="100" y="175" text-anchor="middle" fill="white" font-size="20">Screenshot 4</text></svg>',
                'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="350"><rect width="200" height="350" fill="%233B82F6"/><text x="100" y="175" text-anchor="middle" fill="white" font-size="20">Screenshot 5</text></svg>'
            ],
            icon_url: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64"><rect width="64" height="64" rx="16" fill="%234F46E5"/><text x="32" y="42" text-anchor="middle" fill="white" font-size="32" font-weight="bold">M</text></svg>'
        };
        
        // Stop loading
        clearInterval(loadingInterval);
        completeLoading();
        
        // Show preview
        setTimeout(() => {
            document.getElementById('connectLoading').style.display = 'none';
            document.getElementById('connectPreview').style.display = 'block';
            populatePreview(appData);
        }, 500);
    }, 3000);
}

function isValidStoreUrl(url) {
    return url.includes('play.google.com') || 
           url.includes('apps.apple.com') ||
           url.includes('itunes.apple.com');
}

function showUrlError(message) {
    const errorEl = document.getElementById('urlError');
    document.getElementById('errorMessage').textContent = message;
    errorEl.style.display = 'flex';
    document.getElementById('storeUrl').focus();
}

// ============================================
// Step 3: Premium Loading Experience
// ============================================

function startLoadingAnimation() {
    const steps = document.querySelectorAll('.connect-loading-step');
    const progressBar = document.querySelector('.connect-loading-progress-fill');
    const progressText = document.querySelector('.connect-loading-progress-text');
    let currentStep = 0;
    
    // Mark first step as active
    if (steps.length > 0) {
        steps[0].classList.add('active');
    }
    
    loadingInterval = setInterval(() => {
        if (currentStep < steps.length - 1) {
            // Complete current step
            steps[currentStep].classList.remove('active');
            steps[currentStep].classList.add('completed');
            
            // Activate next step
            currentStep++;
            steps[currentStep].classList.add('active');
            
            // Update progress
            const progress = ((currentStep + 1) / steps.length) * 100;
            progressBar.style.width = progress + '%';
            progressText.textContent = Math.round(progress) + '% complete';
        }
    }, 400);
}

function completeLoading() {
    const steps = document.querySelectorAll('.connect-loading-step');
    const progressBar = document.querySelector('.connect-loading-progress-fill');
    const progressText = document.querySelector('.connect-loading-progress-text');
    
    // Complete all steps
    steps.forEach(step => {
        step.classList.remove('active');
        step.classList.add('completed');
    });
    
    progressBar.style.width = '100%';
    progressText.textContent = '100% complete';
}

// ============================================
// Step 4: App Preview
// ============================================

function populatePreview(data) {
    // App info
    document.querySelector('.connect-preview-app-name').textContent = data.app_name;
    document.querySelector('.connect-preview-app-developer').textContent = data.developer;
    document.querySelector('.connect-preview-app-category').textContent = data.category;
    document.querySelector('.connect-preview-app-rating').textContent = `⭐ ${data.rating} (${data.review_count} reviews)`;
    
    // Platform badge
    const badge = document.querySelector('.connect-preview-platform-badge');
    badge.textContent = data.store === 'google_play' ? 'Google Play' : 'App Store';
    badge.className = `connect-preview-platform-badge ${data.store}`;
    
    // Details
    document.querySelector('.connect-preview-detail-value').textContent = data.package_name;
    document.querySelector('.connect-preview-detail-link').textContent = data.store_url;
    document.querySelector('.connect-preview-detail-link').href = data.store_url;
    
    // Description
    document.querySelector('.connect-preview-description-text').textContent = data.description;
    
    // Screenshots
    const grid = document.querySelector('.connect-preview-screenshots-grid');
    grid.innerHTML = '';
    data.screenshots.slice(0, 4).forEach((src, index) => {
        const div = document.createElement('div');
        div.className = 'connect-preview-screenshot';
        div.innerHTML = `<img src="${src}" alt="Screenshot ${index + 1}">`;
        grid.appendChild(div);
    });
    
    if (data.screenshots.length > 4) {
        const div = document.createElement('div');
        div.className = 'connect-preview-screenshot connect-preview-screenshot-more';
        div.textContent = `+${data.screenshots.length - 4}`;
        grid.appendChild(div);
    }
}

function goBackToConnect() {
    document.getElementById('connectPreview').style.display = 'none';
    document.getElementById('connectStep1').style.display = 'block';
}

// ============================================
// Step 5-6: Connect & Analyze
// ============================================

function connectApp() {
    // Show analysis loading
    document.getElementById('connectPreview').style.display = 'none';
    document.getElementById('connectAnalysis').style.display = 'block';
    
    // Start analysis animation
    startAnalysisAnimation();
    
    // Simulate analysis completion
    setTimeout(() => {
        // Close modal
        closeConnectModal();
        
        // Redirect to workspace
        window.location.href = '/apps/workspace';
    }, 4000);
}

function startAnalysisAnimation() {
    const items = document.querySelectorAll('.connect-analysis-item');
    const progressBar = document.querySelector('.connect-analysis-progress-fill');
    const progressText = document.querySelector('.connect-analysis-progress-text');
    let currentItem = 0;
    
    // Mark first item as active
    if (items.length > 0) {
        items[0].classList.add('active');
    }
    
    const analysisInterval = setInterval(() => {
        if (currentItem < items.length - 1) {
            // Complete current item
            items[currentItem].classList.remove('active');
            items[currentItem].classList.add('completed');
            
            // Activate next item
            currentItem++;
            items[currentItem].classList.add('active');
            
            // Update progress
            const progress = ((currentItem + 1) / items.length) * 100;
            progressBar.style.width = progress + '%';
            progressText.textContent = Math.round(progress) + '% complete';
        } else {
            clearInterval(analysisInterval);
            // Complete all
            items.forEach(item => {
                item.classList.remove('active');
                item.classList.add('completed');
            });
            progressBar.style.width = '100%';
            progressText.textContent = '100% complete';
        }
    }, 500);
}

// ============================================
// Step 7-13: Workspace Welcome
// ============================================

// This is rendered on the workspace page after redirect
// See workspace.html for implementation

// ============================================
// Keyboard Shortcuts
// ============================================

document.addEventListener('keydown', function(e) {
    // Escape to close modal
    if (e.key === 'Escape') {
        const modal = document.getElementById('connectModal');
        if (modal.classList.contains('active')) {
            closeConnectModal();
        }
    }
    
    // Enter to submit in modal
    if (e.key === 'Enter' && document.getElementById('connectModal').classList.contains('active')) {
        const form = document.getElementById('connectForm');
        if (form && document.getElementById('connectStep1').style.display !== 'none') {
            form.dispatchEvent(new Event('submit'));
        }
    }
});

// ============================================
// Initialize
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Auto-focus the URL input when modal opens
    document.querySelector('[data-open="connect"]')?.addEventListener('click', function() {
        setTimeout(() => {
            document.getElementById('storeUrl').focus();
        }, 300);
    });
});
