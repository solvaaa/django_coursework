from django import forms
from mailing.models import Mailing


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing
        fields = '__all__'
