import type { UseFormRegister, Control } from 'react-hook-form';
import { useController } from 'react-hook-form';
import type { Question } from '../../types';

interface SelectInputProps {
  question: Question;
  register: UseFormRegister<any>;
  control: Control<any>;
  error?: string;
  disabled?: boolean;
  defaultValue?: string | string[];
}

export default function SelectInput({ question, control, error, disabled }: SelectInputProps) {
  const isMultiple = question.type === 'multiselect';
  
  const { field } = useController({
    name: question.id,
    control,
    defaultValue: isMultiple ? [] : ''
  });

  if (!question.options?.choices) {
    return (
      <div className="question-container">
        <p className="text-error">Select question missing choices</p>
      </div>
    );
  }

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    if (isMultiple) {
      const selectedOptions = Array.from(event.target.selectedOptions, option => option.value);
      field.onChange(selectedOptions);
    } else {
      field.onChange(event.target.value);
    }
  };

  return (
    <div className="question-container">
      <label htmlFor={question.id} className="question-label">
        {question.text}
        {question.required && <span className="text-error ml-1">*</span>}
      </label>
      
      {question.description && (
        <p className="question-description">{question.description}</p>
      )}
      
      <select
        id={question.id}
        multiple={isMultiple}
        disabled={disabled}
        value={field.value}
        onChange={handleChange}
        className={`select-field ${isMultiple ? 'min-h-[120px]' : ''} ${error ? 'input-error' : ''}`}
      >
        {!isMultiple && !question.required && (
          <option value="">
            {question.placeholder || 'Select an option...'}
          </option>
        )}
        
        {question.options!.choices!.map((choice, index) => (
          <option 
            key={choice.value || index} 
            value={choice.value}
          >
            {choice.text}
          </option>
        ))}
      </select>
      
      {isMultiple && (
        <p className="text-sm text-text-muted mt-1">
          Hold Ctrl/Cmd to select multiple options
        </p>
      )}
      
      {error && (
        <p className="error-message">{error}</p>
      )}
    </div>
  );
}