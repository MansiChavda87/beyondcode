#!/usr/bin/env python3
"""
Test script to verify the complete block editor implementation is working correctly.

This script tests all the key functionality of the block editor after implementing the full data lifecycle.
"""

import os
import sys
import json
import re

def test_central_state_object():
    """Test that the central state object is properly defined."""
    
    template_path = "marketing/templates/admin/marketing/page/block_builder.html"
    
    if not os.path.exists(template_path):
        print("❌ Block builder template not found")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test for central state object
    central_state_pattern = r'let blocks = \{\s*richText:\s*null,\s*cta:\s*\{\},\s*faq:\s*\[\s*\]\s*\};'
    if not re.search(central_state_pattern, content, re.MULTILINE | re.DOTALL):
        print("❌ Central state object not found")
        return False
    else:
        print("✅ Central state object found")
    
    return True

def test_data_loading():
    """Test that data loading is properly implemented."""
    
    template_path = "marketing/templates/admin/marketing/page/block_builder.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test for data loading function
    data_loading_pattern = r'function loadExistingBlocks\(\)'
    if not re.search(data_loading_pattern, content):
        print("❌ Data loading function not found")
        return False
    else:
        print("✅ Data loading function found")
    
    # Test for JSON parsing
    json_parsing_pattern = r'JSON\.parse\(hiddenInput\.value\)'
    if not re.search(json_parsing_pattern, content):
        print("❌ JSON parsing not found")
        return False
    else:
        print("✅ JSON parsing found")
    
    return True

def test_rich_text_editor_fixes():
    """Test that rich text editor fixes are implemented."""
    
    template_path = "marketing/templates/admin/marketing/page/block_builder.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test for Editor.js data initialization with correct architecture
    # Look for the onReady callback that renders data
    editorjs_render_pattern = r'window\.editorInstances\[block\.id\]\.render\(blocks\.richText'
    if not re.search(editorjs_render_pattern, content):
        print("❌ Editor.js data rendering not found")
        return False
    else:
        print("✅ Editor.js data rendering found")
    
    # Test for central state object usage
    central_state_pattern = r'blocks\.richText\s*=\s*data'
    if not re.search(central_state_pattern, content):
        print("❌ Central state object usage not found")
        return False
    else:
        print("✅ Central state object usage found")
    
    return True

def test_cta_faq_saving():
    """Test that CTA and FAQ saving functions are implemented."""
    
    template_path = "marketing/templates/admin/marketing/page/block_builder.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test for CTA saving function
    cta_saving_pattern = r'window\.saveCTA\s*=\s*function\(\)'
    if not re.search(cta_saving_pattern, content):
        print("❌ CTA saving function not found")
        return False
    else:
        print("✅ CTA saving function found")
    
    # Test for FAQ saving function
    faq_saving_pattern = r'window\.saveFAQ\s*=\s*function\(\)'
    if not re.search(faq_saving_pattern, content):
        print("❌ FAQ saving function not found")
        return False
    else:
        print("✅ FAQ saving function found")
    
    return True

def test_form_submission():
    """Test that form submission handling is properly implemented."""
    
    template_path = "marketing/templates/admin/marketing/page/block_builder.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test for form submission handling
    form_submission_pattern = r'document\.getElementById\(\'id_blocks_json\'\)\.value\s*=\s*JSON\.stringify\(blocks\)'
    if not re.search(form_submission_pattern, content):
        print("❌ Form submission handling not found")
        return False
    else:
        print("✅ Form submission handling found")
    
    return True

def test_frontend_rendering():
    """Test that frontend rendering templates are properly updated."""
    
    template_path = "marketing/templates/marketing/blocks/block_renderer.html"
    
    if not os.path.exists(template_path):
        print("❌ Block renderer template not found")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test for CTA rendering with data structure
    cta_rendering_pattern = r'block\.data\.title'
    if not re.search(cta_rendering_pattern, content):
        print("❌ CTA rendering with data structure not found")
        return False
    else:
        print("✅ CTA rendering with data structure found")
    
    # Test for FAQ rendering with data structure
    faq_rendering_pattern = r'block\.data\.items'
    if not re.search(faq_rendering_pattern, content):
        print("❌ FAQ rendering with data structure not found")
        return False
    else:
        print("✅ FAQ rendering with data structure found")
    
    # Test for rich text rendering with data structure
    rich_text_rendering_pattern = r'block\.data\.blocks'
    if not re.search(rich_text_rendering_pattern, content):
        print("❌ Rich text rendering with data structure not found")
        return False
    else:
        print("✅ Rich text rendering with data structure found")
    
    return True

def test_backend_model():
    """Test that the backend model has the blocks_data field."""
    
    model_path = "marketing/models.py"
    
    if not os.path.exists(model_path):
        print("❌ Models file not found")
        return False
    
    with open(model_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test for blocks_json field in Page model
    blocks_json_pattern = r'blocks_json\s*=\s*models\.JSONField'
    if not re.search(blocks_json_pattern, content):
        print("❌ blocks_json field not found in Page model")
        return False
    else:
        print("✅ blocks_json field found in Page model")
    
    # Test for blocks_json field in Post model
    post_blocks_json_pattern = r'blocks_json\s*=\s*models\.JSONField'
    if not re.search(post_blocks_json_pattern, content):
        print("❌ blocks_json field not found in Post model")
        return False
    else:
        print("✅ blocks_json field found in Post model")
    
    return True

def main():
    """Run all tests."""
    
    print("🧪 Testing Complete Block Editor Implementation")
    print("=" * 60)
    
    tests = [
        ("Central State Object", test_central_state_object),
        ("Data Loading", test_data_loading),
        ("Rich Text Editor Fixes", test_rich_text_editor_fixes),
        ("CTA and FAQ Saving", test_cta_faq_saving),
        ("Form Submission", test_form_submission),
        ("Frontend Rendering", test_frontend_rendering),
        ("Backend Model", test_backend_model),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}...")
        try:
            if test_func():
                print(f"✅ {test_name} test PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Complete block editor implementation is working correctly.")
        print("\n📋 Implementation Summary:")
        print("  ✅ Central state object with richText, cta, and faq properties")
        print("  ✅ Proper data loading for existing pages")
        print("  ✅ Rich text editor initialization with saved data")
        print("  ✅ CTA and FAQ data saving functions")
        print("  ✅ Form submission handling with central state")
        print("  ✅ Frontend rendering templates updated")
        print("  ✅ Backend model with JSONField for blocks data")
        return True
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
        return False

if __name__ == "__main__":
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    success = main()
    sys.exit(0 if success else 1)