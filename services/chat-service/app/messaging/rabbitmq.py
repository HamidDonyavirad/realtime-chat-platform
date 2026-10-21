import json
from collection.abc import Awaitable, Callable
from typing import Any
import aio_pika
from aio_pika import DeliveryMode, ExchangeType, Message
from aio_pika.abc import AbstractIncomingMessage

from app.core.config import settings


class RabbitMQ:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None
        self.queue = None
        self.consumer_tag = None

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(settings.rabbitmq_uri,)

        self.channel = await self.connection.channel(publish_confirms=True)

        self.exchange = await self.channel.declare_exchange(
            "chat-events",
            ExchangeType.FANOUT,
            durable=True,
        )

    async def publish(self,event: dict[str, Any],) -> None:
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

    async def start_consumer(self, handler: EventHandler) -> None:
        if self.channel is None or self.exchange is None:
            raise RuntimeError("RabbitMQ is not connected")

        self.queue = await self.channel.declare_queue(
            name = "",
            durable = False,
            exclusive = True,
            auto_delete = True,
        )
        await self.queue.bind(self.exchange)

        async def on_message(message: AbstractIncomingMessage) -> None:
            async with message.process():
                event = json.loads(message.body.decode("utf-8"))
                await handler(event)

        self.consumer_tag = await self.queue.consume(on_message)



    async def close(self) -> None:
        if (
            self.queue is not None
            and self.consumer_tag is not None
        ):
            await self.queue.cancel(self.consumer_tag)

        if self.connection is not None:
            await self.connection.close()