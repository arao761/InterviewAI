"""
Dashboard routes for user statistics and interview history.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.core.database import get_db
from app.models.models import User, Session as SessionModel, Response, Feedback, Question, SessionStatus
from app.api.routes.auth import get_current_user
from app.schemas.dashboard_schemas import DashboardStatsResponse, InterviewHistoryItem, InterviewHistoryResponse
from app.core.logging import logger

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics for the current user.
    
    Returns:
        - total_interviews: Number of completed interview sessions
        - average_score: Average score across all completed interviews
        - best_score: Highest score achieved
        - hours_spent: Total hours spent practicing
    """
    try:
        # Get all completed sessions for the user
        completed_sessions = db.query(SessionModel).filter(
            SessionModel.user_id == current_user.id,
            SessionModel.status == SessionStatus.COMPLETED
        ).all()
        
        total_interviews = len(completed_sessions)
        
        if total_interviews == 0:
            # Return zero stats for new users
            return DashboardStatsResponse(
                total_interviews=0,
                average_score=0.0,
                best_score=None,
                hours_spent=0.0
            )
        
        # Get all scores from feedback for completed sessions
        session_ids = [s.id for s in completed_sessions]
        
        # Get all questions for these sessions
        questions = db.query(Question).filter(
            Question.session_id.in_(session_ids)
        ).all()
        
        question_ids = [q.id for q in questions]
        
        # Get all responses for these questions
        responses = db.query(Response).filter(
            Response.question_id.in_(question_ids)
        ).all()
        
        response_ids = [r.id for r in responses]
        
        # Get all feedback scores
        feedback_scores = db.query(Feedback.overall_score).filter(
            Feedback.response_id.in_(response_ids),
            Feedback.overall_score.isnot(None)
        ).all()
        
        # Convert scores from 0-10 scale to 0-100 percentage
        scores = [score[0] * 10 for score in feedback_scores if score[0] is not None]
        
        # Calculate statistics
        if scores:
            average_score = sum(scores) / len(scores)
            best_score = max(scores)
        else:
            average_score = 0.0
            best_score = None
        
        # Calculate total hours spent
        total_seconds = sum(
            r.duration_seconds for r in responses 
            if r.duration_seconds is not None
        )
        hours_spent = round(total_seconds / 3600, 1) if total_seconds > 0 else 0.0
        
        logger.info(f"Dashboard stats for user {current_user.id}: {total_interviews} interviews, avg score: {average_score:.1f}%")
        
        return DashboardStatsResponse(
            total_interviews=total_interviews,
            average_score=round(average_score, 1),
            best_score=round(best_score, 1) if best_score else None,
            hours_spent=hours_spent
        )
        
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard statistics")


@router.get("/history", response_model=InterviewHistoryResponse)
async def get_interview_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get interview history for the current user.
    
    Returns a list of completed interview sessions with their details.
    """
    try:
        # Get all completed sessions for the user, ordered by most recent
        sessions = db.query(SessionModel).filter(
            SessionModel.user_id == current_user.id,
            SessionModel.status == SessionStatus.COMPLETED
        ).order_by(SessionModel.created_at.desc()).all()
        
        interview_items = []
        
        for session in sessions:
            # Get all questions for this session
            questions = db.query(Question).filter(
                Question.session_id == session.id
            ).all()
            
            question_ids = [q.id for q in questions]
            
            # Get all responses for these questions
            responses = db.query(Response).filter(
                Response.question_id.in_(question_ids)
            ).all()
            
            response_ids = [r.id for r in responses]
            
            # Calculate average score for this session
            feedback_scores = db.query(Feedback.overall_score).filter(
                Feedback.response_id.in_(response_ids),
                Feedback.overall_score.isnot(None)
            ).all()
            
            scores = [score[0] * 10 for score in feedback_scores if score[0] is not None]
            session_score = round(sum(scores) / len(scores), 1) if scores else None
            
            # Calculate total duration
            total_seconds = sum(
                r.duration_seconds for r in responses 
                if r.duration_seconds is not None
            )
            duration_minutes = round(total_seconds / 60, 1) if total_seconds > 0 else None
            
            # Get interview type
            interview_type = session.interview_type.value if session.interview_type else None
            
            interview_items.append(InterviewHistoryItem(
                id=session.id,
                interview_type=interview_type,
                technical_domain=session.technical_domain,
                date=session.created_at,
                score=session_score,
                duration_minutes=duration_minutes,
                status=session.status.value
            ))
        
        logger.info(f"Retrieved {len(interview_items)} interview history items for user {current_user.id}")
        
        return InterviewHistoryResponse(interviews=interview_items)
        
    except Exception as e:
        logger.error(f"Error fetching interview history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch interview history")

