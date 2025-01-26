from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from src.resolver import Resolver


class PrintResolver(Resolver):
    def resolve(
        self,
        channel: BlockingChannel,
        method: Basic.Deliver,
        props: BasicProperties,
        body: str,
    ) -> None:
        print(body)
