import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

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
          const token = localStorage.getItem('admin_token');
          
          const params = new URLSearchParams({
            startDate: dateRange.start,
            endDate: dateRange.end,
          });
          
          // TODO: Replace with actual API endpoint
          const response = await fetch(`/api/admin/analytics/dashboard?${params}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          
          if (!response.ok) {
            throw new Error('Failed to fetch dashboard metrics');
          }
          
          const dashboardMetrics = await response.json();
          
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
          const token = localStorage.getItem('admin_token');
          
          const params = new URLSearchParams({
            startDate: dateRange.start,
            endDate: dateRange.end,
          });
          
          // TODO: Replace with actual API endpoint
          const response = await fetch(`/api/admin/analytics/forms/${formId}?${params}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          
          if (!response.ok) {
            throw new Error('Failed to fetch form analytics');
          }
          
          const formAnalytics = await response.json();
          
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
        try {
          const token = localStorage.getItem('admin_token');
          
          // TODO: Replace with actual API endpoint
          const response = await fetch('/api/admin/analytics/realtime', {
            headers: { Authorization: `Bearer ${token}` },
          });
          
          if (!response.ok) {
            throw new Error('Failed to fetch real-time metrics');
          }
          
          const realTimeMetrics = await response.json();
          
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
          const token = localStorage.getItem('admin_token');
          
          const params = new URLSearchParams({
            startDate: dateRange.start,
            endDate: dateRange.end,
            format,
            ...(formId && { formId }),
          });
          
          // TODO: Replace with actual API endpoint
          const response = await fetch(`/api/admin/analytics/export?${params}`, {
            headers: { Authorization: `Bearer ${token}` },
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