from django import template

register = template.Library()

@register.filter(name='parcelas')
def parcelas(value, arg):
    value = (value/int(arg))
    return value