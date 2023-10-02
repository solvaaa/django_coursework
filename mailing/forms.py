from django import forms
from mailing.models import Mailing, Client, MailingMessage


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing
        fields = '__all__'
        exclude = ('status', 'user', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["clients"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["clients"].queryset = Client.objects.all()


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('user', )


class MessageForm(forms.ModelForm):

    class Meta:
        model = MailingMessage
        fields = '__all__'
        exclude = ('user', )
