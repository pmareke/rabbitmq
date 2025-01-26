from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import equal, expect
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from src.consumer import Consumer
from src.logger import Logger
from src.resolver import Resolver


class DummyResolver(Resolver):
    def __init__(self) -> None:
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
    DEFAULT_EXCHANGE = ""

    def test_recieve_a_message(self) -> None:
        message = "Hello, World!"
        resolver = DummyResolver()
        logger = Mimic(Spy, Logger)
        consumer = Consumer(resolver, logger)

        self._send(message)
        consumer.start()

        log_message = " [*] Waiting for messages. To exit press CTRL+C"
        expect(logger.info).to(have_been_called_with(log_message))
        expect(resolver.expected_message).to(equal(message))

    def _send(self, message: str) -> None:
        params = ConnectionParameters(host="rabbitmq")
        connection = BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=Consumer.QUEUE_NAME)
        channel.basic_publish(
            exchange=self.DEFAULT_EXCHANGE,
            routing_key=Consumer.QUEUE_NAME,
            body=message,
        )
        connection.close()
