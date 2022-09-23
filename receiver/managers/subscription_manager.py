import logging
from aiohttp import ClientSession
from aiohttp.http_exceptions import HttpProcessingError
from aiohttp.client_exceptions import ClientError

from xrpl.models import Subscribe, Unsubscribe
from aioretry import retry

logger = logging.getLogger('xrpl_client')


class SubscriptionManager:
    RETRYS = 3

    def __init__(self, client, service_url):
        self.client = client
        self.service_url = service_url

        self.subscriptions = dict()

    async def start(self):
        """
        Начало получения данных
        - Получаем все аккаунты
        - Подписываемся на них
        """
        logger.info('Start listen XRPL')
        all_accounts = await self._get_all_accounts()
        await self.subscribe(all_accounts)

    async def stop(self):
        logger.info('Stop listen XRPL')
        await self.unsubscribe(list(self.subscriptions.keys()))

    async def subscribe(self, account):
        """Подписка на указанные аккаунты"""
        logger.info(f'Subscribe to accs: {account}')
        if not isinstance(account, list):
            account = [str(account)]
        account = self._get_unsub_accs(account)
        if not account:
            return
        await self._send_sub_message(account)

        self._add_accounts_to_subscriptoins(account)

    async def unsubscribe(self, account):
        """Отписка от аккаунтов, которые удалены"""
        logger.info(f'Unsubscribe to accs: {account}')
        if not isinstance(account, list):
            account = [account]
        if not self._get_unsub_accs(account):
            await self._send_unsub_message(account)
            self._remove_accounts_from_subscriptions(account)

    @retry('_retry_policy')
    async def _get_all_accounts(self):
        """Обращение к джанго сервису для получения аккаунтов, по которым надо получать данные"""
        async with ClientSession(trust_env=True) as session:
            async with session.get(self.service_url) as responce:
                responce_data = await responce.json()
                logger.info(f'Receive new accounts: {responce_data}')

        return [acc['address'] for acc in responce_data]

    def _add_accounts_to_subscriptoins(self, accounts):
        for account in accounts:
            self.subscriptions[account] = True

    def _remove_accounts_from_subscriptions(self, accounts):
        for account in accounts:
            del self.subscriptions[account]

    async def _send_sub_message(self, accounts):
        await self.client.send(Subscribe(
            accounts=accounts
        ))

    async def _send_unsub_message(self, accounts):
        await self.client.send(Unsubscribe(
            accounts=accounts,
        ))

    def _get_unsub_accs(self, accounts):
        """Получение списка аккаунтов, которых ещё нет в подписках"""
        return list(filter(lambda i: i not in list(self.subscriptions.keys()), accounts))

    def _retry_policy(self, info):
        logger.error(f"Retry subscription manager function with error: {info.exception}")
        if not isinstance(info.exception, (HttpProcessingError, ClientError)):
            return True, 0

        return info.fails > self.RETRYS, info.fails * 0.1
