"""
PrepWise AI - Progress Tracking & Analytics Examples
====================================================

This example demonstrates how to use Progress Tracking (Phase 6)
to analyze user performance and generate insights.
"""

from src.session_manager.manager import SessionManager
from src.session_manager.schemas import (
    SessionCreateRequest,
    InterviewMode
)


def example_1_user_progress():
    """Example 1: Track user progress across sessions"""
    print("\n" + "=" * 70)
    print("Example 1: User Progress Tracking")
    print("=" * 70)
    
    manager = SessionManager()
    user_id = "user_progress_demo"
    
    # Create and complete multiple sessions
    print("\n📚 Creating practice sessions...")
    
    for i in range(5):
        request = SessionCreateRequest(
            candidate_name="Progress User",
            user_id=user_id,
            target_role="Software Engineer",
            num_technical=3,
            num_behavioral=1
        )
        
        session = manager.create_session(request)
        manager.start_session(session.session_id)
        
        # Simulate improving answers
        for j in range(3):
            answer_quality = f"Answer for session {i+1}, getting better each time" + " with more detail" * i
            manager.submit_answer(session.session_id, j, answer_quality, 150)
        
        manager.complete_session(session.session_id)
        print(f"   ✅ Completed session {i+1}")
    
    # Get user progress
    print(f"\n📊 User Progress Summary:")
    progress = manager.get_user_progress(user_id)
    
    print(f"   Total Sessions: {progress.total_sessions}")
    print(f"   Completed: {progress.completed_sessions}")
    print(f"   Questions Answered: {progress.total_questions_answered}")
    print(f"   Average Score: {progress.average_score:.1f}/100")
    print(f"   Best Score: {progress.best_score:.1f}/100")
    print(f"   Improvement Rate: {progress.improvement_rate:+.1f}%")
    
    if progress.top_strengths:
        print(f"\n   💪 Top Strengths:")
        for strength in progress.top_strengths[:3]:
            print(f"      • {strength}")
    
    if progress.top_weaknesses:
        print(f"\n   📚 Areas for Improvement:")
        for weakness in progress.top_weaknesses[:3]:
            print(f"      • {weakness}")


def example_2_progress_analytics():
    """Example 2: Detailed progress analytics"""
    print("\n" + "=" * 70)
    print("Example 2: Progress Analytics")
    print("=" * 70)
    
    manager = SessionManager()
    user_id = "user_analytics_demo"
    
    # Create sessions with different types
    print("\n📈 Creating diverse sessions...")
    
    session_configs = [
        {"num_technical": 3, "num_behavioral": 0},
        {"num_technical": 0, "num_behavioral": 3},
        {"num_technical": 2, "num_behavioral": 2},
        {"num_technical": 3, "num_behavioral": 1},
    ]
    
    for i, config in enumerate(session_configs):
        request = SessionCreateRequest(
            candidate_name="Analytics User",
            user_id=user_id,
            target_role="Software Engineer",
            **config
        )
        
        session = manager.create_session(request)
        manager.start_session(session.session_id)
        
        # Answer all questions
        for j in range(session.total_questions):
            manager.submit_answer(
                session.session_id,
                j,
                f"Detailed answer with good structure and examples",
                160 + j * 10
            )
        
        manager.complete_session(session.session_id)
        print(f"   ✅ Session {i+1} completed")
    
    # Get analytics
    print(f"\n📊 Analytics (30 days):")
    analytics = manager.get_progress_analytics(user_id, period="30_days")
    
    print(f"   Sessions Completed: {analytics.sessions_completed}")
    print(f"   Average Score: {analytics.average_score:.1f}/100")
    print(f"   Median Score: {analytics.median_score:.1f}/100")
    print(f"   Improvement: {analytics.improvement_percentage:+.1f}%")
    
    if analytics.sessions_by_type:
        print(f"\n   📋 Sessions by Type:")
        for session_type, count in analytics.sessions_by_type.items():
            print(f"      • {session_type}: {count}")
    
    print(f"\n   ⏱️  Time Analysis:")
    print(f"      Total Practice: {analytics.total_practice_time_hours:.1f} hours")
    print(f"      Avg Session: {analytics.average_session_duration_minutes:.1f} minutes")
    
    if analytics.focus_recommendations:
        print(f"\n   💡 Recommendations:")
        for rec in analytics.focus_recommendations:
            print(f"      • {rec}")


def example_3_learning_path():
    """Example 3: Generate personalized learning path"""
    print("\n" + "=" * 70)
    print("Example 3: Personalized Learning Path")
    print("=" * 70)
    
    manager = SessionManager()
    user_id = "user_learning_path"
    
    # Create some sessions
    print("\n🎓 Building learning profile...")
    
    for i in range(3):
        request = SessionCreateRequest(
            candidate_name="Learning User",
            user_id=user_id,
            target_role="Software Engineer",
            num_technical=2,
            num_behavioral=1
        )
        
        session = manager.create_session(request)
        manager.start_session(session.session_id)
        
        for j in range(3):
            manager.submit_answer(session.session_id, j, "Practice answer", 140)
        
        manager.complete_session(session.session_id)
    
    # Generate learning path
    print(f"\n🗺️  Generating Learning Path...")
    path = manager.generate_learning_path(user_id)
    
    print(f"   Current Level: {path.current_level}")
    print(f"   Target Level: {path.target_level}")
    print(f"   Estimated Time: {path.estimated_completion_weeks} weeks")
    print(f"   Session Frequency: {path.recommended_session_frequency}")
    
    if path.recommended_focus:
        print(f"\n   🎯 Recommended Focus Areas:")
        for focus in path.recommended_focus:
            print(f"      • {focus}")
    
    if path.milestones:
        print(f"\n   🏆 Milestones:")
        for milestone in path.milestones:
            print(f"      • {milestone}")
    
    if path.suggested_resources:
        print(f"\n   📚 Suggested Resources:")
        for resource in path.suggested_resources[:3]:
            print(f"      • {resource}")


def example_4_milestones():
    """Example 4: Achievement milestones"""
    print("\n" + "=" * 70)
    print("Example 4: Achievement Milestones")
    print("=" * 70)
    
    manager = SessionManager()
    user_id = "user_milestones_demo"
    
    # Complete first session
    print("\n🏅 Working towards milestones...")
    
    request = SessionCreateRequest(
        candidate_name="Milestone User",
        user_id=user_id,
        target_role="Software Engineer",
        num_technical=2
    )
    
    session = manager.create_session(request)
    manager.start_session(session.session_id)
    manager.submit_answer(session.session_id, 0, "Good answer", 150)
    manager.submit_answer(session.session_id, 1, "Another good answer", 160)
    manager.complete_session(session.session_id)
    
    # Get milestones
    print(f"\n🎖️  Achievement Milestones:")
    milestones = manager.get_milestones(user_id)
    
    for milestone in milestones:
        status = "✅" if milestone.achieved else "⏳"
        progress = f"({milestone.current_value}/{milestone.threshold})"
        
        print(f"   {status} {milestone.title} {progress}")
        print(f"      {milestone.description}")
        print(f"      Reward: {milestone.reward_points} points")
        
        if milestone.achieved:
            print(f"      Achieved: {milestone.achieved_at}")
        
        print()


def example_5_comparison_and_insights():
    """Example 5: Session comparison and insights"""
    print("\n" + "=" * 70)
    print("Example 5: Session Comparison & Insights")
    print("=" * 70)
    
    manager = SessionManager()
    user_id = "user_comparison"
    
    # Create two sessions at different skill levels
    print("\n📊 Creating sessions to compare...")
    
    # First session - beginner level
    request1 = SessionCreateRequest(
        candidate_name="Comparison User",
        user_id=user_id,
        target_role="Software Engineer",
        num_technical=2
    )
    
    session1 = manager.create_session(request1)
    manager.start_session(session1.session_id)
    manager.submit_answer(session1.session_id, 0, "Short answer", 90)
    manager.submit_answer(session1.session_id, 1, "Brief response", 85)
    completed1 = manager.complete_session(session1.session_id)
    
    print(f"   Session 1: {completed1.average_score:.1f}/100")
    
    # Second session - improved
    request2 = SessionCreateRequest(
        candidate_name="Comparison User",
        user_id=user_id,
        target_role="Software Engineer",
        num_technical=2
    )
    
    session2 = manager.create_session(request2)
    manager.start_session(session2.session_id)
    manager.submit_answer(
        session2.session_id,
        0,
        "Much more detailed answer with examples, clear structure, and technical depth",
        180
    )
    manager.submit_answer(
        session2.session_id,
        1,
        "Comprehensive response covering all aspects with good communication",
        190
    )
    completed2 = manager.complete_session(session2.session_id)
    
    print(f"   Session 2: {completed2.average_score:.1f}/100")
    
    # Compare sessions
    print(f"\n⚖️  Comparison Analysis:")
    comparison = manager.compare_sessions(session1.session_id, session2.session_id)
    
    print(f"   Score Change: {comparison.score_improvement:+.1f} points")
    print(f"   Time Change: {comparison.time_improvement:+d} seconds")
    print(f"   Consistency: {comparison.consistency_score:.1f}/100")
    print(f"   Better Session: Session {'1' if comparison.better_session == session1.session_id else '2'}")
    
    if comparison.improvement_areas:
        print(f"\n   ✨ Improved Areas:")
        for area in comparison.improvement_areas:
            print(f"      • {area}")
    
    if comparison.regression_areas:
        print(f"\n   ⚠️  Regression Areas:")
        for area in comparison.regression_areas:
            print(f"      • {area}")


def example_6_comprehensive_analytics():
    """Example 6: Comprehensive analytics overview"""
    print("\n" + "=" * 70)
    print("Example 6: Comprehensive Analytics Dashboard")
    print("=" * 70)
    
    manager = SessionManager()
    user_id = "user_comprehensive"
    
    # Create multiple sessions with variety
    print("\n📈 Building comprehensive profile...")
    
    modes = [InterviewMode.PRACTICE, InterviewMode.PRACTICE, InterviewMode.MOCK]
    
    for i, mode in enumerate(modes):
        request = SessionCreateRequest(
            candidate_name="Comprehensive User",
            user_id=user_id,
            target_role="Software Engineer",
            mode=mode,
            num_technical=2,
            num_behavioral=1
        )
        
        session = manager.create_session(request)
        manager.start_session(session.session_id)
        
        for j in range(3):
            manager.submit_answer(
                session.session_id,
                j,
                f"Quality answer improving over time with session {i+1}",
                140 + i * 20
            )
        
        manager.complete_session(session.session_id)
    
    # Get all analytics
    progress = manager.get_user_progress(user_id)
    analytics = manager.get_progress_analytics(user_id, period="all_time")
    learning_path = manager.generate_learning_path(user_id)
    milestones = manager.get_milestones(user_id)
    
    print(f"\n📊 Comprehensive Analytics Dashboard")
    print("=" * 70)
    
    # Overview
    print(f"\n📈 Overview:")
    print(f"   Sessions: {progress.total_sessions} ({progress.completed_sessions} completed)")
    print(f"   Questions: {progress.total_questions_answered}")
    print(f"   Practice Time: {progress.total_time_spent_hours:.1f} hours")
    print(f"   Average Score: {progress.average_score:.1f}/100")
    print(f"   Improvement: {progress.improvement_rate:+.1f}%")
    
    # Performance
    print(f"\n🎯 Performance:")
    print(f"   Best: {progress.best_score:.1f}/100")
    print(f"   Worst: {progress.worst_score:.1f}/100")
    if progress.technical_average:
        print(f"   Technical: {progress.technical_average:.1f}/100")
    if progress.behavioral_average:
        print(f"   Behavioral: {progress.behavioral_average:.1f}/100")
    
    # Learning Path
    print(f"\n🗺️  Learning Path:")
    print(f"   Level: {learning_path.current_level} → {learning_path.target_level}")
    print(f"   Timeline: {learning_path.estimated_completion_weeks} weeks")
    print(f"   Next Focus: {', '.join(learning_path.recommended_focus[:3])}")
    
    # Milestones
    achieved = sum(1 for m in milestones if m.achieved)
    total_milestones = len(milestones)
    print(f"\n🏆 Achievements:")
    print(f"   Milestones: {achieved}/{total_milestones} achieved")
    total_points = sum(m.reward_points for m in milestones if m.achieved)
    print(f"   Points: {total_points}")
    
    # Recommendations
    if analytics.focus_recommendations:
        print(f"\n💡 Recommendations:")
        for rec in analytics.focus_recommendations[:3]:
            print(f"   • {rec}")
    
    if analytics.next_steps:
        print(f"\n🎯 Next Steps:")
        for step in analytics.next_steps[:3]:
            print(f"   • {step}")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("PrepWise AI - Progress Tracking & Analytics Examples")
    print("=" * 70)
    
    try:
        example_1_user_progress()
        example_2_progress_analytics()
        example_3_learning_path()
        example_4_milestones()
        example_5_comparison_and_insights()
        example_6_comprehensive_analytics()
        
        print("\n" + "=" * 70)
        print("✅ All examples completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
