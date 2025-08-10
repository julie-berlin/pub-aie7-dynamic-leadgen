import type { FormProgress } from '../types';

interface ProgressBarProps {
  progress: FormProgress;
  showText?: boolean;
}

export default function ProgressBar({ progress, showText = true }: ProgressBarProps) {
  const { currentStep, totalSteps, percentage } = progress;

  return (
    <div className="w-full">
      {showText && (
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-text">
            Step {currentStep} of {totalSteps}
          </span>
          <span className="text-sm text-text-muted">
            {Math.round(percentage)}% complete
          </span>
        </div>
      )}
      
      <div className="progress-bar w-full h-2">
        <div 
          className="progress-bar-fill h-full transition-all duration-300 ease-out"
          style={{ width: `${percentage}%` }}
          role="progressbar"
          aria-valuenow={percentage}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label={`Form progress: ${Math.round(percentage)}% complete`}
        />
      </div>
    </div>
  );
}