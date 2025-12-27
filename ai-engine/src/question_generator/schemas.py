"""
Question Generator Schemas
"""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class QuestionType(str, Enum):
    """Types of interview questions"""
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    SITUATIONAL = "situational"
    SYSTEM_DESIGN = "system_design"
    CODING = "coding"


class DifficultyLevel(str, Enum):
    """Difficulty levels for questions"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class InterviewQuestion(BaseModel):
    """Single interview question"""
    question: str = Field(..., description="The question text")
    type: QuestionType = Field(..., description="Type of question")
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM)
    category: Optional[str] = Field(None, description="Question category")
    skills_tested: List[str] = Field(default_factory=list, description="Skills this question tests")
    expected_duration_minutes: int = Field(default=5, ge=1, le=30)
    follow_up_questions: List[str] = Field(default_factory=list)
    question_id: Optional[str] = None


class QuestionGenerationRequest(BaseModel):
    """Request to generate interview questions"""
    target_role: str = Field(..., description="Target job role")
    target_level: str = Field(default="mid", description="Experience level: junior, mid, senior")
    target_company: Optional[str] = Field(None, description="Target company name")
    num_technical: int = Field(default=3, ge=0, le=20)
    num_behavioral: int = Field(default=2, ge=0, le=10)
    num_situational: int = Field(default=0, ge=0, le=10)
    num_system_design: int = Field(default=0, ge=0, le=5)
    resume_context: Optional[dict] = Field(None, description="Resume/background context")
    focus_areas: List[str] = Field(default_factory=list)
    avoid_topics: List[str] = Field(default_factory=list, description="Topics to avoid")
    tailor_to_experience: bool = Field(default=True, description="Tailor questions to resume experience")


class QuestionSet(BaseModel):
    """Set of generated interview questions"""
    session_id: str
    target_role: str
    target_level: str
    questions: List[InterviewQuestion] = Field(default_factory=list)
    generated_at: Optional[str] = None

    def add_question(self, question: InterviewQuestion) -> None:
        """Add a question to the set"""
        self.questions.append(question)

    def get_questions_by_type(self, question_type: QuestionType) -> List[InterviewQuestion]:
        """Get all questions of a specific type"""
        return [q for q in self.questions if q.type == question_type]

    def get_total_count(self) -> int:
        """Get total number of questions"""
        return len(self.questions)

