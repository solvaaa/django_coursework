from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class IndexView(TemplateView):
    template_name = 'mailing/base.html'
    extra_context = {
        'title': 'test'
    }