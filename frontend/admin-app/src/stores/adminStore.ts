import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { API_ENDPOINTS, API_CONFIG } from '../config/api';

// Admin user interface
export interface AdminUser {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'manager' | 'viewer';
  clientId: string;
  permissions: string[];
  avatar?: string;
  businessName?: string;
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
      // Initial auth state
      user: null,
      isAuthenticated: false,
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
          const response = await fetch(`${API_CONFIG.BASE_URL}/api/admin/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
          });

          if (!response.ok) {
            throw new Error('Login failed');
          }

          const data = await response.json();
          
          // Backend returns { access_token, token_type, expires_in, user }
          const { access_token, user } = data;
          
          // Store token in localStorage for API requests
          localStorage.setItem('admin_token', access_token);
          
          set({ 
            user, 
            isAuthenticated: true, 
            isLoading: false,
            error: null 
          });
          
          // Load business info after successful login
          await get().loadBusinessInfo();
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
          error: null,
          businessInfo: {
            name: 'Survey Admin',
            industry: undefined,
            isLoaded: false
          }
        });
      },

      refreshToken: async () => {
        const token = localStorage.getItem('admin_token');
        if (!token) return;

        try {
          const response = await fetch(`${API_CONFIG.BASE_URL}/api/admin/auth/refresh`, {
            headers: { Authorization: `Bearer ${token}` },
          });

          if (!response.ok) {
            get().logout();
            return;
          }

          const data = await response.json();
          const { access_token, user } = data;
          localStorage.setItem('admin_token', access_token);
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
          const token = localStorage.getItem('admin_token');
          const headers: Record<string, string> = {
            'Content-Type': 'application/json',
          };
          
          if (token) {
            headers['Authorization'] = `Bearer ${token}`;
          }
          
          const response = await fetch(API_ENDPOINTS.CLIENTS.ME, {
            headers
          });

          if (response.ok) {
            const result = await response.json();
            if (result.success && result.data) {
              set({
                businessInfo: {
                  name: result.data.name || 'Survey Admin',
                  industry: result.data.industry,
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