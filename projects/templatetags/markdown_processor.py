"""
Markdown filter Jinja2 template tag.

Attributes:
    register (Library): template library

Methods:
     markdown_processor: markdown filter for Jinja2

"""

from django import template
from markdown import markdown

register = template.Library()


@register.filter(name="markdown", is_safe=True)
def markdown_processor(text: str) -> str:
    """Process Markdown text.

    Generates html template from Markdown text.

    Args:
        text (str):

    Returns:
        (str):
    """
    return markdown(text)
