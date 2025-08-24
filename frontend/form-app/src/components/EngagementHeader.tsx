import type { FormConfig, FormStep } from '../types';

interface EngagementHeaderProps {
  form: FormConfig;
  currentStep: FormStep;
}

/**
 * EngagementHeader Component
 *
 * Displays the AI-generated engaging headline and motivational content for each form step.
 * This content is designed to encourage user engagement and guide them through the survey.
 *
 * Separated from form inputs to maintain clean component boundaries.
 */
export default function EngagementHeader({ form, currentStep }: EngagementHeaderProps) {
  return (
    <div className="engagement-header">
      {/* Step Headline as H2 - AI-generated engaging content */}
      {currentStep.headline && (
        <h2
          className="text-2xl md:text-4xl font-semibold mb-6 text-center"
          style={{ color: 'var(--color-heading)' }}
        >
          {currentStep.headline}
        </h2>
      )}

      {/* Engagement/Motivation Content as P - AI-generated */}
      {currentStep.subheading && (
        <p
          className=""
          style={{ color: 'var(--color-text-light)' }}
        >
          {currentStep.subheading}
        </p>
      )}

      {/* Fallback to form description if no AI-generated engagement content */}
      {!currentStep.subheading && form.description && (
        <p
          className="text-lg md:text-xl leading-relaxed max-w-3xl mx-auto text-center"
          style={{ color: 'var(--color-text-light)' }}
        >
          {form.description}
        </p>
      )}
    </div>
  );
}
