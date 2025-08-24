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
  const { formId } = useParams<{ formId: string }>();
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

  // Business name and logo from persisted form data (loaded once, cached)
  const businessName = currentForm?.businessName;
  const logoUrl = currentForm?.logoUrl;
  const { loadTheme } = useThemeStore();

  useEffect(() => {
    if (!formId) {
      navigate('/404');
      return;
    }

    // Only initialize if we don't already have a form for this formId
    // This prevents unnecessary re-initialization during step transitions
    if (!currentForm || currentForm.id !== formId) {
      // Extract tracking data from URL
      const trackingData = extractUTMParams();

      // Add session ID if resuming
      const sessionId = searchParams.get('session');

      if (sessionId) {
        trackingData.sessionId = sessionId;
      }

      // Initialize form only when needed
      initializeForm(formId, trackingData).catch(err => {
        console.error('Failed to initialize form:', err);
      });
    }

    // Load theme with better error handling
    loadTheme(formId).then(() => {
      console.log('✅ Theme loaded successfully for form:', formId);
    }).catch(err => {
      console.warn('Theme loading failed, using default:', err);
    });
  }, [formId, searchParams, initializeForm, loadTheme, navigate, currentForm]);

  // Update page title with business name
  useEffect(() => {
    if (businessName) {
      document.title = `${businessName} - Hello!`;
    } else {
      document.title = 'Varyq';
    }
  }, [businessName]);

  // Navigate to completion page if form is complete (using React Router for SPA navigation)
  useEffect(() => {
    if (formState?.isComplete) {
      navigate(`/form/${formId}/complete`, {
        replace: true // Use replace to avoid back button issues
      });
    }
  }, [formState?.isComplete, formId, navigate]);

  if (error) {
    return (
      <PageLayout businessName="Varyq">
        <div className="flex items-center justify-center py-12 px-4">
          <ErrorMessage
            title="Form Not Available"
            message={error.includes('not found') ? 
              "Sorry, the form you're looking for doesn't exist or has been removed. Please check the link and try again." :
              error}
            showRetry
            onRetry={() => window.location.reload()}
          />
        </div>
      </PageLayout>
    );
  }

  if (loading || !currentForm || !currentStep) {
    return (
      <PageLayout businessName={businessName || "Loading..."} logoUrl={logoUrl}>
        <div className="flex items-center justify-center min-h-[400px]">
          <LoadingSpinner 
            message={businessName ? `Loading ${businessName}...` : "Loading form..."}
          />
        </div>
      </PageLayout>
    );
  }

  return (
    <PageLayout 
      businessName={businessName}
      logoUrl={logoUrl}
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
