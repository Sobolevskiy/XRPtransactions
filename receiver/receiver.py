import asyncio
import signal
import logging
from typing import Optional

from xrpl.asyncio.clients import AsyncWebsocketClient

from .managers.redis_manager import RedisManager
from .managers.subscription_manager import SubscriptionManager

logger = logging.getLogger('receiver')


class Receiver:
    """Ресивер получает данные о новых транзакциях и отправляет их в брокер сообщений"""
    TIMEOUT = 10

    def __init__(self, settings):
        self._is_running = False
        self._settings = settings

        self.redis_manager: Optional[RedisManager] = None
        self.subscription_manager: Optional[SubscriptionManager] = None
        self.xrpl_websocket_client: Optional[AsyncWebsocketClient] = None

    async def _xrpl_listener(self, client):
        """Получение сообщений от XRPL, на данный момент используется для отправки сообщений на создание транзакции"""
        async for message in client:
            logger.info(f'Receive XRPL mess: {message}')
            if message.get('type') == 'transaction' and message.get('engine_result') == 'tesSUCCESS':
                # Отправить сообщение на создание транзакции
                logger.info(f'Get payment from XRPL: {message}')
                asyncio.create_task(self.redis_manager.send(message['transaction']))
            elif message.get('type') == 'responce':
                # TODO: добавить переподписку при дисконнекте
                logger.info(f'Get responce from XRPL: {message}')

    async def _redis_listener(self):
        """Слушает сообщения от Редиса, на данный момент используется для подписывания на новые аккаунты"""
        async for message in self.redis_manager:
            if message.get('add'):
                asyncio.create_task(self.subscription_manager.subscribe(message['add']))
            elif message.get('delete'):
                asyncio.create_task(self.subscription_manager.unsubscribe(message['delete']))
            else:
                logger.error(f'Unsupported message type: {message}')

    def process(self):
        self._is_running = True
        asyncio.run(self.run())

    async def run(self):
        """
        Главный процесс работы ресивера, в нем происходит инициализация клиентов для получения данных
        и тасок для их обработки
        """
        logger.info('Start receiver')
        async with AsyncWebsocketClient(self._settings.XRPL_SOCKET_URL) as xrpl_client:
            self._initialize_managers(xrpl_client)

            asyncio.create_task(self._xrpl_listener(xrpl_client))
            await self.subscription_manager.start()
            await self.redis_manager.start()
            asyncio.create_task(self._redis_listener())

            asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, self.stop)
            asyncio.get_event_loop().add_signal_handler(signal.SIGINT, self.stop)
            await self._cycle()

            await self.subscription_manager.stop()
            await self.redis_manager.stop()

        logger.info('Stop receiver')

    def stop(self):
        if self._is_running:
            self._is_running = False

    async def _cycle(self):
        while self._is_running:
            await asyncio.sleep(self.TIMEOUT)

    def _initialize_managers(self, client):
        self.subscription_manager = SubscriptionManager(client=client, service_url=self._settings.WEB_SERVICE_URL)
        self.redis_manager = RedisManager(host=self._settings.REDIS['URL'], port=self._settings.REDIS['PORT'],
                                          queue_in=self._settings.QUEUE_IN, queue_out=self._settings.QUEUE_OUT)
