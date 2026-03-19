from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf import settings
import json

# Import EditorJSField for backward compatibility
try:
    from django_editorjs import EditorJsField
except ImportError:
    EditorJsField = None


class EditorJSWidget(forms.Textarea):
    """
    Custom widget for Editor.js integration in Django admin
    Provides a full page builder experience similar to WordPress/Elementor
    """
    
    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/@editorjs/editorjs@2.29.1/dist/editor.min.css',
                'https://cdn.jsdelivr.net/npm/@editorjs/header@2.8.1/dist/bundle.min.css',
                'https://cdn.jsdelivr.net/npm/@editorjs/paragraph@2.11.2/dist/bundle.min.css',
                'https://cdn.jsdelivr.net/npm/@editorjs/list@1.10.0/dist/bundle.min.css',
                'https://cdn.jsdelivr.net/npm/@editorjs/image@2.8.1/dist/bundle.min.css',
                'https://cdn.jsdelivr.net/npm/@editorjs/table@2.3.0/dist/bundle.min.css',
                'https://cdn.jsdelivr.net/npm/@editorjs/embed@2.7.1/dist/bundle.min.css',
                'https://cdn.jsdelivr.net/npm/@editorjs/checklist@1.7.0/dist/bundle.min.css',
                'https://cdn.jsdelivr.net/npm/@editorjs/delimiter@2.0.0/dist/bundle.min.css',
                'https://cdn.jsdelivr.net/npm/@editorjs/warning@1.5.0/dist/bundle.min.css',
                'https://cdn.jsdelivr.net/npm/@editorjs/code@2.9.0/dist/bundle.min.css',
                'https://cdn.jsdelivr.net/npm/@editorjs/raw@2.5.0/dist/bundle.min.css',
                'https://cdn.jsdelivr.net/npm/@editorjs/quote@2.7.0/dist/bundle.min.css',
                'https://cdn.jsdelivr.net/npm/@editorjs/marker@2.0.3/dist/bundle.min.css',
                'https://cdn.jsdelivr.net/npm/@editorjs/inline-code@1.5.0/dist/bundle.min.css',
                'marketing/css/editorjs-custom.css',
            )
        }
        js = (
            'https://cdn.jsdelivr.net/npm/@editorjs/editorjs@2.29.1/dist/editor.min.js',
            'https://cdn.jsdelivr.net/npm/@editorjs/header@2.8.1/dist/bundle.min.js',
            'https://cdn.jsdelivr.net/npm/@editorjs/paragraph@2.11.2/dist/bundle.min.js',
            'https://cdn.jsdelivr.net/npm/@editorjs/list@1.10.0/dist/bundle.min.js',
            'https://cdn.jsdelivr.net/npm/@editorjs/image@2.8.1/dist/bundle.min.js',
            'https://cdn.jsdelivr.net/npm/@editorjs/table@2.3.0/dist/bundle.min.js',
            'https://cdn.jsdelivr.net/npm/@editorjs/embed@2.7.1/dist/bundle.min.js',
            'https://cdn.jsdelivr.net/npm/@editorjs/checklist@1.7.0/dist/bundle.min.js',
            'https://cdn.jsdelivr.net/npm/@editorjs/delimiter@2.0.0/dist/bundle.min.js',
            'https://cdn.jsdelivr.net/npm/@editorjs/warning@1.5.0/dist/bundle.min.js',
            'https://cdn.jsdelivr.net/npm/@editorjs/code@2.9.0/dist/bundle.min.js',
            'https://cdn.jsdelivr.net/npm/@editorjs/raw@2.5.0/dist/bundle.min.js',
            'https://cdn.jsdelivr.net/npm/@editorjs/quote@2.7.0/dist/bundle.min.js',
            'https://cdn.jsdelivr.net/npm/@editorjs/marker@2.0.3/dist/bundle.min.js',
            'https://cdn.jsdelivr.net/npm/@editorjs/inline-code@1.5.0/dist/bundle.min.js',
            'marketing/js/editorjs-drag-drop.js',
            'marketing/js/editorjs-widget.js',
        )

    def __init__(self, attrs=None, tools=None, placeholder=None, minHeight=300, readOnly=False):
        default_attrs = {
            'class': 'editorjs-widget',
            'style': f'min-height: {minHeight}px;',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
        
        # Default tools configuration
        self.tools = tools or {
            'header': {
                'class': 'Header',
                'inlineToolbar': True,
                'config': {
                    'placeholder': 'Enter a header',
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
                        'byFile': reverse('marketing:media_upload'),
                        'byUrl': reverse('marketing:media_upload'),
                    },
                    'field': 'file',
                    'types': 'image/*',
                    'additionalRequestHeaders': {},
                    'additionalRequestData': {},
                    'captionPlaceholder': 'Image caption (optional)',
                    'buttonContent': 'Select an Image',
                    'uploader': {
                        'config': {
                            'serverUrl': reverse('marketing:media_upload'),
                        }
                    }
                }
            },
            'table': {
                'class': 'Table',
                'inlineToolbar': True,
                'config': {
                    'rows': 2,
                    'cols': 3
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
            'checklist': {
                'class': 'Checklist',
                'inlineToolbar': True
            },
            'delimiter': {
                'class': 'Delimiter'
            },
            'warning': {
                'class': 'Warning',
                'inlineToolbar': True,
                'config': {
                    'titlePlaceholder': 'Title',
                    'messagePlaceholder': 'Message'
                }
            },
            'code': {
                'class': 'CodeTool'
            },
            'raw': {
                'class': 'RawTool'
            },
            'quote': {
                'class': 'Quote',
                'inlineToolbar': True,
                'config': {
                    'quotePlaceholder': 'Enter a quote',
                    'captionPlaceholder': 'Quote\'s author'
                }
            },
            'marker': {
                'class': 'Marker',
                'shortcut': 'CMD+SHIFT+M'
            },
            'inlineCode': {
                'class': 'InlineCode',
                'shortcut': 'CMD+SHIFT+M'
            }
        }
        
        self.placeholder = placeholder or "Start creating your content..."
        self.readOnly = readOnly

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        
        # Generate unique ID for this editor instance
        editor_id = f"editorjs_{name}_{id(self)}"
        attrs['id'] = editor_id
        
        # Prepare initial data
        initial_data = {}
        if value and isinstance(value, str):
            try:
                initial_data = json.loads(value)
            except json.JSONDecodeError:
                initial_data = {'blocks': []}
        elif value and isinstance(value, dict):
            initial_data = value
        else:
            initial_data = {'blocks': []}

        # Render the textarea (hidden) and the editor container
        html = f'''
        <div class="editorjs-container">
            <div id="{editor_id}_editor" class="editorjs-editor"></div>
            <textarea name="{name}" id="{editor_id}" class="editorjs-textarea" style="display: none;">
                {json.dumps(initial_data) if initial_data else ''}
            </textarea>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                initializeEditorJS('{editor_id}', {{
                    tools: {json.dumps(self.tools)},
                    data: {json.dumps(initial_data)},
                    placeholder: '{self.placeholder}',
                    readOnly: {str(self.readOnly).lower()},
                    minHeight: {self.attrs.get('style', '').split('min-height: ')[1].split('px')[0] if 'min-height:' in self.attrs.get('style', '') else '300'},
                    onReady: function() {{
                        // Initialize drag and drop
                        if (typeof EditorJSDragDrop !== 'undefined') {{
                            new EditorJSDragDrop({{
                                editor: this
                            }});
                        }}
                    }},
                    onChange: function() {{
                        // Update hidden textarea with current data
                        const editorData = this.save();
                        const textarea = document.getElementById('{editor_id}');
                        editorData.then(function(savedData) {{
                            textarea.value = JSON.stringify(savedData);
                        }});
                    }}
                }});
            }});
        </script>
        '''
        
        return mark_safe(html)


class EditorJSAdminWidget(EditorJSWidget):
    """
    Admin-specific widget with enhanced styling and functionality
    """
    def __init__(self, attrs=None, tools=None, placeholder=None, minHeight=400, readOnly=False):
        super().__init__(attrs, tools, placeholder, minHeight, readOnly)
        
        # Add admin-specific CSS class
        if 'class' in self.attrs:
            self.attrs['class'] += ' editorjs-admin-widget'
        else:
            self.attrs['class'] = 'editorjs-admin-widget'