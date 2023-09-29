from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import IndexView, MailingListView, MailingDetailView

appname = MailingConfig.name


urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
]