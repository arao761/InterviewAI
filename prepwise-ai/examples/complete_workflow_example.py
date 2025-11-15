"""
PrepWise AI - Complete Workflow Example
========================================

This example demonstrates the COMPLETE end-to-end workflow:
1. Parse Resume (Phase 2)
2. Generate Questions (Phase 3)
3. Conduct Interview Session (Phase 5)
4. Evaluate Answers (Phase 4)
5. Track Progress (Phase 6)
6. Generate Reports

This showcases Phases 1-8 integration.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.session_manager.schemas import InterviewMode
from src.api.prepwise_api import PrepWiseAPI


def complete_interview_workflow():
    """Demonstrate complete interview workflow from start to finish"""
    
    print("=" * 80)
    print("PrepWise AI - Complete Interview Workflow")
    print("=" * 80)
    
    # Initialize API
    api = PrepWiseAPI()
    
    # Sample resume text
    sample_resume = """
    JANE SMITH
    Email: jane.smith@example.com | Phone: (555) 123-4567
    LinkedIn: linkedin.com/in/janesmith | GitHub: github.com/janesmith
    
    PROFESSIONAL SUMMARY
    Senior Software Engineer with 7+ years of experience in full-stack development,
    specializing in cloud-native applications and microservices architecture.
    
    WORK EXPERIENCE
    
    Senior Software Engineer | Tech Corp | San Francisco, CA | Jan 2020 - Present
    - Led migration of monolithic application to microservices architecture, improving scalability by 300%
    - Implemented CI/CD pipeline reducing deployment time from 4 hours to 15 minutes
    - Mentored team of 5 junior engineers on best practices and code reviews
    - Technologies: Python, Django, React, Kubernetes, AWS, PostgreSQL
    
    Software Engineer | StartupXYZ | Austin, TX | Mar 2017 - Dec 2019
    - Developed RESTful APIs serving 1M+ requests per day
    - Optimized database queries reducing response time by 60%
    - Built real-time notification system using WebSockets
    - Technologies: Node.js, Express, MongoDB, Redis, Docker
    
    EDUCATION
    B.S. Computer Science | University of Texas | 2017
    GPA: 3.8/4.0
    
    SKILLS
    Languages: Python, JavaScript, TypeScript, Java, Go
    Frameworks: Django, React, Node.js, Express, FastAPI
    Cloud: AWS, GCP, Azure, Kubernetes, Docker
    Databases: PostgreSQL, MongoDB, Redis, DynamoDB
    Tools: Git, Jenkins, GitHub Actions, Terraform
    """
    
    print("\n" + "="*80)
    print("STEP 1: Parse Resume")
    print("="*80)
    
    parsed_resume = api.parse_resume_from_text(sample_resume)
    
    print(f"\n✅ Resume Parsed Successfully!")
    print(f"   Candidate: {parsed_resume.contact.name}")
    print(f"   Email: {parsed_resume.contact.email}")
    print(f"   Experience Level: {parsed_resume.experience_level}")
    print(f"   Total Experience: {parsed_resume.total_years_experience} years")
    print(f"   Companies: {len(parsed_resume.experience)}")
    print(f"   Skills: {len(parsed_resume.skills.technical)} technical skills")
    
    # Determine experience level if not set
    experience_level = parsed_resume.experience_level
    if not experience_level:
        # Infer from years of experience
        years = parsed_resume.total_years_experience or 0
        if years < 2:
            experience_level = "junior"
        elif years < 5:
            experience_level = "mid"
        else:
            experience_level = "senior"
        print(f"   Inferred Experience Level: {experience_level}")
    
    print("\n" + "="*80)
    print("STEP 2: Create Interview Session")
    print("="*80)
    
    # Create session with resume context
    session = api.create_interview_session(
        candidate_name=parsed_resume.contact.name,
        user_id="user_jane_smith",
        target_role="Senior Software Engineer",
        target_company="FAANG",
        experience_level=experience_level,
        mode=InterviewMode.MOCK,
        num_technical=3,
        num_behavioral=2,
        focus_areas=["microservices", "system design", "leadership"],
        resume_data=parsed_resume
    )
    
    print(f"\n✅ Session Created: {session.session_id}")
    print(f"   Total Questions: {session.total_questions}")
    print(f"   Mode: {session.mode.value}")
    print(f"   Target: {session.target_role}")
    
    # Start the session
    session = api.start_session(session.session_id)
    print(f"\n✅ Session Started at {session.started_at}")
    
    print("\n" + "="*80)
    print("STEP 3: Display Interview Questions")
    print("="*80)
    
    for i, response in enumerate(session.responses, 1):
        print(f"\nQuestion {i} [{response.question_type}]:")
        print(f"  {response.question_text}")
    
    print("\n" + "="*80)
    print("STEP 4: Simulate Candidate Answers & Evaluation")
    print("="*80)
    
    # Simulate answers for each question
    sample_answers = [
        # Technical Q1
        """In our migration to microservices at Tech Corp, we used a strangler fig pattern. 
        We started by identifying bounded contexts and breaking down the monolith gradually. 
        Each service had its own database following the database-per-service pattern. We used 
        Kubernetes for orchestration and implemented API gateway for routing. The key challenges 
        were maintaining data consistency across services - we used event sourcing and CQRS for 
        that. We also implemented circuit breakers and retry logic for resilience. The result 
        was 300% improvement in scalability and much better deployment velocity.""",
        
        # Technical Q2
        """For API optimization, I start with profiling to identify bottlenecks. At StartupXYZ, 
        we had slow database queries. I added proper indexing on frequently queried columns, 
        implemented Redis caching for hot data with a TTL strategy, and used connection pooling. 
        We also implemented pagination for large datasets and added database query optimization 
        like SELECT only needed columns. Result was 60% reduction in response time.""",
        
        # Technical Q3
        """System design for a URL shortener: I'd use a hash function to generate short codes, 
        store mappings in a distributed database like DynamoDB for scalability. For high 
        availability, deploy across multiple regions. Use a load balancer and implement caching 
        with Redis for popular URLs. Add analytics tracking with a separate service. Consider 
        rate limiting to prevent abuse. For scale, use consistent hashing for data distribution.""",
        
        # Behavioral Q1
        """When I was leading the team at Tech Corp, we had a junior engineer who was struggling 
        with code quality. I scheduled one-on-one meetings to understand their challenges. They 
        lacked experience with testing. I paired with them on writing tests, shared resources, 
        and set up a mentorship schedule. Within two months, their code quality improved 
        significantly, and they became one of our strongest contributors. I learned that investing 
        time in people pays off tremendously.""",
        
        # Behavioral Q2
        """During the microservices migration, our VP wanted to do a big-bang rewrite, but I knew 
        that was risky. I prepared data showing the risks of big rewrites - downtime, bugs, and 
        opportunity cost. I proposed the strangler pattern with a detailed plan showing incremental 
        value delivery. I created a prototype demonstrating how we could migrate one service at a 
        time. After presenting the data and prototype, the VP agreed. The incremental approach was 
        successful and we had zero downtime."""
    ]
    
    # Submit each answer
    for i, answer in enumerate(sample_answers):
        print(f"\n📝 Submitting Answer {i+1}...")
        result = api.submit_answer(
            session_id=session.session_id,
            answer=answer,
            time_spent_seconds=300 + (i * 30)  # Simulate varying time
        )
        
        print(f"   ✅ Evaluated: {result['score']:.1f}/100")
    
    print("\n" + "="*80)
    print("STEP 5: Complete Session & Generate Summary")
    print("="*80)
    
    completed_session = api.complete_session(session.session_id)
    
    print(f"\n✅ Session Completed!")
    print(f"\n📊 Final Results:")
    print(f"   Overall Score: {completed_session.average_score:.1f}/100")
    print(f"   Questions Answered: {completed_session.questions_answered}/{completed_session.total_questions}")
    print(f"   Total Duration: {completed_session.total_duration_seconds // 60} minutes")
    
    if completed_session.technical_score:
        print(f"   Technical Score: {completed_session.technical_score:.1f}/100")
    if completed_session.behavioral_score:
        print(f"   Behavioral Score: {completed_session.behavioral_score:.1f}/100")
    
    if completed_session.strengths:
        print(f"\n💪 Key Strengths:")
        for strength in completed_session.strengths[:3]:
            print(f"   • {strength}")
    
    if completed_session.weaknesses:
        print(f"\n📚 Areas for Improvement:")
        for weakness in completed_session.weaknesses[:3]:
            print(f"   • {weakness}")
    
    if completed_session.recommendations:
        print(f"\n💡 Recommendations:")
        for rec in completed_session.recommendations[:3]:
            print(f"   • {rec}")
    
    print("\n" + "="*80)
    print("STEP 6: Track User Progress")
    print("="*80)
    
    progress = api.get_user_progress("user_jane_smith")
    
    print(f"\n📈 User Progress:")
    print(f"   Total Sessions: {progress.total_sessions}")
    print(f"   Completed: {progress.completed_sessions}")
    print(f"   Questions Answered: {progress.total_questions_answered}")
    print(f"   Average Score: {progress.average_score:.1f}/100")
    print(f"   Improvement Rate: {progress.improvement_rate:+.1f}%")
    
    if progress.top_strengths:
        print(f"\n   Top Strengths: {', '.join(progress.top_strengths[:3])}")
    if progress.top_weaknesses:
        print(f"   Needs Practice: {', '.join(progress.top_weaknesses[:3])}")
    
    print("\n" + "="*80)
    print("STEP 7: Generate Learning Path")
    print("="*80)
    
    learning_path = api.get_learning_path("user_jane_smith")
    
    print(f"\n🎯 Personalized Learning Path:")
    print(f"   Current Level: {learning_path.current_level}")
    print(f"   Target Level: {learning_path.target_level}")
    print(f"   Estimated Time: {learning_path.estimated_completion_weeks} weeks")
    
    if learning_path.recommended_focus:
        print(f"\n   Focus Areas:")
        for focus in learning_path.recommended_focus[:3]:
            print(f"   • {focus}")
    
    if learning_path.milestones:
        print(f"\n   Milestones:")
        for milestone in learning_path.milestones[:3]:
            print(f"   ✓ {milestone}")
    
    print("\n" + "="*80)
    print("STEP 8: View Achievements")
    print("="*80)
    
    achievements = api.get_achievements("user_jane_smith")
    
    achieved = [a for a in achievements if a["achieved"]]
    in_progress = [a for a in achievements if not a["achieved"]]
    
    print(f"\n🏆 Achievements Unlocked: {len(achieved)}")
    for achievement in achieved:
        print(f"   ✅ {achievement['title']}: {achievement['description']}")
    
    print(f"\n🎯 In Progress: {len(in_progress)}")
    for achievement in in_progress[:3]:
        progress_pct = (achievement['progress'] / achievement['threshold']) * 100
        print(f"   ⏳ {achievement['title']}: {progress_pct:.0f}% ({achievement['progress']:.0f}/{achievement['threshold']})")
    
    print("\n" + "="*80)
    print("STEP 9: Detailed Session Report")
    print("="*80)
    
    report = api.get_session_report(session.session_id)
    
    print(f"\n📋 Session Report:")
    print(f"   Session ID: {report['session_id']}")
    print(f"   Candidate: {report['candidate']}")
    print(f"   Overall Score: {report['overall_score']:.1f}/100")
    print(f"   Duration: {report['duration_minutes']} minutes")
    
    print(f"\n   Question Breakdown:")
    for q in report['questions']:
        status = "✅" if q['score'] else "⏭️"
        score_text = f"{q['score']:.1f}/100" if q['score'] else "skipped"
        print(f"   {status} Q{q['number']} [{q['type']}]: {score_text}")
    
    print("\n" + "="*80)
    print("✅ COMPLETE WORKFLOW FINISHED!")
    print("="*80)
    
    print("\n🎉 PrepWise AI Successfully Demonstrated:")
    print("   ✅ Resume parsing and analysis")
    print("   ✅ Intelligent question generation")
    print("   ✅ Session management and tracking")
    print("   ✅ Real-time answer evaluation")
    print("   ✅ Comprehensive progress tracking")
    print("   ✅ Personalized learning paths")
    print("   ✅ Achievement milestones")
    print("   ✅ Detailed performance analytics")
    
    print("\n📦 All 8 Phases Fully Integrated:")
    print("   Phase 1: Core Infrastructure ✅")
    print("   Phase 2: Resume Parser ✅")
    print("   Phase 3: Question Generator ✅")
    print("   Phase 4: Answer Evaluator ✅")
    print("   Phase 5: Session Manager ✅")
    print("   Phase 6: Progress Tracking ✅")
    print("   Phase 7: Scoring Engine ✅")
    print("   Phase 8: Integration Layer ✅")
    
    print("\n🚀 System Status: PRODUCTION READY")
    
    return completed_session, progress, learning_path


if __name__ == "__main__":
    try:
        session, progress, learning_path = complete_interview_workflow()
        print("\n✅ Workflow completed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
