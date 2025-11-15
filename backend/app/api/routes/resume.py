"""
Resume management routes.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app import ResumeUploadResponse, ResumeProcessRequest, ResumeProcessResponse
from app.utils.file_utils import save_upload_file
from app.models.models import Resume, Session as SessionModel, SessionStatus
from app.core.logging import logger

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and save a resume file."""
    try:
        # Save file to storage
        file_path, unique_filename = await save_upload_file(
            file, subdirectory="resumes", prefix="resume"
        )
        
        # Create a new session first
        session = SessionModel(
            status=SessionStatus.RESUME_UPLOADED
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        # Save resume to database
        resume = Resume(
            session_id=session.id,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file.size or 0
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        logger.info(f"Resume uploaded successfully: {unique_filename}")
        
        return ResumeUploadResponse(
            data={
                "file_id": resume.id,
                "session_id": session.id,
                "filename": unique_filename,
                "file_size": resume.file_size,
                "upload_path": file_path
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resume upload error: {e}")
        raise HTTPException(status_code=500, detail="Resume upload failed")


@router.post("/process", response_model=ResumeProcessResponse)
async def process_resume(
    request: ResumeProcessRequest,
    db: Session = Depends(get_db)
):
    """Process uploaded resume and extract data."""
    try:
        # Get session and resume
        session = db.query(SessionModel).filter(SessionModel.id == request.session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        resume = db.query(Resume).filter(Resume.session_id == request.session_id).first()
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found for session")
        
        # TODO: Call Person 4's parse_resume() function here
        # For now, simulate parsing
        parsed_data = {
            "contact": {
                "email": "john.doe@email.com", 
                "phone": "555-0123",
                "linkedin": "linkedin.com/in/johndoe"
            },
            "experience": [
                {
                    "company": "Tech Corp", 
                    "title": "Software Developer", 
                    "years": 2,
                    "description": "Developed web applications using Python and React"
                },
                {
                    "company": "Startup Inc", 
                    "title": "Junior Developer", 
                    "years": 1,
                    "description": "Built REST APIs and database systems"
                }
            ],
            "skills": ["Python", "JavaScript", "React", "SQL", "FastAPI", "Git"],
            "education": [
                {
                    "degree": "BS Computer Science", 
                    "university": "State University",
                    "graduation_year": 2021
                }
            ],
            "projects": [
                {
                    "name": "E-commerce Platform",
                    "technologies": ["Python", "React", "PostgreSQL"],
                    "description": "Built full-stack web application"
                }
            ]
        }
        
        extracted_text = """
        John Doe
        Software Developer
        Email: john.doe@email.com
        Phone: 555-0123
        
        EXPERIENCE
        Tech Corp - Software Developer (2022-2024)
        - Developed web applications using Python and React
        - Collaborated with cross-functional teams
        
        Startup Inc - Junior Developer (2021-2022)  
        - Built REST APIs and database systems
        - Learned agile development practices
        
        EDUCATION
        State University - BS Computer Science (2021)
        
        SKILLS
        Python, JavaScript, React, SQL, FastAPI, Git
        """
        
        # Update resume with parsed data
        resume.parsed_data = parsed_data
        resume.extracted_text = extracted_text.strip()
        
        # Update session status
        session.status = SessionStatus.RESUME_PROCESSED
        
        db.commit()
        logger.info(f"Resume processed for session {request.session_id}")
        
        return ResumeProcessResponse(
            data={
                "session_id": session.id,
                "status": session.status.value,
                "extracted_text": resume.extracted_text,
                "parsed_data": parsed_data
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resume processing error: {e}")
        raise HTTPException(status_code=500, detail="Resume processing failed")