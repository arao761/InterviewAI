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
  public baseURL: string;

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
   * Automatically wakes up the backend if it's sleeping (Render free tier)
   */
  async register(email: string, name: string, password: string, wakeUpCallback?: (status: string) => void): Promise<User> {
    const url = `${this.baseURL}/auth/register`;
    console.log('📝 Registration attempt:', { email, name, url });
    
    // Step 1: Wake up the backend first
    if (wakeUpCallback) {
      wakeUpCallback('Waking up backend server...');
    }
    
    const backendAwake = await this.wakeUpBackend(45000); // 45 seconds max for wake-up
    
    if (!backendAwake && wakeUpCallback) {
      wakeUpCallback('Backend is slow to respond, attempting registration anyway...');
    }
    
    // Step 2: Attempt registration with retry logic
    const maxRetries = 3;
    let lastError: Error | null = null;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      if (wakeUpCallback && attempt > 1) {
        wakeUpCallback(`Retrying registration (attempt ${attempt}/${maxRetries})...`);
      }
      
      const controller = new AbortController();
      // 30 second timeout per attempt (backend should be awake now)
      const timeoutId = setTimeout(() => controller.abort(), 30000);
      
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, name, password }),
          signal: controller.signal,
        });

        clearTimeout(timeoutId);
        console.log('📡 Registration response status:', response.status, response.statusText);

        if (!response.ok) {
          const error = await response.json().catch(() => ({
            detail: response.statusText,
          }));
          console.error('❌ Registration error:', error);
          throw new Error(error.detail || 'Registration failed');
        }

        const data = await response.json();
        console.log('✅ Registration successful:', data);
        return data;
      } catch (error: any) {
        clearTimeout(timeoutId);
        lastError = error;
        
        // If it's an abort error and we have retries left, wait and retry
        if (error.name === 'AbortError' && attempt < maxRetries) {
          console.log(`⏳ Registration timeout (attempt ${attempt}), retrying...`);
          await new Promise(resolve => setTimeout(resolve, 2000 * attempt)); // Exponential backoff
          continue;
        }
        
        // If it's a network error and we have retries left, wait and retry
        if (!error.message && attempt < maxRetries) {
          console.log(`🌐 Network error (attempt ${attempt}), retrying...`);
          await new Promise(resolve => setTimeout(resolve, 2000 * attempt));
          continue;
        }
        
        // If it's a validation error (email already exists, etc.), don't retry
        if (error.message && (error.message.includes('email') || error.message.includes('already') || error.message.includes('Registration failed'))) {
          throw error;
        }
      }
    }
    
    // If we get here, all retries failed
    console.error('❌ Registration failed after all retries:', lastError);
    if (lastError?.name === 'AbortError') {
      throw new Error('Registration request timed out. The backend server may be experiencing issues. Please try again in a moment.');
    }
    if (lastError?.message) {
      throw lastError;
    }
    throw new Error(`Failed to connect to server at ${this.baseURL}. Please check your internet connection and try again.`);
  }

  /**
   * Wake up the backend server by pinging the health endpoint
   * This is necessary for Render free tier services that sleep after inactivity
   */
  async wakeUpBackend(maxWaitTime: number = 60000): Promise<boolean> {
    const healthUrl = `${this.baseURL.replace('/api/v1', '')}/health`;
    const startTime = Date.now();
    
    console.log('🌅 Attempting to wake up backend:', healthUrl);
    
    // Try to wake up the backend with multiple attempts
    const maxAttempts = 10;
    const attemptDelay = 2000; // 2 seconds between attempts
    
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      // Check if we've exceeded max wait time
      if (Date.now() - startTime > maxWaitTime) {
        console.warn('⏱️ Wake-up timeout exceeded');
        return false;
      }
      
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout per attempt
        
        const response = await fetch(healthUrl, {
          method: 'GET',
          signal: controller.signal,
        });
        
        clearTimeout(timeoutId);
        
        if (response.ok) {
          const elapsed = Date.now() - startTime;
          console.log(`✅ Backend is awake after ${elapsed}ms (attempt ${attempt})`);
          // Give it a moment to fully initialize
          await new Promise(resolve => setTimeout(resolve, 500));
          return true;
        }
      } catch (error: any) {
        // If it's not an abort error, the backend might be responding but with an error
        if (error.name !== 'AbortError') {
          console.log(`⚠️ Backend responded with error (attempt ${attempt}), might be waking up...`);
          // Wait a bit and try the actual login
          await new Promise(resolve => setTimeout(resolve, 1000));
          return true; // Assume it's waking up if we got any response
        }
      }
      
      // Wait before next attempt (except on last attempt)
      if (attempt < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, attemptDelay));
      }
    }
    
    console.warn('⚠️ Could not wake up backend after all attempts');
    return false;
  }

  /**
   * Login with email and password
   * Automatically wakes up the backend if it's sleeping (Render free tier)
   */
  async login(email: string, password: string, wakeUpCallback?: (status: string) => void): Promise<void> {
    const url = `${this.baseURL}/auth/login`;
    console.log('🔐 Login attempt:', { email, url });
    
    // Step 1: Wake up the backend first
    if (wakeUpCallback) {
      wakeUpCallback('Waking up backend server...');
    }
    
    const backendAwake = await this.wakeUpBackend(45000); // 45 seconds max for wake-up
    
    if (!backendAwake && wakeUpCallback) {
      wakeUpCallback('Backend is slow to respond, attempting login anyway...');
    }
    
    // Step 2: Attempt login with retry logic
    const maxRetries = 3;
    let lastError: Error | null = null;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      if (wakeUpCallback && attempt > 1) {
        wakeUpCallback(`Retrying login (attempt ${attempt}/${maxRetries})...`);
      }
      
      const controller = new AbortController();
      // 30 second timeout per attempt (backend should be awake now)
      const timeoutId = setTimeout(() => controller.abort(), 30000);
      
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
          signal: controller.signal,
        });

        clearTimeout(timeoutId);
        console.log('📡 Login response status:', response.status, response.statusText);

        if (!response.ok) {
          const error = await response.json().catch(() => ({
            detail: response.statusText,
          }));
          console.error('❌ Login error:', error);
          const errorMessage = error.detail || 'Login failed';
          // Don't retry on authentication errors (401) or email verification errors (403)
          if (response.status === 401 || response.status === 403) {
            throw new Error(errorMessage);
          }
          throw new Error(errorMessage);
        }

        const data: TokenResponse = await response.json();
        console.log('✅ Login successful, token received');
        this.setToken(data.access_token);
        return; // Success!
      } catch (error: any) {
        clearTimeout(timeoutId);
        lastError = error;
        
        // If it's an abort error and we have retries left, wait and retry
        if (error.name === 'AbortError' && attempt < maxRetries) {
          console.log(`⏳ Login timeout (attempt ${attempt}), retrying...`);
          await new Promise(resolve => setTimeout(resolve, 2000 * attempt)); // Exponential backoff
          continue;
        }
        
        // If it's a network error and we have retries left, wait and retry
        if (!error.message && attempt < maxRetries) {
          console.log(`🌐 Network error (attempt ${attempt}), retrying...`);
          await new Promise(resolve => setTimeout(resolve, 2000 * attempt));
          continue;
        }
        
        // If it's an authentication error or email verification error, don't retry
        if (error.message && (
          error.message.includes('password') || 
          error.message.includes('email') || 
          error.message.includes('verify') ||
          error.message.includes('Login failed')
        )) {
          throw error;
        }
      }
    }
    
    // If we get here, all retries failed
    console.error('❌ Login failed after all retries:', lastError);
    if (lastError?.name === 'AbortError') {
      throw new Error('Login request timed out. The backend server may be experiencing issues. Please try again in a moment.');
    }
    if (lastError?.message) {
      throw lastError;
    }
    throw new Error(`Failed to connect to server at ${this.baseURL}. Please check your internet connection and try again.`);
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
