from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.user import User as UserModel
from app.services import auth_service
from app.models.tapping_log import TappingSessionLog, TappingSessionLogListResponse, TappingSessionLogResponse

router = APIRouter(
    prefix="/progress",
    tags=["Progress"]
)

@router.get("/", response_model=TappingSessionLogListResponse)
def get_progress(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(auth_service.get_current_user),
    start_date: str = Query(None, description="YYYY-MM-DD"),
    end_date: str = Query(None, description="YYYY-MM-DD")
):
    query = db.query(TappingSessionLog).filter(TappingSessionLog.user_id == current_user.id)
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(TappingSessionLog.timestamp >= start_dt)
        except ValueError:
            pass
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(TappingSessionLog.timestamp <= end_dt)
        except ValueError:
            pass
    logs = query.order_by(TappingSessionLog.timestamp.desc()).all()
    sessions = [
        TappingSessionLogResponse(
            problem=log.problem,
            before_intensity=log.before_intensity,
            after_intensity=log.after_intensity,
            timestamp=log.timestamp,
            duration_minutes=log.duration_minutes,
            number_of_rounds=log.number_of_rounds
        ) for log in logs
    ]
    return TappingSessionLogListResponse(sessions=sessions)
