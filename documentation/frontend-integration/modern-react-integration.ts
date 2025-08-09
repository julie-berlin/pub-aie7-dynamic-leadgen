/**
 * Modern React Integration for Survey API (2025)
 * 
 * Using TanStack Query + Zustand instead of hooks for better performance,
 * caching, and state management following 2025 best practices.
 */

import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
  StartSessionRequest,
  SubmitResponsesRequest,
  StartSessionResponse,
  StepResponse,
  SessionStatusResponse,
  ResponseSubmission,
  FormState,
  UTMParams,
  LeadStatus,
  AbandonmentStatus,
  ErrorResponse,
  LEAD_STATUS,
  ABANDONMENT_STATUS,
  API_ENDPOINTS
} from './typescript-types';

// === SURVEY STATE STORE (Zustand) ===

interface SurveyStore {
  // State
  formId: string | null;
  sessionId: string | null;
  currentStep: number;
  completed: boolean;
  questions: any[];
  responses: ResponseSubmission[];
  leadStatus: LeadStatus;
  abandonmentStatus: AbandonmentStatus;
  completionMessage?: string;
  utmParams: UTMParams;
  
  // Actions
  setFormId: (formId: string) => void;
  setSession: (response: StartSessionResponse) => void;
  updateStep: (response: StepResponse) => void;
  addResponses: (responses: ResponseSubmission[]) => void;
  setAbandonmentStatus: (status: AbandonmentStatus) => void;
  resetSurvey: () => void;
  
  // Utilities
  getProgress: () => { percentage: number; step: number; total: number };
  canSubmit: () => boolean;
}

export const useSurveyStore = create<SurveyStore>()(
  subscribeWithSelector(
    (set, get) => ({
      // Initial state
      formId: null,
      sessionId: null,
      currentStep: 0,
      completed: false,
      questions: [],
      responses: [],
      leadStatus: LEAD_STATUS.UNKNOWN,
      abandonmentStatus: ABANDONMENT_STATUS.ACTIVE,
      utmParams: {},

      // Actions
      setFormId: (formId: string) => set({ formId }),
      
      setSession: (response: StartSessionResponse) => set({
        sessionId: response.session_id,
        currentStep: response.step,
        completed: false,
        questions: response.questions,
        responses: [],
        leadStatus: LEAD_STATUS.UNKNOWN,
        abandonmentStatus: ABANDONMENT_STATUS.ACTIVE,
      }),
      
      updateStep: (response: StepResponse) => set(state => ({
        currentStep: response.step,
        completed: response.completed,
        questions: response.questions,
        completionMessage: response.completion_message,
      })),
      
      addResponses: (newResponses: ResponseSubmission[]) => set(state => ({
        responses: [...state.responses, ...newResponses],
      })),
      
      setAbandonmentStatus: (status: AbandonmentStatus) => set({ 
        abandonmentStatus: status 
      }),
      
      resetSurvey: () => set({
        sessionId: null,
        currentStep: 0,
        completed: false,
        questions: [],
        responses: [],
        leadStatus: LEAD_STATUS.UNKNOWN,
        abandonmentStatus: ABANDONMENT_STATUS.ACTIVE,
        completionMessage: undefined,
      }),
      
      // Utilities
      getProgress: () => {
        const state = get();
        const total = Math.max(4, state.currentStep + state.questions.length);
        return {
          percentage: Math.round((state.currentStep / total) * 100),
          step: state.currentStep,
          total,
        };
      },
      
      canSubmit: () => {
        const state = get();
        return state.sessionId && !state.completed && state.questions.length > 0;
      },
    })
  )
);

// === API CLIENT ===

class SurveyApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      credentials: 'include',
    };

    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP ${response.status}`);
    }

    return await response.json();
  }

  async startSession(request: StartSessionRequest): Promise<StartSessionResponse> {
    return this.request<StartSessionResponse>(API_ENDPOINTS.START_SESSION, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async submitResponses(request: SubmitResponsesRequest): Promise<StepResponse> {
    return this.request<StepResponse>(API_ENDPOINTS.SUBMIT_RESPONSES, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async abandonSession(sessionId: string, reason?: string): Promise<void> {
    return this.request<void>(API_ENDPOINTS.ABANDON_SESSION, {
      method: 'POST',
      body: JSON.stringify({ session_id: sessionId, reason }),
    });
  }

  async getSessionStatus(sessionId: string): Promise<SessionStatusResponse> {
    return this.request<SessionStatusResponse>(`${API_ENDPOINTS.SESSION_STATUS}/${sessionId}`);
  }
}

// Singleton API client
export const surveyApi = new SurveyApiClient(
  process.env.REACT_APP_API_URL || 'http://localhost:8000'
);

// === TANSTACK QUERY HOOKS ===

// Query keys factory
export const surveyKeys = {
  all: ['survey'] as const,
  sessions: () => [...surveyKeys.all, 'sessions'] as const,
  session: (sessionId: string) => [...surveyKeys.sessions(), sessionId] as const,
  status: (sessionId: string) => [...surveyKeys.session(sessionId), 'status'] as const,
};

// Start session mutation
export function useStartSession() {
  const queryClient = useQueryClient();
  const setSession = useSurveyStore(state => state.setSession);
  
  return useMutation({
    mutationFn: (request: StartSessionRequest) => surveyApi.startSession(request),
    onSuccess: (response) => {
      setSession(response);
      // Cache the session data
      queryClient.setQueryData(surveyKeys.session(response.session_id), response);
    },
    onError: (error) => {
      console.error('Failed to start session:', error);
    },
  });
}

// Submit responses mutation
export function useSubmitResponses() {
  const queryClient = useQueryClient();
  const updateStep = useSurveyStore(state => state.updateStep);
  const addResponses = useSurveyStore(state => state.addResponses);
  
  return useMutation({
    mutationFn: ({ sessionId, responses }: { sessionId: string; responses: ResponseSubmission[] }) =>
      surveyApi.submitResponses({ session_id: sessionId, responses }),
    onSuccess: (response, variables) => {
      updateStep(response);
      addResponses(variables.responses);
      // Update cached data
      queryClient.setQueryData(surveyKeys.session(variables.sessionId), response);
    },
    onError: (error) => {
      console.error('Failed to submit responses:', error);
    },
  });
}

// Session status query
export function useSessionStatus(sessionId: string | null, enabled: boolean = true) {
  return useQuery({
    queryKey: surveyKeys.status(sessionId || ''),
    queryFn: () => surveyApi.getSessionStatus(sessionId!),
    enabled: enabled && !!sessionId,
    staleTime: 30000, // 30 seconds
    refetchInterval: 60000, // Refetch every minute
  });
}

// Abandon session mutation
export function useAbandonSession() {
  const resetSurvey = useSurveyStore(state => state.resetSurvey);
  
  return useMutation({
    mutationFn: ({ sessionId, reason }: { sessionId: string; reason?: string }) =>
      surveyApi.abandonSession(sessionId, reason),
    onSuccess: () => {
      resetSurvey();
    },
  });
}

// === UTILITY FUNCTIONS ===

export const extractUTMFromURL = (): UTMParams => {
  if (typeof window === 'undefined') return {};
  
  const params = new URLSearchParams(window.location.search);
  return {
    utm_source: params.get('utm_source') || undefined,
    utm_medium: params.get('utm_medium') || undefined,
    utm_campaign: params.get('utm_campaign') || undefined,
    utm_content: params.get('utm_content') || undefined,
    utm_term: params.get('utm_term') || undefined,
  };
};

// Session persistence (using localStorage/sessionStorage)
export const persistSurveyState = () => {
  const state = useSurveyStore.getState();
  if (state.sessionId) {
    sessionStorage.setItem('survey_state', JSON.stringify({
      sessionId: state.sessionId,
      formId: state.formId,
      currentStep: state.currentStep,
      responses: state.responses,
    }));
  }
};

export const restoreSurveyState = () => {
  try {
    const stored = sessionStorage.getItem('survey_state');
    if (stored) {
      const data = JSON.parse(stored);
      // Restore partial state and refetch current status
      useSurveyStore.setState(prevState => ({
        ...prevState,
        sessionId: data.sessionId,
        formId: data.formId,
        currentStep: data.currentStep,
        responses: data.responses,
      }));
      return data.sessionId;
    }
  } catch (error) {
    console.warn('Failed to restore survey state:', error);
  }
  return null;
};

// === ABANDONMENT TRACKING ===

export class AbandonmentTracker {
  private timer: NodeJS.Timeout | null = null;
  private thresholdMs: number;
  
  constructor(thresholdMinutes: number = 5) {
    this.thresholdMs = thresholdMinutes * 60 * 1000;
  }

  start() {
    this.reset();
    this.timer = setTimeout(() => {
      useSurveyStore.getState().setAbandonmentStatus(ABANDONMENT_STATUS.AT_RISK);
    }, this.thresholdMs);
  }

  reset() {
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    useSurveyStore.getState().setAbandonmentStatus(ABANDONMENT_STATUS.ACTIVE);
  }

  stop() {
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
  }
}

export const abandonmentTracker = new AbandonmentTracker();

// === ANALYTICS INTEGRATION ===

export interface AnalyticsEvent {
  type: 'session_started' | 'step_completed' | 'response_submitted' | 'survey_completed' | 'survey_abandoned';
  sessionId: string;
  data?: Record<string, any>;
}

export class SurveyAnalytics {
  private events: AnalyticsEvent[] = [];
  
  track(event: AnalyticsEvent) {
    this.events.push({
      ...event,
      timestamp: new Date().toISOString(),
    });
    
    // Send to analytics service
    this.sendToAnalytics(event);
  }
  
  private async sendToAnalytics(event: AnalyticsEvent) {
    try {
      // Example: Send to Google Analytics 4
      if (typeof gtag !== 'undefined') {
        gtag('event', event.type, {
          session_id: event.sessionId,
          ...event.data,
        });
      }
      
      // Example: Send to custom analytics endpoint
      await fetch('/api/analytics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(event),
      });
    } catch (error) {
      console.warn('Analytics tracking failed:', error);
    }
  }
  
  getEvents(): AnalyticsEvent[] {
    return [...this.events];
  }
}

export const surveyAnalytics = new SurveyAnalytics();

// Auto-track store changes
useSurveyStore.subscribe(
  (state) => state.sessionId,
  (sessionId, prevSessionId) => {
    if (sessionId && !prevSessionId) {
      surveyAnalytics.track({
        type: 'session_started',
        sessionId,
      });
    }
  }
);

useSurveyStore.subscribe(
  (state) => state.completed,
  (completed, prevCompleted) => {
    const state = useSurveyStore.getState();
    if (completed && !prevCompleted && state.sessionId) {
      surveyAnalytics.track({
        type: 'survey_completed',
        sessionId: state.sessionId,
        data: {
          leadStatus: state.leadStatus,
          stepsCompleted: state.currentStep,
        },
      });
    }
  }
);