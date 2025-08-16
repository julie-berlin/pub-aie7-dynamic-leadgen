import { useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { useFormStore } from '../stores/formStore';
import { useThemeStore } from '../stores/themeStore';
import { extractUTMParams } from '../utils/sessionUtils';
import FormContainer from '../components/FormContainer';
import PageLayout from '../components/PageLayout';
import EngagementHeader from '../components/EngagementHeader';
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
    <PageLayout 
      businessName={businessName}
      // TODO: Add logoUrl prop when logo upload is implemented
    >
      {/* Engagement Content */}
      <EngagementHeader 
        form={currentForm}
        currentStep={currentStep}
      />
      
      {/* Form Inputs and Submission */}
      <FormContainer
        form={currentForm}
        currentStep={currentStep}
        formState={formState}
      />
    </PageLayout>
  );
}
