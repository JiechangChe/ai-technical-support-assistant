from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from fastapi import APIRouter, Depends, HTTPException

from schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
)

from services.conversation import (
    create_conversation,
    get_conversations as get_conversations_service,
    get_conversation as get_conversation_service,
)


router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)


@router.post(
    "/",
    response_model=ConversationResponse,
)
def create_conversation_endpoint(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
):
    return create_conversation(
        db=db,
        conversation=conversation,
    )


@router.get(
    "/",
    response_model=list[ConversationResponse],
)
def get_conversations(
    db: Session = Depends(get_db),
):
    return get_conversations_service(db)

@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    conversation = get_conversation_service(
        db=db,
        conversation_id=conversation_id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return conversation