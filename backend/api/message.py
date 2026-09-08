from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.database import get_db
from models.message import Message
from schemas.message import MessageCreate, MessageResponse, ChatResponse
from services.message import create_message
from services.message import create_message


router = APIRouter(
    prefix="/conversations/{conversation_id}/messages",
    tags=["messages"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
def create_message_endpoint(
    conversation_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
):
    result = create_message(
        db=db,
        conversation_id=conversation_id,
        message=message,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    user_message, assistant_message = result

    return ChatResponse(
        user_message=user_message,
        assistant_message=assistant_message,
    )

@router.get("/", response_model=list[MessageResponse])
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )

    messages = db.execute(statement).scalars().all()

    return messages