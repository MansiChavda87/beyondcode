import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def to_json(value):
    """
    Convert a Python object to JSON for use in templates.
    This is useful for passing data to JavaScript.
    """
    try:
        return mark_safe(json.dumps(value))
    except (TypeError, ValueError):
        return mark_safe('null')


@register.filter
def json_script(value, element_id):
    """
    Output value wrapped in a <script> tag.
    """
    json_str = json.dumps(value)
    return mark_safe(
        f'<script id="{element_id}" type="application/json">{json_str}</script>'
    )