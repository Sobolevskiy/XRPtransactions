import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from service import models

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def account():
    return mixer.blend(models.AccountAddress, address='IKnowYouReadThis')


@pytest.fixture
def second_account():
    return mixer.blend(models.AccountAddress, address='ThankYouForYourTime')


@pytest.fixture
def five_transactions(account):
    return mixer.cycle(5).blend(models.Transactions,
                                hash=(count for count in range(5)),
                                ledger_index=13883,
                                amount="1278",
                                account='someaccount',
                                destination=account,
                                destinationTag=1757,
                                fee=12
                                )


@pytest.fixture
def three_transactions_for_second_acc(second_account):
    return mixer.cycle(3).blend(models.Transactions,
                                hash=(count for count in range(7, 10)),
                                ledger_index=1677,
                                amount="288",
                                account='someaccount2',
                                destination=second_account,
                                destinationTag=81299,
                                fee=11
                                )
