// Form configuration and question types
export interface FormConfig {
  id: string;
  title: string;
  description?: string;
  businessName?: string;
  logoUrl?: string;
  questions: Question[];
  theme?: ThemeConfig;
  settings: FormSettings;
}

export interface Question {
  id: string;
  type: QuestionType;
  text: string;
  description?: string;
  placeholder?: string;
  required: boolean;
  options?: QuestionOptions;
  validation?: ValidationRule[];
  conditional?: ConditionalRule;
  metadata?: Record<string, any>;
}

export type QuestionType = 
  | 'text' 
  | 'textarea' 
  | 'email' 
  | 'phone'
  | 'tel'
  | 'number'
  | 'radio' 
  | 'checkbox' 
  | 'select'
  | 'multiselect'
  | 'rating'
  | 'date'
  | 'time'
  | 'datetime'
  | 'file';

export interface QuestionChoice {
  id: string;
  text: string;
  value: string;
  description?: string;
}

export interface QuestionOptions {
  // Choice options for radio, checkbox, select
  choices?: QuestionChoice[];
  
  // Rating options
  maxRating?: string;
  minRating?: string;
  ratingType?: 'stars' | 'numbers' | 'scale';
  ratingLabels?: { start?: string; end?: string; };
  
  // Date options
  minDate?: string;
  maxDate?: string;
  constraintType?: 'future' | 'past' | 'adult';
  helpText?: string;
  
  // File options
  allowedTypes?: string[];
  maxFileSize?: string;
  maxFiles?: string;
  
  // Text options
  rows?: string;
  
  // Other options
  placeholder?: string;
}

export interface ValidationRule {
  type: 'required' | 'minLength' | 'maxLength' | 'pattern' | 'min' | 'max';
  value?: any;
  message: string;
}

export interface ConditionalRule {
  dependsOn: string; // Question ID
  condition: 'equals' | 'contains' | 'greaterThan' | 'lessThan';
  value: any;
  action: 'show' | 'hide' | 'require';
}

export interface FormSettings {
  allowBack: boolean;
  showProgress: boolean;
  saveProgress: boolean;
  timeLimit?: number;
  redirectUrl?: string;
}

// Theme configuration
export interface ThemeConfig {
  name: string;
  colors: {
    primary: string;
    primaryHover: string;
    primaryLight: string;
    secondary: string;
    secondaryHover: string;
    secondaryLight: string;
    accent: string;
    text: string;
    textLight: string;
    textMuted: string;
    background: string;
    backgroundLight: string;
    border: string;
    error: string;
    success: string;
    warning: string;
  };
  typography: {
    primary: string;
    secondary: string;
  };
  spacing: {
    section: string;
    element: string;
    page: string;
    input: string;
    button: string;
  };
  borderRadius: string;
  borderRadiusLg: string;
  shadow: string;
  shadowLg: string;
  logo_url?: string;
  custom_css?: string;
}

// Form state and responses
export interface FormState {
  formId: string;
  sessionId: string;
  currentStep: number;
  totalSteps: number;
  responses: Record<string, FormResponse>;
  isComplete: boolean;
  startedAt: Date;
  lastUpdated: Date;
  metadata?: Record<string, any>;
}

export interface FormResponse {
  questionId: string;
  value: any;
  timestamp: Date;
  metadata?: Record<string, any>;
}

// API response types (following consistent format)
export interface ApiResponse<T = any> {
  success: boolean;
  data: T;
  message: string;
}

export interface StartSessionResponse {
  form: {
    id: string;
    title: string;
    description?: string;
    businessName?: string;
    logoUrl?: string;
    theme?: ThemeConfig;
    clientId?: string;  // Client ID for additional API calls (UUID, safe to expose)
  };
  step: FormStep;
}

export interface FormStep {
  stepNumber: number;
  totalSteps: number;
  questions: Question[];
  headline: string;
  subheading?: string;
  isComplete: boolean;
  canGoBack?: boolean;
  isLastStep?: boolean;
  metadata?: Record<string, any>;
}

export interface SubmitResponseRequest {
  responses: {
    question_id: string | number;  // Backend sends question_id, can be UUID string or number
    answer: any;
  }[];
}

export interface SubmitResponseResponse {
  nextStep?: FormStep;
  isComplete: boolean;
  completionData?: CompletionData;
}

export interface CompletionData {
  leadStatus: 'yes' | 'no' | 'maybe' | 'unknown';
  score: number;
  message: string;
  redirectUrl?: string;
  nextSteps: string[];
}

export interface ValidationError {
  questionId: string;
  field: string;
  message: string;
}

// Client and tracking data
export interface ClientInfo {
  id: string;
  name: string;
  industry?: string;
  branding?: {
    logo?: string;
    colors?: Partial<ThemeConfig['colors']>;
    fonts?: Partial<ThemeConfig['typography']>;
  };
}

export interface TrackingData {
  sessionId: string;
  utmSource?: string;
  utmMedium?: string;
  utmCampaign?: string;
  utmTerm?: string;
  utmContent?: string;
  referrer?: string;
  userAgent: string;
  timestamp: Date;
}

// Store interfaces
export interface FormStore {
  // State
  currentForm: FormConfig | null;
  formState: FormState | null;
  currentStep: FormStep | null;
  theme: ThemeConfig | null;
  completionData: CompletionData | null;
  loading: boolean;
  error: string | null;

  // Actions
  initializeForm: (formId: string, trackingData?: Partial<TrackingData>) => Promise<void>;
  submitStep: (stepNumber: number) => Promise<void>;
  submitResponses: (responses: Record<string, any>) => Promise<void>;
  goBack: () => Promise<void>;
  goToStep: (step: number) => Promise<void>;
  updateTheme: (theme: ThemeConfig) => void;
  saveProgress: () => Promise<void>;
  clearForm: () => void;
  clearCompletionData: () => void;
  setError: (error: string | null) => void;
  setLoading: (loading: boolean) => void;
}

export interface ThemeStore {
  // State
  currentTheme: ThemeConfig | null;
  defaultTheme: ThemeConfig;
  
  // Actions
  loadTheme: (formId: string) => Promise<void>;
  applyTheme: (theme: ThemeConfig) => void;
  validateTheme: (theme: ThemeConfig) => ThemeConfig;
  resetTheme: () => void;
}

// Utility types
export type FormStatus = 'loading' | 'ready' | 'submitting' | 'complete' | 'error';

export interface FormProgress {
  currentStep: number;
  totalSteps: number;
  percentage: number;
  completedSteps: number[];
}

// Navigation and routing
export interface FormRoute {
  formId: string;
  step?: number;
  sessionId?: string;
}