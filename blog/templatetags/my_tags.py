from django import template
from config.settings import MEDIA_URL


register = template.Library()


@register.simple_tag
def mediapath(text):
    return f'{MEDIA_URL}{text}'

