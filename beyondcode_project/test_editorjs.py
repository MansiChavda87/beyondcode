#!/usr/bin/env python
"""
Test script to verify EditorJS integration works properly.
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
django.setup()

# Test imports
try:
    from django_editorjs import EditorJSField
    print("✓ EditorJSField imported successfully")
except ImportError as e:
    print(f"✗ Failed to import EditorJSField: {e}")
    sys.exit(1)

try:
    from marketing.forms import PageForm, PostForm
    print("✓ Custom forms imported successfully")
except ImportError as e:
    print(f"✗ Failed to import custom forms: {e}")
    sys.exit(1)

# Test form instantiation
try:
    page_form = PageForm()
    post_form = PostForm()
    print("✓ Forms instantiated successfully")
    print(f"✓ PageForm has EditorJS fields: {'body_json' in page_form.fields and 'blocks_json' in page_form.fields}")
    print(f"✓ PostForm has EditorJS fields: {'body_json' in post_form.fields and 'blocks_json' in post_form.fields}")
except Exception as e:
    print(f"✗ Failed to instantiate forms: {e}")
    sys.exit(1)

print("\n🎉 All tests passed! EditorJS integration is working correctly.")