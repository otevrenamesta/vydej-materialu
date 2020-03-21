from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from ...config import GROUPS


class Command(BaseCommand):
    help = "Nahraje do databáze skupiny pro oprávnění"

    def handle(self, *args, **options):
        self.stdout.write("Nahrávám skupiny pro oprávnění...")

        for config in GROUPS:
            self.stdout.write(f" - {config['group_name']}")
            group, _ = Group.objects.get_or_create(name=config["group_name"])
            permissions = Permission.objects.filter(codename__in=config["permissions"])
            group.permissions.set(list(permissions))
