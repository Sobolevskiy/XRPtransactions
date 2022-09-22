import json

import pytest
from django.conf import settings

from service import models

pytestmark = pytest.mark.django_db


class TestAccountsModel:

    def test_account_creation_signal(self, mocker, redis_client):
        model = models.AccountAddress.objects.create(address='MyPrettyName')
        mocker.patch('service.tasks.actualize_account.apply_async').return_value = None
        data = redis_client.rpop(settings.REDIS['OUT_QUEUE'])
        assert json.loads(data) == {"add": model.address}

    def test_account_delete_signal(self, redis_client):
        model = models.AccountAddress.objects.create(address='NewnameForTest')
        model.delete()
        data = redis_client.rpop(settings.REDIS['OUT_QUEUE'])
        assert json.loads(data) == {"delete": model.address}



