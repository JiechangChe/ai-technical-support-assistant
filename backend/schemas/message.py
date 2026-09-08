from datetime import datetime

from pydantic import BaseModel

#database model for message 
class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class ChatResponse(BaseModel):
    user_message: MessageResponse
    assistant_message: MessageResponse