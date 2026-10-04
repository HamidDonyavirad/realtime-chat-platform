from fastapi import FastAPI

from app.api.v1.conversations import router as conversations_router
from app.api.v1.websocket import router as websocket_router

app = FastAPI(title="Chat Service",version="1.0.0",)


app.include_router(conversations_router,prefix="/api/v1",tags=["chat-service"])
app.include_router(websocket_router,prefix="/api/v1",tags=["chat-service"])


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}