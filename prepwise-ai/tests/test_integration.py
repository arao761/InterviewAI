"""
Integration Tests for PrepWise AI
Tests complete workflows across all phases
"""
import pytest
from src.api.prepwise_api import PrepWiseAPI
from src.session_manager.schemas import InterviewMode


def test_api_initialization():
    """Test API can be initialized"""
    api = PrepWiseAPI()
    assert api is not None
    assert api.resume_parser is not None
    assert api.question_generator is not None
    assert api.answer_evaluator is not None
    assert api.session_manager is not None


def test_complete_workflow():
    """Test complete interview workflow"""
    api = PrepWiseAPI()
    
    # Sample resume text
    resume_text = """
    John Developer
    Email: john@example.com
    
    EXPERIENCE
    Software Engineer at Google (2020-Present)
    - Developed microservices in Python
    - Led team of 3 engineers
    
    EDUCATION
    B.S. Computer Science, MIT, 2020
    
    SKILLS
    Python, Java, AWS, Docker, Kubernetes
    """
    
    # Step 1: Parse resume
    resume = api.parse_resume_from_text(resume_text)
    assert resume.contact.name is not None
    assert resume.contact.email == "john@example.com"
    
    # Step 2: Create session
    session = api.create_interview_session(
        candidate_name=resume.contact.name,
        target_role="Software Engineer",
        user_id="test_user",
        experience_level="mid",
        mode=InterviewMode.PRACTICE,
        num_technical=2,
        num_behavioral=1,
        resume_data=resume
    )
    
    assert session is not None
    assert session.total_questions == 3
    assert session.status.value == "scheduled"
    
    # Step 3: Start session
    started_session = api.start_session(session.session_id)
    assert started_session.status.value == "in_progress"
    
    # Step 4: Get current question
    current_q = api.get_current_question(session.session_id)
    assert current_q is not None
    assert "question" in current_q
    assert "type" in current_q
    
    # Step 5: Submit answers
    answer1 = "A microservice architecture divides applications into small, independent services."
    result1 = api.submit_answer(session.session_id, answer1, 180)
    assert "score" in result1
    assert result1["score"] >= 0
    
    answer2 = "I use Git for version control with feature branching."
    result2 = api.submit_answer(session.session_id, answer2, 120)
    assert "score" in result2
    
    answer3 = "In my previous role, I led a team through a challenging project..."
    result3 = api.submit_answer(session.session_id, answer3, 200)
    assert "score" in result3
    
    # Step 6: Complete session
    completed = api.complete_session(session.session_id)
    assert completed.status.value == "completed"
    assert completed.average_score is not None
    
    # Step 7: Get report
    report = api.get_session_report(session.session_id)
    assert report["session_id"] == session.session_id
    assert report["overall_score"] is not None
    assert len(report["questions"]) == 3
    
    # Step 8: Check progress
    progress = api.get_user_progress("test_user")
    assert progress.total_sessions >= 1
    assert progress.completed_sessions >= 1


def test_question_generation_standalone():
    """Test standalone question generation"""
    api = PrepWiseAPI()
    
    questions = api.generate_questions(
        target_role="Data Scientist",
        experience_level="senior",
        num_technical=3,
        num_behavioral=2,
        focus_areas=["machine learning", "statistics"]
    )
    
    assert len(questions.questions) == 5
    assert questions.technical_count == 3
    assert questions.behavioral_count == 2


def test_answer_evaluation_standalone():
    """Test standalone answer evaluation"""
    api = PrepWiseAPI()
    
    evaluation = api.evaluate_answer(
        question="What is machine learning?",
        answer="Machine learning is a subset of AI where systems learn from data without explicit programming.",
        question_type="technical"
    )
    
    assert evaluation.overall_score >= 0
    assert evaluation.overall_score <= 100
    assert evaluation.score_level is not None


def test_progress_tracking():
    """Test progress tracking functionality"""
    api = PrepWiseAPI()
    
    # Create and complete a session
    session = api.create_interview_session(
        candidate_name="Test User",
        target_role="Engineer",
        user_id="progress_test_user",
        num_technical=1
    )
    
    api.start_session(session.session_id)
    api.submit_answer(session.session_id, "Good answer here", 100)
    api.complete_session(session.session_id)
    
    # Check progress
    progress = api.get_user_progress("progress_test_user")
    assert progress.completed_sessions >= 1
    
    # Check analytics
    analytics = api.get_progress_analytics("progress_test_user")
    assert analytics.sessions_completed >= 1
    
    # Check learning path
    learning_path = api.get_learning_path("progress_test_user")
    assert learning_path is not None
    assert learning_path.current_level in ["beginner", "intermediate", "advanced"]


def test_session_skip_question():
    """Test skipping questions"""
    api = PrepWiseAPI()
    
    session = api.create_interview_session(
        candidate_name="Skip Test",
        target_role="Developer",
        user_id="skip_user",
        num_technical=2
    )
    
    api.start_session(session.session_id)
    
    # Skip first question
    result = api.skip_question(session.session_id)
    assert result["skipped"] is True
    
    # Answer second question
    api.submit_answer(session.session_id, "Answer to second question", 100)
    
    # Complete
    completed = api.complete_session(session.session_id)
    assert completed.questions_skipped == 1
    assert completed.questions_answered == 1


def test_session_comparison():
    """Test comparing two sessions"""
    api = PrepWiseAPI()
    
    # Create first session
    session1 = api.create_interview_session(
        candidate_name="Compare User",
        target_role="Engineer",
        user_id="compare_user",
        num_technical=1
    )
    
    api.start_session(session1.session_id)
    api.submit_answer(session1.session_id, "Short answer", 60)
    api.complete_session(session1.session_id)
    
    # Create second session
    session2 = api.create_interview_session(
        candidate_name="Compare User",
        target_role="Engineer",
        user_id="compare_user",
        num_technical=1
    )
    
    api.start_session(session2.session_id)
    api.submit_answer(session2.session_id, "Much better detailed answer with examples and explanations", 120)
    api.complete_session(session2.session_id)
    
    # Compare
    comparison = api.compare_sessions(session1.session_id, session2.session_id)
    assert "average_score_change" in comparison
    assert "better_session" in comparison


def test_achievements():
    """Test achievement system"""
    api = PrepWiseAPI()
    
    # Create and complete session
    session = api.create_interview_session(
        candidate_name="Achievement User",
        target_role="Engineer",
        user_id="achievement_user",
        num_technical=1
    )
    
    api.start_session(session.session_id)
    api.submit_answer(session.session_id, "Answer", 100)
    api.complete_session(session.session_id)
    
    # Check achievements
    achievements = api.get_achievements("achievement_user")
    assert len(achievements) > 0
    
    # First session milestone should be achieved
    first_session = next((a for a in achievements if a["id"] == "first_session"), None)
    assert first_session is not None
    assert first_session["achieved"] is True


def test_get_statistics():
    """Test system statistics"""
    api = PrepWiseAPI()
    
    stats = api.get_statistics()
    assert stats["status"] == "operational"
    assert stats["phases_implemented"] == 8
    assert len(stats["features"]) > 0


def test_resume_with_session_integration():
    """Test resume parsing integrated with session creation"""
    api = PrepWiseAPI()
    
    resume_text = """
    Jane Engineer
    jane@example.com
    
    Senior Software Engineer at Amazon
    Python, Java, AWS
    B.S. Computer Science
    """
    
    # Parse resume
    resume = api.parse_resume_from_text(resume_text)
    
    # Determine experience level
    experience_level = resume.experience_level or "senior"  # Default to senior if not set
    
    # Create tailored session
    session = api.create_interview_session(
        candidate_name=resume.contact.name,
        target_role="Senior Software Engineer",
        user_id="jane_user",
        experience_level=experience_level,
        num_technical=2,
        num_behavioral=0,  # Set to 0 to get exactly 2 questions
        resume_data=resume  # Pass resume for tailored questions
    )
    
    assert session.target_role == "Senior Software Engineer"
    assert session.experience_level == experience_level
    assert session.total_questions == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
