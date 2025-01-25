from src.consumer import Consumer
from src.print_resolver import PrintResolver

resolver = PrintResolver()
consumer = Consumer(resolver)

consumer.start()
