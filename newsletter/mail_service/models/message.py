from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Message(models.Model):
    """
    Represent newsletter message.

    Attributes:
        subject: CharField email subject
        body: TextField email body
    """

    subject = models.CharField(max_length=150, verbose_name="Тема письма", help_text="Укажите тему письма")
    body = models.TextField(verbose_name="Тело письма", help_text="Введите сообщение")
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="messages", verbose_name="Владелец"
    )

    def __str__(self) -> str:
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
