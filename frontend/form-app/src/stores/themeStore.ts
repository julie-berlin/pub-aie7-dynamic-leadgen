import { create } from 'zustand';
import { persist } from 'zustand/middleware';
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

// Theme cache for performance
const themeCache = new Map<string, { theme: ThemeConfig; timestamp: number }>();
const CACHE_DURATION = 10 * 60 * 1000; // 10 minutes

export const useThemeStore = create<ThemeStore>()(
  persist(
    (set, get) => ({
      // Initial state
      currentTheme: null,
      defaultTheme,

      // Actions
      loadTheme: async (formId: string) => {
        try {
          // Check cache first
          const cached = themeCache.get(formId);
          if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
            get().applyTheme(cached.theme);
            return;
          }

          const theme = await apiClient.getTheme(formId);
          if (theme) {
            // Validate and cache the theme
            const validatedTheme = get().validateTheme(theme);
            themeCache.set(formId, { theme: validatedTheme, timestamp: Date.now() });
            get().applyTheme(validatedTheme);
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
          console.log(`Set CSS var: --color-${cssVar} = ${value}`);
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
        console.log(`Set border radius: ${theme.borderRadius}, lg: ${theme.borderRadiusLg}`);

        // Apply shadows
        root.style.setProperty('--shadow', theme.shadow);
        root.style.setProperty('--shadow-lg', theme.shadowLg);
        
        console.log('✅ Applied theme:', theme.name);
        console.log('🎨 Primary color:', theme.colors.primary);
        console.log('🟠 Secondary color:', theme.colors.secondary);
      },

      validateTheme: (theme: ThemeConfig): ThemeConfig => {
        const { defaultTheme } = get();
        
        // Create a validated theme with fallbacks
        return {
          name: theme.name || defaultTheme.name,
          colors: { ...defaultTheme.colors, ...theme.colors },
          typography: { ...defaultTheme.typography, ...theme.typography },
          spacing: { ...defaultTheme.spacing, ...theme.spacing },
          borderRadius: theme.borderRadius || defaultTheme.borderRadius,
          borderRadiusLg: theme.borderRadiusLg || defaultTheme.borderRadiusLg,
          shadow: theme.shadow || defaultTheme.shadow,
          shadowLg: theme.shadowLg || defaultTheme.shadowLg
        };
      },

      resetTheme: () => {
        const { defaultTheme } = get();
        get().applyTheme(defaultTheme);
      }
    }),
    {
      name: 'theme-storage',
      partialize: (state) => ({ currentTheme: state.currentTheme }),
    }
  )
);