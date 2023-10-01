from django import forms
from mailing.models import Mailing, Client, MailingMessage


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing
        fields = '__all__'


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'


class MessageForm(forms.ModelForm):

    class Meta:
        model = MailingMessage
        fields = '__all__'
