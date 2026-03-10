#!/usr/bin/env python
"""
Simple test to verify the import works
"""
try:
    from django_editorjs import EditorJSField
    print("SUCCESS: EditorJSField imported successfully from django_editorjs")
except ImportError as e:
    print(f"ERROR: Failed to import EditorJSField: {e}")
    print("This means the package is not installed or there's an import issue")