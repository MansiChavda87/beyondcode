#!/usr/bin/env python3
"""
Test script for the block editor functionality
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

def test_block_editor():
    """Test the block editor functionality"""
    print("Testing Block Editor Functionality...")
    
    # Create a test user
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    user.is_staff = True
    user.save()
    
    # Create test categories and tags
    category = Category.objects.create(name='Test Category', slug='test-category')
    tag = Tag.objects.create(name='Test Tag', slug='test-tag')
    
    # Test block data structure
    test_blocks = [
        {
            "id": 1,
            "type": "paragraph",
            "data": {
                "text": "This is a test paragraph block."
            }
        },
        {
            "id": 2,
            "type": "heading",
            "data": {
                "text": "Test Heading",
                "level": "h2"
            }
        },
        {
            "id": 3,
            "type": "list",
            "data": {
                "style": "unordered",
                "items": ["First item", "Second item", "Third item"]
            }
        },
        {
            "id": 4,
            "type": "quote",
            "data": {
                "text": "This is a test quote.",
                "caption": "Test Author"
            }
        },
        {
            "id": 5,
            "type": "code",
            "data": {
                "code": "console.log('Hello World');",
                "language": "javascript"
            }
        }
    ]
    
    # Test form creation with blocks
    form_data = {
        'title': 'Test Post with Blocks',
        'slug': 'test-post-with-blocks',
        'status': 'draft',
        'author_name': 'Test Author',
        'excerpt': 'This is a test post with block-based content.',
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
        if post.blocks_json and len(post.blocks_json) == 5:
            print("✓ All blocks saved correctly")
            
            # Test block types
            block_types = [block['type'] for block in post.blocks_json]
            expected_types = ['paragraph', 'heading', 'list', 'quote', 'code']
            
            if block_types == expected_types:
                print("✓ Block types are correct")
            else:
                print(f"✗ Block types mismatch. Expected: {expected_types}, Got: {block_types}")
                
        else:
            print(f"✗ Blocks not saved correctly. Expected 5 blocks, got {len(post.blocks_json) if post.blocks_json else 0}")
            
        # Test post retrieval
        retrieved_post = Post.objects.get(slug='test-post-with-blocks')
        if retrieved_post.blocks_json:
            print("✓ Post retrieved with blocks")
        else:
            print("✗ Post retrieved without blocks")
            
    else:
        print("✗ Form validation failed:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
    
    # Clean up
    post.delete()
    category.delete()
    tag.delete()
    user.delete()
    
    print("\nBlock Editor Test Complete!")

if __name__ == '__main__':
    test_block_editor()