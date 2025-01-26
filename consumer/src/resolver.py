from abc import ABC, abstractmethod

from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic


class Resolver(ABC):
    @abstractmethod
    def resolve(
        self,
        channel: BlockingChannel,
        method: Basic.Deliver,
        props: BasicProperties,
        body: str,
    ) -> None:
        raise NotImplementedError
