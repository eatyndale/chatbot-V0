import uuid
from datetime import datetime
from pydantic import BaseModel, Field, conint, constr
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from typing import Annotated

# SQLAlchemy model for a tapping session/log
class TappingSession(Base):
    __tablename__ = "tapping_sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem = Column(String, nullable=False)
    emotion = Column(String, nullable=False)
    body_location = Column(String, nullable=False)
    before_intensity = Column(Integer, nullable=False)
    after_intensity = Column(Integer)
    rounds_completed = Column(Integer, default=1)
    max_rounds_reached = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic schema for session generation request
class TappingGenerateRequest(BaseModel):
    problem: Annotated[str, Field(strip_whitespace=True, min_length=1)]
    emotion: Annotated[str, Field(strip_whitespace=True, min_length=1)]
    body_location: Annotated[str, Field(strip_whitespace=True, min_length=1)]
    intensity: Annotated[int, Field(ge=0, le=10)]

# Pydantic schema for session generation response
class TappingGenerateResponse(BaseModel):
    session_id: uuid.UUID
    setup_statements: list[str]
    tapping_points: dict[str, str]
    before_intensity: int

# Pydantic schema for feedback request
class TappingFeedbackRequest(BaseModel):
    session_id: uuid.UUID
    before_intensity: Annotated[int, Field(ge=0, le=10)]
    after_intensity: Annotated[int, Field(ge=0, le=10)]

# Pydantic schema for feedback response
class TappingFeedbackResponse(BaseModel):
    message: str
    updated_setup_statements: list[str] | None = None
    updated_tapping_points: dict[str, str] | None = None
    rounds_completed: int
    max_rounds_reached: bool

class TappingSessionLog(Base):
    __tablename__ = "tapping_session_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    problem = Column(String, nullable=False)
    before_intensity = Column(Integer, nullable=False)
    after_intensity = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    duration_minutes = Column(Integer, nullable=False)
    number_of_rounds = Column(Integer)

    __table_args__ = (
        Index('ix_tapping_session_logs_user_id', 'user_id'),
        Index('ix_tapping_session_logs_timestamp', 'timestamp'),
    )

class TappingSessionLogResponse(BaseModel):
    problem: str
    before_intensity: int
    after_intensity: int
    timestamp: datetime
    duration_minutes: int
    number_of_rounds: int | None = None

class TappingSessionLogListResponse(BaseModel):
    sessions: list[TappingSessionLogResponse]
