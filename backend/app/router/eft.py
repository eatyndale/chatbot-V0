from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User as UserModel
from app.services import auth_service, tapping_script_generator
from app.models.tapping_log import (
    TappingSession, TappingGenerateRequest, TappingGenerateResponse,
    TappingFeedbackRequest, TappingFeedbackResponse
)
import uuid

router = APIRouter(
    prefix="/eft",
    tags=["EFT"]
)

MAX_ROUNDS = 3

@router.post("/generate", response_model=TappingGenerateResponse)
def generate_tapping(
    request: TappingGenerateRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(auth_service.get_current_user)
):
    # Validate input (Pydantic does most of this)
    if not (0 <= request.intensity <= 10):
        raise HTTPException(status_code=422, detail="Intensity must be between 0 and 10.")
    # Generate statements
    setup_statements, tapping_points = tapping_script_generator.generate_tapping_session(
        request.problem, request.emotion, request.body_location, request.intensity
    )
    # Store session
    session = TappingSession(
        user_id=current_user.id,
        problem=request.problem,
        emotion=request.emotion,
        body_location=request.body_location,
        before_intensity=request.intensity,
        rounds_completed=1,
        max_rounds_reached=False
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return TappingGenerateResponse(
        session_id=session.id,
        setup_statements=setup_statements,
        tapping_points=tapping_points,
        before_intensity=request.intensity
    )

@router.post("/feedback", response_model=TappingFeedbackResponse)
def tapping_feedback(
    request: TappingFeedbackRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(auth_service.get_current_user)
):
    # Validate input
    if not (0 <= request.before_intensity <= 10) or not (0 <= request.after_intensity <= 10):
        raise HTTPException(status_code=422, detail="Intensity must be between 0 and 10.")
    session = db.query(TappingSession).filter(
        TappingSession.id == request.session_id,
        TappingSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    # Update session
    session.after_intensity = request.after_intensity
    session.rounds_completed += 1
    session.updated_at = session.updated_at  # triggers onupdate
    # Check if max rounds reached
    max_rounds = session.rounds_completed >= MAX_ROUNDS
    session.max_rounds_reached = max_rounds
    db.commit()
    # Feedback logic
    if request.after_intensity == 0:
        return TappingFeedbackResponse(
            message="Congratulations! Your intensity is now zero. You may end the session or continue for reinforcement.",
            rounds_completed=session.rounds_completed,
            max_rounds_reached=max_rounds
        )
    elif max_rounds:
        return TappingFeedbackResponse(
            message="You have completed the maximum number of guided rounds. Would you like to continue or stop?",
            rounds_completed=session.rounds_completed,
            max_rounds_reached=True
        )
    else:
        # Generate updated statements with STILL phrasing
        setup_statements, tapping_points = tapping_script_generator.generate_tapping_session(
            session.problem, session.emotion, session.body_location, request.after_intensity, still=True
        )
        return TappingFeedbackResponse(
            message="Let's do another round. Here are updated setup and reminder statements.",
            updated_setup_statements=setup_statements,
            updated_tapping_points=tapping_points,
            rounds_completed=session.rounds_completed,
            max_rounds_reached=False
        )
