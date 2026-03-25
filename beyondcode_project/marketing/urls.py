from django.urls import path
from django.shortcuts import render
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse

from . import views

app_name = 'marketing'

urlpatterns = [
    # Authentication views
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('account/', views.account_view, name='account'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    
    # SEO views
    path('sitemap.xml', views.sitemap_view, name='sitemap'),
    path('robots.txt', views.robots_view, name='robots'),
    
    # Public views
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('demo/', views.demo_page, name='demo_page'),
    # Common page shortcuts that redirect to the dynamic page system
    path('about/', views.page_detail, {'slug': 'about'}, name='about'),
    path('pricing/', views.page_detail, {'slug': 'pricing'}, name='pricing'),
    path('services/', views.page_detail, {'slug': 'services'}, name='services'),
    path('team/', views.page_detail, {'slug': 'team'}, name='team'),
    path('careers/', views.page_detail, {'slug': 'careers'}, name='careers'),
    path('privacy/', views.page_detail, {'slug': 'privacy'}, name='privacy'),
    path('terms/', views.page_detail, {'slug': 'terms'}, name='terms'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/category/<slug:slug>/', views.blog_by_category, name='blog_by_category'),
    path('blog/tag/<slug:slug>/', views.blog_by_tag, name='blog_by_tag'),
    
    # CMS Admin views
    path('cms/', views.cms_dashboard, name='cms_dashboard'),
    path('cms/pages/', views.page_list, name='page_list'),
    path('cms/pages/create/', views.page_create, name='page_create'),
    path('cms/pages/<int:pk>/edit/', views.page_edit, name='page_edit'),
    path('cms/pages/<int:pk>/delete/', views.page_delete, name='page_delete'),
    
    path('cms/posts/', views.post_list, name='post_list'),
    path('cms/posts/create/', views.post_create, name='post_create'),
    path('cms/posts/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('cms/posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    
    path('cms/media/', views.media_list, name='media_list'),
    path('cms/media/upload/', views.media_upload, name='media_upload'),
    path('cms/media/<int:pk>/delete/', views.media_delete, name='media_delete'),
    
    path('cms/navigation/', views.navigation_edit, name='navigation_edit'),
    path('cms/footer/', views.footer_edit, name='footer_edit'),
    
    # Block builder
    path('cms/blocks/builder/', views.block_builder, name='block_builder'),
    path('cms/blocks/preview/', views.render_block_preview, name='block_preview'),
    
    # API endpoints
    path('cms/api/media/', views.api_media_list, name='api_media_list'),
    path('cms/api/categories/', views.api_categories, name='api_categories'),
    path('cms/api/tags/', views.api_tags, name='api_tags'),
    
    # Image upload for block builder (GrapesJS compatibility)
    path('upload-image', views.upload_image, name='upload_image'),
]