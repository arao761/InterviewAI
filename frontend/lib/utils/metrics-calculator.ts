/**
 * Metrics Calculator Utility
 * Derives performance metrics (clarity, confidence, structure, technical accuracy, engagement)
 * from interview evaluation data
 */

import type { InterviewEvaluationReport, ResponseEvaluation } from '../api/types';

export interface PerformanceMetrics {
  clarity: number;
  confidence: number;
  structure: number;
  technicalAccuracy: number;
  engagement: number;
}

/**
 * Keywords for metric calculation
 * Positive keywords increase the metric, negative keywords decrease it
 */
const METRIC_KEYWORDS = {
  clarity: {
    positive: [
      'clear', 'articulate', 'concise', 'specific', 'precise', 'direct',
      'well-explained', 'understandable', 'coherent', 'focused', 'straightforward'
    ],
    negative: [
      'vague', 'unclear', 'confusing', 'rambling', 'ambiguous', 'muddled',
      'unfocused', 'disorganized', 'convoluted', 'verbose'
    ]
  },
  confidence: {
    positive: [
      'confident', 'decisive', 'assertive', 'self-assured', 'certain',
      'strong', 'poised', 'firm', 'convincing', 'assured'
    ],
    negative: [
      'hesitant', 'uncertain', 'tentative', 'unsure', 'lacking confidence',
      'timid', 'wavering', 'doubtful', 'indecisive'
    ]
  },
  structure: {
    positive: [
      'structured', 'organized', 'logical', 'methodical', 'systematic',
      'STAR method', 'step-by-step', 'well-organized', 'coherent flow',
      'clear structure', 'sequential', 'framework'
    ],
    negative: [
      'unstructured', 'disorganized', 'scattered', 'chaotic', 'random',
      'lacking structure', 'all over the place', 'incoherent', 'jumbled'
    ]
  },
  engagement: {
    positive: [
      'engaging', 'enthusiastic', 'passionate', 'energetic', 'animated',
      'interested', 'active', 'involved', 'compelling', 'dynamic'
    ],
    negative: [
      'disengaged', 'monotone', 'flat', 'boring', 'unenthusiastic',
      'passive', 'detached', 'indifferent', 'lifeless'
    ]
  }
};

/**
 * Calculates performance metrics from interview evaluation report
 *
 * @param evaluation - Complete interview evaluation report
 * @returns Performance metrics object with scores 0-100
 */
export function calculatePerformanceMetrics(
  evaluation: InterviewEvaluationReport
): PerformanceMetrics {
  const individualEvals = evaluation.individual_evaluations || [];

  // Calculate each metric
  const clarity = calculateMetricFromFeedback(
    individualEvals,
    METRIC_KEYWORDS.clarity,
    evaluation.overall_score
  );

  const confidence = calculateMetricFromFeedback(
    individualEvals,
    METRIC_KEYWORDS.confidence,
    evaluation.overall_score
  );

  const structure = calculateMetricFromFeedback(
    individualEvals,
    METRIC_KEYWORDS.structure,
    evaluation.overall_score
  );

  // Technical accuracy uses the technical_score directly
  const technicalAccuracy = evaluation.technical_score || evaluation.overall_score;

  // Engagement uses behavioral_score or calculated metric
  const engagement = evaluation.behavioral_score ||
    calculateMetricFromFeedback(
      individualEvals,
      METRIC_KEYWORDS.engagement,
      evaluation.overall_score
    );

  return {
    clarity: Math.round(Math.min(100, Math.max(0, clarity))),
    confidence: Math.round(Math.min(100, Math.max(0, confidence))),
    structure: Math.round(Math.min(100, Math.max(0, structure))),
    technicalAccuracy: Math.round(Math.min(100, Math.max(0, technicalAccuracy))),
    engagement: Math.round(Math.min(100, Math.max(0, engagement))),
  };
}

/**
 * Calculates a specific metric from individual evaluations using keyword analysis
 */
function calculateMetricFromFeedback(
  evaluations: ResponseEvaluation[],
  keywords: { positive: string[]; negative: string[] },
  baseScore: number
): number {
  if (evaluations.length === 0) {
    return baseScore;
  }

  let totalScore = 0;
  let count = 0;

  for (const evaluation of evaluations) {
    // Combine all feedback text
    const feedbackText = [
      evaluation.feedback,
      ...evaluation.strengths,
      ...evaluation.weaknesses,
      ...(evaluation.suggestions || []),
      ...(evaluation.key_takeaways || [])
    ].join(' ').toLowerCase();

    // Count keyword occurrences
    let positiveCount = 0;
    let negativeCount = 0;

    for (const keyword of keywords.positive) {
      if (feedbackText.includes(keyword.toLowerCase())) {
        positiveCount++;
      }
    }

    for (const keyword of keywords.negative) {
      if (feedbackText.includes(keyword.toLowerCase())) {
        negativeCount++;
      }
    }

    // Calculate score for this evaluation
    // Start with the evaluation score, adjust based on keyword sentiment
    let score = evaluation.score;

    // Adjust based on keyword ratio
    const keywordDelta = (positiveCount - negativeCount) * 2;
    score = score + keywordDelta;

    totalScore += score;
    count++;
  }

  // Return average if we have evaluations, otherwise use base score
  return count > 0 ? totalScore / count : baseScore;
}

/**
 * Alternative simple metrics calculation (fallback)
 * Uses score-based approximations when keyword analysis is insufficient
 */
export function calculateSimpleMetrics(
  evaluation: InterviewEvaluationReport
): PerformanceMetrics {
  const baseScore = evaluation.overall_score;
  const techScore = evaluation.technical_score || baseScore;
  const behavScore = evaluation.behavioral_score || baseScore;

  // Calculate strengths/weaknesses ratio
  const strengthCount = evaluation.strengths?.length || 0;
  const weaknessCount = evaluation.areas_for_improvement?.length || 0;
  const balanceBonus = Math.min(5, (strengthCount - weaknessCount) * 1);

  return {
    clarity: Math.round(Math.min(100, baseScore + balanceBonus)),
    confidence: Math.round(Math.min(100, baseScore + (behavScore - baseScore) * 0.5)),
    structure: Math.round(Math.min(100, baseScore * 0.95)),
    technicalAccuracy: Math.round(Math.min(100, techScore)),
    engagement: Math.round(Math.min(100, behavScore)),
  };
}

/**
 * Gets a performance level description based on score
 */
export function getPerformanceLevel(score: number): string {
  if (score >= 90) return 'Excellent';
  if (score >= 80) return 'Good';
  if (score >= 70) return 'Fair';
  return 'Needs Improvement';
}

/**
 * Gets a color class for performance visualization based on score
 */
export function getPerformanceColor(score: number): string {
  if (score >= 90) return 'text-green-500';
  if (score >= 80) return 'text-blue-500';
  if (score >= 70) return 'text-yellow-500';
  return 'text-red-500';
}
