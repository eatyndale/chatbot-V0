import uuid
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

# Pydantic schema for chat message request
class ChatMessageRequest(BaseModel):
    message: str
    conversation_id: uuid.UUID | None = None

# Pydantic schema for chat message response
class ChatMessageResponse(BaseModel):
    reply: str
    conversation_id: uuid.UUID

# SQLAlchemy model for a conversation
class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# SQLAlchemy model for a chat message
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow) 