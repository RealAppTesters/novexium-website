document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Country / Language Switchers
    // ============================================
    
    document.getElementById('countrySelect').addEventListener('change', function() {
        const country = this.value;
        const language = document.getElementById('languageSelect').value;
        reloadPage(country, language);
    });
    
    document.getElementById('languageSelect').addEventListener('change', function() {
        const country = document.getElementById('countrySelect').value;
        const language = this.value;
        reloadPage(country, language);
    });
    
    function reloadPage(country, language) {
        const appId = window.location.pathname.split('/')[2];
        window.location.href = `/apps/${appId}/rank?country=${country}&language=${language}`;
    }
    
    // ============================================
    // Refresh Rankings
    // ============================================
    
    window.refreshRankings = function() {
        const btn = event.currentTarget;
        const originalText = btn.innerHTML;
        
        btn.innerHTML = 'Refreshing...';
        btn.disabled = true;
        
        const appId = window.location.pathname.split('/')[2];
        const country = document.getElementById('countrySelect').value;
        const language = document.getElementById('languageSelect').value;
        
        fetch(`/api/v1/rank/${appId}/refresh?country=${country}&language=${language}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            showToast('Rankings refreshed!', 'success');
            setTimeout(() => {
                location.reload();
            }, 1000);
        })
        .catch(() => {
            showToast('Failed to refresh rankings', 'error');
            btn.innerHTML = originalText;
            btn.disabled = false;
        });
    };
    
    // ============================================
    // Favorite Toggle
    // ============================================
    
    window.toggleFavorite = function(rankId) {
        fetch(`/api/v1/rank/${rankId}/favorite`, {
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
    
    // ============================================
    // View History
    // ============================================
    
    window.viewHistory = function(keyword) {
        const appId = window.location.pathname.split('/')[2];
        const country = document.getElementById('countrySelect').value;
        const language = document.getElementById('languageSelect').value;
        
        window.location.href = `/apps/${appId}/rank/history?keyword=${encodeURIComponent(keyword)}&country=${country}&language=${language}`;
    };
    
    // ============================================
    // Acknowledge Alert
    // ============================================
    
    window.acknowledgeAlert = function(alertId) {
        fetch(`/api/v1/rank/alerts/${alertId}/acknowledge`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            showToast('Alert acknowledged', 'info');
            setTimeout(() => {
                location.reload();
            }, 500);
        })
        .catch(() => {
            showToast('Failed to acknowledge alert', 'error');
        });
    };
    
    // ============================================
    // Start Tracking
    // ============================================
    
    window.startTracking = function() {
        const appId = window.location.pathname.split('/')[2];
        window.location.href = `/apps/${appId}/keywords/explorer`;
    };
});
