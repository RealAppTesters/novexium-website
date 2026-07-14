document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Generate Report
    // ============================================
    
    window.generateReport = function(reportId) {
        const btn = event.currentTarget;
        const originalText = btn.textContent;
        
        btn.textContent = 'Generating...';
        btn.disabled = true;
        
        fetch(`/api/v1/reports/${reportId}/generate`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            showToast('Report generated!', 'success');
            setTimeout(() => {
                location.reload();
            }, 1000);
        })
        .catch(() => {
            showToast('Failed to generate report', 'error');
            btn.textContent = originalText;
            btn.disabled = false;
        });
    };
    
    // ============================================
    // Download Report
    // ============================================
    
    window.downloadReport = function(reportId) {
        showToast('Downloading report...', 'info');
        
        window.open(`/api/v1/reports/${reportId}/export/pdf`, '_blank');
    };
    
    // ============================================
    // Share Report
    // ============================================
    
    window.shareReport = function(reportId) {
        fetch(`/api/v1/reports/${reportId}/share`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                expires_in_days: 7,
                max_views: 10
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.url) {
                const fullUrl = window.location.origin + data.url;
                navigator.clipboard.writeText(fullUrl);
                showToast('Share link copied to clipboard!', 'success');
            }
        })
        .catch(() => {
            showToast('Failed to share report', 'error');
        });
    };
    
    // ============================================
    // Toggle Favorite
    // ============================================
    
    window.toggleFavorite = function(reportId) {
        fetch(`/api/v1/reports/${reportId}/favorite`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            setTimeout(() => {
                location.reload();
            }, 500);
        })
        .catch(() => {
            showToast('Failed to update favorite', 'error');
        });
    };
});
