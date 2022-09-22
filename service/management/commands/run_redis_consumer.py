import logging

import redis
from django.core.management.base import BaseCommand
from django.conf import settings

from service.redis_management import RedisWorker
from service import tasks

logger = logging.getLogger('default')


class Command(BaseCommand):

    def handle(self, *args, **options):
        with redis.Redis(settings.REDIS['HOST'], port=settings.REDIS['PORT']) as redis_cli:
            for message in RedisWorker(redis_cli, 'payments'):
                logger.info(f'Receive message from Redis: {message}')
                tasks.process_payment.apply_async(args=[message])
