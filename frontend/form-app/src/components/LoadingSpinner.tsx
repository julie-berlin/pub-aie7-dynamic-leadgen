
interface LoadingSpinnerProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
}

export default function LoadingSpinner({ message = 'Loading...', size = 'md' }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  const textSizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg'
  };

  return (
    <div className="flex flex-col items-center justify-center space-y-6">
      {/* Modern pulse dots animation */}
      <div className="flex space-x-1">
        <div className={`${size === 'sm' ? 'w-2 h-2' : size === 'md' ? 'w-3 h-3' : 'w-4 h-4'} bg-primary rounded-full animate-pulse`} style={{animationDelay: '0ms', animationDuration: '1s'}}></div>
        <div className={`${size === 'sm' ? 'w-2 h-2' : size === 'md' ? 'w-3 h-3' : 'w-4 h-4'} bg-primary rounded-full animate-pulse`} style={{animationDelay: '150ms', animationDuration: '1s'}}></div>
        <div className={`${size === 'sm' ? 'w-2 h-2' : size === 'md' ? 'w-3 h-3' : 'w-4 h-4'} bg-primary rounded-full animate-pulse`} style={{animationDelay: '300ms', animationDuration: '1s'}}></div>
      </div>
      
      {/* Animated spinner as backup */}
      <div className={`${sizeClasses[size]} relative`}>
        <div className="absolute inset-0 border-4 border-border rounded-full"></div>
        <div className={`absolute inset-0 border-4 border-transparent border-t-primary rounded-full animate-spin`} style={{animationDuration: '1s'}}></div>
      </div>
      
      {message && (
        <p className={`text-text-light ${textSizeClasses[size]} font-medium`}>
          {message}
        </p>
      )}
    </div>
  );
}