'use client';

import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Lightbulb, Code, Clock } from 'lucide-react';
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
    <div className="max-w-4xl space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <span className="text-sm font-semibold text-primary">
            Question {questionNumber} of {totalQuestions}
          </span>
          <div className="flex items-center gap-3 mt-2">
            <h2 className="text-2xl font-bold">{problem.title}</h2>
            <Badge className={getDifficultyColor(problem.difficulty)}>
              {problem.difficulty.toUpperCase()}
            </Badge>
            <Badge variant="outline" className="border-border">
              {problem.topic}
            </Badge>
          </div>
        </div>
        {problem.expected_complexity && (
          <div className="text-right text-sm text-muted-foreground">
            <div className="flex items-center gap-4">
              {problem.expected_complexity.time && (
                <div>
                  <span className="font-semibold">Time:</span> {problem.expected_complexity.time}
                </div>
              )}
              {problem.expected_complexity.space && (
                <div>
                  <span className="font-semibold">Space:</span> {problem.expected_complexity.space}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Problem Statement */}
      <Card className="bg-card border-border p-6">
        <div className="flex gap-4">
          <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
            <Code className="w-5 h-5 text-primary" />
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold mb-3">Problem Statement</h3>
            <p className="text-foreground whitespace-pre-wrap leading-relaxed">
              {problem.problem_statement}
            </p>
          </div>
        </div>
      </Card>

      {/* Examples */}
      {problem.examples && problem.examples.length > 0 && (
        <Card className="bg-card border-border p-6">
          <h3 className="text-lg font-semibold mb-4">Examples</h3>
          <div className="space-y-4">
            {problem.examples.map((example, idx) => (
              <div key={idx} className="bg-muted/50 rounded-lg p-4 border border-border">
                <div className="space-y-2">
                  <div>
                    <span className="text-sm font-semibold text-muted-foreground">Input: </span>
                    <code className="text-sm bg-background px-2 py-1 rounded">
                      {example.input}
                    </code>
                  </div>
                  <div>
                    <span className="text-sm font-semibold text-muted-foreground">Output: </span>
                    <code className="text-sm bg-background px-2 py-1 rounded">
                      {example.output}
                    </code>
                  </div>
                  {example.explanation && (
                    <div className="mt-2">
                      <span className="text-sm font-semibold text-muted-foreground">Explanation: </span>
                      <span className="text-sm text-foreground">{example.explanation}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Constraints */}
      {problem.constraints && problem.constraints.length > 0 && (
        <Card className="bg-card border-border p-6">
          <h3 className="text-lg font-semibold mb-4">Constraints</h3>
          <ul className="list-disc list-inside space-y-2 text-sm">
            {problem.constraints.map((constraint, idx) => (
              <li key={idx} className="text-muted-foreground">
                {constraint}
              </li>
            ))}
          </ul>
        </Card>
      )}

      {/* Function Signatures */}
      {problem.function_signatures && (
        <Card className="bg-card border-border p-6">
          <h3 className="text-lg font-semibold mb-4">Function Signatures</h3>
          <div className="space-y-3">
            {problem.function_signatures.python && (
              <div>
                <span className="text-sm font-semibold text-muted-foreground">Python: </span>
                <code className="text-sm bg-muted px-2 py-1 rounded block mt-1">
                  {problem.function_signatures.python}
                </code>
              </div>
            )}
            {problem.function_signatures.javascript && (
              <div>
                <span className="text-sm font-semibold text-muted-foreground">JavaScript: </span>
                <code className="text-sm bg-muted px-2 py-1 rounded block mt-1">
                  {problem.function_signatures.javascript}
                </code>
              </div>
            )}
            {problem.function_signatures.java && (
              <div>
                <span className="text-sm font-semibold text-muted-foreground">Java: </span>
                <code className="text-sm bg-muted px-2 py-1 rounded block mt-1">
                  {problem.function_signatures.java}
                </code>
              </div>
            )}
            {problem.function_signatures.cpp && (
              <div>
                <span className="text-sm font-semibold text-muted-foreground">C++: </span>
                <code className="text-sm bg-muted px-2 py-1 rounded block mt-1">
                  {problem.function_signatures.cpp}
                </code>
              </div>
            )}
          </div>
        </Card>
      )}

      {/* Hints */}
      {problem.hints && problem.hints.length > 0 && (
        <Card className="bg-card border-border p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <Lightbulb className="w-5 h-5 text-primary" />
              Hints
            </h3>
            <button
              onClick={() => setShowHints(!showHints)}
              className="text-sm text-primary hover:underline"
            >
              {showHints ? 'Hide' : 'Show'} Hints
            </button>
          </div>
          {showHints && (
            <ul className="list-disc list-inside space-y-2 text-sm">
              {problem.hints.map((hint, idx) => (
                <li key={idx} className="text-muted-foreground">
                  {hint}
                </li>
              ))}
            </ul>
          )}
        </Card>
      )}
    </div>
  );
}

