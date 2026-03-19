from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Page, Post, Category, Tag, NavMenu, NavItem, Footer, MediaAsset
from .forms import PageForm, PostForm, NavMenuForm, FooterForm, MediaAssetForm
from .widgets import EditorJSAdminWidget


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    form = MediaAssetForm
    list_display = ['preview_image', 'alt_text', 'caption', 'content_type', 'file_size', 'created_at']
    list_filter = ['content_type', 'created_at']
    search_fields = ['alt_text', 'caption', 'file']
    readonly_fields = ['preview_image', 'file_size', 'created_at']
    fieldsets = (
        (None, {
            'fields': ('file', 'file_upload', 'alt_text', 'caption')
        }),
        ('File Information', {
            'fields': ('width', 'height', 'content_type', 'file_size'),
            'classes': ('collapse',)
        }),
        ('Preview', {
            'fields': ('preview_image',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

    def preview_image(self, obj):
        """Display a preview image or file icon"""
        if obj.is_image and obj.display_url:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 150px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" alt="{}">',
                obj.display_url,
                obj.alt_text or "Preview"
            )
        elif obj.display_url:
            return format_html(
                '<div style="padding: 20px; border: 1px solid #ddd; border-radius: 4px; background: #f8f9fa; text-align: center;">'
                '<i class="fa fa-file" style="font-size: 48px; color: #6c757d;"></i>'
                '<br><br>'
                '<a href="{}" target="_blank" style="color: #007bff; text-decoration: none;">View File</a>'
                '</div>',
                obj.display_url
            )
        return "No file uploaded"
    preview_image.short_description = "Preview"

    def file_size(self, obj):
        """Display file size if available"""
        if obj.file_upload and hasattr(obj.file_upload, 'size'):
            size = obj.file_upload.size
            if size < 1024:
                return f"{size} bytes"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            else:
                return f"{size / (1024 * 1024):.1f} MB"
        return "N/A"
    file_size.short_description = "File Size"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageForm
    list_display = ['title', 'slug', 'status', 'publish_at', 'primary_image_preview', 'is_published', 'created_at']
    list_filter = ['status', 'publish_at', 'created_at']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'primary_image_preview']
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'status', 'publish_at', 'unpublish_at')
        }),
        ('Content', {
            'fields': ('body_json', 'body_html', 'blocks_json', 'blocks_html', 'primary_image', 'primary_image_upload'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'og_title', 'og_description', 'og_image', 'twitter_image'),
            'classes': ('collapse',)
        }),
        ('Image Preview', {
            'fields': ('primary_image_preview',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def primary_image_preview(self, obj):
        """Display a preview of the primary image"""
        if obj.primary_image_upload:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 150px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" alt="Primary Image">',
                obj.primary_image_upload.url
            )
        elif obj.primary_image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 150px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" alt="Primary Image">',
                obj.primary_image
            )
        return "No primary image"
    primary_image_preview.short_description = "Primary Image Preview"

    def is_published(self, obj):
        return obj.is_published
    is_published.boolean = True
    is_published.short_description = 'Published?'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ['title', 'slug', 'status', 'publish_at', 'author_name', 'cover_image_preview', 'primary_image_preview', 'is_published', 'created_at']
    list_filter = ['status', 'publish_at', 'created_at', 'categories', 'tags']
    search_fields = ['title', 'slug', 'author_name']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'computed_excerpt', 'cover_image_preview', 'primary_image_preview']
    filter_horizontal = ['categories', 'tags']
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'status', 'publish_at', 'author_name', 'excerpt')
        }),
        ('Content', {
            'fields': ('body_json', 'body_html', 'blocks_json', 'blocks_html', 'cover_image', 'cover_image_upload', 'primary_image', 'primary_image_upload'),
            'classes': ('collapse',)
        }),
        ('Categories & Tags', {
            'fields': ('categories', 'tags'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'og_title', 'og_description', 'og_image', 'twitter_image'),
            'classes': ('collapse',)
        }),
        ('Image Previews', {
            'fields': ('cover_image_preview', 'primary_image_preview'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'computed_excerpt'),
            'classes': ('collapse',)
        })
    )

    def cover_image_preview(self, obj):
        """Display a preview of the cover image"""
        if obj.cover_image_upload:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 150px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" alt="Cover Image">',
                obj.cover_image_upload.url
            )
        elif obj.cover_image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 150px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" alt="Cover Image">',
                obj.cover_image
            )
        return "No cover image"
    cover_image_preview.short_description = "Cover Image Preview"

    def primary_image_preview(self, obj):
        """Display a preview of the primary image"""
        if obj.primary_image_upload:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 150px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" alt="Primary Image">',
                obj.primary_image_upload.url
            )
        elif obj.primary_image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 150px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" alt="Primary Image">',
                obj.primary_image
            )
        return "No primary image"
    primary_image_preview.short_description = "Primary Image Preview"

    def is_published(self, obj):
        return obj.is_published
    is_published.boolean = True
    is_published.short_description = 'Published?'


@admin.register(NavMenu)
class NavMenuAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(NavItem)
class NavItemAdmin(admin.ModelAdmin):
    list_display = ['menu', 'label', 'url', 'page', 'external', 'parent', 'order']
    list_filter = ['menu', 'external', 'parent']
    search_fields = ['label', 'url']
    list_editable = ['order']


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ['label', 'cta_title', 'cta_button_label']
    search_fields = ['label', 'cta_title']