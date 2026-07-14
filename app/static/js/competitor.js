document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Discover Competitors
    // ============================================
    
    window.discoverCompetitors = function() {
        const btn = event.currentTarget;
        const originalText = btn.textContent;
        
        btn.textContent = 'Discovering...';
        btn.disabled = true;
        
        const appId = window.location.pathname.split('/')[2];
        
        fetch(`/api/v1/competitors/${appId}/discover`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            showToast('Competitors discovered!', 'success');
            setTimeout(() => {
                location.reload();
            }, 1000);
        })
        .catch(() => {
            showToast('Failed to discover competitors', 'error');
            btn.textContent = originalText;
            btn.disabled = false;
        });
    };
    
    // ============================================
    // Refresh Competitors
    // ============================================
    
    window.refreshCompetitors = function() {
        const btn = event.currentTarget;
        const originalText = btn.innerHTML;
        
        btn.innerHTML = 'Refreshing...';
        btn.disabled = true;
        
        const appId = window.location.pathname.split('/')[2];
        
        fetch(`/api/v1/competitors/${appId}/refresh`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            showToast('Competitors refreshed!', 'success');
            setTimeout(() => {
                location.reload();
            }, 1000);
        })
        .catch(() => {
            showToast('Failed to refresh competitors', 'error');
            btn.innerHTML = originalText;
            btn.disabled = false;
        });
    };
    
    // ============================================
    // Toggle Pin
    // ============================================
    
    window.togglePin = function(competitorId) {
        fetch(`/api/v1/competitors/${competitorId}/pin`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            showToast('Watchlist updated!', 'success');
            setTimeout(() => {
                location.reload();
            }, 500);
        })
        .catch(() => {
            showToast('Failed to update watchlist', 'error');
        });
    };
    
    // ============================================
    // Remove Competitor
    // ============================================
    
    window.removeCompetitor = function(competitorId) {
        if (!confirm('Remove this competitor from tracking?')) {
            return;
        }
        
        fetch(`/api/v1/competitors/${competitorId}/remove`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            showToast('Competitor removed', 'info');
            setTimeout(() => {
                location.reload();
            }, 500);
        })
        .catch(() => {
            showToast('Failed to remove competitor', 'error');
        });
    };
    
    // ============================================
    // View Competitor
    // ============================================
    
    window.viewCompetitor = function(competitorId) {
        window.location.href = `/apps/${window.location.pathname.split('/')[2]}/competitors/${competitorId}`;
    };
    
    // ============================================
    // Compare
    // ============================================
    
    window.compareCompetitors = function() {
        window.location.href = `/apps/${window.location.pathname.split('/')[2]}/competitors/comparison`;
    };
    
    window.compareWith = function(competitorId) {
        window.location.href = `/apps/${window.location.pathname.split('/')[2]}/competitors/comparison?competitor=${competitorId}`;
    };
});
