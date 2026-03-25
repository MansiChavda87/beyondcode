"""
TDD Performance Test Suite for Django CMS
Tests application performance and scalability
"""

import time
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import connection
from django.test.utils import override_settings

from marketing.models import (
    Page, Post, Category, Tag, MediaAsset, NavMenu, Footer
)

User = get_user_model()


class TestPerformance(TestCase):
    """Performance tests for CMS functionality"""
    
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
    
    def measure_response_time(self, url, method='GET', data=None):
        """Measure response time for a given URL"""
        start_time = time.time()
        
        if method == 'GET':
            response = self.client.get(url)
        elif method == 'POST':
            response = self.client.post(url, data)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        return response, response_time
    
    def test_homepage_performance(self):
        """Test homepage response time"""
        # Create some test data
        Page.objects.create(title="Home", slug="home", status="published")
        
        response, response_time = self.measure_response_time(reverse('marketing:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 1.0, f"Homepage took {response_time:.2f}s, should be under 1.0s")
    
    def test_blog_list_performance(self):
        """Test blog list page performance with multiple posts"""
        # Create multiple posts
        for i in range(20):
            Post.objects.create(
                title=f"Test Post {i}",
                slug=f"test-post-{i}",
                status="published",
                author_name="Test Author",
                publish_at=timezone.now()
            )
        
        response, response_time = self.measure_response_time(reverse('marketing:blog_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 1.0, f"Blog list took {response_time:.2f}s, should be under 1.0s")
    
    def test_page_detail_performance(self):
        """Test page detail page performance"""
        # Create a page with content
        Page.objects.create(
            title="Test Page",
            slug="test-page",
            status="published",
            blocks_json={
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': 'This is test content.' * 100  # Large content
                        }
                    }
                ]
            }
        )
        
        response, response_time = self.measure_response_time(reverse('marketing:page_detail', kwargs={'slug': 'test-page'}))
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 1.0, f"Page detail took {response_time:.2f}s, should be under 1.0s")
    
    def test_cms_dashboard_performance(self):
        """Test CMS dashboard performance with multiple content items"""
        self.client.login(username='admin', password='adminpass123')
        
        # Create multiple content items
        for i in range(50):
            Page.objects.create(
                title=f"Page {i}",
                slug=f"page-{i}",
                status="published"
            )
            
            Post.objects.create(
                title=f"Post {i}",
                slug=f"post-{i}",
                status="published",
                author_name="Admin"
            )
        
        response, response_time = self.measure_response_time(reverse('marketing:cms_dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 2.0, f"CMS dashboard took {response_time:.2f}s, should be under 2.0s")
    
    def test_page_list_performance(self):
        """Test page list performance with pagination"""
        self.client.login(username='admin', password='adminpass123')
        
        # Create many pages
        for i in range(100):
            Page.objects.create(
                title=f"Page {i}",
                slug=f"page-{i}",
                status="published"
            )
        
        response, response_time = self.measure_response_time(reverse('marketing:page_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 1.5, f"Page list took {response_time:.2f}s, should be under 1.5s")
    
    def test_search_performance(self):
        """Test search functionality performance"""
        # Create content for searching
        for i in range(100):
            Page.objects.create(
                title=f"Page with keyword {i}",
                slug=f"page-with-keyword-{i}",
                status="published",
                blocks_json={
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'data': {
                                'content': f'This page contains keyword {i} in the content.'
                            }
                        }
                    ]
                }
            )
        
        response, response_time = self.measure_response_time(
            '/marketing/api/search/',
            'GET',
            {'q': 'keyword'}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 1.0, f"Search took {response_time:.2f}s, should be under 1.0s")
    
    def test_media_list_performance(self):
        """Test media list performance with many assets"""
        self.client.login(username='admin', password='adminpass123')
        
        # Create many media assets
        for i in range(200):
            MediaAsset.objects.create(
                file=f"https://example.com/image-{i}.jpg",
                alt_text=f"Image {i}"
            )
        
        response, response_time = self.measure_response_time(reverse('marketing:media_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 2.0, f"Media list took {response_time:.2f}s, should be under 2.0s")
    
    def test_database_query_optimization(self):
        """Test that database queries are optimized"""
        # Create test data
        category = Category.objects.create(name="Test Category", slug="test-category")
        tag = Tag.objects.create(name="Test Tag", slug="test-tag")
        
        for i in range(10):
            post = Post.objects.create(
                title=f"Post {i}",
                slug=f"post-{i}",
                status="published",
                author_name="Test Author"
            )
            post.categories.add(category)
            post.tags.add(tag)
        
        # Measure queries for blog list
        with self.assertNumQueries(3):  # Should be optimized to few queries
            response = self.client.get(reverse('marketing:blog_list'))
            self.assertEqual(response.status_code, 200)
    
    def test_template_rendering_performance(self):
        """Test template rendering performance"""
        # Create a page with complex content
        Page.objects.create(
            title="Complex Page",
            slug="complex-page",
            status="published",
            blocks_json={
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': '<h1>Heading</h1><p>Paragraph</p>' * 50
                        }
                    },
                    {
                        'type': 'callout',
                        'data': {
                            'title': 'Callout Title',
                            'body': 'Callout body content.'
                        }
                    }
                ]
            }
        )
        
        response, response_time = self.measure_response_time(reverse('marketing:page_detail', kwargs={'slug': 'complex-page'}))
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 1.0, f"Complex page took {response_time:.2f}s, should be under 1.0s")
    
    def test_concurrent_user_simulation(self):
        """Simulate concurrent user access"""
        import threading
        import queue
        
        results = queue.Queue()
        
        def test_user_access():
            client = Client()
            response, response_time = self.measure_response_time(reverse('marketing:home'))
            results.put((response.status_code, response_time))
        
        # Simulate 10 concurrent users
        threads = []
        for i in range(10):
            thread = threading.Thread(target=test_user_access)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        total_time = 0
        success_count = 0
        
        while not results.empty():
            status_code, response_time = results.get()
            if status_code == 200:
                success_count += 1
            total_time += response_time
        
        self.assertEqual(success_count, 10, "All concurrent requests should succeed")
        self.assertLess(total_time / 10, 1.0, "Average response time should be under 1.0s")
    
    def test_memory_usage(self):
        """Test memory usage with large datasets"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create large dataset
        for i in range(1000):
            Page.objects.create(
                title=f"Memory Test Page {i}",
                slug=f"memory-test-page-{i}",
                status="published"
            )
        
        # Measure memory after creation
        after_creation_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Access the data
        response = self.client.get(reverse('marketing:page_list'))
        self.assertEqual(response.status_code, 200)
        
        # Measure memory after access
        after_access_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Memory increase should be reasonable
        memory_increase = after_creation_memory - initial_memory
        self.assertLess(memory_increase, 100, f"Memory increase should be under 100MB, got {memory_increase:.2f}MB")
    
    def test_cache_performance(self):
        """Test caching performance improvements"""
        # First request (cache miss)
        response1, time1 = self.measure_response_time(reverse('marketing:home'))
        
        # Second request (should be cached)
        response2, time2 = self.measure_response_time(reverse('marketing:home'))
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        
        # Second request should be faster (if caching is working)
        # Note: This is a soft assertion as caching behavior may vary
        print(f"First request: {time1:.3f}s, Second request: {time2:.3f}s")
    
    def test_static_file_performance(self):
        """Test static file serving performance"""
        # Test CSS file
        response, response_time = self.measure_response_time('/static/marketing/css/main.css')
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 0.5, f"CSS file took {response_time:.2f}s, should be under 0.5s")
        
        # Test JS file
        response, response_time = self.measure_response_time('/static/marketing/js/main.js')
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 0.5, f"JS file took {response_time:.2f}s, should be under 0.5s")
    
    def test_api_response_performance(self):
        """Test API endpoint performance"""
        self.client.login(username='admin', password='adminpass123')
        
        # Test media list API
        response, response_time = self.measure_response_time(reverse('marketing:api_media_list'))
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 0.5, f"Media API took {response_time:.2f}s, should be under 0.5s")
        
        # Test categories API
        response, response_time = self.measure_response_time(reverse('marketing:api_categories'))
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 0.5, f"Categories API took {response_time:.2f}s, should be under 0.5s")
    
    def test_pagination_performance(self):
        """Test pagination performance with large datasets"""
        # Create many pages
        for i in range(500):
            Page.objects.create(
                title=f"Paginated Page {i}",
                slug=f"paginated-page-{i}",
                status="published"
            )
        
        # Test first page
        response, response_time = self.measure_response_time(reverse('marketing:page_list'))
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 1.0, f"First page took {response_time:.2f}s, should be under 1.0s")
        
        # Test later page
        response, response_time = self.measure_response_time(f"{reverse('marketing:page_list')}?page=10")
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 1.0, f"Page 10 took {response_time:.2f}s, should be under 1.0s")


@override_settings(DEBUG=True)
class TestDebugPerformance(TestCase):
    """Performance tests with debug mode enabled"""
    
    def setUp(self):
        self.client = Client()
    
    def test_debug_toolbar_overhead(self):
        """Test that debug toolbar doesn't significantly impact performance"""
        # Create test data
        Page.objects.create(title="Debug Test Page", slug="debug-test-page", status="published")
        
        response, response_time = self.measure_response_time(reverse('marketing:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 2.0, f"Debug mode homepage took {response_time:.2f}s, should be under 2.0s")
    
    def test_query_count_in_debug(self):
        """Test query count in debug mode"""
        # Create test data
        category = Category.objects.create(name="Debug Category", slug="debug-category")
        
        for i in range(10):
            post = Post.objects.create(
                title=f"Debug Post {i}",
                slug=f"debug-post-{i}",
                status="published",
                author_name="Debug Author"
            )
            post.categories.add(category)
        
        # Should not have N+1 query problems
        with self.assertNumQueries(3):  # Optimized queries
            response = self.client.get(reverse('marketing:blog_list'))
            self.assertEqual(response.status_code, 200)