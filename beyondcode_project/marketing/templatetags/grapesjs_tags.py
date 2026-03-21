"""
Template tags for GrapesJS integration
"""
from django import template
from django.utils.safestring import mark_safe
from ..utils import render_grapesjs_content, get_grapesjs_html, get_grapesjs_css

register = template.Library()


@register.filter
def render_grapesjs(content_data):
    """
    Template filter to render GrapesJS content with proper CSS styling
    
    Usage in templates:
    {{ post.blocks_html|render_grapesjs|safe }}
    
    Args:
        content_data: Either a string (JSON) or dict containing GrapesJS data
        
    Returns:
        str: HTML content with embedded CSS for proper rendering
    """
    return mark_safe(render_grapesjs_content(content_data))


@register.filter
def grapesjs_html(content_data):
    """
    Template filter to extract just the HTML from GrapesJS content data
    
    Usage in templates:
    {{ post.blocks_html|grapesjs_html|safe }}
    
    Args:
        content_data: Either a string (JSON) or dict containing GrapesJS data
        
    Returns:
        str: HTML content only
    """
    return mark_safe(get_grapesjs_html(content_data))


@register.filter
def grapesjs_css(content_data):
    """
    Template filter to extract just the CSS from GrapesJS content data
    
    Usage in templates:
    {{ post.blocks_html|grapesjs_css|safe }}
    
    Args:
        content_data: Either a string (JSON) or dict containing GrapesJS data
        
    Returns:
        str: CSS content only
    """
    return mark_safe(get_grapesjs_css(content_data))
