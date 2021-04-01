from django import template
register = template.Library()


@register.filter(name='add_attr')
def add_attr(field, extra_attr):
    attrs = field.field.widget.attrs
    attrs.update(extra_attr)
    return field.as_widget(attrs=attrs)


@register.simple_tag
def attr(**kwargs):
    return kwargs
