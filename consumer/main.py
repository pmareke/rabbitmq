from src.consumer import Consumer
from src.printer import Printer

printer = Printer()
consumer = Consumer(printer)
consumer.start()
