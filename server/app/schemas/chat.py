from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MessageBase(BaseModel):
    text: Optional[str] = None
    is_sent: bool
    image: Optional[str] = None


class MessageResponse(MessageBase):
    id: int
    chat_id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class ChatBase(BaseModel):
    name: str
    user_email: str


class ChatCreate(ChatBase):
    pass


class ChatResponse(ChatBase):
    id: int
    created_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        orm_mode = True
