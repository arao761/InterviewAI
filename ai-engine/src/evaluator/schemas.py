"""
Answer Evaluator Schemas
Pydantic models for answer evaluation and feedback
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from datetime import datetime


class EvaluationCriteria(str, Enum):
    """Evaluation criteria for answers"""
    TECHNICAL_ACCURACY = "technical_accuracy"
    COMPLETENESS = "completeness"
    CLARITY = "clarity"
    STRUCTURE = "structure"
    RELEVANCE = "relevance"
    DEPTH = "depth"
    EXAMPLES = "examples"
    COMMUNICATION = "communication"


class FeedbackType(str, Enum):
    """Types of feedback"""
    STRENGTH = "strength"
    WEAKNESS = "weakness"
    SUGGESTION = "suggestion"
    EXAMPLE = "example"


class ScoreLevel(str, Enum):
    """Score level categories"""
    EXCELLENT = "excellent"  # 90-100
    GOOD = "good"  # 70-89
    FAIR = "fair"  # 50-69
    POOR = "poor"  # 0-49


class CriterionScore(BaseModel):
    """Score for a specific evaluation criterion"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "criterion": "technical_accuracy",
                "score": 85,
                "max_score": 100,
                "weight": 0.3,
                "feedback": "Good technical understanding demonstrated"
            }
        }
    )
    
    criterion: EvaluationCriteria
    score: float = Field(..., ge=0, le=100, description="Score out of 100")
    max_score: float = Field(default=100, ge=0)
    weight: float = Field(default=1.0, ge=0, le=1.0, description="Weight of this criterion")
    feedback: Optional[str] = Field(None, description="Specific feedback for this criterion")
    
    @property
    def weighted_score(self) -> float:
        """Calculate weighted score"""
        return (self.score / self.max_score) * self.weight * 100


class FeedbackItem(BaseModel):
    """Individual feedback item"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "strength",
                "category": "technical_accuracy",
                "message": "Excellent explanation of algorithm complexity",
                "priority": "high"
            }
        }
    )
    
    type: FeedbackType
    category: str = Field(..., description="Category or aspect this feedback relates to")
    message: str = Field(..., description="The feedback message")
    priority: Literal["high", "medium", "low"] = Field(default="medium")
    actionable: bool = Field(default=True, description="Whether this is actionable feedback")
    examples: List[str] = Field(default_factory=list, description="Example improvements or references")


class AnswerEvaluation(BaseModel):
    """Complete evaluation of a candidate's answer"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question_id": "q_123",
                "answer_text": "To implement a LRU cache...",
                "overall_score": 82.5,
                "score_level": "good",
                "criterion_scores": [],
                "strengths": [],
                "weaknesses": [],
                "suggestions": [],
                "evaluation_timestamp": "2024-01-15T10:30:00"
            }
        }
    )
    
    # Identifiers
    evaluation_id: str = Field(..., description="Unique evaluation identifier")
    question_id: str = Field(..., description="ID of the question being answered")
    session_id: Optional[str] = Field(None, description="Interview session ID")
    
    # Answer details
    answer_text: str = Field(..., description="The candidate's answer")
    question_text: Optional[str] = Field(None, description="The original question")
    question_type: Optional[str] = Field(None, description="Type of question")
    
    # Scoring
    overall_score: float = Field(..., ge=0, le=100, description="Overall score out of 100")
    score_level: ScoreLevel
    criterion_scores: List[CriterionScore] = Field(default_factory=list)
    
    # Detailed feedback
    strengths: List[FeedbackItem] = Field(default_factory=list)
    weaknesses: List[FeedbackItem] = Field(default_factory=list)
    suggestions: List[FeedbackItem] = Field(default_factory=list)
    
    # Summary
    summary: Optional[str] = Field(None, description="Brief summary of the evaluation")
    key_takeaways: List[str] = Field(default_factory=list)
    improvement_areas: List[str] = Field(default_factory=list)
    
    # Metadata
    evaluation_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    evaluator_model: Optional[str] = Field(None, description="Model used for evaluation")
    evaluation_duration_seconds: Optional[float] = None
    
    # Comparison
    expected_answer_points: List[str] = Field(default_factory=list)
    missing_points: List[str] = Field(default_factory=list)
    extra_points: List[str] = Field(default_factory=list)
    
    @field_validator('overall_score')
    @classmethod
    def validate_overall_score(cls, v: float) -> float:
        """Ensure overall score is valid"""
        return max(0.0, min(100.0, v))
    
    @field_validator('score_level', mode='before')
    @classmethod
    def determine_score_level(cls, v: Any, info) -> ScoreLevel:
        """Auto-determine score level from overall score if not provided"""
        if isinstance(v, str):
            return ScoreLevel(v)
        
        # Get overall_score from data
        if hasattr(info, 'data') and 'overall_score' in info.data:
            score = info.data['overall_score']
            if score >= 90:
                return ScoreLevel.EXCELLENT
            elif score >= 70:
                return ScoreLevel.GOOD
            elif score >= 50:
                return ScoreLevel.FAIR
            else:
                return ScoreLevel.POOR
        
        return ScoreLevel.FAIR
    
    def get_weighted_score(self) -> float:
        """Calculate overall weighted score from criterion scores"""
        if not self.criterion_scores:
            return self.overall_score
        
        total_weight = sum(cs.weight for cs in self.criterion_scores)
        if total_weight == 0:
            return self.overall_score
        
        weighted_sum = sum(cs.weighted_score for cs in self.criterion_scores)
        return weighted_sum / total_weight
    
    def add_strength(self, message: str, category: str = "general", priority: str = "medium") -> None:
        """Add a strength feedback item"""
        self.strengths.append(
            FeedbackItem(
                type=FeedbackType.STRENGTH,
                category=category,
                message=message,
                priority=priority
            )
        )
    
    def add_weakness(self, message: str, category: str = "general", priority: str = "high") -> None:
        """Add a weakness feedback item"""
        self.weaknesses.append(
            FeedbackItem(
                type=FeedbackType.WEAKNESS,
                category=category,
                message=message,
                priority=priority
            )
        )
    
    def add_suggestion(
        self, 
        message: str, 
        category: str = "general", 
        priority: str = "medium",
        examples: List[str] = None
    ) -> None:
        """Add a suggestion feedback item"""
        self.suggestions.append(
            FeedbackItem(
                type=FeedbackType.SUGGESTION,
                category=category,
                message=message,
                priority=priority,
                examples=examples or []
            )
        )
    
    def get_high_priority_feedback(self) -> Dict[str, List[FeedbackItem]]:
        """Get all high-priority feedback items"""
        return {
            "strengths": [s for s in self.strengths if s.priority == "high"],
            "weaknesses": [w for w in self.weaknesses if w.priority == "high"],
            "suggestions": [s for s in self.suggestions if s.priority == "high"]
        }
    
    def get_feedback_by_category(self, category: str) -> Dict[str, List[FeedbackItem]]:
        """Get all feedback for a specific category"""
        return {
            "strengths": [s for s in self.strengths if s.category == category],
            "weaknesses": [w for w in self.weaknesses if w.category == category],
            "suggestions": [s for s in self.suggestions if s.category == category]
        }


class EvaluationRequest(BaseModel):
    """Request to evaluate an answer"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "Explain how a LRU cache works",
                "answer": "A LRU cache uses a hash map and doubly linked list...",
                "question_type": "technical",
                "expected_answer_points": [
                    "Hash map for O(1) lookup",
                    "Doubly linked list for ordering",
                    "Move accessed items to front"
                ],
                "evaluation_criteria": ["technical_accuracy", "completeness", "clarity"]
            }
        }
    )
    
    # Question and answer
    question: str = Field(..., description="The interview question")
    answer: str = Field(..., description="Candidate's answer")
    question_type: Literal["technical", "behavioral", "situational", "system_design"] = Field(
        default="technical"
    )
    question_id: Optional[str] = None
    session_id: Optional[str] = None
    
    # Evaluation parameters
    evaluation_criteria: List[str] = Field(
        default_factory=lambda: [
            "technical_accuracy",
            "completeness",
            "clarity",
            "structure"
        ],
        description="Criteria to evaluate against"
    )
    
    # Reference data
    expected_answer_points: List[str] = Field(
        default_factory=list,
        description="Key points expected in a good answer"
    )
    skills_being_tested: List[str] = Field(
        default_factory=list,
        description="Skills this question tests"
    )
    difficulty_level: Literal["easy", "medium", "hard"] = Field(default="medium")
    
    # Context
    candidate_context: Optional[Dict[str, Any]] = Field(
        None,
        description="Candidate background for personalized feedback"
    )
    job_role: Optional[str] = Field(None, description="Target job role")
    experience_level: Optional[str] = Field(None, description="junior, mid, senior")
    
    # Evaluation settings
    detailed_feedback: bool = Field(default=True, description="Include detailed feedback")
    include_examples: bool = Field(default=True, description="Include example improvements")
    strict_mode: bool = Field(default=False, description="Use stricter evaluation criteria")


class BatchEvaluationRequest(BaseModel):
    """Request to evaluate multiple answers"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "sess_123",
                "evaluations": [
                    {"question": "Q1", "answer": "A1"},
                    {"question": "Q2", "answer": "A2"}
                ],
                "generate_summary": True
            }
        }
    )
    
    session_id: str = Field(..., description="Interview session ID")
    evaluations: List[EvaluationRequest] = Field(..., description="List of answers to evaluate")
    generate_summary: bool = Field(default=True, description="Generate overall session summary")
    candidate_context: Optional[Dict[str, Any]] = None


class SessionSummary(BaseModel):
    """Summary of an entire interview session"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "sess_123",
                "total_questions": 5,
                "average_score": 78.5,
                "score_level": "good",
                "strongest_areas": ["technical_accuracy", "examples"],
                "weakest_areas": ["structure", "completeness"]
            }
        }
    )
    
    session_id: str
    total_questions: int
    questions_answered: int
    
    # Overall performance
    average_score: float = Field(..., ge=0, le=100)
    score_level: ScoreLevel
    score_distribution: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of questions per score level"
    )
    
    # Category breakdown
    technical_score: Optional[float] = None
    behavioral_score: Optional[float] = None
    communication_score: Optional[float] = None
    
    # Insights
    strongest_areas: List[str] = Field(default_factory=list)
    weakest_areas: List[str] = Field(default_factory=list)
    consistency_score: Optional[float] = Field(
        None,
        description="How consistent performance was across questions"
    )
    
    # Recommendations
    overall_feedback: Optional[str] = None
    key_strengths: List[str] = Field(default_factory=list)
    areas_for_improvement: List[str] = Field(default_factory=list)
    recommended_resources: List[str] = Field(default_factory=list)
    
    # Hiring recommendation
    hiring_recommendation: Optional[Literal["strong_yes", "yes", "maybe", "no"]] = None
    hiring_justification: Optional[str] = None
    
    # Metadata
    evaluation_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    total_duration_minutes: Optional[float] = None
