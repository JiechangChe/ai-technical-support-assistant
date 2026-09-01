from sqlalchemy.orm import Session
from sqlalchemy import select

from models.conversation import Conversation
from schemas.conversation import ConversationCreate

#save a conversation session in the database
def create_conversation(
    db: Session,
    conversation: ConversationCreate,
):
    new_conversation = Conversation(
        title=conversation.title
    )

    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)

    return new_conversation

#get all conversations
def get_conversations(db: Session):
    statement = select(Conversation).order_by(
        Conversation.created_at.desc()
    )

    result = db.execute(statement)

    return result.scalars().all()

#get conversation by id
def get_conversation(
    db: Session,
    conversation_id: int,
):
    statement = select(Conversation).where(
        Conversation.id == conversation_id
    )

    result = db.execute(statement)

    return result.scalar_one_or_none()