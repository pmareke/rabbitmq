import pika
from expects import equal, expect
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from src.consumer import Consumer
from src.resolver import Resolver


class DummyResolver(Resolver):
    def __init__(self, message: str) -> None:
        self.message = message
        self.expect_message = ""

    @property
    def expected_message(self) -> str:
        return self.expect_message

    def resolve(
        self,
        channel: BlockingChannel,
        method: Basic.Deliver,
        props: BasicProperties,
        body: str,
    ) -> None:
        self.expect_message = body
        channel.stop_consuming()


class TestConsumer:
    def test_recieve_a_message(self) -> None:
        message = "Hello, World!"
        resolver = DummyResolver(message)
        consumer = Consumer(resolver)

        self._send_command(message)
        consumer.start()

        expect(resolver.expected_message).to(equal(message))

    def _send_command(self, message: str) -> None:
        params = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=Consumer.QUEUE_NAME)
        channel.basic_publish(
            exchange="",
            routing_key=Consumer.QUEUE_NAME,
            body=message,
        )
        connection.close()
