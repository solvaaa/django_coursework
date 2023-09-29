from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView

appname = MailingConfig.name


urlpatterns = [
    path('', MailingListView.as_view(), name='list'),
    path('<int:pk>', MailingDetailView.as_view(), name='detail'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('edit/<int:pk>', MailingUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', MailingDeleteView.as_view(), name='delete'),
]