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
    <div className="flex justify-between items-center mt-12 pt-8">
      {/* Back Button */}
      <div>
        {canGoBack ? (
          <button
            type="button"
            onClick={handleBack}
            disabled={loading}
            className="btn-secondary font-semibold flex items-center transition-colors duration-200"
            style={{
              color: 'var(--color-text-light)',
              backgroundColor: 'var(--color-background-light)',
              borderRadius: 'var(--border-radius-lg)',
              border: '1px solid var(--color-border)',
            }}
            onMouseEnter={(e) => {
              if (!loading) {
                e.currentTarget.style.backgroundColor = 'var(--color-secondary-light)';
              }
            }}
            onMouseLeave={(e) => {
              if (!loading) {
                e.currentTarget.style.backgroundColor = 'var(--color-background-light)';
              }
            }}
          >
            <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back
          </button>
        ) : (
          <div></div>
        )}
      </div>

      {/* Next/Submit Button */}
      <div>
        <button
          type="submit"
          disabled={loading}
          className={`btn-primary text-lg font-semibold text-white flex items-center transition-all duration-200 ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
          style={{
            backgroundColor: 'var(--color-primary)',
            borderRadius: 'var(--border-radius-lg)',
            boxShadow: 'var(--shadow-lg)',
          }}
          onMouseEnter={(e) => {
            if (!loading) {
              e.currentTarget.style.backgroundColor = 'var(--color-primary-hover)';
            }
          }}
          onMouseLeave={(e) => {
            if (!loading) {
              e.currentTarget.style.backgroundColor = 'var(--color-primary)';
            }
          }}
        >
          {loading && (
            <div className="relative w-4 h-4 mr-3">
              <div className="absolute inset-0 border-2 border-white border-opacity-30 rounded-full"></div>
              <div className="absolute inset-0 border-2 border-transparent border-t-white rounded-full animate-spin"></div>
            </div>
          )}
          
          {currentStep.isLastStep ? (
            <>Submit</>
          ) : (
            <>
              Continue
              <svg className="w-5 h-5 ml-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </>
          )}
        </button>
      </div>
    </div>
  );
}