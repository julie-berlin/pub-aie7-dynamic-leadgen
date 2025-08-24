-- Migration: Add example select input type questions
-- Created: 2025-08-23
-- Description: Add examples of select input type to demonstrate the feature

-- Add a select question to the Pawsome Dog Walking form
INSERT INTO form_questions (
    form_id,
    question_id,
    question_order,
    question_text,
    input_type,
    data_type,
    is_required,
    scoring_rubric,
    category,
    placeholder_text,
    options
) VALUES (
    'f1111111-1111-1111-1111-111111111111'::uuid,
    11,
    11, 
    'What time of day would you prefer walks?',
    'select',
    'text',
    false,
    'Morning: +5, Afternoon: +3, Evening: +5, Flexible: +10',
    'scheduling',
    'Choose preferred time',
    '["Morning (6-10am)", "Afternoon (12-4pm)", "Evening (5-8pm)", "Flexible/Any time"]'::jsonb
);

-- Add a select question to the Metro Realty form
INSERT INTO form_questions (
    form_id,
    question_id,
    question_order,
    question_text,
    input_type,
    data_type,
    is_required,
    scoring_rubric,
    category,
    placeholder_text,
    options
) VALUES (
    'f2222222-2222-2222-2222-222222222222'::uuid,
    13,
    13,
    'What is your preferred property type?',
    'select',
    'text',
    true,
    'Single Family: +15, Condo: +10, Townhouse: +12, Multi-Family: +8',
    'property_preferences',
    'Select property type',
    '["Single Family Home", "Condo/Apartment", "Townhouse", "Multi-Family", "Commercial", "Land/Lot"]'::jsonb
);

-- Add comment to document the change
COMMENT ON COLUMN form_questions.input_type IS 'Frontend input type: text, email, tel, number, radio, checkbox, select, textarea, etc.';