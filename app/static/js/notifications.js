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

document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Filters
    // ============================================
    
    document.querySelectorAll('.filter-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(function(b) {
                b.classList.remove('active');
            });
            this.classList.add('active');
            
            const filter = this.dataset.filter;
            filterNotifications(filter);
        });
    });
    
    function filterNotifications(filter) {
        const items = document.querySelectorAll('.notification-item');
        
        items.forEach(function(item) {
            let show = true;
            
            if (filter === 'unread') {
                show = item.classList.contains('unread');
            } else if (filter === 'high') {
                show = item.classList.contains('high') || item.classList.contains('critical');
            } else if (filter === 'bookmarked') {
                const bookmark = item.querySelector('.notification-bookmark');
                show = bookmark && bookmark.textContent === '★';
            }
            
            item.style.display = show ? '' : 'none';
        });
    }
    
    // ============================================
    // Mark All Read
    // ============================================
    
    window.markAllRead = function() {
        fetch('/api/v1/notifications/mark-all-read', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            document.querySelectorAll('.notification-item.unread').forEach(function(item) {
                item.classList.remove('unread');
            });
            showToast('All notifications marked as read', 'success');
        })
        .catch(() => {
            showToast('Failed to mark all as read', 'error');
        });
    };
    
    // ============================================
    // Bookmark
    // ============================================
    
    window.bookmarkNotification = function(notificationId) {
        const btn = event.currentTarget;
        const isBookmarked = btn.textContent === '★';
        
        fetch(`/api/v1/notifications/${notificationId}/bookmark`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            btn.textContent = isBookmarked ? '☆' : '★';
            showToast(isBookmarked ? 'Bookmark removed' : 'Bookmarked!', 'info');
        })
        .catch(() => {
            showToast('Failed to bookmark', 'error');
        });
    };
    
    // ============================================
    // Dismiss
    // ============================================
    
    window.dismissNotification = function(notificationId) {
        const item = event.currentTarget.closest('.notification-item');
        
        fetch(`/api/v1/notifications/${notificationId}/dismiss`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            item.style.display = 'none';
            showToast('Notification dismissed', 'info');
        })
        .catch(() => {
            showToast('Failed to dismiss', 'error');
        });
    };
    
    // ============================================
    // Sort
    // ============================================
    
    document.querySelector('.filter-select').addEventListener('change', function() {
        const sortBy = this.value;
        const list = document.querySelector('.notifications-list');
        const items = Array.from(list.querySelectorAll('.notification-item'));
        
        items.sort(function(a, b) {
            if (sortBy === 'newest') {
                return b.dataset.date - a.dataset.date;
            } else if (sortBy === 'oldest') {
                return a.dataset.date - b.dataset.date;
            } else if (sortBy === 'priority') {
                const priorities = { critical: 0, high: 1, medium: 2, low: 3 };
                const aPriority = a.classList.contains('critical') ? 'critical' : 
                                  a.classList.contains('high') ? 'high' : 
                                  a.classList.contains('medium') ? 'medium' : 'low';
                const bPriority = b.classList.contains('critical') ? 'critical' : 
                                  b.classList.contains('high') ? 'high' : 
                                  b.classList.contains('medium') ? 'medium' : 'low';
                return priorities[aPriority] - priorities[bPriority];
            }
            return 0;
        });
        
        items.forEach(function(item) {
            list.appendChild(item);
        });
    });
});
