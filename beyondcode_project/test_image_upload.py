#!/usr/bin/env python3
"""
Test script for image upload functionality
"""

import os
import sys
import django
from django.conf import settings
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile

# Add the project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'beyondcode_project'))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
django.setup()

def test_image_upload():
    """Test the image upload functionality"""
    print("Testing image upload functionality...")
    
    # Create a test client
    client = Client()
    
    # Create a simple test image (1x1 pixel PNG)
    test_image_content = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13'
        b'\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04'
        b'\x00\x01\xbb}\xa0\x9a\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    
    # Create a SimpleUploadedFile
    test_image = SimpleUploadedFile(
        "test_image.png",
        test_image_content,
        content_type="image/png"
    )
    
    # Test the upload endpoint
    try:
        response = client.post('/admin/upload-image/', {'files': test_image})
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        
        if response.status_code == 200:
            import json
            data = json.loads(response.content)
            print("✅ Image upload test passed!")
            print(f"Uploaded image URL: {data['data'][0]['src']}")
            return True
        else:
            print("❌ Image upload test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

def test_media_serving():
    """Test that uploaded media can be served"""
    print("\nTesting media serving...")
    
    client = Client()
    
    # Try to access a test file
    try:
        response = client.get('/media/uploads/test_image.png')
        print(f"Media serving response status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Media serving test passed!")
            return True
        else:
            print("❌ Media serving test failed!")
            return False
    except Exception as e:
        print(f"❌ Error during media serving test: {e}")
        return False

if __name__ == '__main__':
    print("Starting image upload tests...\n")
    
    # Test image upload
    upload_success = test_image_upload()
    
    # Test media serving
    serving_success = test_media_serving()
    
    print(f"\nTest Results:")
    print(f"Image Upload: {'✅ PASSED' if upload_success else '❌ FAILED'}")
    print(f"Media Serving: {'✅ PASSED' if serving_success else '❌ FAILED'}")
    
    if upload_success and serving_success:
        print("\n🎉 All tests passed! Image upload functionality is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")