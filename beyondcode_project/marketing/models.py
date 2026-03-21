import re
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

from .renderers import render_lexical_json, render_editorjs, sanitize_html


class PublishedStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    SCHEDULED = 'scheduled', 'Scheduled'


class SeoFieldsMixin(models.Model):
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(blank=True)
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.URLField(max_length=500, blank=True)
    twitter_image = models.URLField(max_length=500, blank=True)

    class Meta:
        abstract = True


class MediaAsset(models.Model):
    file = models.URLField(max_length=500, blank=True)
    file_upload = models.FileField(upload_to='media_assets/', blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    content_type = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.alt_text or self.file or f"Media Asset {self.id}"

    @property
    def display_url(self):
        """Return the actual file URL for display"""
        if self.file_upload:
            return self.file_upload.url
        return self.file

    @property
    def is_image(self):
        """Check if this asset is an image"""
        if self.file_upload:
            return self.file_upload.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'))
        return self.content_type.startswith('image/') if self.content_type else False


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Page(SeoFieldsMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    status = models.CharField(
        max_length=20,
        choices=PublishedStatus.choices,
        default=PublishedStatus.DRAFT,
    )
    publish_at = models.DateTimeField(blank=True, null=True)
    unpublish_at = models.DateTimeField(blank=True, null=True)
    body_json = models.JSONField(blank=True, null=True)
    body_html = models.TextField(blank=True)
    blocks_json = models.JSONField(blank=True, null=True)
    blocks_html = models.TextField(blank=True)
    primary_image = models.URLField(max_length=500, blank=True)
    primary_image_upload = models.FileField(upload_to='pages/primary_images/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('marketing:page_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Handle GrapesJS data format
        if self.blocks_json:
            # If blocks_json contains GrapesJS data structure
            if isinstance(self.blocks_json, dict) and ('html' in self.blocks_json or 'components' in self.blocks_json):
                # Extract HTML from GrapesJS format
                if 'html' in self.blocks_json:
                    self.blocks_html = sanitize_html(self.blocks_json['html'])
                elif 'components' in self.blocks_json:
                    # Convert components to HTML if needed
                    self.blocks_html = sanitize_html(str(self.blocks_json['components']))
            else:
                # Legacy format or other format - use blocks_json directly as HTML
                self.blocks_html = sanitize_html(str(self.blocks_json))
        else:
            self.blocks_html = ''
        
        # Keep body_json/body_html for backward compatibility but don't process them
        if self.body_json:
            rendered = render_editorjs(self.body_json)
            self.body_html = sanitize_html(rendered)
        else:
            self.body_html = ''
            
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        now = timezone.now()
        if self.status == PublishedStatus.DRAFT:
            return False
        if self.status == PublishedStatus.PUBLISHED:
            if self.unpublish_at and self.unpublish_at <= now:
                return False
            return True
        if self.status == PublishedStatus.SCHEDULED:
            return bool(self.publish_at and self.publish_at <= now)
        return False

    @property
    def primary_image_url(self):
        """Return the primary image URL (primary_image_upload takes precedence over primary_image)"""
        if self.primary_image_upload:
            return self.primary_image_upload.url
        return self.primary_image


class Post(SeoFieldsMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    status = models.CharField(
        max_length=20,
        choices=PublishedStatus.choices,
        default=PublishedStatus.DRAFT,
    )
    publish_at = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='posts')
    author_name = models.CharField(max_length=255, blank=True)
    excerpt = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    body_json = models.JSONField(blank=True, null=True)
    body_html = models.TextField(blank=True)
    blocks_json = models.JSONField(blank=True, null=True, help_text="Block-based content in JSON format")
    blocks_html = models.TextField(blank=True)
    cover_image = models.URLField(max_length=500, blank=True)
    cover_image_upload = models.FileField(upload_to='posts/cover_images/', blank=True, null=True)
    primary_image = models.URLField(max_length=500, blank=True)
    primary_image_upload = models.FileField(upload_to='posts/primary_images/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-publish_at', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('marketing:blog_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Handle GrapesJS data format
        if self.blocks_json:
            # If blocks_json contains GrapesJS data structure
            if isinstance(self.blocks_json, dict) and ('html' in self.blocks_json or 'components' in self.blocks_json):
                # Extract HTML from GrapesJS format
                if 'html' in self.blocks_json:
                    self.blocks_html = sanitize_html(self.blocks_json['html'])
                elif 'components' in self.blocks_json:
                    # Convert components to HTML if needed
                    self.blocks_html = sanitize_html(str(self.blocks_json['components']))
            else:
                # Legacy format or other format - use blocks_json directly as HTML
                self.blocks_html = sanitize_html(str(self.blocks_json))
        else:
            self.blocks_html = ''
        
        # Keep body_json/body_html for backward compatibility but don't process them
        if self.body_json:
            rendered = render_editorjs(self.body_json)
            self.body_html = sanitize_html(rendered)
        else:
            self.body_html = ''
            
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        now = timezone.now()
        if self.status == PublishedStatus.DRAFT:
            return False
        if self.status == PublishedStatus.PUBLISHED:
            return True
        if self.status == PublishedStatus.SCHEDULED:
            return bool(self.publish_at and self.publish_at <= now)
        return False

    @property
    def computed_excerpt(self):
        """Return the explicit excerpt, or auto-generate from content."""
        if self.excerpt:
            return self.excerpt
        # Fall back to first paragraph from body_html or blocks_html
        html = self.body_html or self.blocks_html or ''
        match = re.search(r'<p[^>]*>(.*?)</p>', html, flags=re.I | re.S)
        if match:
            raw = re.sub(r'<[^>]+>', '', match.group(1)).strip()
            from django.utils.text import Truncator
            return Truncator(raw).chars(200)
        return ''

    @property
    def featured_image(self):
        """Return the featured image URL (cover_image_upload takes precedence over cover_image)"""
        if self.cover_image_upload:
            return self.cover_image_upload.url
        return self.cover_image

    @property
    def primary_image_url(self):
        """Return the primary image URL (primary_image_upload takes precedence over primary_image)"""
        if self.primary_image_upload:
            return self.primary_image_upload.url
        return self.primary_image


class NavMenu(models.Model):
    name = models.CharField(max_length=100, unique=True)
    items_json = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


class NavItem(models.Model):
    menu = models.ForeignKey(NavMenu, on_delete=models.CASCADE, related_name='items')
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=255, blank=True)
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, blank=True, null=True)
    external = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label


class Footer(models.Model):
    label = models.CharField(max_length=100, default='Default')
    columns_json = models.JSONField(blank=True, null=True)
    cta_title = models.CharField(max_length=255, blank=True)
    cta_body = models.TextField(blank=True)
    cta_button_label = models.CharField(max_length=100, blank=True)
    cta_button_url = models.CharField(max_length=255, blank=True)
    legal_text = models.TextField(blank=True)

    def __str__(self):
        return self.label