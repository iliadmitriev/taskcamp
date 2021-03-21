from django import template


register = template.Library()


@register.simple_tag
def query_builder(query, **kwargs):
    query_dict = query.copy()
    for k, v in kwargs.items():
        if k == 'order_by' and query_dict.get(k) == v:
            query_dict[k] = '-' + v
        else:
            query_dict[k] = v
    return '?' + query_dict.urlencode() or ''
