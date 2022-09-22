import asyncio
import logging

from .receiver import Receiver
from . import settings


def initializing():
    logging.basicConfig(level=settings.LOGGING_LEVEL)


def main():
    initializing()
    receiver = Receiver(settings=settings)
    receiver.process()


if __name__ == "__main__":
    main()
