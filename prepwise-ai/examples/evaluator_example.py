"""
PrepWise AI - Answer Evaluator Examples
========================================

This example demonstrates how to use the Answer Evaluator (Phase 4)
to evaluate candidate answers and provide detailed feedback.
"""

from src.evaluator.evaluator import AnswerEvaluator
from src.evaluator.schemas import (
    EvaluationRequest,
    BatchEvaluationRequest,
    EvaluationCriteria,
    ScoreLevel,
    FeedbackType
)


def example_1_basic_evaluation():
    """Example 1: Basic answer evaluation"""
    print("\n" + "=" * 60)
    print("Example 1: Basic Technical Answer Evaluation")
    print("=" * 60)
    
    evaluator = AnswerEvaluator()
    
    # Create evaluation request
    request = EvaluationRequest(
        question="What is a hash table and how does it work?",
        answer="""A hash table is a data structure that provides O(1) average-case 
        lookup time by using a hash function to map keys to array indices. 
        It handles collisions using techniques like chaining (linked lists) 
        or open addressing (probing). The hash function converts keys into 
        array indices, and the load factor determines when to resize.""",
        question_type="technical",
        expected_answer_points=[
            "Hash function",
            "O(1) lookup time",
            "Collision handling",
            "Array/bucket structure"
        ]
    )
    
    # Evaluate the answer
    evaluation = evaluator.evaluate_answer(request)
    
    # Display results
    print(f"\n📊 Overall Score: {evaluation.overall_score}/100")
    print(f"📈 Score Level: {evaluation.score_level.value}")
    print(f"\n📝 Summary: {evaluation.summary}")
    
    print(f"\n✅ Strengths ({len(evaluation.strengths)}):")
    for strength in evaluation.strengths:
        print(f"  • [{strength.category}] {strength.message}")
    
    print(f"\n⚠️  Weaknesses ({len(evaluation.weaknesses)}):")
    for weakness in evaluation.weaknesses:
        print(f"  • [{weakness.category}] {weakness.message}")
    
    print(f"\n💡 Suggestions ({len(evaluation.suggestions)}):")
    for suggestion in evaluation.suggestions:
        print(f"  • [{suggestion.category}] {suggestion.message}")
        if suggestion.examples:
            for example in suggestion.examples:
                print(f"    - {example}")


def example_2_behavioral_evaluation():
    """Example 2: Behavioral answer evaluation"""
    print("\n" + "=" * 60)
    print("Example 2: Behavioral Answer Evaluation")
    print("=" * 60)
    
    evaluator = AnswerEvaluator()
    
    request = EvaluationRequest(
        question="Tell me about a time you had to deal with a difficult team member.",
        answer="""On my previous project, I worked with a team member who consistently 
        missed deadlines. I scheduled a one-on-one meeting to understand the challenges 
        they were facing. It turned out they were overwhelmed with other responsibilities. 
        We worked together to prioritize tasks and I helped redistribute some of the workload. 
        This improved their performance and strengthened our working relationship.""",
        question_type="behavioral",
        evaluation_criteria=[
            "communication",
            "problem_solving",
            "leadership",
            "structure"
        ]
    )
    
    evaluation = evaluator.evaluate_answer(request)
    
    print(f"\n📊 Overall Score: {evaluation.overall_score}/100")
    print(f"📈 Score Level: {evaluation.score_level.value}")
    
    print(f"\n📋 Criterion Scores:")
    for cs in evaluation.criterion_scores:
        print(f"  • {cs.criterion.value}: {cs.score:.1f}/100")
        if cs.feedback:
            print(f"    → {cs.feedback}")
    
    print(f"\n🎯 Key Takeaways:")
    for takeaway in evaluation.key_takeaways:
        print(f"  • {takeaway}")


def example_3_batch_evaluation():
    """Example 3: Batch evaluation with session summary"""
    print("\n" + "=" * 60)
    print("Example 3: Batch Evaluation with Session Summary")
    print("=" * 60)
    
    evaluator = AnswerEvaluator()
    
    # Create multiple evaluation requests
    evaluations_list = [
        EvaluationRequest(
            question="Explain the difference between a stack and a queue.",
            answer="A stack follows LIFO (Last In First Out) while a queue follows FIFO (First In First Out).",
            question_type="technical"
        ),
        EvaluationRequest(
            question="What is Big O notation?",
            answer="Big O notation describes the time or space complexity of an algorithm in terms of input size.",
            question_type="technical"
        ),
        EvaluationRequest(
            question="Describe your leadership style.",
            answer="I believe in collaborative leadership. I set clear goals, empower team members, and provide support when needed.",
            question_type="behavioral"
        )
    ]
    
    # Create batch request
    batch_request = BatchEvaluationRequest(
        session_id="demo_session_001",
        evaluations=evaluations_list,
        generate_summary=True
    )
    
    # Evaluate batch
    evaluations, summary = evaluator.evaluate_batch(batch_request)
    
    print(f"\n📊 Session Results:")
    print(f"  Total Questions: {len(evaluations)}")
    
    for i, eval in enumerate(evaluations, 1):
        print(f"\n  Question {i}:")
        print(f"    Score: {eval.overall_score}/100 ({eval.score_level.value})")
        print(f"    Type: {eval.question_type}")
    
    if summary:
        print(f"\n📈 Session Summary:")
        print(f"  Average Score: {summary.average_score:.1f}/100")
        print(f"  Overall Level: {summary.score_level.value}")
        print(f"  Consistency: {summary.consistency_score:.1f}/100")
        
        if summary.strongest_areas:
            print(f"\n  💪 Strongest Areas:")
            for area in summary.strongest_areas:
                print(f"    • {area}")
        
        if summary.weakest_areas:
            print(f"\n  📚 Areas for Improvement:")
            for area in summary.weakest_areas:
                print(f"    • {area}")
        
        if summary.hiring_recommendation:
            print(f"\n  🎯 Recommendation: {summary.hiring_recommendation}")


def example_4_custom_criteria():
    """Example 4: Evaluation with custom criteria"""
    print("\n" + "=" * 60)
    print("Example 4: Custom Evaluation Criteria")
    print("=" * 60)
    
    evaluator = AnswerEvaluator()
    
    request = EvaluationRequest(
        question="How would you design a URL shortener service?",
        answer="""I would design it using a hash-based approach. Store mappings 
        in a distributed database like DynamoDB for scalability. Use a load 
        balancer to distribute traffic. Implement caching with Redis for 
        frequently accessed URLs. For the hash, I'd use base62 encoding 
        to generate short codes. The system should handle billions of URLs.""",
        question_type="technical",
        evaluation_criteria=[
            "technical_accuracy",
            "depth",
            "system_design",
            "scalability"
        ],
        difficulty_level="senior",
        expected_answer_points=[
            "Hash/encoding mechanism",
            "Database choice",
            "Scalability considerations",
            "Caching strategy"
        ]
    )
    
    evaluation = evaluator.evaluate_answer(request)
    
    print(f"\n📊 Overall Score: {evaluation.overall_score}/100")
    print(f"📈 Difficulty: {request.difficulty_level}")
    
    print(f"\n📋 Custom Criteria Scores:")
    for cs in evaluation.criterion_scores:
        print(f"  • {cs.criterion.value}: {cs.score:.1f}/100 (weight: {cs.weight})")
    
    # Filter high-priority feedback
    high_priority_items = [
        f for f in (evaluation.strengths + evaluation.weaknesses + evaluation.suggestions)
        if f.priority == "high"
    ]
    
    print(f"\n⚡ High Priority Feedback ({len(high_priority_items)}):")
    for item in high_priority_items:
        icon = "✅" if item.type == FeedbackType.STRENGTH else "⚠️" if item.type == FeedbackType.WEAKNESS else "💡"
        print(f"  {icon} [{item.type.value}] {item.message}")


def example_5_compare_answers():
    """Example 5: Compare two different answers"""
    print("\n" + "=" * 60)
    print("Example 5: Compare Two Candidate Answers")
    print("=" * 60)
    
    evaluator = AnswerEvaluator()
    
    question = "What is recursion?"
    
    # Evaluate answer 1
    eval1 = evaluator.evaluate_answer(EvaluationRequest(
        question=question,
        answer="Recursion is when a function calls itself.",
        question_type="technical"
    ))
    
    # Evaluate answer 2
    eval2 = evaluator.evaluate_answer(EvaluationRequest(
        question=question,
        answer="""Recursion is a programming technique where a function calls itself 
        to solve a problem by breaking it into smaller subproblems. It requires 
        a base case to terminate and a recursive case that moves toward the base case. 
        Examples include calculating factorials or traversing tree structures.""",
        question_type="technical"
    ))
    
    # Compare
    comparison = evaluator.compare_answers(eval1, eval2)
    
    print(f"\n📊 Answer Comparison:")
    print(f"  Answer 1: {eval1.overall_score:.1f}/100 ({eval1.score_level.value})")
    print(f"  Answer 2: {eval2.overall_score:.1f}/100 ({eval2.score_level.value})")
    print(f"  Score Difference: {comparison['score_difference']:.1f} points")
    print(f"  Better Answer: {comparison['better_answer']}")
    
    print(f"\n📈 Criterion Comparison:")
    for criterion, diff in comparison['criterion_differences'].items():
        direction = "↑" if diff > 0 else "↓" if diff < 0 else "="
        print(f"  {criterion}: {direction} {abs(diff):.1f} points")
    
    print(f"\n💡 Key Differences:")
    for diff in comparison['key_differences']:
        print(f"  • {diff}")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("PrepWise AI - Answer Evaluator Examples")
    print("=" * 60)
    
    try:
        example_1_basic_evaluation()
        example_2_behavioral_evaluation()
        example_3_batch_evaluation()
        example_4_custom_criteria()
        example_5_compare_answers()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
