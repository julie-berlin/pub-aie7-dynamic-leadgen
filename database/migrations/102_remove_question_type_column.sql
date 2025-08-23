-- Migration: Remove redundant question_type column from form_questions table
-- Created: 2025-08-23
-- Description: Remove the question_type column since it's identical to input_type

-- Remove the redundant question_type column
ALTER TABLE form_questions DROP COLUMN IF EXISTS question_type;

-- Add comment to document the change
COMMENT ON TABLE form_questions IS 'Form questions with input_type field for question types (question_type column removed in migration 102)';