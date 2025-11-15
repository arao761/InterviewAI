"""
AI Service Integration for PrepWise Backend.

This service integrates the prepwise-ai module into the backend,
providing AI-powered features like resume parsing, question generation,
and response evaluation.
"""
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from fastapi import UploadFile, HTTPException
import tempfile
import aiofiles

# Add prepwise-ai to Python path
prepwise_ai_path = Path(__file__).parent.parent.parent.parent / "prepwise-ai"
sys.path.insert(0, str(prepwise_ai_path))

try:
    from src.api import PrepWiseAPI
except ImportError as e:
    raise ImportError(
        f"Failed to import prepwise-ai module. "
        f"Make sure prepwise-ai is in the parent directory. Error: {e}"
    )

from app.core.config import settings
from app.core.logging import logger


class AIService:
    """
    AI Service for handling all AI/NLP operations.

    This service wraps the PrepWiseAI module and provides
    async-compatible methods for the FastAPI backend.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI Service.

        Args:
            api_key: OpenAI API key (uses settings if not provided)
        """
        self.api_key = api_key or settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be set in environment or settings")

        # Set environment variable for PrepWiseAPI to use
        os.environ["OPENAI_API_KEY"] = self.api_key

        self.ai = PrepWiseAPI()
        logger.info("AI Service initialized successfully")

    async def parse_resume_from_upload(self, file: UploadFile) -> Dict[str, Any]:
        """
        Parse resume from uploaded file.

        Args:
            file: Uploaded resume file (PDF or DOCX)

        Returns:
            Parsed resume data

        Raises:
            HTTPException: If file type is invalid or parsing fails
        """
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="File must have a filename")

        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ['.pdf', '.docx']:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file_ext}. Only PDF and DOCX are supported."
            )

        # Save uploaded file temporarily
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
                temp_path = temp_file.name

                # Write uploaded file to temp location
                content = await file.read()
                temp_file.write(content)

            # Parse resume
            logger.info(f"Parsing resume: {file.filename}")
            parsed_resume = self.ai.parse_resume(temp_path)
            logger.info(f"Successfully parsed resume: {file.filename}")

            # Convert ParsedResume object to dict
            return parsed_resume.model_dump()

        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse resume: {str(e)}"
            )
        finally:
            # Clean up temp file
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)

    async def generate_questions(
        self,
        resume_data: Dict[str, Any],
        interview_type: str = "both",
        domain: Optional[str] = None,
        num_questions: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate interview questions based on resume.

        Args:
            resume_data: Parsed resume data
            interview_type: Type of interview ("behavioral", "technical", "both")
            domain: Technical domain (for technical questions)
            num_questions: Number of questions to generate

        Returns:
            List of generated questions
        """
        try:
            logger.info(
                f"Generating {num_questions} {interview_type} questions "
                f"(domain: {domain or 'N/A'})"
            )

            # Extract target role from resume data or use default
            target_role = "Software Engineer"  # Default

            # Try to get from experience (ParsedResume structure)
            if isinstance(resume_data.get("experience"), list) and len(resume_data["experience"]) > 0:
                # Use most recent job title if available
                exp = resume_data["experience"][0]
                if isinstance(exp, dict):
                    target_role = exp.get("title", target_role)
                else:
                    target_role = getattr(exp, "title", target_role)

            # Determine number of technical vs behavioral questions
            if interview_type == "technical":
                num_technical = num_questions
                num_behavioral = 0
            elif interview_type == "behavioral":
                num_technical = 0
                num_behavioral = num_questions
            else:  # both
                num_technical = num_questions // 2
                num_behavioral = num_questions - num_technical

            # Convert resume dict back to ParsedResume if needed
            resume_obj = None
            try:
                from src.resume_parser.schemas import ParsedResume
                # Only pass resume_obj if we successfully convert it
                if resume_data:
                    resume_obj = ParsedResume(**resume_data)
            except Exception as e:
                logger.warning(f"Could not convert resume_data to ParsedResume: {e}")
                resume_obj = None

            # Use PrepWiseAPI's generate_questions method
            question_set = self.ai.generate_questions(
                target_role=target_role,
                experience_level="mid",  # Could extract this from resume
                num_technical=num_technical,
                num_behavioral=num_behavioral,
                focus_areas=[domain] if domain else [],
                resume_data=resume_obj
            )

            # Convert QuestionSet to list of dicts
            questions = [q.model_dump() for q in question_set.questions]

            logger.info(f"Generated {len(questions)} questions successfully")
            return questions

        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate questions: {str(e)}"
            )

    async def evaluate_response(
        self,
        question: Dict[str, Any],
        transcript: str,
        question_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluate a single interview response.

        Args:
            question: The interview question
            transcript: Candidate's response transcript
            question_type: Type of question ("behavioral" or "technical")

        Returns:
            Evaluation results with score and feedback
        """
        try:
            # Extract question text
            question_text = question.get("question") or question.get("text") or str(question)

            logger.info(f"Evaluating response for question: {question_text[:50]}...")

            # Use PrepWiseAPI's evaluate_answer method
            evaluation = self.ai.evaluate_answer(
                question=question_text,
                answer=transcript,
                question_type=question_type or "technical",
                expected_points=question.get("expected_points")
            )

            # Convert AnswerEvaluation to dict format expected by backend
            evaluation_dict = {
                "score": evaluation.overall_score,
                "score_level": evaluation.score_level.value,
                "strengths": [item.message for item in evaluation.strengths],
                "weaknesses": [item.message for item in evaluation.weaknesses],
                "feedback": evaluation.summary or "",
                "suggestions": [item.message for item in evaluation.suggestions],
                "criterion_scores": [cs.model_dump() for cs in evaluation.criterion_scores],
                "key_takeaways": evaluation.key_takeaways,
                "improvement_areas": evaluation.improvement_areas,
            }

            logger.info(f"Response evaluated - Score: {evaluation.overall_score}")
            return evaluation_dict

        except Exception as e:
            logger.error(f"Error evaluating response: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to evaluate response: {str(e)}"
            )

    async def evaluate_full_interview(
        self,
        questions_and_responses: List[tuple],
        interview_type: str = "mixed"
    ) -> Dict[str, Any]:
        """
        Evaluate entire interview session.

        Args:
            questions_and_responses: List of (question, response) tuples
            interview_type: Type of interview

        Returns:
            Complete interview evaluation report
        """
        try:
            logger.info(
                f"Evaluating full interview with {len(questions_and_responses)} Q&A pairs"
            )

            # Evaluate each question-response pair
            individual_evaluations = []
            total_score = 0
            technical_scores = []
            behavioral_scores = []

            for question, response in questions_and_responses:
                # Determine question type
                q_type = question.get("type", "technical") if isinstance(question, dict) else "technical"

                # Evaluate this response
                evaluation = await self.evaluate_response(
                    question=question,
                    transcript=response,
                    question_type=q_type
                )

                individual_evaluations.append(evaluation)
                total_score += evaluation["score"]

                if q_type == "technical":
                    technical_scores.append(evaluation["score"])
                else:
                    behavioral_scores.append(evaluation["score"])

            # Calculate overall statistics
            overall_score = total_score / len(questions_and_responses) if questions_and_responses else 0

            # Aggregate strengths and weaknesses
            all_strengths = []
            all_weaknesses = []
            all_suggestions = []

            for eval in individual_evaluations:
                all_strengths.extend(eval.get("strengths", []))
                all_weaknesses.extend(eval.get("weaknesses", []))
                all_suggestions.extend(eval.get("suggestions", []))

            # Deduplicate and get top items
            strengths = list(set(all_strengths))[:5]
            weaknesses = list(set(all_weaknesses))[:5]
            recommendations = list(set(all_suggestions))[:5]

            # Create comprehensive report
            report = {
                "overall_score": round(overall_score, 2),
                "technical_score": round(sum(technical_scores) / len(technical_scores), 2) if technical_scores else None,
                "behavioral_score": round(sum(behavioral_scores) / len(behavioral_scores), 2) if behavioral_scores else None,
                "question_scores": [e["score"] for e in individual_evaluations],
                "total_questions": len(questions_and_responses),
                "strengths": strengths,
                "areas_for_improvement": weaknesses,
                "detailed_feedback": f"Evaluated {len(questions_and_responses)} responses. Overall performance: {'Excellent' if overall_score >= 90 else 'Good' if overall_score >= 70 else 'Fair' if overall_score >= 50 else 'Needs Improvement'}.",
                "recommendations": recommendations,
                "individual_evaluations": individual_evaluations,
            }

            logger.info(
                f"Interview evaluation complete - Overall score: {overall_score:.2f}"
            )
            return report

        except Exception as e:
            logger.error(f"Error evaluating interview: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to evaluate interview: {str(e)}"
            )


# Singleton instance
_ai_service: Optional[AIService] = None


def get_ai_service() -> AIService:
    """
    Get or create AI Service singleton instance.

    Returns:
        AIService instance
    """
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
