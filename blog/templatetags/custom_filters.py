from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def add_red_star(field):
    if field.field.required:
        return mark_safe(f"<span class='required-field'></span> {field.label_tag()}")
    return field.label_tag()