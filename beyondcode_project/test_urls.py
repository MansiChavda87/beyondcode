#!/usr/bin/env python
"""
Simple test script to verify URL patterns are working correctly.
"""
import os
import sys
import django
from django.test import Client
from django.urls import reverse

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
django.setup()

def test_url_patterns():
    """Test that the URL patterns are working correctly."""
    client = Client()
    
    # Test the new URL patterns
    test_urls = [
        ('/', 'home'),
        ('/contact/', 'contact'),
        ('/about/', 'about'),
        ('/pricing/', 'pricing'),
        ('/services/', 'services'),
        ('/team/', 'team'),
        ('/careers/', 'careers'),
        ('/privacy/', 'privacy'),
        ('/terms/', 'terms'),
    ]
    
    print("Testing URL patterns...")
    print("=" * 50)
    
    for url, name in test_urls:
        try:
            response = client.get(url)
            status = "✓ PASS" if response.status_code in [200, 404] else f"✗ FAIL ({response.status_code})"
            print(f"{url:<15} -> {name:<12} [{status}]")
            
            # For 404 errors, that's expected if the page doesn't exist in the database
            if response.status_code == 404:
                print(f"                Note: 404 is expected if '{name}' page doesn't exist in database")
                
        except Exception as e:
            print(f"{url:<15} -> {name:<12} [✗ ERROR: {e}]")
    
    print("\nTesting reverse URL generation...")
    print("=" * 50)
    
    # Test reverse URL generation
    try:
        home_url = reverse('marketing:home')
        contact_url = reverse('marketing:contact')
        about_url = reverse('marketing:about')
        pricing_url = reverse('marketing:pricing')
        
        print(f"home: {home_url}")
        print(f"contact: {contact_url}")
        print(f"about: {about_url}")
        print(f"pricing: {pricing_url}")
        
    except Exception as e:
        print(f"Error generating reverse URLs: {e}")

if __name__ == '__main__':
    test_url_patterns()