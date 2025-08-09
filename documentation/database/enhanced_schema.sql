-- Enhanced Database Schema for Dynamic Lead Generation Platform
-- Supports Phases 1-6: UTM tracking, abandonment detection, conditional completion
-- Run this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==== CORE BUSINESS TABLES ====

-- Clients table (businesses using the platform) - Enhanced
CREATE TABLE IF NOT EXISTS clients (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    -- Basic info
    name TEXT NOT NULL,
    business_name TEXT, -- For personalized messages
    email TEXT NOT NULL UNIQUE,
    owner_name TEXT NOT NULL, -- For message generation
    contact_name TEXT, -- Alternative contact
    -- Business details
    business_type TEXT, -- "dog walking", "real estate", etc.
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

-- Form configurations - Enhanced
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

-- Individual form questions - New table for database storage
CREATE TABLE IF NOT EXISTS form_questions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL, -- Question number within form
    question_order INTEGER NOT NULL, -- Display order
    question_text TEXT NOT NULL,
    question_type TEXT DEFAULT 'text', -- text, multiple_choice, boolean, etc.
    options JSONB, -- For multiple choice questions
    is_required BOOLEAN DEFAULT false,
    scoring_rubric TEXT, -- How to score this question
    category TEXT, -- contact, service, qualification, etc.
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(form_id, question_id)
);

-- ==== SESSION AND TRACKING TABLES ====

-- Lead sessions - Enhanced with tracking and abandonment
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
    time_on_step INTEGER, -- seconds
    hesitation_indicators INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- UTM and tracking data - New table for marketing attribution
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

-- Individual question responses - Enhanced
CREATE TABLE IF NOT EXISTS responses (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT REFERENCES lead_sessions(session_id) ON DELETE CASCADE,
    
    -- Question context
    question_id INTEGER NOT NULL,
    question_text TEXT NOT NULL, -- Original question text
    phrased_question TEXT, -- AI-phrased version
    answer TEXT NOT NULL,
    
    -- Response metadata
    step INTEGER NOT NULL,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    response_time_seconds INTEGER, -- Time to answer
    
    -- Question configuration
    data_type TEXT DEFAULT 'text',
    is_required BOOLEAN DEFAULT false,
    scoring_rubric TEXT,
    score_awarded INTEGER DEFAULT 0,
    
    -- Timestamps
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==== ANALYTICS AND RECOVERY TABLES ====

-- Historical lead outcomes (for ML learning) - Enhanced
CREATE TABLE IF NOT EXISTS lead_outcomes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT REFERENCES lead_sessions(session_id) ON DELETE CASCADE,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    
    -- Conversion tracking
    actual_conversion BOOLEAN,
    predicted_conversion BOOLEAN, -- What our AI predicted
    conversion_date TIMESTAMP WITH TIME ZONE,
    conversion_value DECIMAL(10,2),
    conversion_type TEXT, -- sale, appointment, signup, etc.
    
    -- Analysis
    prediction_accuracy BOOLEAN, -- Did we predict correctly?
    notes TEXT,
    feedback_score INTEGER, -- 1-5 rating from client
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Session state snapshots (for form recovery) - Enhanced
CREATE TABLE IF NOT EXISTS session_snapshots (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT REFERENCES lead_sessions(session_id) ON DELETE CASCADE,
    
    -- State data
    full_state JSONB NOT NULL, -- Complete hierarchical state
    core_state JSONB, -- Just core state for quick recovery
    step INTEGER NOT NULL,
    
    -- Recovery metadata
    recoverable BOOLEAN DEFAULT true,
    recovery_reason TEXT, -- abandonment, error, timeout, etc.
    
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

-- ==== ROW LEVEL SECURITY ====

ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE forms ENABLE ROW LEVEL SECURITY;
ALTER TABLE form_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE tracking_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE responses ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_outcomes ENABLE ROW LEVEL SECURITY;
ALTER TABLE session_snapshots ENABLE ROW LEVEL SECURITY;

-- Service role policies (backend access)
CREATE POLICY "Enable all operations for service role" ON clients
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Enable all operations for service role" ON forms
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Enable all operations for service role" ON form_questions
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Enable all operations for service role" ON lead_sessions
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Enable all operations for service role" ON tracking_data
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Enable all operations for service role" ON responses
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Enable all operations for service role" ON lead_outcomes
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Enable all operations for service role" ON session_snapshots
    FOR ALL USING (auth.role() = 'service_role');

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
CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON clients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_forms_updated_at BEFORE UPDATE ON forms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

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
CREATE TRIGGER update_lead_sessions_abandonment BEFORE UPDATE ON lead_sessions
    FOR EACH ROW EXECUTE FUNCTION update_abandonment_status();

-- ==== SAMPLE DATA FOR DEVELOPMENT ====

-- Insert enhanced test client
INSERT INTO clients (
    name, business_name, email, owner_name, business_type, industry,
    address, background, goals, target_audience
) VALUES (
    'Darlene''s Doggie Daywalks',
    'Pawsome Dog Walking', 
    'demo@jkwb.mozmail.com',
    'Darlene Demo',
    'dog walking service',
    'Pet services',
    '243 School Street, Somerville, MA',
    'I''m a recent college graduate (Psychology) who loves dogs. I grew up with several family dogs and always loved playing with them and hiking, jogging, swimming. I started this service because there are many busy people near me who may not have the time to walk their dog every day.',
    'I want to find clients that live nearby and have well-behaved dogs to be walked several times per week. If a dog gets along well with other dogs then I can walk several at once which is best for profit.',
    'Dog owners in urban areas who need regular walking services for well-behaved dogs'
) ON CONFLICT (email) DO NOTHING;

-- Insert sample form (will generate UUID automatically)
INSERT INTO forms (
    client_id, title, description,
    lead_scoring_threshold_yes, lead_scoring_threshold_maybe,
    max_questions, min_questions_before_fail
) VALUES (
    (SELECT id FROM clients WHERE email = 'demo@jkwb.mozmail.com'),
    'Dog Walking Service Interest Form',
    'Quick form to see if our dog walking service is right for you and your dog.',
    75, 45, 8, 4
);

-- Get the form ID for inserting questions
DO $$
DECLARE
    demo_form_id UUID;
BEGIN
    SELECT id INTO demo_form_id FROM forms 
    WHERE title = 'Dog Walking Service Interest Form' 
    AND client_id = (SELECT id FROM clients WHERE email = 'demo@jkwb.mozmail.com');
    
    -- Sample form questions (basic set)
    INSERT INTO form_questions (form_id, question_id, question_order, question_text, question_type, is_required, scoring_rubric, category) VALUES
        (demo_form_id, 1, 1, 'What is your name?', 'text', true, 'Contact information required', 'contact'),
        (demo_form_id, 2, 2, 'What is your dog''s name?', 'text', false, '+5 points for engagement', 'basic_info'),
        (demo_form_id, 3, 3, 'What breed is your dog?', 'text', false, '+10 points, helps with compatibility', 'basic_info'),
        (demo_form_id, 4, 4, 'How often would you need dog walking services?', 'multiple_choice', true, '+20 for daily, +15 for 3-4x week, +10 for 1-2x week, +5 for occasional', 'service_needs'),
        (demo_form_id, 5, 5, 'Is your dog up to date on vaccinations?', 'boolean', true, '+25 points if yes, -50 if no', 'qualification'),
        (demo_form_id, 6, 6, 'How does your dog behave around other dogs?', 'multiple_choice', false, '+15 for friendly, +10 for neutral, +5 for shy, -10 for aggressive', 'compatibility'),
        (demo_form_id, 7, 7, 'What is your budget range for dog walking?', 'multiple_choice', false, '+20 for premium, +15 for standard, +10 for budget, +5 for negotiable', 'budget'),
        (demo_form_id, 8, 8, 'What is your email address?', 'email', true, 'Contact information required for qualified leads', 'contact')
    ON CONFLICT (form_id, question_id) DO NOTHING;
END $$;