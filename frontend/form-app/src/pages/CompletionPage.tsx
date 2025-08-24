import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useFormStore } from '../stores/formStore';
import { useThemeStore } from '../stores/themeStore';
import PageLayout from '../components/PageLayout';

export default function CompletionPage() {
  const { formId } = useParams<{ formId: string }>();
  const navigate = useNavigate();
  
  // Get completion data and form info from store (read-only, no side effects)
  const completionData = useFormStore(state => state.completionData);
  const currentForm = useFormStore(state => state.currentForm);
  const { loadTheme } = useThemeStore();

  useEffect(() => {
    if (!formId) {
      navigate('/404');
      return;
    }

    // Load theme for branded experience (same as FormPage)
    loadTheme(formId).catch(err => {
      console.warn('Theme loading failed, using default:', err);
    });
  }, [formId, navigate, loadTheme]);

  // Get business name and logo for branded layout
  const businessName = currentForm?.businessName || "Varyq";
  const logoUrl = currentForm?.logoUrl;

  // If no completion data, show simple message with branding
  if (!completionData) {
    return (
      <PageLayout businessName={businessName} logoUrl={logoUrl}>
        <div className="form-container max-w-2xl w-full mx-auto text-center">
          <h1 className="text-3xl font-bold text-text mb-6">Thank You!</h1>
          <p className="text-text-light text-lg mb-4">Your form has been submitted successfully.</p>
        </div>
      </PageLayout>
    );
  }

  // Show completion data with full branding
  return (
    <PageLayout businessName={businessName} logoUrl={logoUrl}>
      <div className="form-container max-w-2xl w-full mx-auto text-center">
        <div className="mb-8">
          {completionData.leadStatus === 'yes' && (
            <div className="w-16 h-16 mx-auto mb-4 bg-green-500 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            </div>
          )}
          
          {completionData.leadStatus === 'maybe' && (
            <div className="w-16 h-16 mx-auto mb-4 bg-yellow-500 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
          )}
          
          {completionData.leadStatus === 'no' && (
            <div className="w-16 h-16 mx-auto mb-4 bg-gray-500 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
          )}
        </div>

        <h1 className="text-3xl font-bold text-text mb-6">Thank You!</h1>

        <div className="text-text-light text-lg mb-8">
          {completionData.message}
        </div>

        {completionData.nextSteps && completionData.nextSteps.length > 0 && (
          <div className="text-left mb-8">
            <h2 className="text-xl font-semibold text-text mb-4">Next Steps:</h2>
            <ul className="space-y-2">
              {completionData.nextSteps.map((step, index) => (
                <li key={index} className="flex items-start">
                  <span className="w-6 h-6 bg-primary text-white rounded-full flex items-center justify-center text-sm font-medium mr-3 mt-0.5">
                    {index + 1}
                  </span>
                  <span className="text-text-light">{step}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {completionData.redirectUrl && (
          <div className="text-sm text-text-muted">
            You will be redirected automatically in a few seconds...
          </div>
        )}
      </div>
    </PageLayout>
  );
}