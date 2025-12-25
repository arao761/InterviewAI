"""
Tests for Question Generator
"""
import pytest
from src.question_generator.generator import QuestionGenerator
from src.question_generator.schemas import (
    QuestionGenerationRequest,
    QuestionType,
    DifficultyLevel,
    InterviewQuestion,
    QuestionSet
)


def test_question_generator_initialization():
    """Test question generator can be initialized"""
    generator = QuestionGenerator()
    assert generator is not None
    assert generator.llm_client is not None


def test_generate_technical_questions():
    """Test generating technical questions"""
    generator = QuestionGenerator()
    
    request = QuestionGenerationRequest(
        target_role="Software Engineer",
        target_level="mid",
        num_technical=3,
        num_behavioral=0
    )
    
    result = generator.generate_questions(request)
    
    assert result is not None
    assert len(result.questions) == 3
    assert all(q.type == QuestionType.TECHNICAL for q in result.questions)
    assert result.technical_count == 3


def test_generate_behavioral_questions():
    """Test generating behavioral questions"""
    generator = QuestionGenerator()
    
    request = QuestionGenerationRequest(
        target_role="Product Manager",
        target_level="senior",
        num_technical=0,
        num_behavioral=3
    )
    
    result = generator.generate_questions(request)
    
    assert result is not None
    assert len(result.questions) == 3
    assert all(q.type == QuestionType.BEHAVIORAL for q in result.questions)
    assert result.behavioral_count == 3


def test_generate_mixed_questions():
    """Test generating mixed question types"""
    generator = QuestionGenerator()
    
    request = QuestionGenerationRequest(
        target_role="Full Stack Developer",
        target_level="mid",
        num_technical=2,
        num_behavioral=2,
        num_situational=1
    )
    
    result = generator.generate_questions(request)
    
    assert result is not None
    assert len(result.questions) == 5
    assert result.technical_count == 2
    assert result.behavioral_count == 2


def test_generate_system_design_questions():
    """Test generating system design questions"""
    generator = QuestionGenerator()
    
    request = QuestionGenerationRequest(
        target_role="Senior Software Engineer",
        target_level="senior",
        num_technical=0,
        num_behavioral=0,
        num_system_design=2
    )
    
    result = generator.generate_questions(request)
    
    assert result is not None
    assert len(result.questions) == 2
    assert all(q.type == QuestionType.SYSTEM_DESIGN for q in result.questions)


def test_question_set_filters():
    """Test question set filtering methods"""
    generator = QuestionGenerator()
    
    request = QuestionGenerationRequest(
        target_role="Data Scientist",
        target_level="junior",
        num_technical=3,
        num_behavioral=2
    )
    
    result = generator.generate_questions(request)
    
    # Test filtering by type
    technical_qs = result.get_questions_by_type(QuestionType.TECHNICAL)
    assert len(technical_qs) == 3
    
    behavioral_qs = result.get_questions_by_type(QuestionType.BEHAVIORAL)
    assert len(behavioral_qs) == 2


def test_session_id_generation():
    """Test unique session IDs are generated"""
    generator = QuestionGenerator()
    
    request = QuestionGenerationRequest(
        target_role="DevOps Engineer",
        target_level="mid",
        num_technical=1
    )
    
    result1 = generator.generate_questions(request)
    result2 = generator.generate_questions(request)
    
    assert result1.session_id != result2.session_id
    assert result1.session_id.startswith("sess_")
    assert result2.session_id.startswith("sess_")


def test_question_structure():
    """Test that generated questions have proper structure"""
    generator = QuestionGenerator()
    
    request = QuestionGenerationRequest(
        target_role="Software Engineer",
        target_level="mid",
        num_technical=1
    )
    
    result = generator.generate_questions(request)
    
    assert len(result.questions) > 0
    
    question = result.questions[0]
    assert hasattr(question, 'question')
    assert hasattr(question, 'type')
    assert hasattr(question, 'difficulty')
    assert hasattr(question, 'category')
    assert hasattr(question, 'skills_tested')
    assert hasattr(question, 'expected_duration_minutes')
    
    assert isinstance(question.question, str)
    assert len(question.question) > 0
    assert isinstance(question.type, QuestionType)
    assert isinstance(question.difficulty, DifficultyLevel)


def test_difficulty_levels():
    """Test questions are generated with appropriate difficulty"""
    generator = QuestionGenerator()
    
    # Junior level should have easier questions
    junior_request = QuestionGenerationRequest(
        target_role="Software Engineer",
        target_level="junior",
        num_technical=2
    )
    
    junior_result = generator.generate_questions(junior_request)
    
    # Senior level should have harder questions
    senior_request = QuestionGenerationRequest(
        target_role="Software Engineer",
        target_level="senior",
        num_technical=2
    )
    
    senior_result = generator.generate_questions(senior_request)
    
    # Just verify both generate successfully
    assert len(junior_result.questions) == 2
    assert len(senior_result.questions) == 2


def test_focus_areas():
    """Test question generation with focus areas"""
    generator = QuestionGenerator()
    
    request = QuestionGenerationRequest(
        target_role="Software Engineer",
        target_level="mid",
        num_technical=2,
        focus_areas=["Python", "algorithms", "databases"]
    )
    
    result = generator.generate_questions(request)
    
    assert len(result.questions) == 2
    assert result.target_role == "Software Engineer"


def test_question_duration():
    """Test that questions have reasonable durations"""
    generator = QuestionGenerator()
    
    request = QuestionGenerationRequest(
        target_role="Software Engineer",
        target_level="mid",
        num_technical=2,
        num_behavioral=1
    )
    
    result = generator.generate_questions(request)
    
    total_duration = result.get_total_duration()
    assert total_duration > 0
    assert total_duration < 200  # Reasonable upper bound


def test_resume_context():
    """Test question generation with resume context"""
    generator = QuestionGenerator()
    
    resume_data = {
        "skills": {
            "technical": ["Python", "Django", "React"],
            "tools": ["Git", "Docker"]
        },
        "experience": [
            {"title": "Software Engineer", "company": "Tech Corp"}
        ]
    }
    
    request = QuestionGenerationRequest(
        target_role="Senior Software Engineer",
        target_level="senior",
        num_technical=2,
        resume_context=resume_data,
        tailor_to_experience=True
    )
    
    result = generator.generate_questions(request)
    
    assert len(result.questions) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
