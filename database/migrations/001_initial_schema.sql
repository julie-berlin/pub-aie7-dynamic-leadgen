-- Migration 001: Initial Database Schema for Dynamic Lead Generation Platform
-- Safe to run multiple times - uses IF NOT EXISTS
-- Supports Phases 1-21: Complete survey system with tracking and analytics

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==== CORE BUSINESS TABLES ====

-- Clients table (businesses using the platform)
CREATE TABLE IF NOT EXISTS clients (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    -- Basic info
    name TEXT NOT NULL,
    business_name TEXT,
    email TEXT NOT NULL UNIQUE,
    owner_name TEXT NOT NULL,
    contact_name TEXT,
    -- Business details
    business_type TEXT,
    industry TEXT,
    address TEXT,
    phone TEXT,
    website TEXT,
    -- Context for AI
    background TEXT,
    goals TEXT,
    target_audience TEXT,
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Form configurations
CREATE TABLE IF NOT EXISTS forms (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    -- Scoring configuration
    lead_scoring_threshold_yes INTEGER DEFAULT 80,
    lead_scoring_threshold_maybe INTEGER DEFAULT 50,
    -- Business rules
    max_questions INTEGER DEFAULT 8,
    min_questions_before_fail INTEGER DEFAULT 4,
    -- Templates
    completion_message_template TEXT,
    unqualified_message TEXT DEFAULT 'Thank you for your time.',
    -- Configuration
    is_active BOOLEAN DEFAULT true,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Individual form questions
CREATE TABLE IF NOT EXISTS form_questions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL,
    question_order INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    question_type TEXT DEFAULT 'text',
    options JSONB,
    is_required BOOLEAN DEFAULT false,
    scoring_rubric TEXT,
    category TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(form_id, question_id)
);

-- ==== SESSION AND TRACKING TABLES ====

-- Lead sessions with tracking and abandonment
CREATE TABLE IF NOT EXISTS lead_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    session_id TEXT UNIQUE NOT NULL,
    client_id UUID REFERENCES clients(id) ON DELETE SET NULL,
    
    -- Session progress
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    step INTEGER DEFAULT 0,
    completed BOOLEAN DEFAULT false,
    
    -- Lead scoring
    current_score INTEGER DEFAULT 0,
    final_score INTEGER DEFAULT 0,
    lead_status TEXT CHECK (lead_status IN ('unknown', 'yes', 'maybe', 'no')) DEFAULT 'unknown',
    
    -- Completion tracking
    completion_type TEXT CHECK (completion_type IN ('qualified', 'unqualified', 'abandoned', 'qualified_fallback', 'unqualified_error')) DEFAULT NULL,
    completion_message TEXT,
    
    -- Abandonment tracking
    abandonment_status TEXT CHECK (abandonment_status IN ('active', 'at_risk', 'high_risk', 'abandoned')) DEFAULT 'active',
    abandonment_risk DECIMAL(3,2) DEFAULT 0.30,
    last_activity_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    time_on_step INTEGER,
    hesitation_indicators INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- UTM and tracking data for marketing attribution
CREATE TABLE IF NOT EXISTS tracking_data (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT REFERENCES lead_sessions(session_id) ON DELETE CASCADE,
    
    -- UTM parameters
    utm_source TEXT,
    utm_medium TEXT,
    utm_campaign TEXT,
    utm_content TEXT,
    utm_term TEXT,
    
    -- Technical tracking
    referrer TEXT,
    user_agent TEXT,
    ip_address TEXT,
    landing_page TEXT,
    
    -- Session context
    browser_info JSONB,
    device_info JSONB,
    geographic_info JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Individual question responses
CREATE TABLE IF NOT EXISTS responses (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT REFERENCES lead_sessions(session_id) ON DELETE CASCADE,
    
    -- Question context
    question_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    phrased_question TEXT,
    answer TEXT NOT NULL,
    
    -- Response metadata
    step INTEGER NOT NULL,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    response_time_seconds INTEGER,
    
    -- Question configuration
    data_type TEXT DEFAULT 'text',
    is_required BOOLEAN DEFAULT false,
    scoring_rubric TEXT,
    score_awarded INTEGER DEFAULT 0,
    
    -- Timestamps
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==== ANALYTICS AND RECOVERY TABLES ====

-- Historical lead outcomes for ML learning
CREATE TABLE IF NOT EXISTS lead_outcomes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT REFERENCES lead_sessions(session_id) ON DELETE CASCADE,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    
    -- Conversion tracking
    actual_conversion BOOLEAN,
    predicted_conversion BOOLEAN,
    conversion_date TIMESTAMP WITH TIME ZONE,
    conversion_value DECIMAL(10,2),
    conversion_type TEXT,
    
    -- Analysis
    prediction_accuracy BOOLEAN,
    notes TEXT,
    feedback_score INTEGER,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Session state snapshots for form recovery
CREATE TABLE IF NOT EXISTS session_snapshots (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT REFERENCES lead_sessions(session_id) ON DELETE CASCADE,
    
    -- State data
    full_state JSONB NOT NULL,
    core_state JSONB,
    step INTEGER NOT NULL,
    
    -- Recovery metadata
    recoverable BOOLEAN DEFAULT true,
    recovery_reason TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==== PERFORMANCE INDEXES ====

-- Primary query patterns
CREATE INDEX IF NOT EXISTS idx_lead_sessions_form_id ON lead_sessions(form_id);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_session_id ON lead_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_status ON lead_sessions(lead_status);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_completed_at ON lead_sessions(completed_at);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_abandonment ON lead_sessions(abandonment_status);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_completion_type ON lead_sessions(completion_type);

-- Tracking and analytics
CREATE INDEX IF NOT EXISTS idx_tracking_data_session_id ON tracking_data(session_id);
CREATE INDEX IF NOT EXISTS idx_tracking_data_utm_source ON tracking_data(utm_source);
CREATE INDEX IF NOT EXISTS idx_tracking_data_utm_campaign ON tracking_data(utm_campaign);
CREATE INDEX IF NOT EXISTS idx_tracking_data_created_at ON tracking_data(created_at);

-- Responses
CREATE INDEX IF NOT EXISTS idx_responses_session_id ON responses(session_id);
CREATE INDEX IF NOT EXISTS idx_responses_timestamp ON responses(timestamp);
CREATE INDEX IF NOT EXISTS idx_responses_question_id ON responses(question_id);

-- Form questions
CREATE INDEX IF NOT EXISTS idx_form_questions_form_id ON form_questions(form_id);
CREATE INDEX IF NOT EXISTS idx_form_questions_order ON form_questions(form_id, question_order);

-- Recovery and analytics
CREATE INDEX IF NOT EXISTS idx_lead_outcomes_form_id ON lead_outcomes(form_id);
CREATE INDEX IF NOT EXISTS idx_lead_outcomes_conversion ON lead_outcomes(actual_conversion);
CREATE INDEX IF NOT EXISTS idx_session_snapshots_session_id ON session_snapshots(session_id);
CREATE INDEX IF NOT EXISTS idx_session_snapshots_recoverable ON session_snapshots(recoverable);

-- Time-based queries
CREATE INDEX IF NOT EXISTS idx_lead_sessions_started_at ON lead_sessions(started_at);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_last_activity ON lead_sessions(last_activity_timestamp);

-- ==== HELPER FUNCTIONS ====

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for automatic timestamp updates
DROP TRIGGER IF EXISTS update_clients_updated_at ON clients;
CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON clients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_forms_updated_at ON forms;
CREATE TRIGGER update_forms_updated_at BEFORE UPDATE ON forms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_lead_sessions_updated_at ON lead_sessions;
CREATE TRIGGER update_lead_sessions_updated_at BEFORE UPDATE ON lead_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to calculate abandonment risk based on inactivity
CREATE OR REPLACE FUNCTION calculate_abandonment_risk(last_activity TIMESTAMP WITH TIME ZONE)
RETURNS DECIMAL(3,2) AS $$
DECLARE
    minutes_inactive INTEGER;
BEGIN
    minutes_inactive := EXTRACT(EPOCH FROM (NOW() - last_activity)) / 60;
    
    RETURN CASE
        WHEN minutes_inactive > 15 THEN 0.95
        WHEN minutes_inactive > 10 THEN 0.80
        WHEN minutes_inactive > 5 THEN 0.60
        ELSE 0.30
    END;
END;
$$ LANGUAGE plpgsql;

-- Function to automatically update abandonment status
CREATE OR REPLACE FUNCTION update_abandonment_status()
RETURNS TRIGGER AS $$
BEGIN
    NEW.abandonment_risk := calculate_abandonment_risk(NEW.last_activity_timestamp);
    
    NEW.abandonment_status := CASE
        WHEN NEW.abandonment_risk > 0.90 THEN 'abandoned'
        WHEN NEW.abandonment_risk > 0.75 THEN 'high_risk'
        WHEN NEW.abandonment_risk > 0.55 THEN 'at_risk'
        ELSE 'active'
    END;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for automatic abandonment calculation
DROP TRIGGER IF EXISTS update_lead_sessions_abandonment ON lead_sessions;
CREATE TRIGGER update_lead_sessions_abandonment BEFORE UPDATE ON lead_sessions
    FOR EACH ROW EXECUTE FUNCTION update_abandonment_status();

-- ==== ROW LEVEL SECURITY (Optional - uncomment if using Supabase Auth) ====

-- ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE forms ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE form_questions ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE lead_sessions ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE tracking_data ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE responses ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE lead_outcomes ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE session_snapshots ENABLE ROW LEVEL SECURITY;

-- Service role policies (backend access) - uncomment if using Supabase Auth
-- CREATE POLICY "Enable all operations for service role" ON clients
--     FOR ALL USING (auth.role() = 'service_role');
-- CREATE POLICY "Enable all operations for service role" ON forms
--     FOR ALL USING (auth.role() = 'service_role');
-- CREATE POLICY "Enable all operations for service role" ON form_questions
--     FOR ALL USING (auth.role() = 'service_role');
-- CREATE POLICY "Enable all operations for service role" ON lead_sessions
--     FOR ALL USING (auth.role() = 'service_role');
-- CREATE POLICY "Enable all operations for service role" ON tracking_data
--     FOR ALL USING (auth.role() = 'service_role');
-- CREATE POLICY "Enable all operations for service role" ON responses
--     FOR ALL USING (auth.role() = 'service_role');
-- CREATE POLICY "Enable all operations for service role" ON lead_outcomes
--     FOR ALL USING (auth.role() = 'service_role');
-- CREATE POLICY "Enable all operations for service role" ON session_snapshots
--     FOR ALL USING (auth.role() = 'service_role');

-- ==== MIGRATION VERIFICATION ====

-- Create a verification function to check if all tables exist
CREATE OR REPLACE FUNCTION verify_migration_001()
RETURNS TABLE(
    table_name TEXT,
    table_exists BOOLEAN,
    index_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    WITH required_tables AS (
        SELECT unnest(ARRAY[
            'clients', 'forms', 'form_questions', 'lead_sessions',
            'tracking_data', 'responses', 'lead_outcomes', 'session_snapshots'
        ]) AS table_name
    )
    SELECT 
        rt.table_name,
        EXISTS(
            SELECT 1 FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND information_schema.tables.table_name = rt.table_name
        ) AS table_exists,
        (
            SELECT COUNT(*) FROM pg_indexes 
            WHERE schemaname = 'public' 
            AND tablename = rt.table_name
        )::INTEGER AS index_count
    FROM required_tables rt
    ORDER BY rt.table_name;
END;
$$ LANGUAGE plpgsql;

-- Run verification
SELECT * FROM verify_migration_001();