"""
Example usage of Question Generator
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.question_generator.generator import QuestionGenerator
from src.question_generator.schemas import (
    QuestionGenerationRequest,
    QuestionType,
    DifficultyLevel
)
from src.resume_parser.parser import ResumeParser


def example_basic_generation():
    """Example 1: Basic Question Generation"""
    print("=" * 70)
    print("Example 1: Basic Question Generation")
    print("=" * 70)
    
    # Initialize generator
    generator = QuestionGenerator()
    
    # Create a request
    request = QuestionGenerationRequest(
        target_role="Software Engineer",
        target_level="mid",
        num_technical=3,
        num_behavioral=2,
        focus_areas=["Python", "algorithms", "system design"]
    )
    
    # Generate questions
    questions = generator.generate_questions(request)
    
    print(f"\n📊 Generated {len(questions.questions)} questions")
    print(f"   Session ID: {questions.session_id}")
    print(f"   Target Role: {questions.target_role}")
    print(f"   Level: {questions.target_level}")
    print(f"   Technical: {questions.technical_count}")
    print(f"   Behavioral: {questions.behavioral_count}")
    print(f"   Total Duration: {questions.get_total_duration()} minutes")
    
    # Display questions
    print("\n📝 Questions:")
    for i, q in enumerate(questions.questions, 1):
        print(f"\n{i}. [{q.type.value.upper()}] [{q.difficulty.value.upper()}]")
        print(f"   {q.question}")
        print(f"   Category: {q.category}")
        print(f"   Skills: {', '.join(q.skills_tested)}")
        print(f"   Duration: {q.expected_duration_minutes} min")
        if q.follow_up_questions:
            print(f"   Follow-ups: {len(q.follow_up_questions)}")


def example_resume_tailored():
    """Example 2: Resume-Tailored Questions"""
    print("\n\n" + "=" * 70)
    print("Example 2: Resume-Tailored Questions")
    print("=" * 70)
    
    # Simulate parsed resume data
    resume_data = {
        "skills": {
            "technical": ["Python", "Django", "React", "PostgreSQL", "AWS"],
            "tools": ["Git", "Docker", "Jenkins"],
            "frameworks": ["Django", "FastAPI", "React"]
        },
        "experience": [
            {
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "technologies": ["Python", "React", "AWS"],
                "years": 3
            },
            {
                "title": "Software Engineer",
                "company": "StartupXYZ",
                "technologies": ["Django", "PostgreSQL"],
                "years": 2
            }
        ]
    }
    
    generator = QuestionGenerator()
    
    tailored_request = QuestionGenerationRequest(
        target_role="Senior Full Stack Engineer",
        target_level="senior",
        num_technical=4,
        num_behavioral=2,
        num_system_design=1,
        resume_context=resume_data,
        tailor_to_experience=True,
        include_resume_specific=True,
        focus_areas=["Python", "React", "AWS", "system architecture"]
    )
    
    tailored_questions = generator.generate_questions(tailored_request)
    
    print(f"\n📄 Generated {len(tailored_questions.questions)} tailored questions")
    print("   Based on candidate's experience with Python, Django, React, AWS")
    
    print("\n📝 Sample Questions:")
    for i, q in enumerate(tailored_questions.questions[:3], 1):
        print(f"\n{i}. {q.question}")
        print(f"   Type: {q.type.value} | Difficulty: {q.difficulty.value}")


def example_filtering():
    """Example 3: Filtering and Organizing Questions"""
    print("\n\n" + "=" * 70)
    print("Example 3: Filtering Questions")
    print("=" * 70)
    
    generator = QuestionGenerator()
    
    request = QuestionGenerationRequest(
        target_role="Full Stack Developer",
        target_level="mid",
        num_technical=5,
        num_behavioral=3,
        num_situational=2
    )
    
    questions = generator.generate_questions(request)
    
    # Filter by type
    print("\n🔍 Filtering by Question Type:")
    
    technical = questions.get_questions_by_type(QuestionType.TECHNICAL)
    print(f"\n   Technical Questions ({len(technical)}):")
    for q in technical[:2]:
        print(f"   - {q.question[:70]}...")
    
    behavioral = questions.get_questions_by_type(QuestionType.BEHAVIORAL)
    print(f"\n   Behavioral Questions ({len(behavioral)}):")
    for q in behavioral[:2]:
        print(f"   - {q.question[:70]}...")
    
    situational = questions.get_questions_by_type(QuestionType.SITUATIONAL)
    print(f"\n   Situational Questions ({len(situational)}):")
    for q in situational[:2]:
        print(f"   - {q.question[:70]}...")
    
    # Filter by difficulty
    print("\n\n🔍 Filtering by Difficulty:")
    
    easy = questions.get_questions_by_difficulty(DifficultyLevel.EASY)
    medium = questions.get_questions_by_difficulty(DifficultyLevel.MEDIUM)
    hard = questions.get_questions_by_difficulty(DifficultyLevel.HARD)
    
    print(f"   Easy: {len(easy)} | Medium: {len(medium)} | Hard: {len(hard)}")


def example_follow_ups():
    """Example 4: Generate Follow-up Questions"""
    print("\n\n" + "=" * 70)
    print("Example 4: Generate Follow-up Questions")
    print("=" * 70)
    
    generator = QuestionGenerator()
    
    request = QuestionGenerationRequest(
        target_role="Software Engineer",
        target_level="mid",
        num_technical=1,
        include_follow_ups=True
    )
    
    questions = generator.generate_questions(request)
    
    if questions.questions:
        original_q = questions.questions[0]
        
        print(f"\n📝 Original Question:")
        print(f"   {original_q.question}")
        
        # Simulate a candidate answer
        sample_answer = """
        I would first analyze the requirements carefully and break down the problem 
        into smaller, manageable components. Then I'd design the system architecture, 
        considering scalability and maintainability. I'd implement each component 
        with proper testing and code reviews.
        """
        
        print(f"\n💬 Candidate's Answer:")
        print(f"   {sample_answer.strip()[:150]}...")
        
        # Generate follow-up
        print(f"\n🔄 Generating dynamic follow-up question...")
        follow_up = generator.generate_follow_up(original_q, sample_answer)
        
        print(f"\n❓ Follow-up Question:")
        print(f"   {follow_up}")
        
        if original_q.follow_up_questions:
            print(f"\n📋 Pre-defined Follow-ups:")
            for fu in original_q.follow_up_questions[:3]:
                print(f"   - {fu}")


def example_different_levels():
    """Example 5: Questions for Different Experience Levels"""
    print("\n\n" + "=" * 70)
    print("Example 5: Questions for Different Levels")
    print("=" * 70)
    
    generator = QuestionGenerator()
    
    levels = ["junior", "mid", "senior"]
    
    for level in levels:
        request = QuestionGenerationRequest(
            target_role="Software Engineer",
            target_level=level,
            num_technical=2,
            num_behavioral=1
        )
        
        questions = generator.generate_questions(request)
        
        print(f"\n🎯 {level.upper()} Level Questions:")
        print(f"   Role: {questions.target_role}")
        print(f"   Count: {len(questions.questions)}")
        
        if questions.questions:
            sample_q = questions.questions[0]
            print(f"\n   Sample: {sample_q.question[:100]}...")
            print(f"   Difficulty: {sample_q.difficulty.value}")


def example_system_design():
    """Example 6: System Design Questions"""
    print("\n\n" + "=" * 70)
    print("Example 6: System Design Questions")
    print("=" * 70)
    
    generator = QuestionGenerator()
    
    request = QuestionGenerationRequest(
        target_role="Senior Software Engineer",
        target_level="senior",
        num_system_design=3
    )
    
    questions = generator.generate_questions(request)
    
    print(f"\n🏗️  System Design Questions:")
    
    for i, q in enumerate(questions.questions, 1):
        print(f"\n{i}. {q.question}")
        print(f"   Duration: {q.expected_duration_minutes} minutes")
        print(f"   Skills: {', '.join(q.skills_tested)}")
        
        if q.follow_up_questions:
            print(f"   Follow-ups:")
            for fu in q.follow_up_questions[:2]:
                print(f"      - {fu}")
        
        if q.hints:
            print(f"   Hints:")
            for hint in q.hints[:2]:
                print(f"      - {hint}")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("PrepWise AI - Question Generator Examples")
    print("=" * 70)
    
    try:
        example_basic_generation()
        example_resume_tailored()
        example_filtering()
        example_follow_ups()
        example_different_levels()
        example_system_design()
        
        print("\n\n" + "=" * 70)
        print("✅ All examples completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
