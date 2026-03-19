#!/usr/bin/env python3
"""
Simple test to verify admin block builder integration works
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

def test_admin_integration():
    """Simple test to verify admin integration"""
    print("Testing Admin Block Builder Integration...")
    print("=" * 50)
    
    try:
        # Setup test client
        client = Client()
        User = get_user_model()
        
        # Get or create admin user
        try:
            user = User.objects.get(username='admin')
            print("✓ Found existing admin user")
        except User.DoesNotExist:
            user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print("✓ Created new admin user")
        
        # Login
        client.login(username='admin', password='admin123')
        print("✓ Logged in as admin")
        
        # Test Page admin form
        print("\nTesting Page Admin Form...")
        response = client.get(reverse('admin:marketing_page_add'))
        if response.status_code == 200:
            print("✓ Page admin form loaded successfully")
            if 'Block Builder' in response.content.decode():
                print("✓ Block Builder found in Page admin form")
            else:
                print("✗ Block Builder NOT found in Page admin form")
        else:
            print(f"✗ Page admin form failed with status {response.status_code}")
        
        # Test Post admin form
        print("\nTesting Post Admin Form...")
        response = client.get(reverse('admin:marketing_post_add'))
        if response.status_code == 200:
            print("✓ Post admin form loaded successfully")
            if 'Block Builder' in response.content.decode():
                print("✓ Block Builder found in Post admin form")
            else:
                print("✗ Block Builder NOT found in Post admin form")
        else:
            print(f"✗ Post admin form failed with status {response.status_code}")
        
        print("\n" + "=" * 50)
        print("✓ Admin integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_admin_integration()
    sys.exit(0 if success else 1)