from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.manager import ConnectionManager

router = APIRouter()

@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            await websocket.send_json({
                "type" : "echo",
                "data" : data,
            })

    except WebSocketDisconnect:
        pass