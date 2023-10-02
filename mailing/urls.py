from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, MessageListView, \
    MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, LogListView, LogDetailView, \
    MailingStopView

appname = MailingConfig.name


urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('edit/<int:pk>', MailingUpdateView.as_view(), name='mailing_edit'),
    path('delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),
    path('stop/<int:pk>', MailingStopView.as_view(), name='mailing_stop'),

    path('client/list', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),

    path('message/list', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/edit/<int:pk>', MessageUpdateView.as_view(), name='message_edit'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

    path('log/list', LogListView.as_view(), name='log_list'),
    path('log/<int:pk>', LogDetailView.as_view(), name='log_detail'),

]