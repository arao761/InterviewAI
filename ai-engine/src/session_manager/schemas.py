"""
Session Manager Schemas
Pydantic models for interview sessions and progress tracking
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from datetime import datetime
import uuid


class SessionStatus(str, Enum):
    """Interview session status"""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class InterviewMode(str, Enum):
    """Interview mode types"""
    PRACTICE = "practice"
    MOCK = "mock"
    REAL = "real"
    ASSESSMENT = "assessment"


class SessionType(str, Enum):
    """Type of interview session"""
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    MIXED = "mixed"
    SYSTEM_DESIGN = "system_design"
    CODING = "coding"


class QuestionResponse(BaseModel):
    """Single question response in a session"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question_id": "q_123",
                "question_text": "Explain how a hash table works",
                "answer_text": "A hash table uses...",
                "time_spent_seconds": 420,
                "evaluation_score": 85.0,
                "is_skipped": False
            }
        }
    )
    
    question_id: str = Field(..., description="Question identifier")
    question_text: str = Field(..., description="The question asked")
    question_type: str = Field(..., description="Type of question")
    question_difficulty: str = Field(default="medium")
    
    answer_text: Optional[str] = Field(None, description="Candidate's answer")
    time_spent_seconds: int = Field(default=0, ge=0)
    started_at: Optional[str] = None
    answered_at: Optional[str] = None
    
    evaluation_score: Optional[float] = Field(None, ge=0, le=100)
    evaluation_id: Optional[str] = None
    feedback_summary: Optional[str] = None
    
    is_skipped: bool = Field(default=False)
    is_flagged: bool = Field(default=False, description="Flagged for review")
    notes: Optional[str] = Field(None, description="Additional notes")


class InterviewSession(BaseModel):
    """Complete interview session"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "sess_abc123",
                "candidate_name": "John Doe",
                "status": "completed",
                "mode": "practice",
                "session_type": "mixed",
                "target_role": "Software Engineer",
                "total_questions": 5,
                "questions_answered": 5
            }
        }
    )
    
    # Identifiers
    session_id: str = Field(default_factory=lambda: f"sess_{uuid.uuid4().hex[:12]}")
    user_id: Optional[str] = Field(None, description="User identifier")
    
    # Session metadata
    candidate_name: str = Field(..., description="Candidate name")
    candidate_email: Optional[str] = None
    target_role: str = Field(..., description="Target job role")
    target_company: Optional[str] = None
    experience_level: Literal["junior", "mid", "senior"] = Field(default="mid")
    
    # Session configuration
    status: SessionStatus = Field(default=SessionStatus.SCHEDULED)
    mode: InterviewMode = Field(default=InterviewMode.PRACTICE)
    session_type: SessionType = Field(default=SessionType.MIXED)
    
    # Timestamps
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    # Questions and responses
    total_questions: int = Field(default=0, ge=0)
    questions_answered: int = Field(default=0, ge=0)
    questions_skipped: int = Field(default=0, ge=0)
    current_question_index: int = Field(default=0, ge=0)
    
    responses: List[QuestionResponse] = Field(default_factory=list)
    
    # Performance metrics
    average_score: Optional[float] = Field(None, ge=0, le=100)
    total_duration_seconds: Optional[int] = Field(None, ge=0)
    technical_score: Optional[float] = None
    behavioral_score: Optional[float] = None
    
    # Session summary
    session_summary: Optional[str] = None
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    
    # Resume context
    resume_id: Optional[str] = None
    resume_summary: Optional[Dict[str, Any]] = None
    
    def add_response(self, response: QuestionResponse) -> None:
        """Add a question response to the session"""
        self.responses.append(response)
        if not response.is_skipped:
            self.questions_answered += 1
        else:
            self.questions_skipped += 1
        self.current_question_index += 1
        self.updated_at = datetime.now().isoformat()
    
    def calculate_metrics(self) -> None:
        """Calculate session performance metrics"""
        answered_responses = [r for r in self.responses if not r.is_skipped and r.evaluation_score is not None]
        
        if answered_responses:
            scores = [r.evaluation_score for r in answered_responses]
            self.average_score = sum(scores) / len(scores)
            
            # Calculate technical vs behavioral scores
            technical_responses = [r for r in answered_responses if r.question_type in ["technical", "coding", "system_design"]]
            behavioral_responses = [r for r in answered_responses if r.question_type in ["behavioral", "situational"]]
            
            if technical_responses:
                self.technical_score = sum(r.evaluation_score for r in technical_responses) / len(technical_responses)
            
            if behavioral_responses:
                self.behavioral_score = sum(r.evaluation_score for r in behavioral_responses) / len(behavioral_responses)
            
            # Calculate total duration
            time_spent = [r.time_spent_seconds for r in self.responses]
            self.total_duration_seconds = sum(time_spent)
        
        self.updated_at = datetime.now().isoformat()
    
    def get_progress_percentage(self) -> float:
        """Get session progress percentage"""
        if self.total_questions == 0:
            return 0.0
        return (self.current_question_index / self.total_questions) * 100
    
    def is_complete(self) -> bool:
        """Check if session is complete"""
        return self.status == SessionStatus.COMPLETED or self.current_question_index >= self.total_questions


class SessionCreateRequest(BaseModel):
    """Request to create a new interview session"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "candidate_name": "John Doe",
                "candidate_email": "john@example.com",
                "target_role": "Software Engineer",
                "experience_level": "mid",
                "mode": "practice",
                "num_technical": 3,
                "num_behavioral": 2
            }
        }
    )
    
    candidate_name: str
    candidate_email: Optional[str] = None
    user_id: Optional[str] = None
    
    target_role: str
    target_company: Optional[str] = None
    experience_level: Literal["junior", "mid", "senior"] = Field(default="mid")
    
    mode: InterviewMode = Field(default=InterviewMode.PRACTICE)
    session_type: SessionType = Field(default=SessionType.MIXED)
    
    # Question configuration
    num_technical: int = Field(default=3, ge=0, le=20)
    num_behavioral: int = Field(default=2, ge=0, le=10)
    num_system_design: int = Field(default=0, ge=0, le=5)
    num_coding: int = Field(default=0, ge=0, le=5)
    
    focus_areas: List[str] = Field(default_factory=list)
    resume_context: Optional[Dict[str, Any]] = None


class UserProgress(BaseModel):
    """User's progress tracking across sessions"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "user_123",
                "total_sessions": 10,
                "total_questions_answered": 50,
                "average_score": 78.5,
                "improvement_rate": 12.5
            }
        }
    )
    
    user_id: str = Field(..., description="User identifier")
    username: str
    email: Optional[str] = None
    
    # Statistics
    total_sessions: int = Field(default=0, ge=0)
    completed_sessions: int = Field(default=0, ge=0)
    total_questions_answered: int = Field(default=0, ge=0)
    total_time_spent_hours: float = Field(default=0.0, ge=0)
    
    # Performance metrics
    average_score: float = Field(default=0.0, ge=0, le=100)
    best_score: float = Field(default=0.0, ge=0, le=100)
    worst_score: float = Field(default=0.0, ge=0, le=100)
    
    technical_average: float = Field(default=0.0, ge=0, le=100)
    behavioral_average: float = Field(default=0.0, ge=0, le=100)
    
    # Improvement tracking
    improvement_rate: float = Field(default=0.0, description="Percentage improvement over time")
    score_trend: List[float] = Field(default_factory=list, description="Score history")
    
    # Strengths and weaknesses
    top_strengths: List[str] = Field(default_factory=list)
    top_weaknesses: List[str] = Field(default_factory=list)
    mastered_topics: List[str] = Field(default_factory=list)
    needs_practice: List[str] = Field(default_factory=list)
    
    # Session history
    recent_sessions: List[str] = Field(default_factory=list, description="Recent session IDs")
    last_session_date: Optional[str] = None
    
    # Timestamps
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class ProgressAnalytics(BaseModel):
    """Detailed analytics for user progress"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "user_123",
                "period": "30_days",
                "sessions_completed": 8,
                "average_score": 82.3,
                "improvement_percentage": 15.2
            }
        }
    )
    
    user_id: str
    period: Literal["7_days", "30_days", "90_days", "all_time"] = Field(default="30_days")
    
    # Session metrics
    sessions_completed: int = Field(default=0)
    sessions_by_type: Dict[str, int] = Field(default_factory=dict)
    sessions_by_mode: Dict[str, int] = Field(default_factory=dict)
    
    # Performance metrics
    average_score: float = Field(default=0.0)
    median_score: float = Field(default=0.0)
    score_variance: float = Field(default=0.0)
    
    # Score breakdown
    technical_scores: List[float] = Field(default_factory=list)
    behavioral_scores: List[float] = Field(default_factory=list)
    
    # Improvement metrics
    improvement_percentage: float = Field(default=0.0)
    best_performing_areas: List[str] = Field(default_factory=list)
    worst_performing_areas: List[str] = Field(default_factory=list)
    
    # Time analysis
    total_practice_time_hours: float = Field(default=0.0)
    average_session_duration_minutes: float = Field(default=0.0)
    
    # Trends
    score_by_date: Dict[str, float] = Field(default_factory=dict)
    questions_by_date: Dict[str, int] = Field(default_factory=dict)
    
    # Recommendations
    focus_recommendations: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)


class SessionComparison(BaseModel):
    """Comparison between multiple sessions"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_ids": ["sess_1", "sess_2"],
                "score_improvement": 8.5,
                "time_improvement": -120,
                "better_session": "sess_2"
            }
        }
    )
    
    session_ids: List[str] = Field(..., min_length=2, description="Sessions being compared")
    user_id: str
    
    # Score comparison
    scores: List[float] = Field(..., description="Scores for each session")
    score_improvement: float = Field(..., description="Score difference (later - earlier)")
    average_score_change: float = Field(default=0.0)
    
    # Time comparison
    durations: List[int] = Field(..., description="Duration in seconds for each session")
    time_improvement: int = Field(..., description="Time difference in seconds (later - earlier)")
    
    # Performance comparison
    technical_comparison: Optional[Dict[str, float]] = None
    behavioral_comparison: Optional[Dict[str, float]] = None
    
    # Insights
    better_session: str = Field(..., description="ID of better performing session")
    improvement_areas: List[str] = Field(default_factory=list)
    regression_areas: List[str] = Field(default_factory=list)
    
    consistency_score: float = Field(default=0.0, description="How consistent performance was")


class Milestone(BaseModel):
    """Achievement milestone"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "milestone_id": "milestone_first_100",
                "title": "Century Club",
                "description": "Answered 100 questions",
                "achieved_at": "2024-01-15T10:30:00"
            }
        }
    )
    
    milestone_id: str = Field(..., description="Unique milestone identifier")
    title: str = Field(..., description="Milestone title")
    description: str = Field(..., description="Milestone description")
    category: Literal["questions", "sessions", "score", "improvement", "streak"] = Field(default="questions")
    
    threshold: float = Field(..., description="Achievement threshold")
    current_value: float = Field(..., description="Current progress value")
    
    achieved: bool = Field(default=False)
    achieved_at: Optional[str] = None
    
    reward_points: int = Field(default=0, ge=0)
    badge_icon: Optional[str] = None


class LearningPath(BaseModel):
    """Personalized learning path recommendation"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "user_123",
                "current_level": "intermediate",
                "recommended_focus": ["algorithms", "system design"],
                "estimated_completion_weeks": 4
            }
        }
    )
    
    user_id: str
    current_level: Literal["beginner", "intermediate", "advanced"] = Field(default="beginner")
    target_level: Literal["intermediate", "advanced", "expert"] = Field(default="intermediate")
    
    # Current assessment
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    skill_gaps: List[str] = Field(default_factory=list)
    
    # Recommendations
    recommended_focus: List[str] = Field(default_factory=list)
    recommended_topics: List[Dict[str, Any]] = Field(default_factory=list)
    recommended_session_frequency: str = Field(default="3 times per week")
    
    # Timeline
    estimated_completion_weeks: int = Field(default=4, ge=1)
    milestones: List[str] = Field(default_factory=list)
    
    # Resources
    suggested_resources: List[str] = Field(default_factory=list)
    practice_exercises: List[str] = Field(default_factory=list)
    
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
