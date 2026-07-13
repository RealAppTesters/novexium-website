// ============================================
// Auth Form Handling
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Password toggle
    document.querySelectorAll('.password-toggle').forEach(function(button) {
        button.addEventListener('click', function() {
            const input = this.closest('.password-input-wrapper').querySelector('input');
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            
            // Toggle icon
            const eye = this.querySelector('.password-eye');
            if (type === 'text') {
                eye.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>';
            } else {
                eye.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
            }
        });
    });
    
    // Form loading states
    document.querySelectorAll('.auth-form').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const button = this.querySelector('button[type="submit"]');
            if (button) {
                button.classList.add('btn-loading');
                button.disabled = true;
                const originalText = button.textContent.trim();
                button.innerHTML = 'Processing...';
                
                // Re-enable after 5 seconds (fallback)
                setTimeout(function() {
                    button.classList.remove('btn-loading');
                    button.disabled = false;
                    button.textContent = originalText;
                }, 5000);
            }
        });
    });
    
    // Auto-dismiss flash messages
    document.querySelectorAll('.flash').forEach(function(flash) {
        setTimeout(function() {
            flash.classList.add('flash-dismissing');
            setTimeout(function() {
                flash.remove();
            }, 300);
        }, 5000);
    });
});

// ============================================
// Form Validation
// ============================================

// Email validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Password validation
function validatePassword(password) {
    const requirements = {
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[^A-Za-z0-9]/.test(password)
    };
    
    return requirements;
}

// Real-time validation on inputs
document.querySelectorAll('input[required]').forEach(function(input) {
    input.addEventListener('blur', function() {
        if (this.value.trim() === '') {
            this.classList.add('input-error');
        } else {
            this.classList.remove('input-error');
        }
    });
    
    input.addEventListener('input', function() {
        if (this.value.trim() !== '') {
            this.classList.remove('input-error');
        }
    });
});
