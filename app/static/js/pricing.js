document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Pricing Card Interactions
    // ============================================
    
    // Hover effects for pricing cards
    document.querySelectorAll('.pricing-card').forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            // Add subtle glow effect
            this.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
        });
    });
    
    // ============================================
    // Plan Comparison - Toggle
    // ============================================
    
    // Optional: Add toggle for monthly/annual (future)
    // const toggle = document.getElementById('billingToggle');
    // if (toggle) { ... }
    
    // ============================================
    // FAQ Accordion
    // ============================================
    
    document.querySelectorAll('.pricing-faq-question').forEach(function(button) {
        button.addEventListener('click', function() {
            const item = this.closest('.pricing-faq-item');
            const isActive = item.classList.contains('active');
            
            // Close other items
            document.querySelectorAll('.pricing-faq-item').forEach(function(other) {
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
    // Smooth Scroll for Pricing Anchor
    // ============================================
    
    // If URL has #pricing, scroll to pricing cards
    if (window.location.hash === '#pricing') {
        setTimeout(function() {
            const pricingSection = document.querySelector('.pricing-cards');
            if (pricingSection) {
                pricingSection.scrollIntoView({ behavior: 'smooth' });
            }
        }, 300);
    }
    
    // ============================================
    // Keyboard Navigation
    // ============================================
    
    // Enter/Space to toggle FAQ
    document.querySelectorAll('.pricing-faq-question').forEach(function(button) {
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
    
    // ============================================
    // Analytics Tracking (Placeholder)
    // ============================================
    
    // Track pricing card clicks
    document.querySelectorAll('.pricing-card .btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const card = this.closest('.pricing-card');
            const plan = card?.querySelector('.pricing-card-name')?.textContent || 'Unknown';
            
            // Track event (replace with actual analytics)
            console.log(`Pricing: ${plan} plan selected`);
            
            // Example: gtag('event', 'select_plan', { plan: plan });
        });
    });
    
    // ============================================
    // Testimonial Carousel (Optional)
    // ============================================
    
    // If testimonials should be carousel, add logic here
    // For now, they're displayed as a grid
});
