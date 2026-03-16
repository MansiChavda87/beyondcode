from django import forms
from django_editorjs import EditorJsWidget
from django.utils.safestring import mark_safe
from django.urls import reverse
import json


class EnhancedEditorJsWidget(EditorJsWidget):
    """
    Enhanced Editor.js widget with WordPress-like features
    """
    
    def __init__(self, *args, **kwargs):
        # Default Editor.js configuration with more tools
        default_config = {
            'tools': {
                'header': {
                    'class': 'Header',
                    'inlineToolbar': True,
                    'config': {
                        'placeholder': 'Enter a header...',
                        'levels': [1, 2, 3, 4, 5, 6],
                        'defaultLevel': 2
                    }
                },
                'paragraph': {
                    'class': 'Paragraph',
                    'inlineToolbar': True,
                    'config': {
                        'placeholder': 'Enter text...'
                    }
                },
                'list': {
                    'class': 'List',
                    'inlineToolbar': True,
                    'config': {
                        'defaultStyle': 'unordered'
                    }
                },
                'image': {
                    'class': 'ImageTool',
                    'config': {
                        'endpoints': {
                            'byFile': reverse('marketing:upload_image'),
                            'byUrl': reverse('marketing:upload_image')
                        },
                        'field': 'file',
                        'types': 'image/*',
                        'additionalRequestHeaders': {},
                        'additionalRequestData': {},
                        'captionPlaceholder': 'Image caption',
                        'buttonContent': 'Select an Image'
                    }
                },
                'linkTool': {
                    'class': 'LinkTool',
                    'config': {
                        'endpoint': reverse('marketing:search_content')
                    }
                },
                'embed': {
                    'class': 'Embed',
                    'config': {
                        'services': {
                            'youtube': True,
                            'vimeo': True,
                            'instagram': True,
                            'twitter': True,
                            'facebook': True
                        }
                    }
                },
                'quote': {
                    'class': 'Quote',
                    'inlineToolbar': True,
                    'config': {
                        'quotePlaceholder': 'Enter a quote',
                        'captionPlaceholder': 'Quote\'s author'
                    }
                },
                'code': {
                    'class': 'CodeTool',
                    'config': {
                        'placeholder': 'Enter code...'
                    }
                },
                'delimiter': {
                    'class': 'Delimiter'
                },
                'table': {
                    'class': 'Table',
                    'inlineToolbar': True,
                    'config': {
                        'rows': 2,
                        'cols': 3
                    }
                },
                'warning': {
                    'class': 'Warning',
                    'inlineToolbar': True,
                    'config': {
                        'titlePlaceholder': 'Title',
                        'messagePlaceholder': 'Message'
                    }
                },
                'checklist': {
                    'class': 'Checklist',
                    'inlineToolbar': True
                },
                'raw': {
                    'class': 'RawTool'
                },
                'marker': {
                    'class': 'Marker',
                    'shortcut': 'CMD+SHIFT+M'
                },
                'inlineCode': {
                    'class': 'InlineCode',
                    'shortcut': 'CMD+SHIFT+M'
                }
            },
            'holder': self.attrs.get('id', 'editorjs'),
            'placeholder': 'Start writing your content here...',
            'autofocus': True,
            'minHeight': 300,
            'logLevel': 'ERROR'
        }
        
        # Merge with any custom config
        if 'config' in kwargs:
            default_config.update(kwargs['config'])
            del kwargs['config']
        
        kwargs['config'] = default_config
        super().__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None, renderer=None):
        # Get the base widget HTML
        widget_html = super().render(name, value, attrs, renderer)
        
        # Add custom styling and enhancements
        enhanced_html = f'''
        <div class="editorjs-container">
            <div class="editorjs-toolbar">
                <div class="editorjs-actions">
                    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="saveDraft()">
                        <i class="fa fa-save"></i> Save Draft
                    </button>
                    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="previewContent()">
                        <i class="fa fa-eye"></i> Preview
                    </button>
                    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="clearEditor()">
                        <i class="fa fa-eraser"></i> Clear
                    </button>
                </div>
            </div>
            {widget_html}
            <div class="editorjs-footer">
                <small class="text-muted">Tip: Use / to see all available blocks</small>
            </div>
        </div>
        '''
        
        return mark_safe(enhanced_html)


class PostEditorWidget(EnhancedEditorJsWidget):
    """
    Specialized Editor.js widget for blog posts with post-specific tools
    """
    
    def __init__(self, *args, **kwargs):
        # Post-specific configuration
        post_config = {
            'tools': {
                'header': {
                    'class': 'Header',
                    'inlineToolbar': True,
                    'config': {
                        'placeholder': 'Post title...',
                        'levels': [1, 2, 3],
                        'defaultLevel': 1
                    }
                },
                'paragraph': {
                    'class': 'Paragraph',
                    'inlineToolbar': True,
                    'config': {
                        'placeholder': 'Write your post content...'
                    }
                },
                'image': {
                    'class': 'ImageTool',
                    'config': {
                        'endpoints': {
                            'byFile': reverse('marketing:upload_image'),
                            'byUrl': reverse('marketing:upload_image')
                        },
                        'field': 'file',
                        'types': 'image/*',
                        'captionPlaceholder': 'Image caption (optional)',
                        'buttonContent': 'Add Featured Image'
                    }
                },
                'quote': {
                    'class': 'Quote',
                    'inlineToolbar': True,
                    'config': {
                        'quotePlaceholder': 'Enter a quote from your post...',
                        'captionPlaceholder': 'Quote author'
                    }
                },
                'list': {
                    'class': 'List',
                    'inlineToolbar': True,
                    'config': {
                        'defaultStyle': 'unordered'
                    }
                },
                'embed': {
                    'class': 'Embed',
                    'config': {
                        'services': {
                            'youtube': True,
                            'vimeo': True,
                            'twitter': True
                        }
                    }
                },
                'code': {
                    'class': 'CodeTool',
                    'config': {
                        'placeholder': 'Enter code snippet...'
                    }
                },
                'table': {
                    'class': 'Table',
                    'inlineToolbar': True,
                    'config': {
                        'rows': 2,
                        'cols': 3
                    }
                }
            }
        }
        
        if 'config' in kwargs:
            post_config.update(kwargs['config'])
            del kwargs['config']
        
        kwargs['config'] = post_config
        super().__init__(*args, **kwargs)