# your_app/templatetags/nav_tags.py

from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag
def active(request, pattern):
    if pattern == resolve(request.path).url_name:
        return 'active'
    return ''
