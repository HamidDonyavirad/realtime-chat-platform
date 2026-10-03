from fastapi import FastAPI

from app.api.v1.conversations import router

app = FastAPI(title="Chat Service",version="1.0.0",)


app.include_router(router,prefix="/api/v1",tags=["chat-service"])


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}