"""
Pydantic schemas for AI/NLP API endpoints.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from enum import Enum


class InterviewType(str, Enum):
    """Interview type enumeration."""
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    BOTH = "both"
    MIXED = "mixed"


class TechnicalDomain(str, Enum):
    """Technical domain enumeration."""
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
    """Request schema for question generation."""
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
        description="Number of questions to generate"
    )

    class Config:
        extra = "allow"
        json_schema_extra = {
            "example": {
                "resume_data": {
                    "name": "John Doe",
                    "skills": ["Python", "React"],
                    "experience": []
                },
                "interview_type": "both",
                "domain": "web_development",
                "num_questions": 5
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
    """Request schema for response evaluation."""
    question: Dict[str, Any] = Field(..., description="The interview question")
    transcript: str = Field(..., description="Candidate's response transcript")
    question_type: Optional[str] = Field(
        default=None,
        description="Type of question (behavioral/technical)"
    )

    class Config:
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
