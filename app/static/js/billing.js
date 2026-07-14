document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Add Payment Method
    // ============================================
    
    window.addPaymentMethod = function() {
        // In production, use Stripe Elements or Stripe Checkout
        showToast('Payment method form coming soon', 'info');
    };
    
    // ============================================
    // Set Default Payment Method
    // ============================================
    
    window.setDefault = function(paymentMethodId) {
        fetch('/api/v1/billing/payment-methods/default', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ payment_method_id: paymentMethodId })
        })
        .then(response => response.json())
        .then(() => {
            showToast('Default payment method updated!', 'success');
            setTimeout(() => {
                location.reload();
            }, 500);
        })
        .catch(() => {
            showToast('Failed to update default', 'error');
        });
    };
    
    // ============================================
    // Remove Payment Method
    // ============================================
    
    window.removePaymentMethod = function(paymentMethodId) {
        if (!confirm('Remove this payment method?')) {
            return;
        }
        
        fetch('/api/v1/billing/payment-methods/remove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ payment_method_id: paymentMethodId })
        })
        .then(response => response.json())
        .then(() => {
            showToast('Payment method removed', 'info');
            setTimeout(() => {
                location.reload();
            }, 500);
        })
        .catch(() => {
            showToast('Failed to remove payment method', 'error');
        });
    };
});
