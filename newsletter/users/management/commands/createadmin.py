import getpass
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create superuser"

    def handle(self, *args: Any, **options: Any) -> None:

        email = input("Enter your email address: ").strip()

        while True:
            password = getpass.getpass("Enter your password: ")
            password_confirmation = getpass.getpass("Enter your password again: ")
            if password != password_confirmation:
                print("Passwords do not match")
            else:
                break

        User = get_user_model()
        user, created = User.objects.get_or_create(email=email)
        if not created:
            self.stdout.write(self.style.ERROR("User with such address already exists"))
            return
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS("Successfully created user"))
