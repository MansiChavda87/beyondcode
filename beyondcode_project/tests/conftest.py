"""
Pytest configuration and fixtures for Django CMS TDD tests
"""

import pytest
import os
import django
from django.conf import settings
from django.test.utils import get_runner


# Configure Django settings
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
    django.setup()


@pytest.fixture(scope='session')
def django_db_setup():
    """Configure Django database for testing"""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }


@pytest.fixture(scope='function')
def db_transaction(django_db_setup, request):
    """Create database transaction for each test"""
    from django.test import TransactionTestCase
    test_case = TransactionTestCase()
    test_case._pre_setup()
    request.addfinalizer(test_case._post_teardown)


@pytest.fixture
def client():
    """Django test client fixture"""
    from django.test import Client
    return Client()


@pytest.fixture
def admin_client(client):
    """Django admin test client fixture"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )
    
    client.login(username='admin', password='adminpass123')
    return client


@pytest.fixture
def user_client(client):
    """Django user test client fixture"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    
    client.login(username='testuser', password='testpass123')
    return client


# Import test fixtures
from .test_fixtures import (
    test_user, admin_user, test_category, test_tag,
    test_page, test_draft_page, test_post, test_draft_post,
    test_media_asset, test_navigation, test_footer,
    multiple_pages, multiple_posts, multiple_media_assets,
    authenticated_client, admin_client as admin_client_fixture,
    test_image_upload, test_pdf_upload, complex_page_with_blocks,
    complex_post_with_blocks, scheduled_page, expired_page,
    test_data_setup, data_factory
)


# Pytest markers for test categorization
def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
    config.addinivalue_line(
        "markers", "security: marks tests as security tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", "tdd: marks tests as TDD tests"
    )


# Custom pytest hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names"""
    for item in items:
        # Add TDD marker to all tests
        item.add_marker(pytest.mark.tdd)
        
        # Add specific markers based on test file names
        if "performance" in item.nodeid:
            item.add_marker(pytest.mark.performance)
        elif "security" in item.nodeid:
            item.add_marker(pytest.mark.security)
        elif "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "e2e" in item.nodeid:
            item.add_marker(pytest.mark.e2e)
        
        # Mark slow tests
        if any(keyword in item.nodeid for keyword in ['performance', 'integration', 'e2e']):
            item.add_marker(pytest.mark.slow)


# Test data cleanup
@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Auto-cleanup test data after each test"""
    yield
    
    # Clean up any test data that might have been created
    from django.contrib.auth import get_user_model
    from marketing.models import Page, Post, Category, Tag, MediaAsset, NavMenu, Footer
    
    User = get_user_model()
    
    # Delete test users (but keep admin and regular users for other tests)
    test_users = User.objects.filter(username__startswith='testuser_')
    test_users.delete()
    
    # Delete test content
    test_pages = Page.objects.filter(title__startswith='Test ')
    test_pages.delete()
    
    test_posts = Post.objects.filter(title__startswith='Test ')
    test_posts.delete()
    
    test_categories = Category.objects.filter(name__startswith='Test ')
    test_categories.delete()
    
    test_tags = Tag.objects.filter(name__startswith='Test ')
    test_tags.delete()
    
    test_media = MediaAsset.objects.filter(alt_text__startswith='Test ')
    test_media.delete()


# Performance testing fixtures
@pytest.fixture
def performance_timer():
    """Timer fixture for performance testing"""
    import time
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
            return self
        
        def stop(self):
            self.end_time = time.time()
            return self
        
        def duration(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None
    
    return Timer()


# Mock fixtures for testing
@pytest.fixture
def mock_s3_client():
    """Mock S3 client for testing file uploads"""
    from unittest.mock import MagicMock
    
    mock_client = MagicMock()
    mock_client.upload_fileobj.return_value = None
    mock_client.generate_presigned_url.return_value = 'https://example.com/presigned-url'
    
    return mock_client


@pytest.fixture
def mock_email_backend():
    """Mock email backend for testing"""
    from unittest.mock import MagicMock
    
    mock_backend = MagicMock()
    mock_backend.send_mail.return_value = 1
    
    return mock_backend


# Database transaction fixtures
@pytest.fixture
def db_transaction_atomic():
    """Atomic database transaction for tests that need rollback"""
    from django.db import transaction
    
    with transaction.atomic():
        yield
        transaction.set_rollback(True)


# Test utilities
class TestUtils:
    """Utility class for common test operations"""
    
    @staticmethod
    def create_test_page(title, slug, status='published', **kwargs):
        """Create a test page with common defaults"""
        from marketing.models import Page
        
        defaults = {
            'title': title,
            'slug': slug,
            'status': status,
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': f'Test content for {title}'
                        }
                    }
                ]
            }
        }
        defaults.update(kwargs)
        return Page.objects.create(**defaults)
    
    @staticmethod
    def create_test_post(title, slug, author=None, status='published', **kwargs):
        """Create a test post with common defaults"""
        from marketing.models import Post
        from django.contrib.auth import get_user_model
        
        if author is None:
            User = get_user_model()
            author = User.objects.create_user(
                username=f'testuser_{slug}',
                email=f'test_{slug}@example.com',
                password='testpass123'
            )
        
        defaults = {
            'title': title,
            'slug': slug,
            'status': status,
            'author': author,
            'author_name': author.username,
            'excerpt': f'Test excerpt for {title}',
            'publish_at': timezone.now(),
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': f'Test content for {title}'
                        }
                    }
                ]
            }
        }
        defaults.update(kwargs)
        return Post.objects.create(**defaults)
    
    @staticmethod
    def create_test_user(username, email, password='testpass123', **kwargs):
        """Create a test user with common defaults"""
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        defaults = {
            'username': username,
            'email': email,
            'password': password,
        }
        defaults.update(kwargs)
        
        user = User.objects.create_user(**defaults)
        return user


@pytest.fixture
def test_utils():
    """Provide test utilities"""
    return TestUtils


# Test data builders
class TestDataBuilder:
    """Builder pattern for creating test data"""
    
    def __init__(self):
        self._data = {}
    
    def with_title(self, title):
        self._data['title'] = title
        return self
    
    def with_slug(self, slug):
        self._data['slug'] = slug
        return self
    
    def with_status(self, status):
        self._data['status'] = status
        return self
    
    def with_author(self, author):
        self._data['author'] = author
        return self
    
    def with_content(self, content):
        self._data['blocks_json'] = {
            'blocks': [
                {
                    'type': 'rich_text',
                    'data': {
                        'content': content
                    }
                }
            ]
        }
        return self
    
    def build_page(self):
        """Build a test page"""
        from marketing.models import Page
        return Page.objects.create(**self._data)
    
    def build_post(self):
        """Build a test post"""
        from marketing.models import Post
        return Post.objects.create(**self._data)


@pytest.fixture
def data_builder():
    """Provide data builder"""
    return TestDataBuilder()


# Test configuration
class TestConfig:
    """Test configuration settings"""
    
    # Performance thresholds (in seconds)
    PERFORMANCE_THRESHOLDS = {
        'homepage': 1.0,
        'blog_list': 1.0,
        'page_detail': 1.0,
        'cms_dashboard': 2.0,
        'api_response': 0.5,
    }
    
    # Security settings
    SECURITY_HEADERS = [
        'X-Content-Type-Options',
        'X-Frame-Options',
        'X-XSS-Protection',
        'Content-Security-Policy',
    ]
    
    # Test data limits
    TEST_DATA_LIMITS = {
        'max_pages': 100,
        'max_posts': 100,
        'max_media_assets': 50,
    }


@pytest.fixture
def test_config():
    """Provide test configuration"""
    return TestConfig