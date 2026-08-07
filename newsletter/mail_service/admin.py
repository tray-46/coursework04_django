from django.contrib import admin

from .models import Client, MailingList, Message, DispatchAttempt

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Client admin model"""

    list_display = ("email",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Message admin model"""

    list_display = ("subject",)


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    """MailingList admin model"""

    list_display = ("message", "status")

@admin.register(DispatchAttempt)
class DispatchAttemptAdmin(admin.ModelAdmin):
    """DispatchAttempt admin model"""

    list_display = ("mailing_list", "status")
