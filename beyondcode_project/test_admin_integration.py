#!/usr/bin/env python3
"""
Test script to verify the admin block builder integration
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
django.setup()

from marketing.models import Page, Post, Category, Tag


class AdminIntegrationTest(TestCase):
    """Test the admin block builder integration"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        User = get_user_model()
        
        # Try to get existing user or create new one
        try:
            self.user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
        
        self.client.login(username='admin', password='admin123')
        
        # Create test category and tag
        self.category, created = Category.objects.get_or_create(
            name='Test Category', 
            slug='test-category'
        )
        self.tag, created = Tag.objects.get_or_create(
            name='Test Tag', 
            slug='test-tag'
        )
    
    def test_page_admin_form_has_block_builder(self):
        """Test that the page admin form includes the block builder"""
        response = self.client.get(reverse('admin:marketing_page_add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Block Builder')
        self.assertContains(response, 'Add Block')
        self.assertContains(response, 'Drag and drop')
        self.assertContains(response, 'Live Preview')
    
    def test_post_admin_form_has_block_builder(self):
        """Test that the post admin form includes the block builder"""
        response = self.client.get(reverse('admin:marketing_post_add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Block Builder')
        self.assertContains(response, 'Add Block')
        self.assertContains(response, 'Drag and drop')
        self.assertContains(response, 'Live Preview')
    
    def test_page_admin_edit_has_block_builder(self):
        """Test that editing a page includes the block builder"""
        page = Page.objects.create(
            title='Test Page',
            slug='test-page',
            status='published',
            blocks_json='{"blocks": []}'
        )
        response = self.client.get(reverse('admin:marketing_page_change', args=[page.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Block Builder')
        self.assertContains(response, 'Add Block')
        self.assertContains(response, 'Drag and drop')
        self.assertContains(response, 'Live Preview')
    
    def test_post_admin_edit_has_block_builder(self):
        """Test that editing a post includes the block builder"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            status='published',
            author_name='Test Author',
            blocks_json='{"blocks": []}'
        )
        response = self.client.get(reverse('admin:marketing_post_change', args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Block Builder')
        self.assertContains(response, 'Add Block')
        self.assertContains(response, 'Drag and drop')
        self.assertContains(response, 'Live Preview')


def run_tests():
    """Run the admin integration tests"""
    print("Testing Admin Block Builder Integration...")
    print("=" * 50)
    
    # Create a test suite
    import unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(AdminIntegrationTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n✓ All admin integration tests passed!")
        return True
    else:
        print(f"\n✗ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        for failure in result.failures:
            print(f"FAILURE: {failure[0]}")
            print(failure[1])
        for error in result.errors:
            print(f"ERROR: {error[0]}")
            print(error[1])
        return False


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)