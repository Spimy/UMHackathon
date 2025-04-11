from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class Chat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user_email: str
    messages: List["Message"] = Relationship(back_populates="chat")


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: Optional[str] = None
    is_sent: bool
    image: Optional[str] = Field(default=None, max_length=255)
    timestamp: datetime = Field(default_factory=datetime.now)

    chat_id: Optional[int] = Field(default=None, foreign_key="chat.id")
    chat: Optional[Chat] = Relationship(back_populates="messages")
