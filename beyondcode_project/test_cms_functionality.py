#!/usr/bin/env python3
"""
Comprehensive test script for BeyondCode AI CMS functionality
Tests all core features including models, views, templates, and APIs
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test.utils import override_settings
from django.conf import settings

# Add the project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')

# Setup Django
django.setup()

from marketing.models import (
    Page, Post, Category, Tag, MediaAsset, Navigation, Footer,
    RichTextBlock, CalloutBlock, FeatureGridBlock, CTABlock,
    PricingTableBlock, FAQBlock, ComparisonTableBlock, ImageBlock,
    VideoBlock, TestimonialBlock, StatsBlock, ContactFormBlock
)
from marketing.views import (
    PageListView, PageDetailView, PostListView, PostDetailView,
    PostByCategoryView, PostByTagView, BlockBuilderView
)
from marketing.permissions import has_cms_permission


class CMSFunctionalityTest(TestCase):
    """Test suite for BeyondCode AI CMS functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create superuser
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Create test data
        self.create_test_data()
    
    def create_test_data(self):
        """Create test data for testing"""
        # Create categories
        self.category1 = Category.objects.create(
            name='AI & Machine Learning',
            slug='ai-machine-learning',
            description='Posts about AI and machine learning'
        )
        
        self.category2 = Category.objects.create(
            name='Collections',
            slug='collections',
            description='Posts about collections'
        )
        
        # Create tags
        self.tag1 = Tag.objects.create(
            name='AI',
            slug='ai'
        )
        
        self.tag2 = Tag.objects.create(
            name='Automation',
            slug='automation'
        )
        
        # Create pages
        self.page1 = Page.objects.create(
            title='Home',
            slug='home',
            status='published',
            meta_title='Home - BeyondCode AI',
            meta_description='Welcome to BeyondCode AI',
            blocks_json={
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': 'Welcome to our homepage!'
                        }
                    }
                ]
            }
        )
        
        self.page2 = Page.objects.create(
            title='About',
            slug='about',
            status='published',
            meta_title='About Us - BeyondCode AI',
            meta_description='Learn about our company'
        )
        
        # Create posts
        self.post1 = Post.objects.create(
            title='Introduction to AI Collections',
            slug='introduction-to-ai-collections',
            status='published',
            author_name='Test Author',
            excerpt='A comprehensive guide to AI collections',
            publish_at='2024-01-01 10:00:00',
            blocks_json={
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': 'This is a test post about AI collections.'
                        }
                    }
                ]
            }
        )
        
        self.post1.categories.add(self.category1)
        self.post1.tags.add(self.tag1)
        
        self.post2 = Post.objects.create(
            title='Collections Automation',
            slug='collections-automation',
            status='published',
            author_name='Test Author',
            excerpt='How to automate collections',
            publish_at='2024-01-02 10:00:00'
        )
        
        self.post2.categories.add(self.category2)
        self.post2.tags.add(self.tag2)
        
        # Create media assets
        self.media1 = MediaAsset.objects.create(
            title='Test Image',
            file_type='image',
            file_url='https://example.com/test-image.jpg',
            file_size=1024,
            dimensions='800x600'
        )
        
        # Create navigation
        self.navigation = Navigation.objects.create(
            name='Main Navigation',
            items_json=[
                {
                    'label': 'Home',
                    'url': '/',
                    'type': 'internal'
                },
                {
                    'label': 'Blog',
                    'url': '/blog/',
                    'type': 'internal'
                }
            ]
        )
        
        # Create footer
        self.footer = Footer.objects.create(
            copyright_text='© 2024 BeyondCode AI. All rights reserved.',
            social_links_json=[
                {
                    'platform': 'twitter',
                    'url': 'https://twitter.com/beyondcodeai'
                },
                {
                    'platform': 'linkedin',
                    'url': 'https://linkedin.com/company/beyondcodeai'
                }
            ]
        )
    
    def test_page_models(self):
        """Test Page model functionality"""
        print("Testing Page models...")
        
        # Test page creation
        self.assertEqual(Page.objects.count(), 2)
        self.assertEqual(self.page1.title, 'Home')
        self.assertEqual(self.page1.slug, 'home')
        self.assertEqual(self.page1.status, 'published')
        
        # Test page URL generation
        self.assertEqual(self.page2.get_absolute_url(), '/pages/about/')
        
        # Test page status choices
        draft_page = Page.objects.create(
            title='Draft Page',
            slug='draft-page',
            status='draft'
        )
        self.assertEqual(draft_page.status, 'draft')
        
        print("✓ Page models test passed")
    
    def test_post_models(self):
        """Test Post model functionality"""
        print("Testing Post models...")
        
        # Test post creation
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(self.post1.title, 'Introduction to AI Collections')
        self.assertEqual(self.post1.slug, 'introduction-to-ai-collections')
        self.assertEqual(self.post1.status, 'published')
        
        # Test post relationships
        self.assertIn(self.category1, self.post1.categories.all())
        self.assertIn(self.tag1, self.post1.tags.all())
        
        # Test post URL generation
        self.assertEqual(self.post1.get_absolute_url(), '/blog/introduction-to-ai-collections/')
        
        # Test post manager
        published_posts = Post.objects.published()
        self.assertEqual(published_posts.count(), 2)
        
        print("✓ Post models test passed")
    
    def test_category_and_tag_models(self):
        """Test Category and Tag models"""
        print("Testing Category and Tag models...")
        
        # Test category creation
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(self.category1.name, 'AI & Machine Learning')
        self.assertEqual(self.category1.slug, 'ai-machine-learning')
        
        # Test tag creation
        self.assertEqual(Tag.objects.count(), 2)
        self.assertEqual(self.tag1.name, 'AI')
        self.assertEqual(self.tag1.slug, 'ai')
        
        # Test category posts relationship
        self.assertIn(self.post1, self.category1.posts.all())
        
        print("✓ Category and Tag models test passed")
    
    def test_media_asset_model(self):
        """Test MediaAsset model"""
        print("Testing MediaAsset model...")
        
        self.assertEqual(MediaAsset.objects.count(), 1)
        self.assertEqual(self.media1.title, 'Test Image')
        self.assertEqual(self.media1.file_type, 'image')
        self.assertEqual(self.media1.file_url, 'https://example.com/test-image.jpg')
        
        print("✓ MediaAsset model test passed")
    
    def test_navigation_and_footer_models(self):
        """Test Navigation and Footer models"""
        print("Testing Navigation and Footer models...")
        
        self.assertEqual(Navigation.objects.count(), 1)
        self.assertEqual(self.navigation.name, 'Main Navigation')
        
        self.assertEqual(Footer.objects.count(), 1)
        self.assertEqual(self.footer.copyright_text, '© 2024 BeyondCode AI. All rights reserved.')
        
        print("✓ Navigation and Footer models test passed")
    
    def test_block_models(self):
        """Test block models"""
        print("Testing block models...")
        
        # Test RichTextBlock
        rich_text_block = RichTextBlock.objects.create(
            content={
                'time': 1234567890,
                'version': '2.30.2',
                'blocks': [
                    {
                        'type': 'paragraph',
                        'data': {
                            'text': 'Test content'
                        }
                    }
                ]
            }
        )
        self.assertEqual(rich_text_block.content['blocks'][0]['data']['text'], 'Test content')
        
        # Test CalloutBlock
        callout_block = CalloutBlock.objects.create(
            title='Test Callout',
            body='This is a test callout'
        )
        self.assertEqual(callout_block.title, 'Test Callout')
        
        # Test FeatureGridBlock
        feature_grid_block = FeatureGridBlock.objects.create(
            title='Test Features',
            items=[
                {'title': 'Feature 1', 'body': 'Description 1'},
                {'title': 'Feature 2', 'body': 'Description 2'}
            ]
        )
        self.assertEqual(feature_grid_block.title, 'Test Features')
        self.assertEqual(len(feature_grid_block.items), 2)
        
        print("✓ Block models test passed")
    
    def test_page_views(self):
        """Test page views"""
        print("Testing page views...")
        
        # Test page list view
        response = self.client.get(reverse('marketing:page_list'))
        self.assertEqual(response.status_code, 200)
        
        # Test page detail view
        response = self.client.get(reverse('marketing:page_detail', kwargs={'slug': 'home'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home')
        
        # Test non-existent page
        response = self.client.get(reverse('marketing:page_detail', kwargs={'slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)
        
        print("✓ Page views test passed")
    
    def test_post_views(self):
        """Test post views"""
        print("Testing post views...")
        
        # Test post list view
        response = self.client.get(reverse('marketing:blog_list'))
        self.assertEqual(response.status_code, 200)
        
        # Test post detail view
        response = self.client.get(reverse('marketing:blog_detail', kwargs={'slug': 'introduction-to-ai-collections'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Introduction to AI Collections')
        
        # Test post by category
        response = self.client.get(reverse('marketing:blog_by_category', kwargs={'slug': 'ai-machine-learning'}))
        self.assertEqual(response.status_code, 200)
        
        # Test post by tag
        response = self.client.get(reverse('marketing:blog_by_tag', kwargs={'slug': 'ai'}))
        self.assertEqual(response.status_code, 200)
        
        print("✓ Post views test passed")
    
    def test_cms_views(self):
        """Test CMS views"""
        print("Testing CMS views...")
        
        # Test dashboard without authentication
        response = self.client.get(reverse('marketing:cms_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test dashboard with authentication
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:cms_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Test block builder
        response = self.client.get(reverse('marketing:block_builder'))
        self.assertEqual(response.status_code, 200)
        
        print("✓ CMS views test passed")
    
    def test_api_views(self):
        """Test API views"""
        print("Testing API views...")
        
        # Test media list API
        response = self.client.get(reverse('marketing:api_media_list'))
        self.assertEqual(response.status_code, 200)
        
        # Test categories API
        response = self.client.get(reverse('marketing:api_categories'))
        self.assertEqual(response.status_code, 200)
        
        # Test tags API
        response = self.client.get(reverse('marketing:api_tags'))
        self.assertEqual(response.status_code, 200)
        
        print("✓ API views test passed")
    
    def test_permissions(self):
        """Test permission system"""
        print("Testing permissions...")
        
        # Test has_cms_permission function
        self.assertTrue(has_cms_permission(self.superuser))
        self.assertFalse(has_cms_permission(self.user))
        
        # Give user CMS permission
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_page'),
            Permission.objects.get(codename='change_page'),
            Permission.objects.get(codename='delete_page'),
            Permission.objects.get(codename='view_page')
        )
        
        self.assertTrue(has_cms_permission(self.user))
        
        print("✓ Permissions test passed")
    
    def test_management_commands(self):
        """Test management commands"""
        print("Testing management commands...")
        
        # Test seed_cms_content command
        call_command('seed_cms_content')
        
        # Check if content was created
        self.assertGreater(Page.objects.count(), 0)
        self.assertGreater(Post.objects.count(), 0)
        self.assertGreater(Category.objects.count(), 0)
        self.assertGreater(Tag.objects.count(), 0)
        
        print("✓ Management commands test passed")
    
    def test_template_rendering(self):
        """Test template rendering"""
        print("Testing template rendering...")
        
        # Test base template
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Test blog list template
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        
        # Test blog detail template
        response = self.client.get('/blog/introduction-to-ai-collections/')
        self.assertEqual(response.status_code, 200)
        
        print("✓ Template rendering test passed")
    
    def test_seo_functionality(self):
        """Test SEO functionality"""
        print("Testing SEO functionality...")
        
        # Test sitemap
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'urlset')
        
        # Test robots.txt
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User-agent: *')
        
        print("✓ SEO functionality test passed")
    
    def test_search_functionality(self):
        """Test search functionality"""
        print("Testing search functionality...")
        
        # Test search API
        response = self.client.get('/marketing/api/search/?q=test')
        self.assertEqual(response.status_code, 200)
        
        print("✓ Search functionality test passed")
    
    def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("BEYONDCODE AI CMS FUNCTIONALITY TEST SUITE")
        print("=" * 60)
        
        try:
            self.test_page_models()
            self.test_post_models()
            self.test_category_and_tag_models()
            self.test_media_asset_model()
            self.test_navigation_and_footer_models()
            self.test_block_models()
            self.test_page_views()
            self.test_post_views()
            self.test_cms_views()
            self.test_api_views()
            self.test_permissions()
            self.test_management_commands()
            self.test_template_rendering()
            self.test_seo_functionality()
            self.test_search_functionality()
            
            print("\n" + "=" * 60)
            print("🎉 ALL TESTS PASSED! 🎉")
            print("The BeyondCode AI CMS is fully functional!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ TEST FAILED: {e}")
            print("=" * 60)
            return False
        
        return True


def main():
    """Main test runner"""
    # Create test instance
    test_suite = CMSFunctionalityTest()
    test_suite.setUp()
    
    # Run all tests
    success = test_suite.run_all_tests()
    
    if success:
        print("\n✅ CMS functionality verification completed successfully!")
        print("All core features are working as expected.")
    else:
        print("\n❌ CMS functionality verification failed!")
        print("Some features may not be working correctly.")
    
    return success


if __name__ == '__main__':
    main()