from django import forms

from .models import Client, Message, MailingList


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", })


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", })


class MailingListForm(forms.ModelForm):
    class Meta:
        model = MailingList
        # fields = "__all__"
        exclude = ("status",)
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
