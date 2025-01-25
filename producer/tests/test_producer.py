from logging import Logger

import pika
from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import equal, expect
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from src.producer import Producer


class TestProducer:
    def test_send_message(self) -> None:
        message = "Hello, World!"
        logger = Mimic(Spy, Logger)
        producer = Producer(logger)

        producer.send(message)
        read_message = self._read_message()

        expect(read_message).to(equal(message))
        log_message = " [x] Sent 'Hello, World!'"
        expect(logger.info).to(have_been_called_with(log_message))

    def _read_message(self) -> str:
        self.message = ""
        params = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=Producer.QUEUE_NAME)

        def _callback(
            channel: BlockingChannel,
            method: Basic.Deliver,
            properties: BasicProperties,
            body: bytes,
        ) -> None:  # type: ignore
            channel.stop_consuming()
            self.message = body.decode()
            connection.close()

        channel.basic_consume(
            queue=Producer.QUEUE_NAME,
            on_message_callback=_callback,
            auto_ack=True,
        )
        channel.start_consuming()
        return self.message
