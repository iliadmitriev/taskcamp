"""
Html filters and tags for Jinja2 module.

"""
from typing import Dict, Any

from django import template
from django.forms import BoundField
from django.utils.safestring import SafeString

register = template.Library()


@register.filter(name="add_attr")
def add_attr(field: BoundField, extra_attr: Dict[str, str]) -> SafeString:
    """Add css attributes to field widget."""
    attrs = field.field.widget.attrs
    attrs.update(extra_attr)
    return field.as_widget(attrs=attrs)


@register.simple_tag
def attr(**kwargs) -> Dict[str, Any]:
    """Build dict from attributes."""
    return kwargs
