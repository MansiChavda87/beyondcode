"""
TDD Test Suite for Django CMS Models
Tests all model functionality with strict TDD approach
"""

import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from unittest.mock import patch, MagicMock

from marketing.models import (
    Page, Post, Category, Tag, MediaAsset, NavMenu, NavItem, Footer
)

User = get_user_model()


class TestMediaAssetModel(TestCase):
    """Test MediaAsset model - addresses uploaded_at field issue"""
    
    def test_media_asset_creation(self):
        """RED: Write failing test for MediaAsset creation"""
        # This test should fail initially because uploaded_at field doesn't exist
        media = MediaAsset.objects.create(
            file="https://example.com/image.jpg",
            alt_text="Test image",
            content_type="image/jpeg"
        )
        
        # This should fail because uploaded_at field doesn't exist
        self.assertIsNotNone(media.created_at)
        self.assertIsNotNone(media.id)
    
    def test_media_asset_display_url(self):
        """Test display_url property"""
        media = MediaAsset.objects.create(
            file="https://example.com/image.jpg",
            alt_text="Test image"
        )
        
        self.assertEqual(media.display_url, "https://example.com/image.jpg")
    
    def test_media_asset_is_image(self):
        """Test is_image property"""
        # Test with file_upload
        media = MediaAsset.objects.create(
            alt_text="Test image"
        )
        
        # Mock file_upload for testing
        media.file_upload = MagicMock()
        media.file_upload.name = "test.jpg"
        
        self.assertTrue(media.is_image)
    
    def test_media_asset_str_representation(self):
        """Test string representation"""
        media = MediaAsset.objects.create(
            file="https://example.com/image.jpg",
            alt_text="Test image"
        )
        
        self.assertEqual(str(media), "Test image")


class TestPageModel(TestCase):
    """Test Page model functionality"""
    
    def test_page_creation(self):
        """Test basic page creation"""
        page = Page.objects.create(
            title="Test Page",
            slug="test-page",
            status="published"
        )
        
        self.assertEqual(page.title, "Test Page")
        self.assertEqual(page.slug, "test-page")
        self.assertEqual(page.status, "published")
        self.assertIsNotNone(page.created_at)
        self.assertIsNotNone(page.updated_at)
    
    def test_page_slug_uniqueness(self):
        """Test slug uniqueness constraint"""
        Page.objects.create(
            title="Page 1",
            slug="test-slug",
            status="published"
        )
        
        with self.assertRaises(Exception):  # Should raise IntegrityError
            Page.objects.create(
                title="Page 2",
                slug="test-slug",  # Duplicate slug
                status="published"
            )
    
    def test_page_absolute_url(self):
        """Test absolute URL generation"""
        page = Page.objects.create(
            title="Test Page",
            slug="test-page",
            status="published"
        )
        
        expected_url = f"/pages/test-page/"
        self.assertEqual(page.get_absolute_url(), expected_url)
    
    def test_page_is_published_property(self):
        """Test is_published property"""
        # Published page
        published_page = Page.objects.create(
            title="Published Page",
            slug="published-page",
            status="published"
        )
        self.assertTrue(published_page.is_published)
        
        # Draft page
        draft_page = Page.objects.create(
            title="Draft Page",
            slug="draft-page",
            status="draft"
        )
        self.assertFalse(draft_page.is_published)
        
        # Scheduled page (future publish date)
        future_page = Page.objects.create(
            title="Future Page",
            slug="future-page",
            status="scheduled",
            publish_at=timezone.now() + timezone.timedelta(days=1)
        )
        self.assertFalse(future_page.is_published)
    
    def test_page_primary_image_url(self):
        """Test primary_image_url property"""
        page = Page.objects.create(
            title="Test Page",
            slug="test-page",
            primary_image="https://example.com/image.jpg"
        )
        
        self.assertEqual(page.primary_image_url, "https://example.com/image.jpg")


class TestPostModel(TestCase):
    """Test Post model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
    
    def test_post_creation(self):
        """Test basic post creation"""
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            status="published",
            author=self.user,
            author_name="Test Author",
            excerpt="Test excerpt"
        )
        
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.slug, "test-post")
        self.assertEqual(post.status, "published")
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.author_name, "Test Author")
        self.assertEqual(post.excerpt, "Test excerpt")
    
    def test_post_categories_and_tags(self):
        """Test post relationships with categories and tags"""
        category = Category.objects.create(
            name="Test Category",
            slug="test-category"
        )
        
        tag = Tag.objects.create(
            name="Test Tag",
            slug="test-tag"
        )
        
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            status="published"
        )
        
        post.categories.add(category)
        post.tags.add(tag)
        
        self.assertIn(category, post.categories.all())
        self.assertIn(tag, post.tags.all())
    
    def test_post_absolute_url(self):
        """Test post absolute URL"""
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            status="published"
        )
        
        expected_url = f"/blog/test-post/"
        self.assertEqual(post.get_absolute_url(), expected_url)
    
    def test_post_is_published_property(self):
        """Test post is_published property"""
        # Published post
        published_post = Post.objects.create(
            title="Published Post",
            slug="published-post",
            status="published"
        )
        self.assertTrue(published_post.is_published)
        
        # Draft post
        draft_post = Post.objects.create(
            title="Draft Post",
            slug="draft-post",
            status="draft"
        )
        self.assertFalse(draft_post.is_published)
    
    def test_post_computed_excerpt(self):
        """Test computed excerpt functionality"""
        # Test with explicit excerpt
        post_with_excerpt = Post.objects.create(
            title="Test Post",
            slug="test-post",
            status="published",
            excerpt="Explicit excerpt"
        )
        self.assertEqual(post_with_excerpt.computed_excerpt, "Explicit excerpt")
        
        # Test with HTML content
        post_with_html = Post.objects.create(
            title="Test Post",
            slug="test-post",
            status="published",
            blocks_html="<p>This is a test paragraph with some content.</p>"
        )
        self.assertIn("This is a test paragraph", post_with_html.computed_excerpt)
    
    def test_post_featured_image(self):
        """Test featured image URL"""
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            cover_image="https://example.com/cover.jpg"
        )
        
        self.assertEqual(post.featured_image, "https://example.com/cover.jpg")


class TestCategoryModel(TestCase):
    """Test Category model"""
    
    def test_category_creation(self):
        """Test category creation"""
        category = Category.objects.create(
            name="Test Category",
            slug="test-category"
        )
        
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.slug, "test-category")
    
    def test_category_slug_uniqueness(self):
        """Test category slug uniqueness"""
        Category.objects.create(
            name="Category 1",
            slug="test-category"
        )
        
        with self.assertRaises(Exception):  # Should raise IntegrityError
            Category.objects.create(
                name="Category 2",
                slug="test-category"  # Duplicate slug
            )


class TestTagModel(TestCase):
    """Test Tag model"""
    
    def test_tag_creation(self):
        """Test tag creation"""
        tag = Tag.objects.create(
            name="Test Tag",
            slug="test-tag"
        )
        
        self.assertEqual(tag.name, "Test Tag")
        self.assertEqual(tag.slug, "test-tag")
    
    def test_tag_slug_uniqueness(self):
        """Test tag slug uniqueness"""
        Tag.objects.create(
            name="Tag 1",
            slug="test-tag"
        )
        
        with self.assertRaises(Exception):  # Should raise IntegrityError
            Tag.objects.create(
                name="Tag 2",
                slug="test-tag"  # Duplicate slug
            )


class TestNavMenuModel(TestCase):
    """Test Navigation models"""
    
    def test_nav_menu_creation(self):
        """Test navigation menu creation"""
        nav_menu = NavMenu.objects.create(
            name="Primary Navigation"
        )
        
        self.assertEqual(nav_menu.name, "Primary Navigation")
    
    def test_nav_item_creation(self):
        """Test navigation item creation"""
        nav_menu = NavMenu.objects.create(name="Primary Navigation")
        
        nav_item = NavItem.objects.create(
            menu=nav_menu,
            label="Home",
            url="/",
            order=1
        )
        
        self.assertEqual(nav_item.label, "Home")
        self.assertEqual(nav_item.url, "/")
        self.assertEqual(nav_item.order, 1)
        self.assertEqual(nav_item.menu, nav_menu)


class TestFooterModel(TestCase):
    """Test Footer model"""
    
    def test_footer_creation(self):
        """Test footer creation"""
        footer = Footer.objects.create(
            label="Default Footer",
            cta_title="Call to Action",
            cta_body="This is the call to action text.",
            cta_button_label="Click Me",
            cta_button_url="/contact/",
            legal_text="© 2024 Company. All rights reserved."
        )
        
        self.assertEqual(footer.label, "Default Footer")
        self.assertEqual(footer.cta_title, "Call to Action")
        self.assertEqual(footer.cta_body, "This is the call to action text.")
        self.assertEqual(footer.cta_button_label, "Click Me")
        self.assertEqual(footer.cta_button_url, "/contact/")
        self.assertEqual(footer.legal_text, "© 2024 Company. All rights reserved.")


class TestSeoFieldsMixin(TestCase):
    """Test SEO fields mixin functionality"""
    
    def test_page_seo_fields(self):
        """Test SEO fields on Page model"""
        page = Page.objects.create(
            title="Test Page",
            slug="test-page",
            status="published",
            seo_title="SEO Title",
            seo_description="SEO Description",
            og_title="OG Title",
            og_description="OG Description",
            og_image="https://example.com/og-image.jpg",
            twitter_image="https://example.com/twitter-image.jpg"
        )
        
        self.assertEqual(page.seo_title, "SEO Title")
        self.assertEqual(page.seo_description, "SEO Description")
        self.assertEqual(page.og_title, "OG Title")
        self.assertEqual(page.og_description, "OG Description")
        self.assertEqual(page.og_image, "https://example.com/og-image.jpg")
        self.assertEqual(page.twitter_image, "https://example.com/twitter-image.jpg")
    
    def test_post_seo_fields(self):
        """Test SEO fields on Post model"""
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            status="published",
            seo_title="Post SEO Title",
            seo_description="Post SEO Description",
            og_title="Post OG Title",
            og_description="Post OG Description",
            og_image="https://example.com/post-og-image.jpg",
            twitter_image="https://example.com/post-twitter-image.jpg"
        )
        
        self.assertEqual(post.seo_title, "Post SEO Title")
        self.assertEqual(post.seo_description, "Post SEO Description")
        self.assertEqual(post.og_title, "Post OG Title")
        self.assertEqual(post.og_description, "Post OG Description")
        self.assertEqual(post.og_image, "https://example.com/post-og-image.jpg")
        self.assertEqual(post.twitter_image, "https://example.com/post-twitter-image.jpg")