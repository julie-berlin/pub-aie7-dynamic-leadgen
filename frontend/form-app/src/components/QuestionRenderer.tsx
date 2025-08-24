import type { Question, FormResponse } from '../types';
import type { UseFormRegister, Control, FieldErrors, UseFormWatch } from 'react-hook-form';
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
  register: UseFormRegister<any>;
  control: Control<any>;
  errors: FieldErrors<any>;
  watch: UseFormWatch<any>;
}

export default function QuestionRenderer({ 
  questions, 
  responses, 
  disabled = false, 
  register, 
  control, 
  errors, 
  watch 
}: QuestionRendererProps) {
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
    const response = responses[question.id];
    const defaultValue = response ? response.value : (
      question.type === 'checkbox' ? [] :
      question.type === 'rating' ? 0 : ''
    );
    
    const baseProps = {
      question,
      register,
      control,
      error,
      disabled,
      defaultValue
    };

    switch (question.type) {
      case 'text':
      case 'email':
      case 'phone':
      case 'number':
        return <TextInput {...baseProps} />;
      
      case 'textarea':
        return <TextareaInput {...baseProps} />;
      
      case 'radio':
        return <RadioInput {...baseProps} />;
      
      case 'checkbox':
        return <CheckboxInput {...baseProps} />;
      
      case 'select':
      case 'multiselect':
        return <SelectInput {...baseProps} />;
      
      case 'rating':
        return <RatingInput {...baseProps} />;
      
      case 'date':
      case 'time':
        return <DateInput {...baseProps} />;
      
      case 'file':
        return <FileInput {...baseProps} />;
      
      default:
        return (
          <div className="p-4 bg-warning bg-opacity-10 border border-warning border-opacity-20 rounded-theme">
            <p className="text-warning text-sm">
              Unsupported question type: {question.type}
            </p>
          </div>
        );
    }
  };

  return (
    <div>
      {visibleQuestions.map((question) => (
        <div key={question.id}>
          {renderQuestion(question)}
        </div>
      ))}
    </div>
  );
}