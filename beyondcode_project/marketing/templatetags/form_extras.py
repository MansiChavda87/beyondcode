import json

from django import template


register = template.Library()


@register.filter
def add_class(field, css_class):
    attrs = field.field.widget.attrs.copy()
    existing = attrs.get('class', '')
    merged = f"{existing} {css_class}".strip()
    attrs['class'] = merged
    field.field.widget.attrs.update(attrs)
    return field.as_widget(attrs=attrs)


@register.filter
def add_attr(field, attr):
    key, _, value = attr.partition('=')
    attrs = field.field.widget.attrs.copy()
    attrs[key] = value
    field.field.widget.attrs.update(attrs)
    return field.as_widget(attrs=attrs)


@register.filter(is_safe=True)
def to_json(value):
    """Convert a Python object (dict, list, etc.) to a JSON string.

    Handles the case where Django's JSONField returns Python objects
    that need to be serialized for use in HTML attributes or JS.
    """
    if value is None or value == '':
        return ''
    if isinstance(value, str):
        # Already a string -- try parsing to verify it's valid JSON,
        # otherwise treat as raw and re-serialize
        try:
            parsed = json.loads(value)
            return json.dumps(parsed)
        except (json.JSONDecodeError, TypeError):
            return value
    return json.dumps(value)