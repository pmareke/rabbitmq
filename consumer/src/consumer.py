import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from src.resolver import Resolver


class Consumer:
    QUEUE_NAME = "hello"

    def __init__(self, resolver: Resolver) -> None:
        self.resolver = resolver
        self.channel = self._create_channel()

    def _create_channel(self) -> BlockingChannel:
        params = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=self.QUEUE_NAME)
        channel.basic_consume(
            queue=self.QUEUE_NAME,
            on_message_callback=self._callback,
            auto_ack=True,
        )
        return channel

    def start(self) -> None:
        self.channel.start_consuming()

    def _callback(
        self,
        channel: BlockingChannel,
        method: Basic.Deliver,
        props: BasicProperties,
        body: bytes,
    ) -> None:
        payload = body.decode()
        self.resolver.resolve(channel, method, props, payload)
