/**
 * BeyondCode AI - Post Editor
 * Block-based content editor for posts
 */

class PostEditor {
    constructor(config) {
        this.blocksContainer = config.blocksContainer;
        this.blockSelectorPanel = config.blockSelectorPanel;
        this.blockTypesGrid = config.blockTypesGrid;
        this.blocksJsonField = config.blocksJsonField;
        this.addBlockBtn = config.addBlockBtn;
        this.closeSelectorBtn = config.closeSelectorBtn;
        this.previewBtn = config.previewBtn;
        this.previewModal = config.previewModal;
        this.previewContent = config.previewContent;
        this.saveDraftBtn = config.saveDraftBtn;
        this.savePreviewBtn = config.savePreviewBtn;
        this.blockSearch = config.blockSearch;
        
        this.blocks = [];
        this.blockTypes = [];
        this.nextBlockId = 1;
        
        this.init();
    }
    
    init() {
        this.bindEvents();
    }
    
    initialize(blockTypes) {
        this.blockTypes = blockTypes;
        this.renderBlockTypes();
    }
    
    bindEvents() {
        // Add block button
        this.addBlockBtn.addEventListener('click', () => {
            this.showBlockSelector();
        });
        
        // Close selector button
        this.closeSelectorBtn.addEventListener('click', () => {
            this.hideBlockSelector();
        });
        
        // Preview button
        this.previewBtn.addEventListener('click', () => {
            this.previewContent();
        });
        
        // Save draft button
        this.saveDraftBtn.addEventListener('click', () => {
            this.saveAsDraft();
        });
        
        // Save and preview button
        this.savePreviewBtn.addEventListener('click', () => {
            this.saveAndPreview();
        });
        
        // Block search
        this.blockSearch.addEventListener('input', (e) => {
            this.filterBlockTypes(e.target.value);
        });
        
        // Click outside to close selector
        document.addEventListener('click', (e) => {
            if (!this.blockSelectorPanel.contains(e.target) && !this.addBlockBtn.contains(e.target)) {
                this.hideBlockSelector();
            }
        });
    }
    
    renderBlockTypes() {
        this.blockTypesGrid.innerHTML = '';
        
        this.blockTypes.forEach(blockType => {
            const blockCard = document.createElement('div');
            blockCard.className = 'block-card';
            blockCard.innerHTML = `
                <div class="block-card-content" data-block-type="${blockType.type}">
                    <div class="block-icon">${blockType.icon}</div>
                    <div class="block-info">
                        <h5 class="block-name">${blockType.name}</h5>
                        <p class="block-description">${blockType.description}</p>
                    </div>
                </div>
            `;
            
            blockCard.querySelector('.block-card-content').addEventListener('click', () => {
                this.addBlock(blockType.type);
                this.hideBlockSelector();
            });
            
            this.blockTypesGrid.appendChild(blockCard);
        });
    }
    
    filterBlockTypes(searchTerm) {
        const cards = this.blockTypesGrid.querySelectorAll('.block-card');
        
        cards.forEach(card => {
            const blockName = card.querySelector('.block-name').textContent.toLowerCase();
            const blockDescription = card.querySelector('.block-description').textContent.toLowerCase();
            const searchText = searchTerm.toLowerCase();
            
            if (blockName.includes(searchText) || blockDescription.includes(searchText)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    showBlockSelector() {
        this.blockSelectorPanel.style.display = 'block';
        this.blockSearch.value = '';
        this.filterBlockTypes('');
    }
    
    hideBlockSelector() {
        this.blockSelectorPanel.style.display = 'none';
    }
    
    addBlock(type) {
        const blockData = this.createBlockData(type);
        this.blocks.push(blockData);
        this.renderBlocks();
        this.updateBlocksJson();
    }
    
    createBlockData(type) {
        const baseData = {
            id: this.nextBlockId++,
            type: type,
            data: {}
        };
        
        switch (type) {
            case 'paragraph':
                return {
                    ...baseData,
                    data: {
                        text: 'Enter your paragraph text here...'
                    }
                };
                
            case 'heading':
                return {
                    ...baseData,
                    data: {
                        text: 'Enter your heading text here...',
                        level: 'h2'
                    }
                };
                
            case 'list':
                return {
                    ...baseData,
                    data: {
                        style: 'unordered',
                        items: ['List item 1', 'List item 2']
                    }
                };
                
            case 'quote':
                return {
                    ...baseData,
                    data: {
                        text: 'Enter your quote here...',
                        caption: ''
                    }
                };
                
            case 'code':
                return {
                    ...baseData,
                    data: {
                        code: '// Enter your code here...'
                    }
                };
                
            case 'classic':
                return {
                    ...baseData,
                    data: {
                        html: '<p>Enter your content with basic formatting here...</p>'
                    }
                };
                
            default:
                return baseData;
        }
    }
    
    renderBlocks() {
        this.blocksContainer.innerHTML = '';
        
        if (this.blocks.length === 0) {
            const emptyState = document.createElement('div');
            emptyState.className = 'empty-blocks-state';
            emptyState.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-plus-circle" style="font-size: 48px; color: #6c757d;"></i>
                    <h5 class="mt-3">No blocks added yet</h5>
                    <p class="text-muted">Click "Add Block" to start building your content</p>
                </div>
            `;
            this.blocksContainer.appendChild(emptyState);
            return;
        }
        
        this.blocks.forEach((block, index) => {
            const blockElement = this.createBlockElement(block, index);
            this.blocksContainer.appendChild(blockElement);
        });
    }
    
    createBlockElement(block, index) {
        const blockElement = document.createElement('div');
        blockElement.className = 'block-item';
        blockElement.dataset.index = index;
        
        const blockTemplate = document.querySelector(`.block-template[data-block-type="${block.type}"]`);
        if (!blockTemplate) {
            blockElement.innerHTML = `<div class="alert alert-warning">Block type "${block.type}" not supported</div>`;
            return blockElement;
        }
        
        const blockContent = blockTemplate.cloneNode(true);
        blockContent.style.display = 'block';
        
        // Populate block content with existing data
        this.populateBlockContent(blockContent, block);
        
        // Add controls
        const controls = document.createElement('div');
        controls.className = 'block-controls';
        controls.innerHTML = `
            <div class="btn-group" role="group">
                <button type="button" class="btn btn-sm btn-outline-primary move-up-btn" title="Move Up">
                    <i class="bi bi-arrow-up"></i>
                </button>
                <button type="button" class="btn btn-sm btn-outline-primary move-down-btn" title="Move Down">
                    <i class="bi bi-arrow-down"></i>
                </button>
                <button type="button" class="btn btn-sm btn-outline-danger delete-btn" title="Delete">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
            <span class="block-type-badge">${this.getBlockTypeName(block.type)}</span>
        `;
        
        // Bind control events
        controls.querySelector('.move-up-btn').addEventListener('click', () => this.moveBlock(index, 'up'));
        controls.querySelector('.move-down-btn').addEventListener('click', () => this.moveBlock(index, 'down'));
        controls.querySelector('.delete-btn').addEventListener('click', () => this.deleteBlock(index));
        
        blockElement.appendChild(controls);
        blockElement.appendChild(blockContent);
        
        return blockElement;
    }
    
    populateBlockContent(blockContent, block) {
        switch (block.type) {
            case 'paragraph':
                const paragraphInput = blockContent.querySelector('.block-input');
                if (paragraphInput) {
                    paragraphInput.value = block.data.text || '';
                    paragraphInput.addEventListener('input', (e) => {
                        this.updateBlockData(block.id, { text: e.target.value });
                    });
                }
                break;
                
            case 'heading':
                const headingInput = blockContent.querySelector('.block-input');
                const headingLevel = blockContent.querySelector('.block-level');
                
                if (headingInput) {
                    headingInput.value = block.data.text || '';
                    headingInput.addEventListener('input', (e) => {
                        this.updateBlockData(block.id, { text: e.target.value });
                    });
                }
                
                if (headingLevel) {
                    headingLevel.value = block.data.level || 'h2';
                    headingLevel.addEventListener('change', (e) => {
                        this.updateBlockData(block.id, { level: e.target.value });
                    });
                }
                break;
                
            case 'list':
                const listStyle = blockContent.querySelector('.block-style');
                const listItemsContainer = blockContent.querySelector('.list-items');
                const addListItemBtn = blockContent.querySelector('.add-list-item');
                
                if (listStyle) {
                    listStyle.value = block.data.style || 'unordered';
                    listStyle.addEventListener('change', (e) => {
                        this.updateBlockData(block.id, { style: e.target.value });
                    });
                }
                
                if (listItemsContainer) {
                    listItemsContainer.innerHTML = '';
                    const items = block.data.items || ['List item 1'];
                    
                    items.forEach((item, itemIndex) => {
                        const listItem = document.createElement('div');
                        listItem.className = 'list-item';
                        listItem.innerHTML = `
                            <input type="text" class="form-control" value="${item}" placeholder="List item...">
                            <button type="button" class="btn btn-sm btn-outline-danger remove-list-item">Remove</button>
                        `;
                        
                        listItem.querySelector('input').addEventListener('input', (e) => {
                            const newItems = [...(block.data.items || [])];
                            newItems[itemIndex] = e.target.value;
                            this.updateBlockData(block.id, { items: newItems });
                        });
                        
                        listItem.querySelector('.remove-list-item').addEventListener('click', () => {
                            const newItems = [...(block.data.items || [])];
                            newItems.splice(itemIndex, 1);
                            this.updateBlockData(block.id, { items: newItems });
                            this.renderBlocks();
                        });
                        
                        listItemsContainer.appendChild(listItem);
                    });
                }
                
                if (addListItemBtn) {
                    addListItemBtn.addEventListener('click', () => {
                        const newItems = [...(block.data.items || []), 'New list item'];
                        this.updateBlockData(block.id, { items: newItems });
                        this.renderBlocks();
                    });
                }
                break;
                
            case 'quote':
                const quoteInput = blockContent.querySelector('.block-input');
                const quoteCitation = blockContent.querySelector('.block-citation');
                
                if (quoteInput) {
                    quoteInput.value = block.data.text || '';
                    quoteInput.addEventListener('input', (e) => {
                        this.updateBlockData(block.id, { text: e.target.value });
                    });
                }
                
                if (quoteCitation) {
                    quoteCitation.value = block.data.caption || '';
                    quoteCitation.addEventListener('input', (e) => {
                        this.updateBlockData(block.id, { caption: e.target.value });
                    });
                }
                break;
                
            case 'code':
                const codeInput = blockContent.querySelector('.block-input');
                const codeLanguage = blockContent.querySelector('.block-language');
                
                if (codeInput) {
                    codeInput.value = block.data.code || '';
                    codeInput.addEventListener('input', (e) => {
                        this.updateBlockData(block.id, { code: e.target.value });
                    });
                }
                
                if (codeLanguage) {
                    codeLanguage.value = block.data.language || '';
                    codeLanguage.addEventListener('input', (e) => {
                        this.updateBlockData(block.id, { language: e.target.value });
                    });
                }
                break;
                
            case 'classic':
                const classicInput = blockContent.querySelector('.block-input');
                
                if (classicInput) {
                    classicInput.value = block.data.html || '';
                    classicInput.addEventListener('input', (e) => {
                        this.updateBlockData(block.id, { html: e.target.value });
                    });
                }
                break;
        }
    }
    
    updateBlockData(blockId, newData) {
        const blockIndex = this.blocks.findIndex(block => block.id === blockId);
        if (blockIndex !== -1) {
            this.blocks[blockIndex].data = { ...this.blocks[blockIndex].data, ...newData };
            this.updateBlocksJson();
        }
    }
    
    deleteBlock(index) {
        if (confirm('Are you sure you want to delete this block?')) {
            this.blocks.splice(index, 1);
            this.renderBlocks();
            this.updateBlocksJson();
        }
    }
    
    moveBlock(index, direction) {
        if (direction === 'up' && index > 0) {
            [this.blocks[index], this.blocks[index - 1]] = [this.blocks[index - 1], this.blocks[index]];
        } else if (direction === 'down' && index < this.blocks.length - 1) {
            [this.blocks[index], this.blocks[index + 1]] = [this.blocks[index + 1], this.blocks[index]];
        }
        
        this.renderBlocks();
        this.updateBlocksJson();
    }
    
    updateBlocksJson() {
        this.blocksJsonField.value = JSON.stringify(this.blocks);
    }
    
    loadBlocks(blocksData) {
        this.blocks = blocksData || [];
        this.renderBlocks();
        this.updateBlocksJson();
    }
    
    previewContent() {
        const previewHtml = this.renderPreviewHtml();
        this.previewContent.innerHTML = previewHtml;
        this.previewModal.show();
    }
    
    renderPreviewHtml() {
        let html = '';
        
        this.blocks.forEach(block => {
            switch (block.type) {
                case 'paragraph':
                    html += `<p>${this.escapeHtml(block.data.text || '')}</p>`;
                    break;
                    
                case 'heading':
                    const level = block.data.level || 'h2';
                    html += `<${level}>${this.escapeHtml(block.data.text || '')}</${level}>`;
                    break;
                    
                case 'list':
                    const tag = block.data.style === 'ordered' ? 'ol' : 'ul';
                    html += `<${tag}>`;
                    (block.data.items || []).forEach(item => {
                        html += `<li>${this.escapeHtml(item)}</li>`;
                    });
                    html += `</${tag}>`;
                    break;
                    
                case 'quote':
                    html += `<blockquote>`;
                    html += `<p>${this.escapeHtml(block.data.text || '')}</p>`;
                    if (block.data.caption) {
                        html += `<footer>${this.escapeHtml(block.data.caption)}</footer>`;
                    }
                    html += `</blockquote>`;
                    break;
                    
                case 'code':
                    html += `<pre><code class="${block.data.language || ''}">${this.escapeHtml(block.data.code || '')}</code></pre>`;
                    break;
                    
                case 'classic':
                    html += block.data.html || '';
                    break;
            }
        });
        
        return html;
    }
    
    saveAsDraft() {
        // Set status to draft
        const statusField = document.querySelector('select[name="status"]');
        if (statusField) {
            statusField.value = 'draft';
        }
        
        // Submit form
        document.getElementById('post-form').submit();
    }
    
    saveAndPreview() {
        // Save the form first
        document.getElementById('post-form').submit();
        
        // Then show preview after a short delay
        setTimeout(() => {
            this.previewContent();
        }, 1000);
    }
    
    getBlockTypeName(type) {
        const blockType = this.blockTypes.find(bt => bt.type === type);
        return blockType ? blockType.name : type;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Add some CSS styles for the block editor
const style = document.createElement('style');
style.textContent = `
    .block-selector-panel {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        z-index: 1000;
        min-width: 400px;
        max-width: 600px;
        max-height: 80vh;
        overflow: hidden;
    }
    
    .block-selector-header {
        padding: 15px;
        border-bottom: 1px solid #dee2e6;
        background: #f8f9fa;
    }
    
    .block-types-grid {
        padding: 15px;
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        max-height: 60vh;
        overflow-y: auto;
    }
    
    .block-card {
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 10px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .block-card:hover {
        border-color: #007bff;
        background: #f8f9ff;
    }
    
    .block-card-content {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .block-icon {
        font-size: 24px;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #e9ecef;
        border-radius: 50%;
    }
    
    .block-name {
        margin: 0;
        font-size: 14px;
        font-weight: 600;
    }
    
    .block-description {
        margin: 0;
        font-size: 12px;
        color: #6c757d;
    }
    
    .blocks-container {
        min-height: 200px;
        border: 2px dashed #dee2e6;
        border-radius: 8px;
        padding: 20px;
    }
    
    .block-item {
        margin-bottom: 20px;
        padding: 15px;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        background: #fff;
        position: relative;
    }
    
    .block-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .block-type-badge {
        background: #e9ecef;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 500;
        color: #495057;
    }
    
    .empty-blocks-state {
        border: 2px dashed #dee2e6;
        border-radius: 8px;
        background: #f8f9fa;
    }
    
    .list-item {
        display: flex;
        gap: 10px;
        margin-bottom: 5px;
    }
    
    .list-item input {
        flex: 1;
    }
    
    .preview-content h1, .preview-content h2, .preview-content h3, .preview-content h4, .preview-content h5, .preview-content h6 {
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    .preview-content p {
        margin-bottom: 15px;
        line-height: 1.6;
    }
    
    .preview-content blockquote {
        border-left: 4px solid #007bff;
        padding: 15px 20px;
        background: #f8f9ff;
        margin: 20px 0;
    }
    
    .preview-content pre {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 4px;
        overflow-x: auto;
    }
    
    .preview-content code {
        font-family: 'Courier New', monospace;
    }
    
    .preview-content ul, .preview-content ol {
        margin: 15px 0;
        padding-left: 20px;
    }
`;
document.head.appendChild(style);