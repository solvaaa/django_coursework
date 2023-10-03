from django import forms

from mailing.models import Mailing, Client, MailingMessage


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing
        fields = '__all__'
        exclude = ('status', 'user', )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields["clients"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields['mailing_time'].widget = forms.widgets.TimeInput()

        if self.user.is_authenticated:
            if self.user.is_superuser:
                clients = Client.objects.all()
                messages = MailingMessage.objects.all()
            else:
                clients = Client.objects.filter(user=self.user)
                messages = MailingMessage.objects.filter(user=self.user)
        else:
            clients = Client.objects.none()
            messages = MailingMessage.objects.none()

        self.fields["clients"].queryset = clients
        self.fields["message"].queryset = messages


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
