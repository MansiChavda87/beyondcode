import re
from html import escape

from bs4 import BeautifulSoup, Comment


ALLOWED_TAGS = {
    'p', 'strong', 'em', 'b', 'i', 'u', 's', 'a', 'ul', 'ol', 'li', 'br', 'hr',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'pre', 'figure',
    'figcaption', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'span', 'div'
}

ALLOWED_ATTRS = {
    'a': {'href', 'title', 'target', 'rel'},
    'img': {'src', 'alt', 'title', 'width', 'height', 'loading'},
    'div': {'class'},
    'span': {'class'},
    'table': {'class'},
    'thead': {'class'},
    'tbody': {'class'},
    'tr': {'class'},
    'th': {'class'},
    'td': {'class'},
    'figure': {'class'},
    'figcaption': {'class'},
    'p': {'class'},
    'blockquote': {'class'},
    'h1': {'class'}, 'h2': {'class'}, 'h3': {'class'},
    'h4': {'class'}, 'h5': {'class'}, 'h6': {'class'},
}


def render_lexical_json(payload):
    if not payload:
        return ''
    root = payload.get('root', {})
    children = root.get('children', [])
    return ''.join(_render_node(child) for child in children)


def render_editorjs(payload):
    if not payload:
        return ''
    blocks = payload.get('blocks', []) if isinstance(payload, dict) else []
    html = ''
    for block in blocks:
        block_type = block.get('type')
        data = block.get('data', {})
        if block_type == 'paragraph':
            html += _wrap('p', _sanitize_inline_html(data.get('text', '')))
        elif block_type == 'header':
            level = str(data.get('level', 2))
            tag = f"h{level}"
            html += _wrap(tag, _sanitize_inline_html(data.get('text', '')))
        elif block_type == 'list':
            html += _render_editorjs_list(data)
        elif block_type == 'quote':
            html += _wrap('blockquote', _sanitize_inline_html(data.get('text', '')))
        elif block_type == 'table':
            html += _render_editorjs_table(data)
        elif block_type == 'code':
            html += _wrap('pre', _wrap('code', escape(data.get('code', ''))))
        elif block_type == 'delimiter':
            html += '<hr />'
        elif block_type == 'warning':
            title = _sanitize_inline_html(data.get('title', ''))
            message = _sanitize_inline_html(data.get('message', ''))
            html += _wrap('div', _wrap('h4', title) + _wrap('p', message), class_name='cms-callout')
        elif block_type == 'cta':
            html += _render_cta(data)
        elif block_type == 'callout':
            html += _render_callout(data)
        elif block_type == 'comparison':
            html += _render_comparison_table(data)
    return html


def _render_node(node):
    """Render a Lexical node."""
    node_type = node.get('type', '')
    if node_type == 'paragraph':
        children = node.get('children', [])
        return _wrap('p', ''.join(_render_node(child) for child in children))
    elif node_type == 'heading':
        level = node.get('tag', 'h1')
        children = node.get('children', [])
        return _wrap(level, ''.join(_render_node(child) for child in children))
    elif node_type == 'text':
        text = node.get('text', '')
        format = node.get('format', 0)
        if format & 1:  # bold
            text = _wrap('strong', text)
        if format & 2:  # italic
            text = _wrap('em', text)
        if format & 4:  # underline
            text = _wrap('u', text)
        if format & 8:  # strikethrough
            text = _wrap('s', text)
        return text
    elif node_type == 'link':
        url = node.get('url', '')
        children = node.get('children', [])
        return _wrap('a', ''.join(_render_node(child) for child in children), class_name='', attrs={'href': url})
    elif node_type == 'list':
        tag = 'ul' if node.get('listType') == 'bullet' else 'ol'
        children = node.get('children', [])
        return _wrap(tag, ''.join(_render_node(child) for child in children))
    elif node_type == 'listitem':
        children = node.get('children', [])
        return _wrap('li', ''.join(_render_node(child) for child in children))
    elif node_type == 'quote':
        children = node.get('children', [])
        return _wrap('blockquote', ''.join(_render_node(child) for child in children))
    elif node_type == 'code':
        text = node.get('text', '')
        return _wrap('pre', _wrap('code', escape(text)))
    elif node_type == 'table':
        rows = node.get('children', [])
        body_rows = ''.join(_wrap('tr', ''.join(_wrap('td', ''.join(_render_node(cell) for cell in row.get('children', []))) for row in rows)))
        return _wrap('table', _wrap('tbody', body_rows))
    return ''


def _render_cta(data):
    title = escape(data.get('title', ''))
    body = escape(data.get('body', ''))
    label = escape(data.get('button_label', ''))
    url = escape(data.get('button_url', ''))
    button = f"<a class=\"cms-cta-button\" href=\"{url}\">{label}</a>" if label and url else ''
    return _wrap('div', _wrap('h3', title, 'cms-cta-title') + _wrap('p', body, 'cms-cta-body') + button, 'cms-cta')


def _render_callout(data):
    title = escape(data.get('title', ''))
    body = escape(data.get('body', ''))
    return _wrap('div', _wrap('h3', title, 'cms-callout-title') + _wrap('p', body, 'cms-callout-body'), 'cms-callout')


def _render_comparison_table(data):
    headers = data.get('headers', [])
    rows = data.get('rows', [])
    head_cells = ''.join(_wrap('th', escape(header)) for header in headers)
    head = _wrap('thead', _wrap('tr', head_cells))
    body_rows = ''.join(_wrap('tr', ''.join(_wrap('td', escape(cell)) for cell in row)) for row in rows)
    body = _wrap('tbody', body_rows)
    return _wrap('table', head + body, 'cms-comparison')


def _render_editorjs_list(data):
    style = data.get('style', 'unordered')
    tag = 'ol' if style == 'ordered' else 'ul'
    items = ''.join(_wrap('li', _sanitize_inline_html(item)) for item in data.get('items', []))
    return _wrap(tag, items)


def _render_editorjs_table(data):
    rows = data.get('content', [])
    body_rows = ''.join(_wrap('tr', ''.join(_wrap('td', _sanitize_inline_html(cell)) for cell in row)) for row in rows)
    return _wrap('table', _wrap('tbody', body_rows), class_name='cms-table')


def _wrap(tag, content, class_name=None, attrs=None):
    if tag not in ALLOWED_TAGS:
        return ''
    attrs_str = ''
    if class_name:
        attrs_str += f' class="{class_name}"'
    if attrs:
        for key, value in attrs.items():
            if key in ALLOWED_ATTRS.get(tag, set()):
                attrs_str += f' {key}="{escape(value)}"'
    return f'<{tag}{attrs_str}>{content}</{tag}>'


def sanitize_html(html):
    if not html:
        return ''

    # Preserve trusted code blocks (used by CMS admin "code" widget).
    # Everything outside these markers is still sanitized.
    code_blocks = []

    def _stash(m):
        code_blocks.append(m.group(0))
        return f"__TRUSTED_CODE_BLOCK_{len(code_blocks) - 1}__"

    html = re.sub(
        r'<!--TRUSTED_CODE_START-->.*?<!--TRUSTED_CODE_END-->',
        _stash,
        html,
        flags=re.S,
    )

    html = re.sub(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', '', html, flags=re.I | re.S)
    html = re.sub(r'on\w+\s*=\s*"[^"]*"', '', html, flags=re.I)

    for i, block in enumerate(code_blocks):
        html = html.replace(f"__TRUSTED_CODE_BLOCK_{i}__", block)

    return html


def render_block(block):
    """Render a single block for the block builder preview."""
    if not block:
        return ''
    
    block_type = block.get('type')
    if block_type == 'rich_text':
        content = block.get('content', {})
        return render_editorjs(content)
    elif block_type == 'code':
        raw = block.get('html', '')
        if raw:
            return f"<!--TRUSTED_CODE_START-->{raw}<!--TRUSTED_CODE_END-->"
        return ''
    elif block_type == 'callout':
        title = escape(block.get('title', ''))
        body = escape(block.get('body', ''))
        return _wrap('div', _wrap('h3', title, 'cms-callout-title') + _wrap('p', body, 'cms-callout-body'), 'cms-callout')
    elif block_type == 'cta':
        title = escape(block.get('title', ''))
        body = escape(block.get('body', ''))
        label = escape(block.get('button_label', ''))
        url = escape(block.get('button_url', ''))
        button = f"<a class=\"cms-cta-button\" href=\"{url}\">{label}</a>" if label and url else ''
        return _wrap('div', _wrap('h3', title, 'cms-cta-title') + _wrap('p', body, 'cms-cta-body') + button, 'cms-cta')
    elif block_type == 'feature_grid':
        items = block.get('items', [])
        cards = ''.join(_wrap('div', _wrap('h4', escape(item.get('title', ''))) + _wrap('p', escape(item.get('body', ''))), 'cms-feature-card') for item in items)
        return _wrap('div', cards, 'cms-feature-grid')
    elif block_type == 'comparison_table':
        headers = block.get('headers', [])
        rows = block.get('rows', [])
        head_cells = ''.join(_wrap('th', escape(header)) for header in headers)
        head = _wrap('thead', _wrap('tr', head_cells))
        body_rows = ''.join(_wrap('tr', ''.join(_wrap('td', escape(cell)) for cell in row)) for row in rows)
        body = _wrap('tbody', body_rows)
        return _wrap('table', head + body, 'cms-comparison')
    elif block_type == 'table':
        headers = block.get('headers', [])
        rows = block.get('rows', [])
        head_cells = ''.join(_wrap('th', escape(header)) for header in headers)
        head = _wrap('thead', _wrap('tr', head_cells)) if headers else ''
        body_rows = ''.join(_wrap('tr', ''.join(_wrap('td', escape(cell)) for cell in row)) for row in rows)
        body = _wrap('tbody', body_rows)
        return _wrap('table', head + body, 'cms-table')
    elif block_type == 'faq':
        items = block.get('items', [])
        entries = ''.join(_wrap('div', _wrap('h4', escape(item.get('question', ''))) + _wrap('p', escape(item.get('answer', ''))), 'cms-faq-item') for item in items)
        return _wrap('div', entries, 'cms-faq')
    elif block_type == 'quote':
        quote = escape(block.get('quote', ''))
        author = escape(block.get('author', ''))
        inner = _wrap('blockquote', quote)
        if author:
            inner += _wrap('p', author, 'cms-quote-author')
        return _wrap('div', inner, 'cms-quote')
    elif block_type == 'logo_cloud':
        logos = block.get('logos', [])
        items = ''.join(_wrap('div', f"<img src=\"{escape(logo.get('src', ''))}\" alt=\"{escape(logo.get('alt', ''))}\">", 'cms-logo-item') for logo in logos)
        return _wrap('div', items, 'cms-logo-cloud')
    elif block_type == 'pricing_table':
        plans = block.get('plans', [])
        cards = ''
        for plan in plans:
            features = ''.join(_wrap('li', escape(feature)) for feature in plan.get('features', []))
            card = _wrap('h4', escape(plan.get('title', ''))) + _wrap('p', escape(plan.get('price', '')), 'cms-price') + _wrap('ul', features)
            cards += _wrap('div', card, 'cms-pricing-card')
        return _wrap('div', cards, 'cms-pricing')
    elif block_type == 'image_gallery':
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
    
    return ''


def _sanitize_inline_html(html):
    if not html:
        return ''
    soup = BeautifulSoup(html, 'html.parser')
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.find_all(True):
        if tag.name not in ALLOWED_TAGS:
            tag.unwrap()
            continue
        allowed = ALLOWED_ATTRS.get(tag.name, set())
        tag.attrs = {key: value for key, value in tag.attrs.items() if key in allowed}
    return str(soup)