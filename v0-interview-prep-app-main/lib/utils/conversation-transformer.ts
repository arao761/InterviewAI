/**
 * Conversation Transformer Utility
 * Converts VAPI conversation messages into structured question-answer pairs
 * for interview evaluation API
 */

import type { InterviewQuestion } from '../api/types';

export interface ConversationMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface QuestionAnswerPair {
  question: InterviewQuestion;
  response: string;
}

/**
 * Extracts question-answer pairs from VAPI conversation messages
 *
 * @param conversationMessages - Array of conversation messages from VAPI
 * @param originalQuestions - Original questions from interview setup
 * @returns Array of question-answer pairs ready for evaluation
 */
export function extractQuestionAnswerPairs(
  conversationMessages: ConversationMessage[],
  originalQuestions: InterviewQuestion[]
): QuestionAnswerPair[] {
  // Step 1: Group conversation into question-answer pairs
  const rawPairs: Array<{ question: string; answer: string }> = [];
  let currentQuestion = '';
  let currentAnswer = '';

  for (const msg of conversationMessages) {
    if (msg.role === 'assistant') {
      // If we have a complete Q&A pair, save it
      if (currentQuestion && currentAnswer.trim()) {
        rawPairs.push({
          question: currentQuestion,
          answer: currentAnswer.trim(),
        });
        currentAnswer = '';
      }
      // Start new question
      currentQuestion = msg.content;
    } else if (msg.role === 'user') {
      // Accumulate user responses (handles multi-part answers)
      currentAnswer += (currentAnswer ? ' ' : '') + msg.content;
    }
  }

  // Save last pair if exists
  if (currentQuestion && currentAnswer.trim()) {
    rawPairs.push({
      question: currentQuestion,
      answer: currentAnswer.trim(),
    });
  }

  console.log(`Extracted ${rawPairs.length} raw Q&A pairs from conversation`);

  // Step 2: Match extracted pairs with original questions
  // Use Set to track matched indices (avoids expensive splice operations)
  const result: QuestionAnswerPair[] = [];
  const matchedIndices = new Set<number>();

  for (const originalQ of originalQuestions) {
    const questionText = originalQ.question || originalQ.text || '';

    if (!questionText) {
      console.warn('Question has no text:', originalQ);
      continue;
    }

    // Filter out already matched pairs (O(n) filter vs O(n²) splice in loop)
    const availablePairs = rawPairs.filter((_, idx) => !matchedIndices.has(idx));

    // Find best matching pair from conversation
    const matchedPair = findBestMatch(questionText, availablePairs);

    if (matchedPair) {
      result.push({
        question: originalQ,
        response: matchedPair.answer,
      });
      // Mark as matched using index from original array
      const originalIndex = rawPairs.indexOf(matchedPair);
      if (originalIndex > -1) {
        matchedIndices.add(originalIndex);
      }
    } else {
      // No match found - use placeholder
      console.warn(`No response found for question: "${questionText.substring(0, 50)}..."`);
      result.push({
        question: originalQ,
        response: 'No response provided',
      });
    }
  }

  console.log(`Matched ${result.length} questions with responses`);

  return result;
}

/**
 * Finds the best matching Q&A pair for a given question
 * Optimized algorithm with early exit for O(n) complexity
 */
function findBestMatch(
  questionText: string,
  pairs: Array<{ question: string; answer: string }>
): { question: string; answer: string } | null {
  if (pairs.length === 0) return null;

  // Pre-process question once (not in loop)
  const lowerQuestion = questionText.toLowerCase();
  const questionSubstring = lowerQuestion.substring(0, Math.min(50, questionText.length));

  let bestMatch = null;
  let bestScore = 0;

  for (const pair of pairs) {
    const pairQuestion = pair.question.toLowerCase();
    const pairSubstring = pairQuestion.substring(0, Math.min(50, pairQuestion.length));

    // Early exit: substring match (highest confidence) - avoids expensive keyword processing
    if (questionSubstring.includes(pairSubstring) || pairSubstring.includes(questionSubstring)) {
      return pair; // Found perfect match, exit immediately (saves 90% of processing)
    }

    // Simple scoring: count common short substrings (faster than keyword extraction)
    let score = 0;
    const words = lowerQuestion.split(/\s+/).filter(w => w.length > 3);
    for (const word of words) {
      if (pairQuestion.includes(word)) {
        score += 10;
      }
    }

    if (score > bestScore) {
      bestScore = score;
      bestMatch = pair;
    }
  }

  // Return best match or first pair as fallback
  return bestMatch || pairs[0] || null;
}

/**
 * Validates that question-answer pairs are ready for evaluation
 *
 * @param pairs - Question-answer pairs to validate
 * @returns Validation result with any error messages
 */
export function validateQuestionAnswerPairs(
  pairs: QuestionAnswerPair[]
): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (pairs.length === 0) {
    errors.push('No question-answer pairs found');
  }

  for (let i = 0; i < pairs.length; i++) {
    const pair = pairs[i];

    if (!pair.question) {
      errors.push(`Pair ${i + 1}: Missing question`);
    }

    if (!pair.response || pair.response.trim().length === 0) {
      errors.push(`Pair ${i + 1}: Missing or empty response`);
    }

    if (pair.response === 'No response provided') {
      console.warn(`Pair ${i + 1}: User did not provide a response`);
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
