from html import escape

from .renderers import render_editorjs


def render_blocks(payload):
    if not payload:
        return ''
    blocks = payload.get('blocks', []) if isinstance(payload, dict) else payload
    html = ''
    for block in blocks:
        block_type = block.get('type')
        if block_type == 'rich_text':
            html += _rich_text(block)
        elif block_type == 'code':
            html += _code(block)
        elif block_type == 'callout':
            html += _callout(block)
        elif block_type == 'cta':
            html += _cta(block)
        elif block_type == 'feature_grid':
            html += _feature_grid(block)
        elif block_type == 'comparison_table':
            html += _comparison_table(block)
        elif block_type == 'table':
            html += _table(block)
        elif block_type == 'faq':
            html += _faq(block)
        elif block_type == 'quote':
            html += _quote(block)
        elif block_type == 'logo_cloud':
            html += _logo_cloud(block)
        elif block_type == 'pricing_table':
            html += _pricing_table(block)
        elif block_type == 'image_gallery':
            html += _image_gallery(block)
    return html


def _code(block):
    """Trusted raw HTML/JS block.

    This is intended for CMS admins to embed snippets (e.g. clickwrap embed).
    It is wrapped in a marker that the sanitizer preserves.
    """
    raw = block.get('html', '')
    if not raw:
        return ''
    return f"<!--TRUSTED_CODE_START-->{raw}<!--TRUSTED_CODE_END-->"


def _rich_text(block):
    content = block.get('content', {})
    if not content:
        return ''
    rendered = render_editorjs(content)
    return _wrap('div', rendered, 'cms-prose')


def _callout(block):
    title = escape(block.get('title', ''))
    body = escape(block.get('body', ''))
    return _wrap('div', _wrap('h3', title, 'cms-callout-title') + _wrap('p', body, 'cms-callout-body'), 'cms-callout')


def _cta(block):
    title = escape(block.get('title', ''))
    body = escape(block.get('body', ''))
    label = escape(block.get('button_label', ''))
    url = escape(block.get('button_url', ''))
    button = f"<a class=\"cms-cta-button\" href=\"{url}\">{label}</a>" if label and url else ''
    return _wrap('div', _wrap('h3', title, 'cms-cta-title') + _wrap('p', body, 'cms-cta-body') + button, 'cms-cta')


def _feature_grid(block):
    items = block.get('items', [])
    cards = ''.join(_wrap('div', _wrap('h4', escape(item.get('title', ''))) + _wrap('p', escape(item.get('body', ''))), 'cms-feature-card') for item in items)
    return _wrap('div', cards, 'cms-feature-grid')


def _comparison_table(block):
    headers = block.get('headers', [])
    rows = block.get('rows', [])
    head_cells = ''.join(_wrap('th', escape(header)) for header in headers)
    head = _wrap('thead', _wrap('tr', head_cells))
    body_rows = ''.join(_wrap('tr', ''.join(_wrap('td', escape(cell)) for cell in row)) for row in rows)
    body = _wrap('tbody', body_rows)
    return _wrap('table', head + body, 'cms-comparison')


def _table(block):
    headers = block.get('headers', [])
    rows = block.get('rows', [])
    head_cells = ''.join(_wrap('th', escape(header)) for header in headers)
    head = _wrap('thead', _wrap('tr', head_cells)) if headers else ''
    body_rows = ''.join(_wrap('tr', ''.join(_wrap('td', escape(cell)) for cell in row)) for row in rows)
    body = _wrap('tbody', body_rows)
    return _wrap('table', head + body, 'cms-table')


def _faq(block):
    items = block.get('items', [])
    entries = ''.join(_wrap('div', _wrap('h4', escape(item.get('question', ''))) + _wrap('p', escape(item.get('answer', ''))), 'cms-faq-item') for item in items)
    return _wrap('div', entries, 'cms-faq')


def _quote(block):
    quote = escape(block.get('quote', ''))
    author = escape(block.get('author', ''))
    inner = _wrap('blockquote', quote)
    if author:
        inner += _wrap('p', author, 'cms-quote-author')
    return _wrap('div', inner, 'cms-quote')


def _logo_cloud(block):
    logos = block.get('logos', [])
    items = ''.join(_wrap('div', f"<img src=\"{escape(logo.get('src', ''))}\" alt=\"{escape(logo.get('alt', ''))}\">", 'cms-logo-item') for logo in logos)
    return _wrap('div', items, 'cms-logo-cloud')


def _pricing_table(block):
    plans = block.get('plans', [])
    cards = ''
    for plan in plans:
        features = ''.join(_wrap('li', escape(feature)) for feature in plan.get('features', []))
        card = _wrap('h4', escape(plan.get('title', ''))) + _wrap('p', escape(plan.get('price', '')), 'cms-price') + _wrap('ul', features)
        cards += _wrap('div', card, 'cms-pricing-card')
    return _wrap('div', cards, 'cms-pricing')


def _image_gallery(block):
    title = escape(block.get('title', ''))
    layout = block.get('layout', 'grid')
    images = block.get('images', [])

    header = _wrap('h3', title, 'cms-gallery-title') if title else ''

    items = ''
    for img in images:
        src = escape(img.get('src', ''))
        alt = escape(img.get('alt', ''))
        caption = escape(img.get('caption', ''))
        inner = f'<img src="{src}" alt="{alt}" loading="lazy">'
        if caption:
            inner += _wrap('span', caption, 'cms-gallery-caption')
        items += _wrap('figure', inner, 'cms-gallery-item')

    layout_class = f'cms-gallery cms-gallery-{layout}'
    return _wrap('div', header + _wrap('div', items, layout_class), 'cms-gallery-wrap')


def _wrap(tag, content, class_name=None):
    attrs = f' class="{class_name}"' if class_name else ''
    return f'<{tag}{attrs}>{content}</{tag}>'