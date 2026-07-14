document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Refresh Reviews
    // ============================================
    
    window.refreshReviews = function() {
        const btn = event.currentTarget;
        const originalText = btn.innerHTML;
        
        btn.innerHTML = 'Refreshing...';
        btn.disabled = true;
        
        const appId = window.location.pathname.split('/')[2];
        
        fetch(`/api/v1/reviews/${appId}/refresh`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            showToast('Reviews refreshed!', 'success');
            setTimeout(() => {
                location.reload();
            }, 1000);
        })
        .catch(() => {
            showToast('Failed to refresh reviews', 'error');
            btn.innerHTML = originalText;
            btn.disabled = false;
        });
    };
    
    // ============================================
    // Open Response
    // ============================================
    
    window.openResponse = function(reviewId) {
        fetch(`/api/v1/reviews/${reviewId}/response-draft`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            if (data.draft) {
                // Show response modal
                showResponseModal(data);
            } else {
                showToast('Could not generate response draft', 'error');
            }
        })
        .catch(() => {
            showToast('Error generating response', 'error');
        });
    };
    
    // ============================================
    // Response Modal
    // ============================================
    
    function showResponseModal(data) {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay active';
        modal.innerHTML = `
            <div class="modal response-modal">
                <div class="modal-header">
                    <h3 class="modal-title">Respond to Review</h3>
                    <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="response-review">
                        <div class="response-rating">${'⭐'.repeat(data.rating)}</div>
                        <div class="response-sentiment ${data.sentiment}">${data.sentiment}</div>
                    </div>
                    <div class="response-draft-container">
                        <label class="response-draft-label">Draft Response</label>
                        <textarea class="response-draft-textarea" id="responseDraft" rows="4">${data.draft}</textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn-secondary" onclick="this.closest('.modal-overlay').remove()">Cancel</button>
                    <button class="btn-primary" onclick="sendResponse('${data.review_id}')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
                        </svg>
                        Send Response
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }
    
    // ============================================
    // Send Response
    // ============================================
    
    window.sendResponse = function(reviewId) {
        const draft = document.getElementById('responseDraft');
        if (!draft) return;
        
        const btn = event.currentTarget;
        const originalText = btn.innerHTML;
        
        btn.innerHTML = 'Sending...';
        btn.disabled = true;
        
        fetch(`/api/v1/reviews/${reviewId}/respond`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ response: draft.value })
        })
        .then(response => response.json())
        .then(() => {
            showToast('Response sent!', 'success');
            setTimeout(() => {
                location.reload();
            }, 1000);
        })
        .catch(() => {
            showToast('Failed to send response', 'error');
            btn.innerHTML = originalText;
            btn.disabled = false;
        });
    };
    
    // ============================================
    // Bookmark Review
    // ============================================
    
    window.bookmarkReview = function(reviewId) {
        fetch(`/api/v1/reviews/${reviewId}/bookmark`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            showToast('Bookmark toggled', 'info');
            setTimeout(() => {
                location.reload();
            }, 500);
        })
        .catch(() => {
            showToast('Failed to bookmark', 'error');
        });
    };
});
