from django import template
from django.utils import timezone

register = template.Library()

@register.simple_tag
def get_related_posts(post):
    """
    Get related posts from the same category, excluding the current post.
    Returns up to 3 published posts ordered by publish date.
    """
    if not post.categories.exists():
        return []
    
    # Get the first category of the post
    category = post.categories.first()
    
    # Get related posts from the same category
    related_posts = category.posts.filter(
        status='published',
        publish_at__lte=timezone.now()
    ).exclude(pk=post.pk).order_by('-publish_at')[:3]
    
    return related_posts
