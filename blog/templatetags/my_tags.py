from django import template
from config.settings import MEDIA_URL


register = template.Library()


@register.simple_tag
def mediapath(text):
    return f'{MEDIA_URL}{text}'


@register.simple_tag
def get_list_from_queryset(queryset):
    query_list = list(queryset)
    str_list = []
    for item in query_list:
        str_list.append(str(item))
    query_str = '\n'.join(str_list)
    return query_str