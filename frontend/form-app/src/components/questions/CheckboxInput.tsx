import type { UseFormRegister, Control } from 'react-hook-form';
import { useController } from 'react-hook-form';
import type { Question } from '../../types';

interface CheckboxInputProps {
  question: Question;
  register: UseFormRegister<any>;
  control: Control<any>;
  error?: string;
  disabled?: boolean;
  defaultValue?: string[];
}

export default function CheckboxInput({ question, control, error, disabled }: CheckboxInputProps) {
  const { field } = useController({
    name: question.id,
    control,
    defaultValue: []
  });

  if (!question.options?.choices) {
    return (
      <div className="question-container">
        <p className="text-error">Checkbox question missing choices</p>
      </div>
    );
  }

  const handleChange = (value: string, checked: boolean) => {
    const currentValues = field.value || [];
    if (checked) {
      field.onChange([...currentValues, value]);
    } else {
      field.onChange(currentValues.filter((v: string) => v !== value));
    }
  };

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
          {question.options!.choices!.map((choice, index) => {
            const isChecked = (field.value || []).includes(choice.value);
            
            return (
              <label
                key={choice.value || index}
                className="flex items-start space-x-3 cursor-pointer group"
              >
                <input
                  type="checkbox"
                  checked={isChecked}
                  disabled={disabled}
                  onChange={(e) => handleChange(choice.value, e.target.checked)}
                  className="checkbox-input mt-0.5 group-hover:border-primary-hover focus:ring-primary"
                />
                <div className="flex-1">
                  <span className="text-text group-hover:text-primary-hover">
                    {choice.text}
                  </span>
                  {choice.description && (
                    <p className="text-sm text-text-muted mt-1">
                      {choice.description}
                    </p>
                  )}
                </div>
              </label>
            );
          })}
        </div>
      </fieldset>
      
      {error && (
        <p className="error-message">{error}</p>
      )}
    </div>
  );
}