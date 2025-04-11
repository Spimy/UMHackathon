from fastapi import APIRouter, HTTPException, Depends
from models import SessionDep
from schemas.chat import ChatCreate, ChatResponse, MessageBase, MessageResponse
import crud

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
def create_chat(chat: ChatCreate, session: SessionDep):
    return crud.create_chat(session, chat.dict())


@router.get("/{user_email}", response_model=list[ChatResponse])
def get_user_chats(user_email: str, session: SessionDep):
    chats = crud.get_user_chats(session, user_email)
    return [chat[0] for chat in chats]


@router.get("/{chat_id}/messages", response_model=list[MessageResponse])
def get_chat_messages(chat_id: int, session: SessionDep):
    chat = crud.get_chat(session, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    messages = crud.get_chat_messages(session, chat_id)
    return [message[0] for message in messages]


@router.post("/{chat_id}/messages", response_model=MessageResponse)
def add_message(chat_id: int, message: MessageBase, session: SessionDep):
    chat = crud.get_chat(session, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    message_data = message.model_dump()
    message_data["chat_id"] = chat_id
    return crud.add_message(session, message_data)
