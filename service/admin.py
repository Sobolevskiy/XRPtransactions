from django.contrib import admin

from service import models


@admin.register(models.Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    search_fields = ('hash', 'account', 'destination__address', 'ledger_index', 'destinationTag')
    list_filter = ('ledger_index', 'destination__address')
    list_display = ('hash', 'amount', 'destination', 'account', 'ledger_index')


@admin.register(models.AccountAddress)
class AccountAddressAdmin(admin.ModelAdmin):
    search_fields = ('address',)
    list_display = ('address',)
