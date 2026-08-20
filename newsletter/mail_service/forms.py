from datetime import datetime
from typing import Any

from django import forms
from django.utils import timezone

from .models import Client, MailingList, Message


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ("owner",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                }
            )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ("owner",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                }
            )


class MailingListForm(forms.ModelForm):

    class Meta:
        model = MailingList
        # fields = "__all__"
        exclude = (
            "status",
            "owner",
            "is_enable",
        )

        widgets = {
            "dispatch_start": forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={
                    "type": "datetime-local",
                    "step": "1",
                    "class": "form-control",
                },
            ),
            "dispatch_end": forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={
                    "type": "datetime-local",
                    "step": "1",
                    "class": "form-control",
                },
            ),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        user = kwargs.pop("user")
        print(user)
        super().__init__(*args, **kwargs)

        if user:
            assert isinstance(self.fields["message"], forms.ModelChoiceField)
            self.fields["message"].queryset = Message.objects.filter(owner=user)
            assert isinstance(self.fields["recipients"], forms.ModelChoiceField)
            self.fields["recipients"].queryset = Client.objects.filter(owner=user)

        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                }
            )

    def clean_dispatch_start(self) -> datetime | None:
        dispatch_start: datetime | None = self.cleaned_data["dispatch_start"]
        dt_now = timezone.now()
        if dispatch_start and dispatch_start < dt_now:
            raise forms.ValidationError("Начало отправки не может быть в прошлом")
        return dispatch_start

    def clean(self) -> dict[str, Any] | None:
        cleaned_data = super().clean()
        if cleaned_data:
            start = cleaned_data.get("dispatch_start")
            end = cleaned_data.get("dispatch_end")

            if start and end and end < start:
                raise forms.ValidationError("Начало отправки должно быть раньше окончания")
            return cleaned_data
        return None
