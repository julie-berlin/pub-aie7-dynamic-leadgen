import { useLocation, useNavigate } from 'react-router-dom';
import SimpleLayout from '../components/SimpleLayout';

export default function ErrorPage() {
  const location = useLocation();
  const navigate = useNavigate();
  
  const error = location.state?.error || 'An unexpected error occurred';
  const message = location.state?.message || 'Please try again or contact support if the problem persists.';

  return (
    <SimpleLayout>
      <div className="flex items-center justify-center min-h-96">
        <div className="max-w-md text-center">
            {/* Error Icon */}
            <div 
              className="w-20 h-20 mx-auto mb-8 rounded-full flex items-center justify-center"
              style={{ backgroundColor: 'var(--color-error)' }}
            >
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            
            {/* Error Title */}
            <h1 
              className="text-3xl font-bold mb-4"
              style={{ color: 'var(--color-text)' }}
            >
              Oops! Something went wrong
            </h1>
            
            {/* Error Message */}
            <p 
              className="text-lg mb-8 leading-relaxed"
              style={{ color: 'var(--color-text-light)' }}
            >
              {message}
            </p>
            
            {/* Action Buttons */}
            <div className="space-y-4 mb-8">
              <button
                onClick={() => window.location.reload()}
                className="btn-primary w-full font-semibold flex items-center justify-center"
                style={{ padding: 'var(--spacing-button)' }}
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Try Again
              </button>
              
              <button
                onClick={() => navigate(-1)}
                className="btn-secondary w-full font-semibold flex items-center justify-center"
                style={{ padding: 'var(--spacing-button)' }}
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Go Back
              </button>
            </div>
            
            {/* Error Details */}
            <details className="text-left">
              <summary 
                className="cursor-pointer text-sm font-medium mb-2"
                style={{ color: 'var(--color-text-muted)' }}
              >
                Show technical details
              </summary>
              <div 
                className="text-xs p-3 rounded font-mono break-all"
                style={{ 
                  backgroundColor: 'var(--color-background-light)',
                  color: 'var(--color-text-muted)',
                  borderRadius: 'var(--border-radius)'
                }}
              >
                {error}
              </div>
            </details>
        </div>
      </div>
    </SimpleLayout>
  );
}