from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import IndexView, MailingListView

appname = MailingConfig.name


urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list')
]