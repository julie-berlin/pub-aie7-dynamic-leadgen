-- Migration 005: Fix Test Data Input Types
-- Updates all test data questions to use proper input_type and data_type values
-- Safe to run multiple times

-- ==== UPDATE TEST DATA QUESTIONS ====

-- Dog Walking Service Questions (Form f1111111-1111-1111-1111-111111111111)
UPDATE form_questions 
SET 
    input_type = CASE question_id
        WHEN 1 THEN 'text'      -- Name
        WHEN 2 THEN 'text'      -- Dog name and breed  
        WHEN 3 THEN 'text'      -- Location
        WHEN 4 THEN 'select'    -- Frequency
        WHEN 5 THEN 'radio'     -- Vaccinations (boolean -> radio)
        WHEN 6 THEN 'select'    -- Can walk with others
        WHEN 7 THEN 'select'    -- Time preference
        WHEN 8 THEN 'textarea'  -- Special needs (textarea)
        WHEN 9 THEN 'email'     -- Email
        WHEN 10 THEN 'phone'    -- Phone
        ELSE input_type
    END,
    data_type = CASE question_id
        WHEN 1 THEN 'text'      -- Name
        WHEN 2 THEN 'text'      -- Dog name and breed
        WHEN 3 THEN 'text'      -- Location
        WHEN 4 THEN 'text'      -- Frequency
        WHEN 5 THEN 'boolean'   -- Vaccinations (boolean data)
        WHEN 6 THEN 'text'      -- Can walk with others
        WHEN 7 THEN 'text'      -- Time preference
        WHEN 8 THEN 'text'      -- Special needs
        WHEN 9 THEN 'text'      -- Email
        WHEN 10 THEN 'text'     -- Phone
        ELSE data_type
    END
WHERE form_id = 'f1111111-1111-1111-1111-111111111111';

-- Real Estate Questions (Form f2222222-2222-2222-2222-222222222222)
UPDATE form_questions 
SET 
    input_type = CASE question_id
        WHEN 1 THEN 'select'    -- Buy or sell
        WHEN 2 THEN 'select'    -- Timeline
        WHEN 3 THEN 'select'    -- Budget range
        WHEN 4 THEN 'select'    -- Pre-approved
        WHEN 5 THEN 'select'    -- Property type
        WHEN 6 THEN 'text'      -- Areas
        WHEN 7 THEN 'textarea'  -- Most important (textarea)
        WHEN 8 THEN 'select'    -- Previous agent experience
        WHEN 9 THEN 'text'      -- Full name
        WHEN 10 THEN 'email'    -- Email
        WHEN 11 THEN 'phone'    -- Phone
        WHEN 12 THEN 'text'     -- Preferred contact
        ELSE input_type
    END,
    data_type = CASE question_id
        WHEN 1 THEN 'text'      -- Buy or sell
        WHEN 2 THEN 'text'      -- Timeline
        WHEN 3 THEN 'text'      -- Budget range
        WHEN 4 THEN 'text'      -- Pre-approved
        WHEN 5 THEN 'text'      -- Property type
        WHEN 6 THEN 'text'      -- Areas
        WHEN 7 THEN 'text'      -- Most important
        WHEN 8 THEN 'text'      -- Previous agent experience
        WHEN 9 THEN 'text'      -- Full name
        WHEN 10 THEN 'text'     -- Email
        WHEN 11 THEN 'text'     -- Phone
        WHEN 12 THEN 'text'     -- Preferred contact
        ELSE data_type
    END
WHERE form_id = 'f2222222-2222-2222-2222-222222222222';

-- Software Consulting Questions (Form f3333333-3333-3333-3333-333333333333)
UPDATE form_questions 
SET 
    input_type = CASE question_id
        WHEN 1 THEN 'text'      -- Company name and industry
        WHEN 2 THEN 'select'    -- Annual revenue
        WHEN 3 THEN 'select'    -- Number of employees
        WHEN 4 THEN 'textarea'  -- Technology challenges (textarea)
        WHEN 5 THEN 'select'    -- Project budget
        WHEN 6 THEN 'select'    -- Timeline
        WHEN 7 THEN 'select'    -- Decision making role
        WHEN 8 THEN 'select'    -- Previous consultant experience
        WHEN 9 THEN 'text'      -- Name and title
        WHEN 10 THEN 'email'    -- Business email
        WHEN 11 THEN 'phone'    -- Phone number
        ELSE input_type
    END,
    data_type = CASE question_id
        WHEN 1 THEN 'text'      -- Company name and industry
        WHEN 2 THEN 'text'      -- Annual revenue
        WHEN 3 THEN 'text'      -- Number of employees
        WHEN 4 THEN 'text'      -- Technology challenges
        WHEN 5 THEN 'text'      -- Project budget
        WHEN 6 THEN 'text'      -- Timeline
        WHEN 7 THEN 'text'      -- Decision making role
        WHEN 8 THEN 'text'      -- Previous consultant experience
        WHEN 9 THEN 'text'      -- Name and title
        WHEN 10 THEN 'text'     -- Business email
        WHEN 11 THEN 'text'     -- Phone number
        ELSE data_type
    END
WHERE form_id = 'f3333333-3333-3333-3333-333333333333';

-- Personal Training Questions (Form f4444444-4444-4444-4444-444444444444)
UPDATE form_questions 
SET 
    input_type = CASE question_id
        WHEN 1 THEN 'select'    -- Fitness goals
        WHEN 2 THEN 'select'    -- Training frequency
        WHEN 3 THEN 'select'    -- Budget
        WHEN 4 THEN 'textarea'  -- Health conditions (textarea)
        WHEN 5 THEN 'select'    -- Activity level
        WHEN 6 THEN 'select'    -- Previous trainer experience
        WHEN 7 THEN 'select'    -- Time preference
        WHEN 8 THEN 'text'      -- Full name
        WHEN 9 THEN 'email'     -- Email
        WHEN 10 THEN 'phone'    -- Phone
        ELSE input_type
    END,
    data_type = CASE question_id
        WHEN 1 THEN 'text'      -- Fitness goals
        WHEN 2 THEN 'text'      -- Training frequency
        WHEN 3 THEN 'text'      -- Budget
        WHEN 4 THEN 'text'      -- Health conditions
        WHEN 5 THEN 'text'      -- Activity level
        WHEN 6 THEN 'text'      -- Previous trainer experience
        WHEN 7 THEN 'text'      -- Time preference
        WHEN 8 THEN 'text'      -- Full name
        WHEN 9 THEN 'text'      -- Email
        WHEN 10 THEN 'text'     -- Phone
        ELSE data_type
    END
WHERE form_id = 'f4444444-4444-4444-4444-444444444444';

-- Home Cleaning Questions (Form f5555555-5555-5555-5555-555555555555)
UPDATE form_questions 
SET 
    input_type = CASE question_id
        WHEN 1 THEN 'select'    -- Home size
        WHEN 2 THEN 'text'      -- Bedrooms and bathrooms
        WHEN 3 THEN 'select'    -- Cleaning frequency
        WHEN 4 THEN 'select'    -- Budget per cleaning
        WHEN 5 THEN 'text'      -- Location
        WHEN 6 THEN 'select'    -- Pets
        WHEN 7 THEN 'textarea'  -- Special requirements (textarea)
        WHEN 8 THEN 'text'      -- Full name
        WHEN 9 THEN 'text'      -- Email and phone (combined field)
        ELSE input_type
    END,
    data_type = CASE question_id
        WHEN 1 THEN 'text'      -- Home size
        WHEN 2 THEN 'text'      -- Bedrooms and bathrooms
        WHEN 3 THEN 'text'      -- Cleaning frequency
        WHEN 4 THEN 'text'      -- Budget per cleaning
        WHEN 5 THEN 'text'      -- Location
        WHEN 6 THEN 'text'      -- Pets
        WHEN 7 THEN 'text'      -- Special requirements
        WHEN 8 THEN 'text'      -- Full name
        WHEN 9 THEN 'text'      -- Email and phone
        ELSE data_type
    END
WHERE form_id = 'f5555555-5555-5555-5555-555555555555';

-- ==== VERIFICATION QUERIES ====

-- Verify the test data updates
CREATE OR REPLACE FUNCTION verify_test_data_input_types_005()
RETURNS TABLE(
    form_title TEXT,
    question_id INTEGER,
    question_text TEXT,
    old_question_type TEXT,
    new_input_type TEXT,
    new_data_type TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        f.title as form_title,
        fq.question_id,
        SUBSTRING(fq.question_text, 1, 50) || '...' as question_text,
        fq.question_type as old_question_type,
        fq.input_type as new_input_type,
        fq.data_type as new_data_type
    FROM form_questions fq
    JOIN forms f ON f.id = fq.form_id
    WHERE fq.form_id IN (
        'f1111111-1111-1111-1111-111111111111',
        'f2222222-2222-2222-2222-222222222222',
        'f3333333-3333-3333-3333-333333333333',
        'f4444444-4444-4444-4444-444444444444',
        'f5555555-5555-5555-5555-555555555555'
    )
    ORDER BY f.title, fq.question_order;
END;
$$ LANGUAGE plpgsql;

-- Show questions that should be radio buttons (boolean data type)
CREATE OR REPLACE FUNCTION verify_boolean_questions_005()
RETURNS TABLE(
    form_title TEXT,
    question_text TEXT,
    input_type TEXT,
    data_type TEXT,
    should_be_radio BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        f.title as form_title,
        fq.question_text,
        fq.input_type,
        fq.data_type,
        (fq.data_type = 'boolean') as should_be_radio
    FROM form_questions fq
    JOIN forms f ON f.id = fq.form_id
    WHERE fq.data_type = 'boolean' OR fq.input_type = 'radio'
    ORDER BY f.title, fq.question_order;
END;
$$ LANGUAGE plpgsql;

-- Show questions that should be textareas
CREATE OR REPLACE FUNCTION verify_textarea_questions_005()
RETURNS TABLE(
    form_title TEXT,
    question_text TEXT,
    input_type TEXT,
    data_type TEXT,
    should_be_textarea BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        f.title as form_title,
        fq.question_text,
        fq.input_type,
        fq.data_type,
        (fq.input_type = 'textarea') as should_be_textarea
    FROM form_questions fq
    JOIN forms f ON f.id = fq.form_id
    WHERE fq.input_type = 'textarea'
    ORDER BY f.title, fq.question_order;
END;
$$ LANGUAGE plpgsql;

-- ==== RUN VERIFICATION ====

SELECT 'Migration 005 - Test Data Input Types Verification:' as verification_type;
SELECT * FROM verify_test_data_input_types_005();

SELECT 'Migration 005 - Boolean Questions (should be radio):' as verification_type;
SELECT * FROM verify_boolean_questions_005();

SELECT 'Migration 005 - Textarea Questions:' as verification_type;
SELECT * FROM verify_textarea_questions_005();

-- Summary statistics
SELECT 'Migration 005 - Summary Statistics:' as verification_type;
SELECT 
    'Total test questions updated' as metric,
    COUNT(*) as value
FROM form_questions 
WHERE form_id IN (
    'f1111111-1111-1111-1111-111111111111',
    'f2222222-2222-2222-2222-222222222222',
    'f3333333-3333-3333-3333-333333333333',
    'f4444444-4444-4444-4444-444444444444',
    'f5555555-5555-5555-5555-555555555555'
)
UNION ALL
SELECT 
    'Questions with radio input_type',
    COUNT(*) 
FROM form_questions 
WHERE input_type = 'radio'
UNION ALL
SELECT 
    'Questions with textarea input_type',
    COUNT(*) 
FROM form_questions 
WHERE input_type = 'textarea'
UNION ALL
SELECT 
    'Questions with boolean data_type',
    COUNT(*) 
FROM form_questions 
WHERE data_type = 'boolean';