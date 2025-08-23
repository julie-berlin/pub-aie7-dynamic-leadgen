import { API_CONFIG } from '../config/api';

// Simplified theme interface for admin users
export interface SimpleTheme {
  name: string;
  description?: string;
  primary_color: string;    // Hex color: #3b82f6
  font_family: string;      // Font name: "Inter", "Arial", etc.
  logo_url?: string;        // Optional logo URL
  custom_css?: string;      // Optional advanced CSS
  is_default?: boolean;
}

// Backend theme response format
export interface ThemeResponse {
  id: string;
  client_id: string;
  name: string;
  description?: string;
  theme_config: any; // Full backend theme config
  primary_color: string;
  secondary_color: string;
  font_family: string;
  is_default: boolean;
  is_system_theme: boolean;
  created_at: string;
  updated_at: string;
}

// Standard API response format (following API_FORMAT_RULE.md)
interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string;
}

class ThemeService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_CONFIG.BASE_URL;
  }

  // Make authenticated request with proper error handling
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = localStorage.getItem('admin_token');
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    const url = `${this.baseUrl}${endpoint}`;
    console.log('themeService: Making request to:', url, 'with token:', !!token);

    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('themeService: Request failed:', response.status, response.statusText, errorText);
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const result: ApiResponse<T> = await response.json();
    console.log('themeService: API response:', result);
    
    if (!result.success) {
      throw new Error(result.message || 'API request failed');
    }

    return result.data;
  }

  // Generate full theme config from simple theme inputs
  private buildFullThemeConfig(simple: SimpleTheme) {
    // Helper functions for color variations
    const hexToRgb = (hex: string) => {
      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
      } : { r: 59, g: 130, b: 246 }; // fallback to blue
    };

    const darken = (hex: string, factor = 0.8) => {
      const { r, g, b } = hexToRgb(hex);
      const newR = Math.round(r * factor);
      const newG = Math.round(g * factor);
      const newB = Math.round(b * factor);
      return `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`;
    };

    const lighten = (hex: string, factor = 0.9) => {
      const { r, g, b } = hexToRgb(hex);
      const newR = Math.round(r + (255 - r) * factor);
      const newG = Math.round(g + (255 - g) * factor);
      const newB = Math.round(b + (255 - b) * factor);
      return `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`;
    };

    // Build complete theme config
    return {
      name: simple.name,
      colors: {
        primary: simple.primary_color,
        primaryHover: darken(simple.primary_color, 0.85),
        primaryLight: lighten(simple.primary_color, 0.85),
        secondary: '#6b7280',
        secondaryHover: '#4b5563',
        secondaryLight: '#f3f4f6',
        accent: '#10b981',
        text: '#111827',
        textLight: '#6b7280',
        textMuted: '#9ca3af',
        background: '#ffffff',
        backgroundLight: '#f9fafb',
        border: '#e5e7eb',
        error: '#ef4444',
        success: '#10b981',
        warning: '#f59e0b'
      },
      typography: {
        primary: `${simple.font_family}, sans-serif`,
        secondary: `${simple.font_family}, sans-serif`
      },
      spacing: {
        section: '2rem',
        element: '1rem',
      },
      borderRadius: '0.5rem',
      borderRadiusLg: '0.75rem',
      shadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
      shadowLg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
      ...(simple.logo_url && { logo_url: simple.logo_url }),
      ...(simple.custom_css && { custom_css: simple.custom_css })
    };
  }

  // Get all themes for authenticated client
  async getThemes(): Promise<ThemeResponse[]> {
    console.log('themeService: Getting themes from', `${this.baseUrl}/api/themes/`);
    const response = await this.request<{ themes: ThemeResponse[] }>('/api/themes/');
    console.log('themeService: Raw response:', response);
    return response.themes;
  }

  // Get specific theme by ID
  async getTheme(id: string): Promise<ThemeResponse> {
    return this.request<ThemeResponse>(`/api/themes/${id}`);
  }

  // Create new theme from simple inputs
  async createTheme(theme: SimpleTheme): Promise<ThemeResponse> {
    const fullThemeConfig = this.buildFullThemeConfig(theme);
    
    const payload = {
      name: theme.name,
      description: theme.description,
      theme_config: fullThemeConfig,
      primary_color: theme.primary_color,
      secondary_color: '#6b7280', // Default secondary
      font_family: theme.font_family,
      is_default: theme.is_default || false
    };

    return this.request<ThemeResponse>('/api/themes/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  // Update existing theme
  async updateTheme(id: string, theme: Partial<SimpleTheme>): Promise<ThemeResponse> {
    const payload: any = {};
    
    // Add simple fields
    if (theme.name) payload.name = theme.name;
    if (theme.description !== undefined) payload.description = theme.description;
    if (theme.is_default !== undefined) payload.is_default = theme.is_default;
    
    // Rebuild theme config if any theme properties changed
    if (theme.primary_color || theme.font_family || theme.logo_url || theme.custom_css) {
      // Get existing theme first to merge changes
      const existingTheme = await this.getTheme(id);
      const updatedSimpleTheme: SimpleTheme = {
        name: theme.name || existingTheme.name,
        description: theme.description !== undefined ? theme.description : existingTheme.description,
        primary_color: theme.primary_color || existingTheme.primary_color,
        font_family: theme.font_family || existingTheme.font_family,
        logo_url: theme.logo_url,
        custom_css: theme.custom_css
      };
      
      payload.theme_config = this.buildFullThemeConfig(updatedSimpleTheme);
      payload.primary_color = updatedSimpleTheme.primary_color;
      payload.font_family = updatedSimpleTheme.font_family;
    }

    return this.request<ThemeResponse>(`/api/themes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    });
  }

  // Delete theme
  async deleteTheme(id: string): Promise<void> {
    await this.request<void>(`/api/themes/${id}`, {
      method: 'DELETE',
    });
  }

  // Set theme as client default
  async setDefaultTheme(id: string): Promise<ThemeResponse> {
    return this.updateTheme(id, { is_default: true });
  }

  // Extract simple theme from backend response (for editing)
  extractSimpleTheme(themeResponse: ThemeResponse): SimpleTheme {
    return {
      name: themeResponse.name,
      description: themeResponse.description,
      primary_color: themeResponse.primary_color,
      font_family: themeResponse.font_family,
      logo_url: themeResponse.theme_config?.logo_url,
      custom_css: themeResponse.theme_config?.custom_css,
      is_default: themeResponse.is_default
    };
  }
}

export const themeService = new ThemeService();
export default themeService;