
interface ErrorMessageProps {
  title: string;
  message: string;
  showRetry?: boolean;
  onRetry?: () => void;
  type?: 'error' | 'warning' | 'info';
}

export default function ErrorMessage({ 
  title, 
  message, 
  showRetry = false, 
  onRetry, 
  type = 'error' 
}: ErrorMessageProps) {
  const iconColors = {
    error: 'bg-error',
    warning: 'bg-warning',
    info: 'bg-primary'
  };

  const getIcon = () => {
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