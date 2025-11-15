"""
Tests for Session Manager and Progress Tracking
"""
import pytest
from src.session_manager.manager import SessionManager
from src.session_manager.schemas import (
    SessionCreateRequest,
    SessionStatus,
    InterviewMode,
    SessionType
)


def test_session_manager_initialization():
    """Test session manager can be initialized"""
    manager = SessionManager()
    assert manager is not None
    assert manager.data_dir.exists()


def test_create_session():
    """Test creating a new interview session"""
    manager = SessionManager()
    
    request = SessionCreateRequest(
        candidate_name="John Doe",
        candidate_email="john@example.com",
        user_id="user_123",
        target_role="Software Engineer",
        experience_level="mid",
        mode=InterviewMode.PRACTICE,
        num_technical=2,
        num_behavioral=1
    )
    
    session = manager.create_session(request)
    
    assert session is not None
    assert session.session_id.startswith("sess_")
    assert session.candidate_name == "John Doe"
    assert session.total_questions == 3
    assert session.status == SessionStatus.SCHEDULED
    assert len(session.responses) == 3


def test_start_session():
    """Test starting a session"""
    manager = SessionManager()
    
    request = SessionCreateRequest(
        candidate_name="Jane Smith",
        target_role="Data Scientist",
        num_technical=2
    )
    
    session = manager.create_session(request)
    started_session = manager.start_session(session.session_id)
    
    assert started_session.status == SessionStatus.IN_PROGRESS
    assert started_session.started_at is not None


def test_submit_answer():
    """Test submitting an answer"""
    manager = SessionManager()
    
    request = SessionCreateRequest(
        candidate_name="Test User",
        target_role="Software Engineer",
        num_technical=1
    )
    
    session = manager.create_session(request)
    manager.start_session(session.session_id)
    
    answer = "A hash table uses a hash function to map keys to indices..."
    response = manager.submit_answer(
        session_id=session.session_id,
        question_index=0,
        answer_text=answer,
        time_spent_seconds=300
    )
    
    assert response.answer_text == answer
    assert response.time_spent_seconds == 300
    assert response.evaluation_score is not None
    assert response.evaluation_score >= 0
    assert response.evaluation_score <= 100
    assert not response.is_skipped


def test_skip_question():
    """Test skipping a question"""
    manager = SessionManager()
    
    request = SessionCreateRequest(
        candidate_name="Test User",
        target_role="Software Engineer",
        num_technical=2
    )
    
    session = manager.create_session(request)
    manager.start_session(session.session_id)
    
    response = manager.skip_question(
        session_id=session.session_id,
        question_index=0
    )
    
    assert response.is_skipped
    assert response.answered_at is not None
    
    # Check session counters
    updated_session = manager.get_session(session.session_id)
    assert updated_session.questions_skipped == 1
    assert updated_session.current_question_index == 1


def test_complete_session():
    """Test completing a session"""
    manager = SessionManager()
    
    request = SessionCreateRequest(
        candidate_name="Test User",
        user_id="user_test",
        target_role="Software Engineer",
        num_technical=2
    )
    
    session = manager.create_session(request)
    manager.start_session(session.session_id)
    
    # Answer questions
    manager.submit_answer(
        session.session_id,
        0,
        "Answer to question 1",
        300
    )
    manager.submit_answer(
        session.session_id,
        1,
        "Answer to question 2",
        250
    )
    
    # Complete session
    completed = manager.complete_session(session.session_id)
    
    assert completed.status == SessionStatus.COMPLETED
    assert completed.completed_at is not None
    assert completed.average_score is not None
    assert completed.total_duration_seconds > 0


def test_get_user_sessions():
    """Test retrieving user sessions"""
    manager = SessionManager()
    
    user_id = "user_multi"
    
    # Create multiple sessions
    for i in range(3):
        request = SessionCreateRequest(
            candidate_name=f"User {i}",
            user_id=user_id,
            target_role="Software Engineer",
            num_technical=1
        )
        manager.create_session(request)
    
    sessions = manager.get_user_sessions(user_id)
    
    assert len(sessions) == 3
    assert all(s.user_id == user_id for s in sessions)


def test_user_progress():
    """Test user progress calculation"""
    manager = SessionManager()
    
    user_id = "user_progress"
    
    # Create and complete a session
    request = SessionCreateRequest(
        candidate_name="Progress User",
        user_id=user_id,
        target_role="Software Engineer",
        num_technical=2
    )
    
    session = manager.create_session(request)
    manager.start_session(session.session_id)
    
    manager.submit_answer(session.session_id, 0, "Answer 1", 200)
    manager.submit_answer(session.session_id, 1, "Answer 2", 250)
    
    manager.complete_session(session.session_id)
    
    # Get progress
    progress = manager.get_user_progress(user_id)
    
    assert progress.user_id == user_id
    assert progress.total_sessions == 1
    assert progress.completed_sessions == 1
    assert progress.total_questions_answered == 2
    assert progress.average_score > 0


def test_progress_analytics():
    """Test progress analytics generation"""
    manager = SessionManager()
    
    user_id = "user_analytics"
    
    # Create and complete session
    request = SessionCreateRequest(
        candidate_name="Analytics User",
        user_id=user_id,
        target_role="Software Engineer",
        num_technical=2
    )
    
    session = manager.create_session(request)
    manager.start_session(session.session_id)
    manager.submit_answer(session.session_id, 0, "Good answer", 200)
    manager.submit_answer(session.session_id, 1, "Another good answer", 250)
    manager.complete_session(session.session_id)
    
    # Get analytics
    analytics = manager.get_progress_analytics(user_id, period="30_days")
    
    assert analytics.user_id == user_id
    assert analytics.sessions_completed == 1
    assert analytics.average_score > 0
    assert len(analytics.focus_recommendations) > 0


def test_session_comparison():
    """Test comparing two sessions"""
    manager = SessionManager()
    
    user_id = "user_compare"
    
    # Create two sessions
    request = SessionCreateRequest(
        candidate_name="Compare User",
        user_id=user_id,
        target_role="Software Engineer",
        num_technical=1
    )
    
    session1 = manager.create_session(request)
    manager.start_session(session1.session_id)
    manager.submit_answer(session1.session_id, 0, "Short answer", 100)
    manager.complete_session(session1.session_id)
    
    session2 = manager.create_session(request)
    manager.start_session(session2.session_id)
    manager.submit_answer(session2.session_id, 0, "Much better detailed answer with examples", 200)
    manager.complete_session(session2.session_id)
    
    # Compare sessions
    comparison = manager.compare_sessions(session1.session_id, session2.session_id)
    
    assert comparison is not None
    assert len(comparison.session_ids) == 2
    assert len(comparison.scores) == 2
    assert comparison.better_session in [session1.session_id, session2.session_id]


def test_learning_path():
    """Test learning path generation"""
    manager = SessionManager()
    
    user_id = "user_path"
    
    # Create session
    request = SessionCreateRequest(
        candidate_name="Path User",
        user_id=user_id,
        target_role="Software Engineer",
        num_technical=2
    )
    
    session = manager.create_session(request)
    manager.start_session(session.session_id)
    manager.submit_answer(session.session_id, 0, "Answer", 200)
    manager.submit_answer(session.session_id, 1, "Answer", 200)
    manager.complete_session(session.session_id)
    
    # Generate learning path
    path = manager.generate_learning_path(user_id)
    
    assert path.user_id == user_id
    assert path.current_level in ["beginner", "intermediate", "advanced"]
    assert len(path.recommended_focus) > 0
    assert path.estimated_completion_weeks > 0


def test_milestones():
    """Test milestone tracking"""
    manager = SessionManager()
    
    user_id = "user_milestones"
    
    # Create and complete session
    request = SessionCreateRequest(
        candidate_name="Milestone User",
        user_id=user_id,
        target_role="Software Engineer",
        num_technical=1
    )
    
    session = manager.create_session(request)
    manager.start_session(session.session_id)
    manager.submit_answer(session.session_id, 0, "Answer", 200)
    manager.complete_session(session.session_id)
    
    # Get milestones
    milestones = manager.get_milestones(user_id)
    
    assert len(milestones) > 0
    
    # Check if first session milestone is achieved
    first_session_milestone = next((m for m in milestones if m.milestone_id == "first_session"), None)
    assert first_session_milestone is not None
    assert first_session_milestone.achieved


def test_session_persistence():
    """Test that sessions are persisted correctly"""
    manager = SessionManager()
    
    request = SessionCreateRequest(
        candidate_name="Persist User",
        target_role="Software Engineer",
        num_technical=1
    )
    
    session = manager.create_session(request)
    session_id = session.session_id
    
    # Create new manager instance to test loading
    manager2 = SessionManager(data_dir=manager.data_dir)
    loaded_session = manager2.get_session(session_id)
    
    assert loaded_session.session_id == session_id
    assert loaded_session.candidate_name == "Persist User"


def test_session_progress_percentage():
    """Test session progress calculation"""
    manager = SessionManager()
    
    request = SessionCreateRequest(
        candidate_name="Progress User",
        target_role="Software Engineer",
        num_technical=4
    )
    
    session = manager.create_session(request)
    
    assert session.get_progress_percentage() == 0.0
    
    manager.start_session(session.session_id)
    manager.submit_answer(session.session_id, 0, "Answer 1", 100)
    
    updated = manager.get_session(session.session_id)
    assert updated.get_progress_percentage() == 25.0
    
    manager.submit_answer(session.session_id, 1, "Answer 2", 100)
    updated = manager.get_session(session.session_id)
    assert updated.get_progress_percentage() == 50.0


def test_session_metrics_calculation():
    """Test session metrics are calculated correctly"""
    manager = SessionManager()
    
    request = SessionCreateRequest(
        candidate_name="Metrics User",
        target_role="Software Engineer",
        num_technical=2
    )
    
    session = manager.create_session(request)
    manager.start_session(session.session_id)
    
    manager.submit_answer(session.session_id, 0, "Good technical answer", 300)
    manager.submit_answer(session.session_id, 1, "Another technical answer", 250)
    
    updated = manager.get_session(session.session_id)
    updated.calculate_metrics()
    
    assert updated.average_score is not None
    assert updated.total_duration_seconds == 550
    assert updated.technical_score is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
