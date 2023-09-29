from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView

appname = MailingConfig.name


urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('edit/<int:pk>', MailingUpdateView.as_view(), name='mailing_edit'),
    path('delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),

]