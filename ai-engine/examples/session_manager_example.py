"""
PrepWise AI - Session Manager Examples
======================================

This example demonstrates how to use the Session Manager (Phase 5)
to create and manage interview sessions.
"""

from src.session_manager.manager import SessionManager
from src.session_manager.schemas import (
    SessionCreateRequest,
    InterviewMode,
    SessionType
)


def example_1_create_and_run_session():
    """Example 1: Create and run a complete interview session"""
    print("\n" + "=" * 70)
    print("Example 1: Complete Interview Session")
    print("=" * 70)
    
    manager = SessionManager()
    
    # Create session
    request = SessionCreateRequest(
        candidate_name="Alice Johnson",
        candidate_email="alice@example.com",
        user_id="user_alice",
        target_role="Senior Software Engineer",
        experience_level="senior",
        mode=InterviewMode.PRACTICE,
        session_type=SessionType.MIXED,
        num_technical=3,
        num_behavioral=2,
        focus_areas=["Python", "System Design", "Leadership"]
    )
    
    print("\n📋 Creating interview session...")
    session = manager.create_session(request)
    
    print(f"✅ Session created: {session.session_id}")
    print(f"   Candidate: {session.candidate_name}")
    print(f"   Role: {session.target_role}")
    print(f"   Questions: {session.total_questions}")
    print(f"   Status: {session.status.value}")
    
    # Start session
    print("\n🚀 Starting session...")
    manager.start_session(session.session_id)
    print("✅ Session started")
    
    # Answer questions
    print("\n💬 Answering questions...")
    
    sample_answers = [
        "Python is excellent for backend development. I've used Django and FastAPI for RESTful APIs...",
        "In my leadership role, I mentored 3 junior developers and led code reviews...",
        "For a scalable system, I would use microservices architecture with message queues..."
    ]
    
    for i, answer in enumerate(sample_answers[:3]):
        response = manager.submit_answer(
            session.session_id,
            i,
            answer,
            time_spent_seconds=180 + i * 30
        )
        print(f"   Question {i+1}: Score {response.evaluation_score:.1f}/100")
    
    # Complete session
    print("\n✅ Completing session...")
    completed_session = manager.complete_session(session.session_id)
    
    print(f"\n📊 Session Results:")
    print(f"   Average Score: {completed_session.average_score:.1f}/100")
    print(f"   Total Duration: {completed_session.total_duration_seconds // 60} minutes")
    print(f"   Questions Answered: {completed_session.questions_answered}/{completed_session.total_questions}")
    print(f"   Status: {completed_session.status.value}")


def example_2_session_progress_tracking():
    """Example 2: Track progress during a session"""
    print("\n" + "=" * 70)
    print("Example 2: Session Progress Tracking")
    print("=" * 70)
    
    manager = SessionManager()
    
    request = SessionCreateRequest(
        candidate_name="Bob Smith",
        target_role="Data Scientist",
        num_technical=5
    )
    
    session = manager.create_session(request)
    manager.start_session(session.session_id)
    
    print(f"\n📈 Progress Tracking:")
    print(f"   Initial progress: {session.get_progress_percentage():.1f}%")
    
    # Answer questions and track progress
    for i in range(3):
        manager.submit_answer(
            session.session_id,
            i,
            f"Answer to question {i+1} with detailed explanation",
            150
        )
        
        updated = manager.get_session(session.session_id)
        progress = updated.get_progress_percentage()
        print(f"   After question {i+1}: {progress:.1f}% complete")
    
    # Skip a question
    manager.skip_question(session.session_id, 3)
    updated = manager.get_session(session.session_id)
    print(f"   After skipping: {updated.get_progress_percentage():.1f}% complete")
    print(f"   Questions skipped: {updated.questions_skipped}")


def example_3_multiple_sessions():
    """Example 3: Manage multiple sessions for a user"""
    print("\n" + "=" * 70)
    print("Example 3: Multiple Sessions for One User")
    print("=" * 70)
    
    manager = SessionManager()
    user_id = "user_multi_session"
    
    # Create multiple sessions
    print("\n📚 Creating multiple sessions...")
    
    for i in range(3):
        request = SessionCreateRequest(
            candidate_name="Charlie Brown",
            user_id=user_id,
            target_role="Full Stack Developer",
            mode=InterviewMode.PRACTICE if i < 2 else InterviewMode.MOCK,
            num_technical=2
        )
        
        session = manager.create_session(request)
        manager.start_session(session.session_id)
        
        # Answer questions
        for j in range(2):
            manager.submit_answer(
                session.session_id,
                j,
                f"Answer for session {i+1}, question {j+1}",
                120
            )
        
        manager.complete_session(session.session_id)
        print(f"   ✅ Completed session {i+1}: {session.session_id}")
    
    # Retrieve user sessions
    print(f"\n📂 Retrieving all sessions for user...")
    sessions = manager.get_user_sessions(user_id)
    
    print(f"   Total sessions: {len(sessions)}")
    for i, s in enumerate(sessions, 1):
        print(f"   {i}. {s.session_id} - {s.mode.value} - Score: {s.average_score:.1f}/100")


def example_4_session_with_skip():
    """Example 4: Session with skipped questions"""
    print("\n" + "=" * 70)
    print("Example 4: Handling Skipped Questions")
    print("=" * 70)
    
    manager = SessionManager()
    
    request = SessionCreateRequest(
        candidate_name="Diana Prince",
        target_role="DevOps Engineer",
        num_technical=4
    )
    
    session = manager.create_session(request)
    manager.start_session(session.session_id)
    
    print("\n💬 Processing questions...")
    
    # Answer first question
    manager.submit_answer(session.session_id, 0, "Good answer", 180)
    print("   ✅ Question 1: Answered")
    
    # Skip second question
    manager.skip_question(session.session_id, 1)
    print("   ⏭️  Question 2: Skipped")
    
    # Answer third question
    manager.submit_answer(session.session_id, 2, "Another good answer", 200)
    print("   ✅ Question 3: Answered")
    
    # Skip fourth question
    manager.skip_question(session.session_id, 3)
    print("   ⏭️  Question 4: Skipped")
    
    # Complete session
    completed = manager.complete_session(session.session_id)
    
    print(f"\n📊 Session Summary:")
    print(f"   Answered: {completed.questions_answered}")
    print(f"   Skipped: {completed.questions_skipped}")
    print(f"   Completion: {completed.questions_answered}/{completed.total_questions}")
    if completed.average_score:
        print(f"   Average Score: {completed.average_score:.1f}/100")


def example_5_session_comparison():
    """Example 5: Compare two sessions"""
    print("\n" + "=" * 70)
    print("Example 5: Session Comparison")
    print("=" * 70)
    
    manager = SessionManager()
    user_id = "user_compare"
    
    # Create first session
    print("\n📝 Creating first session (baseline)...")
    request = SessionCreateRequest(
        candidate_name="Eve Smith",
        user_id=user_id,
        target_role="Software Engineer",
        num_technical=2
    )
    
    session1 = manager.create_session(request)
    manager.start_session(session1.session_id)
    manager.submit_answer(session1.session_id, 0, "Basic answer", 100)
    manager.submit_answer(session1.session_id, 1, "Another basic answer", 110)
    manager.complete_session(session1.session_id)
    
    score1 = manager.get_session(session1.session_id).average_score
    print(f"   Session 1 score: {score1:.1f}/100")
    
    # Create second session (improved)
    print("\n📝 Creating second session (improved)...")
    session2 = manager.create_session(request)
    manager.start_session(session2.session_id)
    manager.submit_answer(
        session2.session_id,
        0,
        "Much better detailed answer with examples and clear explanation",
        150
    )
    manager.submit_answer(
        session2.session_id,
        1,
        "Another improved answer with technical depth and good structure",
        160
    )
    manager.complete_session(session2.session_id)
    
    score2 = manager.get_session(session2.session_id).average_score
    print(f"   Session 2 score: {score2:.1f}/100")
    
    # Compare sessions
    print("\n📊 Comparing sessions...")
    comparison = manager.compare_sessions(session1.session_id, session2.session_id)
    
    print(f"   Score improvement: {comparison.score_improvement:+.1f} points")
    print(f"   Better session: {comparison.better_session}")
    print(f"   Consistency: {comparison.consistency_score:.1f}/100")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("PrepWise AI - Session Manager Examples")
    print("=" * 70)
    
    try:
        example_1_create_and_run_session()
        example_2_session_progress_tracking()
        example_3_multiple_sessions()
        example_4_session_with_skip()
        example_5_session_comparison()
        
        print("\n" + "=" * 70)
        print("✅ All examples completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
