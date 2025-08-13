-- Migration 003 Rollback: Remove Theme System and Frontend Support
-- CAUTION: This will permanently delete all theme configurations, analytics data, and admin user accounts
-- Only run this if you need to completely rollback Migration 003

-- ==== CONFIRMATION STEP ====
-- Uncomment the next line only if you're absolutely sure you want to rollback
-- SELECT 'WARNING: This will delete all theme and analytics data. Uncomment CONFIRM_ROLLBACK to proceed.' as warning;

DO $$
BEGIN
    -- Check if user confirmed rollback (uncomment the line below to confirm)
    -- IF NOT EXISTS (SELECT 1 WHERE 'CONFIRM_ROLLBACK' = 'CONFIRM_ROLLBACK') THEN
    --     RAISE EXCEPTION 'Rollback not confirmed. Uncomment confirmation line to proceed.';
    -- END IF;
    
    RAISE NOTICE 'Starting Migration 003 rollback...';
END $$;

-- ==== DROP HELPER FUNCTIONS ====
DROP FUNCTION IF EXISTS get_client_default_theme(UUID);
DROP FUNCTION IF EXISTS calculate_form_completion_rate(UUID, DATE, DATE);
DROP FUNCTION IF EXISTS verify_migration_003();
DROP FUNCTION IF EXISTS verify_forms_columns_003();

-- ==== DROP INDEXES ====
-- Theme-related indexes
DROP INDEX IF EXISTS idx_client_themes_client_id;
DROP INDEX IF EXISTS idx_client_themes_is_default;
DROP INDEX IF EXISTS idx_forms_theme_config;

-- Analytics indexes
DROP INDEX IF EXISTS idx_form_analytics_events_session_id;
DROP INDEX IF EXISTS idx_form_analytics_events_form_id;
DROP INDEX IF EXISTS idx_form_analytics_events_type;
DROP INDEX IF EXISTS idx_form_analytics_events_timestamp;
DROP INDEX IF EXISTS idx_form_analytics_events_form_date;

-- Performance metrics indexes
DROP INDEX IF EXISTS idx_form_performance_metrics_form_id;
DROP INDEX IF EXISTS idx_form_performance_metrics_date;
DROP INDEX IF EXISTS idx_form_performance_metrics_period;

-- A/B testing indexes
DROP INDEX IF EXISTS idx_form_variants_form_id;
DROP INDEX IF EXISTS idx_form_variants_active;
DROP INDEX IF EXISTS idx_ab_test_assignments_session;
DROP INDEX IF EXISTS idx_ab_test_assignments_variant;

-- Admin user indexes
DROP INDEX IF EXISTS idx_admin_users_client_id;
DROP INDEX IF EXISTS idx_admin_users_email;
DROP INDEX IF EXISTS idx_admin_users_active;
DROP INDEX IF EXISTS idx_admin_users_verification;
DROP INDEX IF EXISTS idx_admin_users_password_reset;

-- Client settings indexes
DROP INDEX IF EXISTS idx_client_settings_client_id;
DROP INDEX IF EXISTS idx_client_settings_domain;

-- ==== DROP TRIGGERS ====
DROP TRIGGER IF EXISTS update_client_themes_updated_at ON client_themes;
DROP TRIGGER IF EXISTS update_form_variants_updated_at ON form_variants;
DROP TRIGGER IF EXISTS update_admin_users_updated_at ON admin_users;
DROP TRIGGER IF EXISTS update_client_settings_updated_at ON client_settings;

-- ==== DROP TABLES (in reverse dependency order) ====
DROP TABLE IF EXISTS client_settings CASCADE;
DROP TABLE IF EXISTS admin_users CASCADE;
DROP TABLE IF EXISTS ab_test_assignments CASCADE;
DROP TABLE IF EXISTS form_variants CASCADE;
DROP TABLE IF EXISTS form_performance_metrics CASCADE;
DROP TABLE IF EXISTS form_analytics_events CASCADE;
DROP TABLE IF EXISTS client_themes CASCADE;

-- ==== REMOVE COLUMNS FROM EXISTING TABLES ====
-- Remove theme and frontend columns from forms table
DO $$ 
BEGIN
    -- Drop theme_config column
    IF EXISTS (SELECT 1 FROM information_schema.columns 
              WHERE table_name = 'forms' AND column_name = 'theme_config') THEN
        ALTER TABLE forms DROP COLUMN theme_config;
        RAISE NOTICE 'Dropped theme_config column from forms table';
    END IF;
    
    -- Drop display_settings column
    IF EXISTS (SELECT 1 FROM information_schema.columns 
              WHERE table_name = 'forms' AND column_name = 'display_settings') THEN
        ALTER TABLE forms DROP COLUMN display_settings;
        RAISE NOTICE 'Dropped display_settings column from forms table';
    END IF;
    
    -- Drop frontend_metadata column
    IF EXISTS (SELECT 1 FROM information_schema.columns 
              WHERE table_name = 'forms' AND column_name = 'frontend_metadata') THEN
        ALTER TABLE forms DROP COLUMN frontend_metadata;
        RAISE NOTICE 'Dropped frontend_metadata column from forms table';
    END IF;
END $$;

-- ==== VERIFICATION ====
CREATE OR REPLACE FUNCTION verify_rollback_003()
RETURNS TABLE(
    table_name TEXT,
    table_exists BOOLEAN,
    status TEXT
) AS $$
BEGIN
    RETURN QUERY
    WITH dropped_tables AS (
        SELECT unnest(ARRAY[
            'client_themes', 'form_analytics_events', 'form_performance_metrics',
            'form_variants', 'ab_test_assignments', 'admin_users', 'client_settings'
        ]) AS table_name
    )
    SELECT 
        dt.table_name,
        EXISTS(
            SELECT 1 FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND information_schema.tables.table_name = dt.table_name
        ) AS table_exists,
        CASE 
            WHEN EXISTS(
                SELECT 1 FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND information_schema.tables.table_name = dt.table_name
            ) THEN 'ERROR: Table still exists'
            ELSE 'SUCCESS: Table dropped'
        END AS status
    FROM dropped_tables dt
    ORDER BY dt.table_name;
END;
$$ LANGUAGE plpgsql;

-- Check forms table columns were removed
CREATE OR REPLACE FUNCTION verify_forms_rollback_003()
RETURNS TABLE(
    column_name TEXT,
    column_exists BOOLEAN,
    status TEXT
) AS $$
BEGIN
    RETURN QUERY
    WITH dropped_columns AS (
        SELECT unnest(ARRAY[
            'theme_config', 'display_settings', 'frontend_metadata'
        ]) AS column_name
    )
    SELECT 
        dc.column_name,
        EXISTS(
            SELECT 1 FROM information_schema.columns
            WHERE table_schema = 'public' 
            AND table_name = 'forms'
            AND information_schema.columns.column_name = dc.column_name
        ) AS column_exists,
        CASE 
            WHEN EXISTS(
                SELECT 1 FROM information_schema.columns
                WHERE table_schema = 'public' 
                AND table_name = 'forms'
                AND information_schema.columns.column_name = dc.column_name
            ) THEN 'ERROR: Column still exists'
            ELSE 'SUCCESS: Column dropped'
        END AS status
    FROM dropped_columns dc
    ORDER BY dc.column_name;
END;
$$ LANGUAGE plpgsql;

-- Run verification
SELECT 'Migration 003 Rollback Verification:' as verification_type;
SELECT * FROM verify_rollback_003();

SELECT 'Forms Table Rollback Verification:' as verification_type;
SELECT * FROM verify_forms_rollback_003();

-- Clean up verification functions
DROP FUNCTION IF EXISTS verify_rollback_003();
DROP FUNCTION IF EXISTS verify_forms_rollback_003();

RAISE NOTICE 'Migration 003 rollback completed successfully';