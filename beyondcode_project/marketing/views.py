from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Page, Post, NavMenu, Footer, Category, Tag, MediaAsset
from .forms import PageForm, PostForm, NavMenuForm, FooterForm, MediaAssetForm
from .permissions import is_cms_admin
from .renderers import render_block
from .blocks import BLOCK_TYPES


User = get_user_model()


# -- Public Views -----------------------------------------------------------

def home(request):
    """Homepage view - renders the homepage page if it exists."""
    try:
        homepage = Page.objects.get(slug='home', status='published')
    except Page.DoesNotExist:
        # Fallback to a simple homepage if no 'home' page exists
        homepage = None
    
    # Get navigation and footer
    nav_menu = NavMenu.objects.filter(name='Primary').first()
    footer = Footer.objects.filter(label='Default').first()
    
    context = {
        'page': homepage,
        'nav_menu': nav_menu,
        'footer': footer,
    }
    return render(request, 'marketing/pages/home.html', context)


def page_detail(request, slug):
    """Display a single page."""
    page = get_object_or_404(Page, slug=slug, status='published')
    nav_menu = NavMenu.objects.filter(name='Primary').first()
    footer = Footer.objects.filter(label='Default').first()
    
    context = {
        'page': page,
        'nav_menu': nav_menu,
        'footer': footer,
    }
    return render(request, 'marketing/pages/detail.html', context)


def blog_list(request):
    """Display list of blog posts."""
    posts = Post.objects.filter(
        status='published',
        publish_at__lte=timezone.now()
    ).select_related('author').prefetch_related('categories', 'tags').order_by('-publish_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    nav_menu = NavMenu.objects.filter(name='Primary').first()
    footer = Footer.objects.filter(label='Default').first()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    context = {
        'page_obj': page_obj,
        'nav_menu': nav_menu,
        'footer': footer,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'marketing/blog/list.html', context)


def blog_detail(request, slug):
    """Display a single blog post."""
    post = get_object_or_404(Post, slug=slug, status='published')
    nav_menu = NavMenu.objects.filter(name='Primary').first()
    footer = Footer.objects.filter(label='Default').first()
    
    context = {
        'post': post,
        'nav_menu': nav_menu,
        'footer': footer,
    }
    return render(request, 'marketing/blog/detail.html', context)


def blog_by_category(request, slug):
    """Display blog posts by category."""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(
        status='published',
        publish_at__lte=timezone.now(),
        categories=category
    ).select_related('author').prefetch_related('categories', 'tags').order_by('-publish_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    nav_menu = NavMenu.objects.filter(name='Primary').first()
    footer = Footer.objects.filter(label='Default').first()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    context = {
        'page_obj': page_obj,
        'category': category,
        'nav_menu': nav_menu,
        'footer': footer,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'marketing/blog/list.html', context)


def blog_by_tag(request, slug):
    """Display blog posts by tag."""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(
        status='published',
        publish_at__lte=timezone.now(),
        tags=tag
    ).select_related('author').prefetch_related('categories', 'tags').order_by('-publish_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    nav_menu = NavMenu.objects.filter(name='Primary').first()
    footer = Footer.objects.filter(label='Default').first()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    context = {
        'page_obj': page_obj,
        'tag': tag,
        'nav_menu': nav_menu,
        'footer': footer,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'marketing/blog/list.html', context)


# -- CMS Admin Views --------------------------------------------------------

@login_required
@is_cms_admin
def cms_dashboard(request):
    """CMS dashboard for content management."""
    pages = Page.objects.all().order_by('-updated_at')
    posts = Post.objects.all().order_by('-updated_at')
    media_assets = MediaAsset.objects.all().order_by('-uploaded_at')
    
    context = {
        'pages': pages,
        'posts': posts,
        'media_assets': media_assets,
    }
    return render(request, 'marketing/cms/dashboard.html', context)


@login_required
@is_cms_admin
def page_list(request):
    """List all pages."""
    pages = Page.objects.all().order_by('-updated_at')
    return render(request, 'marketing/cms/pages/list.html', {'pages': pages})


@login_required
@is_cms_admin
def page_create(request):
    """Create a new page."""
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.author = request.user
            page.save()
            messages.success(request, 'Page created successfully.')
            return redirect('marketing:page_edit', pk=page.pk)
    else:
        form = PageForm()
    
    return render(request, 'marketing/cms/pages/form.html', {
        'form': form,
        'title': 'Create Page',
    })


@login_required
@is_cms_admin
def page_edit(request, pk):
    """Edit an existing page."""
    page = get_object_or_404(Page, pk=pk)
    
    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            messages.success(request, 'Page updated successfully.')
            return redirect('marketing:page_edit', pk=page.pk)
    else:
        form = PageForm(instance=page)
    
    return render(request, 'marketing/cms/pages/form.html', {
        'form': form,
        'page': page,
        'title': 'Edit Page',
    })


@login_required
@is_cms_admin
def page_delete(request, pk):
    """Delete a page."""
    page = get_object_or_404(Page, pk=pk)
    
    if request.method == 'POST':
        page.delete()
        messages.success(request, 'Page deleted successfully.')
        return redirect('marketing:page_list')
    
    return render(request, 'marketing/cms/pages/confirm_delete.html', {'page': page})


@login_required
@is_cms_admin
def post_list(request):
    """List all blog posts."""
    posts = Post.objects.all().order_by('-updated_at')
    return render(request, 'marketing/cms/posts/list.html', {'posts': posts})


@login_required
@is_cms_admin
def post_create(request):
    """Create a new blog post."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Blog post created successfully.')
            return redirect('marketing:post_edit', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'marketing/cms/posts/form.html', {
        'form': form,
        'title': 'Create Blog Post',
    })


@login_required
@is_cms_admin
def post_edit(request, pk):
    """Edit an existing blog post."""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully.')
            return redirect('marketing:post_edit', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'marketing/cms/posts/form.html', {
        'form': form,
        'post': post,
        'title': 'Edit Blog Post',
    })


@login_required
@is_cms_admin
def post_delete(request, pk):
    """Delete a blog post."""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully.')
        return redirect('marketing:post_list')
    
    return render(request, 'marketing/cms/posts/confirm_delete.html', {'post': post})


@login_required
@is_cms_admin
def media_list(request):
    """List all media assets."""
    media_assets = MediaAsset.objects.all().order_by('-uploaded_at')
    return render(request, 'marketing/cms/media/list.html', {'media_assets': media_assets})


@login_required
@is_cms_admin
def media_upload(request):
    """Upload a new media asset."""
    if request.method == 'POST':
        form = MediaAssetForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.uploaded_by = request.user
            media.save()
            messages.success(request, 'Media asset uploaded successfully.')
            return redirect('marketing:media_list')
    else:
        form = MediaAssetForm()
    
    return render(request, 'marketing/cms/media/form.html', {
        'form': form,
        'title': 'Upload Media',
    })


@login_required
@is_cms_admin
def media_delete(request, pk):
    """Delete a media asset."""
    media = get_object_or_404(MediaAsset, pk=pk)
    
    if request.method == 'POST':
        media.delete()
        messages.success(request, 'Media asset deleted successfully.')
        return redirect('marketing:media_list')
    
    return render(request, 'marketing/cms/media/confirm_delete.html', {'media': media})


@login_required
@is_cms_admin
def navigation_edit(request):
    """Edit navigation menu."""
    nav_menu, created = NavMenu.objects.get_or_create(
        name='Primary',
        defaults={'items_json': []}
    )
    
    if request.method == 'POST':
        form = NavMenuForm(request.POST, instance=nav_menu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Navigation updated successfully.')
            return redirect('marketing:navigation_edit')
    else:
        form = NavMenuForm(instance=nav_menu)
    
    return render(request, 'marketing/cms/navigation/form.html', {
        'form': form,
        'nav_menu': nav_menu,
    })


@login_required
@is_cms_admin
def footer_edit(request):
    """Edit footer content."""
    footer, created = Footer.objects.get_or_create(
        label='Default',
        defaults={
            'columns_json': [],
            'cta_title': '',
            'cta_body': '',
            'cta_button_label': '',
            'cta_button_url': '',
            'legal_text': '',
        }
    )
    
    if request.method == 'POST':
        form = FooterForm(request.POST, instance=footer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Footer updated successfully.')
            return redirect('marketing:footer_edit')
    else:
        form = FooterForm(instance=footer)
    
    return render(request, 'marketing/cms/footer/form.html', {
        'form': form,
        'footer': footer,
    })


# -- Block Builder Views ----------------------------------------------------

@login_required
@is_cms_admin
def block_builder(request):
    """Block builder interface."""
    return render(request, 'marketing/cms/blocks/builder.html', {
        'block_types': BLOCK_TYPES,
    })


@csrf_exempt
@require_POST
@login_required
@is_cms_admin
def render_block_preview(request):
    """Render a block preview for the block builder."""
    try:
        block_data = request.POST.get('block_data')
        if not block_data:
            return JsonResponse({'error': 'No block data provided'}, status=400)
        
        import json
        block = json.loads(block_data)
        html = render_block(block)
        
        return JsonResponse({'html': html})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# -- API Views --------------------------------------------------------------

@login_required
@is_cms_admin
def api_media_list(request):
    """API endpoint for media assets (used by block builder)."""
    media_assets = MediaAsset.objects.all().values('id', 'title', 'file_url', 'file_type')
    return JsonResponse(list(media_assets), safe=False)


@login_required
@is_cms_admin
def api_categories(request):
    """API endpoint for categories."""
    categories = Category.objects.all().values('id', 'name', 'slug')
    return JsonResponse(list(categories), safe=False)


@login_required
@is_cms_admin
def api_tags(request):
    """API endpoint for tags."""
    tags = Tag.objects.all().values('id', 'name', 'slug')
    return JsonResponse(list(tags), safe=False)