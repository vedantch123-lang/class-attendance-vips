// JavaScript for Face Recognition Attendance System

document.addEventListener('DOMContentLoaded', function() {
    initializeFileUpload();
    initializeDragAndDrop();
    initializeFormValidation();
});

// File Upload Functionality
function initializeFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const filePreview = document.getElementById('filePreview');
    const previewImage = document.getElementById('previewImage');
    const fileName = document.getElementById('fileName');
    const uploadArea = document.getElementById('uploadArea');

    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            handleFileSelect(e.target.files[0]);
        });
    }

    if (uploadArea) {
        uploadArea.addEventListener('click', function() {
            fileInput.click();
        });
    }
}

// Handle File Selection
function handleFileSelect(file) {
    if (!file) return;

    // Display file preview
    displayFilePreview(file);
    
    // Always enable upload button when file is selected
    document.getElementById('uploadBtn').disabled = false;
}

// Validate Image File
function isValidImageFile(file) {
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
    return validTypes.includes(file.type);
}

// Display File Preview
function displayFilePreview(file) {
    const filePreview = document.getElementById('filePreview');
    const previewImage = document.getElementById('previewImage');
    const fileName = document.getElementById('fileName');

    // Create preview URL
    const reader = new FileReader();
    reader.onload = function(e) {
        previewImage.src = e.target.result;
        fileName.textContent = file.name;
        filePreview.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// Remove File
function removeFile() {
    const fileInput = document.getElementById('fileInput');
    const filePreview = document.getElementById('filePreview');
    const uploadBtn = document.getElementById('uploadBtn');

    fileInput.value = '';
    filePreview.style.display = 'none';
    uploadBtn.disabled = true;
}

// Drag and Drop Functionality
function initializeDragAndDrop() {
    const uploadArea = document.getElementById('uploadArea');
    
    if (!uploadArea) return;

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });

    // Handle dropped files
    uploadArea.addEventListener('drop', handleDrop, false);
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    const uploadArea = document.getElementById('uploadArea');
    if (uploadArea) {
        uploadArea.classList.add('dragover');
    }
}

function unhighlight(e) {
    const uploadArea = document.getElementById('uploadArea');
    if (uploadArea) {
        uploadArea.classList.remove('dragover');
    }
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
}

// Form Validation - Simplified
function initializeFormValidation() {
    const uploadForm = document.getElementById('uploadForm');
    
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            console.log('Form submitting...');
            // No validation blocking - let form submit normally
        });
    }
}

// Form validation removed - no blocking

// Show Loading Modal (placeholder)
function showLoadingModal() {
    console.log('Loading modal would show here');
}

// Alert System
function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());

    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Insert alert at the top of the container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Utility Functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Smooth Scrolling for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add Loading States to Buttons (Simplified)
document.addEventListener('click', function(e) {
    if (e.target.matches('.btn[type="submit"]')) {
        const btn = e.target;
        const originalText = btn.innerHTML;
        
        // Show loading state but don't disable
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Processing...';
        
        // Reset button after a delay
        setTimeout(() => {
            btn.innerHTML = originalText;
        }, 3000);
    }
});

// Auto-hide alerts after form submission
document.addEventListener('submit', function(e) {
    if (e.target.matches('form')) {
        setTimeout(() => {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(alert => {
                if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
                    alert.remove();
                }
            });
        }, 1000);
    }
});

// Keyboard Navigation Support
document.addEventListener('keydown', function(e) {
    // Escape key to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }
    
    // Enter key to submit forms when file is selected
    if (e.key === 'Enter' && document.activeElement === document.getElementById('fileInput')) {
        const uploadBtn = document.getElementById('uploadBtn');
        if (uploadBtn && !uploadBtn.disabled) {
            uploadBtn.click();
        }
    }
});

// Accessibility Improvements
function improveAccessibility() {
    // Add ARIA labels to interactive elements
    const uploadArea = document.getElementById('uploadArea');
    if (uploadArea) {
        uploadArea.setAttribute('role', 'button');
        uploadArea.setAttribute('tabindex', '0');
        uploadArea.setAttribute('aria-label', 'Click or drag and drop to upload a class photo');
    }
    
    // Add screen reader support for file input
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.setAttribute('aria-describedby', 'file-help');
    }
}

// Initialize accessibility improvements
document.addEventListener('DOMContentLoaded', improveAccessibility);

// Error Handling
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    showAlert('An unexpected error occurred. Please try again.', 'error');
});

// Performance Optimization
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Debounced file validation for better performance
const debouncedFileValidation = debounce(function(file) {
    if (file) {
        handleFileSelect(file);
    }
}, 300);

// Export functions for global access
window.FaceAttendanceApp = {
    showAlert,
    formatFileSize,
    formatDate,
    removeFile,
    showLoadingModal
};

// Debug function to test form submission
function testForm() {
    console.log('Testing form submission...');
    
    const form = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    
    if (!form) {
        console.error('Form not found!');
        return;
    }
    
    if (!fileInput.files[0]) {
        console.log('No file selected, simulating file selection...');
        // Create a fake file for testing
        const fakeFile = new File(['test'], 'test.jpg', { type: 'image/jpeg' });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(fakeFile);
        fileInput.files = dataTransfer.files;
        
        // Enable the button
        document.getElementById('uploadBtn').disabled = false;
    }
    
    console.log('Form action:', form.action);
    console.log('Form method:', form.method);
    console.log('Form enctype:', form.enctype);
    console.log('File input value:', fileInput.value);
    console.log('File input files:', fileInput.files);
    
    // Try to submit the form
    console.log('Attempting to submit form...');
    form.submit();
}
