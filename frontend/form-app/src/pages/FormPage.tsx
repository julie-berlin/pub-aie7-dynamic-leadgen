import { useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { useFormStore } from '../stores/formStore';
import { useThemeStore } from '../stores/themeStore';
import { extractUTMParams } from '../utils/sessionUtils';
import FormContainer from '../components/FormContainer';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

export default function FormPage() {
  const { clientId, formId } = useParams<{ clientId: string; formId: string }>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const {
    currentForm,
    formState,
    currentStep,
    loading,
    error,
    initializeForm
  } = useFormStore();

  // Business name from form data
  const businessName = currentForm?.businessName;
  const { loadTheme } = useThemeStore();

  useEffect(() => {
    if (!clientId || !formId) {
      navigate('/404');
      return;
    }

    // Extract tracking data from URL
    const trackingData = extractUTMParams();

    // Add session ID if resuming
    const sessionId = searchParams.get('session');

    if (sessionId) {
      trackingData.sessionId = sessionId;
    }

    // Initialize form
    initializeForm(clientId, formId, trackingData).catch(err => {
      console.error('Failed to initialize form:', err);
    });

    // Load theme separately with fallback (theme API is slow)
    loadTheme(formId).catch(err => {
      console.warn('Theme loading failed, using default:', err);
      // Theme store will automatically fall back to default theme
    });
  }, [clientId, formId, searchParams, initializeForm, loadTheme, navigate]);

  // Update page title with business name
  useEffect(() => {
    if (businessName) {
      document.title = `${businessName} - Hello!`;
    } else {
      document.title = 'Varyq';
    }
  }, [businessName]);

  // Redirect to completion page if form is complete
  useEffect(() => {
    if (formState?.isComplete) {
      navigate(`/form/${clientId}/${formId}/complete`, {
        state: { sessionId: formState.sessionId }
      });
    }
  }, [formState?.isComplete, clientId, formId, formState?.sessionId, navigate]);

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <ErrorMessage
          title="Form Not Available"
          message={error}
          showRetry
          onRetry={() => window.location.reload()}
        />
      </div>
    );
  }

  if (loading || !currentForm || !currentStep) {
    return (
      <div className="grid h-screen place-items-center max-w-2xl">
        <LoadingSpinner message="Loading..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-200 flex flex-col">
      {/* Header with Logo */}
      <header className="w-full">
        <div className="container mx-auto px-6 py-4 max-w-6xl">
          <div className="flex items-center justify-center">
            {/* Modern Logo */}
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div className="flex flex-col">
                {/* TODO add logo */}
                <span className="text-xl font-bold text-gray-900">
                  {businessName || 'Varyq'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content with theme-based padding */}
      <main className="flex-1 py-8 px-4">
        <div className="container mx-auto max-w-4xl">
          <div className="bg-white rounded-2xl" style={{ padding: 'var(--spacing-page)' }}>
            <FormContainer
              form={currentForm}
              currentStep={currentStep}
              formState={formState}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="w-full p-4 text-center" style={{ backgroundColor: 'var(--color-background-light)' }}>
        <div className="container mx-auto">
          <span className="text-sm" style={{ color: 'var(--color-text-muted)' }}>
            Varyq - Intelligent Leads
          </span>
        </div>
      </footer>
    </div>
  );
}
