"""
Question Generator Schemas
Pydantic models for interview questions
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Literal
from enum import Enum


class QuestionType(str, Enum):
    """Types of interview questions"""
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    SITUATIONAL = "situational"
    SYSTEM_DESIGN = "system_design"
    CODING = "coding"


class DifficultyLevel(str, Enum):
    """Question difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class InterviewQuestion(BaseModel):
    """Single interview question with metadata"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "Describe a time when you had to work with a difficult team member",
                "type": "behavioral",
                "difficulty": "medium",
                "category": "teamwork",
                "skills_tested": ["communication", "conflict resolution"],
                "expected_duration_minutes": 5,
                "follow_up_questions": ["What was the outcome?", "What would you do differently?"]
            }
        }
    )
    
    question: str = Field(..., description="The interview question text")
    type: QuestionType = Field(..., description="Type of question")
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM)
    category: str = Field(..., description="Category or topic (e.g., 'algorithms', 'leadership')")
    skills_tested: List[str] = Field(default_factory=list, description="Skills being evaluated")
    expected_duration_minutes: int = Field(default=5, ge=1, le=30)
    context: Optional[str] = Field(None, description="Additional context for the question")
    follow_up_questions: List[str] = Field(default_factory=list)
    hints: List[str] = Field(default_factory=list)
    sample_answer_points: List[str] = Field(default_factory=list)
    
    # Metadata
    related_resume_section: Optional[str] = Field(None, description="Which resume section this relates to")
    company_specific: bool = Field(default=False)
    role_specific: bool = Field(default=True)


class QuestionSet(BaseModel):
    """Set of questions for an interview session"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "sess_123",
                "target_role": "Software Engineer",
                "target_level": "mid",
                "questions": [],
                "total_duration_minutes": 45,
                "technical_count": 5,
                "behavioral_count": 3
            }
        }
    )
    
    session_id: str = Field(..., description="Unique session identifier")
    target_role: str = Field(..., description="Job role being interviewed for")
    target_level: str = Field(..., description="Experience level: junior, mid, senior")
    target_company: Optional[str] = Field(None, description="Specific company if applicable")
    
    questions: List[InterviewQuestion] = Field(default_factory=list)
    
    # Session metadata
    total_duration_minutes: int = Field(default=45, ge=15, le=180)
    technical_count: int = Field(default=0)
    behavioral_count: int = Field(default=0)
    created_at: Optional[str] = None
    
    def add_question(self, question: InterviewQuestion) -> None:
        """Add a question to the set and update counts"""
        self.questions.append(question)
        
        if question.type == QuestionType.TECHNICAL:
            self.technical_count += 1
        elif question.type == QuestionType.BEHAVIORAL:
            self.behavioral_count += 1
    
    def get_questions_by_type(self, question_type: QuestionType) -> List[InterviewQuestion]:
        """Get all questions of a specific type"""
        return [q for q in self.questions if q.type == question_type]
    
    def get_questions_by_difficulty(self, difficulty: DifficultyLevel) -> List[InterviewQuestion]:
        """Get all questions of a specific difficulty"""
        return [q for q in self.questions if q.difficulty == difficulty]
    
    def get_total_duration(self) -> int:
        """Calculate total duration of all questions"""
        return sum(q.expected_duration_minutes for q in self.questions)


class QuestionGenerationRequest(BaseModel):
    """Request to generate interview questions"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "target_role": "Senior Software Engineer",
                "target_level": "senior",
                "num_technical": 5,
                "num_behavioral": 3,
                "focus_areas": ["system design", "leadership"],
                "difficulty_distribution": {"easy": 1, "medium": 4, "hard": 3}
            }
        }
    )
    
    target_role: str = Field(..., description="Job role")
    target_level: Literal["junior", "mid", "senior"] = Field(default="mid")
    target_company: Optional[str] = None
    
    # Question distribution
    num_technical: int = Field(default=5, ge=0, le=20)
    num_behavioral: int = Field(default=3, ge=0, le=10)
    num_situational: int = Field(default=0, ge=0, le=5)
    num_system_design: int = Field(default=0, ge=0, le=5)
    
    # Customization
    focus_areas: List[str] = Field(default_factory=list, description="Specific topics to focus on")
    avoid_topics: List[str] = Field(default_factory=list, description="Topics to avoid")
    difficulty_distribution: Optional[dict] = Field(
        None,
        description="Distribution like {'easy': 2, 'medium': 4, 'hard': 2}"
    )
    
    # Resume-based customization
    resume_context: Optional[dict] = Field(None, description="Parsed resume data")
    tailor_to_experience: bool = Field(default=True)
    include_resume_specific: bool = Field(default=True)
    
    # Session constraints
    max_duration_minutes: int = Field(default=60, ge=15, le=180)
    include_follow_ups: bool = Field(default=True)
    include_hints: bool = Field(default=False)
