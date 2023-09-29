from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingForm
from mailing.models import Mailing


# Create your views here.
class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    extra_context = {
        'form_name': 'Добавление',
        'button_name': 'Добавить'
    }
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')


class MailingUpdateView(UpdateView):
    model = Mailing
    extra_context = {
        'form_name': 'Редактирование',
        'button_name': 'Редактировать'
    }
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:list')