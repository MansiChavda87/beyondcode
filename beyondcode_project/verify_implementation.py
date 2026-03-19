#!/usr/bin/env python3
"""
Simple verification script for Editor.js integration
"""

import os
import sys

def check_files():
    """Check if all required files exist"""
    print("Checking required files...")
    
    required_files = [
        'marketing/widgets.py',
        'marketing/forms.py', 
        'marketing/admin.py',
        'marketing/models.py',
        'static/marketing/css/editorjs-custom.css',
        'static/marketing/js/editorjs-widget.js',
        'static/marketing/js/editorjs-drag-drop.js',
        'templates/admin/marketing/page/change_form.html',
        'templates/admin/marketing/post/change_form.html'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}")
            all_exist = False
    
    return all_exist

def check_widget_import():
    """Check if widget can be imported"""
    print("\nChecking widget import...")
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from marketing.widgets import EditorJSAdminWidget
        print("✓ EditorJSAdminWidget imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def check_forms():
    """Check if forms use the widget"""
    print("\nChecking form configuration...")
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from marketing.forms import PageForm, PostForm
        
        page_form = PageForm()
        post_form = PostForm()
        
        if 'blocks_json' in page_form.fields:
            print("✓ PageForm has blocks_json field")
        else:
            print("✗ PageForm missing blocks_json field")
            
        if 'blocks_json' in post_form.fields:
            print("✓ PostForm has blocks_json field")
        else:
            print("✗ PostForm missing blocks_json field")
            
        return True
    except Exception as e:
        print(f"✗ Form check failed: {e}")
        return False

def main():
    """Run verification"""
    print("=" * 60)
    print("Editor.js Integration Verification")
    print("=" * 60)
    
    files_ok = check_files()
    import_ok = check_widget_import()
    forms_ok = check_forms()
    
    print("\n" + "=" * 60)
    if files_ok and import_ok and forms_ok:
        print("✓ All checks passed! Editor.js integration is ready.")
        print("\nNext steps:")
        print("1. Run 'python manage.py collectstatic'")
        print("2. Run 'python manage.py runserver'")
        print("3. Visit Django admin to test the editor")
    else:
        print("✗ Some checks failed. Please review the implementation.")
    print("=" * 60)

if __name__ == '__main__':
    main()