/**
 * Frontend Content Editor
 * Provides inline editing capabilities for blog posts and pages
 */

class FrontendEditor {
    constructor() {
        this.isEditing = false;
        this.currentElement = null;
        this.originalContent = null;
        this.toolbar = null;
        this.init();
    }

    init() {
        // Only initialize for staff users
        if (!this.isStaffUser()) return;
        
        this.createToolbar();
        this.attachEventListeners();
        this.makeContentEditable();
    }

    isStaffUser() {
        // Check if user is authenticated staff (we'll add this via template)
        return window.isStaffUser || false;
    }

    createToolbar() {
        this.toolbar = document.createElement('div');
        this.toolbar.className = 'frontend-editor-toolbar';
        this.toolbar.innerHTML = `
            <div class="toolbar-content">
                <button class="toolbar-button" id="edit-mode-toggle">
                    <span class="icon">✏️</span>
                    <span class="text">Edit Mode</span>
                </button>
                <button class="toolbar-button" id="save-changes" style="display: none;">
                    <span class="icon">💾</span>
                    <span class="text">Save</span>
                </button>
                <button class="toolbar-button" id="cancel-edit" style="display: none;">
                    <span class="icon">❌</span>
                    <span class="text">Cancel</span>
                </button>
                <button class="toolbar-button toolbar-minimize" id="minimize-toolbar" title="Hide toolbar">
                    <span class="icon">−</span>
                </button>
                <div class="toolbar-status" id="edit-status"></div>
            </div>
        `;
        
        document.body.appendChild(this.toolbar);
        
        // Create minimized toolbar button
        this.minimizedButton = document.createElement('div');
        this.minimizedButton.className = 'frontend-editor-minimized';
        this.minimizedButton.innerHTML = `
            <button class="toolbar-button" id="show-toolbar" title="Show editing toolbar">
                <span class="icon">✏️</span>
            </button>
        `;
        this.minimizedButton.style.display = 'none';
        document.body.appendChild(this.minimizedButton);
    }

    attachEventListeners() {
        // Toolbar buttons
        document.getElementById('edit-mode-toggle').addEventListener('click', () => {
            this.toggleEditMode();
        });

        document.getElementById('save-changes').addEventListener('click', () => {
            this.saveChanges();
        });

        document.getElementById('cancel-edit').addEventListener('click', () => {
            this.cancelEdit();
        });

        document.getElementById('minimize-toolbar').addEventListener('click', () => {
            this.hideToolbar();
        });

        document.getElementById('show-toolbar').addEventListener('click', () => {
            this.showToolbar();
        });

        // Global key bindings
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                if (e.key === 's' && this.isEditing) {
                    e.preventDefault();
                    this.saveChanges();
                } else if (e.key === 'Escape' && this.isEditing) {
                    e.preventDefault();
                    this.cancelEdit();
                }
            }
        });
    }

    makeContentEditable() {
        // Find editable content areas
        const editableElements = document.querySelectorAll('[data-editable]');
        
        editableElements.forEach(element => {
            element.addEventListener('click', (e) => {
                if (this.isEditing) {
                    this.startEditing(element);
                    e.preventDefault();
                }
            });
        });
    }

    toggleEditMode() {
        this.isEditing = !this.isEditing;
        
        const editButton = document.getElementById('edit-mode-toggle');
        const saveButton = document.getElementById('save-changes');
        const cancelButton = document.getElementById('cancel-edit');
        const status = document.getElementById('edit-status');
        
        if (this.isEditing) {
            editButton.style.display = 'none';
            saveButton.style.display = 'inline-flex';
            cancelButton.style.display = 'inline-flex';
            status.textContent = 'Edit mode active - Click content to edit';
            
            // Add visual indicators
            document.querySelectorAll('[data-editable]').forEach(el => {
                el.classList.add('editable-hover');
            });
            
        } else {
            editButton.style.display = 'inline-flex';
            saveButton.style.display = 'none';
            cancelButton.style.display = 'none';
            status.textContent = '';
            
            // Remove visual indicators
            document.querySelectorAll('[data-editable]').forEach(el => {
                el.classList.remove('editable-hover', 'editing-active');
            });
            
            // Cancel any active editing
            if (this.currentElement) {
                this.stopEditing();
            }
        }
    }

    startEditing(element) {
        // Stop any current editing
        if (this.currentElement && this.currentElement !== element) {
            this.stopEditing();
        }

        this.currentElement = element;
        this.originalContent = element.innerHTML;
        
        // Make element editable
        element.contentEditable = true;
        element.classList.add('editing-active');
        
        // Add rich text toolbar for content editing
        if (element.dataset.editable === 'content') {
            this.showRichTextToolbar(element);
        }
        
        element.focus();
        
        // Update status
        const status = document.getElementById('edit-status');
        status.textContent = `Editing ${element.dataset.editable} - Ctrl+S to save, Esc to cancel`;
    }

    stopEditing() {
        if (!this.currentElement) return;
        
        this.currentElement.contentEditable = false;
        this.currentElement.classList.remove('editing-active');
        this.hideRichTextToolbar();
        this.currentElement = null;
        this.originalContent = null;
    }

    showRichTextToolbar(element) {
        // Remove existing rich text toolbar
        this.hideRichTextToolbar();
        
        // Create rich text toolbar
        const richToolbar = document.createElement('div');
        richToolbar.className = 'rich-text-toolbar';
        richToolbar.innerHTML = `
            <button type="button" data-command="bold" title="Bold (Ctrl+B)"><strong>B</strong></button>
            <button type="button" data-command="italic" title="Italic (Ctrl+I)"><em>I</em></button>
            <button type="button" data-command="underline" title="Underline (Ctrl+U)"><u>U</u></button>
            <div class="toolbar-separator"></div>
            <button type="button" data-command="formatBlock" data-value="h2" title="Heading 2">H2</button>
            <button type="button" data-command="formatBlock" data-value="h3" title="Heading 3">H3</button>
            <button type="button" data-command="formatBlock" data-value="p" title="Paragraph">P</button>
            <div class="toolbar-separator"></div>
            <button type="button" data-command="insertUnorderedList" title="Bullet List">• List</button>
            <button type="button" data-command="insertOrderedList" title="Numbered List">1. List</button>
            <div class="toolbar-separator"></div>
            <button type="button" data-command="createLink" title="Insert Link">🔗</button>
            <button type="button" data-command="unlink" title="Remove Link">🔗❌</button>
        `;
        
        // Position toolbar above the element
        const rect = element.getBoundingClientRect();
        richToolbar.style.position = 'fixed';
        richToolbar.style.top = (rect.top - 50 + window.scrollY) + 'px';
        richToolbar.style.left = rect.left + 'px';
        richToolbar.style.zIndex = '10002';
        
        document.body.appendChild(richToolbar);
        this.richTextToolbar = richToolbar;
        
        // Add event listeners
        richToolbar.addEventListener('click', (e) => {
            if (e.target.tagName === 'BUTTON') {
                e.preventDefault();
                const command = e.target.dataset.command;
                const value = e.target.dataset.value;
                
                if (command === 'createLink') {
                    const url = prompt('Enter URL:');
                    if (url) {
                        document.execCommand(command, false, url);
                    }
                } else {
                    document.execCommand(command, false, value);
                }
                
                // Refocus on content
                element.focus();
            }
        });
    }

    hideRichTextToolbar() {
        if (this.richTextToolbar) {
            this.richTextToolbar.remove();
            this.richTextToolbar = null;
        }
    }

    hideToolbar() {
        // Don't hide if actively editing
        if (this.isEditing) {
            this.showMessage('Please save or cancel your changes first', 'warning');
            return;
        }
        
        this.toolbar.style.display = 'none';
        this.minimizedButton.style.display = 'block';
    }

    showToolbar() {
        this.toolbar.style.display = 'block';
        this.minimizedButton.style.display = 'none';
    }

    async saveChanges() {
        if (!this.currentElement) {
            this.showMessage('No content being edited', 'warning');
            return;
        }

        const contentType = this.currentElement.dataset.editable;
        const contentId = this.getContentId();
        const newContent = this.currentElement.innerHTML;
        
        // Show saving indicator
        const status = document.getElementById('edit-status');
        status.textContent = 'Saving...';
        
        try {
            const endpoint = contentType === 'title' || contentType === 'content' ? 
                (this.isPost() ? `/blog/edit/post/${contentId}/` : `/blog/edit/page/${contentId}/`) :
                null;
                
            if (!endpoint) {
                throw new Error('Unknown content type');
            }
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    [contentType]: newContent
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showMessage('Changes saved successfully!', 'success');
                this.originalContent = newContent; // Update original content
                status.textContent = 'Saved successfully';
                
                // Update any slug if title changed
                if (contentType === 'title') {
                    // Could add slug update logic here
                }
                
            } else {
                throw new Error(result.message || 'Save failed');
            }
            
        } catch (error) {
            console.error('Save error:', error);
            this.showMessage(`Error saving: ${error.message}`, 'error');
            status.textContent = 'Save failed';
            
            // Revert content on error
            this.currentElement.innerHTML = this.originalContent;
        }
    }

    cancelEdit() {
        if (this.currentElement && this.originalContent !== null) {
            this.currentElement.innerHTML = this.originalContent;
            this.showMessage('Changes discarded', 'info');
        }
        
        this.stopEditing();
        this.toggleEditMode(); // Exit edit mode
    }

    getContentId() {
        // Extract content ID from URL or data attribute
        const match = window.location.pathname.match(/\/(post|page)\/([^\/]+)\//);
        if (match) {
            // We have slug, need to get ID - could be passed via template
            return document.body.dataset.contentId || null;
        }
        return null;
    }

    isPost() {
        return window.location.pathname.includes('/post/');
    }

    showMessage(message, type = 'info') {
        // Create a simple toast notification
        const toast = document.createElement('div');
        toast.className = `editor-toast toast-${type}`;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new FrontendEditor();
});