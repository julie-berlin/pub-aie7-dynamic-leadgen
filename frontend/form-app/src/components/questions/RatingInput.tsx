import { useState } from 'react';
import type { UseFormRegister, Control } from 'react-hook-form';
import { useController } from 'react-hook-form';
import type { Question } from '../../types';

interface RatingInputProps {
  question: Question;
  register: UseFormRegister<any>;
  control: Control<any>;
  error?: string;
  disabled?: boolean;
  defaultValue?: number;
}

export default function RatingInput({ question, control, error, disabled }: RatingInputProps) {
  const { field } = useController({
    name: question.id,
    control,
    defaultValue: 0
  });

  const [hoverValue, setHoverValue] = useState(0);
  
  const maxRating = question.options?.maxRating ? parseInt(question.options.maxRating) : 5;
  const minRating = question.options?.minRating ? parseInt(question.options.minRating) : 1;
  const ratingType = question.options?.ratingType || 'stars'; // stars, numbers, or scale
  const labels = question.options?.ratingLabels;

  const handleRatingChange = (value: number) => {
    if (!disabled) {
      field.onChange(value);
    }
  };

  const renderStars = () => (
    <div className="flex items-center space-x-1">
      {Array.from({ length: maxRating }, (_, index) => {
        const ratingValue = index + 1;
        const isActive = ratingValue <= (hoverValue || field.value);
        
        return (
          <button
            key={ratingValue}
            type="button"
            disabled={disabled}
            onClick={() => handleRatingChange(ratingValue)}
            onMouseEnter={() => setHoverValue(ratingValue)}
            onMouseLeave={() => setHoverValue(0)}
            className={`w-8 h-8 transition-colors duration-150 ${
              disabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer hover:scale-110'
            }`}
          >
            <svg
              className={`w-full h-full ${
                isActive ? 'text-warning' : 'text-border'
              }`}
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </button>
        );
      })}
      {field.value > 0 && (
        <span className="ml-2 text-sm text-text-muted">
          {field.value} / {maxRating}
        </span>
      )}
    </div>
  );

  const renderNumbers = () => (
    <div className="flex items-center space-x-2">
      {Array.from({ length: maxRating - minRating + 1 }, (_, index) => {
        const ratingValue = minRating + index;
        const isActive = ratingValue === field.value;
        
        return (
          <button
            key={ratingValue}
            type="button"
            disabled={disabled}
            onClick={() => handleRatingChange(ratingValue)}
            className={`w-10 h-10 rounded-full border-2 transition-all duration-150 font-medium ${
              isActive
                ? 'bg-primary text-white border-primary'
                : 'bg-transparent text-text border-border hover:border-primary hover:text-primary'
            } ${disabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'}`}
          >
            {ratingValue}
          </button>
        );
      })}
    </div>
  );

  const renderScale = () => (
    <div className="w-full">
      <div className="flex justify-between text-sm text-text-muted mb-2">
        {labels?.start && <span>{labels.start}</span>}
        {labels?.end && <span>{labels.end}</span>}
      </div>
      <input
        type="range"
        min={minRating}
        max={maxRating}
        value={field.value}
        disabled={disabled}
        onChange={(e) => handleRatingChange(parseInt(e.target.value))}
        className="w-full h-2 bg-background-light rounded-lg appearance-none cursor-pointer slider"
      />
      <div className="flex justify-between text-xs text-text-muted mt-1">
        <span>{minRating}</span>
        <span className="font-medium">{field.value}</span>
        <span>{maxRating}</span>
      </div>
    </div>
  );

  return (
    <div className="question-container">
      <label className="question-label">
        {question.text}
        {question.required && <span className="text-error ml-1">*</span>}
      </label>
      
      {question.description && (
        <p className="question-description">{question.description}</p>
      )}
      
      <div className="mt-4">
        {ratingType === 'stars' && renderStars()}
        {ratingType === 'numbers' && renderNumbers()}
        {ratingType === 'scale' && renderScale()}
      </div>
      
      {error && (
        <p className="error-message">{error}</p>
      )}
    </div>
  );
}