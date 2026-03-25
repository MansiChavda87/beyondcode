"""
TDD End-to-End Test Suite for Django CMS
Tests complete user workflows and scenarios
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time

User = get_user_model()


class TestE2EWorkflows(TestCase):
    """End-to-end workflow tests"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
    
    def test_user_registration_and_login_workflow(self):
        """Test complete user registration and login workflow"""
        # 1. User visits homepage
        response = self.client.get(reverse('marketing:home'))
        self.assertEqual(response.status_code, 200)
        
        # 2. User clicks register link
        response = self.client.get(reverse('marketing:register'))
        self.assertEqual(response.status_code, 200)
        
        # 3. User fills registration form
        response = self.client.post(reverse('marketing:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        
        # 4. User is created
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.email, 'newuser@example.com')
        
        # 5. User logs in
        response = self.client.post(reverse('marketing:login'), {
            'username': 'newuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        
        # 6. User accesses account page
        response = self.client.get(reverse('marketing:account'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'newuser')
    
    def test_content_creation_workflow(self):
        """Test complete content creation workflow"""
        self.client.login(username='testuser', password='testpass123')
        
        # 1. User visits CMS dashboard
        response = self.client.get(reverse('marketing:cms_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # 2. User creates a new page
        response = self.client.post(reverse('marketing:page_create'), {
            'title': 'E2E Test Page',
            'slug': 'e2e-test-page',
            'status': 'draft',
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': 'This is content created through E2E testing.'
                        }
                    }
                ]
            }
        })
        self.assertEqual(response.status_code, 302)
        
        # 3. Page is created
        page = Page.objects.get(slug='e2e-test-page')
        self.assertEqual(page.title, 'E2E Test Page')
        self.assertEqual(page.status, 'draft')
        
        # 4. User edits the page
        response = self.client.post(reverse('marketing:page_edit', kwargs={'pk': page.pk}), {
            'title': 'Updated E2E Test Page',
            'slug': 'e2e-test-page',
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
        
        # 5. Page is updated
        page.refresh_from_db()
        self.assertEqual(page.title, 'Updated E2E Test Page')
        self.assertEqual(page.status, 'published')
        
        # 6. Page is publicly accessible
        response = self.client.get(reverse('marketing:page_detail', kwargs={'slug': 'e2e-test-page'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Updated E2E Test Page')
    
    def test_blog_post_workflow(self):
        """Test complete blog post creation and publishing workflow"""
        self.client.login(username='testuser', password='testpass123')
        
        # 1. User creates categories and tags
        category = Category.objects.create(name="E2E Testing", slug="e2e-testing")
        tag = Tag.objects.create(name="Testing", slug="testing")
        
        # 2. User creates a blog post
        response = self.client.post(reverse('marketing:post_create'), {
            'title': 'E2E Testing Best Practices',
            'slug': 'e2e-testing-best-practices',
            'status': 'draft',
            'author_name': 'Test Author',
            'excerpt': 'Best practices for E2E testing.',
            'publish_at': timezone.now(),
            'categories': [category.id],
            'tags': [tag.id],
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': 'This is a comprehensive guide to E2E testing.'
                        }
                    }
                ]
            }
        })
        self.assertEqual(response.status_code, 302)
        
        # 3. Post is created
        post = Post.objects.get(slug='e2e-testing-best-practices')
        self.assertEqual(post.title, 'E2E Testing Best Practices')
        self.assertEqual(post.status, 'draft')
        self.assertIn(category, post.categories.all())
        self.assertIn(tag, post.tags.all())
        
        # 4. User publishes the post
        response = self.client.post(reverse('marketing:post_edit', kwargs={'pk': post.pk}), {
            'title': 'E2E Testing Best Practices',
            'slug': 'e2e-testing-best-practices',
            'status': 'published',
            'author_name': 'Test Author',
            'excerpt': 'Best practices for E2E testing.',
            'publish_at': timezone.now(),
            'categories': [category.id],
            'tags': [tag.id],
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': 'This is a comprehensive guide to E2E testing.'
                        }
                    }
                ]
            }
        })
        self.assertEqual(response.status_code, 302)
        
        # 5. Post is published
        post.refresh_from_db()
        self.assertEqual(post.status, 'published')
        
        # 6. Post is publicly accessible
        response = self.client.get(reverse('marketing:blog_detail', kwargs={'slug': 'e2e-testing-best-practices'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E2E Testing Best Practices')
        
        # 7. Post appears in blog list
        response = self.client.get(reverse('marketing:blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E2E Testing Best Practices')
        
        # 8. Post appears in category list
        response = self.client.get(reverse('marketing:blog_by_category', kwargs={'slug': 'e2e-testing'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E2E Testing Best Practices')
        
        # 9. Post appears in tag list
        response = self.client.get(reverse('marketing:blog_by_tag', kwargs={'slug': 'testing'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E2E Testing Best Practices')
    
    def test_media_management_workflow(self):
        """Test complete media asset management workflow"""
        self.client.login(username='testuser', password='testpass123')
        
        # 1. User uploads media asset
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        image_content = b'fake image content'
        uploaded_file = SimpleUploadedFile(
            "e2e_test_image.jpg",
            image_content,
            content_type="image/jpeg"
        )
        
        response = self.client.post(reverse('marketing:media_upload'), {
            'file_upload': uploaded_file,
            'alt_text': 'E2E Test Image',
            'caption': 'This image was uploaded during E2E testing.'
        })
        self.assertEqual(response.status_code, 302)
        
        # 2. Media asset is created
        media = MediaAsset.objects.get(alt_text='E2E Test Image')
        self.assertEqual(media.caption, 'This image was uploaded during E2E testing.')
        
        # 3. User uses media in a page
        page = Page.objects.create(
            title="Page with E2E Media",
            slug="page-with-e2e-media",
            status="published",
            blocks_json={
                'blocks': [
                    {
                        'type': 'image',
                        'data': {
                            'media_asset_id': media.id,
                            'alt_text': 'E2E Test Image'
                        }
                    }
                ]
            }
        )
        
        # 4. Page with media is accessible
        response = self.client.get(reverse('marketing:page_detail', kwargs={'slug': 'page-with-e2e-media'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Page with E2E Media')
    
    def test_navigation_and_footer_workflow(self):
        """Test navigation and footer management workflow"""
        self.client.login(username='testuser', password='testpass123')
        
        # 1. User edits navigation
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
                    'label': 'About',
                    'url': '/pages/about/',
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
        
        # 2. Navigation is updated
        nav_menu = NavMenu.objects.filter(name="Primary").first()
        self.assertIsNotNone(nav_menu)
        self.assertEqual(len(nav_menu.items_json), 4)
        
        # 3. User edits footer
        response = self.client.post(reverse('marketing:footer_edit'), {
            'cta_title': 'Join Our Community',
            'cta_body': 'Subscribe to our newsletter for updates.',
            'cta_button_label': 'Subscribe Now',
            'cta_button_url': '/newsletter/',
            'legal_text': '© 2024 E2E Test Site. All rights reserved.'
        })
        self.assertEqual(response.status_code, 302)
        
        # 4. Footer is updated
        footer = Footer.objects.filter(label="Default").first()
        self.assertIsNotNone(footer)
        self.assertEqual(footer.cta_title, 'Join Our Community')
        self.assertEqual(footer.legal_text, '© 2024 E2E Test Site. All rights reserved.')
        
        # 5. Navigation and footer appear on pages
        response = self.client.get(reverse('marketing:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home')
        self.assertContains(response, 'Join Our Community')
    
    def test_seo_workflow(self):
        """Test SEO optimization workflow"""
        self.client.login(username='testuser', password='testpass123')
        
        # 1. User creates SEO-optimized page
        response = self.client.post(reverse('marketing:page_create'), {
            'title': 'SEO Optimized Page',
            'slug': 'seo-optimized-page',
            'status': 'published',
            'seo_title': 'SEO Optimized Page Title',
            'seo_description': 'This page is optimized for search engines.',
            'og_title': 'Open Graph Title',
            'og_description': 'Open Graph description for social sharing.',
            'og_image': 'https://example.com/og-image.jpg',
            'twitter_image': 'https://example.com/twitter-image.jpg',
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': 'This is SEO-optimized content.'
                        }
                    }
                ]
            }
        })
        self.assertEqual(response.status_code, 302)
        
        # 2. Page is created with SEO fields
        page = Page.objects.get(slug='seo-optimized-page')
        self.assertEqual(page.seo_title, 'SEO Optimized Page Title')
        self.assertEqual(page.seo_description, 'This page is optimized for search engines.')
        
        # 3. Page appears in sitemap
        response = self.client.get(reverse('marketing:sitemap'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'seo-optimized-page')
        
        # 4. Robots.txt is accessible
        response = self.client.get(reverse('marketing:robots'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User-agent: *')
    
    def test_error_handling_workflow(self):
        """Test error handling and user feedback workflow"""
        # 1. User tries to access non-existent page
        response = self.client.get('/pages/nonexistent-page/')
        self.assertEqual(response.status_code, 404)
        
        # 2. User tries to access protected content without authentication
        response = self.client.get(reverse('marketing:cms_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # 3. User tries to access protected content with invalid credentials
        response = self.client.post(reverse('marketing:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page
        
        # 4. User tries to submit invalid form data
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('marketing:page_create'), {
            'title': '',  # Empty title
            'slug': 'invalid-page',
            'status': 'published'
        })
        self.assertEqual(response.status_code, 200)  # Stay on form with errors
        
        # 5. User tries to access restricted functionality
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Redirect to admin login
    
    def test_performance_workflow(self):
        """Test performance under realistic load"""
        self.client.login(username='admin', password='adminpass123')
        
        # 1. Create multiple content items
        for i in range(20):
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
        
        # 2. Test dashboard performance
        start_time = time.time()
        response = self.client.get(reverse('marketing:cms_dashboard'))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 2.0, "Dashboard should load quickly")
        
        # 3. Test list page performance
        start_time = time.time()
        response = self.client.get(reverse('marketing:page_list'))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 1.5, "Page list should load quickly")
        
        # 4. Test public page performance
        start_time = time.time()
        response = self.client.get(reverse('marketing:home'))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 1.0, "Public pages should load quickly")


class TestE2EUserScenarios(TestCase):
    """End-to-end user scenario tests"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test users
        self.content_editor = User.objects.create_user(
            username='editor',
            email='editor@example.com',
            password='editorpass123'
        )
        
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Create test data
        self.create_test_content()
    
    def create_test_content(self):
        """Create test content for scenarios"""
        # Create categories and tags
        self.category = Category.objects.create(
            name="Technology",
            slug="technology",
            description="Technology-related content"
        )
        
        self.tag = Tag.objects.create(
            name="AI",
            slug="ai"
        )
        
        # Create published content
        self.homepage = Page.objects.create(
            title="Home",
            slug="home",
            status="published",
            blocks_html="<h1>Welcome to Our Site</h1>"
        )
        
        self.about_page = Page.objects.create(
            title="About Us",
            slug="about",
            status="published",
            blocks_html="<h1>About Our Company</h1>"
        )
        
        self.blog_post = Post.objects.create(
            title="Introduction to AI",
            slug="introduction-to-ai",
            status="published",
            author_name="Editor",
            excerpt="An introduction to artificial intelligence.",
            publish_at=timezone.now(),
            blocks_html="<h1>Introduction to AI</h1><p>Content about AI...</p>"
        )
        
        self.blog_post.categories.add(self.category)
        self.blog_post.tags.add(self.tag)
    
    def test_content_editor_workflow(self):
        """Test workflow for content editor"""
        # 1. Editor logs in
        self.client.login(username='editor', password='editorpass123')
        
        # 2. Editor visits dashboard
        response = self.client.get(reverse('marketing:cms_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # 3. Editor creates new blog post
        response = self.client.post(reverse('marketing:post_create'), {
            'title': 'New Blog Post',
            'slug': 'new-blog-post',
            'status': 'draft',
            'author_name': 'Editor',
            'excerpt': 'A new blog post.',
            'publish_at': timezone.now(),
            'categories': [self.category.id],
            'tags': [self.tag.id],
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': 'This is the content of the new blog post.'
                        }
                    }
                ]
            }
        })
        self.assertEqual(response.status_code, 302)
        
        # 4. Editor edits the post
        post = Post.objects.get(slug='new-blog-post')
        response = self.client.post(reverse('marketing:post_edit', kwargs={'pk': post.pk}), {
            'title': 'Updated Blog Post',
            'slug': 'new-blog-post',
            'status': 'published',
            'author_name': 'Editor',
            'excerpt': 'An updated blog post.',
            'publish_at': timezone.now(),
            'categories': [self.category.id],
            'tags': [self.tag.id],
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': 'This is the updated content of the blog post.'
                        }
                    }
                ]
            }
        })
        self.assertEqual(response.status_code, 302)
        
        # 5. Post is published and accessible
        post.refresh_from_db()
        self.assertEqual(post.status, 'published')
        
        response = self.client.get(reverse('marketing:blog_detail', kwargs={'slug': 'new-blog-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Updated Blog Post')
    
    def test_admin_workflow(self):
        """Test workflow for admin user"""
        # 1. Admin logs in
        self.client.login(username='admin', password='adminpass123')
        
        # 2. Admin manages navigation
        response = self.client.post(reverse('marketing:navigation_edit'), {
            'items_json': [
                {
                    'label': 'Home',
                    'url': '/',
                    'type': 'internal'
                },
                {
                    'label': 'About',
                    'url': '/pages/about/',
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
        
        # 3. Admin manages footer
        response = self.client.post(reverse('marketing:footer_edit'), {
            'cta_title': 'Stay Updated',
            'cta_body': 'Subscribe to our newsletter.',
            'cta_button_label': 'Subscribe',
            'cta_button_url': '/newsletter/',
            'legal_text': '© 2024 Company. All rights reserved.'
        })
        self.assertEqual(response.status_code, 302)
        
        # 4. Admin reviews content
        response = self.client.get(reverse('marketing:cms_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home')
        self.assertContains(response, 'Introduction to AI')
    
    def test_visitor_workflow(self):
        """Test workflow for site visitor"""
        # 1. Visitor visits homepage
        response = self.client.get(reverse('marketing:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Our Site')
        
        # 2. Visitor visits about page
        response = self.client.get(reverse('marketing:page_detail', kwargs={'slug': 'about'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About Our Company')
        
        # 3. Visitor visits blog
        response = self.client.get(reverse('marketing:blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Introduction to AI')
        
        # 4. Visitor reads blog post
        response = self.client.get(reverse('marketing:blog_detail', kwargs={'slug': 'introduction-to-ai'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Introduction to AI')
        
        # 5. Visitor browses by category
        response = self.client.get(reverse('marketing:blog_by_category', kwargs={'slug': 'technology'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Introduction to AI')
        
        # 6. Visitor browses by tag
        response = self.client.get(reverse('marketing:blog_by_tag', kwargs={'slug': 'ai'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Introduction to AI')
        
        # 7. Visitor accesses SEO endpoints
        response = self.client.get(reverse('marketing:sitemap'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('marketing:robots'))
        self.assertEqual(response.status_code, 200)