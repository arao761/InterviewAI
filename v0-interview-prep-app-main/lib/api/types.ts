/**
 * API Types and Interfaces for PrepWise Backend Integration
 */

// Interview Types
export type InterviewType = 'behavioral' | 'technical' | 'both' | 'mixed';
export type TechnicalDomain = 'algorithms' | 'web_development' | 'machine_learning' | 'system_design' | 'database' | 'devops';

// Resume Data
export interface ParsedResume {
  name: string;
  email?: string;
  phone?: string;
  summary?: string;
  skills: string[];
  experience: Array<{
    title: string;
    company: string;
    duration?: string;
    responsibilities?: string[];
  }>;
  education: Array<{
    degree: string;
    institution: string;
    year?: string;
  }>;
}

// Question Types
export interface InterviewQuestion {
  id: string;
  type: string;
  question: string;
  text?: string;
  difficulty?: string;
  focus_area?: string;
  expected_points?: string[];
}

// Request Types
export interface QuestionGenerationRequest {
  resume_data: ParsedResume | Record<string, any>;
  interview_type: InterviewType;
  domain?: TechnicalDomain;
  num_questions: number;
}

export interface ResponseEvaluationRequest {
  question: InterviewQuestion | Record<string, any>;
  transcript: string;
  question_type?: string;
}

export interface InterviewEvaluationRequest {
  questions_and_responses: Array<{
    question: InterviewQuestion | Record<string, any>;
    response: string;
  }>;
  interview_type: InterviewType;
}

// Response Types
export interface ResumeParseResponse {
  success: boolean;
  data: ParsedResume;
  message?: string;
}

export interface QuestionGenerationResponse {
  success: boolean;
  questions: InterviewQuestion[];
  count: number;
  message?: string;
}

export interface ResponseEvaluation {
  score: number;
  score_level?: string;
  strengths: string[];
  weaknesses: string[];
  feedback: string;
  suggestions: string[];
  criterion_scores?: any[];
  key_takeaways?: string[];
  improvement_areas?: string[];
}

export interface ResponseEvaluationResponse {
  success: boolean;
  evaluation: ResponseEvaluation;
  message?: string;
}

export interface InterviewEvaluationReport {
  overall_score: number;
  technical_score?: number;
  behavioral_score?: number;
  question_scores: number[];
  total_questions: number;
  strengths: string[];
  areas_for_improvement: string[];
  detailed_feedback: string;
  recommendations: string[];
  individual_evaluations: ResponseEvaluation[];
}

export interface InterviewEvaluationResponse {
  success: boolean;
  report: InterviewEvaluationReport;
  message?: string;
}

// Error Response
export interface ErrorResponse {
  success: false;
  error: string;
  detail?: string;
}

// API Response
export type APIResponse<T> = T | ErrorResponse;
