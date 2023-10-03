from django.core.cache import cache

from blog.models import BlogPost
from config import settings
from mailing.models import Mailing, Client


def get_blogposts():
    if settings.CACHE_ENABLED:
        key = 'blogpost_list'
        blogpost_list = cache.get(key)
        if blogpost_list is None:
            blogpost_list = BlogPost.objects.all()
            cache.set(key, blogpost_list)
    else:
        blogpost_list = BlogPost.objects.all()

    return blogpost_list


def get_mailings():
    if settings.CACHE_ENABLED:
        key = 'mailing_list'
        mailing_list = cache.get(key)
        if mailing_list is None:
            mailing_list = Mailing.objects.all()
            cache.set(key, mailing_list)
    else:
        mailing_list = Mailing.objects.all()

    return mailing_list


def get_clients():
    if settings.CACHE_ENABLED:
        key = 'client_list'
        client_list = cache.get(key)
        if client_list is None:
            client_list = Client.objects.all()
            cache.set(key, client_list)
    else:
        client_list = Client.objects.all()

    return client_list
