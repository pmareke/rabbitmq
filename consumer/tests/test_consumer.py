import pika
from expects import equal, expect
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from src.consumer import Consumer


class DummyPrinter:
    def __init__(self, message: str) -> None:
        self.message = message

    def print(
        self,
        channel: BlockingChannel,
        _method: Basic.Deliver,
        _props: BasicProperties,
        recieved_message: str,
    ) -> None:
        expect(self.message).to(equal(recieved_message))
        channel.stop_consuming()


class TestConsumer:
    def test_recieve_a_message(self) -> None:
        message = "Hello, World!"
        printer = DummyPrinter(message)
        consumer = Consumer(printer)  # type: ignore
        self._send_command(message)
        consumer.start()

    def _send_command(self, message: str) -> None:
        params = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue="hello")
        channel.basic_publish(exchange="", routing_key="hello", body=message)
        connection.close()
