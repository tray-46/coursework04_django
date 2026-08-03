from django.contrib import admin

from .models import Client, Message

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Client admin model"""

    list_display = ('email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Message admin model"""

    list_display = ('subject',)
