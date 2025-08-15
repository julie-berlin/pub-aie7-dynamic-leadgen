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

    // Initialize form and load theme concurrently
    Promise.all([
      initializeForm(clientId, formId, trackingData),
      loadTheme(formId)
    ]).catch(err => {
      console.error('Failed to initialize form or load theme:', err);
    });
  }, [clientId, formId, searchParams, initializeForm, loadTheme, navigate]);

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
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner message="Loading form..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <FormContainer 
          form={currentForm}
          currentStep={currentStep}
          formState={formState}
        />
      </div>
    </div>
  );
}