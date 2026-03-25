/**
 * BeyondCode AI - Block Builder
 * Drag and drop interface for building content with blocks
 */

document.addEventListener('DOMContentLoaded', function() {
    initBlockBuilder();
    initGrapesJS();
});

/**
 * Main Block Builder Initialization
 */
function initBlockBuilder() {
    const canvas = document.getElementById('content-canvas');
    const clearCanvasBtn = document.getElementById('clear-canvas');
    const saveContentBtn = document.getElementById('save-content');
    const previewContent = document.getElementById('preview-content');
    const editorContent = document.getElementById('block-editor-content');
    
    let blocks = [];
    let selectedBlockIndex = -1;
    
    // Initialize drag and drop
    initDragAndDrop();
    
    // Event listeners
    clearCanvasBtn.addEventListener('click', clearCanvas);
    saveContentBtn.addEventListener('click', saveContent);
    
    // Block type handlers
    const blockTypes = {
        'rich_text': {
            create: createRichTextBlock,
            render: renderRichTextBlock,
            edit: editRichTextBlock
        },
        'callout': {
            create: createCalloutBlock,
            render: renderCalloutBlock,
            edit: editCalloutBlock
        },
        'feature_grid': {
            create: createFeatureGridBlock,
            render: renderFeatureGridBlock,
            edit: editFeatureGridBlock
        },
        'cta': {
            create: createCTABlock,
            render: renderCTABlock,
            edit: editCTABlock
        },
        'pricing_table': {
            create: createPricingTableBlock,
            render: renderPricingTableBlock,
            edit: editPricingTableBlock
        },
        'faq': {
            create: createFAQBlock,
            render: renderFAQBlock,
            edit: editFAQBlock
        },
        'comparison_table': {
            create: createComparisonTableBlock,
            render: renderComparisonTableBlock,
            edit: editComparisonTableBlock
        },
        'image': {
            create: createImageBlock,
            render: renderImageBlock,
            edit: editImageBlock
        },
        'video': {
            create: createVideoBlock,
            render: renderVideoBlock,
            edit: editVideoBlock
        },
        'testimonial': {
            create: createTestimonialBlock,
            render: renderTestimonialBlock,
            edit: editTestimonialBlock
        },
        'stats': {
            create: createStatsBlock,
            render: renderStatsBlock,
            edit: editStatsBlock
        },
        'contact_form': {
            create: createContactFormBlock,
            render: renderContactFormBlock,
            edit: editContactFormBlock
        }
    };
    
    /**
     * Initialize Drag and Drop
     */
    function initDragAndDrop() {
        const blockTypes = document.querySelectorAll('.block-type');
        
        blockTypes.forEach(blockType => {
            blockType.addEventListener('dragstart', function(e) {
                e.dataTransfer.setData('text/plain', this.dataset.blockType);
                e.dataTransfer.effectAllowed = 'copy';
            });
        });
        
        canvas.addEventListener('dragover', function(e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
            this.classList.add('drag-over');
        });
        
        canvas.addEventListener('dragleave', function() {
            this.classList.remove('drag-over');
        });
        
        canvas.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');
            
            const blockType = e.dataTransfer.getData('text/plain');
            if (blockType && blockTypes[blockType]) {
                addBlock(blockType);
            }
        });
    }
    
    /**
     * Add Block to Canvas
     */
    function addBlock(type) {
        const blockData = blockTypes[type].create();
        blocks.push(blockData);
        renderCanvas();
        renderPreview();
    }
    
    /**
     * Render Canvas
     */
    function renderCanvas() {
        canvas.innerHTML = '';
        
        if (blocks.length === 0) {
            const placeholder = document.createElement('div');
            placeholder.className = 'canvas-placeholder';
            placeholder.innerHTML = '<p>Drag blocks from the palette to start building your content</p>';
            canvas.appendChild(placeholder);
            return;
        }
        
        blocks.forEach((block, index) => {
            const blockElement = document.createElement('div');
            blockElement.className = 'canvas-block';
            blockElement.dataset.index = index;
            
            const blockContent = blockTypes[block.type].render(block);
            blockElement.innerHTML = blockContent;
            
            // Add controls
            const controls = document.createElement('div');
            controls.className = 'block-controls';
            controls.innerHTML = `
                <button class="control-btn edit-btn" title="Edit">✏️</button>
                <button class="control-btn delete-btn" title="Delete">🗑️</button>
                <button class="control-btn move-up-btn" title="Move Up">⬆️</button>
                <button class="control-btn move-down-btn" title="Move Down">⬇️</button>
            `;
            
            blockElement.appendChild(controls);
            
            // Event listeners for controls
            controls.querySelector('.edit-btn').addEventListener('click', () => selectBlock(index));
            controls.querySelector('.delete-btn').addEventListener('click', () => deleteBlock(index));
            controls.querySelector('.move-up-btn').addEventListener('click', () => moveBlock(index, 'up'));
            controls.querySelector('.move-down-btn').addEventListener('click', () => moveBlock(index, 'down'));
            
            // Click to select
            blockElement.addEventListener('click', () => selectBlock(index));
            
            canvas.appendChild(blockElement);
        });
    }
    
    /**
     * Select Block for Editing
     */
    function selectBlock(index) {
        selectedBlockIndex = index;
        
        // Remove previous selection
        const previousSelection = canvas.querySelector('.canvas-block.selected');
        if (previousSelection) {
            previousSelection.classList.remove('selected');
        }
        
        // Add selection
        const blockElement = canvas.querySelector(`.canvas-block[data-index="${index}"]`);
        if (blockElement) {
            blockElement.classList.add('selected');
        }
        
        // Render editor
        renderEditor();
    }
    
    /**
     * Render Block Editor
     */
    function renderEditor() {
        if (selectedBlockIndex === -1) {
            editorContent.innerHTML = '<p class="editor-placeholder">Select a block to edit its content</p>';
            return;
        }
        
        const block = blocks[selectedBlockIndex];
        const editorTemplate = document.getElementById(`editor-template-${block.type}`);
        
        if (!editorTemplate) {
            editorContent.innerHTML = '<p class="editor-error">No editor available for this block type.</p>';
            return;
        }
        
        editorContent.innerHTML = editorTemplate.innerHTML;
        
        // Populate form with current data
        blockTypes[block.type].edit(block, selectedBlockIndex);
        
        // Add save button
        const saveBtn = document.createElement('button');
        saveBtn.className = 'btn btn-primary editor-save-btn';
        saveBtn.textContent = 'Save Changes';
        saveBtn.addEventListener('click', saveBlockChanges);
        
        editorContent.appendChild(saveBtn);
    }
    
    /**
     * Save Block Changes
     */
    function saveBlockChanges() {
        if (selectedBlockIndex === -1) return;
        
        const block = blocks[selectedBlockIndex];
        const updatedBlock = blockTypes[block.type].save(selectedBlockIndex);
        
        if (updatedBlock) {
            blocks[selectedBlockIndex] = updatedBlock;
            renderCanvas();
            renderPreview();
            showNotification('Block updated successfully!');
        }
    }
    
    /**
     * Delete Block
     */
    function deleteBlock(index) {
        if (confirm('Are you sure you want to delete this block?')) {
            blocks.splice(index, 1);
            selectedBlockIndex = -1;
            renderCanvas();
            renderPreview();
            renderEditor();
            showNotification('Block deleted successfully!');
        }
    }
    
    /**
     * Move Block
     */
    function moveBlock(index, direction) {
        if (direction === 'up' && index > 0) {
            [blocks[index], blocks[index - 1]] = [blocks[index - 1], blocks[index]];
            selectedBlockIndex = index - 1;
        } else if (direction === 'down' && index < blocks.length - 1) {
            [blocks[index], blocks[index + 1]] = [blocks[index + 1], blocks[index]];
            selectedBlockIndex = index + 1;
        }
        
        renderCanvas();
        renderPreview();
        renderEditor();
    }
    
    /**
     * Clear Canvas
     */
    function clearCanvas() {
        if (confirm('Are you sure you want to clear all content?')) {
            blocks = [];
            selectedBlockIndex = -1;
            renderCanvas();
            renderPreview();
            renderEditor();
            showNotification('Canvas cleared successfully!');
        }
    }
    
    /**
     * Save Content
     */
    function saveContent() {
        const content = {
            blocks: blocks
        };
        
        // Here you would typically send this to your server
        console.log('Content to save:', JSON.stringify(content, null, 2));
        
        // For now, just show a notification
        showNotification('Content saved successfully! (Check console for JSON)');
    }
    
    /**
     * Render Preview
     */
    function renderPreview() {
        previewContent.innerHTML = '';
        
        blocks.forEach(block => {
            const blockElement = document.createElement('div');
            blockElement.className = 'preview-block';
            blockElement.innerHTML = blockTypes[block.type].render(block);
            previewContent.appendChild(blockElement);
        });
    }
    
    /**
     * Show Notification
     */
    function showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    /**
     * Block Creation Functions
     */
    function createRichTextBlock() {
        return {
            type: 'rich_text',
            content: {
                time: Date.now(),
                version: '2.30.2',
                blocks: [
                    {
                        type: 'paragraph',
                        data: {
                            text: 'Start typing your content here...'
                        }
                    }
                ]
            }
        };
    }
    
    function createCalloutBlock() {
        return {
            type: 'callout',
            title: 'Important Notice',
            body: 'This is a callout block. Use it to highlight important information.'
        };
    }
    
    function createFeatureGridBlock() {
        return {
            type: 'feature_grid',
            title: 'Our Features',
            items: [
                {
                    title: 'Feature 1',
                    body: 'Description of feature 1'
                },
                {
                    title: 'Feature 2',
                    body: 'Description of feature 2'
                }
            ]
        };
    }
    
    function createCTABlock() {
        return {
            type: 'cta',
            title: 'Ready to get started?',
            body: 'Join thousands of satisfied customers today.',
            button_label: 'Get Started',
            button_url: '#'
        };
    }
    
    function createPricingTableBlock() {
        return {
            type: 'pricing_table',
            title: 'Choose Your Plan',
            plans: [
                {
                    title: 'Basic',
                    price: '$9.99/mo',
                    features: ['Feature 1', 'Feature 2']
                },
                {
                    title: 'Premium',
                    price: '$19.99/mo',
                    features: ['Feature 1', 'Feature 2', 'Feature 3']
                }
            ]
        };
    }
    
    function createFAQBlock() {
        return {
            type: 'faq',
            title: 'Frequently Asked Questions',
            items: [
                {
                    question: 'What is this?',
                    answer: 'This is a sample FAQ item.'
                }
            ]
        };
    }
    
    function createComparisonTableBlock() {
        return {
            type: 'comparison_table',
            title: 'Feature Comparison',
            headers: ['Feature', 'Basic', 'Premium'],
            rows: [
                ['Feature 1', '✓', '✓'],
                ['Feature 2', '✗', '✓']
            ]
        };
    }
    
    function createImageBlock() {
        return {
            type: 'image',
            image_url: '',
            alt_text: '',
            caption: ''
        };
    }
    
    function createVideoBlock() {
        return {
            type: 'video',
            video_url: '',
            caption: ''
        };
    }
    
    function createTestimonialBlock() {
        return {
            type: 'testimonial',
            quote: 'This is an amazing product!',
            author: 'Happy Customer',
            company: 'Acme Inc.'
        };
    }
    
    function createStatsBlock() {
        return {
            type: 'stats',
            title: 'Our Numbers',
            items: [
                {
                    value: '1000+',
                    label: 'Happy Customers'
                },
                {
                    value: '99.9%',
                    label: 'Uptime'
                }
            ]
        };
    }
    
    function createContactFormBlock() {
        return {
            type: 'contact_form',
            title: 'Get in Touch',
            description: 'Fill out the form below and we\'ll get back to you soon.'
        };
    }
    
    /**
     * Block Rendering Functions
     */
    function renderRichTextBlock(block) {
        let html = '<div class="block-preview rich-text-preview">';
        html += '<h4>Rich Text Block</h4>';
        html += '<p>Content: ' + (block.content.blocks.length) + ' blocks</p>';
        html += '</div>';
        return html;
    }
    
    function renderCalloutBlock(block) {
        let html = '<div class="block-preview callout-preview">';
        html += '<h4>Callout Block</h4>';
        html += '<p><strong>' + (block.title || 'No title') + '</strong></p>';
        html += '<p>' + (block.body || 'No content') + '</p>';
        html += '</div>';
        return html;
    }
    
    function renderFeatureGridBlock(block) {
        let html = '<div class="block-preview feature-grid-preview">';
        html += '<h4>Feature Grid Block</h4>';
        html += '<p><strong>' + (block.title || 'No title') + '</strong></p>';
        html += '<p>' + (block.items ? block.items.length : 0) + ' features</p>';
        html += '</div>';
        return html;
    }
    
    function renderCTABlock(block) {
        let html = '<div class="block-preview cta-preview">';
        html += '<h4>CTA Block</h4>';
        html += '<p><strong>' + (block.title || 'No title') + '</strong></p>';
        html += '<p>' + (block.button_label || 'No button') + '</p>';
        html += '</div>';
        return html;
    }
    
    function renderPricingTableBlock(block) {
        let html = '<div class="block-preview pricing-table-preview">';
        html += '<h4>Pricing Table Block</h4>';
        html += '<p><strong>' + (block.title || 'No title') + '</strong></p>';
        html += '<p>' + (block.plans ? block.plans.length : 0) + ' plans</p>';
        html += '</div>';
        return html;
    }
    
    function renderFAQBlock(block) {
        let html = '<div class="block-preview faq-preview">';
        html += '<h4>FAQ Block</h4>';
        html += '<p><strong>' + (block.title || 'No title') + '</strong></p>';
        html += '<p>' + (block.items ? block.items.length : 0) + ' questions</p>';
        html += '</div>';
        return html;
    }
    
    function renderComparisonTableBlock(block) {
        let html = '<div class="block-preview comparison-table-preview">';
        html += '<h4>Comparison Table Block</h4>';
        html += '<p><strong>' + (block.title || 'No title') + '</strong></p>';
        html += '<p>' + (block.headers ? block.headers.length : 0) + ' columns</p>';
        html += '</div>';
        return html;
    }
    
    function renderImageBlock(block) {
        let html = '<div class="block-preview image-preview">';
        html += '<h4>Image Block</h4>';
        html += '<p>' + (block.image_url ? 'Image URL provided' : 'No image URL') + '</p>';
        html += '</div>';
        return html;
    }
    
    function renderVideoBlock(block) {
        let html = '<div class="block-preview video-preview">';
        html += '<h4>Video Block</h4>';
        html += '<p>' + (block.video_url ? 'Video URL provided' : 'No video URL') + '</p>';
        html += '</div>';
        return html;
    }
    
    function renderTestimonialBlock(block) {
        let html = '<div class="block-preview testimonial-preview">';
        html += '<h4>Testimonial Block</h4>';
        html += '<p><strong>' + (block.author || 'No author') + '</strong></p>';
        html += '<p>' + (block.quote || 'No quote') + '</p>';
        html += '</div>';
        return html;
    }
    
    function renderStatsBlock(block) {
        let html = '<div class="block-preview stats-preview">';
        html += '<h4>Stats Block</h4>';
        html += '<p><strong>' + (block.title || 'No title') + '</strong></p>';
        html += '<p>' + (block.items ? block.items.length : 0) + ' stats</p>';
        html += '</div>';
        return html;
    }
    
    function renderContactFormBlock(block) {
        let html = '<div class="block-preview contact-form-preview">';
        html += '<h4>Contact Form Block</h4>';
        html += '<p><strong>' + (block.title || 'No title') + '</strong></p>';
        html += '<p>' + (block.description || 'No description') + '</p>';
        html += '</div>';
        return html;
    }
    
    /**
     * Block Editing Functions
     */
    function editRichTextBlock(block, index) {
        const contentInput = editorContent.querySelector('.editor-content-input');
        if (contentInput) {
            contentInput.value = JSON.stringify(block.content, null, 2);
        }
    }
    
    function saveRichTextBlock(index) {
        const contentInput = editorContent.querySelector('.editor-content-input');
        if (contentInput) {
            try {
                const content = JSON.parse(contentInput.value);
                blocks[index].content = content;
                return blocks[index];
            } catch (e) {
                alert('Invalid JSON format for content');
                return null;
            }
        }
        return blocks[index];
    }
    
    // Add save methods to block types
    Object.keys(blockTypes).forEach(type => {
        if (!blockTypes[type].save) {
            blockTypes[type].save = function(index) {
                return blocks[index];
            };
        }
    });
    
    // Override save methods for blocks that need special handling
    blockTypes.rich_text.save = saveRichTextBlock;
    
    // Initialize
    renderCanvas();
    renderPreview();
}

/**
 * Initialize GrapesJS Editor
 */
function initGrapesJS() {
    // Check if GrapesJS is available
    if (typeof grapesjs === 'undefined') {
        console.warn('GrapesJS not loaded, skipping initialization');
        return;
    }
    
    // Initialize GrapesJS editor
    const editor = grapesjs.init({
        container: '#content-canvas',
        fromElement: true,
        height: '600px',
        width: 'auto',
        storageManager: false, // Disable default storage
        assetManager: {
            upload: '/upload-image/',   // Django endpoint
            uploadName: 'files',
            assets: [],
            autoAdd: true,
            dropzone: true,
            credentials: 'include', 
            openAssetsOnDrop: true,
            // Configure headers for CSRF protection
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        },
        plugins: ['gjs-blocks-basic'],
        pluginsOpts: {
            'gjs-blocks-basic': {}
        }
    });
    
    // Fix Image Upload Issues for Block Builder
    fixImageUpload(editor);
    
    // Add custom blocks for our content types
    const blockManager = editor.BlockManager;
    
    // Add image block with upload capability
    blockManager.add('image-upload', {
        label: 'Image Upload',
        category: 'Media',
        content: '<img src="" style="max-width: 100%; height: auto;" />',
        attributes: { class: 'fa fa-image' },
        activate: true,
        select: true
    });
    
    // Add other custom blocks as needed
    blockManager.add('custom-text', {
        label: 'Custom Text',
        category: 'Content',
        content: '<div class="custom-text">Custom text block</div>',
        attributes: { class: 'fa fa-text-width' }
    });
    
    console.log('GrapesJS initialized with image upload support');
    
    return editor;
}

/**
 * Fix Image Upload Issues for Block Builder
 * Addresses: click not opening file dialog, missing HTML input, drag-drop not working
 */
function fixImageUpload(editor) {
    // Debug: Log the upload URL being used
    console.log('UPLOAD URL:', '/upload-image/');
    
    // 1. Enable file picker manually because default trigger is not working
    editor.AssetManager.getConfig().uploadFile = function(e) {
        const files = e.dataTransfer ? e.dataTransfer.files : e.target.files;
        const formData = new FormData();

        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        // Hard override uploadFile to force correct endpoint
        fetch('/upload-image/', {
            method: 'POST',
            body: formData,
            credentials: 'include',   // 🔥 REQUIRED
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(res => res.json())
        .then(data => {
            editor.AssetManager.add(data.data);
        })
        .catch(err => console.error('Upload error:', err));
    };

    // 2. Fix "click not opening file dialog" by forcing input trigger
    editor.on('asset:open', () => {
        const input = document.querySelector('.gjs-am-file-input');
        if (input) {
            input.click();
        }
    });

    // 3. Ensure HTML input exists (GrapesJS sometimes fails to render it)
    setTimeout(() => {
        if (!document.querySelector('.gjs-am-file-input')) {
            const input = document.createElement('input');
            input.type = 'file';
            input.multiple = true;
            input.className = 'gjs-am-file-input';
            input.style.display = 'none';
            input.accept = 'image/*';
            document.body.appendChild(input);

            input.addEventListener('change', (e) => {
                editor.AssetManager.getConfig().uploadFile(e);
            });
        }
    }, 1000);

    // 4. Ensure drag-drop works by configuring asset manager properly
    const assetManager = editor.AssetManager;
    const config = assetManager.getConfig();
    
    // Make sure dropzone is enabled
    if (config.dropzone !== true) {
        config.dropzone = true;
        config.openAssetsOnDrop = true;
    }

    // 5. Add event listener for drag and drop on the editor container
    const editorContainer = document.querySelector('#content-canvas');
    if (editorContainer) {
        editorContainer.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.stopPropagation();
        });

        editorContainer.addEventListener('drop', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                editor.AssetManager.getConfig().uploadFile(e);
            }
        });
    }
}

/**
 * Get CSRF token for AJAX requests (cookie-based)
 */
function getCsrfToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
}
