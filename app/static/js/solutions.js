document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Hero Mockup Audience Toggle
    // ============================================
    
    document.querySelectorAll('.solutions-mockup-audience-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const audience = this.dataset.audience;
            
            // Update active button
            document.querySelectorAll('.solutions-mockup-audience-btn').forEach(function(b) {
                b.classList.remove('active');
            });
            this.classList.add('active');
            
            // Update view
            document.querySelectorAll('.solutions-mockup-view').forEach(function(view) {
                view.style.display = 'none';
            });
            document.querySelector(`.solutions-mockup-view[data-view="${audience}"]`).style.display = 'block';
        });
    });
    
    // ============================================
    // Journey Tabs
    // ============================================
    
    document.querySelectorAll('.solutions-journeys-tab').forEach(function(tab) {
        tab.addEventListener('click', function() {
            const journey = this.dataset.journey;
            
            // Update active tab
            document.querySelectorAll('.solutions-journeys-tab').forEach(function(t) {
                t.classList.remove('active');
            });
            this.classList.add('active');
            
            // Update journey content
            document.querySelectorAll('.solutions-journey').forEach(function(j) {
                j.style.display = 'none';
            });
            document.querySelector(`.solutions-journey[data-journey="${journey}"]`).style.display = 'block';
        });
    });
    
    // ============================================
    // Feature Matching
    // ============================================
    
    document.querySelectorAll('.solutions-matching-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const audience = this.dataset.audience;
            
            // Update active button
            document.querySelectorAll('.solutions-matching-btn').forEach(function(b) {
                b.classList.remove('active');
            });
            this.classList.add('active');
            
            // Highlight relevant features
            document.querySelectorAll('.solutions-matching-indicator').forEach(function(indicator) {
                if (indicator.dataset.audience === audience) {
                    if (indicator.textContent === '✓') {
                        indicator.style.opacity = '1';
                    } else {
                        indicator.style.opacity = '0.3';
                    }
                }
            });
        });
    });
    
    // ============================================
    // FAQ Accordion
    // ============================================
    
    document.querySelectorAll('.solutions-faq-question').forEach(function(button) {
        button.addEventListener('click', function() {
            const item = this.closest('.solutions-faq-item');
            const isActive = item.classList.contains('active');
            
            // Close other items
            document.querySelectorAll('.solutions-faq-item').forEach(function(other) {
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
    
    document.querySelectorAll('.solutions-faq-question').forEach(function(button) {
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
    
    // ============================================
    // Smooth Scroll for Audience Cards
    // ============================================
    
    document.querySelectorAll('.solutions-audience-cta').forEach(function(link) {
        link.addEventListener('click', function(e) {
            // Track clicks on audience CTAs
            const card = this.closest('.solutions-audience-card');
            const audience = card?.querySelector('.solutions-audience-badge')?.textContent || 'Unknown';
            console.log(`Solutions: ${audience} audience explored`);
        });
    });
});
