import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { API_ENDPOINTS, API_CONFIG, buildApiUrl } from '../config/api';

// Helper function to validate JWT token
const isTokenValid = (token: string): boolean => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const now = Date.now() / 1000;
    return payload.exp > now;
  } catch {
    return false;
  }
};

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
  isInitialized: boolean; // Track if auth check is complete
  isLoading: boolean;
  error: string | null;
  businessInfo: BusinessInfo;
}

// Auth actions interface
interface AuthActions {
  initializeAuth: () => Promise<void>;
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
      isInitialized: false,
      isLoading: false,
      error: null,
      businessInfo: {
        name: 'Survey Admin',
        industry: undefined,
        isLoaded: false
      },

      // Auth actions
      initializeAuth: async () => {
        try {
          const token = localStorage.getItem('admin_token');
          
          if (!token || !isTokenValid(token)) {
            // No token or invalid token - user not authenticated
            set({ 
              user: null,
              isAuthenticated: false,
              isInitialized: true,
              error: null 
            });
            return;
          }
          
          // Token exists and is valid - try to get user info
          const response = await fetch(buildApiUrl('/api/admin/auth/me'), {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          });
          
          if (response.ok) {
            const result = await response.json();
            // Use the standard API format response
            if (result.success && result.data) {
              const userData = result.data;
              const user: AdminUser = {
                id: userData.id,
                email: userData.email,
                name: `${userData.first_name} ${userData.last_name}`,
                role: userData.role as 'admin' | 'manager' | 'viewer',
                clientId: userData.client_id,
                permissions: userData.permissions || ['read', 'write', 'delete'],
                businessName: undefined // Will be loaded separately
              };
            
            set({ 
              user,
              isAuthenticated: true,
              isInitialized: true,
              error: null 
            });
            
              // Load business info
              get().loadBusinessInfo().catch(console.warn);
            } else {
              // Response format error
              localStorage.removeItem('admin_token');
              set({ 
                user: null,
                isAuthenticated: false,
                isInitialized: true,
                error: null 
              });
            }
          } else {
            // Token invalid or expired
            localStorage.removeItem('admin_token');
            set({ 
              user: null,
              isAuthenticated: false,
              isInitialized: true,
              error: null 
            });
          }
        } catch (error) {
          console.error('Auth initialization failed:', error);
          // On error, assume not authenticated but mark as initialized
          localStorage.removeItem('admin_token');
          set({ 
            user: null,
            isAuthenticated: false,
            isInitialized: true,
            error: null 
          });
        }
      },

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await fetch(buildApiUrl('/api/admin/auth/login'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
          });

          if (!response.ok) {
            throw new Error('Login failed');
          }

          const result = await response.json();
          
          // Backend now returns standard format: { success, data: { access_token, token_type, expires_in, user }, message }
          if (!result.success) {
            throw new Error(result.message || 'Login failed');
          }
          
          const { access_token, user } = result.data;
          
          // Store token in localStorage for API requests
          localStorage.setItem('admin_token', access_token);
          
          set({ 
            user, 
            isAuthenticated: true,
            isInitialized: true,
            isLoading: false,
            error: null 
          });
          
          // Load business info after successful login (non-blocking)
          get().loadBusinessInfo().catch(console.warn);
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
          isInitialized: true, // Keep initialized as true - we know the auth state
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
          const response = await fetch(buildApiUrl('/api/admin/auth/refresh'), {
            headers: { Authorization: `Bearer ${token}` },
          });

          if (!response.ok) {
            get().logout();
            return;
          }

          const result = await response.json();
          if (result.success && result.data) {
            const { access_token, user } = result.data;
            localStorage.setItem('admin_token', access_token);
            set({ user, isAuthenticated: true });
          } else {
            throw new Error(result.message || 'Token refresh failed');
          }
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
          if (!token) {
            set({ businessInfo: { name: 'Survey Admin', isLoaded: true } });
            return;
          }

          // For now, just set default business info since we have user info from login
          // TODO: Implement proper business info endpoint later
          set({
            businessInfo: {
              name: 'Survey Admin',
              industry: undefined,
              isLoaded: true
            }
          });
        } catch (error) {
          console.error('Failed to load business info:', error);
          set({ businessInfo: { name: 'Survey Admin', isLoaded: true } });
        }
      },
    }),
    {
      name: 'admin-auth-storage',
      storage: createJSONStorage(() => localStorage),
      // Only persist user data, not runtime state
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
        businessInfo: state.businessInfo,
        // Don't persist isInitialized - it should start false on each app load
      }),
    }
  )
);