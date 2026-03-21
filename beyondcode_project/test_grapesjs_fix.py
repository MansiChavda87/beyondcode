#!/usr/bin/env python3
"""
Test script to verify GrapesJS column fixes
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'beyondcode_project'))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
django.setup()

def test_grapesjs_imports():
    """Test that all GrapesJS-related imports work correctly"""
    print("Testing GrapesJS imports...")
    
    try:
        # Test utils import
        from marketing.utils import render_grapesjs_content, get_grapesjs_html, get_grapesjs_css
        print("✅ marketing.utils imports successful")
        
        # Test template tags import
        from marketing.templatetags.grapesjs_tags import render_grapesjs, grapesjs_html, grapesjs_css
        print("✅ marketing.templatetags.grapesjs_tags imports successful")
        
        # Test template loading
        from django.template import Template, Context
        template = Template("{% load grapesjs_tags %}{{ content|render_grapesjs }}")
        print("✅ Template loading with grapesjs_tags successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_grapesjs_content_rendering():
    """Test that GrapesJS content renders correctly"""
    print("\nTesting GrapesJS content rendering...")
    
    try:
        from marketing.utils import render_grapesjs_content
        
        # Test with sample GrapesJS content
        sample_content = {
            'html': '<div class="gjs-row"><div class="gjs-cell">Column 1</div><div class="gjs-cell">Column 2</div></div>',
            'css': '.custom-class { color: red; }'
        }
        
        rendered = render_grapesjs_content(sample_content)
        
        # Check that the base CSS is included
        if '.gjs-row' in rendered and 'display: flex' in rendered:
            print("✅ Base CSS is included in rendered content")
        else:
            print("❌ Base CSS not found in rendered content")
            return False
            
        # Check that the HTML is included
        if 'gjs-row' in rendered and 'gjs-cell' in rendered:
            print("✅ GrapesJS HTML structure is preserved")
        else:
            print("❌ GrapesJS HTML structure not found")
            return False
            
        # Check that custom CSS is included
        if '.custom-class' in rendered:
            print("✅ Custom CSS is included")
        else:
            print("❌ Custom CSS not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error rendering content: {e}")
        return False

def test_template_filter():
    """Test that the template filter works correctly"""
    print("\nTesting template filter...")
    
    try:
        from django.template import Template, Context
        
        # Test template with sample content
        template_str = """
        {% load grapesjs_tags %}
        {{ content|render_grapesjs|safe }}
        """
        
        template = Template(template_str)
        
        # Sample content
        content = {
            'html': '<div class="gjs-row"><div class="gjs-cell">Test Column</div></div>',
            'css': ''
        }
        
        context = Context({'content': content})
        rendered = template.render(context)
        
        # Check that the content was rendered
        if 'gjs-row' in rendered and 'gjs-cell' in rendered:
            print("✅ Template filter renders content correctly")
            return True
        else:
            print("❌ Template filter failed to render content")
            return False
            
    except Exception as e:
        print(f"❌ Error with template filter: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing GrapesJS Column Fixes\n")
    
    tests = [
        test_grapesjs_imports,
        test_grapesjs_content_rendering,
        test_template_filter
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! GrapesJS column fixes are working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)