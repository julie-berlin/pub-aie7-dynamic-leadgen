/**
 * TypeScript types for Survey API
 * Generated from Pydantic models
 * 
 * Last updated: August 9, 2025
 */

// === UNION TYPES (instead of enums) ===

export type LeadStatus = 'unknown' | 'yes' | 'maybe' | 'no';

export type AbandonmentStatus = 'active' | 'at_risk' | 'high_risk' | 'abandoned';

export type CompletionType = 'qualified' | 'unqualified' | 'abandoned' | 'qualified_fallback' | 'unqualified_error';

export type FlowPhase = 'initialization' | 'questioning' | 'qualification' | 'completion';

export type FlowStrategy = 'STANDARD' | 'RECOVERY' | 'QUALIFIED_COMPLETION' | 'ABANDONMENT_PREVENTION';

export type QuestionType = 'text' | 'email' | 'multiple_choice' | 'boolean' | 'textarea' | 'number' | 'phone' | 'url';

// === CONST OBJECTS for type-safe access ===

export const LEAD_STATUS = {
  UNKNOWN: 'unknown',
  YES: 'yes',
  MAYBE: 'maybe',
  NO: 'no',
} as const;

export const ABANDONMENT_STATUS = {
  ACTIVE: 'active',
  AT_RISK: 'at_risk',
  HIGH_RISK: 'high_risk',
  ABANDONED: 'abandoned',
} as const;

export const COMPLETION_TYPE = {
  QUALIFIED: 'qualified',
  UNQUALIFIED: 'unqualified',
  ABANDONED: 'abandoned',
  QUALIFIED_FALLBACK: 'qualified_fallback',
  UNQUALIFIED_ERROR: 'unqualified_error',
} as const;

export const QUESTION_TYPES = {
  TEXT: 'text',
  EMAIL: 'email',
  MULTIPLE_CHOICE: 'multiple_choice',
  BOOLEAN: 'boolean',
  TEXTAREA: 'textarea',
  NUMBER: 'number',
  PHONE: 'phone',
  URL: 'url',
} as const;

// === API REQUEST TYPES ===

export interface StartSessionRequest {
  /** Form configuration identifier */
  form_id: string;
  /** Optional client identifier */
  client_id?: string;
  
  // UTM Parameters
  /** Marketing source (facebook, google, etc.) */
  utm_source?: string;
  /** Marketing medium (social, cpc, email) */
  utm_medium?: string;
  /** Campaign name */
  utm_campaign?: string;
  /** Ad content identifier */
  utm_content?: string;
  /** Search term */
  utm_term?: string;
  
  /** Landing page URL */
  landing_page?: string;
  /** Additional metadata */
  metadata?: Record<string, any>;
}

export interface SubmitResponsesRequest {
  /** Session identifier */
  session_id: string;
  /** User responses for current step */
  responses: ResponseSubmission[];
}

export interface ResponseSubmission {
  /** Question being answered */
  question_id: number;
  /** User's answer */
  answer: string;
  /** Original question text (for logging) */
  question_text?: string;
  /** Time taken to answer in seconds */
  response_time_seconds?: number;
}

export interface AbandonSessionRequest {
  /** Session identifier */
  session_id: string;
  /** Abandonment reason */
  reason?: string;
}

// === API RESPONSE TYPES ===

export interface QuestionData {
  /** Question ID within form */
  id: number;
  /** Original question text */
  question: string;
  /** AI-adapted question text */
  phrased_question: string;
  /** Expected response data type */
  data_type: QuestionType;
  /** Whether question is required */
  is_required: boolean;
  /** Multiple choice options */
  options?: string[];
  /** Scoring criteria */
  scoring_rubric?: string;
}

export interface StartSessionResponse {
  /** Unique session identifier */
  session_id: string;
  /** Initial questions */
  questions: QuestionData[];
  /** Engaging step headline */
  headline: string;
  /** Motivational content */
  motivation: string;
  /** Current step number */
  step: number;
  /** Progress indicators */
  progress?: Record<string, any>;
}

export interface StepResponse {
  /** Session identifier */
  session_id: string;
  /** Current step number */
  step: number;
  /** Questions for this step */
  questions: QuestionData[];
  /** Engaging step headline */
  headline: string;
  /** Motivational content */
  motivation: string;
  /** Progress information */
  progress: Record<string, any>;
  /** Whether survey is complete */
  completed: boolean;
  /** Final completion message (if completed) */
  completion_message?: string;
}

export interface CompletionResponse {
  /** Session identifier */
  session_id: string;
  /** Final lead qualification */
  lead_status: LeadStatus;
  /** Final lead score */
  final_score: number;
  /** Personalized completion message */
  completion_message: string;
  /** Type of completion */
  completion_type: CompletionType;
  /** Completion timestamp */
  completed_at: string;
}

export interface SessionStatusResponse {
  /** Session identifier */
  session_id: string;
  /** Form configuration ID */
  form_id: string;
  /** Current step number */
  step: number;
  /** Whether session is completed */
  completed: boolean;
  /** Current lead qualification */
  lead_status: LeadStatus;
  /** Current lead score */
  current_score: number;
  /** Number of responses collected */
  responses_count: number;
  /** Session start timestamp */
  started_at: string;
  /** Last update timestamp */
  last_updated: string;
  /** Abandonment risk status */
  abandonment_status: AbandonmentStatus;
}

export interface ErrorResponse {
  /** Error type */
  error: string;
  /** Human-readable error message */
  message: string;
  /** Additional error details */
  details?: Record<string, any>;
  /** Error timestamp */
  timestamp: string;
}

export interface AbandonResponse {
  /** Operation status */
  status: string;
  /** Confirmation message */
  message: string;
}

// === FRONTEND UTILITY TYPES ===

export interface ApiResponse<T = any> {
  data?: T;
  error?: ErrorResponse;
  success: boolean;
  status: number;
}

export interface FormState {
  sessionId: string | null;
  currentStep: number;
  completed: boolean;
  questions: QuestionData[];
  responses: ResponseSubmission[];
  leadStatus: LeadStatus;
  abandonmentStatus: AbandonmentStatus;
  completionMessage?: string;
}

export interface ProgressInfo {
  currentStep: number;
  totalSteps: number;
  completionPercentage: number;
  questionsAnswered: number;
}

export interface UTMParams {
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  utm_content?: string;
  utm_term?: string;
}

export interface SurveyConfig {
  apiBaseUrl: string;
  formId: string;
  utmParams?: UTMParams;
  onComplete?: (response: CompletionResponse) => void;
  onAbandon?: (sessionId: string) => void;
  onError?: (error: ErrorResponse) => void;
}

// === API CLIENT INTERFACE ===

export interface SurveyApiClient {
  /**
   * Start a new survey session
   */
  startSession(request: StartSessionRequest): Promise<ApiResponse<StartSessionResponse>>;
  
  /**
   * Submit responses and get next step
   */
  submitResponses(request: SubmitResponsesRequest): Promise<ApiResponse<StepResponse>>;
  
  /**
   * Mark session as abandoned
   */
  abandonSession(request: AbandonSessionRequest): Promise<ApiResponse<AbandonResponse>>;
  
  /**
   * Get current session status
   */
  getSessionStatus(sessionId: string): Promise<ApiResponse<SessionStatusResponse>>;
}

// === FORM VALIDATION TYPES ===

export interface FormValidationRule {
  type: 'required' | 'email' | 'minLength' | 'maxLength' | 'pattern';
  value?: string | number;
  message: string;
}

export interface FormFieldConfig {
  questionId: number;
  type: QuestionType;
  label: string;
  placeholder?: string;
  options?: string[];
  validation?: FormValidationRule[];
  required: boolean;
}

export interface FormStepConfig {
  step: number;
  title: string;
  description?: string;
  fields: FormFieldConfig[];
}

// === EVENT TYPES ===

export interface SurveyEvent {
  type: 'session_started' | 'response_submitted' | 'step_completed' | 'survey_completed' | 'survey_abandoned';
  sessionId: string;
  timestamp: string;
  data?: Record<string, any>;
}

export interface AnalyticsEvent {
  type: 'page_view' | 'question_view' | 'response_submit' | 'abandonment_risk' | 'completion';
  sessionId: string;
  step?: number;
  questionId?: number;
  value?: string | number;
  metadata?: Record<string, any>;
  timestamp: string;
}

// === HOOK TYPES (for React) ===

export interface UseSurveyState {
  state: FormState;
  loading: boolean;
  error: ErrorResponse | null;
  startSession: (formId: string, utmParams?: UTMParams) => Promise<void>;
  submitResponses: (responses: ResponseSubmission[]) => Promise<void>;
  abandonSession: () => Promise<void>;
  resetSurvey: () => void;
}

export interface UseSurveyAnalytics {
  trackEvent: (event: AnalyticsEvent) => void;
  trackPageView: (step: number) => void;
  trackQuestionView: (questionId: number) => void;
  trackResponseSubmit: (questionId: number, answer: string) => void;
  trackAbandonmentRisk: (riskLevel: AbandonmentStatus) => void;
  trackCompletion: (leadStatus: LeadStatus, score: number) => void;
}

// === CONSTANTS ===

export const API_ENDPOINTS = {
  START_SESSION: '/api/survey/start',
  SUBMIT_RESPONSES: '/api/survey/step', 
  ABANDON_SESSION: '/api/survey/abandon',
  SESSION_STATUS: '/api/survey/status',
} as const;

export const ABANDONMENT_THRESHOLDS = {
  AT_RISK_MINUTES: 5,
  HIGH_RISK_MINUTES: 10,
  ABANDONED_MINUTES: 15,
} as const;

// === TYPE GUARDS ===

export const isLeadStatus = (value: string): value is LeadStatus => {
  return Object.values(LEAD_STATUS).includes(value as LeadStatus);
};

export const isAbandonmentStatus = (value: string): value is AbandonmentStatus => {
  return Object.values(ABANDONMENT_STATUS).includes(value as AbandonmentStatus);
};

export const isQuestionType = (value: string): value is QuestionType => {
  return Object.values(QUESTION_TYPES).includes(value as QuestionType);
};

// === UTILITY FUNCTIONS ===

export const getLeadStatusDisplay = (status: LeadStatus): string => {
  const displays = {
    [LEAD_STATUS.UNKNOWN]: 'Unknown',
    [LEAD_STATUS.YES]: 'Qualified Lead',
    [LEAD_STATUS.MAYBE]: 'Potential Lead',
    [LEAD_STATUS.NO]: 'Unqualified',
  };
  return displays[status] || status;
};

export const getAbandonmentRiskLevel = (status: AbandonmentStatus): 'low' | 'medium' | 'high' | 'critical' => {
  switch (status) {
    case ABANDONMENT_STATUS.ACTIVE:
      return 'low';
    case ABANDONMENT_STATUS.AT_RISK:
      return 'medium';
    case ABANDONMENT_STATUS.HIGH_RISK:
      return 'high';
    case ABANDONMENT_STATUS.ABANDONED:
      return 'critical';
    default:
      return 'low';
  }
};