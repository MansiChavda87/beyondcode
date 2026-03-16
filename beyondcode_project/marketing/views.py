from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings

from .models import Page, Post, NavMenu, Footer, Category, Tag, MediaAsset
from .forms import PageForm, PostForm, NavMenuForm, FooterForm, MediaAssetForm, LoginForm, RegisterForm
from .permissions import cms_admin_required
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


def contact(request):
    """Contact page view."""
    nav_menu = NavMenu.objects.filter(name='Primary').first()
    footer = Footer.objects.filter(label='Default').first()
    
    context = {
        'nav_menu': nav_menu,
        'footer': footer,
    }
    return render(request, 'marketing/pages/contact.html', context)


def contact_submit(request):
    """Handle contact form submission."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Basic validation
        if not name or not email or not message:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('marketing:contact')
        
        # Here you would typically:
        # 1. Send an email notification
        # 2. Save to database
        # 3. Or integrate with a CRM
        
        # For now, just show a success message
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('marketing:contact')
    
    # If not POST, redirect to contact page
    return redirect('marketing:contact')


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
@cms_admin_required
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
@cms_admin_required
def page_list(request):
    """List all pages."""
    pages = Page.objects.all().order_by('-updated_at')
    return render(request, 'marketing/cms/pages/list.html', {'pages': pages})


@login_required
@cms_admin_required
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
@cms_admin_required
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
@cms_admin_required
def page_delete(request, pk):
    """Delete a page."""
    page = get_object_or_404(Page, pk=pk)
    
    if request.method == 'POST':
        page.delete()
        messages.success(request, 'Page deleted successfully.')
        return redirect('marketing:page_list')
    
    return render(request, 'marketing/cms/pages/confirm_delete.html', {'page': page})


@login_required
@cms_admin_required
def post_list(request):
    """List all blog posts."""
    posts = Post.objects.all().order_by('-updated_at')
    return render(request, 'marketing/cms/posts/list.html', {'posts': posts})


@login_required
@cms_admin_required
def post_create(request):
    """Create a new blog post."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Blog post created successfully.')
            return redirect('marketing:post_edit', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'marketing/cms/posts/editor.html', {
        'form': form,
        'title': 'Create Blog Post',
    })


@login_required
@cms_admin_required
def post_edit(request, pk):
    """Edit an existing blog post."""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully.')
            return redirect('marketing:post_edit', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'marketing/cms/posts/editor.html', {
        'form': form,
        'post': post,
        'title': 'Edit Blog Post',
    })


@login_required
@cms_admin_required
def post_delete(request, pk):
    """Delete a blog post."""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully.')
        return redirect('marketing:post_list')
    
    return render(request, 'marketing/cms/posts/confirm_delete.html', {'post': post})


@login_required
@cms_admin_required
def media_list(request):
    """List all media assets."""
    media_assets = MediaAsset.objects.all().order_by('-uploaded_at')
    return render(request, 'marketing/cms/media/list.html', {'media_assets': media_assets})


@login_required
@cms_admin_required
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
@cms_admin_required
def media_delete(request, pk):
    """Delete a media asset."""
    media = get_object_or_404(MediaAsset, pk=pk)
    
    if request.method == 'POST':
        media.delete()
        messages.success(request, 'Media asset deleted successfully.')
        return redirect('marketing:media_list')
    
    return render(request, 'marketing/cms/media/confirm_delete.html', {'media': media})


@login_required
@cms_admin_required
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
@cms_admin_required
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
@cms_admin_required
def block_builder(request):
    """Block builder interface."""
    return render(request, 'marketing/cms/blocks/builder.html', {
        'block_types': BLOCK_TYPES,
    })


@csrf_exempt
@require_POST
@login_required
@cms_admin_required
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


# -- Authentication Views -------------------------------------------------

def login_view(request):
    """Custom login view."""
    if request.user.is_authenticated:
        return redirect('marketing:account')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'marketing:account')
            return redirect(next_url)
    else:
        form = LoginForm()
    
    return render(request, 'marketing/auth/login.html', {
        'form': form,
        'title': 'Login'
    })


def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('marketing:account')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Account created successfully! Welcome to BeyondCode AI.')
            return redirect('marketing:account')
    else:
        form = RegisterForm()
    
    return render(request, 'marketing/auth/register.html', {
        'form': form,
        'title': 'Register'
    })


def logout_view(request):
    """Custom logout view."""
    auth_logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('marketing:home')


@login_required
def account_view(request):
    """User account/profile page."""
    user = request.user
    
    # Get user's recent posts if they have any
    user_posts = Post.objects.filter(author=user).order_by('-publish_at')[:5]
    
    context = {
        'user': user,
        'user_posts': user_posts,
        'title': 'My Account'
    }
    return render(request, 'marketing/auth/account.html', context)


def password_reset_view(request):
    """Password reset request view."""
    if request.user.is_authenticated:
        return redirect('marketing:cms_dashboard')
    
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Find users with this email
            users = User.objects.filter(email=email)
            for user in users:
                # Generate token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Send email
                subject = 'Password Reset - BeyondCode AI'
                reset_url = request.build_absolute_uri(
                    f'/accounts/reset/{uid}/{token}/'
                )
                context = {
                    'user': user,
                    'reset_url': reset_url,
                }
                message = render_to_string('marketing/auth/password_reset_email.html', context)
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True
                )
            
            messages.success(request, 'If an account with that email exists, we have sent you password reset instructions.')
            return redirect('marketing:login')
    else:
        form = PasswordResetForm()
    
    return render(request, 'marketing/auth/password_reset.html', {
        'form': form,
        'title': 'Reset Password'
    })


def password_reset_confirm_view(request, uidb64, token):
    """Password reset confirmation view."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset successfully. You can now log in.')
                return redirect('marketing:login')
        else:
            form = SetPasswordForm(user)
        
        return render(request, 'marketing/auth/password_reset_confirm.html', {
            'form': form,
            'title': 'Set New Password',
            'validlink': True
        })
    else:
        return render(request, 'marketing/auth/password_reset_confirm.html', {
            'form': None,
            'title': 'Password Reset Link Invalid',
            'validlink': False
        })


# -- SEO Views --------------------------------------------------------------

def sitemap_view(request):
    """Generate dynamic XML sitemap."""
    from django.utils import timezone
    pages = Page.objects.filter(status='published')
    posts = Post.objects.filter(status='published', publish_at__lte=timezone.now())
    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'request': request,
        'pages': pages,
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'now': timezone.now(),
    }

    sitemap_content = render_to_string('marketing/seo/sitemap.xml', context)
    return HttpResponse(sitemap_content, content_type='application/xml')


def robots_view(request):
    """Serve robots.txt file."""
    robots_content = render_to_string('marketing/seo/robots.txt', {'request': request})
    return HttpResponse(robots_content, content_type='text/plain')


# -- API Views --------------------------------------------------------------

@login_required
@cms_admin_required
def api_media_list(request):
    """API endpoint for media assets (used by block builder)."""
    media_assets = MediaAsset.objects.all().values('id', 'title', 'file_url', 'file_type')
    return JsonResponse(list(media_assets), safe=False)


@login_required
@cms_admin_required
def api_categories(request):
    """API endpoint for categories."""
    categories = Category.objects.all().values('id', 'name', 'slug')
    return JsonResponse(list(categories), safe=False)


@login_required
@cms_admin_required
def api_tags(request):
    """API endpoint for tags."""
    tags = Tag.objects.all().values('id', 'name', 'slug')
    return JsonResponse(list(tags), safe=False)