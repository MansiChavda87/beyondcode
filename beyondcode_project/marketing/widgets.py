from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf import settings
import json


class GrapesJSWidget(forms.Widget):
    """
    Custom widget for GrapesJS integration in Django admin
    Provides a full page builder experience similar to WordPress/Elementor
    """
    
    class Media:
        css = {
            'all': (
                'https://unpkg.com/grapesjs/dist/css/grapes.min.css',
                'marketing/css/grapesjs-custom.css',
            )
        }
        js = (
            'https://unpkg.com/grapesjs',
        )

    def __init__(self, attrs=None, options=None):
        default_attrs = {
            'class': 'grapesjs-widget',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
        
        # Default GrapesJS options
        self.options = options or {
            'height': '600px',
            'width': 'auto',
            'storageManager': False,  # Disable automatic storage
            'plugins': [],
            'pluginsOpts': {},
        }

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        
        # Generate unique ID for this editor instance
        editor_id = f"grapesjs_{name}_{id(self)}"
        attrs['id'] = editor_id
        
        # Prepare initial data
        initial_data = {}
        if value and isinstance(value, str):
            try:
                initial_data = json.loads(value)
            except json.JSONDecodeError:
                initial_data = {}
        elif value and isinstance(value, dict):
            initial_data = value
        else:
            initial_data = {}

        # Render the GrapesJS container and hidden textarea
        html = f'''
        
        <div id="blocks-canvas" style="
            width: 260px;
            border: 1px solid #ddd;
            padding: 10px;
            background: #fafafa;
            overflow-y: auto;
            height: 1000px;
        "></div>
        <div class="grapesjs-container">
            <div id="{editor_id}" class="grapesjs-editor"></div>
            <textarea name="{name}" id="{editor_id}_textarea" class="grapesjs-textarea" style="display: none;">
                {json.dumps(initial_data) if initial_data else '{}'}
            </textarea>
        </div>
        '''
        
        return mark_safe(html)


class GrapesJSAdminWidget(GrapesJSWidget):
    """
    Admin-specific widget with enhanced styling and functionality
    """
    def __init__(self, attrs=None, options=None):
        default_options = {
            'height': '600px',
            'width': 'auto',
            'storageManager': False,
            'plugins': [],
            'pluginsOpts': {},
            'assetManager': {
                'upload': '/upload-image/',
                'uploadName': 'files',
                'autoAdd': True,
                'credentials': 'include', 
                'dropzone': True,
                'openAssetsOnDrop': True,
                'headers': {
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            }
        }
        if options:
            default_options.update(options)
        
        super().__init__(attrs, default_options)
        
        # Add admin-specific CSS class
        if 'class' in self.attrs:
            self.attrs['class'] += ' grapesjs-admin-widget'
        else:
            self.attrs['class'] = 'grapesjs-admin-widget'
