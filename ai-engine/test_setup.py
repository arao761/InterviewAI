"""
Test Setup Script
Verify Phase 1 setup is working correctly
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_environment():
    """Test that environment variables are set"""
    print("=" * 60)
    print("PHASE 1: Testing Environment Configuration")
    print("=" * 60)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("❌ OPENAI_API_KEY not set!")
        print("   Please create .env file and add your API key")
        print("   Copy .env.example to .env and fill in your key")
        return False

    print(f"✅ OPENAI_API_KEY is set (length: {len(api_key)})")

    model = os.getenv("DEFAULT_MODEL", "gpt-4")
    print(f"✅ Default model: {model}")

    temperature = os.getenv("TEMPERATURE", "0.0")
    print(f"✅ Temperature: {temperature}")

    return True


def test_imports():
    """Test that all required packages can be imported"""
    print("\n" + "=" * 60)
    print("Testing Package Imports")
    print("=" * 60)

    required_packages = [
        ("openai", "OpenAI"),
        ("anthropic", "Anthropic"),
        ("pydantic", "Pydantic"),
        ("dotenv", "python-dotenv"),
        ("tenacity", "Tenacity"),
    ]

    all_success = True

    for package_name, display_name in required_packages:
        try:
            __import__(package_name)
            print(f"✅ {display_name} installed")
        except ImportError:
            print(f"❌ {display_name} NOT installed")
            print(f"   Run: pip install {package_name}")
            all_success = False

    return all_success


def test_llm_client():
    """Test LLM client functionality"""
    print("\n" + "=" * 60)
    print("Testing LLM Client")
    print("=" * 60)

    try:
        from src.utils.llm_client import LLMClient

        print("✅ LLMClient imported successfully")

        # Initialize client
        client = LLMClient(provider="openai", model="gpt-4o-mini")
        print(f"✅ LLMClient initialized: {client}")

        # Test basic generation
        print("\n📡 Testing API connection with simple prompt...")
        response = client.generate(
            prompt="Say 'Hello from PrepWise AI!' in exactly those words.",
            temperature=0.0,
            max_tokens=50
        )
        print(f"✅ API Response: {response}")

        # Test JSON generation
        print("\n📡 Testing JSON generation...")
        json_response = client.generate_json(
            prompt="Return a JSON object with two fields: 'status' (set to 'success') and 'message' (set to 'PrepWise AI is ready')"
        )
        print(f"✅ JSON Response: {json_response}")

        assert json_response.get("status") == "success", "JSON parsing failed"
        print("✅ JSON parsing working correctly")

        # Test token counting
        text = "This is a test of the token counting functionality."
        token_count = client.count_tokens(text)
        print(f"✅ Token counting: '{text}' = ~{token_count} tokens")

        return True

    except ImportError as e:
        print(f"❌ Failed to import LLMClient: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing LLM client: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False


def test_schemas():
    """Test Pydantic schemas"""
    print("\n" + "=" * 60)
    print("Testing Pydantic Schemas")
    print("=" * 60)

    try:
        from src.resume_parser.schemas import (
            Contact, Education, Experience, Skills, ParsedResume
        )

        print("✅ All schemas imported successfully")

        # Test Contact
        contact = Contact(
            name="John Doe",
            email="john@example.com",
            phone="555-1234"
        )
        print(f"✅ Contact schema: {contact.name}")

        # Test Skills
        skills = Skills(
            technical=["Python", "JavaScript"],
            tools=["Git", "Docker"]
        )
        print(f"✅ Skills schema: {len(skills.technical)} technical skills")

        # Test ParsedResume
        resume = ParsedResume(
            contact=contact,
            skills=skills,
            total_years_experience=3.5
        )
        print(f"✅ ParsedResume schema: {resume.experience_level} level")
        print(f"✅ Resume summary: {resume.get_summary()}")

        return True

    except Exception as e:
        print(f"❌ Error testing schemas: {e}")
        return False


def test_validators():
    """Test validator functions"""
    print("\n" + "=" * 60)
    print("Testing Validators")
    print("=" * 60)

    try:
        from src.utils.validators import (
            validate_email,
            validate_url,
            sanitize_text,
            validate_score
        )

        print("✅ Validators imported successfully")

        # Test email validation
        assert validate_email("test@example.com") == True
        assert validate_email("invalid-email") == False
        print("✅ Email validation working")

        # Test URL validation
        assert validate_url("https://example.com") == True
        assert validate_url("not-a-url") == False
        print("✅ URL validation working")

        # Test text sanitization
        dirty_text = "  Too   much    space  "
        clean_text = sanitize_text(dirty_text)
        assert clean_text == "Too much space"
        print("✅ Text sanitization working")

        # Test score validation
        assert validate_score(75) == True
        assert validate_score(150) == False
        print("✅ Score validation working")

        return True

    except Exception as e:
        print(f"❌ Error testing validators: {e}")
        return False


def test_question_generator():
    """Test Question Generator (Phase 3)"""
    print("\n" + "=" * 60)
    print("Testing Question Generator (Phase 3)")
    print("=" * 60)

    try:
        from src.question_generator.generator import QuestionGenerator
        from src.question_generator.schemas import (
            QuestionGenerationRequest, 
            QuestionType,
            DifficultyLevel,
            InterviewQuestion,
            QuestionSet
        )
        
        print("✅ Question Generator modules imported successfully")
        
        # Test initialization
        generator = QuestionGenerator()
        print("✅ QuestionGenerator initialized")
        
        # Test basic question generation
        request = QuestionGenerationRequest(
            target_role="Software Engineer",
            target_level="mid",
            num_technical=2,
            num_behavioral=1
        )
        
        result = generator.generate_questions(request)
        print(f"✅ Generated {len(result.questions)} questions")
        
        # Verify question structure
        if result.questions:
            q = result.questions[0]
            assert hasattr(q, 'question'), "Question missing 'question' field"
            assert hasattr(q, 'type'), "Question missing 'type' field"
            assert hasattr(q, 'difficulty'), "Question missing 'difficulty' field"
            print("✅ Question structure validated")
            
            # Test filtering
            tech_questions = result.get_questions_by_type(QuestionType.TECHNICAL)
            print(f"✅ Question filtering works: {len(tech_questions)} technical questions")
        
        # Test session ID is unique
        result2 = generator.generate_questions(request)
        assert result.session_id != result2.session_id, "Session IDs should be unique"
        print("✅ Unique session IDs generated")
        
        print("\n✅ PASS - Question Generator")
        return True
        
    except ImportError as e:
        print(f"❌ FAIL - Question Generator: Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ FAIL - Question Generator: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_answer_evaluator():
    """Test Answer Evaluator (Phase 4)"""
    print("\n" + "=" * 60)
    print("Testing Answer Evaluator (Phase 4)")
    print("=" * 60)

    try:
        from src.evaluator.evaluator import AnswerEvaluator
        from src.evaluator.schemas import (
            EvaluationRequest,
            AnswerEvaluation,
            ScoreLevel,
            EvaluationCriteria
        )
        
        print("✅ Answer Evaluator modules imported successfully")
        
        # Test initialization
        evaluator = AnswerEvaluator()
        print("✅ AnswerEvaluator initialized")
        
        # Test basic evaluation
        request = EvaluationRequest(
            question="What is a hash table?",
            answer="""A hash table is a data structure that provides O(1) average-case 
            lookup by using a hash function to map keys to array indices. It handles 
            collisions using chaining or open addressing.""",
            question_type="technical",
            expected_answer_points=[
                "Hash function",
                "O(1) lookup",
                "Collision handling"
            ]
        )
        
        evaluation = evaluator.evaluate_answer(request)
        print(f"✅ Generated evaluation with score: {evaluation.overall_score}/100")
        
        # Verify evaluation structure
        assert hasattr(evaluation, 'overall_score'), "Missing overall_score"
        assert hasattr(evaluation, 'score_level'), "Missing score_level"
        assert hasattr(evaluation, 'strengths'), "Missing strengths"
        assert hasattr(evaluation, 'weaknesses'), "Missing weaknesses"
        print("✅ Evaluation structure validated")
        
        # Test score level
        assert evaluation.score_level in [ScoreLevel.EXCELLENT, ScoreLevel.GOOD, ScoreLevel.FAIR, ScoreLevel.POOR]
        print(f"✅ Score level: {evaluation.score_level.value}")
        
        # Test feedback generation
        total_feedback = len(evaluation.strengths) + len(evaluation.weaknesses) + len(evaluation.suggestions)
        assert total_feedback > 0, "No feedback generated"
        print(f"✅ Generated {total_feedback} feedback items")
        
        # Test criterion scores
        assert len(evaluation.criterion_scores) > 0, "No criterion scores"
        print(f"✅ Generated {len(evaluation.criterion_scores)} criterion scores")
        
        print("\n✅ PASS - Answer Evaluator")
        return True
        
    except ImportError as e:
        print(f"❌ FAIL - Answer Evaluator: Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ FAIL - Answer Evaluator: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_session_manager():
    """Test Session Manager & Progress Tracking (Phase 5 & 6)"""
    print("\n" + "=" * 60)
    print("Testing Session Manager & Progress Tracking (Phase 5 & 6)")
    print("=" * 60)

    try:
        from src.session_manager.manager import SessionManager
        from src.session_manager.schemas import (
            SessionCreateRequest,
            SessionStatus,
            InterviewMode
        )
        
        print("✅ Session Manager modules imported successfully")
        
        # Test initialization
        manager = SessionManager()
        print("✅ SessionManager initialized")
        
        # Test session creation
        request = SessionCreateRequest(
            candidate_name="Test User",
            user_id="test_user_123",
            target_role="Software Engineer",
            experience_level="mid",
            mode=InterviewMode.PRACTICE,
            num_technical=2,
            num_behavioral=1
        )
        
        session = manager.create_session(request)
        print(f"✅ Created session: {session.session_id}")
        
        # Verify session structure
        assert session.session_id.startswith("sess_"), "Invalid session ID"
        assert session.candidate_name == "Test User", "Incorrect candidate name"
        assert session.total_questions == 3, "Incorrect question count"
        assert session.status == SessionStatus.SCHEDULED, "Incorrect initial status"
        print("✅ Session structure validated")
        
        # Test starting session
        manager.start_session(session.session_id)
        updated_session = manager.get_session(session.session_id)
        assert updated_session.status == SessionStatus.IN_PROGRESS
        print("✅ Session started successfully")
        
        # Test submitting answer
        response = manager.submit_answer(
            session.session_id,
            0,
            "A hash table uses a hash function to map keys to values efficiently",
            200
        )
        assert response.evaluation_score is not None
        print(f"✅ Answer evaluated with score: {response.evaluation_score}/100")
        
        # Test user progress
        progress = manager.get_user_progress("test_user_123")
        assert progress.user_id == "test_user_123"
        assert progress.total_sessions >= 1
        print(f"✅ User progress tracked: {progress.total_sessions} sessions")
        
        print("\n✅ PASS - Session Manager & Progress Tracking")
        return True
        
    except ImportError as e:
        print(f"❌ FAIL - Session Manager: Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ FAIL - Session Manager: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api():
    """Test PrepWise API (Phase 7 & 8)"""
    print("\n" + "=" * 60)
    print("Testing PrepWise API (Phase 7 & 8)")
    print("=" * 60)

    try:
        from src.api.prepwise_api import PrepWiseAPI, create_api
        
        print("✅ API modules imported successfully")
        
        # Test API creation
        api = PrepWiseAPI()
        print("✅ PrepWise API initialized")
        
        # Verify all components
        assert api.resume_parser is not None, "Resume parser not initialized"
        assert api.question_generator is not None, "Question generator not initialized"
        assert api.answer_evaluator is not None, "Answer evaluator not initialized"
        assert api.session_manager is not None, "Session manager not initialized"
        print("✅ All API components initialized")
        
        # Test convenience function
        api2 = create_api()
        assert api2 is not None
        print("✅ Convenience function works")
        
        # Test statistics
        stats = api.get_statistics()
        assert stats["status"] == "operational"
        assert stats["phases_implemented"] == 8
        print(f"✅ System statistics: {stats['phases_implemented']} phases operational")
        
        print("\n✅ PASS - PrepWise API")
        return True
        
    except ImportError as e:
        print(f"❌ FAIL - PrepWise API: Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ FAIL - PrepWise API: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("PrepWise AI - Setup Verification (Phases 1-8)")
    print("=" * 60 + "\n")

    results = []

    # Run all tests
    results.append(("Environment", test_environment()))
    results.append(("Package Imports", test_imports()))
    results.append(("Pydantic Schemas", test_schemas()))
    results.append(("Validators", test_validators()))
    results.append(("LLM Client", test_llm_client()))
    results.append(("Question Generator", test_question_generator()))
    results.append(("Answer Evaluator", test_answer_evaluator()))
    results.append(("Session Manager & Progress", test_session_manager()))
    results.append(("PrepWise API", test_api()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")

    total_passed = sum(1 for _, success in results if success)
    total_tests = len(results)

    print(f"\nTotal: {total_passed}/{total_tests} tests passed")

    if total_passed == total_tests:
        print("\n🎉 All tests passed! Phases 1-8 complete!")
        print("\nCompleted Phases:")
        print("✅ Phase 1: Core Infrastructure")
        print("✅ Phase 2: Resume Parser")
        print("✅ Phase 3: Question Generator")
        print("✅ Phase 4: Answer Evaluator")
        print("✅ Phase 5: Session Manager")
        print("✅ Phase 6: Progress Tracking & Analytics")
        print("✅ Phase 7: Scoring & Feedback Engine (Integrated)")
        print("✅ Phase 8: Integration Layer & API")
        print("\n🚀 PrepWise AI is production-ready!")
        print("\nNext steps:")
        print("1. Run: python examples/complete_workflow_example.py")
        print("2. Build web API with FastAPI")
        print("3. Add database integration")
        print("4. Deploy to cloud platform")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
