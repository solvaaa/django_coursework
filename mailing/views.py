import apscheduler.jobstores.base
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore, register_job

from config.settings import CACHE_ENABLED
from mailing.scheduler import scheduler, send_email_job, start_job, remove_job

from mailing.forms import MailingForm, ClientForm, MessageForm
from mailing.models import Mailing, Client, MailingMessage, MailingLogs


# Create your views here.
class MailingListView(ListView):
    model = Mailing

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        current_user = self.request.user
        if current_user.is_authenticated:
            if current_user.is_staff or current_user.is_superuser:
                return queryset
            else:
                return queryset.filter(user=current_user)
        else:
            return queryset.none()


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Mailing
    extra_context = {
        'form_name': 'Добавление',
        'button_name': 'Добавить'
    }
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def has_permission(self):
        user = self.request.user
        return (not user.is_staff) or (user.is_superuser)

    def form_valid(self, form):
        if form.is_valid():
            new_mailing = form.save(commit=False)
            new_mailing.user = self.request.user
            new_mailing.status = 'START'
            new_mailing.save()

            response = super().form_valid(form)
            job_id = str(form.instance.pk)
            time = form.cleaned_data['mailing_time']
            frequency = form.cleaned_data['frequency']
            message = form.instance.message
            email_list = []
            for client in form.cleaned_data['clients']:
                email_list.append(client.email)
            start_job(job_id, time, frequency, message, email_list)

            if CACHE_ENABLED:
                cache.delete('mailing_list')

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class MailingUpdateView(PermissionRequiredMixin, UpdateView):
    model = Mailing
    extra_context = {
        'form_name': 'Редактирование',
        'button_name': 'Редактировать'
    }
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def has_permission(self):
        user = self.request.user
        return (not user.is_staff) or (user.is_superuser)

    def form_valid(self, form):
        if form.is_valid():

            response = super().form_valid(form)
            job_id = str(form.instance.pk)
            time = form.cleaned_data['mailing_time']
            frequency = form.cleaned_data['frequency']
            message = form.instance.message
            email_list = []
            for client in form.cleaned_data['clients']:
                email_list.append(client.email)
            remove_job(job_id)
            start_job(job_id, time, frequency, message, email_list)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class MailingDeleteView(PermissionRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def has_permission(self):
        user = self.request.user
        return (not user.is_staff) or (user.is_superuser)

    def form_valid(self, form):
        pk = str(self.object.pk)
        try:
            scheduler.remove_job(job_id=pk)
        except apscheduler.jobstores.base.JobLookupError:
            print(f'job {pk} not found')
        return super().form_valid(form)


class MailingStopView(View):

    def get(self, request, pk):
        mailing = Mailing.objects.get(pk=pk)
        mailing.status = 'FIN'
        mailing.save()
        try:
            scheduler.remove_job(job_id=str(pk))
        except apscheduler.jobstores.base.JobLookupError:
            print(f'job {pk} not found')
        return redirect('mailing:mailing_list')


class ClientListView(ListView):
    model = Client

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        current_user = self.request.user
        if current_user.is_authenticated:
            if current_user.is_staff or current_user.is_superuser:
                return queryset
            else:
                return queryset.filter(user=current_user)
        else:
            return queryset.none()


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = Client
    extra_context = {
        'form_name': 'Добавление',
        'button_name': 'Добавить'
    }
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def has_permission(self):
        user = self.request.user
        return (not user.is_staff) or (user.is_superuser)

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save(commit=False)
            new_client.user = self.request.user
            new_client.save()

            if CACHE_ENABLED:
                cache.delete('client_list')
        return super().form_valid(form)


class ClientUpdateView(PermissionRequiredMixin, UpdateView):
    model = Client
    extra_context = {
        'form_name': 'Редактирование',
        'button_name': 'Редактировать'
    }
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def has_permission(self):
        user = self.request.user
        return (not user.is_staff) or (user.is_superuser)


class ClientDeleteView(PermissionRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def has_permission(self):
        user = self.request.user
        return (not user.is_staff) or (user.is_superuser)


class MessageListView(ListView):
    model = MailingMessage

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        current_user = self.request.user
        if current_user.is_authenticated:
            if current_user.is_staff or current_user.is_superuser:
                return queryset
            else:
                return queryset.filter(user=current_user)
        else:
            return queryset.none()


class MessageDetailView(DetailView):
    model = MailingMessage


class MessageCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    model = MailingMessage
    extra_context = {
        'form_name': 'Добавление',
        'button_name': 'Добавить'
    }
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def has_permission(self):
        user = self.request.user
        return (not user.is_staff) or (user.is_superuser)

    def form_valid(self, form):
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user = self.request.user
            new_message.save()
        return super().form_valid(form)


class MessageUpdateView(PermissionRequiredMixin, UpdateView):
    model = MailingMessage
    extra_context = {
        'form_name': 'Редактирование',
        'button_name': 'Редактировать'
    }
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def has_permission(self):
        user = self.request.user
        return (not user.is_staff) or (user.is_superuser)


class MessageDeleteView(PermissionRequiredMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:message_list')

    def has_permission(self):
        user = self.request.user
        return (not user.is_staff) or (user.is_superuser)


class LogListView(ListView):
    model = MailingLogs

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        current_user = self.request.user
        if current_user.is_authenticated:
            if current_user.is_staff or current_user.is_superuser:
                return queryset
            else:
                return queryset.filter(mailing__user=current_user)
        else:
            return queryset.none()


class LogDetailView(DetailView):
    model = MailingLogs