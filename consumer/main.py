import logging

from src.consumer import Consumer
from src.print_resolver import PrintResolver

resolver = PrintResolver()
logger = logging.getLogger(__name__)
consumer = Consumer(resolver, logger)

consumer.start()
