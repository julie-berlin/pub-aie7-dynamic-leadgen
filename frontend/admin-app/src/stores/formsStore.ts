import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { API_ENDPOINTS } from '../config/api';

// Form interface for admin management
export interface AdminForm {
  id: string;
  clientId: string;
  title: string;
  description?: string;
  status: 'draft' | 'active' | 'paused' | 'archived';
  createdAt: string;
  updatedAt: string;
  totalResponses: number;
  conversionRate: number;
  averageCompletionTime: number;
  tags: string[];
  settings: {
    maxResponses?: number;
    expiresAt?: string;
    requireAuth: boolean;
    allowMultipleSubmissions: boolean;
  };
  theme?: {
    primaryColor: string;
    fontFamily: string;
    borderRadius: string;
  };
}

// Forms list state
interface FormsState {
  forms: AdminForm[];
  selectedForm: AdminForm | null;
  isLoading: boolean;
  error: string | null;
  
  // Filtering and sorting
  filters: {
    status: string[];
    tags: string[];
    dateRange: { start?: string; end?: string };
    search: string;
  };
  sortBy: 'createdAt' | 'updatedAt' | 'title' | 'responses' | 'conversionRate';
  sortOrder: 'asc' | 'desc';
  
  // Pagination
  currentPage: number;
  pageSize: number;
  totalCount: number;
}

// Forms actions
interface FormsActions {
  // Data fetching
  fetchForms: () => Promise<void>;
  fetchForm: (id: string) => Promise<void>;
  
  // Form management
  createForm: (form: Partial<AdminForm>) => Promise<AdminForm>;
  updateForm: (id: string, updates: Partial<AdminForm>) => Promise<void>;
  deleteForm: (id: string) => Promise<void>;
  duplicateForm: (id: string, newTitle?: string) => Promise<AdminForm>;
  
  // Bulk operations
  bulkUpdateStatus: (formIds: string[], status: AdminForm['status']) => Promise<void>;
  bulkDelete: (formIds: string[]) => Promise<void>;
  
  // UI state management
  setSelectedForm: (form: AdminForm | null) => void;
  setFilters: (filters: Partial<FormsState['filters']>) => void;
  setSorting: (sortBy: FormsState['sortBy'], sortOrder: FormsState['sortOrder']) => void;
  setPagination: (page: number, pageSize?: number) => void;
  clearFilters: () => void;
  
  // Error handling
  setError: (error: string | null) => void;
  setLoading: (loading: boolean) => void;
}

export interface FormsStore extends FormsState, FormsActions {}

// Create forms management store
export const useFormsStore = create<FormsStore>()(
  persist(
    (set, get) => ({
      // Initial state
      forms: [],
      selectedForm: null,
      isLoading: false,
      error: null,
      
      // Filters and sorting
      filters: {
        status: [],
        tags: [],
        dateRange: {},
        search: '',
      },
      sortBy: 'updatedAt',
      sortOrder: 'desc',
      
      // Pagination
      currentPage: 1,
      pageSize: 20,
      totalCount: 0,

      // Data fetching actions
      fetchForms: async () => {
        set({ isLoading: true, error: null });
        
        try {
          const { filters, sortBy, sortOrder, currentPage, pageSize } = get();
          
          // Build query parameters
          const params = new URLSearchParams({
            page: currentPage.toString(),
            limit: pageSize.toString(),
            sortBy,
            sortOrder,
            search: filters.search,
          });
          
          // Add array filters
          filters.status.forEach(status => params.append('status[]', status));
          filters.tags.forEach(tag => params.append('tags[]', tag));
          
          if (filters.dateRange.start) params.set('startDate', filters.dateRange.start);
          if (filters.dateRange.end) params.set('endDate', filters.dateRange.end);
          
          const token = localStorage.getItem('admin_token');
          const response = await fetch(API_ENDPOINTS.FORMS.LIST(params), {
            headers: { 
              'Content-Type': 'application/json',
              ...(token && { 'Authorization': `Bearer ${token}` })
            },
          });
          
          if (!response.ok) {
            throw new Error('Failed to fetch forms');
          }
          
          const { data } = await response.json();
          const rawForms = Array.isArray(data) ? data : data.forms || [];
          
          // Transform backend response (snake_case) to frontend format (camelCase)
          const forms = rawForms.map((form: any): AdminForm => ({
            id: form.id,
            clientId: form.client_id,
            title: form.title,
            description: form.description,
            status: form.status,
            createdAt: form.created_at,
            updatedAt: form.updated_at,
            totalResponses: form.total_responses || 0,
            conversionRate: form.conversion_rate || 0,
            averageCompletionTime: form.average_completion_time || 0,
            tags: form.tags || [],
            settings: {
              maxResponses: form.max_responses,
              expiresAt: form.expires_at,
              requireAuth: form.require_auth || false,
              allowMultipleSubmissions: form.allow_multiple_submissions || false,
            },
            theme: form.theme_config ? {
              primaryColor: form.theme_config.primary_color || '#3B82F6',
              fontFamily: form.theme_config.font_family || 'Inter',
              borderRadius: form.theme_config.border_radius || '0.5rem',
            } : undefined,
          }));
          
          const totalCount = data.total_count || data.totalCount || data.total || forms.length;
          
          set({ 
            forms, 
            totalCount, 
            isLoading: false,
            error: null 
          });
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Failed to fetch forms',
            isLoading: false 
          });
        }
      },

      fetchForm: async (id: string) => {
        set({ isLoading: true, error: null });
        
        try {
          const token = localStorage.getItem('admin_token');
          const response = await fetch(API_ENDPOINTS.FORMS.BY_ID(id), {
            headers: { 
              'Content-Type': 'application/json',
              ...(token && { 'Authorization': `Bearer ${token}` })
            },
          });
          
          if (!response.ok) {
            throw new Error('Failed to fetch form');
          }
          
          const { data: rawForm } = await response.json();
          
          // Transform backend response (snake_case) to frontend format (camelCase)
          const form: AdminForm = {
            id: rawForm.id,
            clientId: rawForm.client_id,
            title: rawForm.title,
            description: rawForm.description,
            status: rawForm.status,
            createdAt: rawForm.created_at,
            updatedAt: rawForm.updated_at,
            totalResponses: rawForm.total_responses || 0,
            conversionRate: rawForm.conversion_rate || 0,
            averageCompletionTime: rawForm.average_completion_time || 0,
            tags: rawForm.tags || [],
            settings: {
              maxResponses: rawForm.max_responses,
              expiresAt: rawForm.expires_at,
              requireAuth: rawForm.require_auth || false,
              allowMultipleSubmissions: rawForm.allow_multiple_submissions || false,
            },
            theme: rawForm.theme_config ? {
              primaryColor: rawForm.theme_config.primary_color || '#3B82F6',
              fontFamily: rawForm.theme_config.font_family || 'Inter',
              borderRadius: rawForm.theme_config.border_radius || '0.5rem',
            } : undefined,
          };
          
          set({ 
            selectedForm: form, 
            isLoading: false,
            error: null 
          });
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Failed to fetch form',
            isLoading: false 
          });
        }
      },

      // Form management actions
      createForm: async (formData: Partial<AdminForm>): Promise<AdminForm> => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await fetch(API_ENDPOINTS.FORMS.CREATE, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
          });
          
          if (!response.ok) {
            throw new Error('Failed to create form');
          }
          
          const { data: newForm } = await response.json();
          
          set(state => ({ 
            forms: [newForm, ...state.forms],
            totalCount: state.totalCount + 1,
            isLoading: false,
            error: null 
          }));
          
          return newForm;
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Failed to create form',
            isLoading: false 
          });
          throw error;
        }
      },

      updateForm: async (id: string, updates: Partial<AdminForm>) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await fetch(API_ENDPOINTS.FORMS.BY_ID(id), {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(updates),
          });
          
          if (!response.ok) {
            throw new Error('Failed to update form');
          }
          
          const { data: updatedForm } = await response.json();
          
          set(state => ({
            forms: state.forms.map(form => form.id === id ? updatedForm : form),
            selectedForm: state.selectedForm?.id === id ? updatedForm : state.selectedForm,
            isLoading: false,
            error: null 
          }));
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Failed to update form',
            isLoading: false 
          });
        }
      },

      deleteForm: async (id: string) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await fetch(API_ENDPOINTS.FORMS.BY_ID(id), {
            method: 'DELETE',
            headers: { 
              'Content-Type': 'application/json',
              ...(localStorage.getItem('admin_token') && { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` })
            },
          });
          
          if (!response.ok) {
            throw new Error('Failed to delete form');
          }
          
          set(state => ({
            forms: state.forms.filter(form => form.id !== id),
            selectedForm: state.selectedForm?.id === id ? null : state.selectedForm,
            totalCount: state.totalCount - 1,
            isLoading: false,
            error: null 
          }));
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Failed to delete form',
            isLoading: false 
          });
        }
      },

      duplicateForm: async (id: string, newTitle?: string): Promise<AdminForm> => {
        const originalForm = get().forms.find(form => form.id === id);
        if (!originalForm) {
          throw new Error('Form not found');
        }
        
        const duplicatedForm: Partial<AdminForm> = {
          ...originalForm,
          title: newTitle || `${originalForm.title} (Copy)`,
          status: 'draft',
        };
        
        // Remove fields that shouldn't be duplicated
        delete duplicatedForm.id;
        delete duplicatedForm.createdAt;
        delete duplicatedForm.updatedAt;
        delete duplicatedForm.totalResponses;
        delete duplicatedForm.conversionRate;
        delete duplicatedForm.averageCompletionTime;
        
        return get().createForm(duplicatedForm);
      },

      // Bulk operations
      bulkUpdateStatus: async (formIds: string[], status: AdminForm['status']) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await fetch(API_ENDPOINTS.FORMS.BULK_UPDATE, {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ formIds, updates: { status } }),
          });
          
          if (!response.ok) {
            throw new Error('Failed to bulk update forms');
          }
          
          set(state => ({
            forms: state.forms.map(form => 
              formIds.includes(form.id) ? { ...form, status } : form
            ),
            isLoading: false,
            error: null 
          }));
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Failed to bulk update forms',
            isLoading: false 
          });
        }
      },

      bulkDelete: async (formIds: string[]) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await fetch(API_ENDPOINTS.FORMS.BULK_DELETE, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ formIds }),
          });
          
          if (!response.ok) {
            throw new Error('Failed to bulk delete forms');
          }
          
          set(state => ({
            forms: state.forms.filter(form => !formIds.includes(form.id)),
            totalCount: state.totalCount - formIds.length,
            isLoading: false,
            error: null 
          }));
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Failed to bulk delete forms',
            isLoading: false 
          });
        }
      },

      // UI state management
      setSelectedForm: (form: AdminForm | null) => {
        set({ selectedForm: form });
      },

      setFilters: (newFilters: Partial<FormsState['filters']>) => {
        set(state => ({
          filters: { ...state.filters, ...newFilters },
          currentPage: 1, // Reset to first page when filters change
        }));
      },

      setSorting: (sortBy: FormsState['sortBy'], sortOrder: FormsState['sortOrder']) => {
        set({ sortBy, sortOrder, currentPage: 1 });
      },

      setPagination: (currentPage: number, pageSize?: number) => {
        set({ 
          currentPage, 
          ...(pageSize && { pageSize })
        });
      },

      clearFilters: () => {
        set({
          filters: {
            status: [],
            tags: [],
            dateRange: {},
            search: '',
          },
          currentPage: 1,
        });
      },

      setError: (error: string | null) => {
        set({ error });
      },

      setLoading: (isLoading: boolean) => {
        set({ isLoading });
      },
    }),
    {
      name: 'admin-forms-storage',
      storage: createJSONStorage(() => sessionStorage),
      // Only persist UI preferences, not data
      partialize: (state) => ({
        filters: state.filters,
        sortBy: state.sortBy,
        sortOrder: state.sortOrder,
        pageSize: state.pageSize,
      }),
    }
  )
);