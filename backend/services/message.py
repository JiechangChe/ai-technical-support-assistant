from sqlalchemy import select
from sqlalchemy.orm import Session

from models.conversation import Conversation
from models.message import Message
from schemas.message import MessageCreate



def create_message(
    db: Session,
    conversation_id: int,
    message: MessageCreate,
):

    #only return if the conversation exist
    statement = select(Conversation).where(
        Conversation.id == conversation_id
    )

    conversation = db.execute(statement).scalar_one_or_none()

    if conversation is None:
        return None

    new_message = Message(
        conversation_id = conversation_id,
        role=message.role,
        content=message.content
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message

def get_messages(
    db: Session,
    conversation_id: int,
):
    conversation_statement = select(Conversation).where(
        Conversation.id == conversation_id
    )

    conversation = db.execute(
        conversation_statement
    ).scalar_one_or_none()
    #return none if no such conversation exist
    if conversation is None: 
        return None

    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )

    result = db.execute(statement)
    return result.scalars().all()