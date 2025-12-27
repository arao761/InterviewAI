'use client';

import { Badge } from '@/components/ui/badge';
import { Lightbulb } from 'lucide-react';
import { useState } from 'react';

interface DSAProblem {
  title: string;
  problem_statement: string;
  examples: Array<{
    input: string;
    output: string;
    explanation?: string;
  }>;
  constraints: string[];
  function_signatures?: {
    python?: string;
    javascript?: string;
    java?: string;
    cpp?: string;
  };
  hints?: string[];
  expected_complexity?: {
    time?: string;
    space?: string;
  };
  difficulty: string;
  topic: string;
}

interface DSAProblemDisplayProps {
  problem: DSAProblem;
  questionNumber: number;
  totalQuestions: number;
}

export default function DSAProblemDisplay({
  problem,
  questionNumber,
  totalQuestions,
}: DSAProblemDisplayProps) {
  const [showHints, setShowHints] = useState(false);

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy':
        return 'bg-green-500/20 text-green-500 border-green-500/30';
      case 'medium':
        return 'bg-yellow-500/20 text-yellow-500 border-yellow-500/30';
      case 'hard':
        return 'bg-red-500/20 text-red-500 border-red-500/30';
      default:
        return 'bg-blue-500/20 text-blue-500 border-blue-500/30';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header - LeetCode style */}
      <div className="flex items-center gap-3 mb-6">
        <h1 className="text-2xl font-semibold">{questionNumber}. {problem.title}</h1>
        <Badge className={getDifficultyColor(problem.difficulty)}>
          {problem.difficulty.charAt(0).toUpperCase() + problem.difficulty.slice(1)}
        </Badge>
      </div>

      {/* Problem Statement - LeetCode style */}
      <div className="mb-6">
        <p className="text-foreground leading-relaxed whitespace-pre-wrap">
          {problem.problem_statement}
        </p>
      </div>

      {/* Examples - LeetCode style */}
      {problem.examples && problem.examples.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-3">Example {problem.examples.length > 1 ? '1' : ''}:</h3>
          {problem.examples.map((example, idx) => (
            <div key={idx} className="mb-4">
              <div className="space-y-2 mb-2">
                <div>
                  <strong>Input:</strong> <code className="bg-muted px-2 py-1 rounded text-sm">{example.input}</code>
                </div>
                <div>
                  <strong>Output:</strong> <code className="bg-muted px-2 py-1 rounded text-sm">{example.output}</code>
                </div>
                {example.explanation && (
                  <div>
                    <strong>Explanation:</strong> <span className="text-foreground">{example.explanation}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Constraints - LeetCode style */}
      {problem.constraints && problem.constraints.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-3">Constraints:</h3>
          <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
            {problem.constraints.map((constraint, idx) => (
              <li key={idx}>
                <code className="text-foreground">{constraint}</code>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Follow-up (if complexity info available) */}
      {problem.expected_complexity && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-3">Follow-up:</h3>
          <p className="text-sm text-muted-foreground">
            Can you come up with an algorithm that is less than <code className="bg-muted px-1 rounded">O(n²)</code> time complexity?
          </p>
          {problem.expected_complexity.time && problem.expected_complexity.space && (
            <p className="text-sm text-muted-foreground mt-2">
              <strong>Expected:</strong> Time: <code>{problem.expected_complexity.time}</code>, Space: <code>{problem.expected_complexity.space}</code>
            </p>
          )}
        </div>
      )}

      {/* Function Signatures - Compact */}
      {problem.function_signatures && (
        <div className="mb-6 p-4 bg-muted/30 rounded-lg border border-border">
          <h3 className="text-sm font-semibold mb-3 text-muted-foreground">Function Signature:</h3>
          <div className="space-y-2">
            {problem.function_signatures.javascript && (
              <code className="text-sm bg-background px-3 py-2 rounded block font-mono">
                {problem.function_signatures.javascript}
              </code>
            )}
            {problem.function_signatures.python && !problem.function_signatures.javascript && (
              <code className="text-sm bg-background px-3 py-2 rounded block font-mono">
                {problem.function_signatures.python}
              </code>
            )}
          </div>
        </div>
      )}

      {/* Hints - Compact */}
      {problem.hints && problem.hints.length > 0 && (
        <div className="mb-6">
          <button
            onClick={() => setShowHints(!showHints)}
            className="flex items-center gap-2 text-sm text-primary hover:underline mb-2"
          >
            <Lightbulb className="w-4 h-4" />
            {showHints ? 'Hide' : 'Show'} Hints
          </button>
          {showHints && (
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-4">
              {problem.hints.map((hint, idx) => (
                <li key={idx}>{hint}</li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

