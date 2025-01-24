import pika
from expects import equal, expect
from pika.channel import BlockingChannel
from pika.spec import Basic, BasicProperties

from src.producer import Producer


class TestProducer:
    def test_send_message(self) -> None:
        message = "Hello, World!"
        producer = Producer()

        producer.send(message)

        self._send_and_read_message(message)

    def _send_and_read_message(self, message: str) -> None:
        params = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue="hello")

        def _callback(
            channel: BlockingChannel,
            method: Basic.Deliver,
            properties: BasicProperties,
            body: bytes,
        ) -> None:  # type: ignore
            channel.stop_consuming()
            expect(message).to(equal(body.decode()))
            connection.close()

        channel.basic_consume(
            queue="hello", on_message_callback=_callback, auto_ack=True
        )
        channel.start_consuming()
