from src.logger import Logger
from src.producer import Producer

logger = Logger()
producer = Producer(logger)

for name in ["Alice", "Bob", "Charlie"]:
    producer.send(f"Hello, {name}!")
