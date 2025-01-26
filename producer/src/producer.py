from pika import BlockingConnection, ConnectionParameters

from src.logger import Logger


class Producer:
    QUEUE_NAME = "hello"
    DEFAULT_EXCHANGE = ""

    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def send(self, body: str) -> None:
        params = ConnectionParameters(host="rabbitmq")
        connection = BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=self.QUEUE_NAME)
        channel.basic_publish(
            exchange=self.DEFAULT_EXCHANGE,
            routing_key=self.QUEUE_NAME,
            body=body,
        )
        self.logger.info(f" [x] Sent '{body}'")
        connection.close()
