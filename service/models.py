from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from service import tasks
from service.redis_management import send_message


class AccountAddress(models.Model):
    class Meta:
        verbose_name = 'XRPL аккаунт'
        verbose_name_plural = 'XRPL аккаунты'

    address = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.address


@receiver(post_save, sender=AccountAddress)
def get_all_transactions_for_account(sender, instance, created, **kwargs):
    tasks.actualize_account.apply_async(args=[instance.address])
    send_message({'add': instance.address})


@receiver(post_delete, sender=AccountAddress)
def delete_account_from_receiver(sender, instance, **kwargs):
    send_message({'delete': instance.address})


class Transactions(models.Model):
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        indexes = [
            models.Index(fields=['ledger_index']),
            models.Index(fields=['destination', 'account'])
        ]
    hash = models.CharField(max_length=256, unique=True)
    ledger_index = models.PositiveBigIntegerField()
    amount = models.CharField(max_length=80)
    account = models.CharField(max_length=256)
    destination = models.ForeignKey(AccountAddress, related_name='transactions', on_delete=models.CASCADE)
    destinationTag = models.PositiveBigIntegerField(null=True, blank=True)
    fee = models.PositiveIntegerField()
