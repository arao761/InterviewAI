"""
Pydantic schemas for request/response validation.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.models import SessionStatus, InterviewType, QuestionType, DifficultyLevel


# ====== BASE SCHEMAS ======
class BaseResponse(BaseModel):
    """Base response schema."""
    success: bool = True
    message: str = "Operation successful"


class ErrorResponse(BaseModel):
    """Error response schema."""
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    timestamp: datetime
    version: str
    database_status: str = "connected"


# ====== USER SCHEMAS ======
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    name: str


class UserCreate(UserBase):
    """User creation schema."""
    password: Optional[str] = None


class UserProfileUpdate(BaseModel):
    """User profile update schema."""
    name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    profile_picture_url: Optional[str] = None
    target_role: Optional[str] = None
    target_company: Optional[str] = None
    experience_level: Optional[str] = None
    current_position: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = None
    preferred_interview_types: Optional[List[str]] = None
    interview_preferences: Optional[Dict[str, Any]] = None


class UserResponse(UserBase):
    """User response schema with full profile."""
    id: int
    phone: Optional[str] = None
    bio: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    profile_picture_url: Optional[str] = None
    target_role: Optional[str] = None
    target_company: Optional[str] = None
    experience_level: Optional[str] = None
    current_position: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = None
    preferred_interview_types: Optional[List[str]] = None
    interview_preferences: Optional[Dict[str, Any]] = None
    total_sessions: int = 0
    total_questions_answered: int = 0
    average_score: Optional[float] = None
    last_session_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ====== SESSION SCHEMAS ======
class SessionCreate(BaseModel):
    """Session creation schema."""
    interview_type: Optional[InterviewType] = None
    technical_domain: Optional[str] = None


class SessionResponse(BaseModel):
    """Session response schema."""
    id: int
    status: SessionStatus
    interview_type: Optional[InterviewType] = None
    technical_domain: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SessionStatusResponse(BaseResponse):
    """Session status response."""
    data: SessionResponse


# ====== RESUME SCHEMAS ======
class ResumeUploadResponse(BaseResponse):
    """Resume upload response."""
    data: Dict[str, Any]


class ResumeProcessRequest(BaseModel):
    """Resume processing request."""
    session_id: int


class ResumeProcessResponse(BaseResponse):
    """Resume processing response."""
    data: Dict[str, Any]


# ====== QUESTION SCHEMAS ======
class QuestionResponse(BaseModel):
    """Question response schema."""
    id: int
    question_text: str
    question_type: QuestionType
    category: Optional[str] = None
    difficulty_level: Optional[DifficultyLevel] = None
    order_index: int
    
    class Config:
        from_attributes = True


class QuestionsListResponse(BaseResponse):
    """Questions list response."""
    data: List[QuestionResponse]


# ====== INTERVIEW SCHEMAS ======
class StartInterviewRequest(BaseModel):
    """Start interview request."""
    session_id: int
    interview_type: InterviewType
    technical_domain: Optional[str] = None


class StartInterviewResponse(BaseResponse):
    """Start interview response."""
    data: Dict[str, Any]


# ====== RESPONSE SCHEMAS ======
class SubmitResponseRequest(BaseModel):
    """Submit response request."""
    question_id: int
    transcript: Optional[str] = None
    duration_seconds: Optional[float] = None


class ResponseSubmissionResponse(BaseResponse):
    """Response submission response."""
    data: Dict[str, Any]


class ResponseResponse(BaseModel):
    """Response data schema."""
    id: int
    question_id: int
    transcript: Optional[str] = None
    duration_seconds: Optional[float] = None
    submitted_at: datetime
    
    class Config:
        from_attributes = True


# ====== FEEDBACK SCHEMAS ======
class EvaluateResponseRequest(BaseModel):
    """Evaluate response request."""
    response_id: int


class FeedbackResponse(BaseModel):
    """Feedback response schema."""
    id: int
    response_id: int
    overall_score: Optional[float] = None
    star_analysis: Optional[Dict[str, Any]] = None
    technical_accuracy: Optional[Dict[str, Any]] = None
    speech_metrics: Optional[Dict[str, Any]] = None
    improvement_suggestions: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class FeedbackDetailResponse(BaseResponse):
    """Detailed feedback response."""
    data: FeedbackResponse


# ====== RESULTS SCHEMAS ======
class SessionResultsResponse(BaseResponse):
    """Complete session results."""
    data: Dict[str, Any]


class AnalyticsResponse(BaseResponse):
    """Session analytics response."""
    data: Dict[str, Any]


# ====== FILE SCHEMAS ======
class FileUploadResponse(BaseResponse):
    """Generic file upload response."""
    data: Dict[str, Any]