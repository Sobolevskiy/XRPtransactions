import json
import logging

from django.conf import settings

import redis

logger = logging.getLogger('default')


def send_message(message):
    with redis.Redis(settings.REDIS['HOST'], port=settings.REDIS['PORT']) as client:
        message = json.dumps(message)
        client.rpush('accounts', message)


class RedisWorker:
    TIMEOUT = 5
    ENCODING = 'utf-8'

    def __init__(self, client, queue_name):
        self.is_running = True
        self.client = client
        self.queue_name = queue_name

    def __iter__(self):
        while self.is_running:
            message = self._pop_message()
            if message is not None:
                yield self._decode_message(message)

    def _pop_message(self):
        return self.client.blpop(self.queue_name, self.TIMEOUT)

    @staticmethod
    def _decode_message(message):
        return json.loads(message[1])

