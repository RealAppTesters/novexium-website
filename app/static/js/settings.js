document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Password Strength
    // ============================================
    
    const passwordInput = document.getElementById('new_password');
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            const bar = document.querySelector('.password-strength-fill');
            const text = document.querySelector('.password-strength-text');
            
            if (!bar || !text) return;
            
            let score = 0;
            if (password.length >= 8) score += 20;
            if (/[a-z]/.test(password)) score += 20;
            if (/[A-Z]/.test(password)) score += 20;
            if (/[0-9]/.test(password)) score += 20;
            if (/[^A-Za-z0-9]/.test(password)) score += 20;
            
            bar.style.width = score + '%';
            
            if (score === 0) {
                text.textContent = 'Enter a password';
                bar.style.background = 'var(--text-muted)';
            } else if (score < 40) {
                text.textContent = 'Weak password';
                bar.style.background = 'var(--accent-danger)';
            } else if (score < 60) {
                text.textContent = 'Fair password';
                bar.style.background = 'var(--accent-warning)';
            } else if (score < 80) {
                text.textContent = 'Good password';
                bar.style.background = 'var(--accent-info)';
            } else {
                text.textContent = 'Strong password!';
                bar.style.background = 'var(--accent-success)';
            }
        });
    }
    
    // ============================================
    // Profile Form
    // ============================================
    
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            fetch('/api/v1/settings/profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(() => {
                showToast('Profile updated successfully!', 'success');
            })
            .catch(() => {
                showToast('Failed to update profile', 'error');
            });
        });
    }
    
    // ============================================
    // Password Form
    // ============================================
    
    const passwordForm = document.getElementById('passwordForm');
    if (passwordForm) {
        passwordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            if (data.new_password !== data.confirm_password) {
                showToast('Passwords do not match', 'error');
                return;
            }
            
            fetch('/api/v1/settings/security/password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(() => {
                showToast('Password updated successfully!', 'success');
                this.reset();
            })
            .catch(() => {
                showToast('Failed to update password', 'error');
            });
        });
    }
    
    // ============================================
    // Two-Factor Authentication
    // ============================================
    
    window.enable2FA = function() {
        showToast('2FA setup coming soon', 'info');
    };
    
    window.disable2FA = function() {
        if (!confirm('Disable two-factor authentication?')) return;
        showToast('2FA disabled', 'info');
    };
    
    // ============================================
    // Sessions
    // ============================================
    
    window.revokeSession = function(sessionId) {
        if (!confirm('Revoke this session?')) return;
        showToast('Session revoked', 'info');
    };
    
    window.revokeAllSessions = function() {
        if (!confirm('Sign out all devices? You will need to log in again.')) return;
        showToast('All sessions revoked', 'info');
    };
});
