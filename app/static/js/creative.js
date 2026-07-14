document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Refresh Assets
    // ============================================
    
    window.refreshAssets = function() {
        const btn = event.currentTarget;
        const originalText = btn.innerHTML;
        
        btn.innerHTML = 'Refreshing...';
        btn.disabled = true;
        
        const appId = window.location.pathname.split('/')[2];
        
        fetch(`/api/v1/creative/${appId}/refresh`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            showToast('Assets refreshed successfully!', 'success');
            setTimeout(() => {
                location.reload();
            }, 1000);
        })
        .catch(() => {
            showToast('Failed to refresh assets', 'error');
            btn.innerHTML = originalText;
            btn.disabled = false;
        });
    };
    
    // ============================================
    // View Asset
    // ============================================
    
    window.viewAsset = function(assetId) {
        // Navigate to asset detail
        window.location.href = `/creative/assets/${assetId}`;
    };
    
    // ============================================
    // Image Load Fallback
    // ============================================
    
    document.querySelectorAll('.asset-preview img').forEach(function(img) {
        img.addEventListener('error', function() {
            this.src = "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100'><rect width='100' height='100' fill='%23111113'/><text x='50' y='55' text-anchor='middle' fill='%2371717A' font-size='14'>No Image</text></svg>";
        });
    });
});
