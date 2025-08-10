import { create } from 'zustand';
import type { ThemeStore, ThemeConfig } from '../types';
import { apiClient } from '../utils/apiClient';

// Default theme configuration
const defaultTheme: ThemeConfig = {
  name: 'default',
  colors: {
    primary: '#3b82f6',
    primaryHover: '#2563eb',
    primaryLight: '#dbeafe',
    secondary: '#6b7280',
    secondaryHover: '#4b5563',
    secondaryLight: '#f3f4f6',
    accent: '#f59e0b',
    text: '#111827',
    textLight: '#374151',
    textMuted: '#6b7280',
    background: '#ffffff',
    backgroundLight: '#f9fafb',
    border: '#d1d5db',
    error: '#ef4444',
    success: '#10b981',
    warning: '#f59e0b'
  },
  typography: {
    primary: "'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif",
    secondary: "'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
  },
  spacing: {
    section: '2rem',
    element: '1rem'
  },
  borderRadius: '0.5rem',
  borderRadiusLg: '0.75rem',
  shadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
  shadowLg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)'
};

export const useThemeStore = create<ThemeStore>((set, get) => ({
  // Initial state
  currentTheme: null,
  defaultTheme,

  // Actions
  loadTheme: async (formId: string) => {
    try {
      const theme = await apiClient.getTheme(formId);
      if (theme) {
        get().applyTheme(theme);
      } else {
        get().resetTheme();
      }
    } catch (error) {
      console.error('Failed to load theme:', error);
      // Fall back to default theme
      get().resetTheme();
    }
  },

  applyTheme: (theme: ThemeConfig) => {
    set({ currentTheme: theme });
    
    // Apply CSS custom properties to document root
    const root = document.documentElement;
    
    // Apply colors
    Object.entries(theme.colors).forEach(([key, value]) => {
      const cssVar = key.replace(/([A-Z])/g, '-$1').toLowerCase();
      root.style.setProperty(`--color-${cssVar}`, value);
    });

    // Apply typography
    Object.entries(theme.typography).forEach(([key, value]) => {
      const cssVar = key.replace(/([A-Z])/g, '-$1').toLowerCase();
      root.style.setProperty(`--font-${cssVar}`, value);
    });

    // Apply spacing
    root.style.setProperty('--spacing-section', theme.spacing.section);
    root.style.setProperty('--spacing-element', theme.spacing.element);

    // Apply border radius
    root.style.setProperty('--border-radius', theme.borderRadius);
    root.style.setProperty('--border-radius-lg', theme.borderRadiusLg);

    // Apply shadows
    root.style.setProperty('--shadow', theme.shadow);
    root.style.setProperty('--shadow-lg', theme.shadowLg);
  },

  resetTheme: () => {
    const { defaultTheme } = get();
    get().applyTheme(defaultTheme);
  }
}));