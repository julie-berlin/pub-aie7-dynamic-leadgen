-- Migration 003: Theme System and Frontend Support
-- Adds comprehensive theming, admin users, and analytics support for separate frontend applications
-- Safe to run multiple times - uses IF NOT EXISTS and ADD COLUMN IF NOT EXISTS equivalent patterns

-- ==== PHASE 2.1: Enhanced Form Configuration Schema ====

-- Add theme_config column to forms table
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'forms' AND column_name = 'theme_config') THEN
        ALTER TABLE forms ADD COLUMN theme_config JSONB DEFAULT NULL;
    END IF;
END $$;

-- Add form display settings
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'forms' AND column_name = 'display_settings') THEN
        ALTER TABLE forms ADD COLUMN display_settings JSONB DEFAULT '{
            "showProgress": true,
            "allowBack": true,
            "saveProgress": true,
            "timeLimit": null,
            "redirectUrl": null
        }';
    END IF;
END $$;

-- Add form metadata for frontend support
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'forms' AND column_name = 'frontend_metadata') THEN
        ALTER TABLE forms ADD COLUMN frontend_metadata JSONB DEFAULT '{}';
    END IF;
END $$;

-- Create client_themes table for reusable themes
CREATE TABLE IF NOT EXISTS client_themes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    
    -- Theme identity
    name TEXT NOT NULL,
    description TEXT,
    is_default BOOLEAN DEFAULT false,
    is_system_theme BOOLEAN DEFAULT false,
    
    -- Complete theme configuration
    theme_config JSONB NOT NULL,
    
    -- Theme preview
    preview_image_url TEXT,
    color_palette JSONB, -- Quick reference for main colors
    
    -- Usage tracking
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(client_id, name)
);

-- ==== PHASE 2.2: Analytics and Event Tracking Schema ====

-- Form analytics events for detailed user interaction tracking
CREATE TABLE IF NOT EXISTS form_analytics_events (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT REFERENCES lead_sessions(session_id) ON DELETE CASCADE,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    
    -- Event details
    event_type TEXT NOT NULL, -- 'form_view', 'question_view', 'question_answer', 'form_submit', 'form_abandon', 'step_back', 'step_forward'
    event_category TEXT NOT NULL, -- 'interaction', 'navigation', 'completion', 'error'
    event_action TEXT NOT NULL, -- 'click', 'input', 'focus', 'blur', 'scroll', 'resize'
    event_label TEXT, -- Additional context
    event_value INTEGER, -- Numeric value (time, score, etc.)
    
    -- Context data
    question_id INTEGER,
    step_number INTEGER,
    form_element TEXT, -- Which form element triggered the event
    
    -- Technical context
    viewport_size JSONB, -- {width: 1920, height: 1080}
    device_info JSONB, -- {type: 'desktop', os: 'Windows', browser: 'Chrome'}
    interaction_data JSONB, -- Event-specific data
    
    -- Timing
    event_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    session_duration_ms INTEGER, -- Total session duration when event occurred
    step_duration_ms INTEGER, -- Time spent on current step
    
    -- Performance metrics
    page_load_time_ms INTEGER,
    form_render_time_ms INTEGER
);

-- Form performance metrics (aggregated data)
CREATE TABLE IF NOT EXISTS form_performance_metrics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    
    -- Time period for these metrics
    metric_date DATE NOT NULL,
    metric_period TEXT NOT NULL CHECK (metric_period IN ('daily', 'weekly', 'monthly')),
    
    -- Traffic metrics
    total_views INTEGER DEFAULT 0,
    unique_visitors INTEGER DEFAULT 0,
    returning_visitors INTEGER DEFAULT 0,
    
    -- Completion metrics
    total_starts INTEGER DEFAULT 0,
    total_completions INTEGER DEFAULT 0,
    completion_rate DECIMAL(5,2) DEFAULT 0.00,
    
    -- Time metrics (in seconds)
    avg_completion_time INTEGER DEFAULT 0,
    median_completion_time INTEGER DEFAULT 0,
    avg_time_per_step INTEGER DEFAULT 0,
    
    -- Engagement metrics
    avg_questions_answered INTEGER DEFAULT 0,
    bounce_rate DECIMAL(5,2) DEFAULT 0.00,
    step_dropout_rates JSONB, -- {1: 0.05, 2: 0.08, 3: 0.12, ...}
    
    -- Lead quality metrics
    qualified_leads INTEGER DEFAULT 0,
    unqualified_leads INTEGER DEFAULT 0,
    maybe_leads INTEGER DEFAULT 0,
    avg_lead_score DECIMAL(5,2) DEFAULT 0.00,
    
    -- Device and channel metrics
    device_breakdown JSONB, -- {'desktop': 60, 'mobile': 35, 'tablet': 5}
    traffic_sources JSONB, -- {'organic': 40, 'direct': 30, 'referral': 20, 'social': 10}
    
    -- Performance metrics
    avg_load_time_ms INTEGER DEFAULT 0,
    error_rate DECIMAL(5,2) DEFAULT 0.00,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(form_id, metric_date, metric_period)
);

-- ==== PHASE 2.3: A/B Testing Support Schema ====

-- Form variants for A/B testing
CREATE TABLE IF NOT EXISTS form_variants (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    
    -- Variant details
    variant_name TEXT NOT NULL,
    variant_description TEXT,
    is_control BOOLEAN DEFAULT false,
    
    -- Configuration overrides
    theme_config_override JSONB,
    display_settings_override JSONB,
    questions_override JSONB, -- Can override question text, order, etc.
    
    -- Traffic allocation
    traffic_percentage INTEGER DEFAULT 0 CHECK (traffic_percentage >= 0 AND traffic_percentage <= 100),
    is_active BOOLEAN DEFAULT true,
    
    -- Performance tracking
    total_views INTEGER DEFAULT 0,
    total_completions INTEGER DEFAULT 0,
    conversion_rate DECIMAL(5,2) DEFAULT 0.00,
    
    -- Test period
    test_start_date TIMESTAMP WITH TIME ZONE,
    test_end_date TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(form_id, variant_name)
);

-- A/B test assignments to track which variant each session saw
CREATE TABLE IF NOT EXISTS ab_test_assignments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT REFERENCES lead_sessions(session_id) ON DELETE CASCADE,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    variant_id UUID REFERENCES form_variants(id) ON DELETE CASCADE,
    
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==== PHASE 2.4: Client Management and Admin Users ====

-- Admin users table for client organizations
CREATE TABLE IF NOT EXISTS admin_users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    
    -- User identity
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    
    -- Role and permissions
    role TEXT NOT NULL DEFAULT 'admin' CHECK (role IN ('owner', 'admin', 'editor', 'viewer')),
    permissions JSONB DEFAULT '["forms:read", "analytics:read"]',
    
    -- Account status
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    email_verification_token TEXT,
    
    -- Password reset
    password_reset_token TEXT,
    password_reset_expires TIMESTAMP WITH TIME ZONE,
    
    -- Login tracking
    last_login_at TIMESTAMP WITH TIME ZONE,
    login_count INTEGER DEFAULT 0,
    
    -- Account management
    created_by_user_id UUID REFERENCES admin_users(id) ON DELETE SET NULL,
    invitation_token TEXT,
    invitation_expires TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Client settings and branding
CREATE TABLE IF NOT EXISTS client_settings (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE UNIQUE,
    
    -- Branding assets
    logo_url TEXT,
    favicon_url TEXT,
    brand_colors JSONB, -- Primary brand colors for theme generation
    font_preferences JSONB, -- Default fonts for new forms
    
    -- Default form settings
    default_theme_id UUID REFERENCES client_themes(id) ON DELETE SET NULL,
    default_form_settings JSONB DEFAULT '{}',
    
    -- White-label configuration
    custom_domain TEXT,
    custom_domain_verified BOOLEAN DEFAULT false,
    white_label_enabled BOOLEAN DEFAULT false,
    
    -- Email configuration
    from_email TEXT,
    reply_to_email TEXT,
    email_template_config JSONB DEFAULT '{}',
    
    -- Integration settings
    webhook_url TEXT,
    webhook_secret TEXT,
    api_keys JSONB DEFAULT '{}',
    
    -- Subscription and limits
    plan_type TEXT DEFAULT 'free' CHECK (plan_type IN ('free', 'starter', 'professional', 'enterprise')),
    monthly_form_limit INTEGER DEFAULT 1000,
    monthly_response_limit INTEGER DEFAULT 10000,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==== INDEXES FOR PERFORMANCE ====

-- Theme-related indexes
CREATE INDEX IF NOT EXISTS idx_client_themes_client_id ON client_themes(client_id);
CREATE INDEX IF NOT EXISTS idx_client_themes_is_default ON client_themes(client_id, is_default) WHERE is_default = true;
CREATE INDEX IF NOT EXISTS idx_forms_theme_config ON forms USING gin(theme_config) WHERE theme_config IS NOT NULL;

-- Analytics indexes
CREATE INDEX IF NOT EXISTS idx_form_analytics_events_session_id ON form_analytics_events(session_id);
CREATE INDEX IF NOT EXISTS idx_form_analytics_events_form_id ON form_analytics_events(form_id);
CREATE INDEX IF NOT EXISTS idx_form_analytics_events_type ON form_analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_form_analytics_events_timestamp ON form_analytics_events(event_timestamp);
CREATE INDEX IF NOT EXISTS idx_form_analytics_events_form_date ON form_analytics_events(form_id, event_timestamp);

-- Performance metrics indexes
CREATE INDEX IF NOT EXISTS idx_form_performance_metrics_form_id ON form_performance_metrics(form_id);
CREATE INDEX IF NOT EXISTS idx_form_performance_metrics_date ON form_performance_metrics(metric_date);
CREATE INDEX IF NOT EXISTS idx_form_performance_metrics_period ON form_performance_metrics(form_id, metric_period, metric_date);

-- A/B testing indexes
CREATE INDEX IF NOT EXISTS idx_form_variants_form_id ON form_variants(form_id);
CREATE INDEX IF NOT EXISTS idx_form_variants_active ON form_variants(form_id, is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_ab_test_assignments_session ON ab_test_assignments(session_id);
CREATE INDEX IF NOT EXISTS idx_ab_test_assignments_variant ON ab_test_assignments(variant_id);

-- Admin user indexes
CREATE INDEX IF NOT EXISTS idx_admin_users_client_id ON admin_users(client_id);
CREATE INDEX IF NOT EXISTS idx_admin_users_email ON admin_users(email);
CREATE INDEX IF NOT EXISTS idx_admin_users_active ON admin_users(client_id, is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_admin_users_verification ON admin_users(email_verification_token) WHERE email_verification_token IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_admin_users_password_reset ON admin_users(password_reset_token) WHERE password_reset_token IS NOT NULL;

-- Client settings indexes
CREATE INDEX IF NOT EXISTS idx_client_settings_client_id ON client_settings(client_id);
CREATE INDEX IF NOT EXISTS idx_client_settings_domain ON client_settings(custom_domain) WHERE custom_domain IS NOT NULL;

-- ==== UPDATE EXISTING TRIGGERS ====

-- Add triggers for new tables with updated_at columns
DROP TRIGGER IF EXISTS update_client_themes_updated_at ON client_themes;
CREATE TRIGGER update_client_themes_updated_at BEFORE UPDATE ON client_themes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_form_variants_updated_at ON form_variants;
CREATE TRIGGER update_form_variants_updated_at BEFORE UPDATE ON form_variants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_admin_users_updated_at ON admin_users;
CREATE TRIGGER update_admin_users_updated_at BEFORE UPDATE ON admin_users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_client_settings_updated_at ON client_settings;
CREATE TRIGGER update_client_settings_updated_at BEFORE UPDATE ON client_settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==== HELPER FUNCTIONS FOR THEME MANAGEMENT ====

-- Function to get default theme for a client
CREATE OR REPLACE FUNCTION get_client_default_theme(client_uuid UUID)
RETURNS JSONB AS $$
DECLARE
    default_theme JSONB;
BEGIN
    SELECT theme_config INTO default_theme
    FROM client_themes
    WHERE client_id = client_uuid AND is_default = true
    LIMIT 1;
    
    -- Return system default if no client default exists
    IF default_theme IS NULL THEN
        SELECT theme_config INTO default_theme
        FROM client_themes
        WHERE is_system_theme = true AND name = 'Default Professional'
        LIMIT 1;
    END IF;
    
    -- Fallback to basic theme structure if nothing exists
    IF default_theme IS NULL THEN
        default_theme := '{
            "name": "Default",
            "colors": {
                "primary": "#3b82f6",
                "primaryHover": "#2563eb",
                "primaryLight": "#dbeafe",
                "secondary": "#6b7280",
                "secondaryHover": "#4b5563",
                "secondaryLight": "#f3f4f6",
                "accent": "#f59e0b",
                "text": "#111827",
                "textLight": "#374151",
                "textMuted": "#6b7280",
                "background": "#ffffff",
                "backgroundLight": "#f9fafb",
                "border": "#d1d5db",
                "error": "#ef4444",
                "success": "#10b981",
                "warning": "#f59e0b"
            },
            "typography": {
                "primary": "Inter, ui-sans-serif, system-ui, sans-serif",
                "secondary": "Inter, ui-sans-serif, system-ui, sans-serif"
            },
            "spacing": {
                "section": "2rem",
                "element": "1rem"
            },
            "borderRadius": "0.5rem",
            "borderRadiusLg": "0.75rem",
            "shadow": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
            "shadowLg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
        }'::JSONB;
    END IF;
    
    RETURN default_theme;
END;
$$ LANGUAGE plpgsql;

-- Function to calculate completion rate
CREATE OR REPLACE FUNCTION calculate_form_completion_rate(form_uuid UUID, start_date DATE DEFAULT NULL, end_date DATE DEFAULT NULL)
RETURNS DECIMAL(5,2) AS $$
DECLARE
    total_sessions INTEGER;
    completed_sessions INTEGER;
    completion_rate DECIMAL(5,2);
BEGIN
    -- Set default date range if not provided
    IF start_date IS NULL THEN
        start_date := CURRENT_DATE - INTERVAL '30 days';
    END IF;
    IF end_date IS NULL THEN
        end_date := CURRENT_DATE;
    END IF;
    
    -- Count total sessions
    SELECT COUNT(*) INTO total_sessions
    FROM lead_sessions ls
    WHERE ls.form_id = form_uuid
    AND ls.started_at::DATE BETWEEN start_date AND end_date;
    
    -- Count completed sessions
    SELECT COUNT(*) INTO completed_sessions
    FROM lead_sessions ls
    WHERE ls.form_id = form_uuid
    AND ls.completed = true
    AND ls.started_at::DATE BETWEEN start_date AND end_date;
    
    -- Calculate completion rate
    IF total_sessions > 0 THEN
        completion_rate := (completed_sessions::DECIMAL / total_sessions::DECIMAL) * 100;
    ELSE
        completion_rate := 0.00;
    END IF;
    
    RETURN completion_rate;
END;
$$ LANGUAGE plpgsql;

-- ==== SEED DATA FOR SYSTEM THEMES ====

-- Insert system default themes
INSERT INTO client_themes (id, client_id, name, description, is_default, is_system_theme, theme_config, color_palette)
VALUES 
    (
        uuid_generate_v4(),
        NULL, -- System theme
        'Default Professional',
        'Clean, professional theme suitable for business forms',
        false,
        true,
        '{
            "name": "Default Professional",
            "colors": {
                "primary": "#3b82f6",
                "primaryHover": "#2563eb",
                "primaryLight": "#dbeafe",
                "secondary": "#6b7280",
                "secondaryHover": "#4b5563",
                "secondaryLight": "#f3f4f6",
                "accent": "#f59e0b",
                "text": "#111827",
                "textLight": "#374151",
                "textMuted": "#6b7280",
                "background": "#ffffff",
                "backgroundLight": "#f9fafb",
                "border": "#d1d5db",
                "error": "#ef4444",
                "success": "#10b981",
                "warning": "#f59e0b"
            },
            "typography": {
                "primary": "Inter, ui-sans-serif, system-ui, sans-serif",
                "secondary": "Inter, ui-sans-serif, system-ui, sans-serif"
            },
            "spacing": {
                "section": "2rem",
                "element": "1rem"
            },
            "borderRadius": "0.5rem",
            "borderRadiusLg": "0.75rem",
            "shadow": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
            "shadowLg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
        }',
        '{"primary": "#3b82f6", "secondary": "#6b7280", "accent": "#f59e0b"}'
    ),
    (
        uuid_generate_v4(),
        NULL, -- System theme
        'Modern Minimal',
        'Clean, minimal design with subtle colors',
        false,
        true,
        '{
            "name": "Modern Minimal",
            "colors": {
                "primary": "#1f2937",
                "primaryHover": "#111827",
                "primaryLight": "#f3f4f6",
                "secondary": "#9ca3af",
                "secondaryHover": "#6b7280",
                "secondaryLight": "#f9fafb",
                "accent": "#059669",
                "text": "#111827",
                "textLight": "#374151",
                "textMuted": "#6b7280",
                "background": "#ffffff",
                "backgroundLight": "#f9fafb",
                "border": "#e5e7eb",
                "error": "#dc2626",
                "success": "#059669",
                "warning": "#d97706"
            },
            "typography": {
                "primary": "system-ui, -apple-system, sans-serif",
                "secondary": "system-ui, -apple-system, sans-serif"
            },
            "spacing": {
                "section": "2.5rem",
                "element": "1.25rem"
            },
            "borderRadius": "0.375rem",
            "borderRadiusLg": "0.5rem",
            "shadow": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
            "shadowLg": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -1px rgb(0 0 0 / 0.06)"
        }',
        '{"primary": "#1f2937", "secondary": "#9ca3af", "accent": "#059669"}'
    )
ON CONFLICT DO NOTHING;

-- ==== MIGRATION VERIFICATION ====

-- Update verification function to include new tables
CREATE OR REPLACE FUNCTION verify_migration_003()
RETURNS TABLE(
    table_name TEXT,
    table_exists BOOLEAN,
    column_count INTEGER,
    index_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    WITH required_tables AS (
        SELECT unnest(ARRAY[
            'client_themes', 'form_analytics_events', 'form_performance_metrics',
            'form_variants', 'ab_test_assignments', 'admin_users', 'client_settings'
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
            SELECT COUNT(*) FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = rt.table_name
        )::INTEGER AS column_count,
        (
            SELECT COUNT(*) FROM pg_indexes 
            WHERE schemaname = 'public' 
            AND tablename = rt.table_name
        )::INTEGER AS index_count
    FROM required_tables rt
    ORDER BY rt.table_name;
END;
$$ LANGUAGE plpgsql;

-- Verify new columns were added to forms table
CREATE OR REPLACE FUNCTION verify_forms_columns_003()
RETURNS TABLE(
    column_name TEXT,
    data_type TEXT,
    is_nullable TEXT,
    column_default TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.column_name::TEXT,
        c.data_type::TEXT,
        c.is_nullable::TEXT,
        c.column_default::TEXT
    FROM information_schema.columns c
    WHERE c.table_schema = 'public' 
    AND c.table_name = 'forms'
    AND c.column_name IN ('theme_config', 'display_settings', 'frontend_metadata')
    ORDER BY c.column_name;
END;
$$ LANGUAGE plpgsql;

-- Run verification
SELECT 'Migration 003 Table Verification:' as verification_type;
SELECT * FROM verify_migration_003();

SELECT 'Forms Table Column Verification:' as verification_type;
SELECT * FROM verify_forms_columns_003();

SELECT 'System Themes Count:' as verification_type;
SELECT COUNT(*) as system_theme_count FROM client_themes WHERE is_system_theme = true;