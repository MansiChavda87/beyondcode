/**
 * GrapesJS Widget JavaScript
 * Handles initialization and functionality for GrapesJS editor in Django admin
 */

window.initializeGrapesJS = function(editorId, options, initialData) {
    const editor = grapesjs.init({
        container: `#${editorId}`,
        fromElement: true,
        height: options.height || '600px',
        width: options.width || 'auto',
        storageManager: false, // Disable automatic storage as per requirements
        plugins: options.plugins || [],
        pluginsOpts: options.pluginsOpts || {},
        
        // Configure the editor
        blockManager: {
            appendTo: '#blocks-canvas',
        },
        
        styleManager: {
            sectors: [{
                name: 'General',
                open: false,
                buildProps: ['float', 'display', 'position', 'top', 'right', 'left', 'bottom']
            }, {
                name: 'Flex',
                open: false,
                buildProps: ['flex-direction', 'flex-wrap', 'justify-content', 'align-items', 'align-content', 'order', 'flex-grow', 'flex-shrink', 'flex-basis']
            }, {
                name: 'Dimension',
                open: false,
                buildProps: ['width', 'height', 'max-width', 'min-height', 'margin', 'padding']
            }, {
                name: 'Typography',
                open: false,
                buildProps: ['font-family', 'font-size', 'font-weight', 'letter-spacing', 'color', 'line-height', 'text-align', 'text-shadow']
            }, {
                name: 'Decorations',
                open: false,
                buildProps: ['border-radius-c', 'background-color', 'border', 'box-shadow', 'background']
            }, {
                name: 'Extra',
                open: false,
                buildProps: ['transition', 'transform']
            }],
        },
        
        // Configure panels
        panels: {
            defaults: [
                {
                    id: 'commands',
                    buttons: [
                        {
                            id: 'undo',
                            className: 'fa fa-undo',
                            command: 'core:undo',
                            attributes: { title: 'Undo' }
                        },
                        {
                            id: 'redo',
                            className: 'fa fa-repeat',
                            command: 'core:redo',
                            attributes: { title: 'Redo' }
                        }
                    ]
                },
                {
                    id: 'options',
                    buttons: [
                        {
                            id: 'preview',
                            className: 'fa fa-eye',
                            command: 'preview',
                            attributes: { title: 'Preview' }
                        },
                        {
                            id: 'fullscreen',
                            className: 'fa fa-arrows-alt',
                            command: 'fullscreen',
                            attributes: { title: 'Fullscreen' }
                        }
                    ]
                },
                {
                    id: 'views',
                    buttons: [
                        {
                            id: 'open-sm',
                            className: 'fa fa-paint-brush',
                            command: 'open-sm',
                            attributes: { title: 'Open Style Manager' }
                        },
                        {
                            id: 'open-tm',
                            className: 'fa fa-cog',
                            command: 'open-tm',
                            attributes: { title: 'Open Layer Manager' }
                        },
                        {
                            id: 'open-blocks',
                            className: 'fa fa-th-large',
                            command: 'open-blocks',
                            attributes: { title: 'Open Blocks' }
                        }
                    ]
                }
            ]
        },
        
        // Configure blocks
        blockManager: {
            appendTo: '#blocks-canvas',
        }
    });

    // Add custom blocks
    addCustomBlocks(editor);
    
    // Add layout blocks
    addLayoutBlocks(editor);
    
    // Handle data loading
    if (initialData && Object.keys(initialData).length > 0) {
        // If we have project data, load it
        if (initialData.html && initialData.css) {
            editor.setComponents(initialData.html);
            editor.setStyle(initialData.css);
        } else if (initialData.html) {
            editor.setComponents(initialData.html);
        } else if (initialData.blocks) {
            // Legacy Editor.js format - convert if needed
            editor.setComponents(initialData.blocks);
        }
    }

    // Handle data saving
    const textarea = document.getElementById(`${editorId}_textarea`);
    
    // Update textarea when editor changes
    editor.on('component:add component:remove component:update', function() {
        const html = editor.getHtml();
        const css = editor.getCss();
        const data = {
            html: html,
            css: css,
            components: editor.getComponents(),
            style: editor.getStyle()
        };
        
        if (textarea) {
            textarea.value = JSON.stringify(data);
        }
    });

    // Initial save
    setTimeout(() => {
        const html = editor.getHtml();
        const css = editor.getCss();
        const data = {
            html: html,
            css: css,
            components: editor.getComponents(),
            style: editor.getStyle()
        };
        
        if (textarea) {
            textarea.value = JSON.stringify(data);
        }
    }, 100);

    return editor;
};

/**
 * Add custom blocks to GrapesJS
 */
function addCustomBlocks(editor) {
    const bm = editor.BlockManager;

    // Section Block
    bm.add('section', {
        label: 'Section',
        category: 'Layout',
        content: `<section style="padding: 40px 20px; background: #f8f9fa;">
            <div style="max-width: 1200px; margin: 0 auto;">
                <h2>Section Title</h2>
                <p>This is a section with some content.</p>
            </div>
        </section>`,
        media: '<svg viewBox="0 0 24 24"><path d="M4 4h16v2H4zM4 8h16v2H4zM4 12h16v2H4zM4 16h16v2H4z"/></svg>',
    });

    // Text Block
    bm.add('text', {
        label: 'Text',
        category: 'Content',
        content: `<div style="padding: 20px;">
            <p>This is a text block. You can edit this content by clicking on it.</p>
        </div>`,
        media: '<svg viewBox="0 0 24 24"><path d="M4 6h16v2H4zM4 10h10v2H4zM4 14h16v2H4zM4 18h10v2H4z"/></svg>',
    });

    // Heading Block
    bm.add('heading', {
        label: 'Heading',
        category: 'Content',
        content: `<h2 style="font-size: 2rem; margin: 0 0 10px 0; color: #333;">Your Heading Here</h2>`,
        media: '<svg viewBox="0 0 24 24"><path d="M4 6h16v2H4zM4 10h10v2H4zM4 14h16v2H4zM4 18h10v2H4z"/></svg>',
    });

    // Paragraph Block
    bm.add('paragraph', {
        label: 'Paragraph',
        category: 'Content',
        content: `<p style="line-height: 1.6; color: #666; margin: 0 0 20px 0;">This is a paragraph of text. You can edit this content by clicking on it and typing.</p>`,
        media: '<svg viewBox="0 0 24 24"><path d="M4 6h16v2H4zM4 10h10v2H4zM4 14h16v2H4zM4 18h10v2H4z"/></svg>',
    });

    // List Block
    bm.add('list', {
        label: 'List',
        category: 'Content',
        content: `<ul style="padding-left: 20px; line-height: 1.6;">
            <li>First item</li>
            <li>Second item</li>
            <li>Third item</li>
        </ul>`,
        media: '<svg viewBox="0 0 24 24"><path d="M4 6h16v2H4zM4 10h10v2H4zM4 14h16v2H4zM4 18h10v2H4z"/></svg>',
    });

    // Image Block
    bm.add('image', {
        label: 'Image',
        category: 'Media',
        content: `<div style="padding: 20px; text-align: center;">
            <img src="https://via.placeholder.com/600x400" style="max-width: 100%; height: auto; border-radius: 8px;" alt="Placeholder Image">
        </div>`,
        media: '<svg viewBox="0 0 24 24"><path d="M4 4h16v16H4zM4 4l8 8 8-8M4 20l8-8 8 8"/></svg>',
    });

    // Button Block
    bm.add('button', {
        label: 'Button',
        category: 'Elements',
        content: `<div style="padding: 20px; text-align: center;">
            <a href="#" style="display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 4px; font-weight: bold;">Click Me</a>
        </div>`,
        media: '<svg viewBox="0 0 24 24"><path d="M4 4h16v16H4zM4 4l8 8 8-8M4 20l8-8 8 8"/></svg>',
    });

    // FAQ Block
    bm.add('faq', {
        label: 'FAQ',
        category: 'Content',
        content: `<div style="padding: 20px;">
            <div style="border-bottom: 1px solid #ddd; padding: 15px 0;">
                <h4 style="margin: 0 0 10px 0; color: #333;">Question 1</h4>
                <p style="margin: 0; color: #666;">Answer to the first question goes here.</p>
            </div>
            <div style="border-bottom: 1px solid #ddd; padding: 15px 0;">
                <h4 style="margin: 0 0 10px 0; color: #333;">Question 2</h4>
                <p style="margin: 0; color: #666;">Answer to the second question goes here.</p>
            </div>
        </div>`,
        media: '<svg viewBox="0 0 24 24"><path d="M4 6h16v2H4zM4 10h10v2H4zM4 14h16v2H4zM4 18h10v2H4z"/></svg>',
    });
}

/**
 * Add layout blocks (columns)
 */
function addLayoutBlocks(editor) {
    const bm = editor.BlockManager;

    // 2 Column Layout
    bm.add('two-columns', {
        label: '2 Columns',
        category: 'Layout',
        content: `
    <div style="display:flex; gap:20px; width:100%;">
      <div style="flex:1; padding:10px; border:1px solid #ddd;">
        Column 1
      </div>
      <div style="flex:1; padding:10px; border:1px solid #ddd;">
        Column 2
      </div>
    </div>
  `,
        media: '<svg viewBox="0 0 24 24"><path d="M4 4h16v16H4zM4 4l8 8 8-8M4 20l8-8 8 8"/></svg>',
    });

    // 3 Column Layout
    bm.add('three-columns', {
        label: '3 Columns',
        category: 'Layout',
        content: `
    <div style="display:flex; gap:20px; width:100%;">
      <div style="flex:1; padding:10px; border:1px solid #ddd;">Column 1</div>
      <div style="flex:1; padding:10px; border:1px solid #ddd;">Column 2</div>
      <div style="flex:1; padding:10px; border:1px solid #ddd;">Column 3</div>
    </div>
  `,
        media: '<svg viewBox="0 0 24 24"><path d="M4 4h16v16H4zM4 4l8 8 8-8M4 20l8-8 8 8"/></svg>',
    });
}