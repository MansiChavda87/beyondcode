#!/usr/bin/env python3
"""
Test script to verify GrapesJS implementation in Django admin
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

# Add the project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'beyondcode_project'))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')

# Setup Django
django.setup()

def test_grapesjs_implementation():
    """Test the GrapesJS implementation"""
    print("Testing GrapesJS Implementation...")
    print("=" * 50)
    
    # Test 1: Check if GrapesJS widget can be imported
    try:
        from marketing.widgets import GrapesJSWidget, GrapesJSAdminWidget
        print("✓ GrapesJS widgets imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import GrapesJS widgets: {e}")
        return False
    
    # Test 2: Check if forms use GrapesJS widget
    try:
        from marketing.forms import PageForm, PostForm
        
        # Check if PageForm uses GrapesJS widget
        page_form = PageForm()
        if isinstance(page_form.fields['blocks_json'].widget, GrapesJSAdminWidget):
            print("✓ PageForm uses GrapesJS widget")
        else:
            print("✗ PageForm does not use GrapesJS widget")
            return False
            
        # Check if PostForm uses GrapesJS widget
        post_form = PostForm()
        if isinstance(post_form.fields['blocks_json'].widget, GrapesJSAdminWidget):
            print("✓ PostForm uses GrapesJS widget")
        else:
            print("✗ PostForm does not use GrapesJS widget")
            return False
            
    except ImportError as e:
        print(f"✗ Failed to import forms: {e}")
        return False
    
    # Test 3: Check if admin classes are configured correctly
    try:
        from marketing.admin import PageAdmin, PostAdmin
        
        # Check if PageAdmin excludes the correct fields
        if 'body_json' in PageAdmin.exclude and 'body_html' in PageAdmin.exclude:
            print("✓ PageAdmin excludes body_json and body_html fields")
        else:
            print("✗ PageAdmin does not exclude required fields")
            return False
            
        # Check if PostAdmin excludes the correct fields
        if 'body_json' in PostAdmin.exclude and 'body_html' in PostAdmin.exclude:
            print("✓ PostAdmin excludes body_json and body_html fields")
        else:
            print("✗ PostAdmin does not exclude required fields")
            return False
            
    except ImportError as e:
        print(f"✗ Failed to import admin classes: {e}")
        return False
    
    # Test 4: Check if static files exist
    static_files = [
        'beyondcode_project/marketing/static/marketing/js/grapesjs-widget.js',
        'beyondcode_project/marketing/static/marketing/css/grapesjs-custom.css'
    ]
    
    for file_path in static_files:
        if os.path.exists(file_path):
            print(f"✓ Static file exists: {file_path}")
        else:
            print(f"✗ Static file missing: {file_path}")
            return False
    
    # Test 5: Check model save methods handle GrapesJS data
    try:
        from marketing.models import Page, Post
        import uuid
        
        # Test Page model
        page = Page(title="Test Page", slug=f"test-page-{uuid.uuid4().hex[:8]}")
        test_grapesjs_data = {
            'html': '<div>Test content</div>',
            'css': 'div { color: red; }',
            'components': [],
            'style': {}
        }
        page.blocks_json = test_grapesjs_data
        page.save()
        print("✓ Page model handles GrapesJS data correctly")
        
        # Test Post model
        post = Post(title="Test Post", slug=f"test-post-{uuid.uuid4().hex[:8]}")
        post.blocks_json = test_grapesjs_data
        post.save()
        print("✓ Post model handles GrapesJS data correctly")
        
    except Exception as e:
        print(f"✗ Model save method test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! GrapesJS implementation is working correctly.")
    print("\nNext steps:")
    print("1. Run 'python manage.py runserver' to start the Django development server")
    print("2. Navigate to Django admin at http://localhost:8000/admin/")
    print("3. Create or edit a Page or Post to see the GrapesJS editor")
    print("4. Test drag-and-drop functionality with the custom blocks")
    
    return True

if __name__ == '__main__':
    success = test_grapesjs_implementation()
    sys.exit(0 if success else 1)