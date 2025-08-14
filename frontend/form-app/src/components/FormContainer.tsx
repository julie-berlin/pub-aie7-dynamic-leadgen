import type { FormConfig, FormStep, FormState } from '../types';
import QuestionRenderer from './QuestionRenderer';
import FormNavigation from './FormNavigation';
import { useFormStore } from '../stores/formStore';
import { useForm } from 'react-hook-form';

interface FormContainerProps {
  form: FormConfig;
  currentStep: FormStep;
  formState: FormState | null;
}

export default function FormContainer({ form, currentStep, formState }: FormContainerProps) {
  const { loading, error, submitResponses } = useFormStore();

  // Initialize React Hook Form for this step
  const { handleSubmit } = useForm();

  if (!formState) {
    return <div>No form state available</div>;
  }

  // Handle form submission
  const onSubmit = async (data: Record<string, any>) => {
    console.log('Form data submitted:', data);
    await submitResponses(data);
  };

  return (
    <div className="form-container w-full p-6 md:p-8">
      {/* Form Header */}
      <div className="mb-8">
        {/* Company Name as H1 */}
        <h1 className="text-3xl md:text-4xl font-bold text-text mb-4">
          {form.title}
        </h1>
        
        {/* Step Headline as H2 */}
        {currentStep.headline && (
          <h2 className="text-xl md:text-2xl font-semibold text-text mb-3">
            {currentStep.headline}
          </h2>
        )}
        
        {/* Engagement Content as P */}
        {currentStep.subheading && (
          <p className="text-text-light text-lg leading-relaxed">
            {currentStep.subheading}
          </p>
        )}
        
        {/* Fallback to form description if no engagement content */}
        {!currentStep.subheading && form.description && (
          <p className="text-text-light text-lg leading-relaxed">
            {form.description}
          </p>
        )}
      </div>

      {/* Progress Bar removed - dynamic surveys can't show accurate progress */}

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-error bg-opacity-10 border border-error border-opacity-20 rounded-theme">
          <p className="text-error text-sm">{error}</p>
        </div>
      )}

      {/* Form with Questions */}
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="mb-8">
          <QuestionRenderer
            questions={currentStep.questions}
            responses={formState.responses}
            disabled={loading}
          />
        </div>

        {/* Navigation */}
        <FormNavigation
          currentStep={currentStep}
          canGoBack={form.settings.allowBack && currentStep.canGoBack}
          loading={loading}
        />
      </form>
    </div>
  );
}