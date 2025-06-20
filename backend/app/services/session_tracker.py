from sqlalchemy.orm import Session
from datetime import datetime
from app.models.tapping_log import TappingSessionLog

def log_tapping_session(
    db: Session,
    user_id: int,
    problem: str,
    before_intensity: int,
    after_intensity: int,
    duration_minutes: int,
    number_of_rounds: int = None,
    timestamp: datetime = None
):
    log = TappingSessionLog(
        user_id=user_id,
        problem=problem,
        before_intensity=before_intensity,
        after_intensity=after_intensity,
        duration_minutes=duration_minutes,
        number_of_rounds=number_of_rounds,
        timestamp=timestamp or datetime.utcnow()
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
