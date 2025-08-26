import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useFormStore } from '../stores/formStore';
import { useThemeStore } from '../stores/themeStore';
import PageLayout from '../components/PageLayout';
import CompletionView from '../components/CompletionView';

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

  // Show completion view with proper theme support
  return (
    <PageLayout businessName={businessName} logoUrl={logoUrl}>
      <CompletionView 
        completionData={completionData || {
          leadStatus: 'unknown',
          score: 0,
          message: 'Your form has been submitted successfully.',
          nextSteps: []
        }}
        businessName={businessName}
      />
    </PageLayout>
  );
}