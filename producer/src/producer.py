from logging import Logger

import pika


class Producer:
    QUEUE_NAME = "hello"

    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def send(self, body: str) -> None:
        params = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=self.QUEUE_NAME)
        channel.basic_publish(exchange="", routing_key="hello", body=body)
        self.logger.info(f" [x] Sent 'Hello {body}!'")
        connection.close()
