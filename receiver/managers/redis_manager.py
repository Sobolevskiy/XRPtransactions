import asyncio
import logging
import json

import redis

logger = logging.getLogger('redis')


class RedisManager:
    TIMEOUT = 2
    ENCODING = 'utf-8'

    def __init__(self, host, port, queue_in, queue_out):
        self.is_open = False
        self.client = redis.Redis(host, port=port)
        self.queue_in = queue_in
        self.queue_out = queue_out

    async def start(self):
        self.is_open = True

    async def stop(self):
        self.is_open = False
        self.client.close()

    async def send(self, message):
        if not isinstance(message, (str, int, float, bool)):
            message = json.dumps(message)
        self.client.rpush(self.queue_out, message)
        logger.info(f'Send message to redis: {message}')

    async def __aiter__(self):
        while self.is_open:
            message = await self._pop_message()
            if message is not None:
                decoded_message = self._decode_message(message)
                logger.info(f'Get message from redis: {decoded_message}')
                yield decoded_message
            await asyncio.sleep(self.TIMEOUT)
        self.client.close()

    def _decode_message(self, message):
        """Преобразует формат редиса к dict"""
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            message.decode(self.ENCODING)

        if not isinstance(message, dict):
            message = {"message": message}
        return message

    async def _pop_message(self):
        return self.client.rpop(self.queue_in)
