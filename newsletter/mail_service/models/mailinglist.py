from django.db import models
from django.utils import timezone

from .client import Client
from .message import Message


# Create your models here.
class MailingList(models.Model):
    """
    Represent newsletter mailing list.

    Attributes:
        dispatch_start: DateTimeField, start of dispatch
        dispatch_end: DateTimeField, end of dispatch
        status: PositiveIntegerField, state of mailing list
        message: ForeignKey, mailing list message
        recipients: ManyToManyField, mailing list recipients
    """
    STATUS_CHOICES = [
        (0, "Создана"),
        (1, "Запущена"),
        (2, "Завершена"),
    ]

    dispatch_start = models.DateTimeField(verbose_name="Начало отправки", help_text="Дата и время первой отправки")
    dispatch_end = models.DateTimeField(verbose_name="Окончание отправки", help_text="Дата и время окончания отправки")
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=0, verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="mailing_lists", verbose_name="Сообщение")
    recipients = models.ManyToManyField(Client, related_name="mailing_lists")

    def __str__(self):
        return f"{self.message.subject}: {self.get_status_display()}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    @property
    def badge_class(self):
        mapping = {
            "Создана": "bg-warning",
            "Запущена": "bg-success",
            "Завершена": "bg-danger",
        }
        return mapping.get(self.get_status, "bg-secondary")

    @property
    def get_status(self):
        dt_now = timezone.now()
        if dt_now < self.dispatch_start:
            return self.STATUS_CHOICES[0][1]
        elif self.dispatch_start <= dt_now <= self.dispatch_end:
            return self.STATUS_CHOICES[1][1]
        else:
            return self.STATUS_CHOICES[2][1]
