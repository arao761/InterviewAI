"""
PrepWise AI - Unified API
=========================

Main API interface that combines all phases into a cohesive system.
This is the primary entry point for using PrepWise AI.
"""

from typing import Dict, List, Optional, Any
from pathlib import Path

from src.resume_parser.parser import ResumeParser
from src.resume_parser.schemas import ParsedResume
from src.question_generator.generator import QuestionGenerator
from src.question_generator.schemas import (
    QuestionGenerationRequest,
    QuestionSet,
    InterviewQuestion
)
from src.evaluator.evaluator import AnswerEvaluator
from src.evaluator.schemas import (
    EvaluationRequest,
    AnswerEvaluation,
    SessionSummary
)
from src.session_manager.manager import SessionManager
from src.session_manager.schemas import (
    SessionCreateRequest,
    InterviewSession,
    InterviewMode,
    SessionType,
    UserProgress,
    ProgressAnalytics,
    LearningPath
)


class PrepWiseAPI:
    """
    Unified API for PrepWise AI Interview Preparation System
    
    This class provides a simple, cohesive interface to all PrepWise AI functionality:
    - Resume parsing and analysis
    - Interview question generation
    - Answer evaluation and feedback
    - Session management
    - Progress tracking and analytics
    
    Example:
        >>> api = PrepWiseAPI()
        >>> resume = api.parse_resume("resume.pdf")
        >>> session = api.create_interview_session(
        ...     candidate_name=resume.contact.name,
        ...     target_role="Software Engineer",
        ...     resume_data=resume
        ... )
        >>> # Conduct interview...
        >>> report = api.get_session_report(session.session_id)
    """
    
    def __init__(self):
        """Initialize PrepWise AI API with all components"""
        self.resume_parser = ResumeParser()
        self.question_generator = QuestionGenerator()
        self.answer_evaluator = AnswerEvaluator()
        self.session_manager = SessionManager()
    
    # ==================== Resume Operations ====================
    
    def parse_resume(
        self,
        file_path: str,
        calculate_stats: bool = True
    ) -> ParsedResume:
        """
        Parse a resume from PDF or DOCX file

        Args:
            file_path: Path to resume file
            calculate_stats: Whether to calculate parsing statistics (ignored for now)

        Returns:
            ParsedResume object with structured data
        """
        # ResumeParser.parse_resume() doesn't accept calculate_stats parameter
        return self.resume_parser.parse_resume(file_path)
    
    def parse_resume_from_text(self, text: str) -> ParsedResume:
        """
        Parse resume from plain text
        
        Args:
            text: Resume text content
            
        Returns:
            ParsedResume object
        """
        return self.resume_parser.parse_resume_from_text(text)
    
    # ==================== Interview Session Operations ====================
    
    def create_interview_session(
        self,
        candidate_name: str,
        target_role: str,
        experience_level: str = "mid",
        target_company: Optional[str] = None,
        user_id: Optional[str] = None,
        mode: InterviewMode = InterviewMode.PRACTICE,
        session_type: SessionType = SessionType.MIXED,
        num_technical: int = 3,
        num_behavioral: int = 2,
        num_system_design: int = 0,
        focus_areas: Optional[List[str]] = None,
        resume_data: Optional[ParsedResume] = None
    ) -> InterviewSession:
        """
        Create a new interview session with generated questions
        
        Args:
            candidate_name: Candidate's name
            target_role: Job role being interviewed for
            experience_level: junior/mid/senior
            target_company: Optional company name
            user_id: Optional user identifier for tracking
            mode: Interview mode (practice/mock/real)
            session_type: Type of interview
            num_technical: Number of technical questions
            num_behavioral: Number of behavioral questions
            num_system_design: Number of system design questions
            focus_areas: Specific topics to focus on
            resume_data: Optional parsed resume for tailored questions
            
        Returns:
            Created interview session
        """
        request = SessionCreateRequest(
            candidate_name=candidate_name,
            user_id=user_id,
            target_role=target_role,
            target_company=target_company,
            experience_level=experience_level,
            mode=mode,
            session_type=session_type,
            num_technical=num_technical,
            num_behavioral=num_behavioral,
            num_system_design=num_system_design,
            focus_areas=focus_areas or [],
            resume_context=resume_data.model_dump() if resume_data else None
        )
        
        return self.session_manager.create_session(request)
    
    def start_session(self, session_id: str) -> InterviewSession:
        """Start an interview session"""
        return self.session_manager.start_session(session_id)
    
    def get_session(self, session_id: str) -> InterviewSession:
        """Get session by ID"""
        return self.session_manager.get_session(session_id)
    
    def get_current_question(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current question in a session
        
        Returns:
            Question details or None if session complete
        """
        session = self.get_session(session_id)
        
        if session.current_question_index >= len(session.responses):
            return None
        
        response = session.responses[session.current_question_index]
        return {
            "index": session.current_question_index,
            "question": response.question_text,
            "type": response.question_type,
            "difficulty": response.question_difficulty,
            "progress": f"{session.current_question_index + 1}/{session.total_questions}"
        }
    
    def submit_answer(
        self,
        session_id: str,
        answer: str,
        time_spent_seconds: int = 0
    ) -> Dict[str, Any]:
        """
        Submit an answer for the current question
        
        Args:
            session_id: Session identifier
            answer: Candidate's answer
            time_spent_seconds: Time spent on question
            
        Returns:
            Evaluation results
        """
        session = self.get_session(session_id)
        current_index = session.current_question_index
        
        response = self.session_manager.submit_answer(
            session_id=session_id,
            question_index=current_index,
            answer_text=answer,
            time_spent_seconds=time_spent_seconds
        )
        
        return {
            "score": response.evaluation_score,
            "feedback": response.feedback_summary,
            "question_index": current_index,
            "questions_remaining": session.total_questions - current_index - 1
        }
    
    def skip_question(self, session_id: str) -> Dict[str, Any]:
        """Skip the current question"""
        session = self.get_session(session_id)
        current_index = session.current_question_index
        
        self.session_manager.skip_question(session_id, current_index)
        
        return {
            "skipped": True,
            "question_index": current_index,
            "questions_remaining": session.total_questions - current_index - 1
        }
    
    def complete_session(self, session_id: str) -> InterviewSession:
        """Complete an interview session and generate final report"""
        return self.session_manager.complete_session(session_id)
    
    def get_session_report(self, session_id: str) -> Dict[str, Any]:
        """
        Get comprehensive session report
        
        Returns:
            Detailed session report with scores, feedback, and recommendations
        """
        session = self.get_session(session_id)
        
        report = {
            "session_id": session.session_id,
            "candidate": session.candidate_name,
            "role": session.target_role,
            "status": session.status.value,
            "overall_score": session.average_score,
            "technical_score": session.technical_score,
            "behavioral_score": session.behavioral_score,
            "questions_answered": session.questions_answered,
            "total_questions": session.total_questions,
            "duration_minutes": session.total_duration_seconds // 60 if session.total_duration_seconds else 0,
            "strengths": session.strengths,
            "weaknesses": session.weaknesses,
            "recommendations": session.recommendations,
            "summary": session.session_summary,
            "questions": []
        }
        
        # Add question details
        for i, response in enumerate(session.responses, 1):
            question_detail = {
                "number": i,
                "question": response.question_text,
                "type": response.question_type,
                "answer": response.answer_text if not response.is_skipped else "(skipped)",
                "score": response.evaluation_score if not response.is_skipped else None,
                "time_spent": response.time_spent_seconds,
                "feedback": response.feedback_summary
            }
            report["questions"].append(question_detail)
        
        return report
    
    # ==================== Progress & Analytics Operations ====================
    
    def get_user_progress(self, user_id: str) -> UserProgress:
        """Get user's overall progress"""
        return self.session_manager.get_user_progress(user_id)
    
    def get_progress_analytics(
        self,
        user_id: str,
        period: str = "30_days"
    ) -> ProgressAnalytics:
        """Get detailed progress analytics"""
        return self.session_manager.get_progress_analytics(user_id, period)
    
    def get_learning_path(self, user_id: str) -> LearningPath:
        """Generate personalized learning path"""
        return self.session_manager.generate_learning_path(user_id)
    
    def get_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get user's achievements and milestones
        
        Returns:
            List of achievements with status
        """
        milestones = self.session_manager.get_milestones(user_id)
        
        achievements = []
        for milestone in milestones:
            achievements.append({
                "id": milestone.milestone_id,
                "title": milestone.title,
                "description": milestone.description,
                "achieved": milestone.achieved,
                "progress": milestone.current_value,
                "threshold": milestone.threshold,
                "reward_points": milestone.reward_points,
                "achieved_at": milestone.achieved_at
            })
        
        return achievements
    
    def compare_sessions(
        self,
        session_id1: str,
        session_id2: str
    ) -> Dict[str, Any]:
        """Compare two interview sessions"""
        comparison = self.session_manager.compare_sessions(session_id1, session_id2)
        return comparison.model_dump()
    
    # ==================== Question Generation Operations ====================
    
    def generate_questions(
        self,
        target_role: str,
        experience_level: str = "mid",
        num_technical: int = 5,
        num_behavioral: int = 3,
        focus_areas: Optional[List[str]] = None,
        resume_data: Optional[ParsedResume] = None,
        target_company: Optional[str] = None
    ) -> QuestionSet:
        """
        Generate interview questions (without creating a session)

        Useful for previewing questions or custom workflows
        """
        request = QuestionGenerationRequest(
            target_role=target_role,
            target_level=experience_level,
            target_company=target_company,
            num_technical=num_technical,
            num_behavioral=num_behavioral,
            focus_areas=focus_areas or [],
            resume_context=resume_data.model_dump() if resume_data else None
        )

        return self.question_generator.generate_questions(request)
    
    # ==================== Evaluation Operations ====================
    
    def evaluate_answer(
        self,
        question: str,
        answer: str,
        question_type: str = "technical",
        expected_points: Optional[List[str]] = None
    ) -> AnswerEvaluation:
        """
        Evaluate a single answer (without session context)
        
        Useful for standalone evaluation or testing
        """
        request = EvaluationRequest(
            question=question,
            answer=answer,
            question_type=question_type,
            expected_answer_points=expected_points or []
        )
        
        return self.answer_evaluator.evaluate_answer(request)
    
    # ==================== Utility Operations ====================
    
    def get_user_sessions(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[InterviewSession]:
        """Get recent sessions for a user"""
        return self.session_manager.get_user_sessions(user_id, limit)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall system statistics
        
        Returns:
            System usage statistics
        """
        return {
            "status": "operational",
            "version": "1.0.0",
            "phases_implemented": 8,
            "features": [
                "Resume Parsing",
                "Question Generation",
                "Answer Evaluation",
                "Session Management",
                "Progress Tracking",
                "Learning Paths",
                "Scoring Engine",
                "Unified API"
            ]
        }


# Convenience function for quick access
def create_api() -> PrepWiseAPI:
    """Create and return a PrepWise API instance"""
    return PrepWiseAPI()
