from pika import BasicProperties
from pika.spec import Basic, Channel

from src.consumer import Consumer


def printer(
    channel: Channel,
    method: Basic.Deliver,
    props: BasicProperties,
    body: str,
) -> None:
    print(body)


consumer = Consumer(printer)
consumer.start()
