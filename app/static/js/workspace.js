document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Tab Navigation
    // ============================================
    
    const tabs = document.querySelectorAll('.workspace-nav-tab');
    const tabContents = document.querySelectorAll('.workspace-tab');
    
    tabs.forEach(function(tab) {
        tab.addEventListener('click', function() {
            const tabId = this.dataset.tab;
            
            // Update active tab
            tabs.forEach(function(t) {
                t.classList.remove('active');
                t.setAttribute('aria-selected', 'false');
            });
            this.classList.add('active');
            this.setAttribute('aria-selected', 'true');
            
            // Update content
            tabContents.forEach(function(content) {
                content.classList.remove('active');
            });
            document.querySelector(`.workspace-tab[data-tab="${tabId}"]`).classList.add('active');
            
            // Trigger chart resize if needed
            if (tabId === 'overview' && window.resizeCharts) {
                setTimeout(function() {
                    window.resizeCharts();
                }, 100);
            }
        });
    });
    
    // ============================================
    // Quick Actions
    // ============================================
    
    // Toggle quick actions visibility on scroll
    let lastScroll = 0;
    const quickActions = document.getElementById('quickActions');
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        if (currentScroll > 100) {
            quickActions.classList.add('visible');
        } else {
            quickActions.classList.remove('visible');
        }
        lastScroll = currentScroll;
    });
    
    // ============================================
    // Chart Filters
    // ============================================
    
    document.querySelectorAll('.workspace-charts-filter').forEach(function(filter) {
        filter.addEventListener('click', function() {
            document.querySelectorAll('.workspace-charts-filter').forEach(function(f) {
                f.classList.remove('active');
            });
            this.classList.add('active');
            
            const period = this.dataset.period;
            // Update charts with new period
            if (window.updateCharts) {
                window.updateCharts(period);
            }
        });
    });
    
    // ============================================
    // Score Bar Animations
    // ============================================
    
    function animateScoreBars() {
        document.querySelectorAll('.workspace-score-card-fill').forEach(function(bar) {
            const width = bar.style.width;
            bar.style.width = '0%';
            setTimeout(function() {
                bar.style.width = width;
            }, 200);
        });
    }
    
    // Run on load
    setTimeout(animateScoreBars, 300);
    
    // ============================================
    // Recommendation Actions
    // ============================================
    
    window.startRecommendation = function(appId) {
        showToast('Starting recommendation...', 'info');
        setTimeout(function() {
            showToast('Recommendation started!', 'success');
        }, 1500);
    };
    
    window.viewBlueprint = function() {
        // Navigate to blueprint section
        document.querySelector('.workspace-nav-tab[data-tab="overview"]').click();
        document.querySelector('.workspace-blueprint').scrollIntoView({ behavior: 'smooth' });
    };
    
    // ============================================
    // Quick Action Functions
    // ============================================
    
    window.runAudit = function(appId) {
        showToast('Starting audit...', 'info');
        setTimeout(function() {
            showToast('Audit completed!', 'success');
        }, 2000);
    };
    
    window.generateReport = function(appId) {
        showToast('Generating report...', 'info');
        setTimeout(function() {
            showToast('Report ready!', 'success');
        }, 1500);
    };
    
    window.optimizeListing = function(appId) {
        document.querySelector('.workspace-nav-tab[data-tab="store-listing"]').click();
    };
    
    window.refreshData = function(appId) {
        showToast('Refreshing data...', 'info');
        setTimeout(function() {
            showToast('Data refreshed!', 'success');
        }, 2000);
    };
    
    window.exportData = function(appId) {
        showToast('Exporting data...', 'info');
        setTimeout(function() {
            showToast('Export complete!', 'success');
        }, 1500);
    };
    
    window.shareReport = function(appId) {
        showToast('Share link copied to clipboard!', 'success');
    };
    
    window.viewOpportunity = function(oppId) {
        showToast('Opening opportunity details...', 'info');
    };
});
