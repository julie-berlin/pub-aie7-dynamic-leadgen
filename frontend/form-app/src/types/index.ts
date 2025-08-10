// Form configuration and question types
export interface FormConfig {
  id: string;
  clientId: string;
  title: string;
  description?: string;
  questions: Question[];
  theme?: ThemeConfig;
  settings: FormSettings;
}

export interface Question {
  id: string;
  type: QuestionType;
  text: string;
  description?: string;
  required: boolean;
  options?: QuestionOption[];
  validation?: ValidationRule[];
  conditional?: ConditionalRule;
  metadata?: Record<string, any>;
}

export type QuestionType = 
  | 'text' 
  | 'textarea' 
  | 'email' 
  | 'phone'
  | 'number'
  | 'radio' 
  | 'checkbox' 
  | 'select'
  | 'multiselect'
  | 'rating'
  | 'date'
  | 'time'
  | 'file';

export interface QuestionOption {
  id: string;
  text: string;
  value: string;
  description?: string;
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
  };
  borderRadius: string;
  borderRadiusLg: string;
  shadow: string;
  shadowLg: string;
}

// Form state and responses
export interface FormState {
  formId: string;
  clientId: string;
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

// API response types
export interface StartSessionResponse {
  sessionId: string;
  form: FormConfig;
  step: FormStep;
}

export interface FormStep {
  stepNumber: number;
  totalSteps: number;
  questions: Question[];
  canGoBack: boolean;
  isComplete: boolean;
  metadata?: Record<string, any>;
}

export interface SubmitResponseRequest {
  sessionId: string;
  responses: Record<string, any>;
  currentStep: number;
  timestamp: string;
}

export interface SubmitResponseResponse {
  success: boolean;
  nextStep?: FormStep;
  isComplete?: boolean;
  completionData?: CompletionData;
  errors?: ValidationError[];
}

export interface CompletionData {
  leadStatus: 'yes' | 'no' | 'maybe';
  score: number;
  message: string;
  redirectUrl?: string;
  nextSteps?: string[];
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
  loading: boolean;
  error: string | null;

  // Actions
  initializeForm: (clientId: string, formId: string, trackingData?: Partial<TrackingData>) => Promise<void>;
  submitResponses: (responses: Record<string, any>) => Promise<void>;
  goToStep: (step: number) => Promise<void>;
  updateTheme: (theme: ThemeConfig) => void;
  saveProgress: () => Promise<void>;
  clearForm: () => void;
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
  clientId: string;
  formId: string;
  step?: number;
  sessionId?: string;
}