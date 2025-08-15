/**
 * API Configuration
 * 
 * Centralized configuration for API endpoints and settings.
 * Uses environment variables for different environments.
 */

export const API_CONFIG = {
  // Base URL for the backend API
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  
  // Timeout for API requests (in milliseconds)  
  TIMEOUT: 30000,
  
  // Request headers
  DEFAULT_HEADERS: {
    'Content-Type': 'application/json',
  },
} as const;

/**
 * Helper function to build full API URLs
 */
export function buildApiUrl(endpoint: string): string {
  // Remove leading slash if present to avoid double slashes
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  return `${API_CONFIG.BASE_URL}/${cleanEndpoint}`;
}

/**
 * API Endpoints
 */
export const API_ENDPOINTS = {
  // Client/Business endpoints
  CLIENTS: {
    ME: buildApiUrl('/api/clients/me'),
    BY_ID: (id: string) => buildApiUrl(`/api/clients/${id}`),
  },
  
  // Forms endpoints
  FORMS: {
    LIST: (params?: URLSearchParams) => buildApiUrl(`/api/forms${params ? `?${params}` : ''}`),
    BY_ID: (id: string) => buildApiUrl(`/api/forms/${id}`),
    CREATE: buildApiUrl('/api/forms'),
    UPDATE: (id: string) => buildApiUrl(`/api/forms/${id}`),
    DELETE: (id: string) => buildApiUrl(`/api/forms/${id}`),
    BULK_UPDATE: buildApiUrl('/api/forms/bulk-update'),
    BULK_DELETE: buildApiUrl('/api/forms/bulk-delete'),
  },
  
  // Analytics endpoints (for future use)
  ANALYTICS: {
    DASHBOARD: buildApiUrl('/api/analytics/dashboard'),
    FORMS: (id: string) => buildApiUrl(`/api/analytics/forms/${id}`),
  },
} as const;