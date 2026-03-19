(function() {
    'use strict';

    /**
     * Editor.js Drag and Drop Plugin
     * Enables drag-and-drop reordering of blocks within the editor
     */
    class DragDrop {
        constructor({ editor, config = {} }) {
            this.editor = editor;
            this.config = config;
            this.isDragging = false;
            this.draggedBlock = null;
            this.draggedIndex = -1;
            this.placeholder = null;
            this.dropTarget = null;
            
            this.init();
        }

        init() {
            // Add CSS styles for drag and drop
            this.addStyles();
            
            // Listen for editor ready event
            this.editor.onReady(() => {
                this.setupDragDrop();
            });
        }

        addStyles() {
            const style = document.createElement('style');
            style.textContent = `
                /* Drag and Drop Styles */
                .ce-block {
                    position: relative;
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                }
                
                .ce-block.dragging {
                    opacity: 0.5;
                    transform: scale(0.98);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                    z-index: 1000;
                }
                
                .ce-block.drag-over {
                    border-top: 2px solid #007bff;
                    border-bottom: 2px solid #007bff;
                    background-color: #f8f9fa;
                }
                
                .ce-block.drag-over-top {
                    border-top: 2px solid #007bff;
                }
                
                .ce-block.drag-over-bottom {
                    border-bottom: 2px solid #007bff;
                }
                
                .editor-js-drag-handle {
                    position: absolute;
                    left: -40px;
                    top: 50%;
                    transform: translateY(-50%);
                    width: 32px;
                    height: 32px;
                    background: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 4px;
                    cursor: grab;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    opacity: 0;
                    transition: opacity 0.2s ease;
                    z-index: 10;
                }
                
                .ce-block:hover .editor-js-drag-handle {
                    opacity: 1;
                }
                
                .editor-js-drag-handle:active {
                    cursor: grabbing;
                    background: #e9ecef;
                }
                
                .editor-js-drag-handle svg {
                    width: 16px;
                    height: 16px;
                    fill: #6c757d;
                }
                
                .editor-js-drag-placeholder {
                    border: 2px dashed #007bff;
                    background: rgba(0, 123, 255, 0.1);
                    min-height: 40px;
                    margin: 5px 0;
                    border-radius: 4px;
                }
            `;
            document.head.appendChild(style);
        }

        setupDragDrop() {
            const editorWrapper = document.querySelector('.codex-editor');
            if (!editorWrapper) return;

            // Add drag handles to existing blocks
            this.addDragHandles();
            
            // Listen for new blocks being added
            this.observeNewBlocks();
            
            // Setup global event listeners
            document.addEventListener('mousedown', this.onMouseDown.bind(this));
            document.addEventListener('mousemove', this.onMouseMove.bind(this));
            document.addEventListener('mouseup', this.onMouseUp.bind(this));
        }

        addDragHandles() {
            const blocks = document.querySelectorAll('.ce-block');
            blocks.forEach(block => {
                if (!block.querySelector('.editor-js-drag-handle')) {
                    this.createDragHandle(block);
                }
            });
        }

        createDragHandle(block) {
            const handle = document.createElement('div');
            handle.className = 'editor-js-drag-handle';
            handle.innerHTML = `
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M11 18c0 1.1-.9 2-2 2s-2-.9-2-2 .9-2 2-2 2 .9 2 2zm-2-8c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0-6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm6 4c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
                </svg>
            `;
            
            block.appendChild(handle);
            
            // Make the entire block draggable
            block.style.cursor = 'grab';
            block.addEventListener('mousedown', (e) => {
                if (e.target.classList.contains('editor-js-drag-handle') || 
                    e.target.closest('.editor-js-drag-handle')) {
                    this.startDrag(block, e);
                }
            });
        }

        observeNewBlocks() {
            const editorWrapper = document.querySelector('.codex-editor');
            if (!editorWrapper) return;

            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    if (mutation.type === 'childList') {
                        mutation.addedNodes.forEach((node) => {
                            if (node.nodeType === 1 && node.classList && node.classList.contains('ce-block')) {
                                this.createDragHandle(node);
                            }
                        });
                    }
                });
            });

            observer.observe(editorWrapper, {
                childList: true,
                subtree: true
            });
        }

        startDrag(block, event) {
            this.isDragging = true;
            this.draggedBlock = block;
            this.draggedIndex = this.getBlockIndex(block);
            
            // Add dragging class
            block.classList.add('dragging');
            
            // Create placeholder
            this.createPlaceholder(block);
            
            // Prevent text selection
            event.preventDefault();
        }

        createPlaceholder(referenceBlock) {
            this.placeholder = document.createElement('div');
            this.placeholder.className = 'editor-js-drag-placeholder';
            this.placeholder.style.height = referenceBlock.offsetHeight + 'px';
            
            referenceBlock.parentNode.insertBefore(this.placeholder, referenceBlock);
        }

        onMouseMove(event) {
            if (!this.isDragging || !this.draggedBlock || !this.placeholder) return;

            const mouseY = event.clientY;
            const blocks = Array.from(document.querySelectorAll('.ce-block:not(.dragging)'));
            
            // Find the block we're hovering over
            let targetBlock = null;
            let position = 'before';
            
            for (let block of blocks) {
                const rect = block.getBoundingClientRect();
                const blockCenter = rect.top + rect.height / 2;
                
                if (mouseY < blockCenter) {
                    targetBlock = block;
                    position = 'before';
                    break;
                } else if (mouseY > rect.bottom) {
                    targetBlock = block;
                    position = 'after';
                }
            }

            // Update visual feedback
            this.updateVisualFeedback(targetBlock, position);
            
            // Move placeholder
            if (targetBlock) {
                if (position === 'before') {
                    targetBlock.parentNode.insertBefore(this.placeholder, targetBlock);
                } else {
                    targetBlock.parentNode.insertBefore(this.placeholder, targetBlock.nextSibling);
                }
            }
        }

        updateVisualFeedback(targetBlock, position) {
            // Remove previous drag-over classes
            document.querySelectorAll('.ce-block').forEach(block => {
                block.classList.remove('drag-over', 'drag-over-top', 'drag-over-bottom');
            });

            if (targetBlock) {
                targetBlock.classList.add('drag-over');
                if (position === 'before') {
                    targetBlock.classList.add('drag-over-top');
                } else {
                    targetBlock.classList.add('drag-over-bottom');
                }
            }
        }

        onMouseUp() {
            if (!this.isDragging) return;

            this.isDragging = false;
            
            if (this.draggedBlock && this.placeholder) {
                // Move the actual block to the placeholder position
                const placeholderParent = this.placeholder.parentNode;
                const nextSibling = this.placeholder.nextSibling;
                
                // Remove dragging class
                this.draggedBlock.classList.remove('dragging');
                
                // Remove placeholder
                this.placeholder.remove();
                this.placeholder = null;
                
                // Insert block at new position
                if (nextSibling) {
                    placeholderParent.insertBefore(this.draggedBlock, nextSibling);
                } else {
                    placeholderParent.appendChild(this.draggedBlock);
                }
                
                // Update editor's internal state
                this.updateEditorState();
            }
            
            // Remove drag-over classes
            document.querySelectorAll('.ce-block').forEach(block => {
                block.classList.remove('drag-over', 'drag-over-top', 'drag-over-bottom');
            });
        }

        getBlockIndex(block) {
            const blocks = Array.from(document.querySelectorAll('.ce-block'));
            return blocks.indexOf(block);
        }

        updateEditorState() {
            // Trigger editor update to reflect the new block order
            if (this.editor && this.editor.blocks) {
                // Get current blocks in order
                const blocks = Array.from(document.querySelectorAll('.ce-block'));
                const newBlocks = [];
                
                blocks.forEach(block => {
                    const blockId = block.getAttribute('data-block-id');
                    if (blockId) {
                        const blockData = this.editor.blocks.getBlockByIndex(this.getBlockIndex(block));
                        if (blockData) {
                            newBlocks.push(blockData);
                        }
                    }
                });
                
                // Re-render with new order (simplified approach)
                // In a real implementation, you'd use the editor's API to reorder blocks
                console.log('Blocks reordered, new order:', newBlocks.length);
            }
        }
    }

    // Export for use in other scripts
    if (typeof window !== 'undefined') {
        window.EditorJSDragDrop = DragDrop;
    }

    // Auto-initialize if editor is available
    if (typeof window !== 'undefined' && window.EditorJS) {
        document.addEventListener('DOMContentLoaded', () => {
            // Editor.js initialization would happen here
            // This plugin will be used when initializing the editor
        });
    }

})();