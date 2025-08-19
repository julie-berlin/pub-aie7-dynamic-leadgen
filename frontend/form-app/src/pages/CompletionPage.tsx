import { useEffect, useState } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import type { CompletionData } from '../types';
import PageLayout from '../components/PageLayout';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

export default function CompletionPage() {
  const { clientId, formId } = useParams<{ clientId: string; formId: string }>();
  const location = useLocation();
  const navigate = useNavigate();
  
  const [completionData, setCompletionData] = useState<CompletionData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!clientId || !formId) {
      navigate('/404');
      return;
    }

    // Get session ID from location state or localStorage
    const sessionId = location.state?.sessionId;
    
    if (!sessionId) {
      setError('No session found. Please start the form again.');
      setLoading(false);
      return;
    }

    // Load completion data from localStorage (stored by form store)
    try {
      const storedData = localStorage.getItem(`completion_${sessionId}`);
      if (storedData) {
        const data = JSON.parse(storedData);
        setCompletionData(data);
        // Clean up stored data
        localStorage.removeItem(`completion_${sessionId}`);
      } else {
        setError('Completion data not found.');
      }
    } catch (err) {
      setError('Failed to load completion data.');
    } finally {
      setLoading(false);
    }
  }, [clientId, formId, location.state, navigate]);

  // Redirect after a delay if specified
  useEffect(() => {
    if (completionData?.redirectUrl) {
      const timer = setTimeout(() => {
        window.location.href = completionData.redirectUrl!;
      }, 5000); // 5 second delay

      return () => clearTimeout(timer);
    }
  }, [completionData?.redirectUrl]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner message="Loading..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <ErrorMessage 
          title="Completion Error"
          message={error}
          showRetry
          onRetry={() => navigate(`/form/${clientId}/${formId}`)}
        />
      </div>
    );
  }

  return (
    <PageLayout businessName="Varyq">
      <div className="form-container max-w-2xl w-full mx-auto text-center">
        <div className="mb-8">
          {completionData?.leadStatus === 'yes' && (
            <div className="w-16 h-16 mx-auto mb-4 bg-success rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            </div>
          )}
          
          {completionData?.leadStatus === 'maybe' && (
            <div className="w-16 h-16 mx-auto mb-4 bg-warning rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
          )}
          
          {completionData?.leadStatus === 'no' && (
            <div className="w-16 h-16 mx-auto mb-4 bg-secondary rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
          )}
        </div>

        <h1 className="text-3xl font-bold text-text mb-6">
          Thank You!
        </h1>

        <div className="text-text-light text-lg mb-8">
          {completionData?.message || 'Your form has been submitted successfully.'}
        </div>

        {completionData?.nextSteps && completionData.nextSteps.length > 0 && (
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

        {completionData?.redirectUrl && (
          <div className="text-sm text-text-muted">
            You will be redirected automatically in a few seconds...
          </div>
        )}
      </div>
    </PageLayout>
  );
}