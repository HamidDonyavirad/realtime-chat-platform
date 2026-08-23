from fastapi import FastAPI

from app.api.v1.auth import router 

app = FastAPI(title="Auth Service",version="1.0.0")


app.include_router(router,prefix="/api/v1/auth",tags=["authentication"])



@app.get("/health")
async def health_check():
    return {"status": "ok"}