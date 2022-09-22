import logging

from XRPtransactions.celery import app
from service.xrpl_management import get_all_tx
from service import models

logger = logging.getLogger('tasks')


@app.task(name='actualize_account')
def actualize_account(account):
    transactions = get_all_tx(account)
    try:
        account_instance = models.AccountAddress.objects.get(address=account)
    except models.AccountAddress.DoesNotExist:
        return
    tx_for_creation = list()
    for tx_num, transaction in enumerate(transactions):
        transaction_data = transaction['tx']
        tx_for_creation.append(
            models.Transactions(
                hash=transaction_data['hash'],
                ledger_index=transaction_data['ledger_index'],
                amount=transaction_data['Amount'],
                account=transaction_data['Account'],
                destination=account_instance,
                destinationTag=transaction_data.get('DestinationTag'),
                fee=transaction_data['Fee']
            )
        )
    models.Transactions.objects.bulk_create(tx_for_creation, batch_size=300, ignore_conflicts=True)


@app.task(name='process_payment')
def process_payment(payment_body):
    logger.info(f'Process payment: {payment_body}')
    models.Transactions.objects.get_or_create(hash=payment_body['hash'],
                                              defaults={
                                                  'ledger_index': payment_body['ledger_index'],
                                                  'amount': payment_body['Amount'],
                                                  'account': payment_body['Account'],
                                                  'destination': models.AccountAddress.objects.get(
                                                      address=payment_body['Destination']
                                                  ),
                                                  'destinationTag': payment_body.get('DestinationTag'),
                                                  'fee': payment_body['Fee'],
                                              })
