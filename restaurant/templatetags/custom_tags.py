from django import template
from django.utils.timezone import now
register = template.Library()

@register.simple_tag
def current_year():
    current_year = now().year
    if current_year==2024:
        return f"{current_year}"
    else:
        return f"2024-{current_year}"