-- Add missing columns identified during development
-- Run this migration to fix schema mismatches

-- Add step column to responses table to track which step question was asked
ALTER TABLE responses 
ADD COLUMN IF NOT EXISTS step INTEGER DEFAULT 0;

-- Add missing columns to lead_sessions table
ALTER TABLE lead_sessions 
ADD COLUMN IF NOT EXISTS last_activity_time TIMESTAMP WITH TIME ZONE DEFAULT NOW();

ALTER TABLE lead_sessions 
ADD COLUMN IF NOT EXISTS confidence DECIMAL(3,2) DEFAULT 0.00;

-- Add comments for documentation
COMMENT ON COLUMN responses.step IS 'Which step/screen of the survey this question was presented on';
COMMENT ON COLUMN lead_sessions.last_activity_time IS 'Timestamp of last user activity for abandonment tracking';  
COMMENT ON COLUMN lead_sessions.confidence IS 'Confidence score for lead classification (0.00 to 1.00)';