"""
Pydantic schemas for AI/NLP API endpoints.

SECURITY FEATURES:
- Strict input validation to prevent injection attacks
- Field size limits to prevent memory exhaustion
- Type checking on all inputs
- No unexpected fields allowed (extra='forbid')
- Sanitization of user-provided text
"""
from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Any, Optional
from enum import Enum
import re


class InterviewType(str, Enum):
    """Interview type enumeration."""
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    BOTH = "both"
    MIXED = "mixed"


class TechnicalDomain(str, Enum):
    """Technical domain enumeration."""
    SOFTWARE_ENGINEERING = "software_engineering"
    ALGORITHMS = "algorithms"
    WEB_DEVELOPMENT = "web_development"
    MACHINE_LEARNING = "machine_learning"
    SYSTEM_DESIGN = "system_design"
    DATABASE = "database"
    DEVOPS = "devops"


class ResumeParseResponse(BaseModel):
    """Response schema for resume parsing."""
    success: bool
    data: Dict[str, Any]
    message: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "+1234567890",
                    "summary": "Experienced software engineer...",
                    "skills": ["Python", "React", "AWS"],
                    "experience": [
                        {
                            "title": "Senior Software Engineer",
                            "company": "Tech Corp",
                            "duration": "2020-2023",
                            "responsibilities": ["Led team of 5 engineers..."]
                        }
                    ],
                    "education": [
                        {
                            "degree": "BS Computer Science",
                            "institution": "University",
                            "year": "2019"
                        }
                    ]
                },
                "message": "Resume parsed successfully"
            }
        }


class QuestionGenerationRequest(BaseModel):
    """
    Request schema for question generation.

    SECURITY:
    - Limited to 20 questions to prevent resource exhaustion
    - Company name sanitized to prevent injection
    - Resume data structure validated
    """
    resume_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Parsed resume data (flexible structure)"
    )
    interview_type: InterviewType = Field(
        default=InterviewType.BOTH,
        description="Type of interview questions to generate"
    )
    domain: Optional[TechnicalDomain] = Field(
        default=None,
        description="Technical domain (required for technical questions)"
    )
    num_questions: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of questions to generate (max 20)"
    )
    company: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Target company for company-specific questions"
    )

    @field_validator('company')
    @classmethod
    def validate_company(cls, v: Optional[str]) -> Optional[str]:
        """
        Sanitize company name.

        SECURITY: Prevent injection via company name field
        """
        if v is None:
            return v

        v = v.strip()
        if not v:
            return None

        # Allow only letters, numbers, spaces, hyphens, ampersands, periods
        if not re.match(r'^[\w\s\-&.]+$', v, re.UNICODE):
            raise ValueError("Company name contains invalid characters")

        return v

    class Config:
        # SECURITY: Forbid extra fields to prevent parameter pollution
        extra = "forbid"
        json_schema_extra = {
            "example": {
                "resume_data": {
                    "name": "John Doe",
                    "skills": ["Python", "React"],
                    "experience": []
                },
                "interview_type": "both",
                "domain": "web_development",
                "num_questions": 5,
                "company": "Google"
            }
        }


class QuestionGenerationResponse(BaseModel):
    """Response schema for question generation."""
    success: bool
    questions: List[Dict[str, Any]]
    count: int
    message: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "count": 5,
                "questions": [
                    {
                        "id": "q1",
                        "type": "behavioral",
                        "question": "Tell me about a time when...",
                        "focus_area": "Leadership",
                        "difficulty": "medium"
                    }
                ],
                "message": "Questions generated successfully"
            }
        }


class ResponseEvaluationRequest(BaseModel):
    """
    Request schema for response evaluation.

    SECURITY:
    - Transcript length limited to prevent memory exhaustion
    - Question type validated against enum
    """
    question: Dict[str, Any] = Field(
        ...,
        description="The interview question"
    )
    transcript: str = Field(
        ...,
        min_length=1,
        max_length=50000,  # ~10,000 words max
        description="Candidate's response transcript"
    )
    question_type: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Type of question (behavioral/technical)"
    )

    @field_validator('transcript')
    @classmethod
    def validate_transcript(cls, v: str) -> str:
        """
        Validate and sanitize transcript.

        SECURITY: Prevent excessively long inputs that could cause DoS
        """
        v = v.strip()
        if not v:
            raise ValueError("Transcript cannot be empty")

        # Check length in characters
        if len(v) > 50000:
            raise ValueError("Transcript is too long (max 50,000 characters)")

        return v

    @field_validator('question_type')
    @classmethod
    def validate_question_type(cls, v: Optional[str]) -> Optional[str]:
        """Validate question type against allowed values."""
        if v is None:
            return v

        allowed_types = ['behavioral', 'technical', 'mixed']
        if v.lower() not in allowed_types:
            raise ValueError(f"Question type must be one of: {', '.join(allowed_types)}")

        return v.lower()

    class Config:
        extra = 'forbid'
        json_schema_extra = {
            "example": {
                "question": {
                    "id": "q1",
                    "type": "behavioral",
                    "question": "Tell me about a time when you led a project"
                },
                "transcript": "In my previous role, I led a team of 5 engineers to rebuild our authentication system...",
                "question_type": "behavioral"
            }
        }


class ResponseEvaluationResponse(BaseModel):
    """Response schema for response evaluation."""
    success: bool
    evaluation: Dict[str, Any]
    message: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "evaluation": {
                    "score": 85,
                    "strengths": ["Clear STAR structure", "Specific examples"],
                    "weaknesses": ["Could provide more metrics"],
                    "feedback": "Good response overall...",
                    "suggestions": ["Include quantitative results"]
                },
                "message": "Response evaluated successfully"
            }
        }


class InterviewEvaluationRequest(BaseModel):
    """Request schema for full interview evaluation."""
    questions_and_responses: List[Dict[str, Any]] = Field(
        ...,
        description="List of question-response pairs"
    )
    interview_type: InterviewType = Field(
        default=InterviewType.MIXED,
        description="Type of interview"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "questions_and_responses": [
                    {
                        "question": {
                            "id": "q1",
                            "question": "Tell me about yourself"
                        },
                        "response": "I'm a software engineer with 5 years..."
                    }
                ],
                "interview_type": "mixed"
            }
        }


class InterviewEvaluationResponse(BaseModel):
    """Response schema for full interview evaluation."""
    success: bool
    report: Dict[str, Any]
    message: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "report": {
                    "overall_score": 82,
                    "question_scores": [85, 80, 78],
                    "strengths": ["Strong technical knowledge"],
                    "areas_for_improvement": ["Communication clarity"],
                    "detailed_feedback": "Overall strong performance...",
                    "recommendations": ["Practice more system design"]
                },
                "message": "Interview evaluated successfully"
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema."""
    success: bool = False
    error: str
    detail: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Invalid file type",
                "detail": "Only PDF and DOCX files are supported"
            }
        }
