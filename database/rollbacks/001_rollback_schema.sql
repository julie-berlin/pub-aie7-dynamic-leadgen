-- Rollback Migration 001: Remove all tables and functions
-- WARNING: This will delete all data! Use with caution.

-- Drop all triggers first
DROP TRIGGER IF EXISTS update_clients_updated_at ON clients;
DROP TRIGGER IF EXISTS update_forms_updated_at ON forms;
DROP TRIGGER IF EXISTS update_lead_sessions_updated_at ON lead_sessions;
DROP TRIGGER IF EXISTS update_lead_sessions_abandonment ON lead_sessions;

-- Drop all functions
DROP FUNCTION IF EXISTS update_updated_at_column();
DROP FUNCTION IF EXISTS calculate_abandonment_risk(TIMESTAMP WITH TIME ZONE);
DROP FUNCTION IF EXISTS update_abandonment_status();
DROP FUNCTION IF EXISTS verify_migration_001();

-- Drop all tables in correct order (respecting foreign keys)
DROP TABLE IF EXISTS session_snapshots CASCADE;
DROP TABLE IF EXISTS lead_outcomes CASCADE;
DROP TABLE IF EXISTS responses CASCADE;
DROP TABLE IF EXISTS tracking_data CASCADE;
DROP TABLE IF EXISTS lead_sessions CASCADE;
DROP TABLE IF EXISTS form_questions CASCADE;
DROP TABLE IF EXISTS forms CASCADE;
DROP TABLE IF EXISTS clients CASCADE;

-- Verification that rollback was successful
SELECT 
    'Rollback complete. Tables removed: ' || 
    string_agg(table_name, ', ')
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN (
    'clients', 'forms', 'form_questions', 'lead_sessions',
    'tracking_data', 'responses', 'lead_outcomes', 'session_snapshots'
);