from django import forms

from .models import Client, Message, MailingList

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"


class MailingListForm(forms.ModelForm):
    class Meta:
        model = MailingList
        fields = "__all__"
