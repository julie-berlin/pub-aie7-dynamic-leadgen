import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

// Admin user interface
export interface AdminUser {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'manager' | 'viewer';
  clientId: string;
  permissions: string[];
  avatar?: string;
}

// Business info interface
export interface BusinessInfo {
  name: string;
  industry?: string;
  isLoaded: boolean;
}

// Auth state interface
interface AuthState {
  user: AdminUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  businessInfo: BusinessInfo;
}

// Auth actions interface
interface AuthActions {
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
  setUser: (user: AdminUser | null) => void;
  setError: (error: string | null) => void;
  setLoading: (loading: boolean) => void;
  loadBusinessInfo: () => Promise<void>;
}

// Admin store interface
export interface AdminStore extends AuthState, AuthActions {}

// Create admin store with authentication state
export const useAdminStore = create<AdminStore>()(
  persist(
    (set, get) => ({
      // Initial auth state - TEMPORARILY BYPASSING AUTH FOR DEVELOPMENT
      user: {
        id: "mock-admin-user-id",
        email: "admin@example.com",
        name: "Admin User",
        role: "admin",
        clientId: "a1111111-1111-1111-1111-111111111111",
        permissions: ["forms.view", "forms.edit", "settings.edit", "analytics.view"]
      },
      isAuthenticated: true,
      isLoading: false,
      error: null,
      businessInfo: {
        name: 'Survey Admin',
        industry: undefined,
        isLoaded: false
      },

      // Auth actions
      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        
        try {
          // TODO: Replace with actual API call
          const response = await fetch('/api/admin/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
          });

          if (!response.ok) {
            throw new Error('Login failed');
          }

          const { user, token } = await response.json();
          
          // Store token in localStorage for API requests
          localStorage.setItem('admin_token', token);
          
          set({ 
            user, 
            isAuthenticated: true, 
            isLoading: false,
            error: null 
          });
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Login failed',
            isLoading: false 
          });
        }
      },

      logout: () => {
        localStorage.removeItem('admin_token');
        set({ 
          user: null, 
          isAuthenticated: false, 
          error: null 
        });
      },

      refreshToken: async () => {
        const token = localStorage.getItem('admin_token');
        if (!token) return;

        try {
          // TODO: Replace with actual API call
          const response = await fetch('/api/admin/auth/refresh', {
            headers: { Authorization: `Bearer ${token}` },
          });

          if (!response.ok) {
            get().logout();
            return;
          }

          const { user, token: newToken } = await response.json();
          localStorage.setItem('admin_token', newToken);
          set({ user, isAuthenticated: true });
        } catch (error) {
          get().logout();
        }
      },

      setUser: (user: AdminUser | null) => {
        set({ user, isAuthenticated: !!user });
      },

      setError: (error: string | null) => {
        set({ error });
      },

      setLoading: (isLoading: boolean) => {
        set({ isLoading });
      },

      loadBusinessInfo: async () => {
        try {
          const response = await fetch('/api/clients/me', {
            headers: {
              'Content-Type': 'application/json',
            }
          });

          if (response.ok) {
            const { data } = await response.json();
            set({
              businessInfo: {
                name: data.business_name || data.name || 'Survey Admin',
                industry: data.industry,
                isLoaded: true
              }
            });
          } else {
            // Keep default name on error but mark as loaded
            set({
              businessInfo: {
                name: 'Survey Admin',
                industry: undefined,
                isLoaded: true
              }
            });
          }
        } catch (error) {
          console.error('Failed to load business info:', error);
          // Keep default name on error but mark as loaded
          set({
            businessInfo: {
              name: 'Survey Admin',
              industry: undefined,
              isLoaded: true
            }
          });
        }
      },
    }),
    {
      name: 'admin-auth-storage',
      storage: createJSONStorage(() => localStorage),
      // Only persist user data, not sensitive auth state
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
        businessInfo: state.businessInfo,
      }),
    }
  )
);