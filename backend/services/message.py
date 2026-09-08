from sqlalchemy import select
from sqlalchemy.orm import Session

from models.conversation import Conversation
from models.message import Message
from schemas.message import MessageCreate
from services.ai import generate_response


def create_message(
    db: Session,
    conversation_id: int,
    message: MessageCreate,
):
    # 1. Check whether the conversation exists
    statement = select(Conversation).where(
        Conversation.id == conversation_id
    )

    conversation = db.execute(statement).scalar_one_or_none()

    if conversation is None:
        return None

    # 2. Save the user's message
    user_message = Message(
        conversation_id=conversation_id,
        role="user",
        content=message.content,
    )

    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # 3. Get conversation history
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )

    history = db.execute(statement).scalars().all()

    # 4. Convert database messages into LLM messages
    llm_messages = [
        {
            "role": msg.role,
            "content": msg.content,
        }
        for msg in history
    ]

    # 5. Generate AI response
    answer = generate_response(llm_messages)

    # 6. Save assistant message
    assistant_message = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=answer,
    )

    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return user_message, assistant_message

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