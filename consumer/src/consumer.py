from typing import Callable

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from src.printer import Printer


class Consumer:
    _QUEUE_NAME = "hello"

    def __init__(self, printer: Printer) -> None:
        self.printer = printer
        self.channel = self._create_channel()

    def _create_channel(self) -> BlockingChannel:
        params = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=self._QUEUE_NAME)
        channel.basic_consume(
            queue=self._QUEUE_NAME,
            on_message_callback=self._callback(),
            auto_ack=True,
        )
        return channel

    def start(self) -> None:
        self.channel.start_consuming()

    def _callback(self) -> Callable:
        def _func(
            channel: BlockingChannel,
            method: Basic.Deliver,
            props: BasicProperties,
            body: bytes,
        ) -> None:
            payload = body.decode()
            self.printer.print(channel, method, props, payload)

        return _func
