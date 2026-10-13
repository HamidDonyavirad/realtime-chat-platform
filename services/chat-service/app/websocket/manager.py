from uuid import UUID
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID, WebSocket] = {}

        self.conversation_connections: dict[UUID,set[UUID],] = {}

    async def connect(self,user_id: UUID,websocket: WebSocket,) -> None:
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self,user_id: UUID,) -> None:
        self.active_connections.pop(user_id,None,)

        for users in self.conversation_connections.values():
            users.discard(user_id)

    def join_conversation(self,conversation_id: UUID,user_id: UUID,) -> None:
        if conversation_id not in self.conversation_connections:
            self.conversation_connections[conversation_id] = set()

        self.conversation_connections[conversation_id].add(user_id)

    def leave_conversation(self,conversation_id: UUID,user_id: UUID,) -> None:
        users = self.conversation_connections.get(conversation_id)

        if users is None:
            return

        users.discard(user_id)

        if not users:
            self.conversation_connections.pop(conversation_id,None,)

    async def send_to_user(self,user_id: UUID,message: dict,) -> None:
        websocket = self.active_connections.get(user_id)

        if websocket is not None:
            await websocket.send_json(message)

    async def broadcast_to_conversation(
            self,
            conversation_id: UUID,
            message: dict,
            exclude_user_id: UUID | None = None,
    ) -> None:
        users = self.conversation_connections.get(conversation_id,set(),)

        for user_id in users:
            if user_id == exclude_user_id:
                continue

            websocket = self.active_connections.get(user_id)

            if websocket is not None:
                await websocket.send_json(message)