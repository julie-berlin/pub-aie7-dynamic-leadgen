-- Migration 100: Consolidated Database Schema
-- Complete schema with all tables, indexes, RLS, and relationships
-- Safe to run on fresh database - uses IF NOT EXISTS patterns
-- Replaces migrations 001, 003-008

-- Enable required extensions
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
    -- Legacy logo support (kept for backward compatibility)
    company_logo_url TEXT,
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Forms table with complete configuration
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
    -- Templates and messages
    completion_message_template TEXT,
    unqualified_message TEXT DEFAULT 'Thank you for your time.',
    -- Form status and configuration
    is_active BOOLEAN DEFAULT true,
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'paused', 'archived')),
    settings JSONB DEFAULT '{}',
    theme_config JSONB DEFAULT '{}',
    display_settings JSONB DEFAULT '{
        "showProgress": true,
        "allowBack": true,
        "saveProgress": true,
        "timeLimit": null,
        "redirectUrl": null
    }',
    frontend_metadata JSONB DEFAULT '{}',
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Form questions with enhanced configuration
CREATE TABLE IF NOT EXISTS form_questions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL,
    question_order INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    question_type TEXT DEFAULT 'text',
    input_type TEXT DEFAULT 'text',
    data_type TEXT DEFAULT 'string' CHECK (data_type IN ('string', 'number', 'boolean', 'date', 'email', 'phone', 'url', 'json')),
    options JSONB,
    is_required BOOLEAN DEFAULT false,
    scoring_rubric TEXT,
    category TEXT,
    placeholder_text TEXT,
    validation_rules JSONB DEFAULT '{}',
    conditional_logic JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(form_id, question_id)
);

-- ==== SESSION AND TRACKING TABLES ====

-- Lead sessions with comprehensive tracking
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
    abandonment_detected_at TIMESTAMP WITH TIME ZONE,
    
    -- Device and browser tracking
    user_agent TEXT,
    ip_address INET,
    device_fingerprint TEXT,
    
    -- Analytics metadata
    metadata JSONB DEFAULT '{}'
);

-- Individual question responses
CREATE TABLE IF NOT EXISTS responses (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id UUID REFERENCES lead_sessions(id) ON DELETE CASCADE,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL,
    
    -- Response data
    answer TEXT,
    answer_data JSONB,
    score INTEGER DEFAULT 0,
    
    -- Timing and validation
    response_time_ms INTEGER,
    is_validated BOOLEAN DEFAULT false,
    validation_errors JSONB,
    
    -- Metadata
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- UTM and marketing attribution tracking
CREATE TABLE IF NOT EXISTS tracking_data (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id UUID REFERENCES lead_sessions(id) ON DELETE CASCADE,
    
    -- UTM parameters
    utm_source TEXT,
    utm_medium TEXT,
    utm_campaign TEXT,
    utm_term TEXT,
    utm_content TEXT,
    
    -- Additional tracking
    referrer TEXT,
    landing_page TEXT,
    gclid TEXT,
    fbclid TEXT,
    
    -- Device and location
    device_type TEXT,
    browser_name TEXT,
    browser_version TEXT,
    os_name TEXT,
    os_version TEXT,
    screen_resolution TEXT,
    
    -- Geographic data
    country TEXT,
    region TEXT,
    city TEXT,
    timezone TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Session state snapshots for resumption
CREATE TABLE IF NOT EXISTS session_snapshots (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id UUID REFERENCES lead_sessions(id) ON DELETE CASCADE,
    
    -- State data
    step_number INTEGER NOT NULL,
    form_state JSONB NOT NULL,
    responses_snapshot JSONB,
    score_snapshot INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() + INTERVAL '7 days'
);

-- Final lead outcomes and notifications
CREATE TABLE IF NOT EXISTS lead_outcomes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id UUID REFERENCES lead_sessions(id) ON DELETE CASCADE,
    client_id UUID REFERENCES clients(id) ON DELETE SET NULL,
    form_id UUID REFERENCES forms(id) ON DELETE SET NULL,
    
    -- Outcome data
    final_status TEXT NOT NULL CHECK (final_status IN ('qualified', 'maybe', 'unqualified')),
    contact_info JSONB,
    lead_score INTEGER NOT NULL,
    confidence_score DECIMAL(3,2) DEFAULT 0.00,
    
    -- Notification tracking
    notification_sent BOOLEAN DEFAULT false,
    notification_method TEXT,
    notification_sent_at TIMESTAMP WITH TIME ZONE,
    
    -- Follow-up tracking
    follow_up_required BOOLEAN DEFAULT false,
    follow_up_date DATE,
    follow_up_notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==== FILE UPLOAD TABLES ====

-- Uploaded files metadata tracking
CREATE TABLE IF NOT EXISTS uploaded_files (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    
    -- File identification
    filename TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    file_type TEXT NOT NULL CHECK (file_type IN ('logo', 'favicon', 'image', 'document')),
    
    -- File metadata
    size_bytes INTEGER NOT NULL,
    mime_type TEXT NOT NULL,
    file_hash TEXT NOT NULL, -- SHA256 hash for integrity verification
    
    -- Storage information
    storage_path TEXT NOT NULL, -- Relative path from uploads directory
    url TEXT NOT NULL, -- Public URL to access the file
    
    -- Upload tracking
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    uploaded_by UUID, -- Future: reference to admin_users when available
    
    -- File status
    is_active BOOLEAN DEFAULT true,
    deleted_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==== ADMIN AND THEMING TABLES ====

-- Client themes for reusable styling
CREATE TABLE IF NOT EXISTS client_themes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    theme_config JSONB NOT NULL DEFAULT '{}',
    is_default BOOLEAN DEFAULT false,
    is_system_theme BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(client_id, name)
);

-- Client settings and preferences
CREATE TABLE IF NOT EXISTS client_settings (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE UNIQUE,
    
    -- Branding assets
    logo_url TEXT,
    favicon_url TEXT,
    logo_file_id UUID REFERENCES uploaded_files(id) ON DELETE SET NULL,
    favicon_file_id UUID REFERENCES uploaded_files(id) ON DELETE SET NULL,
    brand_colors JSONB DEFAULT '{}',
    font_preferences JSONB DEFAULT '{}',
    
    -- Default settings
    default_theme_id UUID REFERENCES client_themes(id) ON DELETE SET NULL,
    default_form_settings JSONB DEFAULT '{}',
    
    -- Domain configuration
    custom_domain TEXT,
    custom_domain_verified BOOLEAN DEFAULT false,
    ssl_enabled BOOLEAN DEFAULT false,
    
    -- Notification preferences
    notification_settings JSONB DEFAULT '{
        "email_notifications": true,
        "webhook_notifications": false,
        "slack_notifications": false
    }',
    
    -- Analytics settings
    analytics_enabled BOOLEAN DEFAULT true,
    analytics_settings JSONB DEFAULT '{}',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Admin users for client management
CREATE TABLE IF NOT EXISTS admin_users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    
    -- User details
    email TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT DEFAULT 'admin' CHECK (role IN ('admin', 'editor', 'viewer')),
    
    -- Permissions
    permissions JSONB DEFAULT '["read", "write"]',
    
    -- Account status
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    last_login_at TIMESTAMP WITH TIME ZONE,
    login_count INTEGER DEFAULT 0,
    
    -- Security
    password_hash TEXT,
    password_reset_token TEXT,
    password_reset_expires_at TIMESTAMP WITH TIME ZONE,
    email_verification_token TEXT,
    email_verification_expires_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==== ANALYTICS TABLES ====

-- Form analytics events
CREATE TABLE IF NOT EXISTS form_analytics_events (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    session_id UUID REFERENCES lead_sessions(id) ON DELETE SET NULL,
    event_type TEXT NOT NULL CHECK (event_type IN ('view', 'start', 'step_complete', 'abandon', 'complete')),
    step_number INTEGER,
    question_id INTEGER,
    event_data JSONB DEFAULT '{}',
    user_agent TEXT,
    ip_address INET,
    referrer TEXT,
    device_type TEXT,
    browser_name TEXT,
    os_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Form performance metrics
CREATE TABLE IF NOT EXISTS form_performance_metrics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    date_recorded DATE NOT NULL DEFAULT CURRENT_DATE,
    total_views INTEGER DEFAULT 0,
    total_starts INTEGER DEFAULT 0,
    total_completions INTEGER DEFAULT 0,
    total_abandons INTEGER DEFAULT 0,
    avg_completion_time_seconds INTEGER DEFAULT 0,
    conversion_rate DECIMAL(5,4) DEFAULT 0.0000,
    abandonment_rate DECIMAL(5,4) DEFAULT 0.0000,
    bounce_rate DECIMAL(5,4) DEFAULT 0.0000,
    mobile_views INTEGER DEFAULT 0,
    desktop_views INTEGER DEFAULT 0,
    tablet_views INTEGER DEFAULT 0,
    top_referrers JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(form_id, date_recorded)
);

-- Question-level analytics
CREATE TABLE IF NOT EXISTS question_analytics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL,
    date_recorded DATE NOT NULL DEFAULT CURRENT_DATE,
    times_shown INTEGER DEFAULT 0,
    times_answered INTEGER DEFAULT 0,
    times_skipped INTEGER DEFAULT 0,
    avg_time_spent_seconds INTEGER DEFAULT 0,
    response_rate DECIMAL(5,4) DEFAULT 0.0000,
    abandonment_at_question INTEGER DEFAULT 0,
    common_responses JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(form_id, question_id, date_recorded)
);

-- A/B testing variants
CREATE TABLE IF NOT EXISTS form_variants (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    variant_name TEXT NOT NULL,
    variant_config JSONB NOT NULL DEFAULT '{}',
    traffic_percentage INTEGER DEFAULT 50 CHECK (traffic_percentage >= 0 AND traffic_percentage <= 100),
    is_active BOOLEAN DEFAULT true,
    start_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    end_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(form_id, variant_name)
);

-- A/B test assignments tracking
CREATE TABLE IF NOT EXISTS ab_test_assignments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id UUID REFERENCES lead_sessions(id) ON DELETE CASCADE,
    form_id UUID REFERENCES forms(id) ON DELETE CASCADE,
    variant_id UUID REFERENCES form_variants(id) ON DELETE SET NULL,
    variant_name TEXT NOT NULL,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(session_id, form_id)
);

-- ==== INDEXES FOR PERFORMANCE ====

-- Core table indexes
CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email);
CREATE INDEX IF NOT EXISTS idx_forms_client_id ON forms(client_id);
CREATE INDEX IF NOT EXISTS idx_forms_active ON forms(is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_forms_status ON forms(status);
CREATE INDEX IF NOT EXISTS idx_form_questions_form_id ON form_questions(form_id);
CREATE INDEX IF NOT EXISTS idx_form_questions_order ON form_questions(form_id, question_order);

-- Session and response indexes
CREATE INDEX IF NOT EXISTS idx_lead_sessions_form_id ON lead_sessions(form_id);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_session_id ON lead_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_client_id ON lead_sessions(client_id);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_status ON lead_sessions(lead_status);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_completed ON lead_sessions(completed);
CREATE INDEX IF NOT EXISTS idx_lead_sessions_started_at ON lead_sessions(started_at);

CREATE INDEX IF NOT EXISTS idx_responses_session_id ON responses(session_id);
CREATE INDEX IF NOT EXISTS idx_responses_form_id ON responses(form_id);
CREATE INDEX IF NOT EXISTS idx_responses_question_id ON responses(form_id, question_id);

-- Tracking and analytics indexes
CREATE INDEX IF NOT EXISTS idx_tracking_data_session_id ON tracking_data(session_id);
CREATE INDEX IF NOT EXISTS idx_tracking_data_utm_source ON tracking_data(utm_source);
CREATE INDEX IF NOT EXISTS idx_session_snapshots_session_id ON session_snapshots(session_id);
CREATE INDEX IF NOT EXISTS idx_session_snapshots_expires ON session_snapshots(expires_at);

CREATE INDEX IF NOT EXISTS idx_lead_outcomes_session_id ON lead_outcomes(session_id);
CREATE INDEX IF NOT EXISTS idx_lead_outcomes_client_id ON lead_outcomes(client_id);
CREATE INDEX IF NOT EXISTS idx_lead_outcomes_status ON lead_outcomes(final_status);

-- File upload indexes
CREATE INDEX IF NOT EXISTS idx_uploaded_files_client_id ON uploaded_files(client_id);
CREATE INDEX IF NOT EXISTS idx_uploaded_files_type ON uploaded_files(file_type);
CREATE INDEX IF NOT EXISTS idx_uploaded_files_active ON uploaded_files(client_id, is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_uploaded_files_hash ON uploaded_files(file_hash);
CREATE UNIQUE INDEX IF NOT EXISTS idx_uploaded_files_unique_per_client 
    ON uploaded_files(client_id, file_type, filename) 
    WHERE is_active = true;

-- Admin and theme indexes
CREATE INDEX IF NOT EXISTS idx_client_themes_client_id ON client_themes(client_id);
CREATE INDEX IF NOT EXISTS idx_client_themes_default ON client_themes(client_id, is_default);
CREATE INDEX IF NOT EXISTS idx_client_settings_client_id ON client_settings(client_id);
CREATE INDEX IF NOT EXISTS idx_client_settings_logo_file_id ON client_settings(logo_file_id);
CREATE INDEX IF NOT EXISTS idx_client_settings_favicon_file_id ON client_settings(favicon_file_id);
CREATE INDEX IF NOT EXISTS idx_admin_users_client_id ON admin_users(client_id);
CREATE INDEX IF NOT EXISTS idx_admin_users_email ON admin_users(email);
CREATE INDEX IF NOT EXISTS idx_admin_users_active ON admin_users(is_active) WHERE is_active = true;

-- Analytics indexes
CREATE INDEX IF NOT EXISTS idx_form_analytics_events_form_id ON form_analytics_events(form_id);
CREATE INDEX IF NOT EXISTS idx_form_analytics_events_session_id ON form_analytics_events(session_id);
CREATE INDEX IF NOT EXISTS idx_form_analytics_events_type ON form_analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_form_analytics_events_created ON form_analytics_events(created_at);

CREATE INDEX IF NOT EXISTS idx_form_performance_metrics_form_id ON form_performance_metrics(form_id);
CREATE INDEX IF NOT EXISTS idx_form_performance_metrics_date ON form_performance_metrics(date_recorded);

CREATE INDEX IF NOT EXISTS idx_question_analytics_form_id ON question_analytics(form_id);
CREATE INDEX IF NOT EXISTS idx_question_analytics_date ON question_analytics(date_recorded);

CREATE INDEX IF NOT EXISTS idx_form_variants_form_id ON form_variants(form_id);
CREATE INDEX IF NOT EXISTS idx_form_variants_active ON form_variants(is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_ab_test_assignments_session_id ON ab_test_assignments(session_id);

-- ==== TRIGGERS FOR UPDATED_AT TIMESTAMPS ====

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply triggers to all tables with updated_at
DROP TRIGGER IF EXISTS update_clients_updated_at ON clients;
CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON clients FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_forms_updated_at ON forms;
CREATE TRIGGER update_forms_updated_at BEFORE UPDATE ON forms FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_responses_updated_at ON responses;
CREATE TRIGGER update_responses_updated_at BEFORE UPDATE ON responses FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_uploaded_files_updated_at ON uploaded_files;
CREATE TRIGGER update_uploaded_files_updated_at BEFORE UPDATE ON uploaded_files FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_client_themes_updated_at ON client_themes;
CREATE TRIGGER update_client_themes_updated_at BEFORE UPDATE ON client_themes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_client_settings_updated_at ON client_settings;
CREATE TRIGGER update_client_settings_updated_at BEFORE UPDATE ON client_settings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_admin_users_updated_at ON admin_users;
CREATE TRIGGER update_admin_users_updated_at BEFORE UPDATE ON admin_users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_form_performance_metrics_updated_at ON form_performance_metrics;
CREATE TRIGGER update_form_performance_metrics_updated_at BEFORE UPDATE ON form_performance_metrics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_question_analytics_updated_at ON question_analytics;
CREATE TRIGGER update_question_analytics_updated_at BEFORE UPDATE ON question_analytics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_form_variants_updated_at ON form_variants;
CREATE TRIGGER update_form_variants_updated_at BEFORE UPDATE ON form_variants FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==== COMPREHENSIVE ROW LEVEL SECURITY ====

-- Enable RLS on all tables
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE forms ENABLE ROW LEVEL SECURITY;
ALTER TABLE form_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE responses ENABLE ROW LEVEL SECURITY;
ALTER TABLE tracking_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE session_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_outcomes ENABLE ROW LEVEL SECURITY;
ALTER TABLE uploaded_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE client_themes ENABLE ROW LEVEL SECURITY;
ALTER TABLE client_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE form_analytics_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE form_performance_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE question_analytics ENABLE ROW LEVEL SECURITY;
ALTER TABLE form_variants ENABLE ROW LEVEL SECURITY;
ALTER TABLE ab_test_assignments ENABLE ROW LEVEL SECURITY;

-- SERVICE ROLE POLICIES (Backend gets full access)
CREATE POLICY "Service role full access to clients" ON clients FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to forms" ON forms FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to form_questions" ON form_questions FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to lead_sessions" ON lead_sessions FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to responses" ON responses FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to tracking_data" ON tracking_data FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to session_snapshots" ON session_snapshots FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to lead_outcomes" ON lead_outcomes FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to uploaded_files" ON uploaded_files FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to client_themes" ON client_themes FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to client_settings" ON client_settings FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to admin_users" ON admin_users FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to form_analytics_events" ON form_analytics_events FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to form_performance_metrics" ON form_performance_metrics FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to question_analytics" ON question_analytics FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to form_variants" ON form_variants FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access to ab_test_assignments" ON ab_test_assignments FOR ALL USING (auth.role() = 'service_role');

-- ANONYMOUS USER POLICIES (Survey participants)
-- Allow anonymous users to access what they need for surveys
CREATE POLICY "Anonymous can view active forms" ON forms FOR SELECT
    USING (auth.role() = 'anon' AND is_active = true);

CREATE POLICY "Anonymous can view questions for active forms" ON form_questions FOR SELECT
    USING (auth.role() = 'anon' AND EXISTS (
        SELECT 1 FROM forms 
        WHERE forms.id = form_questions.form_id AND forms.is_active = true
    ));

CREATE POLICY "Anonymous can create sessions" ON lead_sessions FOR INSERT
    WITH CHECK (auth.role() = 'anon' AND EXISTS (
        SELECT 1 FROM forms 
        WHERE forms.id = lead_sessions.form_id AND forms.is_active = true
    ));

CREATE POLICY "Anonymous can update sessions" ON lead_sessions FOR UPDATE
    USING (auth.role() = 'anon');

CREATE POLICY "Anonymous can select sessions" ON lead_sessions FOR SELECT
    USING (auth.role() = 'anon');

CREATE POLICY "Anonymous can insert responses" ON responses FOR INSERT
    WITH CHECK (auth.role() = 'anon');

CREATE POLICY "Anonymous can insert tracking_data" ON tracking_data FOR INSERT
    WITH CHECK (auth.role() = 'anon');

CREATE POLICY "Anonymous can insert session_snapshots" ON session_snapshots FOR INSERT
    WITH CHECK (auth.role() = 'anon');

CREATE POLICY "Anonymous can update session_snapshots" ON session_snapshots FOR UPDATE
    USING (auth.role() = 'anon');

-- GRANT PERMISSIONS
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO service_role;

-- Grant permissions for anonymous users (survey participants)
GRANT SELECT ON forms TO anon;
GRANT SELECT ON form_questions TO anon;
GRANT INSERT, UPDATE, SELECT ON lead_sessions TO anon;
GRANT INSERT ON responses TO anon;
GRANT INSERT ON tracking_data TO anon;
GRANT INSERT, UPDATE ON session_snapshots TO anon;

-- Grant permissions for authenticated users (for future client features)
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- ==== TABLE COMMENTS ====
COMMENT ON TABLE uploaded_files IS 'Tracks metadata for all uploaded files including logos, favicons, and other assets';
COMMENT ON COLUMN uploaded_files.file_hash IS 'SHA256 hash of file content for integrity verification and duplicate detection';
COMMENT ON COLUMN uploaded_files.storage_path IS 'Relative path from uploads directory, e.g. clients/{client_id}/logos/{filename}';
COMMENT ON COLUMN uploaded_files.is_active IS 'Soft delete flag - false when file is deleted but record is kept for audit';

COMMENT ON TABLE client_settings IS 'Client-specific settings including branding, themes, and preferences';
COMMENT ON TABLE form_analytics_events IS 'Individual analytics events for detailed tracking';
COMMENT ON TABLE form_performance_metrics IS 'Daily aggregated performance metrics per form';

-- Migration complete
SELECT 'Consolidated database schema implemented successfully!' as status;