from uuid import UUID
from fastapi import Websocket


class ConnectionManager:
    def __init__(self):
        self.active_connections : dict [UUID,Websocket] = {}

    async def connect(self,user_id:UUID,websocket:Websocket)->None:
        await websocket.accept()
        self.active_connections[user_id] = websockets

    def disconnect(self,user_id:UUID)->None:
        self.active_connections.pop(user_id, None)

    async def send_to_user(self,user_id:UUID,message:dict)->None:
        websocket = self.active_connections.get(user_id)

        if websocket is not None:
            await websocket.send_json(message)

