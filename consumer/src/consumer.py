from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from src.logger import Logger
from src.resolver import Resolver


class Consumer:
    QUEUE_NAME = "hello"

    def __init__(self, resolver: Resolver, logger: Logger) -> None:
        self.resolver = resolver
        self.logger = logger

    def start(self) -> None:
        channel = self._create_channel()
        channel.start_consuming()

    def _create_channel(self) -> BlockingChannel:
        params = ConnectionParameters(host="rabbitmq")
        connection = BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=self.QUEUE_NAME)
        channel.basic_consume(
            queue=self.QUEUE_NAME,
            on_message_callback=self._callback,
            auto_ack=True,
        )
        self.logger.info(" [*] Waiting for messages. To exit press CTRL+C")
        return channel

    def _callback(
        self,
        channel: BlockingChannel,
        method: Basic.Deliver,
        props: BasicProperties,
        body: bytes,
    ) -> None:
        payload = body.decode()
        self.resolver.resolve(channel, method, props, payload)
