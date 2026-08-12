"""

"""
import os
from typing import Any

from django.core.management import BaseCommand, CommandError, call_command

from ...services import send_mailinglist


class Command(BaseCommand):

    help = "start mailing list send"

    def handle(self, *args: Any, **options: Any) -> None:
        ml_id = int(input("Enter mailing list id:\n"))
        send_mailinglist(ml_id)
