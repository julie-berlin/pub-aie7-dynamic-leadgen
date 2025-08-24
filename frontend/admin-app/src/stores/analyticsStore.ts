import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { API_CONFIG, buildApiUrl } from '../config/api';

// Helper function to get authenticated headers
const getAuthHeaders = () => {
  const token = localStorage.getItem('admin_token');
  if (!token) {
    throw new Error('No authentication token found');
  }
  return {
    ...API_CONFIG.DEFAULT_HEADERS,
    Authorization: `Bearer ${token}`
  };
};

// Retry logic removed - auth is now guaranteed to be ready before components render

// Analytics data interfaces
export interface DashboardMetrics {
  totalForms: number;
  activeForms: number;
  totalResponses: number;
  averageConversionRate: number;
  totalViews: number;
  responseRate: number;
  averageCompletionTime: number;
  topPerformingForm: {
    id: string;
    title: string;
    conversionRate: number;
  } | null;
}

export interface FormAnalytics {
  formId: string;
  formTitle: string;
  totalViews: number;
  totalResponses: number;
  conversionRate: number;
  averageCompletionTime: number;
  completionsByDay: Array<{
    date: string;
    views: number;
    responses: number;
    conversionRate: number;
  }>;
  questionAnalytics: Array<{
    questionId: string;
    questionText: string;
    responseRate: number;
    averageTimeSpent: number;
    abandonmentRate: number;
    commonResponses?: Array<{
      value: string;
      count: number;
      percentage: number;
    }>;
  }>;
  userJourney: Array<{
    step: number;
    questionId: string;
    questionText: string;
    completionRate: number;
    averageTimeSpent: number;
    dropOffRate: number;
  }>;
}

export interface RealTimeMetrics {
  activeUsers: number;
  activeForms: Array<{
    formId: string;
    formTitle: string;
    activeUsers: number;
    responsesInLastHour: number;
  }>;
  recentResponses: Array<{
    id: string;
    formId: string;
    formTitle: string;
    timestamp: string;
    location?: string;
    device: string;
    status: 'completed' | 'abandoned';
  }>;
  systemHealth: {
    status: 'healthy' | 'warning' | 'error';
    apiResponseTime: number;
    dbResponseTime: number;
    errorRate: number;
  };
}

// Date range interface
export interface DateRange {
  start: string;
  end: string;
  preset?: 'today' | 'yesterday' | 'last7days' | 'last30days' | 'last90days' | 'custom';
}

// Analytics state
interface AnalyticsState {
  // Dashboard metrics
  dashboardMetrics: DashboardMetrics | null;
  
  // Form-specific analytics
  formAnalytics: Record<string, FormAnalytics>;
  selectedFormAnalytics: FormAnalytics | null;
  
  // Real-time data
  realTimeMetrics: RealTimeMetrics | null;
  
  // Date range for analytics
  dateRange: DateRange;
  
  // UI state
  isLoading: boolean;
  error: string | null;
  lastUpdated: string | null;
  
  // Preferences
  autoRefresh: boolean;
  refreshInterval: number; // seconds
  selectedMetrics: string[];
}

// Analytics actions
interface AnalyticsActions {
  // Data fetching
  fetchDashboardMetrics: (dateRange?: DateRange) => Promise<void>;
  fetchFormAnalytics: (formId: string, dateRange?: DateRange) => Promise<void>;
  fetchRealTimeMetrics: () => Promise<void>;
  
  // Data management
  setDateRange: (dateRange: DateRange) => void;
  setSelectedFormAnalytics: (formId: string | null) => void;
  refreshData: () => Promise<void>;
  
  // Real-time updates
  startRealTimeUpdates: () => void;
  stopRealTimeUpdates: () => void;
  
  // Preferences
  setAutoRefresh: (enabled: boolean) => void;
  setRefreshInterval: (seconds: number) => void;
  setSelectedMetrics: (metrics: string[]) => void;
  
  // Export functionality
  exportAnalytics: (formId?: string, format?: 'csv' | 'xlsx' | 'pdf') => Promise<void>;
  
  // Error handling
  setError: (error: string | null) => void;
  setLoading: (loading: boolean) => void;
}

export interface AnalyticsStore extends AnalyticsState, AnalyticsActions {}

// Real-time update timer
let realTimeTimer: NodeJS.Timeout | null = null;

// Create analytics store
export const useAnalyticsStore = create<AnalyticsStore>()(
  persist(
    (set, get) => ({
      // Initial state
      dashboardMetrics: null,
      formAnalytics: {},
      selectedFormAnalytics: null,
      realTimeMetrics: null,
      
      // Default date range - last 30 days
      dateRange: {
        start: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        end: new Date().toISOString().split('T')[0],
        preset: 'last30days',
      },
      
      // UI state
      isLoading: false,
      error: null,
      lastUpdated: null,
      
      // Preferences
      autoRefresh: true,
      refreshInterval: 30, // 30 seconds
      selectedMetrics: ['totalResponses', 'conversionRate', 'averageCompletionTime'],

      // Data fetching actions
      fetchDashboardMetrics: async (customDateRange?: DateRange) => {
        set({ isLoading: true, error: null });
        
        try {
          const dateRange = customDateRange || get().dateRange;
          
          const params = new URLSearchParams({
            startDate: dateRange.start,
            endDate: dateRange.end,
          });
          
          const response = await fetch(buildApiUrl(`/api/analytics/dashboard?${params}`), {
            headers: getAuthHeaders(),
          });
          
          if (!response.ok) {
            throw new Error(`Failed to fetch dashboard metrics: ${response.status} ${response.statusText}`);
          }
          
          const { data: rawMetrics } = await response.json();
          
          // Transform backend response (snake_case) to frontend format (camelCase)
          const dashboardMetrics: DashboardMetrics = {
            totalForms: rawMetrics.total_forms || 0,
            activeForms: rawMetrics.active_forms || 0,
            totalResponses: rawMetrics.total_responses || 0,
            averageConversionRate: rawMetrics.average_conversion_rate || 0,
            totalViews: rawMetrics.total_views || 0,
            responseRate: rawMetrics.response_rate || 0,
            averageCompletionTime: rawMetrics.average_completion_time || 0,
            topPerformingForm: rawMetrics.top_performing_form ? {
              id: rawMetrics.top_performing_form.id,
              title: rawMetrics.top_performing_form.title,
              conversionRate: rawMetrics.top_performing_form.conversion_rate || 0
            } : null
          };
          
          set({ 
            dashboardMetrics,
            lastUpdated: new Date().toISOString(),
            isLoading: false,
            error: null 
          });
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Failed to fetch dashboard metrics',
            isLoading: false 
          });
        }
      },

      fetchFormAnalytics: async (formId: string, customDateRange?: DateRange) => {
        set({ isLoading: true, error: null });
        
        try {
          const dateRange = customDateRange || get().dateRange;
          
          const params = new URLSearchParams({
            startDate: dateRange.start,
            endDate: dateRange.end,
          });
          
          const response = await fetch(buildApiUrl(`/api/analytics/forms/${formId}?${params}`), {
            headers: getAuthHeaders(),
          });
          
          if (!response.ok) {
            throw new Error('Failed to fetch form analytics');
          }
          
          const { data: rawAnalytics } = await response.json();
          
          // Transform backend response (snake_case) to frontend format (camelCase)
          const formAnalytics: FormAnalytics = {
            formId: rawAnalytics.form_id || formId,
            formTitle: rawAnalytics.form_title || '',
            totalViews: rawAnalytics.total_views || 0,
            totalResponses: rawAnalytics.total_responses || 0,
            conversionRate: rawAnalytics.conversion_rate || 0,
            averageCompletionTime: rawAnalytics.average_completion_time || 0,
            completionsByDay: rawAnalytics.completions_by_day || [],
            questionAnalytics: rawAnalytics.question_analytics?.map((q: any) => ({
              questionId: q.question_id,
              questionText: q.question_text,
              responseRate: q.response_rate || 0,
              averageTimeSpent: q.average_time_spent || 0,
              abandonmentRate: q.abandonment_rate || 0,
              commonResponses: q.common_responses || []
            })) || [],
            userJourney: rawAnalytics.user_journey?.map((step: any) => ({
              step: step.step,
              questionId: step.question_id,
              questionText: step.question_text,
              completionRate: step.completion_rate || 0,
              averageTimeSpent: step.average_time_spent || 0,
              dropOffRate: step.drop_off_rate || 0
            })) || []
          };
          
          set(state => ({
            formAnalytics: {
              ...state.formAnalytics,
              [formId]: formAnalytics,
            },
            selectedFormAnalytics: formAnalytics,
            lastUpdated: new Date().toISOString(),
            isLoading: false,
            error: null 
          }));
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Failed to fetch form analytics',
            isLoading: false 
          });
        }
      },

      fetchRealTimeMetrics: async () => {
        set({ error: null });
        
        try {
          const response = await fetch(buildApiUrl('/api/analytics/realtime'), {
            headers: getAuthHeaders(),
          });
          
          if (!response.ok) {
            throw new Error(`Failed to fetch real-time metrics: ${response.status} ${response.statusText}`);
          }
          
          const { data: rawMetrics } = await response.json();
          
          // Transform backend response (snake_case) to frontend format (camelCase)
          const realTimeMetrics: RealTimeMetrics = {
            activeUsers: rawMetrics.active_users || 0,
            activeForms: rawMetrics.active_forms?.map((form: any) => ({
              formId: form.form_id,
              formTitle: form.form_title,
              activeUsers: form.active_users || 0,
              responsesInLastHour: form.responses_in_last_hour || 0
            })) || [],
            recentResponses: rawMetrics.recent_responses?.map((response: any) => ({
              id: response.id,
              formId: response.form_id,
              formTitle: response.form_title,
              timestamp: response.timestamp,
              location: response.location,
              device: response.device,
              status: response.status
            })) || [],
            systemHealth: {
              status: rawMetrics.system_health?.status || 'unknown',
              apiResponseTime: rawMetrics.system_health?.api_response_time || 0,
              dbResponseTime: rawMetrics.system_health?.db_response_time || 0,
              errorRate: rawMetrics.system_health?.error_rate || 0
            }
          };
          
          set({ 
            realTimeMetrics,
            lastUpdated: new Date().toISOString(),
          });
        } catch (error) {
          console.error('Failed to fetch real-time metrics:', error);
          // Don't set error state for real-time updates to avoid disrupting UI
        }
      },

      // Data management
      setDateRange: (dateRange: DateRange) => {
        set({ dateRange });
        
        // Refresh data with new date range
        get().refreshData();
      },

      setSelectedFormAnalytics: (formId: string | null) => {
        if (!formId) {
          set({ selectedFormAnalytics: null });
          return;
        }
        
        const formAnalytics = get().formAnalytics[formId];
        if (formAnalytics) {
          set({ selectedFormAnalytics: formAnalytics });
        } else {
          // Fetch analytics for this form
          get().fetchFormAnalytics(formId);
        }
      },

      refreshData: async () => {
        const { selectedFormAnalytics } = get();
        
        // Refresh dashboard metrics
        await get().fetchDashboardMetrics();
        
        // Refresh selected form analytics if any
        if (selectedFormAnalytics) {
          await get().fetchFormAnalytics(selectedFormAnalytics.formId);
        }
        
        // Refresh real-time metrics
        await get().fetchRealTimeMetrics();
      },

      // Real-time updates
      startRealTimeUpdates: () => {
        const { refreshInterval, autoRefresh } = get();
        
        if (!autoRefresh || realTimeTimer) return;
        
        realTimeTimer = setInterval(() => {
          get().fetchRealTimeMetrics();
        }, refreshInterval * 1000);
      },

      stopRealTimeUpdates: () => {
        if (realTimeTimer) {
          clearInterval(realTimeTimer);
          realTimeTimer = null;
        }
      },

      // Preferences
      setAutoRefresh: (autoRefresh: boolean) => {
        set({ autoRefresh });
        
        if (autoRefresh) {
          get().startRealTimeUpdates();
        } else {
          get().stopRealTimeUpdates();
        }
      },

      setRefreshInterval: (refreshInterval: number) => {
        set({ refreshInterval });
        
        // Restart real-time updates with new interval
        get().stopRealTimeUpdates();
        if (get().autoRefresh) {
          get().startRealTimeUpdates();
        }
      },

      setSelectedMetrics: (selectedMetrics: string[]) => {
        set({ selectedMetrics });
      },

      // Export functionality
      exportAnalytics: async (formId?: string, format: 'csv' | 'xlsx' | 'pdf' = 'csv') => {
        set({ isLoading: true, error: null });
        
        try {
          const { dateRange } = get();
          
          const params = new URLSearchParams({
            startDate: dateRange.start,
            endDate: dateRange.end,
            format,
            ...(formId && { formId }),
          });
          
          const response = await fetch(buildApiUrl(`/api/analytics/export?${params}`), {
            headers: getAuthHeaders(),
          });
          
          if (!response.ok) {
            throw new Error('Failed to export analytics');
          }
          
          // Download the file
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = `analytics-${formId || 'dashboard'}-${dateRange.start}-${dateRange.end}.${format}`;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          window.URL.revokeObjectURL(url);
          
          set({ isLoading: false });
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Failed to export analytics',
            isLoading: false 
          });
        }
      },

      // Error handling
      setError: (error: string | null) => {
        set({ error });
      },

      setLoading: (isLoading: boolean) => {
        set({ isLoading });
      },
    }),
    {
      name: 'admin-analytics-storage',
      storage: createJSONStorage(() => sessionStorage),
      // Only persist preferences and date range
      partialize: (state) => ({
        dateRange: state.dateRange,
        autoRefresh: state.autoRefresh,
        refreshInterval: state.refreshInterval,
        selectedMetrics: state.selectedMetrics,
      }),
    }
  )
);