document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Contact Form
    // ============================================
    
    const form = document.getElementById('contactForm');
    const submitBtn = document.getElementById('contactSubmit');
    const successMessage = document.getElementById('contactSuccess');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validate form
            if (!validateForm()) {
                return;
            }
            
            // Show loading state
            const text = submitBtn.querySelector('.contact-submit-text');
            const loading = submitBtn.querySelector('.contact-submit-loading');
            const icon = submitBtn.querySelector('svg');
            
            text.style.display = 'none';
            loading.style.display = 'inline-flex';
            icon.style.display = 'none';
            submitBtn.disabled = true;
            
            // Simulate form submission
            setTimeout(function() {
                // Hide form
                form.querySelectorAll('.contact-form-group').forEach(function(group) {
                    group.style.display = 'none';
                });
                submitBtn.style.display = 'none';
                
                // Show success
                successMessage.classList.add('visible');
                successMessage.style.display = 'block';
            }, 2000);
        });
    }
    
    // ============================================
    // Form Validation
    // ============================================
    
    function validateForm() {
        let isValid = true;
        
        // Name
        const name = document.getElementById('contactName');
        if (!name.value.trim()) {
            name.classList.add('error');
            isValid = false;
        } else {
            name.classList.remove('error');
        }
        
        // Email
        const email = document.getElementById('contactEmail');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.value.trim())) {
            email.classList.add('error');
            isValid = false;
        } else {
            email.classList.remove('error');
        }
        
        // Subject
        const subject = document.getElementById('contactSubject');
        if (!subject.value.trim()) {
            subject.classList.add('error');
            isValid = false;
        } else {
            subject.classList.remove('error');
        }
        
        // Message
        const message = document.getElementById('contactMessage');
        if (!message.value.trim()) {
            message.classList.add('error');
            isValid = false;
        } else {
            message.classList.remove('error');
        }
        
        return isValid;
    }
    
    // Real-time validation
    document.querySelectorAll('.contact-form-input, .contact-form-textarea').forEach(function(input) {
        input.addEventListener('blur', function() {
            if (this.value.trim()) {
                this.classList.remove('error');
            }
        });
        
        input.addEventListener('input', function() {
            if (this.value.trim()) {
                this.classList.remove('error');
            }
        });
    });
    
    // ============================================
    // FAQ Accordion
    // ============================================
    
    document.querySelectorAll('.contact-faq-question').forEach(function(button) {
        button.addEventListener('click', function() {
            const item = this.closest('.contact-faq-item');
            const isActive = item.classList.contains('active');
            
            // Close other items
            document.querySelectorAll('.contact-faq-item').forEach(function(other) {
                if (other !== item) {
                    other.classList.remove('active');
                }
            });
            
            if (isActive) {
                item.classList.remove('active');
            } else {
                item.classList.add('active');
            }
        });
    });
    
    // ============================================
    // Keyboard Navigation
    // ============================================
    
    document.querySelectorAll('.contact-faq-question').forEach(function(button) {
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
});
