"""
Full Integration Example: Resume Parser → Question Generator → Answer Evaluator
Demonstrates complete end-to-end workflow from resume to evaluation
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.resume_parser.parser import ResumeParser
from src.question_generator.generator import QuestionGenerator
from src.question_generator.schemas import QuestionGenerationRequest
from src.evaluator.evaluator import AnswerEvaluator
from src.evaluator.schemas import EvaluationRequest, BatchEvaluationRequest


def main():
    """Demonstrate full integration: Resume → Questions → Evaluation"""
    print("=" * 70)
    print("PrepWise AI - Complete Integration Demo")
    print("Resume Parser → Question Generator → Answer Evaluator")
    print("=" * 70)
    
    # Sample resume text
    sample_resume = """
    John Doe
    Email: john.doe@email.com
    Phone: (555) 123-4567
    LinkedIn: linkedin.com/in/johndoe
    
    EXPERIENCE
    Senior Software Engineer | Tech Corp | 2021 - Present
    - Led development of microservices architecture using Python and AWS
    - Managed team of 5 engineers
    - Reduced API latency by 40% through optimization
    - Technologies: Python, Django, React, PostgreSQL, AWS, Docker
    
    Software Engineer | StartupXYZ | 2018 - 2021
    - Built REST APIs using Django and Flask
    - Implemented CI/CD pipelines with Jenkins
    - Technologies: Python, Flask, MongoDB, Redis
    
    EDUCATION
    B.S. Computer Science | Stanford University | 2018
    GPA: 3.8/4.0
    
    SKILLS
    Languages: Python, JavaScript, Java, SQL
    Frameworks: Django, Flask, React, Node.js
    Tools: Git, Docker, Kubernetes, Jenkins
    Cloud: AWS, GCP
    Databases: PostgreSQL, MongoDB, Redis
    """
    
    print("\n📄 Step 1: Parse Resume")
    print("-" * 70)
    
    # Initialize parser
    parser = ResumeParser()
    
    # Parse resume
    try:
        parsed_resume = parser.parse_resume_from_text(sample_resume)
        
        print(f"✅ Resume Parsed Successfully!")
        print(f"\n📊 Candidate Profile:")
        print(f"   Name: {parsed_resume.contact.name}")
        print(f"   Email: {parsed_resume.contact.email}")
        print(f"   Experience Level: {parsed_resume.experience_level or 'Not set'}")
        print(f"   Total Experience: {parsed_resume.total_years_experience or 0} years")
        print(f"   Current Role: {parsed_resume.experience[0].title if parsed_resume.experience else 'N/A'}")
        print(f"   Technical Skills: {len(parsed_resume.skills.technical)} skills")
        print(f"   Top Skills: {', '.join(parsed_resume.skills.technical[:5])}")
        
        # Convert to dict for question generator
        resume_context = {
            "contact": {
                "name": parsed_resume.contact.name,
                "email": parsed_resume.contact.email
            },
            "skills": {
                "technical": parsed_resume.skills.technical,
                "tools": parsed_resume.skills.tools,
                "frameworks": parsed_resume.skills.frameworks
            },
            "experience": [
                {
                    "title": exp.title,
                    "company": exp.company,
                    "technologies": exp.technologies
                }
                for exp in parsed_resume.experience
            ],
            "total_years": parsed_resume.total_years_experience,
            "level": parsed_resume.experience_level
        }
        
    except Exception as e:
        print(f"❌ Error parsing resume: {e}")
        return
    
    print("\n\n📝 Step 2: Generate Tailored Questions")
    print("-" * 70)
    
    # Initialize question generator
    generator = QuestionGenerator()
    
    # Determine experience level for question generation
    experience_level = parsed_resume.experience_level or "mid"
    if parsed_resume.total_years_experience:
        if parsed_resume.total_years_experience < 2:
            experience_level = "junior"
        elif parsed_resume.total_years_experience >= 5:
            experience_level = "senior"
    
    # Extract focus areas from skills
    focus_areas = parsed_resume.skills.technical[:5] if parsed_resume.skills.technical else ["general programming"]
    
    # Create request
    request = QuestionGenerationRequest(
        target_role="Senior Software Engineer",
        target_level=experience_level,
        num_technical=4,
        num_behavioral=2,
        num_system_design=1,
        focus_areas=focus_areas,
        resume_context=resume_context,
        tailor_to_experience=True,
        include_resume_specific=True
    )
    
    print(f"\n🎯 Generating questions for:")
    print(f"   Role: {request.target_role}")
    print(f"   Level: {request.target_level}")
    print(f"   Focus Areas: {', '.join(focus_areas)}")
    print(f"   Question Mix: {request.num_technical} technical, {request.num_behavioral} behavioral, {request.num_system_design} system design")
    
    try:
        questions = generator.generate_questions(request)
        
        print(f"\n✅ Generated {len(questions.questions)} tailored questions")
        print(f"   Session ID: {questions.session_id}")
        print(f"   Total Duration: {questions.get_total_duration()} minutes")
        
        # Display questions
        print("\n\n📋 Generated Interview Questions:")
        print("=" * 70)
        
        for i, q in enumerate(questions.questions, 1):
            print(f"\n{i}. [{q.type.value.upper()}] [{q.difficulty.value.upper()}]")
            print(f"   {q.question}")
            print(f"   • Category: {q.category}")
            print(f"   • Skills Tested: {', '.join(q.skills_tested)}")
            print(f"   • Duration: {q.expected_duration_minutes} minutes")
            
            if q.follow_up_questions:
                print(f"   • Follow-ups:")
                for fu in q.follow_up_questions[:2]:
                    print(f"     - {fu}")
            
            if q.hints:
                print(f"   • Hints:")
                for hint in q.hints[:2]:
                    print(f"     - {hint}")
        
        # Summary statistics
        print("\n\n📊 Interview Session Summary:")
        print("=" * 70)
        print(f"Candidate: {parsed_resume.contact.name}")
        print(f"Target Role: {questions.target_role}")
        print(f"Experience Level: {questions.target_level}")
        print(f"Total Questions: {len(questions.questions)}")
        print(f"  • Technical: {questions.technical_count}")
        print(f"  • Behavioral: {questions.behavioral_count}")
        print(f"  • Other: {len(questions.questions) - questions.technical_count - questions.behavioral_count}")
        print(f"Estimated Duration: {questions.get_total_duration()} minutes")
        print(f"Session ID: {questions.session_id}")
        
        # Question breakdown by difficulty
        from src.question_generator.schemas import DifficultyLevel
        easy = len(questions.get_questions_by_difficulty(DifficultyLevel.EASY))
        medium = len(questions.get_questions_by_difficulty(DifficultyLevel.MEDIUM))
        hard = len(questions.get_questions_by_difficulty(DifficultyLevel.HARD))
        
        print(f"\nDifficulty Distribution:")
        print(f"  • Easy: {easy}")
        print(f"  • Medium: {medium}")
        print(f"  • Hard: {hard}")
        
        print("\n\n✅ Questions Generated Successfully!")
        
    except Exception as e:
        print(f"\n❌ Error generating questions: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 3: Evaluate Answers
    try:
        print("\n\n🎯 Step 3: Evaluate Sample Answers")
        print("-" * 70)
        
        # Initialize evaluator
        evaluator = AnswerEvaluator()
        
        # Sample answers for the first 3 questions
        sample_answers = [
            """Python is my primary language. I've used it extensively for backend development,
            building REST APIs with Django and Flask. I've also worked with async programming 
            using asyncio for high-performance applications. My projects include microservices 
            handling millions of requests per day.""",
            
            """In my current role at Tech Corp, I reduced API latency by 40% by implementing 
            caching strategies with Redis and optimizing database queries. I profiled the application 
            to identify bottlenecks, then introduced connection pooling and query optimization. 
            This improvement directly enhanced user experience.""",
            
            """I would design a scalable URL shortener using a distributed hash table approach. 
            Use base62 encoding to generate short codes from sequential IDs. Store mappings in 
            a distributed database like DynamoDB. Implement Redis caching for frequently accessed 
            URLs. Use load balancers and CDN for global distribution."""
        ]
        
        # Evaluate each answer
        evaluations = []
        for i, (question, answer) in enumerate(zip(questions.questions[:3], sample_answers)):
            print(f"\nEvaluating Question {i+1}: {question.question[:60]}...")
            
            eval_request = EvaluationRequest(
                question=question.question,
                answer=answer,
                question_type=question.type.value,
                difficulty_level=question.difficulty.value,
                session_id=questions.session_id
            )
            
            evaluation = evaluator.evaluate_answer(eval_request)
            evaluations.append(evaluation)
            
            print(f"  ✅ Score: {evaluation.overall_score}/100 ({evaluation.score_level.value})")
            print(f"  💪 Strengths: {len(evaluation.strengths)}")
            print(f"  ⚠️  Weaknesses: {len(evaluation.weaknesses)}")
        
        # Generate session summary
        print("\n\n📈 Step 4: Generate Session Summary")
        print("-" * 70)
        
        summary = evaluator.generate_session_summary(
            session_id=questions.session_id,
            evaluations=evaluations
        )
        
        print(f"\n📊 Interview Session Results:")
        print(f"   Candidate: {parsed_resume.contact.name}")
        print(f"   Questions Answered: {summary.questions_answered}/{summary.total_questions}")
        print(f"   Average Score: {summary.average_score:.1f}/100")
        print(f"   Overall Level: {summary.score_level.value}")
        print(f"   Consistency: {summary.consistency_score:.1f}/100")
        
        if summary.technical_score:
            print(f"   Technical Score: {summary.technical_score:.1f}/100")
        if summary.behavioral_score:
            print(f"   Behavioral Score: {summary.behavioral_score:.1f}/100")
        
        if summary.strongest_areas:
            print(f"\n   💪 Strongest Areas:")
            for area in summary.strongest_areas[:3]:
                print(f"      • {area}")
        
        if summary.weakest_areas:
            print(f"\n   📚 Areas for Improvement:")
            for area in summary.weakest_areas[:3]:
                print(f"      • {area}")
        
        if summary.hiring_recommendation:
            print(f"\n   🎯 Recommendation: {summary.hiring_recommendation}")
        
        # Detailed feedback for first question
        print("\n\n📝 Detailed Feedback Example (Question 1):")
        print("=" * 70)
        first_eval = evaluations[0]
        
        print(f"\nQuestion: {questions.questions[0].question}")
        print(f"Score: {first_eval.overall_score}/100 ({first_eval.score_level.value})")
        print(f"\n{first_eval.summary}")
        
        if first_eval.strengths:
            print(f"\n✅ Strengths:")
            for strength in first_eval.strengths:
                print(f"  • [{strength.category}] {strength.message}")
        
        if first_eval.weaknesses:
            print(f"\n⚠️  Weaknesses:")
            for weakness in first_eval.weaknesses:
                print(f"  • [{weakness.category}] {weakness.message}")
        
        if first_eval.suggestions:
            print(f"\n💡 Suggestions:")
            for suggestion in first_eval.suggestions[:3]:
                print(f"  • [{suggestion.category}] {suggestion.message}")
        
        if first_eval.key_takeaways:
            print(f"\n🎯 Key Takeaways:")
            for takeaway in first_eval.key_takeaways[:3]:
                print(f"  • {takeaway}")
        
        print("\n\n✅ Complete Integration Demo Finished!")
        print("=" * 70)
        print("\n🎉 PrepWise AI successfully demonstrated:")
        print("   1. ✅ Resume parsing and skill extraction")
        print("   2. ✅ Tailored question generation based on candidate profile")
        print("   3. ✅ Answer evaluation with detailed feedback")
        print("   4. ✅ Session summary with hiring recommendations")
        print("\n📦 All 4 Phases Integrated Successfully!")
        print("   Phase 1: Core Infrastructure ✅")
        print("   Phase 2: Resume Parser ✅")
        print("   Phase 3: Question Generator ✅")
        print("   Phase 4: Answer Evaluator ✅")
        
    except Exception as e:
        print(f"\n❌ Error in evaluation: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
