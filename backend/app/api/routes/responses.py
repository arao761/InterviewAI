"""
Response submission and evaluation routes.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app import ResponseSubmissionResponse, FeedbackDetailResponse
from app.models.models import Question, Response, Feedback
from app.utils.file_utils import save_upload_file
from app.core.logging import logger

router = APIRouter(prefix="/responses", tags=["Responses"])


@router.post("/submit", response_model=ResponseSubmissionResponse)
async def submit_response(
    question_id: int = Form(...),
    transcript: str = Form(None),
    duration_seconds: float = Form(None),
    audio_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """Submit response with audio and/or transcript."""
    try:
        # Validate question exists
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        audio_path = None
        if audio_file:
            # Save audio file
            audio_path, unique_filename = await save_upload_file(
                audio_file, subdirectory="responses", prefix="response"
            )
            logger.info(f"Audio saved: {unique_filename}")
        
        # TODO: If no transcript provided, call Person 3's transcription API
        if not transcript and audio_file:
            transcript = "Sample transcribed text from audio..."
        
        # Create response record
        response = Response(
            question_id=question_id,
            audio_file_path=audio_path,
            transcript=transcript,
            duration_seconds=duration_seconds
        )
        db.add(response)
        db.commit()
        db.refresh(response)
        
        logger.info(f"Response submitted for question {question_id}")
        
        return ResponseSubmissionResponse(
            data={
                "response_id": response.id,
                "question_id": question_id,
                "transcript": transcript,
                "audio_saved": audio_path is not None,
                "duration_seconds": duration_seconds
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Submit response error: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit response")


@router.post("/{response_id}/evaluate", response_model=FeedbackDetailResponse)
async def evaluate_response(
    response_id: int,
    db: Session = Depends(get_db)
):
    """Evaluate response and generate feedback."""
    try:
        # Get response and related question
        response = db.query(Response).filter(Response.id == response_id).first()
        if not response:
            raise HTTPException(status_code=404, detail="Response not found")
        
        question = db.query(Question).filter(Question.id == response.question_id).first()
        
        # TODO: Call Person 4's evaluation functions
        # For now, create sample feedback
        sample_feedback = {
            "overall_score": 75.0,
            "star_analysis": {
                "situation": {"present": True, "score": 8, "feedback": "Good context provided"},
                "task": {"present": True, "score": 7, "feedback": "Task clearly defined"},  
                "action": {"present": True, "score": 8, "feedback": "Specific actions described"},
                "result": {"present": False, "score": 5, "feedback": "Could include more specific outcomes"}
            },
            "strengths": [
                "Clear communication",
                "Good structure", 
                "Specific examples"
            ],
            "improvements": [
                "Add quantifiable results",
                "More detail on impact",
                "Stronger conclusion"
            ]
        }
        
        # Create feedback record
        feedback = Feedback(
            response_id=response_id,
            overall_score=sample_feedback["overall_score"],
            star_analysis=sample_feedback["star_analysis"],
            improvement_suggestions={"areas": sample_feedback["improvements"]}
        )
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        
        logger.info(f"Feedback generated for response {response_id}")
        
        return FeedbackDetailResponse(
            data={
                "id": feedback.id,
                "response_id": response_id,
                "overall_score": feedback.overall_score,
                "star_analysis": feedback.star_analysis,
                "technical_accuracy": feedback.technical_accuracy,
                "speech_metrics": feedback.speech_metrics,
                "improvement_suggestions": feedback.improvement_suggestions,
                "created_at": feedback.created_at
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Evaluate response error: {e}")
        raise HTTPException(status_code=500, detail="Failed to evaluate response")