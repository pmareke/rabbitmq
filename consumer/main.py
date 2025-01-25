from src.consumer import Consumer
from src.logger import Logger
from src.print_resolver import PrintResolver

resolver = PrintResolver()
logger = Logger()
consumer = Consumer(resolver, logger)

consumer.start()
