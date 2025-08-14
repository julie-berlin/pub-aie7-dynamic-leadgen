-- Migration 003: Fix Compound Questions - Split into Single-Purpose Questions
-- Critical UX Fix: Each question should ask for exactly ONE piece of information

-- Update compound questions to single-purpose questions and add the split questions

-- 1. Fix Dog Walking Form (f1111111-1111-1111-1111-111111111111)
-- Split "What is your dog's name and breed?" into two questions

-- Update the existing compound question to ask only for name
UPDATE form_questions 
SET question_text = 'What is your dog''s name?'
WHERE form_id = 'f1111111-1111-1111-1111-111111111111'::uuid 
  AND question_text = 'What is your dog''s name and breed?';

-- Add the breed question as a new question
INSERT INTO form_questions (
    form_id, question_id, question_order, question_text, question_type, 
    options, is_required, scoring_rubric, category
) VALUES (
    'f1111111-1111-1111-1111-111111111111'::uuid,
    11, -- New question ID
    3,  -- Insert after name question
    'What breed is your dog?',
    'text',
    NULL,
    false,
    '+3 points for breed info',
    'basic_info'
) ON CONFLICT (form_id, question_id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    scoring_rubric = EXCLUDED.scoring_rubric;

-- 2. Fix TechSolve Consulting Form (f3333333-3333-3333-3333-333333333333)
-- Split "What is your company name and industry?" into two questions

-- Update the existing compound question to ask only for company name
UPDATE form_questions 
SET question_text = 'What is your company name?'
WHERE form_id = 'f3333333-3333-3333-3333-333333333333'::uuid 
  AND question_text = 'What is your company name and industry?';

-- Add the industry question as a new question
INSERT INTO form_questions (
    form_id, question_id, question_order, question_text, question_type, 
    options, is_required, scoring_rubric, category
) VALUES (
    'f3333333-3333-3333-3333-333333333333'::uuid,
    12, -- New question ID
    2,  -- Insert after company name
    'What industry is your company in?',
    'select',
    '["Healthcare", "Finance", "Manufacturing", "Technology", "Retail", "Education", "Other"]',
    false,
    '+8 points for target industry (Healthcare, Finance, Manufacturing), +3 points for others',
    'qualification'
) ON CONFLICT (form_id, question_id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    options = EXCLUDED.options,
    scoring_rubric = EXCLUDED.scoring_rubric;

-- 3. Fix FitLife Personal Training Form (f4444444-4444-4444-4444-444444444444)
-- Split "Your full name and title?" into two questions

-- Update the existing compound question to ask only for name
UPDATE form_questions 
SET question_text = 'What is your full name?'
WHERE form_id = 'f4444444-4444-4444-4444-444444444444'::uuid 
  AND question_text = 'Your full name and title?';

-- Add the title question as a new question
INSERT INTO form_questions (
    form_id, question_id, question_order, question_text, question_type, 
    options, is_required, scoring_rubric, category
) VALUES (
    'f4444444-4444-4444-4444-444444444444'::uuid,
    11, -- New question ID
    2,  -- Insert after name
    'What is your job title?',
    'text',
    NULL,
    false,
    '+5 points for executive/management titles',
    'demographic'
) ON CONFLICT (form_id, question_id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    scoring_rubric = EXCLUDED.scoring_rubric;

-- 4. Fix Sparkle Clean Solutions Form (f5555555-5555-5555-5555-555555555555)
-- Split "Your email and phone number?" into two questions

-- Update the existing compound question to ask only for email
UPDATE form_questions 
SET question_text = 'What is your email address?',
    question_type = 'email'
WHERE form_id = 'f5555555-5555-5555-5555-555555555555'::uuid 
  AND question_text = 'Your email and phone number?';

-- Add the phone question as a new question  
INSERT INTO form_questions (
    form_id, question_id, question_order, question_text, question_type, 
    options, is_required, scoring_rubric, category
) VALUES (
    'f5555555-5555-5555-5555-555555555555'::uuid,
    10, -- New question ID
    4,  -- Insert after email
    'What is your phone number?',
    'phone',
    NULL,
    false,
    '+2 points for providing phone contact',
    'contact'
) ON CONFLICT (form_id, question_id) DO UPDATE SET
    question_text = EXCLUDED.question_text,
    question_type = EXCLUDED.question_type,
    scoring_rubric = EXCLUDED.scoring_rubric;

-- Update question orders to accommodate new questions
-- This ensures proper ordering after adding new questions

-- Dog Walking Form: Shift questions after the breed question
UPDATE form_questions 
SET question_order = question_order + 1
WHERE form_id = 'f1111111-1111-1111-1111-111111111111'::uuid 
  AND question_order >= 3 
  AND question_id != 11; -- Don't update the new breed question

-- TechSolve Form: Shift questions after the industry question  
UPDATE form_questions 
SET question_order = question_order + 1
WHERE form_id = 'f3333333-3333-3333-3333-333333333333'::uuid 
  AND question_order >= 2 
  AND question_id != 12; -- Don't update the new industry question

-- FitLife Form: Shift questions after the title question
UPDATE form_questions 
SET question_order = question_order + 1
WHERE form_id = 'f4444444-4444-4444-4444-444444444444'::uuid 
  AND question_order >= 2 
  AND question_id != 11; -- Don't update the new title question

-- Sparkle Clean Form: Shift questions after the phone question
UPDATE form_questions 
SET question_order = question_order + 1
WHERE form_id = 'f5555555-5555-5555-5555-555555555555'::uuid 
  AND question_order >= 4 
  AND question_id != 10; -- Don't update the new phone question

-- Verification: Check the updated questions
SELECT 
    f.title as form_title,
    fq.question_order,
    fq.question_id,
    fq.question_text,
    fq.question_type,
    fq.category
FROM forms f
JOIN form_questions fq ON f.id = fq.form_id
WHERE f.id IN (
    'f1111111-1111-1111-1111-111111111111'::uuid,
    'f3333333-3333-3333-3333-333333333333'::uuid,
    'f4444444-4444-4444-4444-444444444444'::uuid,
    'f5555555-5555-5555-5555-555555555555'::uuid
)
ORDER BY f.title, fq.question_order;