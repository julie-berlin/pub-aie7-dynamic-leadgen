
interface ErrorMessageProps {
  title: string;
  message: string;
  showRetry?: boolean;
  onRetry?: () => void;
}

export default function ErrorMessage({ 
  title, 
  message, 
  showRetry = false, 
  onRetry
}: ErrorMessageProps) {
  return (
    <div className="max-w-md mx-auto text-center p-8">
      {/* Simple Icon */}
      <div className="mb-6">
        <div className="w-12 h-12 mx-auto bg-gray-100 rounded-full flex items-center justify-center">
          <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
      </div>
      
      {/* Title */}
      <h1 className="text-xl font-bold text-gray-900 mb-3">
        {title}
      </h1>
      
      {/* Message */}
      <p className="text-gray-600 mb-8 leading-relaxed">
        {message}
      </p>
      
      {/* Actions */}
      <div className="space-y-3">
        {showRetry && onRetry && (
          <button
            onClick={onRetry}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            Try Again
          </button>
        )}
        
        <button
          onClick={() => window.history.back()}
          className="w-full bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded-lg transition-colors"
        >
          Go Back
        </button>
      </div>
    </div>
  );
}