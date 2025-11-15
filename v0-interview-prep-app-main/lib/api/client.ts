/**
 * API Client for PrepWise Backend
 * Handles all communication with the FastAPI backend
 */

import {
  ParsedResume,
  QuestionGenerationRequest,
  QuestionGenerationResponse,
  ResumeParseResponse,
  ResponseEvaluationRequest,
  ResponseEvaluationResponse,
  InterviewEvaluationRequest,
  InterviewEvaluationResponse,
  APIResponse,
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class PrepWiseAPIClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  /**
   * Generic fetch wrapper with error handling
   */
  private async fetch<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<APIResponse<T>> {
    try {
      const url = `${this.baseURL}${endpoint}`;
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({
          error: 'Request failed',
          detail: response.statusText,
        }));
        return {
          success: false,
          error: error.detail || error.error || 'Unknown error',
          detail: error.detail,
        };
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  }

  /**
   * Upload and parse resume
   */
  async parseResume(file: File): Promise<APIResponse<ResumeParseResponse>> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const url = `${this.baseURL}/ai/parse-resume`;
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({
          error: 'Failed to parse resume',
        }));
        return {
          success: false,
          error: error.detail || 'Failed to parse resume',
        };
      }

      return await response.json();
    } catch (error) {
      console.error('Resume parse error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to parse resume',
      };
    }
  }

  /**
   * Generate interview questions
   */
  async generateQuestions(
    request: QuestionGenerationRequest
  ): Promise<APIResponse<QuestionGenerationResponse>> {
    console.log('Sending question generation request:', request);
    const response = await this.fetch<QuestionGenerationResponse>('/ai/generate-questions', {
      method: 'POST',
      body: JSON.stringify(request),
    });
    console.log('Question generation response:', response);
    return response;
  }

  /**
   * Evaluate a single response
   */
  async evaluateResponse(
    request: ResponseEvaluationRequest
  ): Promise<APIResponse<ResponseEvaluationResponse>> {
    return this.fetch<ResponseEvaluationResponse>('/ai/evaluate-response', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Evaluate full interview
   */
  async evaluateInterview(
    request: InterviewEvaluationRequest
  ): Promise<APIResponse<InterviewEvaluationResponse>> {
    return this.fetch<InterviewEvaluationResponse>('/ai/evaluate-interview', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Health check for AI service
   */
  async healthCheck(): Promise<any> {
    return this.fetch('/ai/health', {
      method: 'GET',
    });
  }
}

// Export singleton instance
export const apiClient = new PrepWiseAPIClient();
export default apiClient;
