document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Sidebar Toggle
    // ============================================
    const sidebar = document.getElementById('dashboardSidebar');
    const collapseBtn = document.getElementById('sidebarCollapse');
    
    if (collapseBtn) {
        collapseBtn.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        });
        
        // Load saved state
        if (localStorage.getItem('sidebarCollapsed') === 'true') {
            sidebar.classList.add('collapsed');
        }
    }
    
    // ============================================
    // Mobile Navigation
    // ============================================
    const mobileToggle = document.getElementById('mobileToggle');
    const mobileNav = document.querySelector('.mobile-nav-overlay');
    const mobileClose = document.querySelector('.mobile-nav-close');
    
    if (mobileToggle && mobileNav) {
        mobileToggle.addEventListener('click', function() {
            mobileNav.classList.toggle('active');
            this.classList.toggle('active');
            document.body.style.overflow = mobileNav.classList.contains('active') ? 'hidden' : '';
        });
    }
    
    if (mobileClose && mobileNav) {
        mobileClose.addEventListener('click', function() {
            mobileNav.classList.remove('active');
            mobileToggle.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
    
    // Close mobile nav on escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileNav && mobileNav.classList.contains('active')) {
            mobileNav.classList.remove('active');
            mobileToggle.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
    
    // ============================================
    // Profile Dropdown
    // ============================================
    const profileBtn = document.getElementById('profileMenuBtn');
    const profileDropdown = document.getElementById('profileDropdown');
    
    if (profileBtn && profileDropdown) {
        profileBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            const isOpen = profileDropdown.classList.contains('active');
            profileDropdown.classList.toggle('active');
            this.setAttribute('aria-expanded', !isOpen);
        });
        
        // Close on click outside
        document.addEventListener('click', function(e) {
            if (!profileBtn.contains(e.target) && !profileDropdown.contains(e.target)) {
                profileDropdown.classList.remove('active');
                profileBtn.setAttribute('aria-expanded', 'false');
            }
        });
        
        // Close on escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && profileDropdown.classList.contains('active')) {
                profileDropdown.classList.remove('active');
                profileBtn.setAttribute('aria-expanded', 'false');
            }
        });
    }
    
    // ============================================
    // Notifications Panel
    // ============================================
    const notificationsBtn = document.getElementById('notificationsBtn');
    const notificationsPanel = document.getElementById('notificationsPanel');
    
    if (notificationsBtn && notificationsPanel) {
        notificationsBtn.addEventListener('click', function() {
            notificationsPanel.classList.toggle('active');
        });
        
        // Close on click outside
        document.addEventListener('click', function(e) {
            if (!notificationsBtn.contains(e.target) && !notificationsPanel.contains(e.target)) {
                notificationsPanel.classList.remove('active');
            }
        });
    }
    
    // ============================================
    // Mark All Notifications Read
    // ============================================
    const markAllRead = document.getElementById('markAllRead');
    if (markAllRead) {
        markAllRead.addEventListener('click', function() {
            document.querySelectorAll('.notification-item.unread').forEach(function(item) {
                item.classList.remove('unread');
            });
            const dot = document.querySelector('.notification-dot');
            if (dot) dot.style.display = 'none';
        });
    }
    
    // ============================================
    // Global Search
    // ============================================
    const searchBtns = document.querySelectorAll('#sidebarSearchBtn, #headerSearchBtn');
    const searchOverlay = document.getElementById('searchOverlay');
    
    if (searchOverlay) {
        searchBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                searchOverlay.classList.add('active');
                document.body.style.overflow = 'hidden';
                const input = document.getElementById('searchInput');
                if (input) setTimeout(function() { input.focus(); }, 100);
            });
        });
    }
    
    // ============================================
    // FAQ Accordion
    // ============================================
    document.querySelectorAll('.faq-question').forEach(function(button) {
        button.addEventListener('click', function() {
            const item = this.closest('.faq-item');
            const isActive = item.classList.contains('active');
            
            // Close other items
            document.querySelectorAll('.faq-item').forEach(function(other) {
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
    // Quick Action Cards
    // ============================================
    document.querySelectorAll('.quick-action').forEach(function(card) {
        card.addEventListener('click', function() {
            const href = this.getAttribute('data-href');
            if (href) {
                window.location.href = href;
            }
        });
    });
    
    // ============================================
    // Refresh Blueprint
    // ============================================
    window.refreshBlueprint = function() {
        const btn = document.querySelector('.growth-blueprint-refresh');
        if (btn) {
            btn.classList.add('refreshing');
            btn.innerHTML = 'Refreshing...';
            
            setTimeout(function() {
                btn.classList.remove('refreshing');
                btn.innerHTML = `
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M23 4v6h-6"/>
                        <path d="M1 20v-6h6"/>
                        <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
                    </svg>
                    <span>Refresh</span>
                `;
            }, 1500);
        }
    };
});

// ============================================
// Keyboard Shortcuts
// ============================================
document.addEventListener('keydown', function(e) {
    // Ctrl+K or Cmd+K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchOverlay = document.getElementById('searchOverlay');
        if (searchOverlay) {
            searchOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
            const input = document.getElementById('searchInput');
            if (input) setTimeout(function() { input.focus(); }, 100);
        }
    }
    
    // Escape to close search
    if (e.key === 'Escape') {
        const searchOverlay = document.getElementById('searchOverlay');
        if (searchOverlay && searchOverlay.classList.contains('active')) {
            searchOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
});
