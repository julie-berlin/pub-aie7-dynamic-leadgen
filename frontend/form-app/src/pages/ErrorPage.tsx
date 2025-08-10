import { useLocation, useNavigate } from 'react-router-dom';

export default function ErrorPage() {
  const location = useLocation();
  const navigate = useNavigate();
  
  const error = location.state?.error || 'An unexpected error occurred';
  const message = location.state?.message || 'Please try again or contact support if the problem persists.';

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="form-container max-w-md w-full p-8 text-center">
        <div className="w-16 h-16 mx-auto mb-6 bg-error rounded-full flex items-center justify-center">
          <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        </div>
        
        <h1 className="text-2xl font-bold text-text mb-4">
          Something went wrong
        </h1>
        
        <p className="text-text-light mb-8">
          {message}
        </p>
        
        <div className="space-y-3">
          <button
            onClick={() => window.location.reload()}
            className="btn-primary w-full px-6 py-3 font-medium"
          >
            Try Again
          </button>
          
          <button
            onClick={() => navigate(-1)}
            className="btn-secondary w-full px-6 py-3 font-medium"
          >
            Go Back
          </button>
        </div>
        
        <div className="mt-8 text-sm text-text-muted">
          Error: {error}
        </div>
      </div>
    </div>
  );
}