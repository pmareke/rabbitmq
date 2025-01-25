import logging

from src.producer import Producer

logger = logging.getLogger(__name__)
producer = Producer(logger)

for name in ["Alice", "Bob", "Charlie"]:
    producer.send(f"Hello, {name}!")
