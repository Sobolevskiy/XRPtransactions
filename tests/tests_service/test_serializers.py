import pytest

from service import serializers

pytestmark = pytest.mark.django_db


class TestTransactionSerializer:
    serializer_class = serializers.TransactionSerializer

    def test_as_list(self, three_transactions_for_second_acc):
        tx = three_transactions_for_second_acc[0]
        serializer = self.serializer_class(tx)
        tx_data = {
            'account': tx.account,
            'amount': tx.amount,
            'destination': tx.destination.address,
            'destinationTag': tx.destinationTag,
            'fee': tx.fee,
            'hash': tx.hash,
            'ledger_index': tx.ledger_index,
            'id': tx.id
        }
        assert serializer.data == tx_data

    def test_creation(self, account):
        tx_creation_data = {
            'account': "someAcc2",
            'amount': "123",
            'destination': account.address,
            'destinationTag': None,
            'fee': 2,
            'hash': 'UniqueHash',
            'ledger_index': 123,
        }
        serializer = self.serializer_class(data=tx_creation_data)
        assert serializer.is_valid()


def test_account_serializer(account):
    serializer = serializers.AccountsSerializer(account)
    assert serializer.data == {'address': account.address}

