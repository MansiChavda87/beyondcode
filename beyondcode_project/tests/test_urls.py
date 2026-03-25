"""
TDD URL Test Suite for Django CMS
Tests all URL patterns and routing functionality
"""

from django.test import TestCase
from django.urls import reverse, resolve, NoReverseMatch
from django.http import HttpResponseNotFound


class TestURLPatterns(TestCase):
    """Test URL patterns and routing"""
    
    def test_home_url(self):
        """Test home URL pattern"""
        url = reverse('marketing:home')
        self.assertEqual(url, '/')
        
        # Test that URL resolves to correct view
        resolved = resolve('/')
        self.assertEqual(resolved.view_name, 'marketing:home')
    
    def test_contact_url(self):
        """Test contact URL pattern"""
        url = reverse('marketing:contact')
        self.assertEqual(url, '/contact/')
        
        resolved = resolve('/contact/')
        self.assertEqual(resolved.view_name, 'marketing:contact')
    
    def test_contact_submit_url(self):
        """Test contact submit URL pattern"""
        url = reverse('marketing:contact_submit')
        self.assertEqual(url, '/contact/submit/')
        
        resolved = resolve('/contact/submit/')
        self.assertEqual(resolved.view_name, 'marketing:contact_submit')
    
    def test_page_detail_url(self):
        """Test page detail URL pattern"""
        url = reverse('marketing:page_detail', kwargs={'slug': 'test-page'})
        self.assertEqual(url, '/pages/test-page/')
        
        resolved = resolve('/pages/test-page/')
        self.assertEqual(resolved.view_name, 'marketing:page_detail')
        self.assertEqual(resolved.kwargs['slug'], 'test-page')
    
    def test_demo_page_url(self):
        """Test demo page URL pattern"""
        url = reverse('marketing:demo_page')
        self.assertEqual(url, '/demo/')
        
        resolved = resolve('/demo/')
        self.assertEqual(resolved.view_name, 'marketing:demo_page')
    
    def test_blog_list_url(self):
        """Test blog list URL pattern"""
        url = reverse('marketing:blog_list')
        self.assertEqual(url, '/blog/')
        
        resolved = resolve('/blog/')
        self.assertEqual(resolved.view_name, 'marketing:blog_list')
    
    def test_blog_detail_url(self):
        """Test blog detail URL pattern"""
        url = reverse('marketing:blog_detail', kwargs={'slug': 'test-post'})
        self.assertEqual(url, '/blog/test-post/')
        
        resolved = resolve('/blog/test-post/')
        self.assertEqual(resolved.view_name, 'marketing:blog_detail')
        self.assertEqual(resolved.kwargs['slug'], 'test-post')
    
    def test_blog_by_category_url(self):
        """Test blog by category URL pattern"""
        url = reverse('marketing:blog_by_category', kwargs={'slug': 'test-category'})
        self.assertEqual(url, '/blog/category/test-category/')
        
        resolved = resolve('/blog/category/test-category/')
        self.assertEqual(resolved.view_name, 'marketing:blog_by_category')
        self.assertEqual(resolved.kwargs['slug'], 'test-category')
    
    def test_blog_by_tag_url(self):
        """Test blog by tag URL pattern"""
        url = reverse('marketing:blog_by_tag', kwargs={'slug': 'test-tag'})
        self.assertEqual(url, '/blog/tag/test-tag/')
        
        resolved = resolve('/blog/tag/test-tag/')
        self.assertEqual(resolved.view_name, 'marketing:blog_by_tag')
        self.assertEqual(resolved.kwargs['slug'], 'test-tag')
    
    def test_cms_dashboard_url(self):
        """Test CMS dashboard URL pattern"""
        url = reverse('marketing:cms_dashboard')
        self.assertEqual(url, '/cms/')
        
        resolved = resolve('/cms/')
        self.assertEqual(resolved.view_name, 'marketing:cms_dashboard')
    
    def test_page_list_url(self):
        """Test page list URL pattern"""
        url = reverse('marketing:page_list')
        self.assertEqual(url, '/cms/pages/')
        
        resolved = resolve('/cms/pages/')
        self.assertEqual(resolved.view_name, 'marketing:page_list')
    
    def test_page_create_url(self):
        """Test page create URL pattern"""
        url = reverse('marketing:page_create')
        self.assertEqual(url, '/cms/pages/create/')
        
        resolved = resolve('/cms/pages/create/')
        self.assertEqual(resolved.view_name, 'marketing:page_create')
    
    def test_page_edit_url(self):
        """Test page edit URL pattern"""
        url = reverse('marketing:page_edit', kwargs={'pk': 1})
        self.assertEqual(url, '/cms/pages/1/edit/')
        
        resolved = resolve('/cms/pages/1/edit/')
        self.assertEqual(resolved.view_name, 'marketing:page_edit')
        self.assertEqual(resolved.kwargs['pk'], '1')
    
    def test_page_delete_url(self):
        """Test page delete URL pattern"""
        url = reverse('marketing:page_delete', kwargs={'pk': 1})
        self.assertEqual(url, '/cms/pages/1/delete/')
        
        resolved = resolve('/cms/pages/1/delete/')
        self.assertEqual(resolved.view_name, 'marketing:page_delete')
        self.assertEqual(resolved.kwargs['pk'], '1')
    
    def test_post_list_url(self):
        """Test post list URL pattern"""
        url = reverse('marketing:post_list')
        self.assertEqual(url, '/cms/posts/')
        
        resolved = resolve('/cms/posts/')
        self.assertEqual(resolved.view_name, 'marketing:post_list')
    
    def test_post_create_url(self):
        """Test post create URL pattern"""
        url = reverse('marketing:post_create')
        self.assertEqual(url, '/cms/posts/create/')
        
        resolved = resolve('/cms/posts/create/')
        self.assertEqual(resolved.view_name, 'marketing:post_create')
    
    def test_post_edit_url(self):
        """Test post edit URL pattern"""
        url = reverse('marketing:post_edit', kwargs={'pk': 1})
        self.assertEqual(url, '/cms/posts/1/edit/')
        
        resolved = resolve('/cms/posts/1/edit/')
        self.assertEqual(resolved.view_name, 'marketing:post_edit')
        self.assertEqual(resolved.kwargs['pk'], '1')
    
    def test_post_delete_url(self):
        """Test post delete URL pattern"""
        url = reverse('marketing:post_delete', kwargs={'pk': 1})
        self.assertEqual(url, '/cms/posts/1/delete/')
        
        resolved = resolve('/cms/posts/1/delete/')
        self.assertEqual(resolved.view_name, 'marketing:post_delete')
        self.assertEqual(resolved.kwargs['pk'], '1')
    
    def test_media_list_url(self):
        """Test media list URL pattern"""
        url = reverse('marketing:media_list')
        self.assertEqual(url, '/cms/media/')
        
        resolved = resolve('/cms/media/')
        self.assertEqual(resolved.view_name, 'marketing:media_list')
    
    def test_media_upload_url(self):
        """Test media upload URL pattern"""
        url = reverse('marketing:media_upload')
        self.assertEqual(url, '/cms/media/upload/')
        
        resolved = resolve('/cms/media/upload/')
        self.assertEqual(resolved.view_name, 'marketing:media_upload')
    
    def test_media_delete_url(self):
        """Test media delete URL pattern"""
        url = reverse('marketing:media_delete', kwargs={'pk': 1})
        self.assertEqual(url, '/cms/media/1/delete/')
        
        resolved = resolve('/cms/media/1/delete/')
        self.assertEqual(resolved.view_name, 'marketing:media_delete')
        self.assertEqual(resolved.kwargs['pk'], '1')
    
    def test_navigation_edit_url(self):
        """Test navigation edit URL pattern"""
        url = reverse('marketing:navigation_edit')
        self.assertEqual(url, '/cms/navigation/')
        
        resolved = resolve('/cms/navigation/')
        self.assertEqual(resolved.view_name, 'marketing:navigation_edit')
    
    def test_footer_edit_url(self):
        """Test footer edit URL pattern"""
        url = reverse('marketing:footer_edit')
        self.assertEqual(url, '/cms/footer/')
        
        resolved = resolve('/cms/footer/')
        self.assertEqual(resolved.view_name, 'marketing:footer_edit')
    
    def test_block_builder_url(self):
        """Test block builder URL pattern"""
        url = reverse('marketing:block_builder')
        self.assertEqual(url, '/cms/blocks/')
        
        resolved = resolve('/cms/blocks/')
        self.assertEqual(resolved.view_name, 'marketing:block_builder')
    
    def test_render_block_preview_url(self):
        """Test render block preview URL pattern"""
        url = reverse('marketing:render_block_preview')
        self.assertEqual(url, '/cms/blocks/preview/')
        
        resolved = resolve('/cms/blocks/preview/')
        self.assertEqual(resolved.view_name, 'marketing:render_block_preview')
    
    def test_login_url(self):
        """Test login URL pattern"""
        url = reverse('marketing:login')
        self.assertEqual(url, '/accounts/login/')
        
        resolved = resolve('/accounts/login/')
        self.assertEqual(resolved.view_name, 'marketing:login')
    
    def test_register_url(self):
        """Test register URL pattern"""
        url = reverse('marketing:register')
        self.assertEqual(url, '/accounts/register/')
        
        resolved = resolve('/accounts/register/')
        self.assertEqual(resolved.view_name, 'marketing:register')
    
    def test_logout_url(self):
        """Test logout URL pattern"""
        url = reverse('marketing:logout')
        self.assertEqual(url, '/accounts/logout/')
        
        resolved = resolve('/accounts/logout/')
        self.assertEqual(resolved.view_name, 'marketing:logout')
    
    def test_account_url(self):
        """Test account URL pattern"""
        url = reverse('marketing:account')
        self.assertEqual(url, '/accounts/')
        
        resolved = resolve('/accounts/')
        self.assertEqual(resolved.view_name, 'marketing:account')
    
    def test_password_reset_url(self):
        """Test password reset URL pattern"""
        url = reverse('marketing:password_reset')
        self.assertEqual(url, '/accounts/password-reset/')
        
        resolved = resolve('/accounts/password-reset/')
        self.assertEqual(resolved.view_name, 'marketing:password_reset')
    
    def test_password_reset_confirm_url(self):
        """Test password reset confirm URL pattern"""
        url = reverse('marketing:password_reset_confirm', kwargs={'uidb64': 'test', 'token': 'test-token'})
        self.assertEqual(url, '/accounts/reset/test/test-token/')
        
        resolved = resolve('/accounts/reset/test/test-token/')
        self.assertEqual(resolved.view_name, 'marketing:password_reset_confirm')
        self.assertEqual(resolved.kwargs['uidb64'], 'test')
        self.assertEqual(resolved.kwargs['token'], 'test-token')
    
    def test_sitemap_url(self):
        """Test sitemap URL pattern"""
        url = reverse('marketing:sitemap')
        self.assertEqual(url, '/sitemap.xml')
        
        resolved = resolve('/sitemap.xml')
        self.assertEqual(resolved.view_name, 'marketing:sitemap')
    
    def test_robots_url(self):
        """Test robots.txt URL pattern"""
        url = reverse('marketing:robots')
        self.assertEqual(url, '/robots.txt')
        
        resolved = resolve('/robots.txt')
        self.assertEqual(resolved.view_name, 'marketing:robots')
    
    def test_api_media_list_url(self):
        """Test API media list URL pattern"""
        url = reverse('marketing:api_media_list')
        self.assertEqual(url, '/marketing/api/media/')
        
        resolved = resolve('/marketing/api/media/')
        self.assertEqual(resolved.view_name, 'marketing:api_media_list')
    
    def test_api_categories_url(self):
        """Test API categories URL pattern"""
        url = reverse('marketing:api_categories')
        self.assertEqual(url, '/marketing/api/categories/')
        
        resolved = resolve('/marketing/api/categories/')
        self.assertEqual(resolved.view_name, 'marketing:api_categories')
    
    def test_api_tags_url(self):
        """Test API tags URL pattern"""
        url = reverse('marketing:api_tags')
        self.assertEqual(url, '/marketing/api/tags/')
        
        resolved = resolve('/marketing/api/tags/')
        self.assertEqual(resolved.view_name, 'marketing:api_tags')
    
    def test_url_reversal_errors(self):
        """Test that invalid URL reversals raise appropriate errors"""
        # Test missing required parameters
        with self.assertRaises(NoReverseMatch):
            reverse('marketing:page_detail')
        
        with self.assertRaises(NoReverseMatch):
            reverse('marketing:blog_detail')
        
        with self.assertRaises(NoReverseMatch):
            reverse('marketing:page_edit')
        
        with self.assertRaises(NoReverseMatch):
            reverse('marketing:post_edit')
    
    def test_url_parameter_validation(self):
        """Test URL parameter validation"""
        # Test valid slugs
        valid_slugs = ['test-page', 'test-post', 'test-category', 'test-tag']
        
        for slug in valid_slugs:
            url = reverse('marketing:page_detail', kwargs={'slug': slug})
            self.assertIn(slug, url)
            
            resolved = resolve(f'/pages/{slug}/')
            self.assertEqual(resolved.kwargs['slug'], slug)
    
    def test_url_case_sensitivity(self):
        """Test URL case sensitivity"""
        # URLs should be case-sensitive
        with self.assertRaises(NoReverseMatch):
            reverse('marketing:PAGE_DETAIL', kwargs={'slug': 'test-page'})
    
    def test_url_uniqueness(self):
        """Test that URL patterns don't conflict"""
        # Test that different views have different URLs
        urls = [
            reverse('marketing:home'),
            reverse('marketing:contact'),
            reverse('marketing:demo_page'),
            reverse('marketing:cms_dashboard'),
        ]
        
        # All URLs should be unique
        self.assertEqual(len(urls), len(set(urls)))
    
    def test_url_redirects(self):
        """Test URL redirects and legacy URL handling"""
        # Test that old URLs redirect properly (if applicable)
        # This would depend on your URL migration strategy
        
        # Test trailing slash handling
        response = self.client.get('/cms')
        self.assertEqual(response.status_code, 301)  # Should redirect to /cms/
        
        response = self.client.get('/cms/', follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_url_security(self):
        """Test URL security measures"""
        # Test that URLs don't expose sensitive information
        response = self.client.get('/cms/pages/../../../etc/passwd')
        self.assertEqual(response.status_code, 404)
        
        # Test that URLs are properly encoded
        response = self.client.get('/pages/test%20page/')  # URL-encoded space
        self.assertEqual(response.status_code, 404)  # Should not resolve to valid page
    
    def test_url_performance(self):
        """Test URL resolution performance"""
        import time
        
        # Test URL resolution speed
        start_time = time.time()
        
        for i in range(100):
            reverse('marketing:page_detail', kwargs={'slug': f'test-page-{i}'})
        
        end_time = time.time()
        resolution_time = end_time - start_time
        
        # URL resolution should be fast
        self.assertLess(resolution_time, 1.0, f"URL resolution took {resolution_time:.3f}s for 100 iterations")
    
    def test_url_documentation(self):
        """Test that URL patterns are properly documented"""
        # This test ensures that URL patterns follow consistent naming
        from django.urls import get_resolver
        
        resolver = get_resolver()
        url_patterns = resolver.url_patterns
        
        # Check that all URL patterns have names
        for pattern in url_patterns:
            if hasattr(pattern, 'url_patterns'):
                # Skip include patterns
                continue
            
            if hasattr(pattern, 'name') and pattern.name:
                # URL name should follow convention: app:view_name
                self.assertIn(':', pattern.name)
                app_name, view_name = pattern.name.split(':', 1)
                self.assertTrue(app_name)
                self.assertTrue(view_name)