from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """
    Represent site user

    Inherits from AbstractUser.
    Redefine username field to email.

    Attributes:
        first_name: (CharField)
        last_name: (CharField)
        email: (EmailField) Email address of user, required
        is_staff: (BooleanField)
        is_active: (BooleanField)
        date_joined: (DateTimeField)
    """

    username: Optional[str] = None  # type: ignore[assignment]
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Введите Ваш email")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """Meta options for User model"""

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]
