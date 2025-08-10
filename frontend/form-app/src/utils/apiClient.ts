import type { 
  StartSessionResponse,
  SubmitResponseRequest,
  SubmitResponseResponse,
  FormStep,
  ThemeConfig,
  TrackingData
} from '../types';

// API configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class APIClient {
  private baseUrl: string;
  
  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl.replace(/\/$/, ''); // Remove trailing slash
  }

  /**
   * Make HTTP request with error handling
   */
  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.message || 
          errorData.detail || 
          `HTTP ${response.status}: ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  /**
   * Start or resume a form session
   */
  async startSession(params: {
    clientId: string;
    formId: string;
    sessionId?: string;
    trackingData?: Partial<TrackingData>;
  }): Promise<StartSessionResponse> {
    return this.request<StartSessionResponse>('/api/survey/start', {
      method: 'POST',
      body: JSON.stringify({
        client_id: params.clientId,
        form_id: params.formId,
        session_id: params.sessionId,
        tracking_data: params.trackingData
      }),
    });
  }

  /**
   * Submit form responses
   */
  async submitResponses(request: SubmitResponseRequest): Promise<SubmitResponseResponse> {
    return this.request<SubmitResponseResponse>('/api/survey/submit', {
      method: 'POST',
      body: JSON.stringify({
        session_id: request.sessionId,
        responses: request.responses,
        current_step: request.currentStep,
        timestamp: request.timestamp
      }),
    });
  }

  /**
   * Get a specific form step
   */
  async getStep(sessionId: string, step: number): Promise<FormStep> {
    return this.request<FormStep>(`/api/survey/step/${sessionId}/${step}`, {
      method: 'GET',
    });
  }

  /**
   * Save progress for session recovery
   */
  async saveProgress(sessionId: string, data: {
    responses: Record<string, any>;
    currentStep: number;
    lastUpdated: string;
  }): Promise<void> {
    await this.request<void>('/api/survey/save-progress', {
      method: 'POST',
      body: JSON.stringify({
        session_id: sessionId,
        ...data
      }),
    });
  }

  /**
   * Get theme configuration for a form
   */
  async getTheme(formId: string): Promise<ThemeConfig | null> {
    try {
      return await this.request<ThemeConfig>(`/api/survey/theme/${formId}`, {
        method: 'GET',
      });
    } catch (error) {
      // Theme is optional, return null if not found
      console.warn(`Theme not found for form ${formId}:`, error);
      return null;
    }
  }

  /**
   * Resume session from recovery data
   */
  async resumeSession(sessionId: string): Promise<StartSessionResponse> {
    return this.request<StartSessionResponse>(`/api/survey/resume/${sessionId}`, {
      method: 'POST',
    });
  }

  /**
   * Get form completion data
   */
  async getCompletionData(sessionId: string): Promise<{
    leadStatus: string;
    score: number;
    message: string;
    redirectUrl?: string;
    nextSteps?: string[];
  }> {
    return this.request(`/api/survey/completion/${sessionId}`, {
      method: 'GET',
    });
  }

  /**
   * Validate form access
   */
  async validateFormAccess(clientId: string, formId: string): Promise<{
    valid: boolean;
    form?: {
      id: string;
      title: string;
      description?: string;
      active: boolean;
    };
    error?: string;
  }> {
    return this.request(`/api/survey/validate/${clientId}/${formId}`, {
      method: 'GET',
    });
  }

  /**
   * Report form abandonment for analytics
   */
  async reportAbandonment(sessionId: string, data: {
    step: number;
    timeSpent: number;
    reason?: string;
  }): Promise<void> {
    await this.request('/api/survey/abandon', {
      method: 'POST',
      body: JSON.stringify({
        session_id: sessionId,
        ...data
      }),
    });
  }

  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    return this.request('/health', {
      method: 'GET',
    });
  }
}

// Export singleton instance
export const apiClient = new APIClient();

// Export class for testing
export { APIClient };