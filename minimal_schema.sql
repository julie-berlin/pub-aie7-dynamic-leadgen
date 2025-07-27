-- Minimal Schema - Run this if you're getting conflicts
-- Just creates the tables we need without policies

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Clients table
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

-- Lead sessions
CREATE TABLE IF NOT EXISTS lead_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    form_id TEXT NOT NULL,
    session_id TEXT UNIQUE NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    final_score INTEGER DEFAULT 0,
    lead_status TEXT DEFAULT 'unknown',
    completed BOOLEAN DEFAULT false,
    step_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Responses table
CREATE TABLE IF NOT EXISTS responses (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT NOT NULL,
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

-- Insert test client
INSERT INTO clients (name, email, owner, address, background, goals) VALUES (
    'Darlene''s Doggie Daywalks',
    'demo@jkwb.mozmail.com',
    'Darlene Demo',
    '243 School Street, Somerville, MA',
    'Dog walking service',
    'Find local clients with well-behaved dogs'
) ON CONFLICT (email) DO NOTHING;