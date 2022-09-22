from django.core.management.base import BaseCommand

from service import models
from service import tasks


class Command(BaseCommand):

    def handle(self, *args, **options):
        accounts = list(models.AccountAddress.objects.all().values_list('address', flat=True))
        for account in accounts:
            tasks.actualize_account.apply_async(args=[account])
