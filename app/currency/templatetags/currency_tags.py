from django import template

register = template.Library()


@register.filter
def minus(value, arg):
    return value - arg
