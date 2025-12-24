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
const TOKEN_KEY = 'prepwise_auth_token';

interface User {
  id: number;
  email: string;
  name: string;
  created_at: string;
}

interface TokenResponse {
  access_token: string;
  token_type: string;
}

class PrepWiseAPIClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  /**
   * Get stored authentication token
   */
  getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem(TOKEN_KEY);
  }

  /**
   * Store authentication token
   */
  private setToken(token: string): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem(TOKEN_KEY, token);
  }

  /**
   * Remove authentication token
   */
  logout(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem(TOKEN_KEY);
  }

  /**
   * Get authorization header if token exists
   */
  private getAuthHeaders(): Record<string, string> {
    const token = this.getToken();
    if (token) {
      return { Authorization: `Bearer ${token}` };
    }
    return {};
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
          ...this.getAuthHeaders(),
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

  /**
   * Register a new user
   */
  async register(email: string, name: string, password: string): Promise<User> {
    const response = await fetch(`${this.baseURL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, name, password }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: response.statusText,
      }));
      throw new Error(error.detail || 'Registration failed');
    }

    return await response.json();
  }

  /**
   * Login with email and password
   */
  async login(email: string, password: string): Promise<void> {
    const response = await fetch(`${this.baseURL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: response.statusText,
      }));
      throw new Error(error.detail || 'Login failed');
    }

    const data: TokenResponse = await response.json();
    this.setToken(data.access_token);
  }

  /**
   * Get current authenticated user
   */
  async getCurrentUser(): Promise<User> {
    const token = this.getToken();
    if (!token) {
      throw new Error('Not authenticated');
    }

    const response = await fetch(`${this.baseURL}/auth/me`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        this.logout();
      }
      const error = await response.json().catch(() => ({
        detail: response.statusText,
      }));
      throw new Error(error.detail || 'Failed to get user');
    }

    return await response.json();
  }
}

// Export singleton instance
export const apiClient = new PrepWiseAPIClient();
export default apiClient;
