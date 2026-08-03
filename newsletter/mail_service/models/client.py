from django.db import models


# Create your models here.
class Client(models.Model):
    """
    Represent newsletter client.

    Attributes:
        email (EmailField): client's Email
        surname (CharField): client's surname
        first_name (CharField): client's first name
        patronymic (CharField): client's patronymic
        comment (TextField): comment for client
    """
    email = models.EmailField(unique=True, verbose_name="Email", help_text="введите email клиента")
    surname = models.CharField(max_length=100, verbose_name="Фамилия", help_text="введите фамилию клиента")
    first_name = models.CharField(max_length=100, verbose_name="Имя", help_text="введите имя клиента")
    patronymic = models.CharField(max_length=100, null=True, blank=True, verbose_name="Отчество",
                                  help_text="введите отчество клиента (при наличии)")
    comment = models.TextField(null=True, blank=True, verbose_name="Комметарий", help_text="добавте комметарий")

    def __str__(self):
        return f"{self.surname} {self.first_name} {self.patronymic}"
