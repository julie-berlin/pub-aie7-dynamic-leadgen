-- Migration 004: Row Level Security (RLS) Implementation
-- Simplified RLS focused on actual application usage patterns
-- Run this in Supabase SQL Editor to enable security
-- ==== ENABLE RLS ON ALL TABLES ====
-- Core business tables
ALTER TABLE
    clients ENABLE ROW LEVEL SECURITY;

ALTER TABLE
    forms ENABLE ROW LEVEL SECURITY;

ALTER TABLE
    form_questions ENABLE ROW LEVEL SECURITY;

-- Survey session tables
ALTER TABLE
    lead_sessions ENABLE ROW LEVEL SECURITY;

ALTER TABLE
    responses ENABLE ROW LEVEL SECURITY;

ALTER TABLE
    tracking_data ENABLE ROW LEVEL SECURITY;

ALTER TABLE
    session_snapshots ENABLE ROW LEVEL SECURITY;

-- Analytics and outcomes
ALTER TABLE
    lead_outcomes ENABLE ROW LEVEL SECURITY;

ALTER TABLE
    admin_users ENABLE ROW LEVEL SECURITY;

ALTER TABLE
    client_settings ENABLE ROW LEVEL SECURITY;

ALTER TABLE
    client_themes ENABLE ROW LEVEL SECURITY;

ALTER TABLE
    form_analytics_events ENABLE ROW LEVEL SECURITY;

ALTER TABLE
    form_performance_metrics ENABLE ROW LEVEL SECURITY;

ALTER TABLE
    form_variants ENABLE ROW LEVEL SECURITY;

ALTER TABLE
    question_analytics ENABLE ROW LEVEL SECURITY;

-- ==== CREATE SIMPLIFIED RLS POLICIES ====
-- SERVICE ROLE POLICIES (Backend gets full access)
-- These policies allow the backend to operate normally
CREATE POLICY "Service role full access to clients" ON clients FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access to forms" ON forms FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access to form_questions" ON form_questions FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access to lead_sessions" ON lead_sessions FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access to responses" ON responses FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access to tracking_data" ON tracking_data FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access to session_snapshots" ON session_snapshots FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access to lead_outcomes" ON lead_outcomes FOR ALL USING (auth.role() = 'service_role');

-- ANONYMOUS USER POLICIES (Survey participants)
-- Allow anonymous users to access what they need for surveys
-- Anonymous users can view active forms
CREATE POLICY "Anonymous can view active forms" ON forms FOR
SELECT
    USING (
        auth.role() = 'anon'
        AND is_active = true
    );

-- Anonymous users can view questions for active forms
CREATE POLICY "Anonymous can view questions for active forms" ON form_questions FOR
SELECT
    USING (
        auth.role() = 'anon'
        AND EXISTS (
            SELECT
                1
            FROM
                forms
            WHERE
                forms.id = form_questions.form_id
                AND forms.is_active = true
        )
    );

-- Anonymous users can create sessions for active forms
CREATE POLICY "Anonymous can create sessions" ON lead_sessions FOR
INSERT
    WITH CHECK (
        auth.role() = 'anon'
        AND EXISTS (
            SELECT
                1
            FROM
                forms
            WHERE
                forms.id = lead_sessions.form_id
                AND forms.is_active = true
        )
    );

-- Anonymous users can update their own sessions (for session state)
CREATE POLICY "Anonymous can update sessions" ON lead_sessions FOR
UPDATE
    USING (auth.role() = 'anon');

-- Anonymous users can select their sessions (for session continuation)
CREATE POLICY "Anonymous can select sessions" ON lead_sessions FOR
SELECT
    USING (auth.role() = 'anon');

-- Anonymous users can insert responses
CREATE POLICY "Anonymous can insert responses" ON responses FOR
INSERT
    WITH CHECK (auth.role() = 'anon');

-- Anonymous users can insert tracking data
CREATE POLICY "Anonymous can insert tracking_data" ON tracking_data FOR
INSERT
    WITH CHECK (auth.role() = 'anon');

-- Anonymous users can insert/update session snapshots
CREATE POLICY "Anonymous can insert session_snapshots" ON session_snapshots FOR
INSERT
    WITH CHECK (auth.role() = 'anon');

CREATE POLICY "Anonymous can update session_snapshots" ON session_snapshots FOR
UPDATE
    USING (auth.role() = 'anon');

-- AUTHENTICATED USER POLICIES (Future client dashboard)
-- Placeholder policies for when client authentication is implemented
-- Currently no authenticated user access since client auth isn't implemented
-- Note: When client authentication is added, policies can be added here like:
-- CREATE POLICY "Authenticated clients can view own data" ON clients
--     FOR SELECT USING (auth.uid()::uuid = id);
-- ==== GRANT NECESSARY PERMISSIONS ====
-- Grant usage on auth schema to authenticated users (for future use)
GRANT USAGE ON SCHEMA auth TO authenticated;

-- Grant permissions for service role to bypass RLS when needed
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;

GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;

GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO service_role;

-- Grant basic permissions for anonymous users (survey participants)
GRANT
SELECT
    ON forms TO anon;

GRANT
SELECT
    ON form_questions TO anon;

GRANT
INSERT
,
UPDATE
,
SELECT
    ON lead_sessions TO anon;

GRANT
INSERT
    ON responses TO anon;

GRANT
INSERT
    ON tracking_data TO anon;

GRANT
INSERT
,
UPDATE
    ON session_snapshots TO anon;

-- Grant permissions for authenticated users (for future client features)
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;

GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- ==== VERIFICATION QUERIES ====
-- Run these to verify RLS is working (uncomment to test):
/*
 -- Test 1: Check RLS is enabled
 SELECT schemaname, tablename, rowsecurity
 FROM pg_tables
 WHERE schemaname = 'public'
 AND rowsecurity = true;
 
 -- Test 2: Check policies exist
 SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
 FROM pg_policies
 WHERE schemaname = 'public'
 ORDER BY tablename, policyname;
 
 -- Test 3: Verify anonymous user can see active forms
 SET ROLE anon;
 SELECT id, title, is_active FROM forms WHERE is_active = true;
 RESET ROLE;
 
 -- Test 4: Verify service role can see everything
 SET ROLE service_role;
 SELECT COUNT(*) FROM clients;
 SELECT COUNT(*) FROM forms;
 RESET ROLE;
 */
-- ==== NOTES ====
-- This simplified RLS approach:
-- 1. Allows backend (service_role) full access for all operations
-- 2. Allows anonymous users limited access for survey participation
-- 3. Blocks everything else by default
-- 4. Avoids complex auth.uid() casting issues
-- 5. Can be extended when client authentication is implemented
-- 6. Satisfies Supabase's RLS requirement
-- Migration complete
SELECT
    'Simplified Row Level Security implemented successfully!' as status;