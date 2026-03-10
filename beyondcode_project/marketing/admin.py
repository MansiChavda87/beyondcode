from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Page, Post, Category, Tag, NavMenu, NavItem, Footer, MediaAsset
from .forms import PageForm, PostForm, NavMenuForm, FooterForm, MediaAssetForm


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ['file', 'alt_text', 'caption', 'content_type', 'created_at']
    list_filter = ['content_type', 'created_at']
    search_fields = ['alt_text', 'caption', 'file']


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
    list_display = ['title', 'slug', 'status', 'publish_at', 'is_published', 'created_at']
    list_filter = ['status', 'publish_at', 'created_at']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'status', 'publish_at', 'unpublish_at')
        }),
        ('Content', {
            'fields': ('body_json', 'body_html', 'blocks_json', 'blocks_html', 'primary_image'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'og_title', 'og_description', 'og_image', 'twitter_image'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def is_published(self, obj):
        return obj.is_published
    is_published.boolean = True
    is_published.short_description = 'Published?'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ['title', 'slug', 'status', 'publish_at', 'author_name', 'is_published', 'created_at']
    list_filter = ['status', 'publish_at', 'created_at', 'categories', 'tags']
    search_fields = ['title', 'slug', 'author_name']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'computed_excerpt']
    filter_horizontal = ['categories', 'tags']
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'status', 'publish_at', 'author_name', 'excerpt')
        }),
        ('Content', {
            'fields': ('body_json', 'body_html', 'blocks_json', 'blocks_html', 'cover_image', 'primary_image'),
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
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'computed_excerpt'),
            'classes': ('collapse',)
        })
    )

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