import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { 
  FormStore, 
  FormState, 
  ThemeConfig, 
  TrackingData,
  SubmitResponseRequest,
  SubmitResponseResponse 
} from '../types';
import { apiClient } from '../utils/apiClient';

export const useFormStore = create<FormStore>()(
  persist(
    (set, get) => ({
      // Initial state
      currentForm: null,
      formState: null,
      currentStep: null,
      theme: null,
      loading: false,
      error: null,

      // Actions
      initializeForm: async (clientId: string, formId: string, trackingData?: Partial<TrackingData>) => {
        // Clear any stale state when initializing
        set({ 
          loading: true, 
          error: null,
          currentStep: null,  // Clear old step data
          formState: null     // Clear old form state
        });
        
        try {
          // Check if we have an existing session for this form
          const existingState = get().formState;

          // Note: Real session ID is managed by backend via HTTP-only cookies
          // Frontend state is separate from backend session management

          // Start or resume session
          const response = await apiClient.startSession({
            formId,
            clientId,
            trackingData: {
              ...trackingData
              // userAgent and timestamp are not supported by backend API
            }
          });

          // Note: Backend manages session via HTTP-only cookies, no frontend session ID needed
          // Frontend state tracks progress independently of backend session management
          
          const newFormState: FormState = {
            formId,
            clientId,
            sessionId: '', // Backend session managed via HTTP-only cookies
            currentStep: response.step.stepNumber,
            totalSteps: response.step.totalSteps,
            responses: existingState?.responses || {},
            isComplete: response.step.isComplete,
            startedAt: existingState?.startedAt || new Date(),
            lastUpdated: new Date()
          };

          set({
            currentForm: {
              id: response.form.id,
              clientId,
              title: response.form.title,
              description: response.form.description,
              businessName: response.form.businessName,
              logoUrl: response.form.logoUrl,
              questions: [], // Will be populated from steps
              theme: response.form.theme,
              settings: {
                allowBack: true,
                showProgress: true,
                saveProgress: true
              }
            },
            formState: newFormState,
            currentStep: response.step,
            theme: response.form.theme || null,
            loading: false,
            error: null
          });

          // Note: Theme loading is handled by the dedicated theme store

        } catch (error) {
          console.error('Failed to initialize form:', error);
          set({ 
            error: error instanceof Error ? error.message : 'Failed to load form',
            loading: false 
          });
        }
      },

      submitResponses: async (responses: Record<string, any>) => {
        const { formState, currentStep } = get();
        
        if (!formState || !currentStep) {
          set({ error: 'No active form session' });
          return;
        }

        set({ loading: true, error: null });

        try {
          // Convert responses to the expected API format
          // CRITICAL FIX: Backend expects numeric question IDs
          const apiResponses = Object.entries(responses).map(([questionId, value]) => ({
            question_id: parseInt(questionId, 10),  // Convert to number for backend
            answer: value
          }));

          const submitRequest: SubmitResponseRequest = {
            responses: apiResponses
          };

          const response: SubmitResponseResponse = await apiClient.submitResponses(submitRequest);

          // If we got new questions back, clear responses and only keep current step responses
          // This prevents old answers from persisting when question IDs are reused
          let updatedResponses: Record<string, any>;
          
          if (response.nextStep && response.nextStep.questions) {
            // New questions received - start fresh with only current responses
            updatedResponses = {};
            console.log('New questions received, clearing old responses');
          } else {
            // No new questions, keep existing responses
            updatedResponses = { ...formState.responses };
          }

          // Add the current submitted responses
          Object.entries(responses).forEach(([questionId, value]) => {
            updatedResponses[questionId] = {
              questionId,
              value,
              timestamp: new Date()
            };
          });

          const updatedFormState: FormState = {
            ...formState,
            responses: updatedResponses,
            currentStep: response.nextStep?.stepNumber || formState.currentStep,
            isComplete: response.isComplete,
            lastUpdated: new Date()
          };

          set({
            formState: updatedFormState,
            currentStep: response.nextStep || null,
            loading: false
          });

          // If form is complete, handle completion
          if (response.isComplete && response.completionData) {
            // Store completion data for the completion page (using form ID since session is cookie-managed)
            localStorage.setItem(
              `completion_${formState.formId}_${Date.now()}`, 
              JSON.stringify(response.completionData)
            );
          }

        } catch (error) {
          console.error('Failed to submit responses:', error);
          set({ 
            error: error instanceof Error ? error.message : 'Failed to submit responses',
            loading: false 
          });
        }
      },

      submitStep: async (stepNumber: number) => {
        // This is a convenience method that triggers form validation and submission
        const { currentStep } = get();
        
        if (!currentStep) {
          set({ error: 'No current step available' });
          return;
        }

        // For now, this will trigger React Hook Form validation
        // The actual submission will be handled by the form component
        console.log('Submitting step:', stepNumber);
      },

      goBack: async () => {
        const { formState, currentStep } = get();
        
        if (!formState || !currentStep || currentStep.stepNumber <= 1) {
          return;
        }

        await get().goToStep(currentStep.stepNumber - 1);
      },

      goToStep: async (step: number) => {
        // TODO: Implement step navigation when backend supports it
        console.warn('Step navigation not yet implemented');
        set({ error: 'Step navigation not yet supported' });
      },

      updateTheme: (theme: ThemeConfig) => {
        set({ theme });
        
        // Apply CSS custom properties
        const root = document.documentElement;
        Object.entries(theme.colors).forEach(([key, value]) => {
          const cssVar = key.replace(/([A-Z])/g, '-$1').toLowerCase();
          root.style.setProperty(`--color-${cssVar}`, value);
        });

        Object.entries(theme.typography).forEach(([key, value]) => {
          const cssVar = key.replace(/([A-Z])/g, '-$1').toLowerCase();
          root.style.setProperty(`--font-${cssVar}`, value);
        });

        root.style.setProperty('--spacing-section', theme.spacing.section);
        root.style.setProperty('--spacing-element', theme.spacing.element);
        root.style.setProperty('--border-radius', theme.borderRadius);
        root.style.setProperty('--border-radius-lg', theme.borderRadiusLg);
        root.style.setProperty('--shadow', theme.shadow);
        root.style.setProperty('--shadow-lg', theme.shadowLg);
      },

      saveProgress: async () => {
        const { formState } = get();
        
        if (!formState) return;

        try {
          await apiClient.saveProgress({
            responses: formState.responses,
            currentStep: formState.currentStep,
            lastUpdated: formState.lastUpdated.toISOString()
          });
        } catch (error) {
          console.error('Failed to save progress:', error);
          // Don't set error state for background saves
        }
      },

      clearForm: () => {
        set({
          currentForm: null,
          formState: null,
          currentStep: null,
          theme: null,
          loading: false,
          error: null
        });
        
        // Clear theme
        const root = document.documentElement;
        root.removeAttribute('style');
      },

      setError: (error: string | null) => {
        set({ error });
      },

      setLoading: (loading: boolean) => {
        set({ loading });
      }
    }),
    {
      name: 'form-storage',
      storage: createJSONStorage(() => localStorage),
      // Only persist minimal form state (no questions data)
      partialize: (state) => ({
        formState: state.formState ? {
          ...state.formState,
          // Don't persist responses to avoid stale data
          responses: {}
        } : null
        // Don't persist currentStep - always fetch fresh from backend
      }),
      // Skip hydration for sensitive data
      skipHydration: false,
    }
  )
);