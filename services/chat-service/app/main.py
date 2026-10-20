from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.conversations import router as conversations_router
from app.api.v1.websocket import router as websocket_router
from app.messaging.rabbitmq import RabbitMQ


app = FastAPI(title="Chat Service",version="1.0.0",)


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbitmq = RabbitMQ()
    await rabbitmq.connect()

    app.state.rabbitmq = rabbitmq

    try:
        yield
    finally:
        await rabbitmq.close()

app.include_router(conversations_router,prefix="/api/v1",tags=["chat-service"])
app.include_router(websocket_router,prefix="/api/v1",tags=["chat-service"])


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}