"""
AI Service Integration for PrepWise Backend.

This service integrates the ai-engine module into the backend,
providing AI-powered features like resume parsing, question generation,
and response evaluation.
"""
import os
import asyncio
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from fastapi import UploadFile, HTTPException
import tempfile
from app.core.cache import cache_manager

# Import PrepWiseAPI correctly
try:
    from src.api.prepwise_api import PrepWiseAPI
    from src.resume_parser.schemas import ParsedResume
    from src.question_generator.schemas import QuestionSet
except ImportError as e:
    print(f"ERROR: Cannot import PrepWiseAPI. Make sure ai-engine is installed.")
    print(f"Run: cd backend && pip install -e ../ai-engine")
    raise ImportError(f"PrepWise AI not installed: {e}")

from app.core.config import settings
from app.core.logging import logger
from app.services.dsa_generator import DSAGenerator


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
        try:
            self.ai = PrepWiseAPI()
            logger.info("✅ PrepWise AI initialized successfully")
            
            # Initialize DSA generator
            self.dsa_generator = DSAGenerator()
            logger.info("✅ DSA Generator initialized")
            
            # Verify API key is configured
            openai_key = os.getenv("OPENAI_API_KEY")
            if not openai_key or openai_key == "your-openai-api-key-here":
                logger.warning("⚠️  OPENAI_API_KEY not properly configured in .env")
            else:
                logger.info(f"✅ OpenAI API key configured (ends with: ...{openai_key[-4:]})")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize PrepWise AI: {e}")
            raise RuntimeError(f"PrepWise AI initialization failed: {e}")

    async def parse_resume_from_upload(self, file: UploadFile) -> Dict[str, Any]:
        """
        Parse resume from uploaded file with Redis caching for 99% faster duplicate uploads.

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

        # Read file content
        content = await file.read()

        # Check cache using file hash (saves 5-10 seconds for duplicate uploads)
        file_hash = hashlib.sha256(content).hexdigest()
        cache_key = f"resume:hash:{file_hash}"

        cached_result = await cache_manager.get(cache_key)
        if cached_result:
            logger.info(f"✅ Cache HIT for resume {file.filename} (hash: {file_hash[:8]})")
            return json.loads(cached_result)

        logger.info(f"⚠️  Cache MISS for resume {file.filename} - parsing with AI...")

        # Save uploaded file temporarily
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
                temp_path = temp_file.name
                temp_file.write(content)

            # Parse resume with AI (expensive operation)
            logger.info(f"Parsing resume: {file.filename}")
            parsed_resume = self.ai.parse_resume(temp_path)
            logger.info(f"Successfully parsed resume: {file.filename}")

            # Convert ParsedResume object to dict
            result = parsed_resume.model_dump()

            # Cache result for 1 hour (3600 seconds)
            await cache_manager.setex(cache_key, 3600, json.dumps(result))
            logger.info(f"💾 Cached resume parsing result (hash: {file_hash[:8]})")

            return result

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
        num_questions: int = 5,
        company: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate interview questions based on resume.

        Args:
            resume_data: Parsed resume data
            interview_type: Type of interview ("behavioral", "technical", "both")
            domain: Technical domain (for technical questions)
            num_questions: Number of questions to generate
            company: Target company for company-specific questions

        Returns:
            List of generated questions
        """
        try:
            logger.info(
                f"🎯 Generating questions - Type: {interview_type}, "
                f"Domain: {domain or 'N/A'}, Count: {num_questions}, "
                f"Company: {company or 'N/A'}"
            )

            # Extract target role from resume data
            target_role = "Software Engineer"  # Default
            experience_level = "intermediate"  # Default

            # Valid experience levels (frontend format)
            VALID_LEVELS = ["beginner", "intermediate", "advanced"]
            LEVEL_MAPPING = {
                "beginner": "junior",
                "intermediate": "mid",
                "advanced": "senior"
            }

            # Try to extract from resume
            if resume_data:
                # Check for experience level - must be non-None and valid
                raw_level = resume_data.get("experience_level")
                if raw_level and isinstance(raw_level, str) and raw_level.lower() in VALID_LEVELS:
                    experience_level = raw_level.lower()
                elif raw_level:
                    logger.warning(f"⚠️  Invalid experience_level '{raw_level}', defaulting to 'intermediate'")
                    experience_level = "intermediate"

                # Try to infer from total_years_experience if level is still default/invalid
                if experience_level == "intermediate" and "total_years_experience" in resume_data:
                    total_years = resume_data.get("total_years_experience")
                    if total_years is not None and isinstance(total_years, (int, float)):
                        if total_years < 2:
                            experience_level = "beginner"
                        elif total_years >= 7:
                            experience_level = "advanced"
                        else:
                            experience_level = "intermediate"
                        logger.info(f"📊 Inferred experience level from {total_years} years: {experience_level}")

                # Check for job title from experience
                if "experience" in resume_data and isinstance(resume_data["experience"], list):
                    if len(resume_data["experience"]) > 0:
                        first_exp = resume_data["experience"][0]
                        if isinstance(first_exp, dict):
                            # Try multiple keys for job title
                            target_role = first_exp.get("title") or first_exp.get("position") or target_role

            # Final validation - ensure experience_level is never None or invalid
            if not experience_level or experience_level not in VALID_LEVELS:
                logger.warning(f"⚠️  Experience level invalid or None, forcing to 'intermediate'")
                experience_level = "intermediate"

            logger.info(f"📋 Target role: {target_role}, Level: {experience_level}")

            # Determine question split based on interview type
            if interview_type == "technical":
                num_technical = num_questions
                num_behavioral = 0
            elif interview_type == "behavioral":
                num_technical = 0
                num_behavioral = num_questions
            else:  # both
                num_technical = num_questions // 2
                num_behavioral = num_questions - num_technical

            logger.info(f"📊 Question split - Technical: {num_technical}, Behavioral: {num_behavioral}")

            # Check if we need DSA coding questions
            # DSA questions are for technical interviews focused on coding/algorithms
            use_dsa_questions = False
            coding_domains = ["coding", "algorithms", "data structures", "dsa", "leetcode", "competitive programming"]
            
            if interview_type == "technical" and num_technical > 0:
                # For technical interviews, always use DSA questions by default
                # This ensures coding questions are shown for technical interviews
                use_dsa_questions = True
                logger.info("🎯 Technical interview detected - will generate DSA coding questions")
                
                # Check if domain explicitly indicates non-coding (e.g., system design, architecture)
                non_coding_domains = ["system design", "architecture", "infrastructure", "devops", "cloud"]
                if domain and any(non_coding in domain.lower() for non_coding in non_coding_domains):
                    use_dsa_questions = False
                    logger.info("🎯 Non-coding domain detected - will use regular technical questions")
                # Check if domain explicitly indicates coding/DSA (reinforce the decision)
                elif domain and any(coding_domain in domain.lower() for coding_domain in coding_domains):
                    logger.info("🎯 Coding/DSA domain confirmed - will generate DSA questions")
                # Also check if it's a software engineering role (reinforce the decision)
                elif "software" in target_role.lower() or "engineer" in target_role.lower():
                    logger.info("🎯 Software engineering role confirmed - will generate DSA questions")

            # Convert resume_data to ParsedResume if possible
            resume_obj = None
            try:
                if resume_data:
                    resume_obj = ParsedResume(**resume_data)
                    logger.info("✅ Converted resume_data to ParsedResume object")
            except Exception as e:
                logger.warning(f"⚠️  Could not convert to ParsedResume (will use dict): {e}")

            # Generate questions
            questions = []
            
            # Generate DSA coding questions if needed
            if use_dsa_questions and num_technical > 0:
                logger.info(f"💻 Generating {num_technical} DSA coding question(s)")
                
                # Map experience level to difficulty
                difficulty_map = {
                    "beginner": "easy",
                    "intermediate": "medium",
                    "advanced": "hard"
                }
                difficulty = difficulty_map.get(experience_level, "medium")
                
                # Generate DSA questions
                dsa_questions = await self.dsa_generator.generate_dsa_question(
                    difficulty=difficulty,
                    topic=None,  # Let AI choose topic
                    num_questions=num_technical
                )
                
                # Convert DSA questions to standard format
                for dsa_q in dsa_questions:
                    question_dict = {
                        "id": dsa_q.get("title", "dsa_question")[:50],
                        "question": dsa_q.get("problem_statement", ""),
                        "type": "coding",  # Mark as coding question
                        "difficulty": dsa_q.get("difficulty", difficulty),
                        "category": dsa_q.get("topic", "Data Structures & Algorithms"),
                        "dsa_data": dsa_q,  # Store full DSA data
                        "question_type": "coding"  # For frontend
                    }
                    questions.append(question_dict)
                
                logger.info(f"✅ Generated {len(dsa_questions)} DSA question(s)")
            
            # Generate regular technical/behavioral questions if needed
            if not use_dsa_questions or num_behavioral > 0:
            # Generate questions using PrepWise AI
            focus_areas = []
            if domain:
                focus_areas = [domain]
            
            # Extract skills as focus areas if available
            if resume_data and "skills" in resume_data:
                if isinstance(resume_data["skills"], dict) and "technical" in resume_data["skills"]:
                    skills = resume_data["skills"]["technical"]
                    if isinstance(skills, list):
                        focus_areas.extend(skills[:3])  # Top 3 skills
                elif isinstance(resume_data["skills"], list):
                    focus_areas.extend(resume_data["skills"][:3])

            logger.info(f"🔍 Focus areas: {focus_areas}")

            # Final validation before calling PrepWise API
            logger.info(f"🔧 Final params - Role: {target_role}, Level: {experience_level} (type: {type(experience_level).__name__})")

            # Ensure experience_level is a valid string
            if not isinstance(experience_level, str) or experience_level not in VALID_LEVELS:
                logger.error(f"❌ Invalid experience_level before API call: {experience_level}")
                experience_level = "intermediate"
                logger.info(f"✅ Forced experience_level to 'intermediate'")
            
            # Map frontend level to question generator level
            mapped_level = LEVEL_MAPPING.get(experience_level, "mid")
            logger.info(f"🔄 Mapped {experience_level} → {mapped_level} for question generator")

                # Adjust technical count if we already generated DSA questions
                remaining_technical = 0 if use_dsa_questions else num_technical

            # Call PrepWise API with validated parameters
            try:
                question_set = self.ai.generate_questions(
                    target_role=target_role,
                    experience_level=mapped_level,
                        num_technical=remaining_technical,
                    num_behavioral=num_behavioral,
                    focus_areas=focus_areas if focus_areas else None,
                    resume_data=resume_obj,
                    target_company=company
                )
            except Exception as api_error:
                logger.error(f"❌ PrepWise API error: {str(api_error)}")
                # If API call fails, try with minimal parameters
                logger.info(f"🔄 Retrying with minimal parameters...")
                question_set = self.ai.generate_questions(
                    target_role="Software Engineer",
                    experience_level=mapped_level,
                        num_technical=remaining_technical,
                    num_behavioral=num_behavioral,
                    focus_areas=None,
                    resume_data=None,
                    target_company=None
                )

            # Convert questions to dicts
            for q in question_set.questions:
                question_dict = q.model_dump()
                # Ensure required fields for frontend
                question_dict["id"] = question_dict.get("question", "")[:50]  # Generate simple ID
                questions.append(question_dict)

            logger.info(f"✅ Generated {len(questions)} questions successfully")
            
            # Log first question for verification
            if questions:
                logger.info(f"📝 Sample question: {questions[0].get('question', '')[:100]}...")

            return questions

        except Exception as e:
            logger.error(f"❌ Question generation error: {str(e)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
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

            # Evaluate each question-response pair IN PARALLEL for much faster performance
            # Create evaluation tasks for all Q&A pairs
            evaluation_tasks = []
            q_types = []

            for question, response in questions_and_responses:
                # Determine question type
                q_type = question.get("type", "technical") if isinstance(question, dict) else "technical"
                q_types.append(q_type)

                # Create async task (don't await yet)
                task = self.evaluate_response(
                    question=question,
                    transcript=response,
                    question_type=q_type
                )
                evaluation_tasks.append(task)

            # Execute all evaluations in parallel using asyncio.gather()
            # This reduces evaluation time from N×10s to ~10s for any N questions
            logger.info(f"Starting parallel evaluation of {len(evaluation_tasks)} questions...")
            individual_evaluations = await asyncio.gather(*evaluation_tasks)
            logger.info("Parallel evaluation completed!")

            # Calculate scores from results
            total_score = 0
            technical_scores = []
            behavioral_scores = []

            for evaluation, q_type in zip(individual_evaluations, q_types):
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
