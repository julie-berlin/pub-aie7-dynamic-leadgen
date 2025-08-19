-- Migration 005: Admin Support Schema Enhancements
-- Implements Phase 2 database changes for admin frontend support
-- Adds theme management, analytics tracking, and enhanced client features

-- ==== PHASE 2.1: ENHANCED FORM CONFIGURATION SCHEMA ====

-- Add theme configuration to forms table
ALTER TABLE forms ADD COLUMN IF NOT EXISTS theme_config JSONB DEFAULT '{}';
ALTER TABLE forms ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'paused', 'archived'));
ALTER TABLE forms ADD COLUMN IF NOT EXISTS tags TEXT[] DEFAULT '{}';

-- Create client_themes table for reusable themes
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

-- Add indexes for theme performance
CREATE INDEX IF NOT EXISTS idx_client_themes_client_id ON client_themes(client_id);
CREATE INDEX IF NOT EXISTS idx_client_themes_default ON client_themes(client_id, is_default);

-- ==== PHASE 2.2: ANALYTICS AND TRACKING SCHEMA ====

-- Form analytics events table
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

-- Form performance metrics table
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

-- A/B testing support
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

-- ==== PHASE 2.3: CLIENT MANAGEMENT SCHEMA ====

-- Enhance clients table with admin features
ALTER TABLE clients ADD COLUMN IF NOT EXISTS company_logo_url TEXT;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS primary_color TEXT DEFAULT '#3B82F6';
ALTER TABLE clients ADD COLUMN IF NOT EXISTS secondary_color TEXT DEFAULT '#64748B';
ALTER TABLE clients ADD COLUMN IF NOT EXISTS custom_domain TEXT;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS notification_settings JSONB DEFAULT '{"email_alerts": true, "daily_reports": true, "weekly_summaries": true}';
ALTER TABLE clients ADD COLUMN IF NOT EXISTS subscription_tier TEXT DEFAULT 'starter' CHECK (subscription_tier IN ('starter', 'professional', 'enterprise'));
ALTER TABLE clients ADD COLUMN IF NOT EXISTS monthly_form_limit INTEGER DEFAULT 5;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS monthly_response_limit INTEGER DEFAULT 1000;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true;

-- Client settings and branding table
CREATE TABLE IF NOT EXISTS client_settings (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE UNIQUE,
    logo_url TEXT,
    favicon_url TEXT,
    brand_colors JSONB DEFAULT '{}',
    font_preferences JSONB DEFAULT '{}',
    default_theme_id UUID REFERENCES client_themes(id) ON DELETE SET NULL,
    default_form_settings JSONB DEFAULT '{}',
    custom_domain TEXT,
    custom_domain_verified BOOLEAN DEFAULT false,
    white_label_enabled BOOLEAN DEFAULT false,
    from_email TEXT,
    reply_to_email TEXT,
    webhook_url TEXT,
    plan_type TEXT DEFAULT 'free',
    monthly_form_limit INTEGER DEFAULT 1000,
    monthly_response_limit INTEGER DEFAULT 10000,
    email_templates JSONB DEFAULT '{}',
    webhook_urls JSONB DEFAULT '[]',
    api_keys JSONB DEFAULT '{}',
    integrations JSONB DEFAULT '{}',
    branding_config JSONB DEFAULT '{}',
    custom_css TEXT,
    custom_javascript TEXT,
    footer_text TEXT,
    privacy_policy_url TEXT,
    terms_of_service_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Admin user accounts (comprehensive structure for admin interface)
CREATE TABLE IF NOT EXISTS admin_users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT DEFAULT 'admin' CHECK (role IN ('owner', 'admin', 'editor', 'viewer')),
    permissions JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    last_login_at TIMESTAMP WITH TIME ZONE,
    login_count INTEGER DEFAULT 0,
    invitation_token TEXT,
    invitation_expires TIMESTAMP WITH TIME ZONE,
    created_by_user_id UUID REFERENCES admin_users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==== INDEXES FOR PERFORMANCE ====

-- Analytics indexes
CREATE INDEX IF NOT EXISTS idx_form_analytics_events_form_id ON form_analytics_events(form_id);
CREATE INDEX IF NOT EXISTS idx_form_analytics_events_session_id ON form_analytics_events(session_id);
CREATE INDEX IF NOT EXISTS idx_form_analytics_events_type_date ON form_analytics_events(event_type, created_at);
CREATE INDEX IF NOT EXISTS idx_form_analytics_events_form_date ON form_analytics_events(form_id, created_at);

CREATE INDEX IF NOT EXISTS idx_form_performance_metrics_form_id ON form_performance_metrics(form_id);
CREATE INDEX IF NOT EXISTS idx_form_performance_metrics_date ON form_performance_metrics(date_recorded);

CREATE INDEX IF NOT EXISTS idx_question_analytics_form_id ON question_analytics(form_id);
CREATE INDEX IF NOT EXISTS idx_question_analytics_question_id ON question_analytics(question_id);
CREATE INDEX IF NOT EXISTS idx_question_analytics_date ON question_analytics(date_recorded);

-- Form indexes
CREATE INDEX IF NOT EXISTS idx_forms_status ON forms(status);
CREATE INDEX IF NOT EXISTS idx_forms_client_status ON forms(client_id, status);
CREATE INDEX IF NOT EXISTS idx_forms_tags ON forms USING GIN(tags);

-- Client indexes
CREATE INDEX IF NOT EXISTS idx_clients_subscription_tier ON clients(subscription_tier);
CREATE INDEX IF NOT EXISTS idx_clients_is_active ON clients(is_active);
CREATE INDEX IF NOT EXISTS idx_admin_users_client_id ON admin_users(client_id);
CREATE INDEX IF NOT EXISTS idx_admin_users_email ON admin_users(email);

-- ==== DEFAULT SYSTEM THEMES ====

-- Insert default system themes that all clients can use
INSERT INTO client_themes (id, client_id, name, description, theme_config, is_default, is_system_theme, created_at, updated_at) 
VALUES 
(
    uuid_generate_v4(),
    NULL, -- System theme, not tied to specific client
    'Professional Blue',
    'Clean, professional theme with blue accents',
    '{
        "colors": {
            "primary": "#3B82F6",
            "secondary": "#64748B",
            "accent": "#10B981",
            "background": "#FFFFFF",
            "surface": "#F8FAFC",
            "text": {
                "primary": "#1E293B",
                "secondary": "#64748B",
                "light": "#94A3B8"
            },
            "border": "#E2E8F0",
            "success": "#10B981",
            "warning": "#F59E0B",
            "error": "#EF4444"
        },
        "typography": {
            "fontFamily": "Inter, system-ui, sans-serif",
            "fontSize": {
                "base": "16px",
                "heading": "24px",
                "small": "14px"
            },
            "fontWeight": {
                "normal": 400,
                "medium": 500,
                "semibold": 600,
                "bold": 700
            }
        },
        "spacing": {
            "section": "2rem",
            "element": "1rem",
            "compact": "0.5rem"
        },
        "borderRadius": "0.5rem",
        "borderRadiusLg": "0.75rem",
        "shadow": "0 1px 3px 0 rgb(0 0 0 / 0.1)",
        "shadowLg": "0 10px 15px -3px rgb(0 0 0 / 0.1)"
    }',
    true,
    true,
    NOW(),
    NOW()
),
(
    uuid_generate_v4(),
    NULL,
    'Modern Green',
    'Fresh, modern theme with green accents',
    '{
        "colors": {
            "primary": "#10B981",
            "secondary": "#6B7280",
            "accent": "#3B82F6",
            "background": "#FFFFFF",
            "surface": "#F9FAFB",
            "text": {
                "primary": "#111827",
                "secondary": "#6B7280",
                "light": "#9CA3AF"
            },
            "border": "#E5E7EB",
            "success": "#10B981",
            "warning": "#F59E0B",
            "error": "#EF4444"
        },
        "typography": {
            "fontFamily": "Inter, system-ui, sans-serif",
            "fontSize": {
                "base": "16px",
                "heading": "24px",
                "small": "14px"
            },
            "fontWeight": {
                "normal": 400,
                "medium": 500,
                "semibold": 600,
                "bold": 700
            }
        },
        "spacing": {
            "section": "2rem",
            "element": "1rem",
            "compact": "0.5rem"
        },
        "borderRadius": "0.5rem",
        "borderRadiusLg": "0.75rem",
        "shadow": "0 1px 3px 0 rgb(0 0 0 / 0.1)",
        "shadowLg": "0 10px 15px -3px rgb(0 0 0 / 0.1)"
    }',
    false,
    true,
    NOW(),
    NOW()
),
(
    uuid_generate_v4(),
    NULL,
    'Elegant Purple',
    'Sophisticated theme with purple and gray tones',
    '{
        "colors": {
            "primary": "#8B5CF6",
            "secondary": "#64748B",
            "accent": "#EC4899",
            "background": "#FFFFFF",
            "surface": "#FAFAFB",
            "text": {
                "primary": "#1F2937",
                "secondary": "#64748B",
                "light": "#9CA3AF"
            },
            "border": "#E5E7EB",
            "success": "#10B981",
            "warning": "#F59E0B",
            "error": "#EF4444"
        },
        "typography": {
            "fontFamily": "Inter, system-ui, sans-serif",
            "fontSize": {
                "base": "16px",
                "heading": "24px",
                "small": "14px"
            },
            "fontWeight": {
                "normal": 400,
                "medium": 500,
                "semibold": 600,
                "bold": 700
            }
        },
        "spacing": {
            "section": "2rem",
            "element": "1rem",
            "compact": "0.5rem"
        },
        "borderRadius": "0.5rem",
        "borderRadiusLg": "0.75rem",
        "shadow": "0 1px 3px 0 rgb(0 0 0 / 0.1)",
        "shadowLg": "0 10px 15px -3px rgb(0 0 0 / 0.1)"
    }',
    false,
    true,
    NOW(),
    NOW()
)
ON CONFLICT DO NOTHING;

-- ==== UPDATED TRIGGERS ====

-- Update triggers for new tables
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers for updated_at columns
CREATE TRIGGER update_client_themes_updated_at BEFORE UPDATE ON client_themes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_form_performance_metrics_updated_at BEFORE UPDATE ON form_performance_metrics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_question_analytics_updated_at BEFORE UPDATE ON question_analytics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_form_variants_updated_at BEFORE UPDATE ON form_variants FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_client_settings_updated_at BEFORE UPDATE ON client_settings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_admin_users_updated_at BEFORE UPDATE ON admin_users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Also add trigger for forms table if it doesn't exist
DROP TRIGGER IF EXISTS update_forms_updated_at ON forms;
CREATE TRIGGER update_forms_updated_at BEFORE UPDATE ON forms FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==== HELPER FUNCTIONS FOR ANALYTICS ====

-- Function to calculate daily form metrics
CREATE OR REPLACE FUNCTION calculate_daily_form_metrics(target_form_id UUID, target_date DATE DEFAULT CURRENT_DATE)
RETURNS VOID AS $$
DECLARE
    metrics_record RECORD;
BEGIN
    -- Calculate metrics for the specified form and date
    SELECT 
        COUNT(CASE WHEN event_type = 'view' THEN 1 END) as total_views,
        COUNT(CASE WHEN event_type = 'start' THEN 1 END) as total_starts,
        COUNT(CASE WHEN event_type = 'complete' THEN 1 END) as total_completions,
        COUNT(CASE WHEN event_type = 'abandon' THEN 1 END) as total_abandons,
        COALESCE(AVG(CASE WHEN event_type = 'complete' THEN EXTRACT(EPOCH FROM (created_at - (
            SELECT MIN(e2.created_at) 
            FROM form_analytics_events e2 
            WHERE e2.session_id = form_analytics_events.session_id 
            AND e2.event_type = 'start'
        ))) END), 0) as avg_completion_time,
        COUNT(CASE WHEN event_data->>'device_type' = 'mobile' THEN 1 END) as mobile_views,
        COUNT(CASE WHEN event_data->>'device_type' = 'desktop' THEN 1 END) as desktop_views,
        COUNT(CASE WHEN event_data->>'device_type' = 'tablet' THEN 1 END) as tablet_views
    INTO metrics_record
    FROM form_analytics_events 
    WHERE form_id = target_form_id 
    AND DATE(created_at) = target_date;

    -- Insert or update metrics
    INSERT INTO form_performance_metrics (
        form_id, 
        date_recorded, 
        total_views, 
        total_starts, 
        total_completions, 
        total_abandons,
        avg_completion_time_seconds,
        conversion_rate,
        abandonment_rate,
        bounce_rate,
        mobile_views,
        desktop_views,
        tablet_views
    ) VALUES (
        target_form_id,
        target_date,
        COALESCE(metrics_record.total_views, 0),
        COALESCE(metrics_record.total_starts, 0),
        COALESCE(metrics_record.total_completions, 0),
        COALESCE(metrics_record.total_abandons, 0),
        COALESCE(metrics_record.avg_completion_time, 0),
        CASE 
            WHEN COALESCE(metrics_record.total_starts, 0) > 0 
            THEN COALESCE(metrics_record.total_completions, 0)::DECIMAL / metrics_record.total_starts 
            ELSE 0 
        END,
        CASE 
            WHEN COALESCE(metrics_record.total_starts, 0) > 0 
            THEN COALESCE(metrics_record.total_abandons, 0)::DECIMAL / metrics_record.total_starts 
            ELSE 0 
        END,
        CASE 
            WHEN COALESCE(metrics_record.total_views, 0) > 0 
            THEN (COALESCE(metrics_record.total_views, 0) - COALESCE(metrics_record.total_starts, 0))::DECIMAL / metrics_record.total_views 
            ELSE 0 
        END,
        COALESCE(metrics_record.mobile_views, 0),
        COALESCE(metrics_record.desktop_views, 0),
        COALESCE(metrics_record.tablet_views, 0)
    )
    ON CONFLICT (form_id, date_recorded) 
    DO UPDATE SET
        total_views = EXCLUDED.total_views,
        total_starts = EXCLUDED.total_starts,
        total_completions = EXCLUDED.total_completions,
        total_abandons = EXCLUDED.total_abandons,
        avg_completion_time_seconds = EXCLUDED.avg_completion_time_seconds,
        conversion_rate = EXCLUDED.conversion_rate,
        abandonment_rate = EXCLUDED.abandonment_rate,
        bounce_rate = EXCLUDED.bounce_rate,
        mobile_views = EXCLUDED.mobile_views,
        desktop_views = EXCLUDED.desktop_views,
        tablet_views = EXCLUDED.tablet_views,
        updated_at = NOW();
END;
$$ LANGUAGE plpgsql;

-- Migration complete
SELECT 'Phase 2 Admin Support Schema completed successfully!' as status;