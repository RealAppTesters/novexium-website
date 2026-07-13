// Theme Management
const ThemeManager = {
    currentTheme: 'dark',
    storageKey: 'novexium-theme',

    init() {
        // Load saved theme or system preference
        const savedTheme = localStorage.getItem(this.storageKey);
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        this.currentTheme = savedTheme || (prefersDark ? 'dark' : 'light');
        this.applyTheme(this.currentTheme);
        
        // Setup toggle button
        document.addEventListener('DOMContentLoaded', () => {
            const toggle = document.getElementById('themeToggle');
            if (toggle) {
                toggle.addEventListener('click', () => this.toggle());
            }
        });
    },

    toggle() {
        this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.applyTheme(this.currentTheme);
        localStorage.setItem(this.storageKey, this.currentTheme);
        this.dispatchThemeEvent();
    },

    applyTheme(theme) {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.remove('light');
        
        if (theme === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.add('light');
        }
        
        // Update meta theme-color
        const metaTheme = document.querySelector('meta[name="theme-color"]');
        if (metaTheme) {
            metaTheme.content = theme === 'dark' ? '#09090B' : '#FAFAFA';
        }
    },

    dispatchThemeEvent() {
        document.dispatchEvent(new CustomEvent('themeChange', {
            detail: { theme: this.currentTheme }
        }));
    }
};

// Initialize theme manager
ThemeManager.init();

// Expose for use in other scripts
window.themeManager = ThemeManager;
