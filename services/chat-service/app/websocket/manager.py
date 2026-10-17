from uuid import UUID
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID, set[WebSocket]] = {}
        self.conversation_connections: dict[UUID, set[UUID]] = {}

    async def connect(self,user_id: UUID,websocket: WebSocket,) -> None:
        await websocket.accept()
        self.active_connections.setdefault(user_id, set()).add(websocket)


    def disconnect(self,user_id: UUID,websocket: WebSocket,) -> None:
        connections = self.active_connections.get(user_id)

        if connections is not None:
            connections.discard(websocket)

            if not connections:
                self.active_connections.pop(user_id, None)

        for conversation_id, users in list(self.conversation_connections.items()):
            if user_id not in users:
                continue
            still_connected = any(conn is not websocket for conn in connections or set())

            if not still_connected:
                users.discard(user_id)

            if not users:
                self.conversation_connections.pop(conversation_id, None)

    def join_conversation(self,conversation_id: UUID,user_id: UUID,) -> None:
        self.conversation_connections.setdefault(conversation_id, set()).add(user_id)

    def leave_conversation(self,conversation_id: UUID,user_id: UUID,) -> None:
        users = self.conversation_connections.get(conversation_id)

        if users is not None:
            users.discard(user_id)

            if not users:
                self.conversation_connections.pop(conversation_id, None)

    async def send_to_user(self,user_id: UUID,message: dict,) -> None:
        for websocket in list(self.active_connections.get(user_id, set())):
            try:
                await websocket.send_json(message)
            except Exception:
                self.disconnect(user_id, websocket)

    async def broadcast_to_conversation(self,conversation_id: UUID,message: dict,exclude_user_id: UUID | None = None,
    ) -> None:
        for user_id in list(self.conversation_connections.get(conversation_id, set())):
            if user_id == exclude_user_id:
                continue

            await self.send_to_user(user_id, message)


manager = ConnectionManager()
