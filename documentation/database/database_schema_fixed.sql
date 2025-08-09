-- Database Schema for Dynamic Lead Generation Platform
-- Run this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Clients table (businesses using the platform)
CREATE TABLE IF NOT EXISTS clients (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    owner TEXT NOT NULL,
    address TEXT,
    background TEXT,
    goals TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Form configurations
CREATE TABLE IF NOT EXISTS forms (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    questions_config JSONB NOT NULL,
    business_rules JSONB,
    theme_config JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Lead sessions (individual form submissions)
CREATE TABLE IF NOT EXISTS lead_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    session_id TEXT UNIQUE NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    final_score INTEGER DEFAULT 0,
    lead_status TEXT CHECK (lead_status IN ('unknown', 'yes', 'maybe', 'no')) DEFAULT 'unknown',
    completed BOOLEAN DEFAULT false,
    step_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Individual question responses
CREATE TABLE IF NOT EXISTS responses (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT REFERENCES lead_sessions(session_id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL,
    original_question TEXT NOT NULL,
    phrased_question TEXT NOT NULL,
    answer TEXT NOT NULL,
    step INTEGER NOT NULL,
    data_type TEXT,
    is_required BOOLEAN DEFAULT false,
    scoring_rubric TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Historical lead outcomes (for ML learning)
CREATE TABLE IF NOT EXISTS lead_outcomes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT REFERENCES lead_sessions(session_id) ON DELETE CASCADE,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    actual_conversion BOOLEAN,
    conversion_date TIMESTAMP WITH TIME ZONE,
    conversion_value DECIMAL(10,2),
    conversion_type TEXT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Session state snapshots (for form recovery)
CREATE TABLE IF NOT EXISTS session_snapshots (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT REFERENCES lead_sessions(session_id) ON DELETE CASCADE,
    state_data JSONB NOT NULL,
    step INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_lead_sessions_form_id ON lead_sessions(form_id);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_status ON lead_sessions(lead_status);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_completed_at ON lead_sessions(completed_at);
CREATE INDEX IF NOT EXISTS idx_responses_session_id ON responses(session_id);
CREATE INDEX IF NOT EXISTS idx_responses_timestamp ON responses(timestamp);
CREATE INDEX IF NOT EXISTS idx_lead_outcomes_form_id ON lead_outcomes(form_id);
CREATE INDEX IF NOT EXISTS idx_session_snapshots_session_id ON session_snapshots(session_id);

-- Row Level Security (RLS) Policies
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE forms ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE responses ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_outcomes ENABLE ROW LEVEL SECURITY;
ALTER TABLE session_snapshots ENABLE ROW LEVEL SECURITY;

-- Basic RLS policies (allowing service_role to access everything)
CREATE POLICY "Enable all operations for service role" ON clients
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Enable all operations for service role" ON forms
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Enable all operations for service role" ON lead_sessions
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Enable all operations for service role" ON responses
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Enable all operations for service role" ON lead_outcomes
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Enable all operations for service role" ON session_snapshots
    FOR ALL USING (auth.role() = 'service_role');

-- Insert initial test client (based on your dogwalk example)
INSERT INTO clients (name, email, owner, address, background, goals) VALUES (
    'Darlene''s Doggie Daywalks',
    'demo@jkwb.mozmail.com',
    'Darlene Demo',
    '243 School Street, Somerville, MA',
    'I''m a recent college graduate (Psychology) who loves dogs. I grew up with several family dogs and always loved playing with them and hiking, jogging, swimming. I started this service because there are many busy people near me who may not have the time to walk their dog every day.',
    'I want to find clients that live nearby and have well-behaved dogs to be walked several times per week. If a dog gets along well with other dogs then I can walk several at once which is best for profit.'
) ON CONFLICT (email) DO NOTHING;

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at
CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON clients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_forms_updated_at BEFORE UPDATE ON forms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_lead_sessions_updated_at BEFORE UPDATE ON lead_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();