import logging

from django.conf import settings
from xrpl.account import get_account_payment_transactions
from xrpl.clients import JsonRpcClient

logger = logging.getLogger('default')


def get_all_tx(address):
    client = JsonRpcClient(settings.JSON_RPC_URL)
    return get_account_payment_transactions(address=str(address), client=client)
