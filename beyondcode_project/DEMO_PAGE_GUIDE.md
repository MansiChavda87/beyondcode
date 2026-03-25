# Demo Page Implementation Guide

This document provides a comprehensive guide for using the dynamic Demo Page functionality implemented with GrapesJS in Django.

## Overview

The Demo Page is a fully dynamic page that allows administrators to create and edit page content using the GrapesJS visual editor. All content (HTML and CSS) is stored in the database and rendered dynamically on the frontend without any static HTML files.

## Features

✅ **Dynamic Content Storage**: Page content is stored in the database using the `blocks_json` field
✅ **Visual Editor**: GrapesJS editor in Django admin for drag-and-drop page building
✅ **CSS Integration**: Custom CSS is automatically embedded and applied
✅ **No Static Files**: Everything is generated dynamically from database content
✅ **Template Tags**: Proper template tags for safe rendering of GrapesJS content
✅ **URL Routing**: Clean URL at `/demo/` for the demo page

## Architecture

### Database Model
The `Page` model includes:
- `blocks_json`: Stores GrapesJS content structure (HTML + CSS)
- `blocks_html`: Processed HTML content (auto-generated)
- `status`: Publication status (draft/published/scheduled)
- `slug`: URL identifier (must be 'demo' for the demo page)

### Admin Interface
- GrapesJS editor widget for visual page building
- Form validation and content processing
- Preview capabilities

### Frontend Rendering
- Dynamic content rendering using template tags
- Automatic CSS embedding
- Fallback content for empty pages

## Usage Instructions

### 1. Creating the Demo Page

1. **Login to Django Admin**
   - Visit: `http://localhost:8000/admin/`
   - Login with admin credentials

2. **Create a New Page**
   - Navigate to: Marketing → Pages
   - Click "Add Page"
   - Fill in the following fields:
     - **Title**: "Demo Page" (or your preferred title)
     - **Slug**: `demo` (this is required for the URL)
     - **Status**: `Published`
     - **Content**: Use the GrapesJS editor below to design your page

3. **Using the GrapesJS Editor**
   - The editor provides a drag-and-drop interface
   - Add sections, text, images, buttons, etc.
   - Style elements using the built-in CSS editor
   - Preview your changes in real-time

4. **Save the Page**
   - Click "Save" to store your content in the database
   - The content is automatically processed and stored as JSON

### 2. Viewing the Demo Page

1. **Visit the Demo Page**
   - Navigate to: `http://localhost:8000/demo/`
   - Your created content will be displayed

2. **Content Rendering**
   - HTML content is rendered with embedded CSS
   - All styles are applied automatically
   - Responsive design is preserved

### 3. Editing Existing Content

1. **Return to Admin Panel**
   - Go back to Django admin
   - Navigate to Marketing → Pages
   - Find your "demo" page

2. **Edit Content**
   - Click "Edit" next to the page
   - Make changes using the GrapesJS editor
   - Save your changes

3. **View Updates**
   - Refresh the `/demo/` page to see changes
   - Changes are applied immediately

## Technical Implementation

### Models

```python
class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20, choices=PublishedStatus.choices)
    blocks_json = models.JSONField(blank=True, null=True)  # GrapesJS content
    blocks_html = models.TextField(blank=True)  # Processed HTML
    # ... other fields
```

### Views

```python
def demo_page(request):
    """Display the Demo Page with dynamic content from database."""
    try:
        demo_page = Page.objects.get(slug='demo', status='published')
    except Page.DoesNotExist:
        demo_page = None
    
    context = {
        'page': demo_page,
        # ... other context
    }
    return render(request, 'marketing/pages/demo.html', context)
```

### Templates

```html
{% load grapesjs_tags %}

{% if page.blocks_json %}
    <!-- Render GrapesJS content with CSS using template tags -->
    {{ page.blocks_json|render_grapesjs|safe }}
{% else %}
    <!-- Fallback content -->
    <div class="demo-page-fallback">
        <!-- Static fallback content -->
    </div>
{% endif %}
```

### URL Configuration

```python
path('demo/', views.demo_page, name='demo_page'),
```

## Best Practices

### Content Creation
- Use semantic HTML structure
- Apply consistent styling
- Test responsive behavior
- Keep content accessible

### Performance
- Optimize images before uploading
- Minimize CSS bloat
- Use efficient selectors
- Consider content caching for high-traffic scenarios

### Security
- Content is automatically sanitized
- Template tags ensure safe rendering
- Admin permissions control access
- Regular backups of database content

## Troubleshooting

### Common Issues

1. **Page Not Found**
   - Ensure the page slug is exactly `demo`
   - Check that status is `Published`
   - Verify the page exists in the database

2. **Content Not Displaying**
   - Check if `blocks_json` contains valid content
   - Verify template tags are loaded (`{% load grapesjs_tags %}`)
   - Ensure CSS is properly formatted

3. **Styling Issues**
   - Check CSS syntax in GrapesJS editor
   - Verify CSS is being embedded in the template
   - Test in different browsers

4. **Editor Not Loading**
   - Ensure GrapesJS assets are loaded
   - Check browser console for JavaScript errors
   - Verify widget configuration

### Debug Commands

```bash
# Check if demo page exists
python manage.py shell
>>> from marketing.models import Page
>>> page = Page.objects.get(slug='demo')
>>> print(page.blocks_json)

# Test template rendering
>>> from marketing.utils import render_grapesjs_content
>>> content = page.blocks_json
>>> rendered = render_grapesjs_content(content)
>>> print(rendered[:200])  # First 200 chars
```

## Advanced Usage

### Custom CSS Classes
- Use Tailwind CSS classes for styling
- Add custom CSS in the GrapesJS editor
- Leverage existing CSS framework classes

### Dynamic Content
- Integrate with other Django models
- Use template variables in content
- Create reusable content blocks

### Multi-Language Support
- Create separate pages for different languages
- Use language-specific slugs (e.g., `demo-en`, `demo-es`)
- Implement language switching

## Migration from Static HTML

If you have existing static HTML content:

1. **Extract Content**
   - Copy HTML structure
   - Extract CSS styles
   - Identify assets (images, fonts)

2. **Import to GrapesJS**
   - Use the GrapesJS editor's import feature
   - Paste HTML content
   - Import CSS styles
   - Upload assets

3. **Test and Refine**
   - Verify rendering matches original
   - Test responsive behavior
   - Optimize for performance

## Future Enhancements

- **Content Versioning**: Track changes and enable rollback
- **Preview Mode**: Preview changes before publishing
- **Scheduled Publishing**: Set publication dates
- **Content Blocks**: Reusable content components
- **Analytics Integration**: Track page performance
- **A/B Testing**: Test different content variations

## Support

For technical issues or questions:
1. Check the troubleshooting section
2. Review Django admin logs
3. Test with minimal content
4. Consult Django and GrapesJS documentation

## Files Modified/Created

- `marketing/views.py` - Added `demo_page` view
- `marketing/urls.py` - Added `/demo/` URL route
- `marketing/templates/marketing/pages/demo.html` - Demo page template
- `test_demo_page.py` - Test suite for verification
- `DEMO_PAGE_GUIDE.md` - This documentation file

## Conclusion

The Demo Page implementation provides a powerful, flexible solution for creating dynamic content without static HTML files. The combination of GrapesJS for editing and Django for backend management creates an efficient workflow for content creation and management.

The system is designed to be:
- **User-friendly**: Visual editor for non-technical users
- **Developer-friendly**: Clean code structure and documentation
- **Scalable**: Can handle complex content and high traffic
- **Maintainable**: Clear separation of concerns and good practices