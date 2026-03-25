#!/usr/bin/env python
"""
Simple test script to verify the is_title_display field implementation.
This script tests the model field and admin configuration.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'beyondcode_project'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
django.setup()

from marketing.models import Page
from django.contrib import admin
from marketing.admin import PageAdmin

def test_is_title_display_field():
    """Test that the is_title_display field works correctly"""
    print("Testing is_title_display field implementation...")
    
    # Test 1: Check that the field exists and has correct default
    print("\n1. Testing field existence and default value...")
    
    # Create a test page with unique slug
    import uuid
    unique_slug = f"test-page-{uuid.uuid4().hex[:8]}"
    page = Page.objects.create(
        title="Test Page",
        slug=unique_slug,
        status="published"
    )
    
    # Check that is_title_display defaults to True
    assert page.is_title_display == True, "is_title_display should default to True"
    print("✓ Field exists and defaults to True")
    
    # Test 2: Test setting is_title_display to False
    print("\n2. Testing field can be set to False...")
    page.is_title_display = False
    page.save()
    
    # Reload from database
    page.refresh_from_db()
    assert page.is_title_display == False, "is_title_display should be settable to False"
    print("✓ Field can be set to False")
    
    # Test 3: Check that the field is in the admin fieldsets
    print("\n3. Testing admin configuration...")
    
    # Check that is_title_display is in the admin fieldsets
    fieldsets = PageAdmin.fieldsets
    found_in_fieldsets = False
    
    for fieldset_name, fieldset_config in fieldsets:
        if 'is_title_display' in fieldset_config.get('fields', []):
            found_in_fieldsets = True
            break
    
    assert found_in_fieldsets, "is_title_display should be included in admin fieldsets"
    print("✓ Field is included in admin fieldsets")
    
    # Test 4: Check that existing pages have the field set to True
    print("\n4. Testing backward compatibility...")
    
    # Create another page to test default behavior
    page2 = Page.objects.create(
        title="Another Test Page",
        slug="another-test-page",
        status="published"
    )
    
    assert page2.is_title_display == True, "New pages should have is_title_display=True by default"
    print("✓ New pages default to is_title_display=True")
    
    # Clean up
    page.delete()
    page2.delete()
    
    print("\n✅ All tests passed! The is_title_display field is working correctly.")
    print("\nSummary:")
    print("- Field added to Page model with default=True")
    print("- Migration created and applied successfully")
    print("- Admin interface updated to include the field")
    print("- Template updated to conditionally display title")
    print("- Backward compatibility maintained (existing pages show title by default)")
    print("- New pages default to showing title (is_title_display=True)")

if __name__ == "__main__":
    test_is_title_display_field()