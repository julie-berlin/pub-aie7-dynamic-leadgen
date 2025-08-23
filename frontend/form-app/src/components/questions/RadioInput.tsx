import type { UseFormRegister, Control } from 'react-hook-form';
import type { Question } from '../../types';

interface RadioInputProps {
  question: Question;
  register: UseFormRegister<any>;
  control: Control<any>;
  error?: string;
  disabled?: boolean;
  defaultValue?: string;
}

export default function RadioInput({ question, register, error, disabled }: RadioInputProps) {
  if (!question.options?.choices) {
    return (
      <div className="question-container">
        <p className="text-error">Radio question missing choices</p>
      </div>
    );
  }

  return (
    <div className="question-container">
      <fieldset>
        <legend className="question-label">
          {question.text}
          {question.required && <span className="text-error ml-1">*</span>}
        </legend>
        
        {question.description && (
          <p className="question-description">{question.description}</p>
        )}
        
        <div className="space-y-3 mt-4">
          {question.options!.choices!.map((choice, index) => (
            <label
              key={choice.value || index}
              className="flex items-start space-x-3 cursor-pointer group hover:bg-background-light p-3 rounded-theme transition-colors"
            >
              <input
                type="radio"
                value={choice.value}
                disabled={disabled}
                className="mt-1 h-4 w-4 text-primary border-border focus:ring-primary focus:ring-2 focus:ring-offset-0 disabled:opacity-50"
                {...register(question.id)}
              />
              <div className="flex-1 min-w-0">
                <span className="text-text font-medium group-hover:text-primary transition-colors leading-relaxed">
                  {choice.text}
                </span>
                {choice.description && (
                  <p className="text-sm text-text-muted mt-1 leading-relaxed">
                    {choice.description}
                  </p>
                )}
              </div>
            </label>
          ))}
        </div>
      </fieldset>
      
      {error && (
        <p className="error-message">{error}</p>
      )}
    </div>
  );
}