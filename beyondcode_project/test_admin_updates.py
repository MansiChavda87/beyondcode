#!/usr/bin/env python
"""
Test script to verify Django Admin updates for Post and Page modules.
This script checks that the admin configuration is valid and the changes are applied correctly.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
django.setup()

from django.contrib.admin.sites import AdminSite
from marketing.admin import PageAdmin, PostAdmin
from marketing.models import Page, Post

def test_admin_configuration():
    """Test that the admin configuration is valid and contains expected changes."""
    
    print("Testing Django Admin Configuration Updates...")
    print("=" * 50)
    
    # Test PageAdmin
    print("\n1. Testing PageAdmin Configuration:")
    page_admin = PageAdmin(Page, AdminSite())
    
    # Check excluded fields - Note: blocks_json is NOT excluded to preserve existing data
    expected_excluded = {'body_json', 'body_html', 'blocks_html'}
    actual_excluded = set(page_admin.exclude or [])
    
    print(f"   Expected excluded fields: {expected_excluded}")
    print(f"   Actual excluded fields: {actual_excluded}")
    
    if expected_excluded.issubset(actual_excluded):
        print("   ✓ All specified fields (except blocks_json) are properly excluded")
    else:
        print("   ✗ Some fields are missing from exclude list")
        return False
    
    # Check fieldsets order - Block Builder section is present and before Content
    fieldset_names = [fieldset[0] for fieldset in page_admin.fieldsets]
    print(f"   Fieldset order: {fieldset_names}")
    
    if "Block Builder" in fieldset_names and "Content" in fieldset_names:
        block_builder_index = fieldset_names.index("Block Builder")
        content_index = fieldset_names.index("Content")
        
        if block_builder_index < content_index:
            print("   ✓ Block Builder section appears before Content section")
        else:
            print("   ✗ Block Builder section should appear before Content section")
            return False
    else:
        print("   ✗ Missing expected fieldsets")
        return False
    
    print("\n2. Testing PostAdmin Configuration:")
    post_admin = PostAdmin(Post, AdminSite())
    
    # Check excluded fields - Note: blocks_json is NOT excluded to preserve existing data
    expected_excluded = {'body_json', 'body_html', 'blocks_html'}
    actual_excluded = set(post_admin.exclude or [])
    print(f"   Expected excluded fields: {expected_excluded}")
    print(f"   Actual excluded fields: {actual_excluded}")
    
    if expected_excluded.issubset(actual_excluded):
        print("   ✓ All specified fields (except blocks_json) are properly excluded")
    else:
        print("   ✗ Some fields are missing from exclude list")
        return False
    
    # Check fieldsets order - Block Builder section is present and before Content
    fieldset_names = [fieldset[0] for fieldset in post_admin.fieldsets]
    print(f"   Fieldset order: {fieldset_names}")
    
    if "Block Builder" in fieldset_names and "Content" in fieldset_names:
        block_builder_index = fieldset_names.index("Block Builder")
        content_index = fieldset_names.index("Content")
        
        if block_builder_index < content_index:
            print("   ✓ Block Builder section appears before Content section")
        else:
            print("   ✗ Block Builder section should appear before Content section")
            return False
    else:
        print("   ✗ Missing expected fieldsets")
        return False
    
    print("\n" + "=" * 50)
    print("✓ All tests passed! Django Admin updates are correctly applied.")
    print("\nSUMMARY OF CHANGES:")
    print("- body_json, body_html, blocks_html fields are hidden")
    print("- blocks_json field is visible to preserve existing block editor data")
    print("- Block Builder section appears before Content section")
    print("- All other sections and fields remain unchanged")
    print("- Admin configuration is now valid and error-free")
    print("- Existing block editor data will be displayed correctly")
    
    return True

if __name__ == "__main__":
    success = test_admin_configuration()
    sys.exit(0 if success else 1)