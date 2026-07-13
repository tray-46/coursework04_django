from django.urls import path

from ..mail_service.apps import MailServiceConfig

from . import views

app_name = MailServiceConfig.name

urlpatterns = [
]
