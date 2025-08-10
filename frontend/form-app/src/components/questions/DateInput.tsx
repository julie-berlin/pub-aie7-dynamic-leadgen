import type { UseFormRegister, Control } from 'react-hook-form';
import type { Question } from '../../types';

interface DateInputProps {
  question: Question;
  register: UseFormRegister<any>;
  control: Control<any>;
  error?: string;
  disabled?: boolean;
  defaultValue?: string;
}

export default function DateInput({ question, register, error, disabled }: DateInputProps) {
  const inputType = question.type === 'time' ? 'time' : 
                   question.type === 'datetime' ? 'datetime-local' : 'date';

  // Format date constraints if provided
  const getDateConstraints = () => {
    const constraints: { min?: string; max?: string } = {};
    
    if (question.options?.minDate) {
      constraints.min = question.options.minDate;
    }
    if (question.options?.maxDate) {
      constraints.max = question.options.maxDate;
    }
    
    // Set common constraints
    if (question.options?.constraintType) {
      const today = new Date().toISOString().split('T')[0];
      
      switch (question.options.constraintType) {
        case 'future':
          constraints.min = today;
          break;
        case 'past':
          constraints.max = today;
          break;
        case 'adult': // 18+ years ago
          const adultDate = new Date();
          adultDate.setFullYear(adultDate.getFullYear() - 18);
          constraints.max = adultDate.toISOString().split('T')[0];
          break;
      }
    }
    
    return constraints;
  };

  const constraints = getDateConstraints();

  return (
    <div className="question-container">
      <label htmlFor={question.id} className="question-label">
        {question.text}
        {question.required && <span className="text-error ml-1">*</span>}
      </label>
      
      {question.description && (
        <p className="question-description">{question.description}</p>
      )}
      
      <input
        id={question.id}
        type={inputType}
        disabled={disabled}
        className={`input-field ${error ? 'input-error' : ''}`}
        {...constraints}
        {...register(question.id)}
      />
      
      {question.options?.helpText && (
        <p className="text-sm text-text-muted mt-1">
          {question.options.helpText}
        </p>
      )}
      
      {error && (
        <p className="error-message">{error}</p>
      )}
    </div>
  );
}