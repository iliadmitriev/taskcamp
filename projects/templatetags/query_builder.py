"""
Query builder template tag module.

"""

from django import template
from django.http import QueryDict

register = template.Library()


@register.simple_tag
def query_builder(query: QueryDict, **kwargs) -> str:
    """Register template tag for query building.

    Builds query from base GET query adding extra parameters to it.

    Examples:
        Add params page: 0, limit: 10 to get query
        {% query_builder request.GET page=0 limit=10 %}

    Args:
        query (QueryDict): base query
        **kwargs: extra parameters to add

    Returns:
        (str) GET query string starting with ?
    """
    query_dict = query.copy()
    for k, v in kwargs.items():
        if k == "order_by" and query_dict.get(k) == v:
            query_dict[k] = "-" + v
        else:
            query_dict[k] = v
    return "?" + query_dict.urlencode() or ""
