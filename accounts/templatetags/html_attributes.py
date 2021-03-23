from django import template
register = template.Library()


@register.filter(name='class')
def add_class(field, value):
    return field.as_widget(attrs={'class': value})
