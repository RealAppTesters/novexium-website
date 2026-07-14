let autosaveTimer = null;
let isDirty = false;

document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // Platform Toggle
    // ============================================
    
    document.querySelectorAll('.preview-toggle').forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            const platform = this.dataset.preview;
            
            document.querySelectorAll('.preview-toggle').forEach(function(t) {
                t.classList.remove('active');
            });
            this.classList.add('active');
            
            document.querySelectorAll('.preview-content').forEach(function(content) {
                content.style.display = 'none';
            });
            document.querySelector(`.preview-content[data-preview="${platform}"]`).style.display = 'block';
            
            document.getElementById('previewPlatform').textContent = 
                platform === 'app_store' ? 'App Store' : 'Google Play';
        });
    });
    
    // ============================================
    // Editor Updates
    // ============================================
    
    // Title
    const titleInput = document.getElementById('titleInput');
    if (titleInput) {
        titleInput.addEventListener('input', function() {
            updateCounter('titleCount', this.value.length, 'titleMax', 'titleBar', 30);
            updatePreview('previewTitle', this.value);
            markDirty();
        });
    }
    
    // Short Description
    const shortDescInput = document.getElementById('shortDescInput');
    if (shortDescInput) {
        shortDescInput.addEventListener('input', function() {
            updateCounter('shortDescCount', this.value.length, 'shortDescMax', 'shortDescBar', 150);
            updatePreview('previewShortDesc', this.value);
            markDirty();
        });
    }
    
    // Long Description
    const longDescInput = document.getElementById('longDescInput');
    if (longDescInput) {
        longDescInput.addEventListener('input', function() {
            updateCounter('longDescCount', this.value.length, 'longDescMax', 'longDescBar', 4000);
            updatePreview('previewLongDesc', this.value.substring(0, 200) + '...');
            markDirty();
        });
    }
    
    // What's New
    const whatsNewInput = document.getElementById('whatsNewInput');
    if (whatsNewInput) {
        whatsNewInput.addEventListener('input', function() {
            updatePreview('previewWhatsNew', this.value);
            markDirty();
        });
    }
    
    // ============================================
    // Auto-save
    // ============================================
    
    setInterval(function() {
        if (isDirty) {
            saveDraft();
        }
    }, 30000);
});

// ============================================
// Helper Functions
// ============================================

function updateCounter(countId, value, maxId, barId, maxLength) {
    document.getElementById(countId).textContent = value;
    
    const bar = document.getElementById(barId);
    if (bar) {
        const percentage = (value / maxLength) * 100;
        bar.style.width = Math.min(percentage, 100) + '%';
        
        bar.classList.remove('warning', 'danger');
        if (percentage > 90) {
            bar.classList.add('danger');
        } else if (percentage > 75) {
            bar.classList.add('warning');
        }
    }
}

function updatePreview(elementId, value) {
    const el = document.getElementById(elementId);
    if (el) {
        el.textContent = value || '—';
    }
}

function markDirty() {
    isDirty = true;
    document.getElementById('autosaveStatus').textContent = 'Unsaved changes';
    document.getElementById('autosaveStatus').style.color = 'var(--accent-warning)';
}

// ============================================
// Save Functions
// ============================================

window.saveDraft = function() {
    const data = getListingData();
    
    fetch('/api/v1/listing/draft', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(() => {
        isDirty = false;
        document.getElementById('autosaveStatus').textContent = 'Saved';
        document.getElementById('autosaveStatus').style.color = 'var(--accent-success)';
        showToast('Draft saved successfully!', 'success');
    })
    .catch(() => {
        showToast('Failed to save draft', 'error');
    });
};

window.updateListing = function(field) {
    const data = getListingData();
    
    // Debounce update
    clearTimeout(autosaveTimer);
    autosaveTimer = setTimeout(function() {
        fetch('/api/v1/listing/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(() => {
            isDirty = false;
            document.getElementById('autosaveStatus').textContent = 'Auto-saved';
            document.getElementById('autosaveStatus').style.color = 'var(--accent-success)';
        })
        .catch(() => {
            document.getElementById('autosaveStatus').textContent = 'Auto-save failed';
            document.getElementById('autosaveStatus').style.color = 'var(--accent-danger)';
        });
    }, 1000);
};

function getListingData() {
    return {
        title: document.getElementById('titleInput').value,
        short_description: document.getElementById('shortDescInput').value,
        long_description: document.getElementById('longDescInput').value,
        what_new: document.getElementById('whatsNewInput').value,
        platform: document.getElementById('platformSelect').value,
        language: document.getElementById('languageSelect').value
    };
}

window.publishListing = function() {
    if (!confirm('Are you sure you want to publish this listing?')) {
        return;
    }
    
    const data = getListingData();
    
    fetch('/api/v1/listing/publish', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(() => {
        showToast('Listing published successfully!', 'success');
    })
    .catch(() => {
        showToast('Failed to publish listing', 'error');
    });
};

window.formatText = function() {
    const textarea = document.getElementById('longDescInput');
    if (textarea) {
        // Basic text formatting
        let text = textarea.value;
        // Add double line breaks for paragraphs
        text = text.replace(/\n{2,}/g, '\n\n');
        // Add bullet points
        text = text.replace(/^- /gm, '• ');
        textarea.value = text;
        markDirty();
        updateListing('long_description');
        showToast('Text formatted!', 'success');
    }
};

window.clearListing = function() {
    if (!confirm('Clear all fields?')) {
        return;
    }
    
    document.getElementById('titleInput').value = '';
    document.getElementById('shortDescInput').value = '';
    document.getElementById('longDescInput').value = '';
    document.getElementById('whatsNewInput').value = '';
    
    // Update all previews
    document.querySelectorAll('.preview-app-title').forEach(el => el.textContent = '');
    document.getElementById('previewShortDesc').textContent = '';
    document.getElementById('previewLongDesc').textContent = '';
    document.getElementById('previewWhatsNew').textContent = '';
    
    // Reset counters
    document.querySelectorAll('.editor-field-fill').forEach(bar => bar.style.width = '0%');
    document.querySelectorAll('.editor-field-counter span:first-child').forEach(el => el.textContent = '0');
    
    markDirty();
    showToast('Listing cleared', 'info');
};
