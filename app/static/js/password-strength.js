document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    if (!passwordInput) return;
    
    const strengthBar = document.querySelector('.password-strength-fill');
    const strengthText = document.querySelector('.password-strength-text');
    const requirements = document.querySelectorAll('.requirement');
    
    function checkPasswordStrength(password) {
        const requirementsMet = {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            lowercase: /[a-z]/.test(password),
            number: /[0-9]/.test(password),
            special: /[^A-Za-z0-9]/.test(password)
        };
        
        // Update requirements list
        requirements.forEach(function(req) {
            const reqType = req.dataset.requirement;
            if (requirementsMet[reqType]) {
                req.classList.add('met');
                req.innerHTML = req.innerHTML.replace('○', '✓');
            } else {
                req.classList.remove('met');
                req.innerHTML = req.innerHTML.replace('✓', '○');
            }
        });
        
        // Calculate score
        const metCount = Object.values(requirementsMet).filter(Boolean).length;
        const score = (metCount / 5) * 100;
        
        // Update strength bar
        strengthBar.style.width = score + '%';
        
        // Update strength text and color
        if (score === 0) {
            strengthText.textContent = 'Enter a strong password';
            strengthBar.style.background = '#71717A';
        } else if (score < 40) {
            strengthText.textContent = 'Weak password';
            strengthBar.style.background = '#EF4444';
        } else if (score < 60) {
            strengthText.textContent = 'Fair password';
            strengthBar.style.background = '#F59E0B';
        } else if (score < 80) {
            strengthText.textContent = 'Good password';
            strengthBar.style.background = '#3B82F6';
        } else {
            strengthText.textContent = 'Strong password!';
            strengthBar.style.background = '#22C55E';
        }
        
        return requirementsMet;
    }
    
    passwordInput.addEventListener('input', function() {
        checkPasswordStrength(this.value);
    });
});
