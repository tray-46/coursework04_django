from django.db import models

from .mailinglist import MailingList

# Create your models here.
class DispatchAttempt(models.Model):
    """
    Represent dispatch attempt of mailing list.

    Attributes:
        mailing_list: ForeignKey, mailing list
        attempt_dt: DateTimeField, date and time of attempt
        status: BooleanField, status of attempt - success, or failure
        smtp_response: TextField, response of SMTP server
    """
    STATUS_CHOICES = [
        (False, "Не успешно"),
        (True, "Успешно"),
    ]

    mailing_list = models.ForeignKey(MailingList, on_delete=models.SET_NULL, null=True, verbose_name="Рассылка")
    attempt_dt = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.BooleanField(choices=STATUS_CHOICES, default=False, verbose_name="Статус")
    smtp_response = models.TextField(verbose_name="Ответ почтового сервера")

    def __str__(self):
        return f"{self.mailing_list.message}: {self.status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
