-- Migration 004: Add input_type and data_type columns to form_questions
-- Separates frontend input type from backend data type for proper form rendering
-- Safe to run multiple times - uses IF NOT EXISTS and proper data migration

-- ==== ADD NEW COLUMNS ====

-- Add input_type column (frontend input type: text, textarea, radio, select, etc.)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'form_questions' AND column_name = 'input_type') THEN
        ALTER TABLE form_questions ADD COLUMN input_type TEXT;
    END IF;
END $$;

-- Add data_type column (backend data type: text, integer, float, boolean, etc.)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'form_questions' AND column_name = 'data_type') THEN
        ALTER TABLE form_questions ADD COLUMN data_type TEXT DEFAULT 'text';
    END IF;
END $$;

-- ==== DATA MIGRATION ====

-- Populate input_type and data_type based on existing question_type values
-- This fixes the frontend issue where boolean questions show as textareas instead of radio buttons

UPDATE form_questions 
SET 
    input_type = CASE question_type
        WHEN 'text' THEN 'text'
        WHEN 'textarea' THEN 'textarea'
        WHEN 'email' THEN 'email'
        WHEN 'phone' THEN 'phone'
        WHEN 'number' THEN 'number'
        WHEN 'select' THEN 'select'
        WHEN 'radio' THEN 'radio'
        WHEN 'checkbox' THEN 'checkbox'
        WHEN 'multiselect' THEN 'multiselect'
        WHEN 'boolean' THEN 'radio'  -- CRITICAL FIX: boolean questions should use radio buttons
        WHEN 'rating' THEN 'rating'
        WHEN 'date' THEN 'date'
        WHEN 'time' THEN 'time'
        WHEN 'datetime' THEN 'datetime'
        WHEN 'file' THEN 'file'
        ELSE 'text'  -- Default fallback
    END,
    data_type = CASE question_type
        WHEN 'text' THEN 'text'
        WHEN 'textarea' THEN 'text'
        WHEN 'email' THEN 'text'
        WHEN 'phone' THEN 'text'
        WHEN 'number' THEN 'integer'
        WHEN 'select' THEN 'text'
        WHEN 'radio' THEN 'text'
        WHEN 'checkbox' THEN 'text'
        WHEN 'multiselect' THEN 'text'
        WHEN 'boolean' THEN 'boolean'  -- CRITICAL: boolean data type for proper validation
        WHEN 'rating' THEN 'integer'
        WHEN 'date' THEN 'text'
        WHEN 'time' THEN 'text'
        WHEN 'datetime' THEN 'text'
        WHEN 'file' THEN 'text'
        ELSE 'text'  -- Default fallback
    END
WHERE input_type IS NULL OR data_type IS NULL;

-- ==== ADD CONSTRAINTS AND INDEXES ====

-- Add NOT NULL constraints after data migration
DO $$ 
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns 
              WHERE table_name = 'form_questions' AND column_name = 'input_type' 
              AND is_nullable = 'YES') THEN
        ALTER TABLE form_questions ALTER COLUMN input_type SET NOT NULL;
    END IF;
END $$;

DO $$ 
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns 
              WHERE table_name = 'form_questions' AND column_name = 'data_type' 
              AND is_nullable = 'YES') THEN
        ALTER TABLE form_questions ALTER COLUMN data_type SET NOT NULL;
    END IF;
END $$;

-- Add validation constraints for input_type
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.check_constraints 
                  WHERE constraint_name = 'form_questions_input_type_check') THEN
        ALTER TABLE form_questions 
        ADD CONSTRAINT form_questions_input_type_check 
        CHECK (input_type IN (
            'text', 'textarea', 'email', 'phone', 'number', 
            'select', 'radio', 'checkbox', 'multiselect', 
            'rating', 'date', 'time', 'datetime', 'file'
        ));
    END IF;
END $$;

-- Add validation constraints for data_type
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.check_constraints 
                  WHERE constraint_name = 'form_questions_data_type_check') THEN
        ALTER TABLE form_questions 
        ADD CONSTRAINT form_questions_data_type_check 
        CHECK (data_type IN (
            'text', 'integer', 'float', 'boolean', 'date', 'time', 'datetime'
        ));
    END IF;
END $$;

-- Add indexes for query performance
CREATE INDEX IF NOT EXISTS idx_form_questions_input_type ON form_questions(input_type);
CREATE INDEX IF NOT EXISTS idx_form_questions_data_type ON form_questions(data_type);

-- ==== HELPER FUNCTIONS ====

-- Function to get frontend question format with both input_type and data_type
CREATE OR REPLACE FUNCTION get_question_frontend_format(question_row form_questions)
RETURNS JSONB AS $$
BEGIN
    RETURN jsonb_build_object(
        'question_id', question_row.question_id,
        'question_text', question_row.question_text,
        'input_type', question_row.input_type,
        'data_type', question_row.data_type,
        'question_type', question_row.question_type, -- Keep for backward compatibility
        'is_required', question_row.is_required,
        'options', question_row.options,
        'category', question_row.category
    );
END;
$$ LANGUAGE plpgsql;

-- ==== VERIFICATION QUERIES ====

-- Verify the migration worked correctly
CREATE OR REPLACE FUNCTION verify_migration_004()
RETURNS TABLE(
    question_type TEXT,
    input_type TEXT,
    data_type TEXT,
    count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        fq.question_type,
        fq.input_type,
        fq.data_type,
        COUNT(*) as count
    FROM form_questions fq
    GROUP BY fq.question_type, fq.input_type, fq.data_type
    ORDER BY fq.question_type, fq.input_type, fq.data_type;
END;
$$ LANGUAGE plpgsql;

-- Verify boolean questions are properly mapped
CREATE OR REPLACE FUNCTION verify_boolean_questions_004()
RETURNS TABLE(
    form_title TEXT,
    question_text TEXT,
    question_type TEXT,
    input_type TEXT,
    data_type TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        f.title as form_title,
        fq.question_text,
        fq.question_type,
        fq.input_type,
        fq.data_type
    FROM form_questions fq
    JOIN forms f ON f.id = fq.form_id
    WHERE fq.question_type = 'boolean' OR fq.data_type = 'boolean'
    ORDER BY f.title, fq.question_order;
END;
$$ LANGUAGE plpgsql;

-- ==== RUN VERIFICATION ====

SELECT 'Migration 004 - Question Type Mapping Verification:' as verification_type;
SELECT * FROM verify_migration_004();

SELECT 'Migration 004 - Boolean Questions Verification:' as verification_type;
SELECT * FROM verify_boolean_questions_004();

-- Show summary statistics
SELECT 'Migration 004 - Summary Statistics:' as verification_type;
SELECT 
    'Total questions' as metric,
    COUNT(*) as value
FROM form_questions
UNION ALL
SELECT 
    'Questions with input_type',
    COUNT(*) 
FROM form_questions 
WHERE input_type IS NOT NULL
UNION ALL
SELECT 
    'Questions with data_type',
    COUNT(*) 
FROM form_questions 
WHERE data_type IS NOT NULL
UNION ALL
SELECT 
    'Boolean questions (should use radio inputs)',
    COUNT(*) 
FROM form_questions 
WHERE data_type = 'boolean';