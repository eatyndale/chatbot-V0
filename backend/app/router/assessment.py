from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User as UserModel
from app.services import auth_service, anxiety_scoring
from app.models.assessment import Assessment, AssessmentRequest, AssessmentResponse

router = APIRouter(
    prefix="/assessment",
    tags=["Assessment"]
)

@router.post("/submit", response_model=AssessmentResponse)
def submit_assessment(
    request: AssessmentRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(auth_service.get_current_user)
):
    try:
        # The Pydantic model with its validator already handles the input checks.
        # If the input is invalid, FastAPI will return a 422 error automatically.
        
        # Calculate score and severity
        result = anxiety_scoring.calculate_assessment(request.responses)

        # Create a new assessment record
        new_assessment = Assessment(
            user_id=current_user.id,
            responses=request.responses,
            total_score=result["total_score"],
            severity=result["severity"]
        )
        
        db.add(new_assessment)
        db.commit()
        
        return result

    except ValueError as e:
        # This is another layer of error handling, though Pydantic should catch it first.
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the assessment."
        )
