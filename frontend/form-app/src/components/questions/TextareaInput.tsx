import type { UseFormRegister, Control } from 'react-hook-form';
import type { Question } from '../../types';

interface TextareaInputProps {
  question: Question;
  register: UseFormRegister<any>;
  control: Control<any>;
  error?: string;
  disabled?: boolean;
  defaultValue?: string;
}

export default function TextareaInput({ question, register, error, disabled }: TextareaInputProps) {
  const rows = question.options?.rows ? parseInt(question.options.rows) : 4;

  return (
    <div className="question-container">
      <label htmlFor={question.id} className="question-label">
        {question.text}
        {question.required && <span className="text-error ml-1">*</span>}
      </label>
      
      {question.description && (
        <p className="question-description">{question.description}</p>
      )}
      
      <textarea
        id={question.id}
        placeholder={question.placeholder}
        disabled={disabled}
        rows={rows}
        className={`input-field resize-y ${error ? 'input-error' : ''}`}
        {...register(question.id)}
      />
      
      {error && (
        <p className="error-message">{error}</p>
      )}
    </div>
  );
}