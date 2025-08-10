import type { UseFormRegister, Control } from 'react-hook-form';
import type { Question } from '../../types';

interface TextInputProps {
  question: Question;
  register: UseFormRegister<any>;
  control: Control<any>;
  error?: string;
  disabled?: boolean;
  defaultValue?: string;
}

export default function TextInput({ question, register, error, disabled }: TextInputProps) {
  const inputType = question.type === 'email' ? 'email' : 
                   question.type === 'phone' ? 'tel' :
                   question.type === 'number' ? 'number' : 'text';

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
        placeholder={question.placeholder}
        disabled={disabled}
        className={`input-field ${error ? 'input-error' : ''}`}
        {...register(question.id)}
      />
      
      {error && (
        <p className="error-message">{error}</p>
      )}
    </div>
  );
}