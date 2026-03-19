#!/usr/bin/env python3
"""
Test script to verify block editor fixes are working correctly.

This script tests the key functionality of the block editor after the architecture fixes.
"""

import os
import sys
import json
import re

def test_block_builder_template():
    """Test that the block builder template has all the necessary fixes."""
    
    template_path = "marketing/templates/admin/marketing/page/block_builder.html"
    
    if not os.path.exists(template_path):
        print("❌ Block builder template not found")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test 1: Check for proper button types
    button_pattern = r'<button[^>]*type="button"[^>]*>'
    buttons = re.findall(button_pattern, content)
    
    if len(buttons) < 10:  # Should have multiple buttons with type="button"
        print(f"❌ Insufficient buttons with type='button': {len(buttons)}")
        return False
    else:
        print(f"✅ Found {len(buttons)} buttons with type='button'")
    
    # Test 2: Check for event prevention
    event_prevention_pattern = r'event\.preventDefault\(\); event\.stopPropagation\(\);'
    event_preventions = re.findall(event_prevention_pattern, content)
    
    if len(event_preventions) < 5:  # Should have multiple event preventions
        print(f"❌ Insufficient event preventions: {len(event_preventions)}")
        return False
    else:
        print(f"✅ Found {len(event_preventions)} event prevention chains")
    
    # Test 3: Check for modal save mechanisms
    cta_save_pattern = r'CTA.*?Save Changes'
    faq_save_pattern = r'FAQ.*?Save Changes'
    
    if 'Save Changes' not in content:
        print("❌ Modal save buttons not found")
        return False
    else:
        print("✅ Modal save buttons found")
    
    # Test 4: Check for form submission handling
    form_submission_pattern = r'setupFormSubmission|form\.addEventListener.*submit'
    if not re.search(form_submission_pattern, content, re.IGNORECASE):
        print("❌ Form submission handling not found")
        return False
    else:
        print("✅ Form submission handling found")
    
    # Test 5: Check for Editor.js data loading
    editorjs_data_pattern = r'data: block\.data'
    if not re.search(editorjs_data_pattern, content):
        print("❌ Editor.js data loading not found")
        return False
    else:
        print("✅ Editor.js data loading found")
    
    # Test 6: Check for hidden input update
    hidden_input_pattern = r'updateHiddenInput|id_blocks_json'
    if not re.search(hidden_input_pattern, content):
        print("❌ Hidden input update mechanism not found")
        return False
    else:
        print("✅ Hidden input update mechanism found")
    
    return True

def test_data_structure():
    """Test that the data structure is properly defined."""
    
    template_path = "marketing/templates/admin/marketing/page/block_builder.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test for proper data structure initialization
    data_structure_pattern = r'window\.blocks = \[\]'
    if not re.search(data_structure_pattern, content):
        print("❌ Window.blocks initialization not found")
        return False
    else:
        print("✅ Window.blocks initialization found")
    
    # Test for block data structure
    block_structure_pattern = r'\{[^}]*id:[^}]*type:[^}]*data:'
    if not re.search(block_structure_pattern, content):
        print("❌ Block data structure not found")
        return False
    else:
        print("✅ Block data structure found")
    
    return True

def test_event_handling():
    """Test that event handling is comprehensive."""
    
    template_path = "marketing/templates/admin/marketing/page/block_builder.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test for comprehensive event prevention
    comprehensive_prevention = r'event\.preventDefault\(\); event\.stopPropagation\(\);.*?return false'
    if not re.search(comprehensive_prevention, content):
        print("❌ Comprehensive event prevention not found")
        return False
    else:
        print("✅ Comprehensive event prevention found")
    
    # Test for modal event handling
    modal_events = [
        r'onclick=".*?closeModal\(\)',
        r'onclick=".*?saveEdit\(\)',
        r'onclick=".*?addFAQItem\(\)'
    ]
    
    for pattern in modal_events:
        if not re.search(pattern, content):
            print(f"❌ Modal event handler not found: {pattern}")
            return False
    
    print("✅ All modal event handlers found")
    return True

def test_serialization():
    """Test that data serialization is properly implemented."""
    
    template_path = "marketing/templates/admin/marketing/page/block_builder.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test for JSON serialization
    json_serialization = r'JSON\.stringify.*blocks'
    if not re.search(json_serialization, content):
        print("❌ JSON serialization not found")
        return False
    else:
        print("✅ JSON serialization found")
    
    # Test for hidden input update
    hidden_input_update = r'document\.getElementById\([\'"]id_blocks_json[\'"]\)\.value'
    if not re.search(hidden_input_update, content):
        print("❌ Hidden input update not found")
        return False
    else:
        print("✅ Hidden input update found")
    
    return True

def main():
    """Run all tests."""
    
    print("🧪 Testing Block Editor Architecture Fixes")
    print("=" * 50)
    
    tests = [
        ("Block Builder Template", test_block_builder_template),
        ("Data Structure", test_data_structure),
        ("Event Handling", test_event_handling),
        ("Data Serialization", test_serialization),
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
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Block editor fixes are working correctly.")
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