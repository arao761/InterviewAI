"""
Tests for Answer Evaluator
"""
import pytest
from src.evaluator.evaluator import AnswerEvaluator
from src.evaluator.schemas import (
    EvaluationRequest,
    BatchEvaluationRequest,
    EvaluationCriteria,
    ScoreLevel,
    FeedbackType
)


def test_evaluator_initialization():
    """Test answer evaluator can be initialized"""
    evaluator = AnswerEvaluator()
    assert evaluator is not None
    assert evaluator.llm_client is not None
    assert len(evaluator.criteria_definitions) > 0


def test_evaluate_technical_answer():
    """Test evaluating a technical answer"""
    evaluator = AnswerEvaluator()
    
    request = EvaluationRequest(
        question="Explain how a hash table works",
        answer="""A hash table is a data structure that uses a hash function to map keys to indices 
        in an array. It provides O(1) average-case lookup, insertion, and deletion. The hash function 
        converts the key into an index. Collisions can be handled using chaining (linked lists) or 
        open addressing (probing). Hash tables are used extensively in databases, caches, and 
        implementing sets and maps.""",
        question_type="technical",
        expected_answer_points=[
            "Hash function maps keys to indices",
            "O(1) average time complexity",
            "Collision handling methods"
        ],
        difficulty_level="medium"
    )
    
    evaluation = evaluator.evaluate_answer(request)
    
    assert evaluation is not None
    assert evaluation.overall_score >= 0
    assert evaluation.overall_score <= 100
    assert evaluation.score_level in [ScoreLevel.EXCELLENT, ScoreLevel.GOOD, ScoreLevel.FAIR, ScoreLevel.POOR]
    assert evaluation.evaluation_id.startswith("eval_")
    assert evaluation.answer_text == request.answer
    assert evaluation.question_text == request.question


def test_evaluate_behavioral_answer():
    """Test evaluating a behavioral answer"""
    evaluator = AnswerEvaluator()
    
    request = EvaluationRequest(
        question="Tell me about a time you had to work with a difficult team member",
        answer="""In my previous role, I worked with a colleague who often missed deadlines. 
        I approached them privately to understand the challenges they were facing. They were 
        overwhelmed with tasks. I suggested we break down their work into smaller milestones 
        and offered to help with some tasks. We set up weekly check-ins. Over time, they became 
        more reliable and our team's productivity improved significantly.""",
        question_type="behavioral",
        expected_answer_points=[
            "Specific situation described",
            "Actions taken",
            "Positive outcome"
        ]
    )
    
    evaluation = evaluator.evaluate_answer(request)
    
    assert evaluation is not None
    assert len(evaluation.strengths) > 0 or len(evaluation.weaknesses) > 0
    assert evaluation.question_type == "behavioral"


def test_poor_answer_evaluation():
    """Test evaluating a poor/short answer"""
    evaluator = AnswerEvaluator()
    
    request = EvaluationRequest(
        question="Explain the difference between TCP and UDP",
        answer="TCP is reliable, UDP is fast.",
        question_type="technical",
        difficulty_level="easy"
    )
    
    evaluation = evaluator.evaluate_answer(request)
    
    # Poor answer should get low score
    assert evaluation.overall_score < 60
    assert len(evaluation.weaknesses) > 0
    # Should identify completeness issues
    completeness_weaknesses = [w for w in evaluation.weaknesses if "complete" in w.message.lower() or "detail" in w.message.lower()]
    assert len(completeness_weaknesses) > 0


def test_excellent_answer_evaluation():
    """Test evaluating an excellent answer"""
    evaluator = AnswerEvaluator()
    
    request = EvaluationRequest(
        question="What is a RESTful API?",
        answer="""A RESTful API is an architectural style for web services that uses HTTP methods 
        (GET, POST, PUT, DELETE) to perform CRUD operations on resources. Key principles include:
        1) Statelessness - each request contains all necessary information
        2) Resource-based URLs - endpoints represent resources, not actions
        3) Standard HTTP methods for operations
        4) JSON or XML for data exchange
        5) Proper use of HTTP status codes
        
        For example, GET /users/123 retrieves user 123, POST /users creates a new user.
        REST APIs are scalable, maintainable, and language-agnostic, making them ideal for 
        modern web applications.""",
        question_type="technical",
        expected_answer_points=[
            "HTTP methods",
            "Stateless",
            "Resource-based",
            "Standard protocols"
        ],
        difficulty_level="easy"
    )
    
    evaluation = evaluator.evaluate_answer(request)
    
    # Excellent answer should get high score
    assert evaluation.overall_score >= 70
    assert len(evaluation.strengths) > 0


def test_criterion_scores():
    """Test that criterion scores are calculated"""
    evaluator = AnswerEvaluator()
    
    request = EvaluationRequest(
        question="What is polymorphism in OOP?",
        answer="Polymorphism allows objects of different types to be treated uniformly. It includes method overriding and interfaces.",
        question_type="technical",
        evaluation_criteria=["technical_accuracy", "clarity", "completeness"]
    )
    
    evaluation = evaluator.evaluate_answer(request)
    
    assert len(evaluation.criterion_scores) > 0
    for cs in evaluation.criterion_scores:
        assert cs.score >= 0
        assert cs.score <= 100
        assert cs.weight > 0


def test_feedback_items():
    """Test that feedback items are generated"""
    evaluator = AnswerEvaluator()
    
    request = EvaluationRequest(
        question="Explain database indexing",
        answer="Indexes make queries faster by creating a separate data structure.",
        question_type="technical"
    )
    
    evaluation = evaluator.evaluate_answer(request)
    
    # Should have some feedback
    total_feedback = len(evaluation.strengths) + len(evaluation.weaknesses) + len(evaluation.suggestions)
    assert total_feedback > 0
    
    # Check feedback structure
    for strength in evaluation.strengths:
        assert strength.type == FeedbackType.STRENGTH
        assert len(strength.message) > 0
    
    for weakness in evaluation.weaknesses:
        assert weakness.type == FeedbackType.WEAKNESS
        assert len(weakness.message) > 0


def test_batch_evaluation():
    """Test evaluating multiple answers in batch"""
    evaluator = AnswerEvaluator()
    
    batch_request = BatchEvaluationRequest(
        session_id="test_session_123",
        evaluations=[
            EvaluationRequest(
                question="What is a binary search tree?",
                answer="A BST is a tree where left children are smaller and right children are larger.",
                question_type="technical"
            ),
            EvaluationRequest(
                question="Describe a challenging project",
                answer="I led a team to migrate a legacy system to microservices, coordinating across multiple teams.",
                question_type="behavioral"
            )
        ],
        generate_summary=True
    )
    
    evaluations, summary = evaluator.evaluate_batch(batch_request)
    
    assert len(evaluations) == 2
    assert all(e.session_id == "test_session_123" for e in evaluations)
    
    # Check summary
    assert summary is not None
    assert summary.session_id == "test_session_123"
    assert summary.total_questions == 2
    assert summary.average_score >= 0
    assert summary.average_score <= 100


def test_session_summary_generation():
    """Test session summary generation"""
    evaluator = AnswerEvaluator()
    
    # Create mock evaluations
    from src.evaluator.schemas import AnswerEvaluation
    
    evaluations = []
    for i in range(3):
        eval_req = EvaluationRequest(
            question=f"Question {i+1}",
            answer=f"Answer {i+1} with reasonable detail and explanation",
            question_type="technical" if i < 2 else "behavioral"
        )
        evaluation = evaluator.evaluate_answer(eval_req)
        evaluations.append(evaluation)
    
    summary = evaluator.generate_session_summary("test_session", evaluations)
    
    assert summary.total_questions == 3
    assert summary.questions_answered == 3
    assert summary.average_score >= 0
    assert summary.average_score <= 100
    assert len(summary.score_distribution) > 0
    assert summary.hiring_recommendation in ["strong_yes", "yes", "maybe", "no"]


def test_missing_expected_points():
    """Test identification of missing points"""
    evaluator = AnswerEvaluator()
    
    request = EvaluationRequest(
        question="Explain the SOLID principles",
        answer="SOLID includes Single Responsibility and Open/Closed principles.",
        question_type="technical",
        expected_answer_points=[
            "Single Responsibility Principle",
            "Open/Closed Principle",
            "Liskov Substitution Principle",
            "Interface Segregation Principle",
            "Dependency Inversion Principle"
        ]
    )
    
    evaluation = evaluator.evaluate_answer(request)
    
    # Should identify missing points
    assert len(evaluation.missing_points) > 0 or evaluation.overall_score < 80


def test_evaluation_with_context():
    """Test evaluation with candidate context"""
    evaluator = AnswerEvaluator()
    
    request = EvaluationRequest(
        question="How would you implement authentication?",
        answer="I would use JWT tokens with proper security measures.",
        question_type="technical",
        candidate_context={
            "experience_level": "junior",
            "years_experience": 1
        },
        experience_level="junior"
    )
    
    evaluation = evaluator.evaluate_answer(request)
    
    # Evaluation should complete successfully
    assert evaluation is not None
    assert evaluation.overall_score >= 0


def test_answer_comparison():
    """Test comparing two answers"""
    evaluator = AnswerEvaluator()
    
    request1 = EvaluationRequest(
        question="What is recursion?",
        answer="Recursion is when a function calls itself.",
        question_type="technical"
    )
    
    request2 = EvaluationRequest(
        question="What is recursion?",
        answer="""Recursion is a programming technique where a function calls itself to solve a problem. 
        It requires a base case to stop and a recursive case. For example, calculating factorial: 
        factorial(n) = n * factorial(n-1). Benefits include elegant code for tree/graph traversal. 
        Drawbacks include stack overflow risk and potential inefficiency.""",
        question_type="technical"
    )
    
    eval1 = evaluator.evaluate_answer(request1)
    eval2 = evaluator.evaluate_answer(request2)
    
    comparison = evaluator.compare_answers(eval1, eval2)
    
    assert comparison is not None
    assert "score_difference" in comparison
    assert "better_answer" in comparison
    # The detailed answer should score better
    assert abs(comparison["score_difference"]) > 0


def test_high_priority_feedback():
    """Test filtering high-priority feedback"""
    evaluator = AnswerEvaluator()
    
    request = EvaluationRequest(
        question="Explain memory management in Python",
        answer="Python uses reference counting.",
        question_type="technical",
        difficulty_level="medium"
    )
    
    evaluation = evaluator.evaluate_answer(request)
    high_priority = evaluation.get_high_priority_feedback()
    
    assert "strengths" in high_priority
    assert "weaknesses" in high_priority
    assert "suggestions" in high_priority
    
    # All items should be high priority
    for weakness in high_priority["weaknesses"]:
        assert weakness.priority == "high"


def test_feedback_by_category():
    """Test filtering feedback by category"""
    evaluator = AnswerEvaluator()
    
    request = EvaluationRequest(
        question="What is a design pattern?",
        answer="Design patterns are reusable solutions to common problems.",
        question_type="technical"
    )
    
    evaluation = evaluator.evaluate_answer(request)
    
    # Test filtering by a category
    if evaluation.criterion_scores:
        category = evaluation.criterion_scores[0].criterion.value
        category_feedback = evaluation.get_feedback_by_category(category)
        
        assert "strengths" in category_feedback
        assert "weaknesses" in category_feedback
        assert "suggestions" in category_feedback


def test_evaluation_id_uniqueness():
    """Test that evaluation IDs are unique"""
    evaluator = AnswerEvaluator()
    
    request = EvaluationRequest(
        question="Test question",
        answer="Test answer",
        question_type="technical"
    )
    
    eval1 = evaluator.evaluate_answer(request)
    eval2 = evaluator.evaluate_answer(request)
    
    assert eval1.evaluation_id != eval2.evaluation_id
    assert eval1.evaluation_id.startswith("eval_")
    assert eval2.evaluation_id.startswith("eval_")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
