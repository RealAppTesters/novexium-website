document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Track Keyword
    // ============================================
    
    window.trackKeyword = function(appId, keywordId) {
        const btn = event.currentTarget;
        const originalText = btn.textContent;
        
        btn.textContent = 'Tracking...';
        btn.disabled = true;
        
        fetch(`/api/v1/keywords/${appId}/track`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ keyword_id: keywordId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'tracking_started' || data.status === 'already_tracking') {
                btn.textContent = '✓ Tracked';
                btn.classList.add('tracked');
                showToast('Keyword tracking started!', 'success');
            } else {
                btn.textContent = originalText;
                btn.disabled = false;
                showToast('Failed to track keyword', 'error');
            }
        })
        .catch(error => {
            btn.textContent = originalText;
            btn.disabled = false;
            showToast('Error tracking keyword', 'error');
        });
    };
    
    // ============================================
    // Sort Filter
    // ============================================
    
    document.querySelectorAll('.explorer-filter').forEach(function(select) {
        select.addEventListener('change', function() {
            const form = this.closest('.explorer-search-form');
            if (form) {
                form.submit();
            }
        });
    });
    
    // ============================================
    // Quick Win Tracking
    // ============================================
    
    document.querySelectorAll('.quick-win-track').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const appId = this.dataset.appId;
            const keywordId = this.dataset.keywordId;
            trackKeyword(appId, keywordId);
        });
    });
});
