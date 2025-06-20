from sqlalchemy.orm import Session
import uuid
from typing import List, Dict
from app.models.chat import Conversation, ChatMessage

def get_or_create_conversation(db: Session, user_id: int, conversation_id: uuid.UUID = None) -> Conversation:
    if conversation_id:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == user_id).first()
        if conversation:
            return conversation
    
    # If no conversation_id or not found, create a new one
    new_conversation = Conversation(user_id=user_id)
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    return new_conversation

def get_conversation_history(db: Session, conversation_id: uuid.UUID) -> List[Dict[str, str]]:
    history = (
        db.query(ChatMessage)
        .filter(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at)
        .all()
    )
    return [{"role": msg.role, "content": msg.content} for msg in history]

def add_message_to_history(db: Session, conversation_id: uuid.UUID, role: str, content: str):
    new_message = ChatMessage(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message 