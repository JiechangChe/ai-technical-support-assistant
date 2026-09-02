from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.message import (
    MessageCreate,
    MessageResponse,
)
from services.message import (
    create_message,
    get_messages,
)
router = APIRouter(
    prefix="/conversations/{conversation_id}/messages",
    tags=["messages"],
)

@router.post(
    "/",
    response_model=MessageResponse,
)
def create_message_endpoint(
    conversation_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
):
    message = create_message(
        db=db,
        conversation_id=conversation_id,
        message=message,
    )

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )
    return message

@router.get(
    "/",
    response_model=list[MessageResponse],
)
def get_messages_endpoint(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    messages = get_messages(
        db=db,
        conversation_id=conversation_id,
    )

    if messages is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return messages