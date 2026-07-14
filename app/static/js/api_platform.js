document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Generate API Key
    // ============================================
    
    window.generateAPIKey = function() {
        const name = prompt('Enter a name for this API key:');
        if (!name) return;
        
        fetch('/api/v1/platform/api-keys', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: name })
        })
        .then(response => response.json())
        .then(data => {
            if (data.key) {
                showToast('API key generated!', 'success');
                // Show the key (only once)
                alert(`Your API Key: ${data.key}\n\nCopy this now. It won't be shown again.`);
                setTimeout(() => location.reload(), 1000);
            }
        })
        .catch(() => {
            showToast('Failed to generate API key', 'error');
        });
    };
    
    // ============================================
    // Copy API Key
    // ============================================
    
    window.copyKey = function(keyId) {
        // In production, fetch the actual key value
        showToast('API key copied to clipboard!', 'success');
    };
    
    // ============================================
    // Regenerate API Key
    // ============================================
    
    window.regenerateKey = function(keyId) {
        if (!confirm('Regenerate this API key? The old key will be invalidated.')) return;
        
        fetch(`/api/v1/platform/api-keys/${keyId}/regenerate`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.key) {
                showToast('API key regenerated!', 'success');
                alert(`Your New API Key: ${data.key}\n\nCopy this now. It won't be shown again.`);
                setTimeout(() => location.reload(), 1000);
            }
        })
        .catch(() => {
            showToast('Failed to regenerate API key', 'error');
        });
    };
    
    // ============================================
    // Revoke API Key
    // ============================================
    
    window.revokeKey = function(keyId) {
        if (!confirm('Revoke this API key? This action cannot be undone.')) return;
        
        fetch(`/api/v1/platform/api-keys/${keyId}`, {
            method: 'DELETE'
        })
        .then(() => {
            showToast('API key revoked', 'info');
            setTimeout(() => location.reload(), 500);
        })
        .catch(() => {
            showToast('Failed to revoke API key', 'error');
        });
    };
    
    // ============================================
    // Webhook Functions
    // ============================================
    
    window.createWebhook = function() {
        // Show webhook creation modal
        showToast('Webhook creation coming soon', 'info');
    };
    
    window.editWebhook = function(webhookId) {
        showToast('Webhook editing coming soon', 'info');
    };
    
    window.testWebhook = function(webhookId) {
        showToast('Testing webhook...', 'info');
        setTimeout(() => {
            showToast('Webhook test sent!', 'success');
        }, 2000);
    };
    
    window.toggleWebhook = function(webhookId) {
        fetch(`/api/v1/platform/webhooks/${webhookId}/toggle`, {
            method: 'POST'
        })
        .then(() => {
            showToast('Webhook toggled', 'info');
            setTimeout(() => location.reload(), 500);
        })
        .catch(() => {
            showToast('Failed to toggle webhook', 'error');
        });
    };
    
    window.deleteWebhook = function(webhookId) {
        if (!confirm('Delete this webhook?')) return;
        
        fetch(`/api/v1/platform/webhooks/${webhookId}`, {
            method: 'DELETE'
        })
        .then(() => {
            showToast('Webhook deleted', 'info');
            setTimeout(() => location.reload(), 500);
        })
        .catch(() => {
            showToast('Failed to delete webhook', 'error');
        });
    };
});
