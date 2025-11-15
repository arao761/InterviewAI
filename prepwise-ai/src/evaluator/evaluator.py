"""
Answer Evaluator
Evaluates candidate answers and generates detailed feedback
"""

from typing import List, Dict, Optional, Any, Tuple
import re
import uuid
from datetime import datetime
import time

from src.evaluator.schemas import (
    AnswerEvaluation,
    EvaluationRequest,
    BatchEvaluationRequest,
    SessionSummary,
    CriterionScore,
    FeedbackItem,
    EvaluationCriteria,
    FeedbackType,
    ScoreLevel
)
from src.utils.llm_client import LLMClient


class AnswerEvaluator:
    """Evaluates interview answers using LLM"""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """
        Initialize answer evaluator
        
        Args:
            llm_client: LLM client for evaluation
        """
        self.llm_client = llm_client or LLMClient()
        self._load_evaluation_criteria()
    
    def _load_evaluation_criteria(self):
        """Load evaluation criteria definitions"""
        self.criteria_definitions = {
            EvaluationCriteria.TECHNICAL_ACCURACY: {
                "description": "Correctness of technical information",
                "weight": 0.30
            },
            EvaluationCriteria.COMPLETENESS: {
                "description": "Coverage of all important aspects",
                "weight": 0.20
            },
            EvaluationCriteria.CLARITY: {
                "description": "Clear and understandable explanation",
                "weight": 0.15
            },
            EvaluationCriteria.STRUCTURE: {
                "description": "Logical organization and flow",
                "weight": 0.10
            },
            EvaluationCriteria.RELEVANCE: {
                "description": "Staying on topic and addressing the question",
                "weight": 0.10
            },
            EvaluationCriteria.DEPTH: {
                "description": "Level of detail and insight",
                "weight": 0.10
            },
            EvaluationCriteria.EXAMPLES: {
                "description": "Use of examples to illustrate points",
                "weight": 0.05
            }
        }
    
    def evaluate_answer(
        self,
        request: EvaluationRequest
    ) -> AnswerEvaluation:
        """
        Evaluate a single answer
        
        Args:
            request: Evaluation request with question and answer
            
        Returns:
            AnswerEvaluation with scores and feedback
        """
        start_time = time.time()
        
        # Generate evaluation ID
        eval_id = self._generate_evaluation_id()
        
        # Determine question ID
        question_id = request.question_id or f"q_{uuid.uuid4().hex[:8]}"
        
        # Build evaluation prompt
        prompt = self._build_evaluation_prompt(request)
        
        try:
            # Get LLM evaluation
            llm_response = self.llm_client.generate_json(
                prompt=prompt,
                temperature=0.3,
                max_tokens=2000
            )
            
            # Parse LLM response
            evaluation = self._parse_llm_evaluation(
                llm_response,
                request,
                eval_id,
                question_id
            )
            
        except Exception as e:
            print(f"Error getting LLM evaluation: {e}")
            # Fallback to rule-based evaluation
            evaluation = self._fallback_evaluation(request, eval_id, question_id)
        
        # Calculate duration
        evaluation.evaluation_duration_seconds = time.time() - start_time
        evaluation.evaluator_model = self.llm_client.model
        
        # Add criterion scores if not present
        if not evaluation.criterion_scores:
            evaluation.criterion_scores = self._calculate_criterion_scores(
                evaluation.overall_score,
                request.evaluation_criteria
            )
        
        return evaluation
    
    def evaluate_batch(
        self,
        request: BatchEvaluationRequest
    ) -> Tuple[List[AnswerEvaluation], Optional[SessionSummary]]:
        """
        Evaluate multiple answers in a session
        
        Args:
            request: Batch evaluation request
            
        Returns:
            Tuple of (list of evaluations, optional session summary)
        """
        evaluations = []
        
        # Evaluate each answer
        for eval_request in request.evaluations:
            eval_request.session_id = request.session_id
            if request.candidate_context:
                eval_request.candidate_context = request.candidate_context
            
            evaluation = self.evaluate_answer(eval_request)
            evaluations.append(evaluation)
        
        # Generate session summary if requested
        summary = None
        if request.generate_summary:
            summary = self.generate_session_summary(
                session_id=request.session_id,
                evaluations=evaluations
            )
        
        return evaluations, summary
    
    def generate_session_summary(
        self,
        session_id: str,
        evaluations: List[AnswerEvaluation]
    ) -> SessionSummary:
        """
        Generate summary for an interview session
        
        Args:
            session_id: Session identifier
            evaluations: List of answer evaluations
            
        Returns:
            SessionSummary with overall performance analysis
        """
        if not evaluations:
            return SessionSummary(
                session_id=session_id,
                total_questions=0,
                questions_answered=0,
                average_score=0.0,
                score_level=ScoreLevel.POOR
            )
        
        # Calculate statistics
        total_questions = len(evaluations)
        average_score = sum(e.overall_score for e in evaluations) / total_questions
        
        # Score distribution
        score_distribution = {
            "excellent": sum(1 for e in evaluations if e.score_level == ScoreLevel.EXCELLENT),
            "good": sum(1 for e in evaluations if e.score_level == ScoreLevel.GOOD),
            "fair": sum(1 for e in evaluations if e.score_level == ScoreLevel.FAIR),
            "poor": sum(1 for e in evaluations if e.score_level == ScoreLevel.POOR)
        }
        
        # Calculate category scores
        technical_evals = [e for e in evaluations if e.question_type == "technical"]
        behavioral_evals = [e for e in evaluations if e.question_type == "behavioral"]
        
        technical_score = None
        if technical_evals:
            technical_score = sum(e.overall_score for e in technical_evals) / len(technical_evals)
        
        behavioral_score = None
        if behavioral_evals:
            behavioral_score = sum(e.overall_score for e in behavioral_evals) / len(behavioral_evals)
        
        # Identify strengths and weaknesses
        all_strengths = [s.category for e in evaluations for s in e.strengths]
        all_weaknesses = [w.category for e in evaluations for w in e.weaknesses]
        
        strongest_areas = self._get_most_common(all_strengths, 3)
        weakest_areas = self._get_most_common(all_weaknesses, 3)
        
        # Calculate consistency
        scores = [e.overall_score for e in evaluations]
        consistency_score = self._calculate_consistency(scores)
        
        # Determine hiring recommendation
        hiring_rec, hiring_just = self._determine_hiring_recommendation(
            average_score,
            consistency_score,
            evaluations
        )
        
        # Generate overall feedback
        overall_feedback = self._generate_overall_feedback(
            average_score,
            strongest_areas,
            weakest_areas,
            technical_score,
            behavioral_score
        )
        
        # Collect key insights
        key_strengths = []
        areas_for_improvement = []
        
        for eval in evaluations:
            high_priority = eval.get_high_priority_feedback()
            key_strengths.extend([s.message for s in high_priority["strengths"][:1]])
            areas_for_improvement.extend([w.message for w in high_priority["weaknesses"][:1]])
        
        # Remove duplicates and limit
        key_strengths = list(dict.fromkeys(key_strengths))[:5]
        areas_for_improvement = list(dict.fromkeys(areas_for_improvement))[:5]
        
        return SessionSummary(
            session_id=session_id,
            total_questions=total_questions,
            questions_answered=total_questions,
            average_score=round(average_score, 2),
            score_level=self._score_to_level(average_score),
            score_distribution=score_distribution,
            technical_score=round(technical_score, 2) if technical_score else None,
            behavioral_score=round(behavioral_score, 2) if behavioral_score else None,
            strongest_areas=strongest_areas,
            weakest_areas=weakest_areas,
            consistency_score=round(consistency_score, 2),
            overall_feedback=overall_feedback,
            key_strengths=key_strengths,
            areas_for_improvement=areas_for_improvement,
            hiring_recommendation=hiring_rec,
            hiring_justification=hiring_just
        )
    
    def _build_evaluation_prompt(self, request: EvaluationRequest) -> str:
        """Build prompt for LLM evaluation"""
        
        criteria_desc = "\n".join([
            f"- {c}: {self.criteria_definitions.get(EvaluationCriteria(c), {}).get('description', '')}"
            for c in request.evaluation_criteria
        ])
        
        expected_points_section = ""
        if request.expected_answer_points:
            expected_points_section = f"""
Expected Key Points:
{chr(10).join(f"- {point}" for point in request.expected_answer_points)}
"""
        
        prompt = f"""Evaluate this interview answer comprehensively.

Question Type: {request.question_type}
Difficulty: {request.difficulty_level}
{f"Target Role: {request.job_role}" if request.job_role else ""}
{f"Experience Level: {request.experience_level}" if request.experience_level else ""}

Question:
{request.question}

Candidate's Answer:
{request.answer}

{expected_points_section}

Evaluation Criteria:
{criteria_desc}

Provide a JSON evaluation with:
1. overall_score: Overall score out of 100
2. criterion_scores: Array of scores for each criterion with feedback
3. strengths: Array of strength feedback items
4. weaknesses: Array of weakness feedback items
5. suggestions: Array of actionable improvement suggestions
6. summary: Brief 2-3 sentence summary
7. key_takeaways: Array of key points from the evaluation
8. missing_points: Points from expected answer that were missed
9. extra_points: Additional good points mentioned

Format:
{{
  "overall_score": 75,
  "criterion_scores": [
    {{
      "criterion": "technical_accuracy",
      "score": 80,
      "feedback": "Good technical understanding..."
    }}
  ],
  "strengths": [
    {{
      "type": "strength",
      "category": "technical_accuracy",
      "message": "Clear explanation of concepts",
      "priority": "high"
    }}
  ],
  "weaknesses": [
    {{
      "type": "weakness",
      "category": "completeness",
      "message": "Missing discussion of edge cases",
      "priority": "high"
    }}
  ],
  "suggestions": [
    {{
      "type": "suggestion",
      "category": "structure",
      "message": "Consider using STAR format",
      "priority": "medium",
      "examples": ["Situation: ...", "Task: ..."]
    }}
  ],
  "summary": "Good answer demonstrating solid understanding...",
  "key_takeaways": ["Strong technical knowledge", "Could improve structure"],
  "missing_points": ["Discussion of time complexity"],
  "extra_points": ["Mentioned real-world applications"]
}}

Be constructive, specific, and actionable in your feedback."""
        
        return prompt
    
    def _parse_llm_evaluation(
        self,
        llm_response: Dict[str, Any],
        request: EvaluationRequest,
        eval_id: str,
        question_id: str
    ) -> AnswerEvaluation:
        """Parse LLM response into AnswerEvaluation"""
        
        overall_score = llm_response.get("overall_score", 50)
        
        # Parse criterion scores
        criterion_scores = []
        for cs in llm_response.get("criterion_scores", []):
            try:
                criterion_scores.append(
                    CriterionScore(
                        criterion=EvaluationCriteria(cs["criterion"]),
                        score=cs["score"],
                        feedback=cs.get("feedback"),
                        weight=self.criteria_definitions.get(
                            EvaluationCriteria(cs["criterion"]),
                            {}
                        ).get("weight", 1.0)
                    )
                )
            except Exception as e:
                print(f"Error parsing criterion score: {e}")
                continue
        
        # Parse feedback items
        strengths = []
        for s in llm_response.get("strengths", []):
            try:
                strengths.append(FeedbackItem(**s))
            except:
                strengths.append(
                    FeedbackItem(
                        type=FeedbackType.STRENGTH,
                        category=s.get("category", "general"),
                        message=s.get("message", ""),
                        priority=s.get("priority", "medium")
                    )
                )
        
        weaknesses = []
        for w in llm_response.get("weaknesses", []):
            try:
                weaknesses.append(FeedbackItem(**w))
            except:
                weaknesses.append(
                    FeedbackItem(
                        type=FeedbackType.WEAKNESS,
                        category=w.get("category", "general"),
                        message=w.get("message", ""),
                        priority=w.get("priority", "high")
                    )
                )
        
        suggestions = []
        for sug in llm_response.get("suggestions", []):
            try:
                suggestions.append(FeedbackItem(**sug))
            except:
                suggestions.append(
                    FeedbackItem(
                        type=FeedbackType.SUGGESTION,
                        category=sug.get("category", "general"),
                        message=sug.get("message", ""),
                        priority=sug.get("priority", "medium"),
                        examples=sug.get("examples", [])
                    )
                )
        
        evaluation = AnswerEvaluation(
            evaluation_id=eval_id,
            question_id=question_id,
            session_id=request.session_id,
            answer_text=request.answer,
            question_text=request.question,
            question_type=request.question_type,
            overall_score=overall_score,
            score_level=self._score_to_level(overall_score),
            criterion_scores=criterion_scores,
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions,
            summary=llm_response.get("summary"),
            key_takeaways=llm_response.get("key_takeaways", []),
            improvement_areas=llm_response.get("improvement_areas", []),
            expected_answer_points=request.expected_answer_points,
            missing_points=llm_response.get("missing_points", []),
            extra_points=llm_response.get("extra_points", [])
        )
        
        return evaluation
    
    def _fallback_evaluation(
        self,
        request: EvaluationRequest,
        eval_id: str,
        question_id: str
    ) -> AnswerEvaluation:
        """Fallback rule-based evaluation when LLM fails"""
        
        answer = request.answer.strip()
        
        # Basic scoring heuristics
        base_score = 50
        
        # Length check
        word_count = len(answer.split())
        if word_count < 20:
            base_score -= 20
        elif word_count > 100:
            base_score += 10
        
        # Check for expected points
        expected_found = 0
        for point in request.expected_answer_points:
            if any(word.lower() in answer.lower() for word in point.split()[:3]):
                expected_found += 1
        
        if request.expected_answer_points:
            coverage = expected_found / len(request.expected_answer_points)
            base_score += coverage * 30
        
        # Check for examples
        if any(marker in answer.lower() for marker in ["for example", "such as", "like", "e.g."]):
            base_score += 5
        
        # Check for structure
        if answer.count('\n') >= 2 or answer.count('.') >= 3:
            base_score += 5
        
        # Cap at 100
        overall_score = min(100, max(0, base_score))
        
        # Generate criterion scores
        criterion_scores = self._calculate_criterion_scores(
            overall_score,
            request.evaluation_criteria
        )
        
        # Generate basic feedback lists
        strengths = []
        weaknesses = []
        suggestions = []
        
        # Add basic feedback
        if word_count < 30:
            weaknesses.append(
                FeedbackItem(
                    type=FeedbackType.WEAKNESS,
                    category="completeness",
                    message="Answer could be more detailed",
                    priority="high"
                )
            )
        else:
            strengths.append(
                FeedbackItem(
                    type=FeedbackType.STRENGTH,
                    category="depth",
                    message="Provided adequate explanation length",
                    priority="medium"
                )
            )
        
        if request.expected_answer_points:
            if expected_found < len(request.expected_answer_points) / 2:
                weaknesses.append(
                    FeedbackItem(
                        type=FeedbackType.WEAKNESS,
                        category="technical_accuracy",
                        message="Missing several key concepts from expected answer",
                        priority="high"
                    )
                )
            else:
                strengths.append(
                    FeedbackItem(
                        type=FeedbackType.STRENGTH,
                        category="technical_accuracy",
                        message="Covered most key concepts",
                        priority="high"
                    )
                )
        
        # Add suggestions for improvement
        if overall_score < 70:
            suggestions.append(
                FeedbackItem(
                    type=FeedbackType.SUGGESTION,
                    category="improvement",
                    message="Provide more detailed explanations with examples",
                    priority="high",
                    examples=["Add real-world use cases", "Include specific examples"]
                )
            )
        
        evaluation = AnswerEvaluation(
            evaluation_id=eval_id,
            question_id=question_id,
            session_id=request.session_id,
            answer_text=request.answer,
            question_text=request.question,
            question_type=request.question_type,
            overall_score=overall_score,
            score_level=self._score_to_level(overall_score),
            criterion_scores=criterion_scores,
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions,
            summary=f"Answer demonstrates {'good' if overall_score >= 70 else 'fair'} understanding. Score based on length, coverage of key points, and structure."
        )
        
        return evaluation
    
    def _calculate_criterion_scores(
        self,
        overall_score: float,
        criteria: List[str]
    ) -> List[CriterionScore]:
        """Calculate individual criterion scores based on overall score"""
        
        scores = []
        for criterion_name in criteria:
            try:
                criterion = EvaluationCriteria(criterion_name)
                definition = self.criteria_definitions.get(criterion, {})
                
                # Add some variance (+/- 10%)
                import random
                variance = random.uniform(-10, 10)
                score = max(0, min(100, overall_score + variance))
                
                scores.append(
                    CriterionScore(
                        criterion=criterion,
                        score=score,
                        weight=definition.get("weight", 1.0),
                        feedback=f"{definition.get('description', 'Evaluation')} score"
                    )
                )
            except:
                continue
        
        return scores
    
    def _score_to_level(self, score: float) -> ScoreLevel:
        """Convert numeric score to score level"""
        if score >= 90:
            return ScoreLevel.EXCELLENT
        elif score >= 70:
            return ScoreLevel.GOOD
        elif score >= 50:
            return ScoreLevel.FAIR
        else:
            return ScoreLevel.POOR
    
    def _get_most_common(self, items: List[str], n: int) -> List[str]:
        """Get n most common items from list"""
        from collections import Counter
        counter = Counter(items)
        return [item for item, count in counter.most_common(n)]
    
    def _calculate_consistency(self, scores: List[float]) -> float:
        """Calculate consistency score (lower variance = higher consistency)"""
        if len(scores) < 2:
            return 100.0
        
        import statistics
        mean = statistics.mean(scores)
        stdev = statistics.stdev(scores)
        
        # Normalize: lower stdev = higher consistency
        # Max stdev could be ~40 (e.g., scores ranging 0-100)
        consistency = max(0, 100 - (stdev / 40 * 100))
        return consistency
    
    def _determine_hiring_recommendation(
        self,
        average_score: float,
        consistency_score: float,
        evaluations: List[AnswerEvaluation]
    ) -> Tuple[str, str]:
        """Determine hiring recommendation"""
        
        if average_score >= 85 and consistency_score >= 70:
            return "strong_yes", "Consistently excellent performance across all questions"
        elif average_score >= 75 and consistency_score >= 60:
            return "yes", "Strong performance with good consistency"
        elif average_score >= 60:
            return "maybe", "Adequate performance but with areas needing improvement"
        else:
            return "no", "Performance below expected standards for the role"
    
    def _generate_overall_feedback(
        self,
        average_score: float,
        strongest_areas: List[str],
        weakest_areas: List[str],
        technical_score: Optional[float],
        behavioral_score: Optional[float]
    ) -> str:
        """Generate overall feedback text"""
        
        level = self._score_to_level(average_score)
        
        feedback_parts = []
        
        # Overall performance
        if level == ScoreLevel.EXCELLENT:
            feedback_parts.append("Outstanding interview performance demonstrating strong expertise.")
        elif level == ScoreLevel.GOOD:
            feedback_parts.append("Good interview performance with solid understanding.")
        elif level == ScoreLevel.FAIR:
            feedback_parts.append("Fair performance with room for improvement.")
        else:
            feedback_parts.append("Performance needs significant improvement.")
        
        # Strongest areas
        if strongest_areas:
            feedback_parts.append(
                f"Particularly strong in: {', '.join(strongest_areas[:2])}."
            )
        
        # Areas for improvement
        if weakest_areas:
            feedback_parts.append(
                f"Focus on improving: {', '.join(weakest_areas[:2])}."
            )
        
        # Score breakdown
        if technical_score and behavioral_score:
            feedback_parts.append(
                f"Technical: {technical_score:.0f}/100, Behavioral: {behavioral_score:.0f}/100."
            )
        
        return " ".join(feedback_parts)
    
    def _generate_evaluation_id(self) -> str:
        """Generate unique evaluation ID"""
        return f"eval_{uuid.uuid4().hex[:12]}"
    
    def compare_answers(
        self,
        answer1: AnswerEvaluation,
        answer2: AnswerEvaluation
    ) -> Dict[str, Any]:
        """Compare two answer evaluations"""
        
        score_diff = answer1.overall_score - answer2.overall_score
        
        comparison = {
            "answer1_id": answer1.evaluation_id,
            "answer2_id": answer2.evaluation_id,
            "score_difference": round(score_diff, 2),
            "better_answer": answer1.evaluation_id if score_diff > 0 else answer2.evaluation_id,
            "score_improvement_percentage": round(abs(score_diff) / max(answer1.overall_score, answer2.overall_score) * 100, 2) if max(answer1.overall_score, answer2.overall_score) > 0 else 0,
            "level_change": answer1.score_level != answer2.score_level,
            "common_strengths": list(set([s.category for s in answer1.strengths]) & set([s.category for s in answer2.strengths])),
            "common_weaknesses": list(set([w.category for w in answer1.weaknesses]) & set([w.category for w in answer2.weaknesses]))
        }
        
        return comparison
