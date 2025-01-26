import logging
import sys


class Logger:
    def __init__(self):
        _pika_logger = logging.getLogger("pika")
        _pika_logger.setLevel(logging.WARNING)

        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def info(self, message: str):
        self.logger.info(message)
