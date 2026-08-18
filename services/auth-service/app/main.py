from fastapi import FastAPI

app = FastAPI(title="Auth Service",version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "ok"}