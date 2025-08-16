import type { FormConfig, FormStep, FormState } from '../types';
import QuestionRenderer from './QuestionRenderer';
import FormNavigation from './FormNavigation';
import { useFormStore } from '../stores/formStore';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

interface FormContainerProps {
  form: FormConfig;
  currentStep: FormStep;
  formState: FormState | null;
}

// Create dynamic validation schema based on questions
function createValidationSchema(questions: any[]) {
  const shape: Record<string, z.ZodType> = {};

  questions.forEach(question => {
    let schema: z.ZodType;

    switch (question.type) {
      case 'email':
        schema = z.string().email({ message: 'Please enter a valid email address' });
        break;
      case 'number':
        schema = z.coerce.number();
        break;
      case 'phone':
        schema = z.string().min(10, 'Please enter a valid phone number');
        break;
      case 'checkbox':
        schema = z.array(z.string()).min(1, 'Please select at least one option');
        break;
      case 'rating':
        schema = z.number().min(1).max(10);
        break;
      case 'date':
        schema = z.string().min(1, 'Please select a date');
        break;
      default:
        schema = z.string();
    }

    // Apply custom validation rules
    if (question.validation) {
      question.validation.forEach((rule: any) => {
        switch (rule.type) {
          case 'required':
            if (question.type === 'checkbox') {
              schema = (schema as z.ZodArray<z.ZodString>).min(1, rule.message);
            } else {
              schema = (schema as z.ZodString).min(1, rule.message);
            }
            break;
          case 'minLength':
            schema = (schema as z.ZodString).min(rule.value, rule.message);
            break;
          case 'maxLength':
            schema = (schema as z.ZodString).max(rule.value, rule.message);
            break;
          case 'pattern':
            schema = (schema as z.ZodString).regex(new RegExp(rule.value), rule.message);
            break;
        }
      });
    } else if (question.required) {
      if (question.type === 'checkbox') {
        schema = (schema as z.ZodArray<z.ZodString>).min(1, 'This field is required');
      } else {
        schema = (schema as z.ZodString).min(1, 'This field is required');
      }
    } else {
      schema = schema.optional();
    }

    shape[question.id] = schema;
  });

  return z.object(shape);
}

export default function FormContainer({ form, currentStep, formState }: FormContainerProps) {
  const { loading, error, submitResponses } = useFormStore();

  // Create validation schema
  const validationSchema = createValidationSchema(currentStep.questions || []);

  // Initialize form with existing responses
  const defaultValues = (currentStep.questions || []).reduce((acc: any, question: any) => {
    const response = formState?.responses[question.id];
    if (response) {
      acc[question.id] = response.value;
    } else {
      // Set default values based on question type
      switch (question.type) {
        case 'checkbox':
          acc[question.id] = [];
          break;
        case 'rating':
          acc[question.id] = 0;
          break;
        default:
          acc[question.id] = '';
      }
    }
    return acc;
  }, {} as Record<string, any>);

  // Initialize React Hook Form for this step
  const formMethods = useForm({
    resolver: zodResolver(validationSchema),
    defaultValues,
    mode: 'onBlur'
  });

  const { handleSubmit, register, control, formState: { errors }, watch } = formMethods;

  if (!formState) {
    return <div>No form state available</div>;
  }

  // Handle form submission
  const onSubmit = async (data: Record<string, any>) => {
    console.log('Form data submitted:', data);
    await submitResponses(data);
  };

  return (
    <div className="form-container">
      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-error bg-opacity-10 border border-error border-opacity-20 rounded-theme">
          <p className="text-error text-sm">{error}</p>
        </div>
      )}

      {/* Form with Questions */}
      <form onSubmit={handleSubmit(onSubmit)} className="max-w-3xl mx-auto">
        <div className="mb-36">
          <QuestionRenderer
            questions={currentStep.questions}
            responses={formState.responses}
            disabled={loading}
            register={register}
            control={control}
            errors={errors}
            watch={watch}
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
