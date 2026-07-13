document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Search Functionality
    // ============================================
    
    const searchInput = document.getElementById('resourcesSearch');
    const grid = document.getElementById('resourcesGrid');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            if (query.length > 0) {
                // Perform search
                filterResources(query);
            } else {
                // Show all
                resetFilters();
            }
        });
    }
    
    // ============================================
    // Category Filters
    // ============================================
    
    document.querySelectorAll('.resources-category-filter').forEach(function(filter) {
        filter.addEventListener('click', function() {
            const category = this.dataset.category;
            
            // Update active state
            document.querySelectorAll('.resources-category-filter').forEach(function(f) {
                f.classList.remove('active');
            });
            this.classList.add('active');
            
            // Filter resources
            filterResourcesByCategory(category);
        });
    });
    
    // ============================================
    // Filter Functions
    // ============================================
    
    const allResources = [
        { title: 'The Complete ASO Guide', category: 'getting-started', type: 'guide' },
        { title: 'Google Play Optimization Checklist', category: 'checklists', type: 'checklist' },
        { title: 'App Store Optimization Checklist', category: 'checklists', type: 'checklist' },
        { title: 'Keyword Research Guide', category: 'keywords', type: 'guide' },
        { title: 'Screenshot Best Practices', category: 'creatives', type: 'guide' },
        { title: 'App Icon Best Practices', category: 'creatives', type: 'guide' },
        { title: 'Review Management Guide', category: 'reviews', type: 'guide' },
        { title: 'Competitor Analysis Guide', category: 'competitors', type: 'guide' },
        { title: 'Store Listing Optimization Guide', category: 'store-listings', type: 'guide' },
        { title: 'Release Notes Best Practices', category: 'growth', type: 'guide' },
    ];
    
    function filterResources(query) {
        const filtered = allResources.filter(function(resource) {
            return resource.title.toLowerCase().includes(query);
        });
        renderResources(filtered);
    }
    
    function filterResourcesByCategory(category) {
        if (category === 'all') {
            renderResources(allResources);
        } else {
            const filtered = allResources.filter(function(resource) {
                return resource.category === category;
            });
            renderResources(filtered);
        }
    }
    
    function resetFilters() {
        renderResources(allResources);
        document.querySelectorAll('.resources-category-filter').forEach(function(f) {
            f.classList.remove('active');
        });
        document.querySelector('.resources-category-filter[data-category="all"]').classList.add('active');
    }
    
    function renderResources(resources) {
        if (!grid) return;
        
        if (resources.length === 0) {
            grid.innerHTML = `
                <div class="resources-empty">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <circle cx="11" cy="11" r="8"/>
                        <path d="M21 21L17 17"/>
                    </svg>
                    <h4>No resources found</h4>
                    <p>Try adjusting your search or filter</p>
                </div>
            `;
            return;
        }
        
        grid.innerHTML = resources.map(function(resource) {
            return `
                <div class="resources-category-card">
                    <div class="resources-category-card-meta">
                        <span class="resources-category-card-category">${resource.category}</span>
                        <span class="resources-category-card-type">${resource.type}</span>
                    </div>
                    <h4 class="resources-category-card-title">${resource.title}</h4>
                    <a href="/resources/${resource.type}s/${resource.title.toLowerCase().replace(/ /g, '-')}" class="resources-category-card-btn">Read Guide →</a>
                </div>
            `;
        }).join('');
    }
    
    // ============================================
    // FAQ Accordion
    // ============================================
    
    document.querySelectorAll('.resources-faq-question').forEach(function(button) {
        button.addEventListener('click', function() {
            const item = this.closest('.resources-faq-item');
            const isActive = item.classList.contains('active');
            
            // Close other items
            document.querySelectorAll('.resources-faq-item').forEach(function(other) {
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
    
    // Ctrl+K or Cmd+K for search focus
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const search = document.getElementById('resourcesSearch');
            if (search) {
                search.focus();
            }
        }
        
        // Escape to blur search
        if (e.key === 'Escape') {
            const search = document.getElementById('resourcesSearch');
            if (search && document.activeElement === search) {
                search.blur();
            }
        }
    });
    
    // ============================================
    // Newsletter Form
    // ============================================
    
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            
            if (email) {
                // Simulate subscription
                const btn = this.querySelector('button[type="submit"]');
                const originalText = btn.innerHTML;
                btn.innerHTML = 'Subscribed! ✓';
                btn.classList.add('btn-success');
                btn.classList.remove('btn-primary');
                
                setTimeout(function() {
                    btn.innerHTML = originalText;
                    btn.classList.remove('btn-success');
                    btn.classList.add('btn-primary');
                }, 3000);
            }
        });
    }
});
