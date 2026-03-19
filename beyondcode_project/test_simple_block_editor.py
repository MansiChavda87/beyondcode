#!/usr/bin/env python3
"""
Test script for the simple block editor functionality
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

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from marketing.models import Post, Category, Tag
from marketing.forms import PostForm

User = get_user_model()

def test_simple_block_editor():
    """Test the simple block editor functionality"""
    print("Testing Simple Block Editor Functionality...")
    
    # Create a test user (handle if user already exists)
    try:
        user = User.objects.get(username='testuser')
        print("✓ Using existing test user")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print("✓ Created new test user")
    user.is_staff = True
    user.save()
    
    # Create test categories and tags
    category = Category.objects.create(name='Test Category', slug='test-category')
    tag = Tag.objects.create(name='Test Tag', slug='test-tag')
    
    # Test block data structure for simple blocks
    test_blocks = [
        {
            "id": 1,
            "type": "rich_text",
            "data": {
                "time": 1700000000000,
                "version": "2.29.1",
                "blocks": [
                    {
                        "type": "paragraph",
                        "data": {
                            "text": "This is a test paragraph block."
                        }
                    },
                    {
                        "type": "header",
                        "data": {
                            "text": "Test Heading",
                            "level": 2
                        }
                    }
                ]
            }
        },
        {
            "id": 2,
            "type": "cta",
            "data": {
                "title": "Call to Action Title",
                "body": "Description for your call to action.",
                "button_label": "Click Here",
                "button_url": "#"
            }
        },
        {
            "id": 3,
            "type": "faq",
            "data": {
                "title": "Frequently Asked Questions",
                "items": [
                    {
                        "question": "What is this?",
                        "answer": "This is a sample FAQ answer."
                    },
                    {
                        "question": "How does it work?",
                        "answer": "It works by using block-based content."
                    }
                ]
            }
        }
    ]
    
    # Test form creation with blocks
    form_data = {
        'title': 'Test Post with Simple Blocks',
        'slug': 'test-post-with-simple-blocks',
        'status': 'draft',
        'author_name': 'Test Author',
        'excerpt': 'This is a test post with simple block-based content.',
        'seo_title': 'Test Post SEO Title',
        'seo_description': 'Test post description for SEO',
        'categories': [category.id],
        'tags': [tag.id],
        'blocks_json': test_blocks
    }
    
    form = PostForm(data=form_data)
    
    if form.is_valid():
        print("✓ Form validation passed")
        post = form.save(commit=False)
        post.author = user
        post.save()
        form.save_m2m()
        
        print(f"✓ Post created: {post.title}")
        print(f"✓ Blocks JSON saved: {len(post.blocks_json)} blocks")
        
        # Test that blocks_json is properly stored
        if post.blocks_json and len(post.blocks_json) == 3:
            print("✓ All blocks saved correctly")
            
            # Test block types
            block_types = [block['type'] for block in post.blocks_json]
            expected_types = ['rich_text', 'cta', 'faq']
            
            if block_types == expected_types:
                print("✓ Block types are correct")
            else:
                print(f"✗ Block types mismatch. Expected: {expected_types}, Got: {block_types}")
                
        else:
            print(f"✗ Blocks not saved correctly. Expected 3 blocks, got {len(post.blocks_json) if post.blocks_json else 0}")
            
        # Test that blocks_html is generated
        if post.blocks_html and len(post.blocks_html) > 0:
            print("✓ Blocks HTML generated successfully")
            print(f"  HTML length: {len(post.blocks_html)} characters")
        else:
            print("✗ Blocks HTML not generated")
            
        # Test post retrieval
        retrieved_post = Post.objects.get(slug='test-post-with-simple-blocks')
        if retrieved_post.blocks_json:
            print("✓ Post retrieved with blocks")
        else:
            print("✗ Post retrieved without blocks")
            
        # Test the render_blocks function
        from marketing.blocks import render_blocks
        html_output = render_blocks({"blocks": test_blocks})
        if html_output and len(html_output) > 0:
            print("✓ render_blocks function works correctly")
            print(f"  Generated HTML length: {len(html_output)} characters")
        else:
            print("✗ render_blocks function failed")
            
    else:
        print("✗ Form validation failed:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
    
    # Clean up
    post.delete()
    category.delete()
    tag.delete()
    user.delete()
    
    print("\nSimple Block Editor Test Complete!")

if __name__ == '__main__':
    test_simple_block_editor()