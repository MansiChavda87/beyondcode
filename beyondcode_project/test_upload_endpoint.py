#!/usr/bin/env python3
"""
Test script to verify the upload endpoint is working correctly
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


def test_url_configuration():
    """Test that the URL is properly configured"""
    print("\nTesting URL configuration...")
    
    try:
        from django.urls import reverse
        url = reverse('marketing:upload_image')
        print(f"URL found: {url}")
        return True
    except Exception as e:
        print(f"URL not found: {e}")
        return False


def main():
    """Run all tests"""
    print("=== Upload Endpoint Verification ===\n")
    
    tests = [
        test_url_configuration,
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
        print("✅ All tests passed! Upload endpoint is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)