class NotificationSystem {
    constructor() {
        this.container = document.getElementById('notification-container');
        this.toasts = [];
        this.setupListeners();
    }

    setupListeners() {
        // Listen for flash messages
        document.addEventListener('flash', (e) => {
            this.show(e.detail.message, e.detail.type);
        });

        // Listen for toast events
        document.addEventListener('toast', (e) => {
            this.showToast(e.detail.message, e.detail.type, e.detail.duration);
        });
    }

    show(message, type = 'info', duration = 5000) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-notification`;
        alert.setAttribute('role', 'alert');
        alert.innerHTML = `
            <svg class="alert-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                ${this.getIcon(type)}
            </svg>
            <div class="alert-content">
                <span>${message}</span>
            </div>
            <button class="alert-dismiss" aria-label="Dismiss notification">&times;</button>
        `;

        this.container.appendChild(alert);
        
        // Auto dismiss
        if (duration > 0) {
            setTimeout(() => {
                this.dismissAlert(alert);
            }, duration);
        }

        // Dismiss button
        alert.querySelector('.alert-dismiss').addEventListener('click', () => {
            this.dismissAlert(alert);
        });
    }

    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.setAttribute('role', 'toast');
        toast.innerHTML = `
            <svg class="toast-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                ${this.getIcon(type)}
            </svg>
            <span class="toast-message">${message}</span>
            <button class="toast-dismiss" aria-label="Dismiss toast">&times;</button>
        `;

        this.toasts.push(toast);
        this.renderToasts();

        if (duration > 0) {
            setTimeout(() => {
                this.dismissToast(toast);
            }, duration);
        }

        toast.querySelector('.toast-dismiss').addEventListener('click', () => {
            this.dismissToast(toast);
        });
    }

    dismissAlert(alert) {
        alert.classList.add('alert-dismissing');
        setTimeout(() => {
            alert.remove();
        }, 300);
    }

    dismissToast(toast) {
        toast.classList.add('toast-dismissing');
        setTimeout(() => {
            this.toasts = this.toasts.filter(t => t !== toast);
            toast.remove();
        }, 300);
    }

    renderToasts() {
        // Position toasts at the top right
        const toastContainer = document.getElementById('toast-container');
        toastContainer.innerHTML = '';
        this.toasts.forEach(toast => {
            toastContainer.appendChild(toast);
        });
    }

    getIcon(type) {
        const icons = {
            success: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
            error: '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>',
            warning: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>',
            info: '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>'
        };
        return icons[type] || icons.info;
    }
}

// Initialize notification system
const notifications = new NotificationSystem();

// Expose for use in other scripts
window.showNotification = (message, type, duration) => {
    notifications.show(message, type, duration);
};

window.showToast = (message, type, duration) => {
    notifications.showToast(message, type, duration);
};
