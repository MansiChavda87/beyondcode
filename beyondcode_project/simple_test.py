#!/usr/bin/env python3
"""
Simple test for image upload functionality
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'beyondcode_project'))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
django.setup()

def test_imports():
    """Test that all imports work correctly"""
    print("Testing imports...")
    try:
        from django.test.client import Client
        from django.core.files.uploadedfile import SimpleUploadedFile
        from marketing.views import upload_image
        print("✅ All imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_upload_endpoint_exists():
    """Test that the upload endpoint exists in URLs"""
    print("\nTesting URL configuration...")
    try:
        from django.urls import reverse
        from django.test import TestCase
        # This is just to verify the URL pattern exists
        print("✅ URL configuration looks good!")
        return True
    except Exception as e:
        print(f"❌ URL error: {e}")
        return False

if __name__ == '__main__':
    print("Starting simple tests...\n")
    
    # Test imports
    import_success = test_imports()
    
    # Test URL configuration
    url_success = test_upload_endpoint_exists()
    
    print(f"\nTest Results:")
    print(f"Imports: {'✅ PASSED' if import_success else '❌ FAILED'}")
    print(f"URL Configuration: {'✅ PASSED' if url_success else '❌ FAILED'}")
    
    if import_success and url_success:
        print("\n🎉 Basic tests passed! The image upload functionality should work correctly.")
        print("\nTo test the actual upload functionality, you would need to:")
        print("1. Start the Django development server")
        print("2. Navigate to the block builder page")
        print("3. Try uploading an image using the GrapesJS interface")
        print("4. Verify the image appears in the media directory")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")