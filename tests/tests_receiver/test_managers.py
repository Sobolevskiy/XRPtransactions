from unittest.mock import AsyncMock

import pytest

from receiver.managers.subscription_manager import SubscriptionManager


class TestSubscriptionManager:
    def test_get_unsub_accs(self):
        manager = SubscriptionManager(None, None)
        manager.subscriptions = {'ac1': True, 'ac2': True}
        unsub_accs = ['ac2', 'ac3']
        result = manager._get_unsub_accs(unsub_accs)
        assert result == ['ac3']

    @pytest.mark.asyncio
    async def test_subscribe(self, mocker):
        mocker.patch('receiver.managers.subscription_manager.SubscriptionManager._send_sub_message',
                     side_effect=AsyncMock(return_value=None))
        manager = SubscriptionManager(None, None)
        sub_accs = ['ac1', 'ac2', 'ac3']
        await manager.subscribe(sub_accs)
        assert manager.subscriptions == {name: True for name in sub_accs}
        new_accs = ['ac4']
        await manager.subscribe(new_accs)
        assert manager.subscriptions == {name: True for name in sub_accs + new_accs}

    @pytest.mark.asyncio
    async def test_unsubscribe(self, mocker):
        mocker.patch('receiver.managers.subscription_manager.SubscriptionManager._send_sub_message',
                     side_effect=AsyncMock(return_value=None))
        mocker.patch('receiver.managers.subscription_manager.SubscriptionManager._send_unsub_message',
                     side_effect=AsyncMock(return_value=None))
        manager = SubscriptionManager(None, None)
        accs = ['ac1', 'ac2', 'ac3']
        await manager.subscribe(accs)
        await manager.unsubscribe(accs)
        assert manager.subscriptions == {}
