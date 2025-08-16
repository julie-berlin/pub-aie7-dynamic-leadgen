/**
 * Auto-generated TypeScript types for Dynamic Survey Platform
 * Generated from Pydantic models
 * 
 * Last updated: 2025-08-16
 * 
 * DO NOT EDIT MANUALLY - This file is auto-generated
 * Run `python3 backend/generate_typescript_types.py` to update
 * 
 * Phase 2 Support: ❌ Not Available
 */


// === CORE ENUMS ===

export enum LeadStatus {
  UNKNOWN = 'unknown',
  YES = 'yes',
  MAYBE = 'maybe',
  NO = 'no',
}

export enum AbandonmentStatus {
  ACTIVE = 'active',
  AT_RISK = 'at_risk',
  HIGH_RISK = 'high_risk',
  ABANDONED = 'abandoned',
}

export enum CompletionType {
  QUALIFIED = 'qualified',
  UNQUALIFIED = 'unqualified',
  ABANDONED = 'abandoned',
  QUALIFIED_FALLBACK = 'qualified_fallback',
  UNQUALIFIED_ERROR = 'unqualified_error',
}

export enum FlowPhase {
  INITIALIZATION = 'initialization',
  QUESTIONING = 'questioning',
  QUALIFICATION = 'qualification',
  COMPLETION = 'completion',
}

export enum FlowStrategy {
  STANDARD = 'STANDARD',
  RECOVERY = 'RECOVERY',
  QUALIFIED_COMPLETION = 'QUALIFIED_COMPLETION',
  ABANDONMENT_PREVENTION = 'ABANDONMENT_PREVENTION',
}

// === CORE SURVEY API TYPES ===

export interface StartSessionRequest {
  /** Form configuration identifier */
  form_id: string;
  /** Optional client identifier */
  client_id?: string;
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
  /** User responses for current step */
  responses: Record<string, any>[];
}

export interface AbandonSessionRequest {
  /** Session identifier */
  session_id: string;
  /** Abandonment reason */
  reason?: string;
}

export interface StartSessionResponse {
  /** Unique session identifier */
  session_id: string;
  /** Initial questions */
  questions: any[];
  /** Engaging step headline */
  headline: string;
  /** Motivational content */
  motivation: string;
  /** Current step number */
  step?: number;
  /** Progress indicators */
  progress?: Record<string, any>;
}

export interface StepResponse {
  /** Session identifier */
  session_id: string;
  /** Current step number */
  step: number;
  /** Questions for this step */
  questions: any[];
  /** Engaging step headline */
  headline: string;
  /** Motivational content */
  motivation: string;
  /** Progress information */
  progress?: Record<string, any>;
  /** Whether survey is complete */
  completed?: boolean;
}

export interface CompletionResponse {
  /** Session identifier */
  session_id: string;
  /** Final lead qualification */
  lead_status: "unknown" | "yes" | "maybe" | "no";
  /** Final lead score */
  final_score: number;
  /** Personalized completion message */
  completion_message: string;
  /** Type of completion */
  completion_type: "qualified" | "unqualified" | "abandoned" | "qualified_fallback" | "unqualified_error";
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
  lead_status: "unknown" | "yes" | "maybe" | "no";
  /** Current lead score */
  current_score: number;
  /** Number of responses collected */
  responses_count: number;
  /** Session start timestamp */
  started_at: string;
  /** Last update timestamp */
  last_updated: string;
  /** Abandonment risk status */
  abandonment_status: "active" | "at_risk" | "high_risk" | "abandoned";
}

export interface ErrorResponse {
  /** Error type */
  error: string;
  /** Human-readable error message */
  message: string;
  /** Additional error details */
  details?: Record<string, any>;
  /** Error timestamp */
  timestamp?: string;
}

export interface QuestionData {
  /** Question ID within form */
  id: number;
  /** Original question text */
  question: string;
  /** AI-adapted question text */
  phrased_question: string;
  /** Expected response data type */
  data_type?: string;
  /** Whether question is required */
  is_required?: boolean;
  /** Multiple choice options */
  options?: string[];
  /** Scoring criteria */
  scoring_rubric?: string;
}

// === UTILITY TYPES ===

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

export interface AbandonResponse {
  /** Operation status */
  status: string;
  /** Confirmation message */
  message: string;
}

// === API CLIENT TYPES ===

export interface ApiResponse<T> {
  data?: T;
  error?: ErrorResponse;
  success: boolean;
}

export interface SurveyApiClient {
  startSession(request: StartSessionRequest): Promise<ApiResponse<StartSessionResponse>>;
  submitResponses(request: SubmitResponsesRequest): Promise<ApiResponse<StepResponse>>;
  abandonSession(request: AbandonSessionRequest): Promise<ApiResponse<AbandonResponse>>;
  getSessionStatus(sessionId: string): Promise<ApiResponse<SessionStatusResponse>>;
}


// === FRONTEND HELPERS ===

export interface FormState {
  sessionId: string | null;
  currentStep: number;
  completed: boolean;
  questions: QuestionData[];
  responses: ResponseSubmission[];
  leadStatus: LeadStatus;
  abandonment_status: AbandonmentStatus;
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

// === API ENDPOINTS ===

export const API_ENDPOINTS = {
  // Survey API
  START_SESSION: '/api/survey/start',
  SUBMIT_RESPONSES: '/api/survey/step',
  ABANDON_SESSION: '/api/survey/abandon',
  SESSION_STATUS: '/api/survey/status',

} as const;

