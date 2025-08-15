/**
 * Auto-generated TypeScript types for Dynamic Survey Platform
 * Generated from Pydantic models
 * 
 * Last updated: 2025-08-15
 * 
 * DO NOT EDIT MANUALLY - This file is auto-generated
 * Run `python3 backend/generate_typescript_types.py` to update
 * 
 * Phase 2 Support: ✅ Included
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

// === THEME MANAGEMENT API TYPES ===

export interface ThemeColors {
  /** Primary brand color */
  primary: string;
  /** Primary color on hover */
  primaryHover: string;
  /** Light variant of primary */
  primaryLight: string;
  /** Secondary color */
  secondary: string;
  /** Secondary color on hover */
  secondaryHover: string;
  /** Light variant of secondary */
  secondaryLight: string;
  /** Accent color for highlights */
  accent: string;
  /** Primary text color */
  text: string;
  /** Light text color */
  textLight: string;
  /** Muted text color */
  textMuted: string;
  /** Main background color */
  background: string;
  /** Light background color */
  backgroundLight: string;
  /** Border color */
  border: string;
  /** Error state color */
  error: string;
  /** Success state color */
  success: string;
  /** Warning state color */
  warning: string;
}

export interface ThemeTypography {
  /** Primary font family */
  primary: string;
  /** Secondary font family */
  secondary: string;
}

export interface ThemeSpacing {
  /** Section spacing */
  section?: string;
  /** Element spacing */
  element?: string;
}

export interface ThemeConfig {
  /** Theme name */
  name: string;
  colors: any;
  typography: any;
  spacing: any;
  /** Default border radius */
  borderRadius?: string;
  /** Large border radius */
  borderRadiusLg?: string;
  /** Default shadow */
  shadow?: string;
  /** Large shadow */
  shadowLg?: string;
}

export interface ClientThemeRequest {
  /** Theme name */
  name: string;
  /** Theme description */
  description?: string;
  theme_config: any;
  /** Set as client default theme */
  is_default?: boolean;
}

export interface ClientThemeResponse {
  id: string;
  client_id: string?;
  name: string;
  description: string?;
  theme_config: any;
  is_default: boolean;
  is_system_theme: boolean;
  usage_count: number;
  last_used_at: string?;
  created_at: string;
  updated_at: string;
}

export interface FormDisplaySettings {
  /** Show progress bar */
  showProgress?: boolean;
  /** Allow back navigation */
  allowBack?: boolean;
  /** Auto-save form progress */
  saveProgress?: boolean;
  /** Time limit in minutes */
  timeLimit?: number;
  /** Redirect URL after completion */
  redirectUrl?: string;
}

export interface FormConfigRequest {
  /** Custom theme for this form */
  theme_config?: any;
  /** ID of existing theme to use */
  theme_id?: string;
  /** Display settings */
  display_settings?: any;
  /** Additional frontend metadata */
  frontend_metadata?: Record<string, any>;
}

export interface FormConfigResponse {
  id: string;
  client_id: string;
  title: string;
  description: string?;
  theme_config: any?;
  display_settings: any;
  frontend_metadata: Record<string, any>;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ThemeListResponse {
  themes: any[];
  total_count: number;
  system_themes_count: number;
}

// === ANALYTICS API TYPES ===

export interface EventTrackingRequest {
  session_id: string;
  event_type: "form_view" | "question_view" | "question_answer" | "form_submit" | "form_abandon" | "step_back" | "step_forward" | "field_focus" | "field_blur";
  event_category: "interaction" | "navigation" | "completion" | "error";
  event_action: "click" | "input" | "focus" | "blur" | "scroll" | "resize" | "submit";
  event_label?: string;
  event_value?: number;
  question_id?: number;
  step_number?: number;
  form_element?: string;
  viewport_size?: Record<string, number>;
  device_info?: Record<string, any>;
  interaction_data?: Record<string, any>;
  session_duration_ms?: number;
  step_duration_ms?: number;
  page_load_time_ms?: number;
  form_render_time_ms?: number;
}

export interface FormMetrics {
  total_views: number;
  unique_visitors: number;
  returning_visitors: number;
  total_starts: number;
  total_completions: number;
  completion_rate: number;
  avg_completion_time: number;
  median_completion_time: number;
  avg_questions_answered: number;
  bounce_rate: number;
  qualified_leads: number;
  unqualified_leads: number;
  maybe_leads: number;
  avg_lead_score: number;
}

export interface FormPerformanceResponse {
  form_id: string;
  metrics: any;
  step_dropout_rates: Record<string, number>;
  device_breakdown: Record<string, number>;
  traffic_sources: Record<string, number>;
  time_period: string;
  start_date: any;
  end_date: any;
}

export interface AnalyticsTimeSeriesData {
  date: any;
  value: number;
  label: string;
}

export interface FormAnalyticsDashboard {
  form_id: string;
  form_title: string;
  summary_metrics: any;
  performance_trend: any[];
  completion_funnel: Record<string, any>[];
  top_exit_questions: Record<string, any>[];
  device_analytics: Record<string, number>;
  traffic_analytics: Record<string, number>;
  lead_quality_breakdown: Record<string, number>;
  conversion_by_source: Record<string, any>[];
}

export interface EventAnalyticsResponse {
  total_events: number;
  events_by_type: Record<string, number>;
  events_by_category: Record<string, number>;
  events_timeline: any[];
  top_interactions: Record<string, any>[];
}

// === ADMIN MANAGEMENT API TYPES ===

export interface AdminUserRegister {
  email: string;
  /** Password must be at least 8 characters */
  password: string;
  first_name: string;
  last_name: string;
  /** Client organization ID */
  client_id: string;
  role?: "owner" | "admin" | "editor" | "viewer";
}

export interface AdminUserLogin {
  email: string;
  password: string;
}

export interface AdminUserResponse {
  id: string;
  client_id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  permissions: string[];
  is_active: boolean;
  email_verified: boolean;
  last_login_at: string?;
  login_count: number;
  created_at: string;
}

export interface AdminTokenResponse {
  access_token: string;
  token_type?: string;
  expires_in: number;
  user: any;
}

export interface ClientSettingsRequest {
  logo_url?: string;
  favicon_url?: string;
  brand_colors?: Record<string, string>;
  font_preferences?: Record<string, string>;
  default_theme_id?: string;
  default_form_settings?: Record<string, any>;
  custom_domain?: string;
  white_label_enabled?: boolean;
  from_email?: string;
  reply_to_email?: string;
  webhook_url?: string;
}

export interface ClientSettingsResponse {
  id: string;
  client_id: string;
  logo_url: string?;
  favicon_url: string?;
  brand_colors: Record<string, string>?;
  font_preferences: Record<string, string>?;
  default_theme_id: string?;
  default_form_settings: Record<string, any>;
  custom_domain: string?;
  custom_domain_verified: boolean;
  white_label_enabled: boolean;
  from_email: string?;
  reply_to_email: string?;
  webhook_url: string?;
  plan_type: string;
  monthly_form_limit: number;
  monthly_response_limit: number;
  created_at: string;
  updated_at: string;
}

export interface TeamInviteRequest {
  email: string;
  role: "admin" | "editor" | "viewer";
  first_name: string;
  last_name: string;
}

export interface TeamMemberResponse {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  is_active: boolean;
  last_login_at: string?;
  invitation_status: "pending" | "accepted" | "expired";
  created_at: string;
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


// === PHASE 2 API CLIENTS ===

export interface ThemeApiClient {
  getClientThemes(clientId: string, includeSystem?: boolean): Promise<ApiResponse<ThemeListResponse>>;
  createClientTheme(clientId: string, theme: ClientThemeRequest): Promise<ApiResponse<ClientThemeResponse>>;
  getTheme(themeId: string): Promise<ApiResponse<ClientThemeResponse>>;
  updateTheme(themeId: string, theme: ClientThemeRequest): Promise<ApiResponse<ClientThemeResponse>>;
  deleteTheme(themeId: string): Promise<ApiResponse<{status: string; message: string}>>;
  getFormConfig(formId: string): Promise<ApiResponse<FormConfigResponse>>;
  updateFormConfig(formId: string, config: FormConfigRequest): Promise<ApiResponse<FormConfigResponse>>;
  getFormTheme(formId: string): Promise<ApiResponse<ThemeConfig>>;
  getSystemThemes(): Promise<ApiResponse<ThemeListResponse>>;
}

export interface AnalyticsApiClient {
  trackEvent(event: EventTrackingRequest): Promise<ApiResponse<{status: string; message: string}>>;
  trackEventsBatch(events: EventTrackingRequest[]): Promise<ApiResponse<{status: string; processed: number}>>;
  getFormPerformance(formId: string, startDate?: string, endDate?: string, period?: 'daily' | 'weekly' | 'monthly'): Promise<ApiResponse<FormPerformanceResponse>>;
  getFormDashboard(formId: string, days?: number): Promise<ApiResponse<FormAnalyticsDashboard>>;
  getFormEvents(formId: string, days?: number, eventType?: string): Promise<ApiResponse<EventAnalyticsResponse>>;
  recalculateMetrics(formId: string): Promise<ApiResponse<{status: string; message: string}>>;
}

export interface AdminApiClient {
  register(user: AdminUserRegister): Promise<ApiResponse<AdminTokenResponse>>;
  login(credentials: AdminUserLogin): Promise<ApiResponse<AdminTokenResponse>>;
  getCurrentUser(): Promise<ApiResponse<AdminUserResponse>>;
  getClientSettings(): Promise<ApiResponse<ClientSettingsResponse>>;
  updateClientSettings(settings: ClientSettingsRequest): Promise<ApiResponse<ClientSettingsResponse>>;
  getTeamMembers(): Promise<ApiResponse<TeamMemberResponse[]>>;
  inviteTeamMember(invite: TeamInviteRequest): Promise<ApiResponse<TeamMemberResponse>>;
  removeTeamMember(userId: string): Promise<ApiResponse<{status: string; message: string}>>;
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

  
  // Theme API
  CLIENT_THEMES: '/api/themes/client',
  THEME_BY_ID: '/api/themes/theme',
  FORM_CONFIG: '/api/themes/form',
  SYSTEM_THEMES: '/api/themes/system',
  
  // Analytics API
  TRACK_EVENT: '/api/analytics/events/track',
  TRACK_BATCH: '/api/analytics/events/track/batch',
  FORM_PERFORMANCE: '/api/analytics/form',
  FORM_DASHBOARD: '/api/analytics/form',
  FORM_EVENTS: '/api/analytics/form',
  
  // Admin API
  ADMIN_REGISTER: '/api/admin/auth/register',
  ADMIN_LOGIN: '/api/admin/auth/login',
  ADMIN_ME: '/api/admin/auth/me',
  CLIENT_SETTINGS: '/api/admin/client/settings',
  TEAM_MEMBERS: '/api/admin/team/members',
  TEAM_INVITE: '/api/admin/team/invite',

} as const;

