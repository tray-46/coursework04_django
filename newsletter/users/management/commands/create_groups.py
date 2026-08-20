from typing import Any

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create groups and assign permissions"

    def handle(self, *args: Any, **options: Any) -> None:
        managers, _ = Group.objects.get_or_create(name="Managers")
        client_view_permission = Permission.objects.get(codename="can_view_client")
        mailinglist_can_disable_permission = Permission.objects.get(codename="can_disable_mailinglist")
        mailinglist_view_permission = Permission.objects.get(codename="can_view_mailinglist")
        message_view_permission = Permission.objects.get(codename="can_view_message")
        user_can_block_permission = Permission.objects.get(codename="can_block_user")
        user_view_permission = Permission.objects.get(codename="can_view_user")

        managers.permissions.add(
            client_view_permission,
            mailinglist_can_disable_permission,
            mailinglist_view_permission,
            message_view_permission,
            user_can_block_permission,
            user_view_permission,
        )
        managers.save()

        users, _ = Group.objects.get_or_create(name="Users")
        users.save()

        self.stdout.write(self.style.SUCCESS("Groups successfully added"))
