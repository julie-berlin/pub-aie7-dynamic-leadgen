import type { FormConfig, FormStep, FormState } from '../types';
import ProgressBar from './ProgressBar';
import QuestionRenderer from './QuestionRenderer';
import FormNavigation from './FormNavigation';
import { useFormStore } from '../stores/formStore';

interface FormContainerProps {
  form: FormConfig;
  currentStep: FormStep;
  formState: FormState | null;
}

export default function FormContainer({ form, currentStep, formState }: FormContainerProps) {
  const { loading, error } = useFormStore();

  if (!formState) {
    return <div>No form state available</div>;
  }

  const progress = {
    currentStep: currentStep.stepNumber,
    totalSteps: currentStep.totalSteps,
    percentage: (currentStep.stepNumber / currentStep.totalSteps) * 100,
    completedSteps: Array.from({ length: currentStep.stepNumber - 1 }, (_, i) => i + 1)
  };

  return (
    <div className="form-container w-full p-6 md:p-8">
      {/* Form Header */}
      <div className="mb-8">
        <h1 className="text-2xl md:text-3xl font-bold text-text mb-2">
          {form.title}
        </h1>
        
        {form.description && (
          <p className="text-text-light">
            {form.description}
          </p>
        )}
      </div>

      {/* Progress Bar */}
      {form.settings.showProgress && (
        <div className="mb-8">
          <ProgressBar progress={progress} />
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-error bg-opacity-10 border border-error border-opacity-20 rounded-theme">
          <p className="text-error text-sm">{error}</p>
        </div>
      )}

      {/* Questions */}
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
    </div>
  );
}