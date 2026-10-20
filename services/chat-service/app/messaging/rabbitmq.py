import json
from typing import Any
import aio_pika
from aio_pika import DeliveryMode, ExchangeType, Message

from app.core.config import settings


class RabbitMQ:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(settings.rabbitmq_uri,)

        self.channel = await self.connection.channel(publish_confirms=True)

        self.exchange = await self.channel.declare_exchange(
            "chat-events",
            ExchangeType.FANOUT,
            durable=True,
        )

    async def publish(
            self,
            event: dict[str, Any],
    ) -> None:
        if self.exchange is None:
            raise RuntimeError("RabbitMQ is not connected")

        body = json.dumps(event).encode("utf-8")
        await self.exchange.publish(
            Message(
                body=body,
                content_type="application/json",
                delivery_mode=DelleveryMode.PERSISTENT,
            ),
            routing_key="",
        )

    async def close(self) -> None:
        if self.connection is not None:
            await self.connection.close()
