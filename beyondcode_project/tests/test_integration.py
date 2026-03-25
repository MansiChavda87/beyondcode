"""
TDD Integration Test Suite for Django CMS
Tests end-to-end functionality and integration between components
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from marketing.models import (
    Page, Post, Category, Tag, MediaAsset, NavMenu, Footer
)

User = get_user_model()


class TestCMSIntegration(TestCase):
    """Integration tests for CMS functionality"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Create test data
        self.create_test_data()
    
    def create_test_data(self):
        """Create comprehensive test data"""
        # Create navigation
        self.nav_menu = NavMenu.objects.create(name="Primary")
        
        # Create footer
        self.footer = Footer.objects.create(label="Default")
        
        # Create categories and tags
        self.category = Category.objects.create(
            name="AI & Machine Learning",
            slug="ai-machine-learning"
        )
        
        self.tag = Tag.objects.create(
            name="AI",
            slug="ai"
        )
    
    def test_complete_page_workflow(self):
        """Test complete page creation and publishing workflow"""
        # Login as user
        self.client.login(username='testuser', password='testpass123')
        
        # Create page
        response = self.client.post(reverse('marketing:page_create'), {
            'title': 'Integration Test Page',
            'slug': 'integration-test-page',
            'status': 'draft',
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': 'This is a test page created through integration testing.'
                        }
                    }
                ]
            }
        })
        self.assertEqual(response.status_code, 302)
        
        # Get the created page
        page = Page.objects.get(slug='integration-test-page')
        self.assertEqual(page.title, 'Integration Test Page')
        self.assertEqual(page.status, 'draft')
        
        # Edit page
        response = self.client.post(reverse('marketing:page_edit', kwargs={'pk': page.pk}), {
            'title': 'Updated Integration Test Page',
            'slug': 'integration-test-page',
            'status': 'published',
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': 'This page has been updated and published.'
                        }
                    }
                ]
            }
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify update
        page.refresh_from_db()
        self.assertEqual(page.title, 'Updated Integration Test Page')
        self.assertEqual(page.status, 'published')
        self.assertTrue(page.is_published)
        
        # View page publicly
        response = self.client.get(reverse('marketing:page_detail', kwargs={'slug': 'integration-test-page'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Updated Integration Test Page')
    
    def test_complete_post_workflow(self):
        """Test complete post creation and publishing workflow"""
        # Login as user
        self.client.login(username='testuser', password='testpass123')
        
        # Create post
        response = self.client.post(reverse('marketing:post_create'), {
            'title': 'Integration Test Post',
            'slug': 'integration-test-post',
            'status': 'draft',
            'author_name': 'Test Author',
            'excerpt': 'This is a test post.',
            'publish_at': timezone.now(),
            'categories': [self.category.id],
            'tags': [self.tag.id],
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': 'This is the content of the test post.'
                        }
                    }
                ]
            }
        })
        self.assertEqual(response.status_code, 302)
        
        # Get the created post
        post = Post.objects.get(slug='integration-test-post')
        self.assertEqual(post.title, 'Integration Test Post')
        self.assertEqual(post.status, 'draft')
        self.assertIn(self.category, post.categories.all())
        self.assertIn(self.tag, post.tags.all())
        
        # Edit post
        response = self.client.post(reverse('marketing:post_edit', kwargs={'pk': post.pk}), {
            'title': 'Updated Integration Test Post',
            'slug': 'integration-test-post',
            'status': 'published',
            'author_name': 'Updated Author',
            'excerpt': 'This is an updated test post.',
            'publish_at': timezone.now(),
            'categories': [self.category.id],
            'tags': [self.tag.id],
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': 'This post has been updated and published.'
                        }
                    }
                ]
            }
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify update
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Integration Test Post')
        self.assertEqual(post.status, 'published')
        self.assertEqual(post.author_name, 'Updated Author')
        self.assertTrue(post.is_published)
        
        # View post publicly
        response = self.client.get(reverse('marketing:blog_detail', kwargs={'slug': 'integration-test-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Updated Integration Test Post')
    
    def test_media_asset_workflow(self):
        """Test media asset upload and usage workflow"""
        # Login as user
        self.client.login(username='testuser', password='testpass123')
        
        # Upload media asset
        image_content = b'fake image content'
        uploaded_file = SimpleUploadedFile(
            "test_image.jpg",
            image_content,
            content_type="image/jpeg"
        )
        
        response = self.client.post(reverse('marketing:media_upload'), {
            'file_upload': uploaded_file,
            'alt_text': 'Test Image',
            'caption': 'This is a test image'
        })
        self.assertEqual(response.status_code, 302)
        
        # Get the created media asset
        media_asset = MediaAsset.objects.get(alt_text='Test Image')
        self.assertEqual(media_asset.alt_text, 'Test Image')
        self.assertEqual(media_asset.caption, 'This is a test image')
        self.assertTrue(media_asset.is_image)
        
        # Test media asset in page
        page = Page.objects.create(
            title="Page with Media",
            slug="page-with-media",
            status="published",
            blocks_json={
                'blocks': [
                    {
                        'type': 'image',
                        'data': {
                            'media_asset_id': media_asset.id,
                            'alt_text': 'Test Image'
                        }
                    }
                ]
            }
        )
        
        # View page with media
        response = self.client.get(reverse('marketing:page_detail', kwargs={'slug': 'page-with-media'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Page with Media')
    
    def test_navigation_and_footer_integration(self):
        """Test navigation and footer integration"""
        # Login as user
        self.client.login(username='testuser', password='testpass123')
        
        # Edit navigation
        response = self.client.post(reverse('marketing:navigation_edit'), {
            'items_json': [
                {
                    'label': 'Home',
                    'url': '/',
                    'type': 'internal'
                },
                {
                    'label': 'Blog',
                    'url': '/blog/',
                    'type': 'internal'
                },
                {
                    'label': 'Contact',
                    'url': '/contact/',
                    'type': 'internal'
                }
            ]
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify navigation was updated
        self.nav_menu.refresh_from_db()
        self.assertEqual(len(self.nav_menu.items_json), 3)
        
        # Edit footer
        response = self.client.post(reverse('marketing:footer_edit'), {
            'cta_title': 'Join Our Newsletter',
            'cta_body': 'Subscribe to get the latest updates.',
            'cta_button_label': 'Subscribe',
            'cta_button_url': '/newsletter/',
            'legal_text': '© 2024 BeyondCode AI. All rights reserved.'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify footer was updated
        self.footer.refresh_from_db()
        self.assertEqual(self.footer.cta_title, 'Join Our Newsletter')
        self.assertEqual(self.footer.legal_text, '© 2024 BeyondCode AI. All rights reserved.')
        
        # Test that navigation and footer appear on pages
        response = self.client.get(reverse('marketing:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home')
        self.assertContains(response, 'Join Our Newsletter')
    
    def test_authentication_flow(self):
        """Test complete authentication flow"""
        # Test registration
        response = self.client.post(reverse('marketing:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify user was created
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.email, 'newuser@example.com')
        
        # Test login
        response = self.client.post(reverse('marketing:login'), {
            'username': 'newuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify user is logged in
        response = self.client.get(reverse('marketing:account'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'newuser')
        
        # Test logout
        response = self.client.get(reverse('marketing:logout'))
        self.assertEqual(response.status_code, 302)
        
        # Verify user is logged out
        response = self.client.get(reverse('marketing:account'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_seo_integration(self):
        """Test SEO functionality integration"""
        # Create published content
        Page.objects.create(
            title="SEO Test Page",
            slug="seo-test-page",
            status="published",
            seo_title="SEO Optimized Page",
            seo_description="This page is optimized for search engines.",
            og_title="Open Graph Title",
            og_description="Open Graph description for social sharing."
        )
        
        Post.objects.create(
            title="SEO Test Post",
            slug="seo-test-post",
            status="published",
            publish_at=timezone.now(),
            seo_title="SEO Optimized Post",
            seo_description="This post is optimized for search engines.",
            og_title="Post Open Graph Title",
            og_description="Post Open Graph description."
        )
        
        # Test sitemap includes content
        response = self.client.get(reverse('marketing:sitemap'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'seo-test-page')
        self.assertContains(response, 'seo-test-post')
        
        # Test robots.txt
        response = self.client.get(reverse('marketing:robots'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User-agent: *')
    
    def test_cms_dashboard_integration(self):
        """Test CMS dashboard with all content types"""
        # Login as superuser
        self.client.login(username='admin', password='adminpass123')
        
        # Create various content
        page = Page.objects.create(title="Dashboard Test Page", slug="dashboard-test-page", status="published")
        post = Post.objects.create(title="Dashboard Test Post", slug="dashboard-test-post", status="published", author_name="Admin")
        media = MediaAsset.objects.create(file="https://example.com/test.jpg", alt_text="Dashboard Test Image")
        
        # Test dashboard shows all content
        response = self.client.get(reverse('marketing:cms_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard Test Page')
        self.assertContains(response, 'Dashboard Test Post')
        self.assertContains(response, 'Dashboard Test Image')
    
    def test_block_builder_integration(self):
        """Test block builder integration with page editing"""
        # Login as user
        self.client.login(username='testuser', password='testpass123')
        
        # Test block builder page
        response = self.client.get(reverse('marketing:block_builder'))
        self.assertEqual(response.status_code, 200)
        
        # Test block preview
        block_data = {
            'type': 'rich_text',
            'data': {
                'content': 'This is a preview of rich text content.'
            }
        }
        
        response = self.client.post(reverse('marketing:render_block_preview'), {
            'block_data': block_data
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'html': '<p>This is a preview of rich text content.</p>'})
    
    def test_error_handling_integration(self):
        """Test error handling across the application"""
        # Test 404 handling
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)
        
        # Test unauthorized access
        response = self.client.get(reverse('marketing:cms_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test invalid form submissions
        self.client.login(username='testuser', password='testpass123')
        
        # Invalid page creation (missing required fields)
        response = self.client.post(reverse('marketing:page_create'), {
            'title': '',  # Empty title
            'slug': 'invalid-page',
            'status': 'published'
        })
        self.assertEqual(response.status_code, 200)  # Should stay on form with errors
        
        # Invalid post creation (missing required fields)
        response = self.client.post(reverse('marketing:post_create'), {
            'title': '',  # Empty title
            'slug': 'invalid-post',
            'status': 'published',
            'author_name': 'Test Author'
        })
        self.assertEqual(response.status_code, 200)  # Should stay on form with errors
    
    def test_performance_integration(self):
        """Test performance with multiple content items"""
        # Login as superuser
        self.client.login(username='admin', password='adminpass123')
        
        # Create multiple pages and posts
        for i in range(10):
            Page.objects.create(
                title=f"Performance Test Page {i}",
                slug=f"performance-test-page-{i}",
                status="published"
            )
            
            Post.objects.create(
                title=f"Performance Test Post {i}",
                slug=f"performance-test-post-{i}",
                status="published",
                author_name="Admin",
                publish_at=timezone.now()
            )
        
        # Test that dashboard loads efficiently
        response = self.client.get(reverse('marketing:cms_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Test that list views handle pagination
        response = self.client.get(reverse('marketing:page_list'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('marketing:post_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_data_consistency_integration(self):
        """Test data consistency across operations"""
        # Create content with relationships
        page = Page.objects.create(title="Consistency Test Page", slug="consistency-test-page", status="published")
        post = Post.objects.create(title="Consistency Test Post", slug="consistency-test-post", status="published", author_name="Test Author")
        
        # Add relationships
        post.categories.add(self.category)
        post.tags.add(self.tag)
        
        # Test that relationships are maintained
        self.assertIn(self.category, post.categories.all())
        self.assertIn(self.tag, post.tags.all())
        
        # Test that deleting related objects doesn't break things
        self.category.delete()
        post.refresh_from_db()
        self.assertNotIn(self.category, post.categories.all())
        
        # Test that content can still be accessed
        response = self.client.get(reverse('marketing:page_detail', kwargs={'slug': 'consistency-test-page'}))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('marketing:blog_detail', kwargs={'slug': 'consistency-test-post'}))
        self.assertEqual(response.status_code, 200)