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
  question_id?: string | number;  // CRITICAL: Form-specific question ID from backend
  question: string;
  phrased_question: string;
  input_type: string;  // Frontend input type (text, textarea, radio, select, etc.)
  data_type: string;   // Backend data type (text, integer, float, boolean, etc.)
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
    logoUrl?: string;
    theme?: ThemeConfig;
    clientId?: string;  // Client ID resolved from form (UUID, safe to expose)
  };
  step: BackendFormStep;
}

// API configuration
// In development, use relative URLs to go through Vite proxy
const API_BASE_URL = import.meta.env.PROD ? (import.meta.env.VITE_API_URL || 'http://localhost:8000') : '';

class APIClient {
  private baseUrl: string;
  
  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl.replace(/\/$/, ''); // Remove trailing slash
  }

  /**
   * Transform backend question data to frontend format
   */
  private transformQuestion(backendQuestion: BackendQuestion, index: number): Question {
    // CRITICAL FIX: Use actual question_id from backend for proper tracking
    // Backend now sends question_id - use them instead of generating from index
    const questionId = backendQuestion.question_id 
      ? String(backendQuestion.question_id)  // Convert to string (can be UUID or number)
      : (index + 1).toString();              // Fallback only if no ID provided
    
    return {
      id: questionId,
      type: backendQuestion.input_type as QuestionType,  // Use input_type directly for frontend rendering
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
   * Map backend data_type to frontend QuestionType (DEPRECATED)
   * 
   * NOTE: This method is no longer used since we now use input_type directly.
   * Keeping for backward compatibility in case of rollback.
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
      'file': 'file',
      'boolean': 'radio'  // Boolean questions should be radio buttons (Yes/No)
    };
    
    return typeMap[dataType] || 'text';
  }

  /**
   * Transform backend options to frontend format
   */
  private transformQuestionOptions(backendQuestion: BackendQuestion) {
    // Special handling for boolean questions - they need Yes/No options
    if (backendQuestion.data_type === 'boolean') {
      return {
        choices: [
          { id: '1', text: 'Yes', value: 'yes' },
          { id: '2', text: 'No', value: 'no' }
        ]
      };
    }

    if (!backendQuestion.options) return undefined;

    // If options is an array, transform to choices format
    if (Array.isArray(backendQuestion.options)) {
      // Check if array contains objects with label/value or strings
      const firstOption = backendQuestion.options[0];
      
      if (typeof firstOption === 'string') {
        // Array of strings - convert to choice objects
        return {
          choices: backendQuestion.options.map((option: string, index: number) => ({
            id: (index + 1).toString(),
            text: option,
            value: option
          }))
        };
      } else if (typeof firstOption === 'object' && 'label' in firstOption && 'value' in firstOption) {
        // Array of {label, value} objects - transform to {id, text, value} format
        return {
          choices: backendQuestion.options.map((option: any, index: number) => ({
            id: (index + 1).toString(),
            text: option.label,
            value: option.value
          }))
        };
      }
    }

    // If options is an object with choices property, return as-is
    if (backendQuestion.options && typeof backendQuestion.options === 'object' && 'choices' in backendQuestion.options) {
      return backendQuestion.options;
    }

    // Fallback - return undefined for unsupported option formats
    return undefined;
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
    trackingData?: Partial<TrackingData>;
  }): Promise<StartSessionResponse> {
    const response = await this.request<BackendStartSessionResponse>('/api/survey/start', {
      method: 'POST',
      body: JSON.stringify({
        form_id: params.formId,
        // client_id is automatically extracted by backend from form record
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
        logoUrl: response.form.logoUrl,
        theme: response.form.theme,
        clientId: response.form.clientId  // Pass through client ID for additional API calls
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
   * Get current form step (not implemented in backend yet)
   * TODO: Backend should provide a GET /api/survey/step endpoint
   */
  async getCurrentStep(): Promise<FormStep> {
    throw new Error('getCurrentStep not implemented - backend should provide GET /api/survey/step');
  }

  /**
   * Save progress for session recovery using session cookie
   */
  async saveProgress(data: {
    responses: Record<string, any>;
    currentStep: number;
    lastUpdated: string;
  }): Promise<void> {
    await this.request<void>('/api/survey/save-progress', {
      method: 'POST',
      body: JSON.stringify(data),
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
   * Resume session from recovery data using session cookie
   */
  async resumeSession(): Promise<StartSessionResponse> {
    return this.request<StartSessionResponse>('/api/survey/resume', {
      method: 'POST',
    });
  }

  /**
   * Get form completion data using session cookie
   */
  async getCompletionData(): Promise<{
    leadStatus: string;
    score: number;
    message: string;
    redirectUrl?: string;
    nextSteps?: string[];
  }> {
    return this.request('/api/survey/completion', {
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