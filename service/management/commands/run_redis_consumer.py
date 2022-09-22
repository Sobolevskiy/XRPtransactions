import logging

import redis
from django.core.management.base import BaseCommand
from django.conf import settings

from service.redis_management import RedisWorker
from service import tasks

logging.basicConfig(level="INFO")
logger = logging.getLogger('default')


class Command(BaseCommand):

    def handle(self, *args, **options):
        logger.info('Starting redis consumer')
        try:
            with redis.Redis(settings.REDIS['HOST'], port=settings.REDIS['PORT']) as redis_cli:
                for message in RedisWorker(redis_cli, settings.REDIS['IN_QUEUE']):
                    logger.info(f'Receive message from Redis: {message}')
                    tasks.process_payment.apply_async(args=[message])
        except Exception as e:
            redis_cli.close()
            logger.error(f'Error while running redis consumer: {e}')
            raise e
