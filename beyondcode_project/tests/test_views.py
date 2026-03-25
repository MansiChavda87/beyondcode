"""
TDD Test Suite for Django CMS Views
Tests all view functionality with strict TDD approach
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from unittest.mock import patch, MagicMock

from marketing.models import (
    Page, Post, Category, Tag, MediaAsset, NavMenu, Footer
)

User = get_user_model()


class TestPublicViews(TestCase):
    """Test public-facing views"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test data
        self.create_test_data()
    
    def create_test_data(self):
        """Create test data for views"""
        # Create homepage
        self.homepage = Page.objects.create(
            title="Home",
            slug="home",
            status="published",
            blocks_html="<h1>Welcome to BeyondCode AI</h1>"
        )
        
        # Create navigation
        self.nav_menu = NavMenu.objects.create(name="Primary")
        
        # Create footer
        self.footer = Footer.objects.create(label="Default")
        
        # Create blog post
        self.post = Post.objects.create(
            title="Test Blog Post",
            slug="test-blog-post",
            status="published",
            author_name="Test Author",
            excerpt="Test excerpt",
            publish_at=timezone.now()
        )
        
        # Create category and tag
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category"
        )
        
        self.tag = Tag.objects.create(
            name="Test Tag",
            slug="test-tag"
        )
    
    def test_home_view(self):
        """Test homepage view"""
        response = self.client.get(reverse('marketing:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home")
        self.assertTemplateUsed(response, 'marketing/pages/home.html')
    
    def test_contact_view(self):
        """Test contact page view"""
        response = self.client.get(reverse('marketing:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/pages/contact.html')
    
    def test_contact_submit_valid(self):
        """Test contact form submission with valid data"""
        response = self.client.post(reverse('marketing:contact_submit'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Test message'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
    
    def test_contact_submit_invalid(self):
        """Test contact form submission with invalid data"""
        response = self.client.post(reverse('marketing:contact_submit'), {
            'name': '',
            'email': '',
            'message': ''
        })
        
        self.assertEqual(response.status_code, 302)  # Should redirect back to contact
    
    def test_page_detail_view(self):
        """Test page detail view"""
        response = self.client.get(reverse('marketing:page_detail', kwargs={'slug': 'home'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home")
        self.assertTemplateUsed(response, 'marketing/pages/detail.html')
    
    def test_page_detail_not_found(self):
        """Test page detail view for non-existent page"""
        response = self.client.get(reverse('marketing:page_detail', kwargs={'slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)
    
    def test_demo_page_view(self):
        """Test demo page view"""
        response = self.client.get(reverse('marketing:demo_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/pages/demo.html')
    
    def test_blog_list_view(self):
        """Test blog list view"""
        response = self.client.get(reverse('marketing:blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/blog/list.html')
    
    def test_blog_detail_view(self):
        """Test blog detail view"""
        response = self.client.get(reverse('marketing:blog_detail', kwargs={'slug': 'test-blog-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Blog Post")
        self.assertTemplateUsed(response, 'marketing/blog/detail.html')
    
    def test_blog_detail_not_found(self):
        """Test blog detail view for non-existent post"""
        response = self.client.get(reverse('marketing:blog_detail', kwargs={'slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)
    
    def test_blog_by_category_view(self):
        """Test blog by category view"""
        self.post.categories.add(self.category)
        
        response = self.client.get(reverse('marketing:blog_by_category', kwargs={'slug': 'test-category'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/blog/list.html')
    
    def test_blog_by_tag_view(self):
        """Test blog by tag view"""
        self.post.tags.add(self.tag)
        
        response = self.client.get(reverse('marketing:blog_by_tag', kwargs={'slug': 'test-tag'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/blog/list.html')


class TestCMSAdminViews(TestCase):
    """Test CMS admin views - addresses template and dashboard issues"""
    
    def setUp(self):
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
        """Create test data for CMS views"""
        # Create pages
        self.page = Page.objects.create(
            title="Test Page",
            slug="test-page",
            status="published"
        )
        
        # Create posts
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            status="published",
            author_name="Test Author"
        )
        
        # Create media assets
        self.media_asset = MediaAsset.objects.create(
            file="https://example.com/image.jpg",
            alt_text="Test image"
        )
    
    def test_cms_dashboard_without_auth(self):
        """Test CMS dashboard without authentication"""
        response = self.client.get(reverse('marketing:cms_dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
    
    def test_cms_dashboard_with_auth(self):
        """Test CMS dashboard with authentication"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:cms_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/dashboard.html')
    
    def test_cms_dashboard_with_superuser(self):
        """Test CMS dashboard with superuser"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('marketing:cms_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/dashboard.html')
    
    def test_page_list_view(self):
        """Test page list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:page_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/pages/list.html')
    
    def test_page_create_view_get(self):
        """Test page create view (GET)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:page_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/pages/form.html')
    
    def test_page_create_view_post(self):
        """Test page create view (POST)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('marketing:page_create'), {
            'title': 'New Page',
            'slug': 'new-page',
            'status': 'published'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
    
    def test_page_edit_view_get(self):
        """Test page edit view (GET)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:page_edit', kwargs={'pk': self.page.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/pages/form.html')
    
    def test_page_edit_view_post(self):
        """Test page edit view (POST)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('marketing:page_edit', kwargs={'pk': self.page.pk}), {
            'title': 'Updated Page',
            'slug': 'test-page',
            'status': 'published'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after update
    
    def test_page_delete_view_get(self):
        """Test page delete view (GET)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:page_delete', kwargs={'pk': self.page.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/pages/confirm_delete.html')
    
    def test_page_delete_view_post(self):
        """Test page delete view (POST)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('marketing:page_delete', kwargs={'pk': self.page.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
    
    def test_post_list_view(self):
        """Test post list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/posts/list.html')
    
    def test_post_create_view_get(self):
        """Test post create view (GET)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/posts/editor.html')
    
    def test_post_create_view_post(self):
        """Test post create view (POST)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('marketing:post_create'), {
            'title': 'New Post',
            'slug': 'new-post',
            'status': 'published',
            'author_name': 'Test Author',
            'excerpt': 'Test excerpt'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
    
    def test_post_edit_view_get(self):
        """Test post edit view (GET)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:post_edit', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/posts/editor.html')
    
    def test_post_edit_view_post(self):
        """Test post edit view (POST)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('marketing:post_edit', kwargs={'pk': self.post.pk}), {
            'title': 'Updated Post',
            'slug': 'test-post',
            'status': 'published',
            'author_name': 'Test Author',
            'excerpt': 'Updated excerpt'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after update
    
    def test_post_delete_view_get(self):
        """Test post delete view (GET)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/posts/confirm_delete.html')
    
    def test_post_delete_view_post(self):
        """Test post delete view (POST)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('marketing:post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
    
    def test_media_list_view(self):
        """Test media list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:media_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/media/list.html')
    
    def test_media_upload_view_get(self):
        """Test media upload view (GET)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:media_upload'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/media/form.html')
    
    def test_media_upload_view_post(self):
        """Test media upload view (POST)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('marketing:media_upload'), {
            'file': 'https://example.com/image.jpg',
            'alt_text': 'Test image'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after upload
    
    def test_media_delete_view_get(self):
        """Test media delete view (GET)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:media_delete', kwargs={'pk': self.media_asset.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/media/confirm_delete.html')
    
    def test_media_delete_view_post(self):
        """Test media delete view (POST)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('marketing:media_delete', kwargs={'pk': self.media_asset.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
    
    def test_navigation_edit_view(self):
        """Test navigation edit view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:navigation_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/navigation/form.html')
    
    def test_footer_edit_view(self):
        """Test footer edit view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:footer_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/footer/form.html')


class TestBlockBuilderViews(TestCase):
    """Test block builder views"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_block_builder_view(self):
        """Test block builder view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:block_builder'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/cms/blocks/builder.html')
    
    def test_render_block_preview_view(self):
        """Test render block preview view"""
        self.client.login(username='testuser', password='testpass123')
        
        block_data = {
            'type': 'rich_text',
            'data': {
                'content': 'Test content'
            }
        }
        
        response = self.client.post(reverse('marketing:render_block_preview'), {
            'block_data': block_data
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'html': '<p>Test content</p>'})


class TestAuthenticationViews(TestCase):
    """Test authentication views - addresses CMS-specific login flow"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_view_get(self):
        """Test login view (GET)"""
        response = self.client.get(reverse('marketing:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/auth/login.html')
    
    def test_login_view_post_valid(self):
        """Test login view (POST) with valid credentials"""
        response = self.client.post(reverse('marketing:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
    
    def test_login_view_post_invalid(self):
        """Test login view (POST) with invalid credentials"""
        response = self.client.post(reverse('marketing:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertTemplateUsed(response, 'marketing/auth/login.html')
    
    def test_register_view_get(self):
        """Test register view (GET)"""
        response = self.client.get(reverse('marketing:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/auth/register.html')
    
    def test_register_view_post_valid(self):
        """Test register view (POST) with valid data"""
        response = self.client.post(reverse('marketing:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
    
    def test_logout_view(self):
        """Test logout view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
    
    def test_account_view(self):
        """Test account view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/auth/account.html')


class TestSEOViews(TestCase):
    """Test SEO views - addresses missing robots.txt and sitemap.xml"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test data
        self.create_test_data()
    
    def create_test_data(self):
        """Create test data for SEO views"""
        # Create published pages
        Page.objects.create(
            title="Home",
            slug="home",
            status="published"
        )
        
        Page.objects.create(
            title="About",
            slug="about",
            status="published"
        )
        
        # Create published posts
        Post.objects.create(
            title="Test Post",
            slug="test-post",
            status="published",
            publish_at=timezone.now()
        )
        
        # Create category and tag
        Category.objects.create(
            name="Test Category",
            slug="test-category"
        )
        
        Tag.objects.create(
            name="Test Tag",
            slug="test-tag"
        )
    
    def test_sitemap_view(self):
        """Test sitemap view"""
        response = self.client.get(reverse('marketing:sitemap'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertContains(response, 'urlset')
    
    def test_robots_view(self):
        """Test robots.txt view"""
        response = self.client.get(reverse('marketing:robots'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertContains(response, 'User-agent: *')


class TestAPIViews(TestCase):
    """Test API views"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test data
        self.create_test_data()
    
    def create_test_data(self):
        """Create test data for API views"""
        # Create media assets
        MediaAsset.objects.create(
            file="https://example.com/image1.jpg",
            alt_text="Image 1"
        )
        
        MediaAsset.objects.create(
            file="https://example.com/image2.jpg",
            alt_text="Image 2"
        )
        
        # Create categories
        Category.objects.create(
            name="Category 1",
            slug="category-1"
        )
        
        Category.objects.create(
            name="Category 2",
            slug="category-2"
        )
        
        # Create tags
        Tag.objects.create(
            name="Tag 1",
            slug="tag-1"
        )
        
        Tag.objects.create(
            name="Tag 2",
            slug="tag-2"
        )
    
    def test_api_media_list(self):
        """Test media list API"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:api_media_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
    
    def test_api_categories(self):
        """Test categories API"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:api_categories'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
    
    def test_api_tags(self):
        """Test tags API"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:api_tags'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')