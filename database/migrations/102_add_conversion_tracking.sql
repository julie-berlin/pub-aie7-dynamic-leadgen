-- Add conversion tracking columns to lead_outcomes table
-- These track when qualified leads actually become paying customers

ALTER TABLE lead_outcomes 
ADD COLUMN IF NOT EXISTS converted BOOLEAN DEFAULT false,
ADD COLUMN IF NOT EXISTS conversion_date TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS conversion_value DECIMAL(10,2),
ADD COLUMN IF NOT EXISTS conversion_type TEXT,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
ADD COLUMN IF NOT EXISTS updated_by_user_id UUID;

-- Add index for conversion queries
CREATE INDEX IF NOT EXISTS idx_lead_outcomes_converted ON lead_outcomes(converted);
CREATE INDEX IF NOT EXISTS idx_lead_outcomes_conversion_date ON lead_outcomes(conversion_date);

-- Add comment explaining the distinction
COMMENT ON COLUMN lead_outcomes.final_status IS 'Lead qualification status: qualified, maybe, unqualified';
COMMENT ON COLUMN lead_outcomes.converted IS 'Whether this qualified lead actually became a paying customer (manual tracking)';
COMMENT ON COLUMN lead_outcomes.conversion_date IS 'Date when lead became a customer';
COMMENT ON COLUMN lead_outcomes.conversion_value IS 'Value of the conversion (sale amount, contract value, etc.)';
COMMENT ON COLUMN lead_outcomes.conversion_type IS 'Type of conversion (sale, subscription, contract, etc.)';