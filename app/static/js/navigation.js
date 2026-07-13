class NavigationSystem {
    constructor() {
        this.header = document.querySelector('.header');
        this.mobileToggle = document.querySelector('.mobile-menu-toggle');
        this.mobileNav = document.querySelector('#mobileNav');
        this.mobileClose = document.querySelector('.mobile-nav-close');
        this.dropdownTriggers = document.querySelectorAll('.dropdown-trigger');
        this.setupEventListeners();
        this.handleScroll();
    }

    setupEventListeners() {
        // Mobile menu
        if (this.mobileToggle && this.mobileNav) {
            this.mobileToggle.addEventListener('click', () => this.toggleMobileNav());
        }
        if (this.mobileClose) {
            this.mobileClose.addEventListener('click', () => this.closeMobileNav());
        }

        // Dropdown menus
        this.dropdownTriggers.forEach(trigger => {
            const button = trigger.querySelector('button');
            const menu = trigger.querySelector('.mega-menu');
            
            if (button && menu) {
                // Hover
                trigger.addEventListener('mouseenter', () => this.openDropdown(button, menu));
                trigger.addEventListener('mouseleave', () => this.closeDropdown(button, menu));
                
                // Click for mobile
                button.addEventListener('click', (e) => {
                    if (window.innerWidth <= 768) {
                        e.preventDefault();
                        this.toggleDropdown(button, menu);
                    }
                });
            }
        });

        // Search
        const searchBtn = document.querySelector('.header-search-btn');
        const searchOverlay = document.getElementById('searchOverlay');
        const searchInput = document.getElementById('searchInput');

        if (searchBtn && searchOverlay) {
            searchBtn.addEventListener('click', () => this.openSearch(searchOverlay, searchInput));
        }

        if (searchOverlay) {
            // Close on backdrop click
            searchOverlay.addEventListener('click', (e) => {
                if (e.target === searchOverlay) {
                    this.closeSearch(searchOverlay);
                }
            });

            // Keyboard shortcut
            document.addEventListener('keydown', (e) => {
                if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                    e.preventDefault();
                    this.openSearch(searchOverlay, searchInput);
                }
                if (e.key === 'Escape') {
                    this.closeSearch(searchOverlay);
                }
            });
        }

        // Close mobile nav on resize
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                this.closeMobileNav();
            }
        });
    }

    toggleMobileNav() {
        const isOpen = this.mobileNav.classList.contains('active');
        if (isOpen) {
            this.closeMobileNav();
        } else {
            this.openMobileNav();
        }
    }

    openMobileNav() {
        this.mobileNav.classList.add('active');
        document.body.style.overflow = 'hidden';
        this.mobileToggle.setAttribute('aria-expanded', 'true');
    }

    closeMobileNav() {
        this.mobileNav.classList.remove('active');
        document.body.style.overflow = '';
        this.mobileToggle.setAttribute('aria-expanded', 'false');
    }

    openDropdown(button, menu) {
        button.setAttribute('aria-expanded', 'true');
        menu.style.display = 'block';
    }

    closeDropdown(button, menu) {
        button.setAttribute('aria-expanded', 'false');
        menu.style.display = 'none';
    }

    toggleDropdown(button, menu) {
        const isOpen = button.getAttribute('aria-expanded') === 'true';
        if (isOpen) {
            this.closeDropdown(button, menu);
        } else {
            this.openDropdown(button, menu);
        }
    }

    openSearch(overlay, input) {
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        if (input) {
            setTimeout(() => input.focus(), 100);
        }
    }

    closeSearch(overlay) {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    handleScroll() {
        let lastScroll = 0;
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            if (currentScroll > 50) {
                this.header.classList.add('header-scrolled');
            } else {
                this.header.classList.remove('header-scrolled');
            }
            
            lastScroll = currentScroll;
        });
    }
}

// Initialize navigation
document.addEventListener('DOMContentLoaded', () => {
    new NavigationSystem();
});
