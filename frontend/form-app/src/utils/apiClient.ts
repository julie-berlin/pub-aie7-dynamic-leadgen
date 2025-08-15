import type { 
  ApiResponse,
  StartSessionResponse,
  SubmitResponseRequest,
  SubmitResponseResponse,
  FormStep,
  ThemeConfig,
  TrackingData,
  Question,
  QuestionType
} from '../types';

// Backend API response types
interface BackendQuestion {
  question: string;
  phrased_question: string;
  data_type: string;
  is_required: boolean;
  options?: string[] | Record<string, any>;
  description?: string;
  placeholder?: string;
  // Note: scoring_rubric deliberately excluded - sensitive backend data
}

interface BackendFormStep {
  stepNumber: number;
  totalSteps: number;
  questions: BackendQuestion[];
  headline: string;
  subheading?: string;
  isComplete: boolean;
  canGoBack?: boolean;
  isLastStep?: boolean;
}

interface BackendStartSessionResponse {
  form: {
    id?: string;
    title: string;
    description?: string;
    businessName?: string;
    theme?: ThemeConfig;
  };
  step: BackendFormStep;
}

// API configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class APIClient {
  private baseUrl: string;
  
  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl.replace(/\/$/, ''); // Remove trailing slash
  }

  /**
   * Transform backend question data to frontend format
   */
  private transformQuestion(backendQuestion: BackendQuestion, index: number): Question {
    return {
      id: (index + 1).toString(), // Generate ID from index since backend doesn't provide it
      type: this.mapDataTypeToQuestionType(backendQuestion.data_type),
      text: backendQuestion.phrased_question || backendQuestion.question,
      description: backendQuestion.description,
      placeholder: backendQuestion.placeholder,
      required: backendQuestion.is_required || false,
      options: this.transformQuestionOptions(backendQuestion),
      validation: this.transformValidationRules(backendQuestion),
      conditional: undefined // Backend doesn't seem to provide conditional logic yet
    };
  }

  /**
   * Map backend data_type to frontend QuestionType
   */
  private mapDataTypeToQuestionType(dataType: string): QuestionType {
    const typeMap: Record<string, QuestionType> = {
      'text': 'text',
      'textarea': 'textarea', 
      'email': 'email',
      'phone': 'phone',
      'number': 'number',
      'select': 'select',
      'radio': 'radio',
      'checkbox': 'checkbox',
      'multiselect': 'multiselect',
      'rating': 'rating',
      'date': 'date',
      'time': 'time',
      'datetime': 'datetime',
      'file': 'file'
    };
    
    return typeMap[dataType] || 'text';
  }

  /**
   * Transform backend options to frontend format
   */
  private transformQuestionOptions(backendQuestion: BackendQuestion) {
    if (!backendQuestion.options) return undefined;

    // If options is an array of strings (like for select), convert to choices
    if (Array.isArray(backendQuestion.options)) {
      return {
        choices: backendQuestion.options.map((option: string, index: number) => ({
          id: (index + 1).toString(),
          text: option,
          value: option
        }))
      };
    }

    // If options is an object, return as-is (for complex option structures)
    return backendQuestion.options;
  }

  /**
   * Transform backend validation to frontend format
   */
  private transformValidationRules(backendQuestion: BackendQuestion) {
    const rules = [];
    
    if (backendQuestion.is_required) {
      rules.push({
        type: 'required' as const,
        message: 'This field is required'
      });
    }

    // Add more validation transformations as needed based on backend schema
    return rules.length > 0 ? rules : undefined;
  }

  /**
   * Transform backend step response to frontend format
   */
  private transformFormStep(backendStep: BackendFormStep): FormStep {
    return {
      stepNumber: backendStep.stepNumber,
      totalSteps: backendStep.totalSteps,
      questions: backendStep.questions.map((q, index) => this.transformQuestion(q, index)),
      headline: backendStep.headline || '',
      subheading: backendStep.subheading,
      isComplete: backendStep.isComplete,
      canGoBack: backendStep.canGoBack,
      isLastStep: backendStep.isLastStep
    };
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
    const response = await this.request<BackendStartSessionResponse>('/api/survey/start', {
      method: 'POST',
      body: JSON.stringify({
        form_id: params.formId,
        // Don't send client_id - backend will extract it from form details
        utm_source: params.trackingData?.utmSource,
        utm_medium: params.trackingData?.utmMedium,
        utm_campaign: params.trackingData?.utmCampaign,
        utm_content: params.trackingData?.utmContent,
        utm_term: params.trackingData?.utmTerm
      }),
    });

    // Transform the response to match frontend types
    return {
      form: {
        id: response.form.id || 'unknown',
        title: response.form.title,
        description: response.form.description,
        businessName: response.form.businessName,
        theme: response.form.theme
      },
      step: this.transformFormStep(response.step)
    };
  }

  /**
   * Submit form responses using secure session cookie
   * Session ID is automatically included via HTTP-only cookie
   */
  async submitResponses(request: SubmitResponseRequest): Promise<SubmitResponseResponse> {
    const response = await this.request<{
      isComplete: boolean;
      nextStep?: BackendFormStep;
      completionData?: any;
    }>('/api/survey/step', {
      method: 'POST',
      body: JSON.stringify({
        responses: request.responses
      }),
    });

    // Transform the response to match frontend types
    return {
      isComplete: response.isComplete,
      nextStep: response.nextStep ? this.transformFormStep(response.nextStep) : undefined,
      completionData: response.completionData
    };
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
   * Returns the effective theme (form-specific or client default)
   */
  async getTheme(formId: string): Promise<ThemeConfig | null> {
    try {
      return await this.request<ThemeConfig>(`/api/themes/form/${formId}/theme`, {
        method: 'GET',
      });
    } catch (error) {
      console.warn(`Failed to load theme for form ${formId}, using default:`, error);
      return null;
    }
  }

  /**
   * Get client information by ID
   */
  async getClient(clientId: string): Promise<{
    id: string;
    business_name: string;
    name: string;
    industry: string;
    website?: string;
  } | null> {
    try {
      const response = await this.request<{ 
        data: {
          id: string;
          business_name: string;
          name: string;
          industry: string;
          website?: string;
        }
      }>(`/api/clients/${clientId}`, {
        method: 'GET',
      });
      
      return response.data;
    } catch (error) {
      console.warn(`Failed to load client info for ${clientId}:`, error);
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
  async validateFormAccess(formId: string): Promise<{
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