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
    const url = `${this.baseURL}/auth/login`;
    console.log('🔐 Login attempt:', { email, url });
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      console.log('📡 Login response status:', response.status, response.statusText);

      if (!response.ok) {
        const error = await response.json().catch(() => ({
          detail: response.statusText,
        }));
        console.error('❌ Login error:', error);
        throw new Error(error.detail || 'Login failed');
      }

      const data: TokenResponse = await response.json();
      console.log('✅ Login successful, token received');
      this.setToken(data.access_token);
    } catch (error: any) {
      console.error('❌ Login exception:', error);
      if (error.message) {
        throw error;
      }
      throw new Error(error.message || 'Failed to connect to server. Make sure the backend is running.');
    }
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

  /**
   * Create Stripe checkout session for subscription
   */
  async createCheckoutSession(plan: 'starter' | 'professional'): Promise<{ checkout_url: string; session_id: string }> {
    const token = this.getToken();
    if (!token) {
      throw new Error('Not authenticated');
    }

    const response = await fetch(`${this.baseURL}/payments/create-checkout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ plan }),
    });

    if (!response.ok) {
      let error;
      try {
        error = await response.json();
      } catch {
        error = { detail: response.statusText || 'Unknown error' };
      }
      
      // Provide more helpful error messages
      const errorMessage = error.detail || error.message || 'Failed to create checkout session';
      
      // Check for specific Stripe configuration errors
      if (errorMessage.includes('not configured') || errorMessage.includes('Stripe is not configured')) {
        throw new Error('Stripe payment is not configured. Please add your Stripe API keys to the backend .env file and restart the server.');
      }
      
      throw new Error(errorMessage);
    }

    return await response.json();
  }

  /**
   * Get user's subscription status
   */
  async getSubscription(): Promise<any> {
    const token = this.getToken();
    if (!token) {
      throw new Error('Not authenticated');
    }

    const response = await fetch(`${this.baseURL}/payments/subscription`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: response.statusText,
      }));
      throw new Error(error.detail || 'Failed to get subscription');
    }

    return await response.json();
  }

  /**
   * Get checkout session details
   */
  async getCheckoutSession(sessionId: string): Promise<any> {
    const token = this.getToken();
    if (!token) {
      throw new Error('Not authenticated');
    }

    const response = await fetch(`${this.baseURL}/payments/checkout-session/${sessionId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: response.statusText,
      }));
      throw new Error(error.detail || 'Failed to get checkout session');
    }

    return await response.json();
  }

  /**
   * Cancel user's subscription
   */
  async cancelSubscription(): Promise<any> {
    const token = this.getToken();
    if (!token) {
      throw new Error('Not authenticated');
    }

    const response = await fetch(`${this.baseURL}/payments/cancel-subscription`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: response.statusText,
      }));
      throw new Error(error.detail || 'Failed to cancel subscription');
    }

    return await response.json();
  }

  /**
   * Get dashboard statistics
   */
  async getDashboardStats(): Promise<{
    total_interviews: number;
    average_score: number;
    best_score: number | null;
    hours_spent: number;
  }> {
    const token = this.getToken();
    if (!token) {
      throw new Error('Not authenticated');
    }

    const response = await fetch(`${this.baseURL}/dashboard/stats`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: response.statusText,
      }));
      throw new Error(error.detail || 'Failed to get dashboard statistics');
    }

    return await response.json();
  }

  /**
   * Get interview history
   */
  async getInterviewHistory(): Promise<{
    interviews: Array<{
      id: number;
      interview_type: string | null;
      technical_domain: string | null;
      date: string;
      score: number | null;
      duration_minutes: number | null;
      status: string;
    }>;
  }> {
    const token = this.getToken();
    if (!token) {
      throw new Error('Not authenticated');
    }

    const response = await fetch(`${this.baseURL}/dashboard/history`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: response.statusText,
      }));
      throw new Error(error.detail || 'Failed to get interview history');
    }

    return await response.json();
  }
}

// Export singleton instance
export const apiClient = new PrepWiseAPIClient();
export default apiClient;
