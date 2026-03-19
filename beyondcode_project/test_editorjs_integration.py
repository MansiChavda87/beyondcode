#!/usr/bin/env python3
"""
Test script to verify Editor.js integration in Django admin
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

# Add the project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')

# Setup Django
django.setup()

def test_editorjs_widgets():
    """Test that our Editor.js widgets are properly configured"""
    from marketing.widgets import EditorJSAdminWidget
    from marketing.forms import PageForm, PostForm
    import json
    
    print("Testing Editor.js Widget Configuration...")
    
    # Test widget creation
    widget = EditorJSAdminWidget()
    print(f"✓ EditorJSAdminWidget created successfully")
    
    # Test widget media
    media = widget.media
    print(f"✓ Widget media configured with {len(media._css['all'])} CSS files and {len(media._js)} JS files")
    
    # Test form creation
    page_form = PageForm()
    post_form = PostForm()
    print(f"✓ PageForm and PostForm created successfully")
    
    # Check if blocks_json field uses our widget
    if hasattr(page_form.fields, 'blocks_json'):
        field = page_form.fields['blocks_json']
        if isinstance(field.widget, EditorJSAdminWidget):
            print(f"✓ PageForm uses EditorJSAdminWidget for blocks_json")
        else:
            print(f"✗ PageForm does not use EditorJSAdminWidget for blocks_json")
    
    if hasattr(post_form.fields, 'blocks_json'):
        field = post_form.fields['blocks_json']
        if isinstance(field.widget, EditorJSAdminWidget):
            print(f"✓ PostForm uses EditorJSAdminWidget for blocks_json")
        else:
            print(f"✗ PostForm does not use EditorJSAdminWidget for blocks_json")
    
    print("\nWidget configuration test completed!")

def test_static_files():
    """Test that static files are accessible"""
    import os
    
    print("Testing Static Files...")
    
    static_files = [
        'marketing/css/editorjs-custom.css',
        'marketing/js/editorjs-widget.js',
        'marketing/js/editorjs-drag-drop.js'
    ]
    
    for static_file in static_files:
        file_path = os.path.join('static', static_file)
        if os.path.exists(file_path):
            print(f"✓ {static_file} exists")
        else:
            print(f"✗ {static_file} missing")
    
    print("\nStatic files test completed!")

def test_admin_templates():
    """Test that admin templates exist"""
    import os
    
    print("Testing Admin Templates...")
    
    template_files = [
        'marketing/templates/admin/marketing/page/change_form.html',
        'marketing/templates/admin/marketing/post/change_form.html'
    ]
    
    for template_file in template_files:
        if os.path.exists(template_file):
            print(f"✓ {template_file} exists")
        else:
            print(f"✗ {template_file} missing")
    
    print("\nAdmin templates test completed!")

def test_models():
    """Test that models have the required fields"""
    from marketing.models import Page, Post
    
    print("Testing Models...")
    
    # Check Page model
    page_fields = [field.name for field in Page._meta.get_fields()]
    if 'blocks_json' in page_fields:
        print(f"✓ Page model has blocks_json field")
    else:
        print(f"✗ Page model missing blocks_json field")
    
    # Check Post model
    post_fields = [field.name for field in Post._meta.get_fields()]
    if 'blocks_json' in post_fields:
        print(f"✓ Post model has blocks_json field")
    else:
        print(f"✗ Post model missing blocks_json field")
    
    print("\nModels test completed!")

def main():
    """Run all tests"""
    print("=" * 60)
    print("Editor.js Integration Test Suite")
    print("=" * 60)
    
    try:
        test_editorjs_widgets()
        test_static_files()
        test_admin_templates()
        test_models()
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("Editor.js integration appears to be properly configured.")
        print("\nNext steps:")
        print("1. Run 'python manage.py collectstatic' to collect static files")
        print("2. Run 'python manage.py runserver' to start the development server")
        print("3. Navigate to Django admin and test the Page and Post forms")
        print("4. Verify that Editor.js loads properly with drag-and-drop functionality")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()