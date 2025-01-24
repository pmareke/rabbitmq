from src.consumer import Consumer
from src.system_printer import SystemPrinter

printer = SystemPrinter()
consumer = Consumer(printer)

consumer.start()
