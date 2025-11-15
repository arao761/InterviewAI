"""
Session management routes.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app import SessionCreate, SessionResponse
from app.models.models import Session as SessionModel, SessionStatus
from app.core.logging import logger

router = APIRouter(prefix="/sessions", tags=["Sessions"])

# Your existing code goes here...
@router.post("/create", response_model=SessionResponse)
async def create_session(
    request: SessionCreate,
    db: Session = Depends(get_db)
):
    """Create a new interview session."""
    try:
        # Create new session
        session = SessionModel(
            interview_type=request.interview_type,
            technical_domain=request.technical_domain,
            status=SessionStatus.CREATED
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        logger.info(f"Session created: {session.id}")
        return session
        
    except Exception as e:
        logger.error(f"Session creation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create session")


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """Get session details."""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session