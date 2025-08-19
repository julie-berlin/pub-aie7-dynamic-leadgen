import type { FormStep } from '../types';
import { useFormStore } from '../stores/formStore';

interface FormNavigationProps {
  currentStep: FormStep;
  canGoBack?: boolean;
  loading?: boolean;
}

export default function FormNavigation({ currentStep, canGoBack = false, loading = false }: FormNavigationProps) {
  const { goBack } = useFormStore();

  const handleBack = () => {
    if (canGoBack) {
      goBack();
    }
  };

  return (
    <div className="flex justify-between items-center pt-6 border-t border-border">
      {/* Back Button */}
      <div>
        {canGoBack ? (
          <button
            type="button"
            onClick={handleBack}
            disabled={loading}
            className="btn-secondary px-6 py-2 font-medium"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back
          </button>
        ) : (
          <div></div> // Spacer to maintain layout
        )}
      </div>

      {/* Step Indicator removed - dynamic surveys don't show progress */}
      <div></div>

      {/* Next/Submit Button */}
      <div>
        <button
          type="submit"
          disabled={loading}
          className={`px-6 py-2 font-medium btn-primary ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {loading && (
            <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          )}
          
          {currentStep.isLastStep ? (
            <>Submit</>
          ) : (
            <>
              Next
              <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </>
          )}
        </button>
      </div>
    </div>
  );
}