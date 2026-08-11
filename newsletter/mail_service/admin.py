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

    list_display = ("mailing_list__message", "status")

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
