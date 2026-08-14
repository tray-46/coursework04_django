from django import forms
from django.utils import timezone

from .models import Client, Message, MailingList


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", })


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", })


class MailingListForm(forms.ModelForm):

    class Meta:
        model = MailingList
        # fields = "__all__"
        exclude = ("status", "owner",)

        widgets = {
            "dispatch_start": forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={"type": "datetime-local",
                       "step": "1",
                       "class": "form-control", }),
            "dispatch_end": forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={"type": "datetime-local",
                       "step": "1",
                       "class": "form-control", }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", })

    def clean_dispatch_start(self):
        dispatch_start = self.cleaned_data["dispatch_start"]
        dt_now = timezone.now()
        if dispatch_start and dispatch_start < dt_now:
            raise forms.ValidationError("Начало отправки не может быть в прошлом")
        return dispatch_start

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("dispatch_start")
        end = cleaned_data.get("dispatch_end")

        if start and end and end < start:
            raise forms.ValidationError("Начало отправки должно быть раньше окончания")
