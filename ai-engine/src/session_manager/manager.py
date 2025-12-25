"""
Session Manager
Manages interview sessions and user progress tracking
"""

from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
import json
from pathlib import Path
import statistics

from src.session_manager.schemas import (
    InterviewSession,
    SessionCreateRequest,
    QuestionResponse,
    SessionStatus,
    InterviewMode,
    UserProgress,
    ProgressAnalytics,
    SessionComparison,
    Milestone,
    LearningPath
)
from src.question_generator.generator import QuestionGenerator
from src.question_generator.schemas import QuestionGenerationRequest
from src.evaluator.evaluator import AnswerEvaluator
from src.evaluator.schemas import EvaluationRequest


class SessionManager:
    """Manages interview sessions and progress"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize session manager
        
        Args:
            data_dir: Directory to store session data
        """
        self.data_dir = data_dir or Path("data/sessions")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.question_generator = QuestionGenerator()
        self.answer_evaluator = AnswerEvaluator()
        
        # In-memory cache
        self._sessions: Dict[str, InterviewSession] = {}
        self._user_progress: Dict[str, UserProgress] = {}
    
    def create_session(
        self,
        request: SessionCreateRequest
    ) -> InterviewSession:
        """
        Create a new interview session
        
        Args:
            request: Session creation request
            
        Returns:
            Created interview session
        """
        # Generate questions for the session
        question_request = QuestionGenerationRequest(
            target_role=request.target_role,
            target_level=request.experience_level,
            target_company=request.target_company,
            num_technical=request.num_technical,
            num_behavioral=request.num_behavioral,
            num_system_design=request.num_system_design,
            focus_areas=request.focus_areas,
            resume_context=request.resume_context
        )
        
        questions = self.question_generator.generate_questions(question_request)
        
        # Create session
        session = InterviewSession(
            candidate_name=request.candidate_name,
            candidate_email=request.candidate_email,
            user_id=request.user_id,
            target_role=request.target_role,
            target_company=request.target_company,
            experience_level=request.experience_level,
            mode=request.mode,
            session_type=request.session_type,
            total_questions=len(questions.questions),
            resume_summary=request.resume_context
        )
        
        # Store questions as metadata (not full responses yet)
        session.responses = [
            QuestionResponse(
                question_id=f"q_{i}",
                question_text=q.question,
                question_type=q.type.value,
                question_difficulty=q.difficulty.value
            )
            for i, q in enumerate(questions.questions)
        ]
        
        # Reset counters
        session.questions_answered = 0
        session.questions_skipped = 0
        
        # Save session
        self._save_session(session)
        self._sessions[session.session_id] = session
        
        return session
    
    def start_session(self, session_id: str) -> InterviewSession:
        """
        Start an interview session
        
        Args:
            session_id: Session identifier
            
        Returns:
            Updated session
        """
        session = self.get_session(session_id)
        
        if session.status != SessionStatus.SCHEDULED:
            raise ValueError(f"Session {session_id} is not in scheduled state")
        
        session.status = SessionStatus.IN_PROGRESS
        session.started_at = datetime.now().isoformat()
        session.updated_at = datetime.now().isoformat()
        
        self._save_session(session)
        return session
    
    def submit_answer(
        self,
        session_id: str,
        question_index: int,
        answer_text: str,
        time_spent_seconds: int = 0
    ) -> QuestionResponse:
        """
        Submit an answer for a question
        
        Args:
            session_id: Session identifier
            question_index: Index of question being answered
            answer_text: Candidate's answer
            time_spent_seconds: Time spent on question
            
        Returns:
            Updated question response with evaluation
        """
        session = self.get_session(session_id)
        
        if question_index >= len(session.responses):
            raise ValueError(f"Invalid question index: {question_index}")
        
        response = session.responses[question_index]
        
        # Update response
        response.answer_text = answer_text
        response.time_spent_seconds = time_spent_seconds
        response.answered_at = datetime.now().isoformat()
        response.is_skipped = False
        
        # Evaluate answer
        eval_request = EvaluationRequest(
            question=response.question_text,
            answer=answer_text,
            question_type=response.question_type,
            difficulty_level=response.question_difficulty,
            session_id=session_id
        )
        
        evaluation = self.answer_evaluator.evaluate_answer(eval_request)
        
        # Store evaluation results
        response.evaluation_score = evaluation.overall_score
        response.evaluation_id = evaluation.evaluation_id
        response.feedback_summary = evaluation.summary
        
        # Update session counters
        if session.responses[question_index].is_skipped:
            session.questions_skipped -= 1
        session.questions_answered += 1
        session.current_question_index = question_index + 1
        session.updated_at = datetime.now().isoformat()
        
        # Recalculate metrics
        session.calculate_metrics()
        
        self._save_session(session)
        
        return response
    
    def skip_question(
        self,
        session_id: str,
        question_index: int
    ) -> QuestionResponse:
        """
        Skip a question
        
        Args:
            session_id: Session identifier
            question_index: Index of question to skip
            
        Returns:
            Updated question response
        """
        session = self.get_session(session_id)
        
        if question_index >= len(session.responses):
            raise ValueError(f"Invalid question index: {question_index}")
        
        response = session.responses[question_index]
        response.is_skipped = True
        response.answered_at = datetime.now().isoformat()
        
        session.questions_skipped += 1
        session.current_question_index = question_index + 1
        session.updated_at = datetime.now().isoformat()
        
        self._save_session(session)
        
        return response
    
    def complete_session(self, session_id: str) -> InterviewSession:
        """
        Complete an interview session
        
        Args:
            session_id: Session identifier
            
        Returns:
            Completed session with final metrics
        """
        session = self.get_session(session_id)
        
        session.status = SessionStatus.COMPLETED
        session.completed_at = datetime.now().isoformat()
        session.updated_at = datetime.now().isoformat()
        
        # Calculate final metrics
        session.calculate_metrics()
        
        # Generate session summary using evaluator
        evaluations = []
        for response in session.responses:
            if not response.is_skipped and response.evaluation_id:
                # Create minimal evaluation object for summary
                from src.evaluator.schemas import AnswerEvaluation, ScoreLevel
                eval_obj = AnswerEvaluation(
                    evaluation_id=response.evaluation_id,
                    question_id=response.question_id,
                    answer_text=response.answer_text or "",
                    question_text=response.question_text,
                    question_type=response.question_type,
                    overall_score=response.evaluation_score or 0,
                    score_level=self._score_to_level(response.evaluation_score or 0)
                )
                evaluations.append(eval_obj)
        
        if evaluations:
            summary = self.answer_evaluator.generate_session_summary(
                session_id=session_id,
                evaluations=evaluations
            )
            
            session.session_summary = summary.overall_feedback
            session.strengths = summary.key_strengths
            session.weaknesses = summary.areas_for_improvement
            session.recommendations = summary.recommended_resources
        
        self._save_session(session)
        
        # Update user progress
        if session.user_id:
            self._update_user_progress(session)
        
        return session
    
    def get_session(self, session_id: str) -> InterviewSession:
        """
        Get session by ID
        
        Args:
            session_id: Session identifier
            
        Returns:
            Interview session
        """
        if session_id in self._sessions:
            return self._sessions[session_id]
        
        # Load from disk
        session = self._load_session(session_id)
        self._sessions[session_id] = session
        return session
    
    def get_user_sessions(
        self,
        user_id: str,
        limit: int = 10,
        status: Optional[SessionStatus] = None
    ) -> List[InterviewSession]:
        """
        Get sessions for a user
        
        Args:
            user_id: User identifier
            limit: Maximum number of sessions to return
            status: Filter by session status
            
        Returns:
            List of sessions
        """
        sessions = []
        
        # Load all sessions from disk (in production, use database query)
        for session_file in self.data_dir.glob(f"session_*.json"):
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)
                    if data.get('user_id') == user_id:
                        session = InterviewSession(**data)
                        if status is None or session.status == status:
                            sessions.append(session)
            except Exception as e:
                print(f"Error loading session {session_file}: {e}")
                continue
        
        # Sort by created_at descending
        sessions.sort(key=lambda s: s.created_at, reverse=True)
        
        return sessions[:limit]
    
    def get_user_progress(self, user_id: str) -> UserProgress:
        """
        Get user's progress summary
        
        Args:
            user_id: User identifier
            
        Returns:
            User progress summary
        """
        if user_id in self._user_progress:
            return self._user_progress[user_id]
        
        # Calculate progress from sessions
        sessions = self.get_user_sessions(user_id, limit=1000)
        
        if not sessions:
            # Create new progress
            progress = UserProgress(
                user_id=user_id,
                username=user_id
            )
        else:
            progress = self._calculate_user_progress(user_id, sessions)
        
        self._user_progress[user_id] = progress
        self._save_user_progress(progress)
        
        return progress
    
    def get_progress_analytics(
        self,
        user_id: str,
        period: str = "30_days"
    ) -> ProgressAnalytics:
        """
        Get detailed progress analytics
        
        Args:
            user_id: User identifier
            period: Time period for analytics
            
        Returns:
            Progress analytics
        """
        sessions = self.get_user_sessions(user_id, limit=1000)
        completed_sessions = [s for s in sessions if s.status == SessionStatus.COMPLETED]
        
        # Filter by period
        if period != "all_time":
            days = int(period.split("_")[0])
            cutoff_date = datetime.now() - timedelta(days=days)
            completed_sessions = [
                s for s in completed_sessions
                if datetime.fromisoformat(s.created_at) >= cutoff_date
            ]
        
        analytics = ProgressAnalytics(
            user_id=user_id,
            period=period,
            sessions_completed=len(completed_sessions)
        )
        
        if not completed_sessions:
            return analytics
        
        # Calculate metrics
        scores = [s.average_score for s in completed_sessions if s.average_score]
        if scores:
            analytics.average_score = sum(scores) / len(scores)
            analytics.median_score = statistics.median(scores)
            if len(scores) > 1:
                analytics.score_variance = statistics.variance(scores)
        
        # Session breakdown
        analytics.sessions_by_type = {}
        analytics.sessions_by_mode = {}
        
        for session in completed_sessions:
            # By type
            type_key = session.session_type.value
            analytics.sessions_by_type[type_key] = analytics.sessions_by_type.get(type_key, 0) + 1
            
            # By mode
            mode_key = session.mode.value
            analytics.sessions_by_mode[mode_key] = analytics.sessions_by_mode.get(mode_key, 0) + 1
        
        # Technical vs behavioral scores
        for session in completed_sessions:
            if session.technical_score:
                analytics.technical_scores.append(session.technical_score)
            if session.behavioral_score:
                analytics.behavioral_scores.append(session.behavioral_score)
        
        # Improvement calculation
        if len(scores) >= 2:
            first_half = scores[:len(scores)//2]
            second_half = scores[len(scores)//2:]
            
            avg_first = sum(first_half) / len(first_half)
            avg_second = sum(second_half) / len(second_half)
            
            if avg_first > 0:
                analytics.improvement_percentage = ((avg_second - avg_first) / avg_first) * 100
        
        # Time analysis
        durations = [s.total_duration_seconds for s in completed_sessions if s.total_duration_seconds]
        if durations:
            analytics.total_practice_time_hours = sum(durations) / 3600
            analytics.average_session_duration_minutes = (sum(durations) / len(durations)) / 60
        
        # Score trends by date
        for session in completed_sessions:
            date_key = session.created_at.split('T')[0]
            if session.average_score:
                analytics.score_by_date[date_key] = session.average_score
            analytics.questions_by_date[date_key] = analytics.questions_by_date.get(date_key, 0) + session.questions_answered
        
        # Generate recommendations
        analytics.focus_recommendations = self._generate_recommendations(completed_sessions)
        analytics.next_steps = self._generate_next_steps(analytics)
        
        return analytics
    
    def compare_sessions(
        self,
        session_id1: str,
        session_id2: str
    ) -> SessionComparison:
        """
        Compare two sessions
        
        Args:
            session_id1: First session ID
            session_id2: Second session ID
            
        Returns:
            Session comparison
        """
        session1 = self.get_session(session_id1)
        session2 = self.get_session(session_id2)
        
        if session1.user_id != session2.user_id:
            raise ValueError("Sessions must belong to the same user")
        
        score1 = session1.average_score or 0
        score2 = session2.average_score or 0
        
        duration1 = session1.total_duration_seconds or 0
        duration2 = session2.total_duration_seconds or 0
        
        comparison = SessionComparison(
            session_ids=[session_id1, session_id2],
            user_id=session1.user_id or session2.user_id or "unknown",
            scores=[score1, score2],
            score_improvement=score2 - score1,
            average_score_change=(score2 - score1) / 2 if score1 > 0 else 0,
            durations=[duration1, duration2],
            time_improvement=duration2 - duration1,
            better_session=session_id2 if score2 > score1 else session_id1
        )
        
        # Technical comparison
        if session1.technical_score and session2.technical_score:
            comparison.technical_comparison = {
                session_id1: session1.technical_score,
                session_id2: session2.technical_score,
                "improvement": session2.technical_score - session1.technical_score
            }
        
        # Behavioral comparison
        if session1.behavioral_score and session2.behavioral_score:
            comparison.behavioral_comparison = {
                session_id1: session1.behavioral_score,
                session_id2: session2.behavioral_score,
                "improvement": session2.behavioral_score - session1.behavioral_score
            }
        
        # Identify improvement/regression areas
        strengths1 = set(session1.strengths)
        strengths2 = set(session2.strengths)
        weaknesses1 = set(session1.weaknesses)
        weaknesses2 = set(session2.weaknesses)
        
        comparison.improvement_areas = list(weaknesses1 - weaknesses2)
        comparison.regression_areas = list(weaknesses2 - weaknesses1)
        
        # Consistency score
        comparison.consistency_score = 100 - abs(score2 - score1)
        
        return comparison
    
    def generate_learning_path(self, user_id: str) -> LearningPath:
        """
        Generate personalized learning path
        
        Args:
            user_id: User identifier
            
        Returns:
            Learning path recommendation
        """
        progress = self.get_user_progress(user_id)
        
        # Determine current level
        avg_score = progress.average_score
        if avg_score < 60:
            current_level = "beginner"
            target_level = "intermediate"
        elif avg_score < 80:
            current_level = "intermediate"
            target_level = "advanced"
        else:
            current_level = "advanced"
            target_level = "expert"
        
        learning_path = LearningPath(
            user_id=user_id,
            current_level=current_level,
            target_level=target_level,
            strengths=progress.top_strengths,
            weaknesses=progress.top_weaknesses,
            skill_gaps=progress.needs_practice
        )
        
        # Recommended focus areas
        learning_path.recommended_focus = progress.needs_practice[:5] if progress.needs_practice else ["general practice"]
        
        # Recommended topics with priority
        for weakness in progress.top_weaknesses[:3]:
            learning_path.recommended_topics.append({
                "topic": weakness,
                "priority": "high",
                "current_proficiency": "needs_improvement",
                "target_proficiency": "proficient"
            })
        
        # Session frequency
        if progress.total_sessions < 5:
            learning_path.recommended_session_frequency = "3-4 times per week"
        elif progress.total_sessions < 20:
            learning_path.recommended_session_frequency = "2-3 times per week"
        else:
            learning_path.recommended_session_frequency = "2 times per week"
        
        # Estimate completion time
        sessions_needed = max(12 - progress.completed_sessions, 4)
        weeks_needed = sessions_needed // 3
        learning_path.estimated_completion_weeks = max(weeks_needed, 2)
        
        # Milestones
        learning_path.milestones = [
            f"Complete {sessions_needed//3} more sessions",
            f"Achieve average score of {avg_score + 10}/100",
            f"Master {', '.join(progress.needs_practice[:2])}",
            "Complete 3 mock interviews"
        ]
        
        # Resources
        learning_path.suggested_resources = [
            "LeetCode - Daily Coding Challenge",
            "System Design Primer",
            "Cracking the Coding Interview",
            "Behavioral Interview Questions Guide"
        ]
        
        return learning_path
    
    def _score_to_level(self, score: float):
        """Convert score to score level"""
        from src.evaluator.schemas import ScoreLevel
        if score >= 90:
            return ScoreLevel.EXCELLENT
        elif score >= 70:
            return ScoreLevel.GOOD
        elif score >= 50:
            return ScoreLevel.FAIR
        else:
            return ScoreLevel.POOR
    
    def _calculate_user_progress(
        self,
        user_id: str,
        sessions: List[InterviewSession]
    ) -> UserProgress:
        """Calculate user progress from sessions"""
        completed = [s for s in sessions if s.status == SessionStatus.COMPLETED]
        
        progress = UserProgress(
            user_id=user_id,
            username=user_id,
            total_sessions=len(sessions),
            completed_sessions=len(completed)
        )
        
        if not completed:
            return progress
        
        # Calculate statistics
        progress.total_questions_answered = sum(s.questions_answered for s in completed)
        
        durations = [s.total_duration_seconds for s in completed if s.total_duration_seconds]
        if durations:
            progress.total_time_spent_hours = sum(durations) / 3600
        
        # Score statistics
        scores = [s.average_score for s in completed if s.average_score]
        if scores:
            progress.average_score = sum(scores) / len(scores)
            progress.best_score = max(scores)
            progress.worst_score = min(scores)
            progress.score_trend = scores[-10:]  # Last 10 sessions
        
        # Technical vs behavioral
        tech_scores = [s.technical_score for s in completed if s.technical_score]
        beh_scores = [s.behavioral_score for s in completed if s.behavioral_score]
        
        if tech_scores:
            progress.technical_average = sum(tech_scores) / len(tech_scores)
        if beh_scores:
            progress.behavioral_average = sum(beh_scores) / len(beh_scores)
        
        # Improvement rate
        if len(scores) >= 2:
            first_half = scores[:len(scores)//2]
            second_half = scores[len(scores)//2:]
            
            avg_first = sum(first_half) / len(first_half)
            avg_second = sum(second_half) / len(second_half)
            
            if avg_first > 0:
                progress.improvement_rate = ((avg_second - avg_first) / avg_first) * 100
        
        # Aggregate strengths and weaknesses
        all_strengths = []
        all_weaknesses = []
        
        for session in completed:
            all_strengths.extend(session.strengths)
            all_weaknesses.extend(session.weaknesses)
        
        # Get top 5 most common
        from collections import Counter
        strength_counter = Counter(all_strengths)
        weakness_counter = Counter(all_weaknesses)
        
        progress.top_strengths = [s for s, _ in strength_counter.most_common(5)]
        progress.top_weaknesses = [w for w, _ in weakness_counter.most_common(5)]
        
        # Determine mastered topics and needs practice
        progress.mastered_topics = progress.top_strengths[:3]
        progress.needs_practice = progress.top_weaknesses[:3]
        
        # Recent sessions
        progress.recent_sessions = [s.session_id for s in sessions[:5]]
        progress.last_session_date = completed[0].created_at if completed else None
        
        return progress
    
    def _update_user_progress(self, session: InterviewSession) -> None:
        """Update user progress after session completion"""
        if not session.user_id:
            return
        
        progress = self.get_user_progress(session.user_id)
        
        # Recalculate from all sessions
        sessions = self.get_user_sessions(session.user_id, limit=1000)
        updated_progress = self._calculate_user_progress(session.user_id, sessions)
        
        # Update cache
        self._user_progress[session.user_id] = updated_progress
        self._save_user_progress(updated_progress)
    
    def _generate_recommendations(self, sessions: List[InterviewSession]) -> List[str]:
        """Generate focus recommendations"""
        recommendations = []
        
        if not sessions:
            return ["Start with practice sessions to build confidence"]
        
        latest = sessions[0]
        
        if latest.average_score and latest.average_score < 70:
            recommendations.append("Focus on fundamental concepts")
        
        if latest.technical_score and latest.technical_score < latest.average_score:
            recommendations.append("Strengthen technical interview skills")
        
        if latest.behavioral_score and latest.behavioral_score < latest.average_score:
            recommendations.append("Practice behavioral questions using STAR method")
        
        if latest.questions_skipped > latest.questions_answered * 0.2:
            recommendations.append("Work on time management and confidence")
        
        return recommendations or ["Continue consistent practice"]
    
    def _generate_next_steps(self, analytics: ProgressAnalytics) -> List[str]:
        """Generate next steps"""
        steps = []
        
        if analytics.sessions_completed < 5:
            steps.append("Complete at least 5 practice sessions")
        
        if analytics.average_score < 75:
            steps.append("Target average score of 75+")
        
        if analytics.improvement_percentage < 5:
            steps.append("Focus on areas needing improvement")
        
        steps.append("Schedule mock interview with a peer")
        steps.append("Review and revise weak topics")
        
        return steps
    
    def _save_session(self, session: InterviewSession) -> None:
        """Save session to disk"""
        session_file = self.data_dir / f"session_{session.session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(session.model_dump(), f, indent=2)
    
    def _load_session(self, session_id: str) -> InterviewSession:
        """Load session from disk"""
        session_file = self.data_dir / f"session_{session_id}.json"
        
        if not session_file.exists():
            raise ValueError(f"Session {session_id} not found")
        
        with open(session_file, 'r') as f:
            data = json.load(f)
        
        return InterviewSession(**data)
    
    def _save_user_progress(self, progress: UserProgress) -> None:
        """Save user progress to disk"""
        progress_file = self.data_dir / f"progress_{progress.user_id}.json"
        with open(progress_file, 'w') as f:
            json.dump(progress.model_dump(), f, indent=2)
    
    def get_milestones(self, user_id: str) -> List[Milestone]:
        """Get user's milestones"""
        progress = self.get_user_progress(user_id)
        
        milestones = [
            Milestone(
                milestone_id="first_session",
                title="First Steps",
                description="Complete your first interview session",
                category="sessions",
                threshold=1,
                current_value=progress.completed_sessions,
                achieved=progress.completed_sessions >= 1,
                reward_points=10
            ),
            Milestone(
                milestone_id="ten_sessions",
                title="Dedicated Learner",
                description="Complete 10 interview sessions",
                category="sessions",
                threshold=10,
                current_value=progress.completed_sessions,
                achieved=progress.completed_sessions >= 10,
                reward_points=50
            ),
            Milestone(
                milestone_id="score_80",
                title="Excellence",
                description="Achieve average score of 80+",
                category="score",
                threshold=80,
                current_value=progress.average_score,
                achieved=progress.average_score >= 80,
                reward_points=100
            ),
            Milestone(
                milestone_id="hundred_questions",
                title="Century Club",
                description="Answer 100 questions",
                category="questions",
                threshold=100,
                current_value=progress.total_questions_answered,
                achieved=progress.total_questions_answered >= 100,
                reward_points=75
            ),
            Milestone(
                milestone_id="improvement_20",
                title="Rising Star",
                description="Improve by 20% or more",
                category="improvement",
                threshold=20,
                current_value=progress.improvement_rate,
                achieved=progress.improvement_rate >= 20,
                reward_points=150
            )
        ]
        
        # Set achieved_at for achieved milestones
        for milestone in milestones:
            if milestone.achieved and not milestone.achieved_at:
                milestone.achieved_at = datetime.now().isoformat()
        
        return milestones
