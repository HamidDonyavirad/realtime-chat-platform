from uuid import UUID
from pydantic import BaseModel


class CreateConversationRequest(BaseModel):
    user_id: UUID


class ConversationResponse(BaseModel):
    id: UUID