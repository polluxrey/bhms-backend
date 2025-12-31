from django import template

register = template.Library()


@register.filter
def currency(value, symbol="PHP"):
    return f"{symbol}{float(value):,.2f}"
