"""
AI/NLP API Routes for PrepWise Backend.

This module provides REST API endpoints for AI-powered features:
- Resume parsing
- Interview question generation
- Response evaluation
- Full interview evaluation
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import Dict, Any
import traceback

from app.schemas.ai_schemas import (
    ResumeParseResponse,
    QuestionGenerationRequest,
    QuestionGenerationResponse,
    ResponseEvaluationRequest,
    ResponseEvaluationResponse,
    InterviewEvaluationRequest,
    InterviewEvaluationResponse,
    ErrorResponse,
)
from app.services.ai_service import get_ai_service, AIService
from app.core.logging import logger


router = APIRouter(
    prefix="/ai",
    tags=["AI/NLP"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
        400: {"model": ErrorResponse, "description": "Bad request"},
    },
)


@router.post(
    "/parse-resume",
    response_model=ResumeParseResponse,
    summary="Parse Resume",
    description="Upload and parse a resume (PDF or DOCX) to extract structured data",
)
async def parse_resume(
    file: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
    ai_service: AIService = Depends(get_ai_service),
) -> ResumeParseResponse:
    """
    Parse a resume file and extract structured information.

    - **file**: Upload a PDF or DOCX resume file
    - Returns parsed resume data including name, contact, skills, experience, education
    """
    try:
        logger.info(f"📤 Received resume upload: {file.filename}")

        # Parse resume using AI service
        resume_data = await ai_service.parse_resume_from_upload(file)

        return ResumeParseResponse(
            success=True,
            data=resume_data,
            message="Resume parsed successfully",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Resume parsing failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse resume: {str(e)}"
        )


@router.post(
    "/generate-questions",
    response_model=QuestionGenerationResponse,
    summary="Generate Interview Questions",
    description="Generate tailored interview questions based on parsed resume data",
)
async def generate_questions(
    request: QuestionGenerationRequest,
    ai_service: AIService = Depends(get_ai_service),
) -> QuestionGenerationResponse:
    """
    Generate interview questions tailored to candidate's resume.

    - **resume_data**: Parsed resume data (from /parse-resume endpoint)
    - **interview_type**: Type of questions (behavioral, technical, or both)
    - **domain**: Technical domain (required for technical questions)
    - **num_questions**: Number of questions to generate (1-20)
    """
    try:
        logger.info(
            f"📝 Question generation request - "
            f"Type: {request.interview_type}, "
            f"Domain: {request.domain}, "
            f"Count: {request.num_questions}"
        )
        
        # Log resume data summary
        if request.resume_data:
            logger.info(f"📋 Resume data keys: {list(request.resume_data.keys())}")
        
        # Generate questions
        questions = await ai_service.generate_questions(
            resume_data=request.resume_data or {},
            interview_type=request.interview_type.value,
            domain=request.domain.value if request.domain else None,
            num_questions=request.num_questions,
        )

        logger.info(f"✅ Generated {len(questions)} questions")
        
        return QuestionGenerationResponse(
            success=True,
            questions=questions,
            count=len(questions),
            message=f"Generated {len(questions)} questions successfully",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Question generation failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate questions: {str(e)}"
        )


@router.post(
    "/evaluate-response",
    response_model=ResponseEvaluationResponse,
    summary="Evaluate Interview Response",
    description="Evaluate a candidate's response to a single interview question",
)
async def evaluate_response(
    request: ResponseEvaluationRequest,
    ai_service: AIService = Depends(get_ai_service),
) -> ResponseEvaluationResponse:
    """
    Evaluate a single interview response.

    - **question**: The interview question asked
    - **transcript**: The candidate's response (text)
    - **question_type**: Type of question (behavioral or technical)
    - Returns evaluation with score, strengths, weaknesses, and feedback
    """
    try:
        logger.info(f"Evaluating response for question type: {request.question_type}")

        # Evaluate response
        evaluation = await ai_service.evaluate_response(
            question=request.question,
            transcript=request.transcript,
            question_type=request.question_type,
        )

        return ResponseEvaluationResponse(
            success=True,
            evaluation=evaluation,
            message="Response evaluated successfully",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in evaluate_response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/evaluate-interview",
    response_model=InterviewEvaluationResponse,
    summary="Evaluate Full Interview",
    description="Evaluate a complete interview session with multiple questions and responses",
)
async def evaluate_interview(
    request: InterviewEvaluationRequest,
    ai_service: AIService = Depends(get_ai_service),
) -> InterviewEvaluationResponse:
    """
    Evaluate a full interview session.

    - **questions_and_responses**: List of question-response pairs
    - **interview_type**: Type of interview (behavioral, technical, or mixed)
    - Returns comprehensive evaluation report with overall score and feedback
    """
    try:
        logger.info(
            f"Evaluating full interview - Type: {request.interview_type}, "
            f"Questions: {len(request.questions_and_responses)}"
        )

        # Convert request data to format expected by AI service
        qa_pairs = [
            (item["question"], item["response"])
            for item in request.questions_and_responses
        ]

        # Evaluate full interview
        report = await ai_service.evaluate_full_interview(
            questions_and_responses=qa_pairs,
            interview_type=request.interview_type.value,
        )

        return InterviewEvaluationResponse(
            success=True,
            report=report,
            message="Interview evaluated successfully",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in evaluate_interview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/health",
    summary="AI Service Health Check",
    description="Check if AI service is initialized and ready",
)
async def ai_health_check(
    ai_service: AIService = Depends(get_ai_service),
) -> Dict[str, Any]:
    """
    Health check for AI service.

    Returns status and configuration info.
    """
    import os
    return {
        "status": "healthy",
        "service": "AI/NLP Service",
        "model": "PrepWise AI (Multi-Model Support)",
        "ready": True,
        "api_key_configured": bool(os.getenv("OPENAI_API_KEY")),
    }
