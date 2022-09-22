import json
import pytest

from service import models

pytestmark = pytest.mark.django_db


class TestTransactionsEndpoint:
    ENDPOINT = '/api/transactions/'

    def test_list(self, api_client, five_transactions):
        response = api_client().get(self.ENDPOINT)
        content = json.loads(response.content)
        assert response.status_code == 200
        assert len(content) == len(five_transactions)
        for num, tx in enumerate(five_transactions):
            assert content[num]['hash'] == tx.hash
            assert content[num]['destination'] == tx.destination.address
            assert content[num]['ledger_index'] == tx.ledger_index

    def test_list_filters(self, api_client, five_transactions, three_transactions_for_second_acc):
        tx_hash = five_transactions[0].hash
        response = api_client().get(self.ENDPOINT, {'hash': tx_hash})
        content = json.loads(response.content)
        assert response.status_code == 200
        assert len(content) == 1
        for tx in content:
            assert tx['hash'] == str(tx_hash)

        ledger_index = three_transactions_for_second_acc[0].ledger_index
        response = api_client().get(self.ENDPOINT, {'ledger_index': ledger_index})
        content = json.loads(response.content)
        assert response.status_code == 200
        assert len(content) == len(three_transactions_for_second_acc)
        for tx in content:
            assert tx['ledger_index'] == ledger_index

    def test_create(self, api_client, account):
        tx_body = {
            'hash': 'WhyDidYouReadThis',
            'ledger_index': 7788,
            'amount': '288',
            'account':'someaccount2',
            'destination': account.address,
            'destinationTag': 12899,
            'fee': 10
        }
        response = api_client().post(self.ENDPOINT, data=tx_body)
        assert response.status_code == 201
        try:
            models.Transactions.objects.get(hash=tx_body['hash'])
        except models.Transactions.DoesNotExist:
            assert False


class TestAccountsEndpoint:
    ENDPOINT = '/api/accounts/'

    def test_list(self, api_client, account, second_account):
        response = api_client().get(self.ENDPOINT)
        content = json.loads(response.content)
        assert response.status_code == 200
        assert len(content) == 2
        assert [acc['address'] for acc in content] == [account.address, second_account.address]

