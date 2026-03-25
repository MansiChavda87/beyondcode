#!/usr/bin/env python3
"""
Test script to verify GrapesJS image upload functionality
This script tests the upload endpoint and verifies the fixes are working
"""

import os
import sys
import django
from django.conf import settings
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

# Add the project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'beyondcode_project'))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
django.setup()

from marketing.models import MediaAsset
from django.contrib.auth.models import User


def test_upload_endpoint():
    """Test the image upload endpoint"""
    print("Testing image upload endpoint...")
    
    # Create a test client
    client = Client()
    
    # Create a test user
    user = User.objects.create_user(
        username='testuser',
        password='testpass123',
        is_staff=True,
        is_superuser=True
    )
    
    # Login as admin
    client.login(username='testuser', password='testpass123')
    
    # Create a test image file
    test_image_content = b'fake image content'
    test_image = SimpleUploadedFile(
        "test_image.jpg",
        test_image_content,
        content_type="image/jpeg"
    )
    
    # Test the upload endpoint
    response = client.post('/admin/upload-image/', {
        'files': test_image
    })
    
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.content.decode()}")
    
    if response.status_code == 200:
        try:
            import json
            data = json.loads(response.content)
            print(f"Upload successful: {data}")
            return True
        except Exception as e:
            print(f"Error parsing response: {e}")
            return False
    else:
        print(f"Upload failed with status {response.status_code}")
        return False


def test_asset_manager_config():
    """Test that asset manager configuration is correct"""
    print("\nTesting asset manager configuration...")
    
    # Check if the widget has the correct configuration
    from marketing.widgets import GrapesJSAdminWidget
    
    widget = GrapesJSAdminWidget()
    
    if hasattr(widget, 'options') and 'assetManager' in widget.options:
        asset_manager = widget.options['assetManager']
        
        required_config = {
            'upload': '/admin/upload-image/',
            'uploadName': 'files',
            'autoAdd': True,
            'dropzone': True,
            'openAssetsOnDrop': True
        }
        
        for key, value in required_config.items():
            if key not in asset_manager or asset_manager[key] != value:
                print(f"Missing or incorrect config for {key}: expected {value}, got {asset_manager.get(key)}")
                return False
        
        print("Asset manager configuration is correct!")
        return True
    else:
        print("Asset manager configuration not found in widget options")
        return False


def test_css_fixes():
    """Test that CSS fixes are in place"""
    print("\nTesting CSS fixes...")
    
    css_file = 'beyondcode_project/marketing/static/marketing/css/grapesjs-custom.css'
    
    if not os.path.exists(css_file):
        print(f"CSS file not found: {css_file}")
        return False
    
    with open(css_file, 'r') as f:
        css_content = f.read()
    
    # Check for key CSS fixes
    required_fixes = [
        '.gjs-am-file-uploader',
        'pointer-events: auto',
        '.gjs-am-file-input',
        'display: none',
        '.gjs-am-assets',
        'z-index: 1000'
    ]
    
    missing_fixes = []
    for fix in required_fixes:
        if fix not in css_content:
            missing_fixes.append(fix)
    
    if missing_fixes:
        print(f"Missing CSS fixes: {missing_fixes}")
        return False
    
    print("CSS fixes are in place!")
    return True


def test_javascript_fixes():
    """Test that JavaScript fixes are in place"""
    print("\nTesting JavaScript fixes...")
    
    js_files = [
        'beyondcode_project/static/marketing/js/block-builder.js',
        'beyondcode_project/marketing/templates/admin/marketing/page/change_form.html',
        'beyondcode_project/marketing/templates/admin/marketing/post/change_form.html'
    ]
    
    required_js_fixes = [
        'fixImageUpload',
        'uploadFile',
        'gjs-am-file-input',
        'getCSRFToken',
        'dropzone: true'
    ]
    
    for js_file in js_files:
        if not os.path.exists(js_file):
            print(f"JavaScript file not found: {js_file}")
            return False
        
        with open(js_file, 'r') as f:
            js_content = f.read()
        
        missing_fixes = []
        for fix in required_js_fixes:
            if fix not in js_content:
                missing_fixes.append(fix)
        
        if missing_fixes:
            print(f"Missing JavaScript fixes in {js_file}: {missing_fixes}")
            return False
    
    print("JavaScript fixes are in place!")
    return True


def main():
    """Run all tests"""
    print("=== GrapesJS Image Upload Fix Verification ===\n")
    
    tests = [
        test_asset_manager_config,
        test_css_fixes,
        test_javascript_fixes,
        test_upload_endpoint
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"Test failed with exception: {e}")
            results.append(False)
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("✅ All tests passed! Image upload fixes are working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)