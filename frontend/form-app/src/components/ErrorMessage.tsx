
interface ErrorMessageProps {
  title: string;
  message: string;
  showRetry?: boolean;
  onRetry?: () => void;
  type?: 'error' | 'warning' | 'info';
  variant?: 'default' | 'form-unavailable';
  supportEmail?: string;
}

export default function ErrorMessage({ 
  title, 
  message, 
  showRetry = false, 
  onRetry, 
  type = 'error',
  variant = 'default',
  supportEmail = 'support@varyq.com'
}: ErrorMessageProps) {
  const iconColors = {
    error: 'bg-error',
    warning: 'bg-warning',
    info: 'bg-primary'
  };

  const getIcon = () => {
    if (variant === 'form-unavailable') {
      return (
        <svg className="text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24" width="24" height="24" style={{ width: '24px', height: '24px', minWidth: '24px', minHeight: '24px', maxWidth: '24px', maxHeight: '24px' }}>
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" 
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" 
                d="M6 18L18 6M6 6l12 12" className="text-error opacity-50" />
        </svg>
      );
    }

    switch (type) {
      case 'warning':
        return (
          <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        );
      case 'info':
        return (
          <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
        );
      default:
        return (
          <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        );
    }
  };

  if (variant === 'form-unavailable') {
    return (
      <div className="max-w-lg w-full mx-auto">
        {/* Main Error Card */}
        <div className="bg-background rounded-theme-lg shadow-theme-lg border border-border p-8 text-center">
          {/* Icon */}
          <div className="w-16 h-16 max-w-16 max-h-16 mx-auto mb-6 bg-background-light rounded-full flex items-center justify-center border-2 border-border flex-shrink-0">
            {getIcon()}
          </div>
          
          {/* Title */}
          <h1 className="text-2xl font-bold text-text mb-4">
            {title}
          </h1>
          
          {/* Message */}
          <p className="text-text-light text-lg leading-relaxed mb-8">
            {message}
          </p>
          
          {/* Action Buttons */}
          <div className="space-y-4">
            {showRetry && onRetry && (
              <button
                onClick={onRetry}
                className="w-full bg-primary hover:bg-primary-hover text-white font-semibold py-3 px-6 rounded-theme transition-colors duration-200 shadow-theme"
              >
                <svg className="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" 
                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Try Again
              </button>
            )}
            
            <button
              onClick={() => window.history.back()}
              className="w-full bg-secondary hover:bg-secondary-hover text-white font-medium py-3 px-6 rounded-theme transition-colors duration-200"
            >
              <svg className="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" 
                      d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Go Back
            </button>
          </div>
        </div>
        
        {/* Help Section */}
        <div className="mt-8 text-center">
          <p className="text-text-muted text-sm mb-4">
            Need help? Contact us for assistance.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <a
              href={`mailto:${supportEmail}?subject=Form Access Issue`}
              className="flex items-center text-primary hover:text-primary-hover transition-colors duration-200 font-medium text-sm"
            >
              <svg className="w-3 h-3 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" 
                      d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Email Support
            </a>
            
            <span className="text-text-muted hidden sm:inline">•</span>
            
            <button
              onClick={() => window.location.href = '/'}
              className="flex items-center text-secondary hover:text-secondary-hover transition-colors duration-200 font-medium text-sm"
            >
              <svg className="w-3 h-3 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" 
                      d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              Home Page
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Default variant (original implementation for other error types)
  return (
    <div className="form-container max-w-md w-full p-6 text-center">
      <div className={`w-12 h-12 mx-auto mb-4 ${iconColors[type]} rounded-full flex items-center justify-center`}>
        {getIcon()}
      </div>
      
      <h2 className="text-xl font-semibold text-text mb-3">
        {title}
      </h2>
      
      <p className="text-text-light mb-6">
        {message}
      </p>
      
      {showRetry && onRetry && (
        <button
          onClick={onRetry}
          className="btn-primary px-6 py-2 font-medium"
        >
          Try Again
        </button>
      )}
    </div>
  );
}