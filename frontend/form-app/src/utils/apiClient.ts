import type { 
  ApiResponse,
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
   * Make HTTP request with error handling and consistent API response format
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
      credentials: 'include', // Include HTTP-only cookies for secure session management
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      const result = await response.json().catch(() => ({})) as ApiResponse<T>;
      
      if (!response.ok || !result.success) {
        throw new Error(
          result.message || 
          `HTTP ${response.status}: ${response.statusText}`
        );
      }

      return result.data;
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  /**
   * Start a new survey session with secure HTTP-only cookie
   * Session ID is automatically managed via secure cookies
   */
  async startSession(params: {
    formId: string;
    clientId?: string;
    trackingData?: Partial<TrackingData>;
  }): Promise<StartSessionResponse> {
    return this.request<StartSessionResponse>('/api/survey/start', {
      method: 'POST',
      body: JSON.stringify({
        form_id: params.formId,
        client_id: params.clientId,
        utm_source: params.trackingData?.utmSource,
        utm_medium: params.trackingData?.utmMedium,
        utm_campaign: params.trackingData?.utmCampaign,
        utm_content: params.trackingData?.utmContent,
        utm_term: params.trackingData?.utmTerm,
        landing_page: params.trackingData?.landing_page
      }),
    });
  }

  /**
   * Submit form responses using secure session cookie
   * Session ID is automatically included via HTTP-only cookie
   */
  async submitResponses(request: SubmitResponseRequest): Promise<SubmitResponseResponse> {
    return this.request<SubmitResponseResponse>('/api/survey/step', {
      method: 'POST',
      body: JSON.stringify({
        responses: request.responses
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
   * Note: Theme endpoint not implemented yet, always returns null
   */
  async getTheme(formId: string): Promise<ThemeConfig | null> {
    // Theme loading not implemented yet - return null to use default theme
    console.log(`Theme loading skipped for form ${formId} - using default theme`);
    return null;
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
    try {
      const result = await this.request<{
        form: {
          id: string;
          title: string;
          description?: string;
          active: boolean;
        };
      }>(`/api/survey/forms/${formId}/validate`, {
        method: 'GET',
      });
      
      return {
        valid: true,
        form: result.form
      };
    } catch (error) {
      return {
        valid: false,
        error: error instanceof Error ? error.message : 'Form validation failed'
      };
    }
  }

  /**
   * Report form abandonment for analytics
   * Session ID is automatically included via HTTP-only cookie
   */
  async reportAbandonment(data?: {
    step?: number;
    timeSpent?: number;
    reason?: string;
  }): Promise<void> {
    await this.request<void>('/api/survey/abandon', {
      method: 'POST',
      body: JSON.stringify(data || {}),
    });
  }

  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    return this.request<{ status: string; timestamp: string }>('/health', {
      method: 'GET',
    });
  }
}

// Export singleton instance
export const apiClient = new APIClient();

// Export class for testing
export { APIClient };