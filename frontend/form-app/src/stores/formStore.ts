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
        set({ loading: true, error: null });
        
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
              ...trackingData,
              userAgent: navigator.userAgent,
              timestamp: new Date()
            }
          });

          // Generate a new session ID for frontend state (backend manages real session via cookies)
          const frontendSessionId = `frontend_${Date.now()}`;
          
          const newFormState: FormState = {
            formId,
            clientId,
            sessionId: frontendSessionId,
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
          const apiResponses = Object.entries(responses).map(([questionId, value]) => ({
            question_id: parseInt(questionId),
            answer: value
          }));

          const submitRequest: SubmitResponseRequest = {
            responses: apiResponses
          };

          const response: SubmitResponseResponse = await apiClient.submitResponses(submitRequest);

          // Update form state with new responses
          const updatedResponses = { ...formState.responses };
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
            // Store completion data for the completion page
            localStorage.setItem(
              `completion_${formState.sessionId}`, 
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
        const { formState } = get();
        
        if (!formState) {
          set({ error: 'No active form session' });
          return;
        }

        set({ loading: true, error: null });

        try {
          const response = await apiClient.getStep(formState.sessionId, step);
          
          set({
            currentStep: response,
            formState: {
              ...formState,
              currentStep: step,
              lastUpdated: new Date()
            },
            loading: false
          });

        } catch (error) {
          console.error('Failed to navigate to step:', error);
          set({ 
            error: error instanceof Error ? error.message : 'Failed to navigate',
            loading: false 
          });
        }
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
          await apiClient.saveProgress(formState.sessionId, {
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
      // Only persist form state and current step
      partialize: (state) => ({
        formState: state.formState,
        currentStep: state.currentStep
      }),
      // Skip hydration for sensitive data
      skipHydration: false,
    }
  )
);