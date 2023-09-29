from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from mailing.models import Mailing


# Create your views here.

class IndexView(TemplateView):
    template_name = 'mailing/base.html'
    extra_context = {
        'title': 'test'
    }


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing



