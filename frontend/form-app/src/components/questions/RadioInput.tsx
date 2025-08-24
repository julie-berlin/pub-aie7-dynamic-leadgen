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
        <p className="question-label">
          {question.text}
          {question.required && <span className="text-error ml-1">*</span>}
        </p>

        {question.description && (
          <p className="question-description">{question.description}</p>
        )}

        <div className="">
          {question.options!.choices!.map((choice, index) => (
            <label
              key={choice.value || index}
              className="cursor-pointer m-0 flex"
            >
              <input
                type="radio"
                value={choice.value}
                disabled={disabled}
                className=""
                {...register(question.id)}
              />
              <div className="inline pl-2">
                <span className="">
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
