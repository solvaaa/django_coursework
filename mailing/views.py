from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore, register_job
from mailing.scheduler import scheduler

from mailing.forms import MailingForm, ClientForm, MessageForm
from mailing.models import Mailing, Client, MailingMessage, MailingLogs

from mailing.services import send_email


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
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mailing = form.save(commit=False)
            new_mailing.status = 'START'
            new_mailing.save()

            frequencies = {
                'ONCE': 'ONCE',
                'DAILY': 'DAILY',
                'WEEKLY': 'WEEKLY',
                'MONTHLY': 'MONTHLY'
            }

            response = super().form_valid(form)
            job_id = str(form.instance.pk)
            time = form.cleaned_data['mailing_time']
            frequency = form.cleaned_data['frequency']
            scheduler_frequency = frequencies[frequency]
            message = form.instance.message
            email_list = []
            scheduler_args = [
                message.subject,
                message.body
            ]
            for client in form.cleaned_data['clients']:
                email_list.append(client.email)
            scheduler.add_job(
                send_email,
                args=scheduler_args,
                trigger=CronTrigger(second="*/10"),  # Every 10 seconds
                id=job_id,  # The `id` assigned to each job MUST be unique
                max_instances=1,
                replace_existing=True,
            )
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    extra_context = {
        'form_name': 'Редактирование',
        'button_name': 'Редактировать'
    }
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    extra_context = {
        'form_name': 'Добавление',
        'button_name': 'Добавить'
    }
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    extra_context = {
        'form_name': 'Редактирование',
        'button_name': 'Редактировать'
    }
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class MessageListView(ListView):
    model = MailingMessage


class MessageDetailView(DetailView):
    model = MailingMessage


class MessageCreateView(CreateView):
    model = MailingMessage
    extra_context = {
        'form_name': 'Добавление',
        'button_name': 'Добавить'
    }
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(UpdateView):
    model = MailingMessage
    extra_context = {
        'form_name': 'Редактирование',
        'button_name': 'Редактировать'
    }
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:message_list')


class LogListView(ListView):
    model = MailingLogs


class LogDetailView(DetailView):
    model = MailingLogs