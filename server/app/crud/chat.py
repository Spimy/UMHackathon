from sqlmodel import col, select
from models import SessionDep
from models.chat import Chat, Message
from typing import List, Optional
from schemas.chat import MessageBase


def create_chat(session: SessionDep, chat_data: dict) -> Chat:
    db_chat = Chat(**chat_data)
    session.add(db_chat)
    session.commit()
    session.refresh(db_chat)
    return db_chat


def get_user_chats(session: SessionDep, user_email: str) -> List[Chat]:
    statement = select(Chat).where(
        Chat.user_email == user_email
    ).order_by(Chat.created_at.desc())
    return session.execute(statement).all()


def get_chat(session: SessionDep, chat_id: int) -> Optional[Chat]:
    statement = select(Chat).where(Chat.id == chat_id)
    return session.execute(statement).first()


def add_message(session: SessionDep, message_data: MessageBase) -> Message:
    db_message = Message(**message_data)
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message


def get_chat_messages(session: SessionDep, chat_id: int) -> List[Message]:
    statement = select(Message).where(
        Message.chat_id == chat_id
    ).order_by(col(Message.timestamp).asc())
    return session.execute(statement).all()
