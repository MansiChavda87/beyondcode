// Editor.js Widget Initialization
// Handles the initialization and management of Editor.js instances in Django admin

(function() {
    'use strict';

    // Global Editor.js instances storage
    window.editorjsInstances = {};

    /**
     * Initialize Editor.js instance
     * @param {string} editorId - The ID of the editor container
     * @param {Object} config - Editor.js configuration
     */
    window.initializeEditorJS = function(editorId, config) {
        const editorContainer = document.getElementById(editorId + '_editor');
        const textarea = document.getElementById(editorId);
        
        if (!editorContainer || !textarea) {
            console.error('Editor.js container or textarea not found:', editorId);
            return;
        }

        try {
            // Create Editor.js instance
            const editor = new EditorJS({
                holder: editorContainer.id,
                tools: config.tools || {},
                data: config.data || { blocks: [] },
                placeholder: config.placeholder || 'Start writing...',
                readOnly: config.readOnly || false,
                minHeight: config.minHeight || 300,
                onReady: function() {
                    // Store instance reference
                    window.editorjsInstances[editorId] = this;
                    
                    // Call custom onReady callback if provided
                    if (typeof config.onReady === 'function') {
                        config.onReady.call(this);
                    }
                    
                    // Add custom event listeners
                    setupEventListeners(this, editorId);
                    
                    // Initialize drag and drop if available
                    if (typeof EditorJSDragDrop !== 'undefined') {
                        new EditorJSDragDrop({
                            editor: this
                        });
                    }
                },
                onChange: function() {
                    // Call custom onChange callback if provided
                    if (typeof config.onChange === 'function') {
                        config.onChange.call(this);
                    } else {
                        // Default behavior: update textarea with current data
                        updateTextarea(this, textarea);
                    }
                }
            });

        } catch (error) {
            console.error('Failed to initialize Editor.js:', error);
            // Fallback to textarea if Editor.js fails
            textarea.style.display = 'block';
            editorContainer.style.display = 'none';
        }
    };

    /**
     * Setup custom event listeners for the editor
     * @param {Object} editor - Editor.js instance
     * @param {string} editorId - The ID of the editor
     */
    function setupEventListeners(editor, editorId) {
        // Listen for block changes
        editor.on('blockChanged', function(event) {
            updateTextarea(editor, document.getElementById(editorId));
        });

        // Listen for block added
        editor.on('blockAdded', function(event) {
            updateTextarea(editor, document.getElementById(editorId));
        });

        // Listen for block removed
        editor.on('blockRemoved', function(event) {
            updateTextarea(editor, document.getElementById(editorId));
        });

        // Listen for toolbar actions
        editor.on('toolbarOpened', function() {
            // Add custom styling when toolbar is open
            const container = document.getElementById(editorId + '_editor');
            if (container) {
                container.classList.add('toolbar-open');
            }
        });

        editor.on('toolbarClosed', function() {
            // Remove custom styling when toolbar is closed
            const container = document.getElementById(editorId + '_editor');
            if (container) {
                container.classList.remove('toolbar-open');
            }
        });
    }

    /**
     * Update the hidden textarea with current editor data
     * @param {Object} editor - Editor.js instance
     * @param {HTMLElement} textarea - The textarea element to update
     */
    function updateTextarea(editor, textarea) {
        if (!editor || !textarea) return;

        editor.save().then(function(savedData) {
            textarea.value = JSON.stringify(savedData);
            // Trigger change event for form validation
            textarea.dispatchEvent(new Event('change', { bubbles: true }));
        }).catch(function(error) {
            console.error('Error saving editor data:', error);
        });
    }

    /**
     * Get editor data as JSON
     * @param {string} editorId - The ID of the editor
     * @returns {Promise} Promise that resolves to the editor data
     */
    window.getEditorJSData = function(editorId) {
        const editor = window.editorjsInstances[editorId];
        if (!editor) {
            console.error('Editor.js instance not found:', editorId);
            return Promise.reject(new Error('Editor.js instance not found'));
        }

        return editor.save();
    };

    /**
     * Set editor data from JSON
     * @param {string} editorId - The ID of the editor
     * @param {Object} data - The data to set
     * @returns {Promise} Promise that resolves when data is set
     */
    window.setEditorJSData = function(editorId, data) {
        const editor = window.editorjsInstances[editorId];
        if (!editor) {
            console.error('Editor.js instance not found:', editorId);
            return Promise.reject(new Error('Editor.js instance not found'));
        }

        return editor.render(data);
    };

    /**
     * Clear editor content
     * @param {string} editorId - The ID of the editor
     * @returns {Promise} Promise that resolves when content is cleared
     */
    window.clearEditorJS = function(editorId) {
        return setEditorJSData(editorId, { blocks: [] });
    };

    /**
     * Destroy editor instance
     * @param {string} editorId - The ID of the editor
     */
    window.destroyEditorJS = function(editorId) {
        const editor = window.editorjsInstances[editorId];
        if (editor) {
            editor.destroy();
            delete window.editorjsInstances[editorId];
        }
    };

    /**
     * Validate editor content
     * @param {string} editorId - The ID of the editor
     * @returns {Promise} Promise that resolves to validation result
     */
    window.validateEditorJS = function(editorId) {
        return getEditorJSData(editorId).then(function(data) {
            // Basic validation: check if there are any blocks
            if (!data.blocks || data.blocks.length === 0) {
                return {
                    isValid: false,
                    message: 'Content cannot be empty'
                };
            }

            // Check for empty blocks that shouldn't be empty
            const emptyBlocks = data.blocks.filter(function(block) {
                if (block.type === 'paragraph') {
                    return !block.data.text || block.data.text.trim() === '';
                }
                if (block.type === 'header') {
                    return !block.data.text || block.data.text.trim() === '';
                }
                return false;
            });

            if (emptyBlocks.length > 0) {
                return {
                    isValid: false,
                    message: 'Some blocks contain empty content'
                };
            }

            return {
                isValid: true,
                message: 'Content is valid'
            };
        }).catch(function(error) {
            return {
                isValid: false,
                message: 'Error validating content: ' + error.message
            };
        });
    };

    /**
     * Export editor content as HTML (basic implementation)
     * @param {string} editorId - The ID of the editor
     * @returns {Promise} Promise that resolves to HTML string
     */
    window.exportEditorJSAsHTML = function(editorId) {
        return getEditorJSData(editorId).then(function(data) {
            let html = '';
            
            data.blocks.forEach(function(block) {
                switch (block.type) {
                    case 'header':
                        const level = block.data.level || 2;
                        html += `<h${level}>${block.data.text || ''}</h${level}>`;
                        break;
                    case 'paragraph':
                        html += `<p>${block.data.text || ''}</p>`;
                        break;
                    case 'list':
                        const tag = block.data.style === 'ordered' ? 'ol' : 'ul';
                        html += `<${tag}>`;
                        (block.data.items || []).forEach(function(item) {
                            html += `<li>${item}</li>`;
                        });
                        html += `</${tag}>`;
                        break;
                    case 'image':
                        html += `<img src="${block.data.file ? block.data.file.url : ''}" alt="${block.data.caption || ''}" />`;
                        if (block.data.caption) {
                            html += `<p class="image-caption">${block.data.caption}</p>`;
                        }
                        break;
                    case 'quote':
                        html += `<blockquote><p>${block.data.text || ''}</p>`;
                        if (block.data.caption) {
                            html += `<cite>${block.data.caption}</cite>`;
                        }
                        html += `</blockquote>`;
                        break;
                    default:
                        html += `<p>[${block.type} block]</p>`;
                }
            });

            return html;
        });
    };

    // Auto-initialize any existing editors on page load
    document.addEventListener('DOMContentLoaded', function() {
        // Look for any existing editor containers that might need initialization
        const editorContainers = document.querySelectorAll('.editorjs-editor');
        editorContainers.forEach(function(container) {
            const textarea = container.nextElementSibling;
            if (textarea && textarea.classList.contains('editorjs-textarea')) {
                // This container might need initialization
                // Check if it's already initialized by looking for Editor.js elements
                if (!container.querySelector('.ce-toolbar')) {
                    // Not initialized, try to initialize with default config
                    const editorId = container.id.replace('_editor', '');
                    if (editorId) {
                        window.initializeEditorJS(editorId, {
                            tools: getDefaultTools(),
                            data: { blocks: [] },
                            placeholder: 'Start writing...',
                            minHeight: 300
                        });
                    }
                }
            }
        });
    });

    // Helper function to get default tools configuration
    function getDefaultTools() {
        return {
            header: {
                class: window.Header,
                inlineToolbar: true,
                config: {
                    placeholder: 'Enter a header',
                    levels: [1, 2, 3, 4, 5, 6],
                    defaultLevel: 2
                }
            },
            paragraph: {
                class: window.Paragraph,
                inlineToolbar: true,
                config: {
                    placeholder: 'Enter text...'
                }
            },
            list: {
                class: window.List,
                inlineToolbar: true,
                config: {
                    defaultStyle: 'unordered'
                }
            }
        };
    }

    // Handle form submission to ensure editor data is saved
    document.addEventListener('submit', function(event) {
        const form = event.target;
        if (form && form.tagName === 'FORM') {
            // Find all editor instances in this form
            const editorContainers = form.querySelectorAll('.editorjs-editor');
            let hasErrors = false;

            editorContainers.forEach(function(container) {
                const textarea = container.nextElementSibling;
                if (textarea && textarea.classList.contains('editorjs-textarea')) {
                    const editorId = container.id.replace('_editor', '');
                    const editor = window.editorjsInstances[editorId];
                    
                    if (editor) {
                        // Force save current content to textarea
                        editor.save().then(function(savedData) {
                            textarea.value = JSON.stringify(savedData);
                        }).catch(function(error) {
                            console.error('Error saving editor content on form submit:', error);
                            hasErrors = true;
                        });
                    }
                }
            });

            if (hasErrors) {
                event.preventDefault();
                alert('There was an error saving the editor content. Please try again.');
            }
        }
    });

    // Handle window unload to warn about unsaved changes (optional)
    window.addEventListener('beforeunload', function(event) {
        const hasUnsavedChanges = Object.keys(window.editorjsInstances).some(function(editorId) {
            const editor = window.editorjsInstances[editorId];
            // This is a simplified check - in a real implementation you'd track changes
            return editor && editor.configuration && !editor.configuration.readOnly;
        });

        if (hasUnsavedChanges) {
            event.preventDefault();
            event.returnValue = 'You have unsaved changes. Are you sure you want to leave?';
        }
    });

})();