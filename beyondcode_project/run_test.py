#!/usr/bin/env python3
"""
Simple test runner for the block editor tests
"""

import os
import sys
import subprocess

def run_test(test_file):
    """Run a specific test file"""
    print(f"Running {test_file}...")
    print("=" * 50)
    
    try:
        # Run the test from the current directory
        result = subprocess.run([sys.executable, f'beyondcode_project/{test_file}'], 
                              capture_output=True, text=True, timeout=60)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✓ {test_file} completed successfully!")
        else:
            print(f"✗ {test_file} failed with return code {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print(f"✗ {test_file} timed out after 60 seconds")
    except Exception as e:
        print(f"✗ Error running {test_file}: {e}")

def main():
    """Main test runner"""
    print("Block Editor Test Runner")
    print("=" * 50)
    
    # List of test files to run
    test_files = [
        'test_editorjs_integration.py',
        'test_simple_block_editor.py',
        'test_admin_integration.py'
    ]
    
    for test_file in test_files:
        if os.path.exists(f'beyondcode_project/{test_file}'):
            run_test(test_file)
            print("\n" + "=" * 50 + "\n")
        else:
            print(f"✗ Test file {test_file} not found in beyondcode_project/")
    
    print("Test runner completed!")

if __name__ == '__main__':
    main()