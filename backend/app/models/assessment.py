import uuid
from datetime import datetime
from pydantic import BaseModel, conlist, validator
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

# Pydantic schema for the assessment request payload
class AssessmentRequest(BaseModel):
    responses: conlist(int, min_length=9, max_length=9)

    @validator('responses', each_item=True)
    def check_response_values(cls, v):
        if not 0 <= v <= 3:
            raise ValueError('Response values must be between 0 and 3')
        return v

# Pydantic schema for the assessment response
class AssessmentResponse(BaseModel):
    total_score: int
    severity: str
    next_steps: str

# SQLAlchemy model for the Assessment
class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    responses = Column(ARRAY(Integer), nullable=False)
    total_score = Column(Integer, nullable=False)
    severity = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
