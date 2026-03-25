"""
TDD Test Fixtures for Django CMS
Provides reusable test data and fixtures for consistent testing
"""

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from marketing.models import (
    Page, Post, Category, Tag, MediaAsset, NavMenu, Footer
)

User = get_user_model()


@pytest.fixture
def test_user():
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def admin_user():
    """Create an admin user"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )


@pytest.fixture
def test_category():
    """Create a test category"""
    return Category.objects.create(
        name="Test Category",
        slug="test-category",
        description="A test category for testing purposes"
    )


@pytest.fixture
def test_tag():
    """Create a test tag"""
    return Tag.objects.create(
        name="Test Tag",
        slug="test-tag"
    )


@pytest.fixture
def test_page(test_user):
    """Create a test page"""
    return Page.objects.create(
        title="Test Page",
        slug="test-page",
        status="published",
        seo_title="Test Page SEO Title",
        seo_description="Test page SEO description",
        blocks_json={
            'blocks': [
                {
                    'type': 'rich_text',
                    'data': {
                        'content': 'This is test page content.'
                    }
                }
            ]
        }
    )


@pytest.fixture
def test_draft_page(test_user):
    """Create a draft test page"""
    return Page.objects.create(
        title="Draft Test Page",
        slug="draft-test-page",
        status="draft",
        blocks_json={
            'blocks': [
                {
                    'type': 'rich_text',
                    'data': {
                        'content': 'This is draft page content.'
                    }
                }
            ]
        }
    )


@pytest.fixture
def test_post(test_user, test_category, test_tag):
    """Create a test post"""
    post = Post.objects.create(
        title="Test Post",
        slug="test-post",
        status="published",
        author=test_user,
        author_name="Test Author",
        excerpt="This is a test post excerpt.",
        publish_at=timezone.now(),
        blocks_json={
            'blocks': [
                {
                    'type': 'rich_text',
                    'data': {
                        'content': 'This is test post content.'
                    }
                }
            ]
        }
    )
    
    # Add relationships
    post.categories.add(test_category)
    post.tags.add(test_tag)
    
    return post


@pytest.fixture
def test_draft_post(test_user, test_category, test_tag):
    """Create a draft test post"""
    post = Post.objects.create(
        title="Draft Test Post",
        slug="draft-test-post",
        status="draft",
        author=test_user,
        author_name="Test Author",
        excerpt="This is a draft post excerpt.",
        blocks_json={
            'blocks': [
                {
                    'type': 'rich_text',
                    'data': {
                        'content': 'This is draft post content.'
                    }
                }
            ]
        }
    )
    
    # Add relationships
    post.categories.add(test_category)
    post.tags.add(test_tag)
    
    return post


@pytest.fixture
def test_media_asset():
    """Create a test media asset"""
    return MediaAsset.objects.create(
        file="https://example.com/test-image.jpg",
        alt_text="Test Image",
        caption="This is a test image",
        content_type="image/jpeg",
        width=800,
        height=600
    )


@pytest.fixture
def test_navigation():
    """Create a test navigation menu"""
    nav_menu = NavMenu.objects.create(
        name="Primary Navigation"
    )
    
    # Add some navigation items
    NavItem.objects.create(
        menu=nav_menu,
        label="Home",
        url="/",
        order=1
    )
    
    NavItem.objects.create(
        menu=nav_menu,
        label="Blog",
        url="/blog/",
        order=2
    )
    
    NavItem.objects.create(
        menu=nav_menu,
        label="Contact",
        url="/contact/",
        order=3
    )
    
    return nav_menu


@pytest.fixture
def test_footer():
    """Create a test footer"""
    return Footer.objects.create(
        label="Default Footer",
        cta_title="Join Our Newsletter",
        cta_body="Subscribe to get the latest updates and news.",
        cta_button_label="Subscribe",
        cta_button_url="/newsletter/",
        legal_text="© 2024 BeyondCode AI. All rights reserved."
    )


@pytest.fixture
def multiple_pages():
    """Create multiple test pages"""
    pages = []
    
    for i in range(5):
        page = Page.objects.create(
            title=f"Test Page {i+1}",
            slug=f"test-page-{i+1}",
            status="published",
            blocks_json={
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': f'This is test page {i+1} content.'
                        }
                    }
                ]
            }
        )
        pages.append(page)
    
    return pages


@pytest.fixture
def multiple_posts(test_user, test_category, test_tag):
    """Create multiple test posts"""
    posts = []
    
    for i in range(5):
        post = Post.objects.create(
            title=f"Test Post {i+1}",
            slug=f"test-post-{i+1}",
            status="published",
            author=test_user,
            author_name="Test Author",
            excerpt=f"This is test post {i+1} excerpt.",
            publish_at=timezone.now(),
            blocks_json={
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': f'This is test post {i+1} content.'
                        }
                    }
                ]
            }
        )
        
        # Add relationships
        post.categories.add(test_category)
        post.tags.add(test_tag)
        
        posts.append(post)
    
    return posts


@pytest.fixture
def multiple_media_assets():
    """Create multiple test media assets"""
    media_assets = []
    
    for i in range(3):
        media = MediaAsset.objects.create(
            file=f"https://example.com/test-image-{i+1}.jpg",
            alt_text=f"Test Image {i+1}",
            caption=f"This is test image {i+1}",
            content_type="image/jpeg",
            width=800,
            height=600
        )
        media_assets.append(media)
    
    return media_assets


@pytest.fixture
def authenticated_client(client, test_user):
    """Create an authenticated client"""
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def admin_client(client, admin_user):
    """Create an admin client"""
    client.login(username='admin', password='adminpass123')
    return client


@pytest.fixture
def test_image_upload():
    """Create a test image upload file"""
    return SimpleUploadedFile(
        "test_image.jpg",
        b"fake image content",
        content_type="image/jpeg"
    )


@pytest.fixture
def test_pdf_upload():
    """Create a test PDF upload file"""
    return SimpleUploadedFile(
        "test_document.pdf",
        b"fake pdf content",
        content_type="application/pdf"
    )


@pytest.fixture
def complex_page_with_blocks():
    """Create a page with multiple block types"""
    return Page.objects.create(
        title="Complex Test Page",
        slug="complex-test-page",
        status="published",
        blocks_json={
            'blocks': [
                {
                    'type': 'rich_text',
                    'data': {
                        'content': 'This is rich text content.'
                    }
                },
                {
                    'type': 'callout',
                    'data': {
                        'title': 'Important Notice',
                        'body': 'This is an important callout message.'
                    }
                },
                {
                    'type': 'feature_grid',
                    'data': {
                        'title': 'Our Features',
                        'items': [
                            {'title': 'Feature 1', 'body': 'Description of feature 1'},
                            {'title': 'Feature 2', 'body': 'Description of feature 2'},
                            {'title': 'Feature 3', 'body': 'Description of feature 3'}
                        ]
                    }
                }
            ]
        }
    )


@pytest.fixture
def complex_post_with_blocks(test_user, test_category, test_tag):
    """Create a post with multiple block types"""
    post = Post.objects.create(
        title="Complex Test Post",
        slug="complex-test-post",
        status="published",
        author=test_user,
        author_name="Test Author",
        excerpt="This post contains multiple block types.",
        publish_at=timezone.now(),
        blocks_json={
            'blocks': [
                {
                    'type': 'rich_text',
                    'data': {
                        'content': 'This is the introduction.'
                    }
                },
                {
                    'type': 'image',
                    'data': {
                        'media_asset_id': 1,  # Will be updated in tests
                        'alt_text': 'Test Image'
                    }
                },
                {
                    'type': 'cta',
                    'data': {
                        'title': 'Call to Action',
                        'body': 'This is a call to action.',
                        'button_label': 'Click Here',
                        'button_url': '/contact/'
                    }
                }
            ]
        }
    )
    
    # Add relationships
    post.categories.add(test_category)
    post.tags.add(test_tag)
    
    return post


@pytest.fixture
def scheduled_page():
    """Create a scheduled page"""
    return Page.objects.create(
        title="Scheduled Test Page",
        slug="scheduled-test-page",
        status="scheduled",
        publish_at=timezone.now() + timezone.timedelta(days=1),
        blocks_json={
            'blocks': [
                {
                    'type': 'rich_text',
                    'data': {
                        'content': 'This page is scheduled for future publication.'
                    }
                }
            ]
        }
    )


@pytest.fixture
def expired_page():
    """Create an expired page"""
    return Page.objects.create(
        title="Expired Test Page",
        slug="expired-test-page",
        status="published",
        publish_at=timezone.now() - timezone.timedelta(days=2),
        unpublish_at=timezone.now() - timezone.timedelta(days=1),
        blocks_json={
            'blocks': [
                {
                    'type': 'rich_text',
                    'data': {
                        'content': 'This page has expired.'
                    }
                }
            ]
        }
    )


@pytest.fixture
def test_data_setup(test_user, admin_user, test_category, test_tag, test_page, test_post, test_media_asset, test_navigation, test_footer):
    """Complete test data setup"""
    return {
        'user': test_user,
        'admin': admin_user,
        'category': test_category,
        'tag': test_tag,
        'page': test_page,
        'post': test_post,
        'media': test_media_asset,
        'navigation': test_navigation,
        'footer': test_footer
    }


# Test data factories for more complex scenarios

class TestDataFactory:
    """Factory for creating test data"""
    
    @staticmethod
    def create_page(title, slug, status="published", **kwargs):
        """Create a page with given parameters"""
        defaults = {
            'title': title,
            'slug': slug,
            'status': status,
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': f'Content for {title}'
                        }
                    }
                ]
            }
        }
        defaults.update(kwargs)
        return Page.objects.create(**defaults)
    
    @staticmethod
    def create_post(title, slug, author=None, status="published", **kwargs):
        """Create a post with given parameters"""
        if author is None:
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
            'excerpt': f'Excerpt for {title}',
            'publish_at': timezone.now(),
            'blocks_json': {
                'blocks': [
                    {
                        'type': 'rich_text',
                        'data': {
                            'content': f'Content for {title}'
                        }
                    }
                ]
            }
        }
        defaults.update(kwargs)
        return Post.objects.create(**defaults)
    
    @staticmethod
    def create_category(name, slug=None, **kwargs):
        """Create a category with given parameters"""
        if slug is None:
            slug = name.lower().replace(' ', '-')
        
        defaults = {
            'name': name,
            'slug': slug,
            'description': f'Description for {name}'
        }
        defaults.update(kwargs)
        return Category.objects.create(**defaults)
    
    @staticmethod
    def create_tag(name, slug=None, **kwargs):
        """Create a tag with given parameters"""
        if slug is None:
            slug = name.lower().replace(' ', '-')
        
        defaults = {
            'name': name,
            'slug': slug
        }
        defaults.update(kwargs)
        return Tag.objects.create(**defaults)
    
    @staticmethod
    def create_media_asset(file_url, alt_text, **kwargs):
        """Create a media asset with given parameters"""
        defaults = {
            'file': file_url,
            'alt_text': alt_text,
            'caption': f'Caption for {alt_text}',
            'content_type': 'image/jpeg',
            'width': 800,
            'height': 600
        }
        defaults.update(kwargs)
        return MediaAsset.objects.create(**defaults)


@pytest.fixture
def data_factory():
    """Provide access to the test data factory"""
    return TestDataFactory