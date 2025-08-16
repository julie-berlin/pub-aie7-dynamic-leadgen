import SimpleLayout from '../components/SimpleLayout';

export default function NotFoundPage() {
  return (
    <SimpleLayout>
      <div className="flex items-center justify-center min-h-96">
        <div className="max-w-md text-center">
        <div className="text-8xl font-bold text-text-muted mb-4">
          404
        </div>
        
        <h1 className="text-2xl font-bold text-text mb-4">
          Page Not Found
        </h1>
        
        <p className="text-text-light mb-8">
          The form or page you're looking for doesn't exist or may have been moved.
        </p>
        
        <div className="space-y-3">
          <button
            onClick={() => window.history.back()}
            className="btn-primary w-full px-6 py-3 font-medium"
          >
            Go Back
          </button>
        </div>
        
        <div className="mt-8 text-sm text-text-muted">
          If you believe this is an error, please check the URL or contact support.
        </div>
        </div>
      </div>
    </SimpleLayout>
  );
}