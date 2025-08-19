import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import type { Question, FormResponse } from '../types';
import TextInput from './questions/TextInput';
import TextareaInput from './questions/TextareaInput';
import RadioInput from './questions/RadioInput';
import CheckboxInput from './questions/CheckboxInput';
import SelectInput from './questions/SelectInput';
import RatingInput from './questions/RatingInput';
import DateInput from './questions/DateInput';
import FileInput from './questions/FileInput';

interface QuestionRendererProps {
  questions: Question[];
  responses: Record<string, FormResponse>;
  disabled?: boolean;
}

// Create dynamic validation schema based on questions
function createValidationSchema(questions: Question[]) {
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
      question.validation.forEach(rule => {
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

export default function QuestionRenderer({ questions, responses, disabled = false }: QuestionRendererProps) {
  // Create validation schema
  const validationSchema = createValidationSchema(questions);
  
  // Initialize form with existing responses
  const defaultValues = questions.reduce((acc, question) => {
    const response = responses[question.id];
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

  const {
    register,
    control,
    formState: { errors },
    watch
  } = useForm({
    resolver: zodResolver(validationSchema),
    defaultValues,
    mode: 'onBlur'
  });

  // Watch all form values for conditional logic
  const watchedValues = watch();

  // Filter questions based on conditional rules
  const visibleQuestions = questions.filter(question => {
    if (!question.conditional) return true;
    
    const dependentValue = watchedValues[question.conditional.dependsOn];
    
    switch (question.conditional.condition) {
      case 'equals':
        return dependentValue === question.conditional.value;
      case 'contains':
        return Array.isArray(dependentValue) 
          ? dependentValue.includes(question.conditional.value)
          : String(dependentValue).includes(question.conditional.value);
      case 'greaterThan':
        return Number(dependentValue) > Number(question.conditional.value);
      case 'lessThan':
        return Number(dependentValue) < Number(question.conditional.value);
      default:
        return true;
    }
  });

  const renderQuestion = (question: Question) => {
    const error = errors[question.id]?.message as string;
    
    const baseProps = {
      question,
      register,
      control,
      error,
      disabled,
      defaultValue: defaultValues[question.id]
    };

    switch (question.type) {
      case 'text':
      case 'email':
      case 'phone':
      case 'number':
        return <TextInput key={question.id} {...baseProps} />;
      
      case 'textarea':
        return <TextareaInput key={question.id} {...baseProps} />;
      
      case 'radio':
        return <RadioInput key={question.id} {...baseProps} />;
      
      case 'checkbox':
        return <CheckboxInput key={question.id} {...baseProps} />;
      
      case 'select':
      case 'multiselect':
        return <SelectInput key={question.id} {...baseProps} />;
      
      case 'rating':
        return <RatingInput key={question.id} {...baseProps} />;
      
      case 'date':
      case 'time':
        return <DateInput key={question.id} {...baseProps} />;
      
      case 'file':
        return <FileInput key={question.id} {...baseProps} />;
      
      default:
        return (
          <div key={question.id} className="p-4 bg-warning bg-opacity-10 border border-warning border-opacity-20 rounded-theme">
            <p className="text-warning text-sm">
              Unsupported question type: {question.type}
            </p>
          </div>
        );
    }
  };

  return (
    <div className="space-y-6">
      {visibleQuestions.map((question) => renderQuestion(question))}
    </div>
  );
}