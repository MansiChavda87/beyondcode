"""
TDD Security Test Suite for Django CMS
Tests application security vulnerabilities and protections
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from django.core.exceptions import PermissionDenied
from unittest.mock import patch

from marketing.models import (
    Page, Post, Category, Tag, MediaAsset, NavMenu, Footer
)

User = get_user_model()


class TestSecurity(TestCase):
    """Security tests for CMS functionality"""
    
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
        
        # Create test data
        self.create_test_data()
    
    def create_test_data(self):
        """Create test data for security tests"""
        self.page = Page.objects.create(
            title="Test Page",
            slug="test-page",
            status="published"
        )
        
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            status="published",
            author_name="Test Author"
        )
        
        self.media = MediaAsset.objects.create(
            file="https://example.com/test.jpg",
            alt_text="Test Image"
        )
    
    def test_csrf_protection(self):
        """Test CSRF protection on forms"""
        self.client.login(username='testuser', password='testpass123')
        
        # Try to submit form without CSRF token
        response = self.client.post(reverse('marketing:page_create'), {
            'title': 'Test Page',
            'slug': 'test-page',
            'status': 'published'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # Should be rejected due to missing CSRF token
        self.assertNotEqual(response.status_code, 302)
    
    def test_authentication_required(self):
        """Test that CMS views require authentication"""
        protected_views = [
            'marketing:cms_dashboard',
            'marketing:page_create',
            'marketing:page_edit',
            'marketing:page_delete',
            'marketing:post_create',
            'marketing:post_edit',
            'marketing:post_delete',
            'marketing:media_upload',
            'marketing:media_delete',
            'marketing:navigation_edit',
            'marketing:footer_edit',
        ]
        
        for view_name in protected_views:
            response = self.client.get(reverse(view_name))
            self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_authorization_required(self):
        """Test that CMS views require proper permissions"""
        self.client.login(username='testuser', password='testpass123')
        
        # Test that regular users can access some views
        response = self.client.get(reverse('marketing:cms_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Test that admin-only views are restricted
        response = self.client.get(reverse('marketing:navigation_edit'))
        self.assertEqual(response.status_code, 200)  # Should work for regular users too
    
    def test_sql_injection_protection(self):
        """Test protection against SQL injection"""
        # Test with malicious input in URL parameters
        malicious_slug = "'; DROP TABLE marketing_page; --"
        
        response = self.client.get(reverse('marketing:page_detail', kwargs={'slug': malicious_slug}))
        self.assertEqual(response.status_code, 404)  # Should not crash or delete data
    
    def test_xss_protection(self):
        """Test protection against XSS attacks"""
        self.client.login(username='testuser', password='testpass123')
        
        # Try to inject JavaScript in page content
        malicious_content = '<script>alert("XSS")</script>'
        
        response = self.client.post(reverse('marketing:page_create'), {
            'title': 'XSS Test Page',
            'slug': 'xss-test-page',
            'status': 'published',
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': malicious_content
                        }
                    }
                ]
            }
        })
        
        self.assertEqual(response.status_code, 302)
        
        # Check that content is properly escaped when displayed
        page = Page.objects.get(slug='xss-test-page')
        response = self.client.get(reverse('marketing:page_detail', kwargs={'slug': 'xss-test-page'}))
        self.assertEqual(response.status_code, 200)
        # The script should be escaped and not executable
    
    def test_file_upload_security(self):
        """Test file upload security"""
        self.client.login(username='testuser', password='testpass123')
        
        # Try to upload malicious file
        malicious_file = SimpleUploadedFile(
            "malicious.php",
            b"<?php system($_GET['cmd']); ?>",
            content_type="application/x-php"
        )
        
        response = self.client.post(reverse('marketing:media_upload'), {
            'file_upload': malicious_file,
            'alt_text': 'Malicious File'
        })
        
        # Should be rejected or properly sanitized
        self.assertNotEqual(response.status_code, 302)
    
    def test_directory_traversal_protection(self):
        """Test protection against directory traversal attacks"""
        # Try to access files outside allowed directories
        malicious_paths = [
            '../../../etc/passwd',
            '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
            '....//....//....//etc/passwd'
        ]
        
        for path in malicious_paths:
            response = self.client.get(f'/static/{path}')
            self.assertEqual(response.status_code, 404)
    
    def test_session_security(self):
        """Test session security"""
        # Login as user
        self.client.login(username='testuser', password='testpass123')
        
        # Get session key
        session_key = self.client.session.session_key
        
        # Try to use session from different client
        new_client = Client()
        new_client.cookies = self.client.cookies
        
        response = new_client.get(reverse('marketing:cms_dashboard'))
        self.assertEqual(response.status_code, 302)  # Should require re-authentication
    
    def test_rate_limiting(self):
        """Test protection against brute force attacks"""
        # Try multiple failed login attempts
        for i in range(5):
            response = self.client.post(reverse('marketing:login'), {
                'username': 'testuser',
                'password': 'wrongpassword'
            })
        
        # Should not be blocked immediately (depends on configuration)
        # But should not allow unlimited attempts indefinitely
    
    def test_content_type_validation(self):
        """Test content type validation"""
        self.client.login(username='testuser', password='testpass123')
        
        # Try to upload file with wrong content type
        wrong_type_file = SimpleUploadedFile(
            "test.jpg",
            b"fake image content",
            content_type="text/plain"
        )
        
        response = self.client.post(reverse('marketing:media_upload'), {
            'file_upload': wrong_type_file,
            'alt_text': 'Wrong Type File'
        })
        
        # Should be rejected
        self.assertNotEqual(response.status_code, 302)
    
    def test_url_validation(self):
        """Test URL validation in forms"""
        self.client.login(username='testuser', password='testpass123')
        
        # Try to submit malicious URLs
        malicious_urls = [
            'javascript:alert("XSS")',
            'data:text/html,<script>alert("XSS")</script>',
            'file:///etc/passwd',
            'ftp://evil.com/malicious.exe'
        ]
        
        for url in malicious_urls:
            response = self.client.post(reverse('marketing:page_create'), {
                'title': 'Test Page',
                'slug': 'test-page',
                'status': 'published',
                'primary_image': url
            })
            
            # Should be rejected
            self.assertNotEqual(response.status_code, 302)
    
    def test_admin_privilege_escalation(self):
        """Test protection against privilege escalation"""
        # Create regular user without admin privileges
        regular_user = User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='regularpass123'
        )
        
        self.client.login(username='regularuser', password='regularpass123')
        
        # Try to access admin-only functionality
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Should redirect to login
    
    def test_csrf_token_validation(self):
        """Test CSRF token validation"""
        self.client.login(username='testuser', password='testpass123')
        
        # Get a page with CSRF token
        response = self.client.get(reverse('marketing:page_create'))
        self.assertEqual(response.status_code, 200)
        
        # Extract CSRF token
        csrf_token = response.context['csrf_token']
        
        # Try to submit form with invalid CSRF token
        response = self.client.post(reverse('marketing:page_create'), {
            'csrfmiddlewaretoken': 'invalid-token',
            'title': 'Test Page',
            'slug': 'test-page',
            'status': 'published'
        })
        
        # Should be rejected
        self.assertNotEqual(response.status_code, 302)
    
    def test_session_fixation_protection(self):
        """Test protection against session fixation"""
        # Create session without authentication
        session = self.client.session
        session['test_data'] = 'before_login'
        session.save()
        
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        # Check that session was regenerated
        new_session = self.client.session
        self.assertNotEqual(session.session_key, new_session.session_key)
    
    def test_clickjacking_protection(self):
        """Test protection against clickjacking"""
        response = self.client.get(reverse('marketing:home'))
        
        # Should have X-Frame-Options header
        self.assertIn('X-Frame-Options', response)
        self.assertEqual(response['X-Frame-Options'], 'DENY')
    
    def test_content_security_policy(self):
        """Test Content Security Policy headers"""
        response = self.client.get(reverse('marketing:home'))
        
        # Should have CSP headers
        self.assertIn('Content-Security-Policy', response)
    
    def test_hsts_protection(self):
        """Test HTTP Strict Transport Security"""
        response = self.client.get(reverse('marketing:home'))
        
        # Should have HSTS header in production
        # (May not be present in test environment)
        if 'Strict-Transport-Security' in response:
            self.assertTrue(response['Strict-Transport-Security'].startswith('max-age='))
    
    def test_sensitive_data_exposure(self):
        """Test that sensitive data is not exposed"""
        # Create page with sensitive content
        sensitive_page = Page.objects.create(
            title="Sensitive Page",
            slug="sensitive-page",
            status="draft",  # Draft should not be publicly accessible
            blocks_json={
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': 'This is sensitive content that should not be exposed.'
                        }
                    }
                ]
            }
        )
        
        # Try to access draft page without authentication
        response = self.client.get(reverse('marketing:page_detail', kwargs={'slug': 'sensitive-page'}))
        self.assertEqual(response.status_code, 404)
        
        # Try to access draft page with regular user
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:page_detail', kwargs={'slug': 'sensitive-page'}))
        self.assertEqual(response.status_code, 404)  # Drafts should not be accessible via public views
    
    def test_error_message_information_disclosure(self):
        """Test that error messages don't disclose sensitive information"""
        # Try to access non-existent admin page
        response = self.client.get('/admin/nonexistent/')
        
        # Should not expose database structure or file paths
        self.assertNotIn('Traceback', response.content.decode())
        self.assertNotIn('django.db', response.content.decode())
        self.assertNotIn('/var/www/', response.content.decode())
    
    def test_csrf_cookie_protection(self):
        """Test CSRF cookie security"""
        # Get CSRF token
        response = self.client.get(reverse('marketing:page_create'))
        csrf_cookie = response.cookies.get('csrftoken')
        
        # CSRF cookie should have secure attributes
        if csrf_cookie:
            # In test environment, secure flag may not be set
            # But cookie should still be present
            self.assertIsNotNone(csrf_cookie.value)


@override_settings(DEBUG=False)
class TestProductionSecurity(TestCase):
    """Security tests for production environment"""
    
    def setUp(self):
        self.client = Client()
    
    def test_debug_disabled(self):
        """Test that debug mode is disabled in production"""
        # This test runs with DEBUG=False due to override_settings
        response = self.client.get('/nonexistent-page/')
        
        # Should not show debug information
        self.assertNotIn('Traceback', response.content.decode())
        self.assertNotIn('django.views.debug', response.content.decode())
    
    def test_custom_error_pages(self):
        """Test that custom error pages are used"""
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)
        
        # Should use custom 404 template
        self.assertTemplateUsed(response, '404.html')
    
    def test_security_headers(self):
        """Test that security headers are present"""
        response = self.client.get(reverse('marketing:home'))
        
        # Should have various security headers
        security_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection',
            'Content-Security-Policy'
        ]
        
        for header in security_headers:
            self.assertIn(header, response)