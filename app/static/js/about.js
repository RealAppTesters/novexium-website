document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // FAQ Accordion
    // ============================================
    
    document.querySelectorAll('.about-faq-question').forEach(function(button) {
        button.addEventListener('click', function() {
            const item = this.closest('.about-faq-item');
            const isActive = item.classList.contains('active');
            
            // Close other items
            document.querySelectorAll('.about-faq-item').forEach(function(other) {
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
    
    document.querySelectorAll('.about-faq-question').forEach(function(button) {
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
    
    // ============================================
    // Intersection Observer for Animations
    // ============================================
    
    if ('IntersectionObserver' in window) {
        const cards = document.querySelectorAll('.about-belief-card, .about-audience-card, .about-trust-card');
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1
        });
        
        cards.forEach(function(card) {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(card);
        });
    }
});
