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
                   question.type === 'tel' ? 'tel' :
                   question.type === 'number' ? 'number' : 'text';

  return (
    <div className="question-container mb-8">
      <label 
        htmlFor={question.id} 
        className="block text-xl font-semibold mb-3"
        style={{ color: 'var(--color-text)' }}
      >
        {question.text}
        {question.required && <span style={{ color: 'var(--color-error)' }} className="ml-1">*</span>}
      </label>
      
      {question.description && (
        <p 
          className="text-base mb-4 leading-relaxed"
          style={{ color: 'var(--color-text-light)' }}
        >
          {question.description}
        </p>
      )}
      
      <input
        id={question.id}
        type={inputType}
        placeholder={question.placeholder}
        disabled={disabled}
        className={`
          input-field text-lg 
          ${disabled ? 'cursor-not-allowed' : ''}
          ${error ? 'input-error' : ''}
        `}
        style={{
          borderRadius: 'var(--border-radius-lg)',
        }}
        onFocus={(e) => {
          if (!error) {
            e.target.style.borderColor = 'var(--color-primary)';
            e.target.style.boxShadow = '0 0 0 4px var(--color-primary-light)';
          }
        }}
        {...register(question.id, {
          onBlur: (e) => {
            if (!error) {
              e.target.style.borderColor = 'var(--color-border)';
              e.target.style.boxShadow = 'none';
            }
          }
        })}
      />
      
      {error && (
        <p 
          className="text-base mt-3 px-2 font-medium"
          style={{ color: 'var(--color-error)' }}
        >
          {error}
        </p>
      )}
    </div>
  );
}