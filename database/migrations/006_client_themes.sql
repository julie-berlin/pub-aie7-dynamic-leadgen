-- Migration 006: Add Custom Themes for Each Client
-- This script adds brand-specific themes for each of the 5 existing clients

-- Pawsome Dog Walking - Pet-friendly, friendly blues and oranges
INSERT INTO client_themes (
    id, client_id, name, description, theme_config, is_default, is_system_theme
) VALUES (
    'th111111-1111-1111-1111-111111111111'::uuid,
    'a1111111-1111-1111-1111-111111111111'::uuid,
    'Pawsome Blue',
    'Friendly pet service theme with blue and orange accents',
    '{
        "name": "Pawsome Blue",
        "colors": {
            "primary": "#2563eb",
            "primaryHover": "#1d4ed8",
            "primaryLight": "#dbeafe",
            "secondary": "#f97316",
            "secondaryHover": "#ea580c",
            "secondaryLight": "#fed7aa",
            "accent": "#fbbf24",
            "text": "#1f2937",
            "textLight": "#374151",
            "textMuted": "#6b7280",
            "background": "#ffffff",
            "backgroundLight": "#f8fafc",
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
        "borderRadius": "0.75rem",
        "borderRadiusLg": "1rem",
        "shadow": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
        "shadowLg": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)"
    }'::jsonb,
    true,
    false
) ON CONFLICT (id) DO NOTHING;

-- Metro Realty Group - Professional real estate theme with teal and gold
INSERT INTO client_themes (
    id, client_id, name, description, theme_config, is_default, is_system_theme
) VALUES (
    'th222222-2222-2222-2222-222222222222'::uuid,
    'a2222222-2222-2222-2222-222222222222'::uuid,
    'Metro Professional',
    'Professional real estate theme with teal and gold accents',
    '{
        "name": "Metro Professional",
        "colors": {
            "primary": "#0f766e",
            "primaryHover": "#0d9488",
            "primaryLight": "#ccfbf1",
            "secondary": "#d97706",
            "secondaryHover": "#b45309",
            "secondaryLight": "#fef3c7",
            "accent": "#eab308",
            "text": "#111827",
            "textLight": "#374151",
            "textMuted": "#6b7280",
            "background": "#ffffff",
            "backgroundLight": "#f8fafc",
            "border": "#d1d5db",
            "error": "#dc2626",
            "success": "#059669",
            "warning": "#d97706"
        },
        "typography": {
            "primary": "Inter, ui-sans-serif, system-ui, sans-serif",
            "secondary": "Inter, ui-sans-serif, system-ui, sans-serif"
        },
        "spacing": {
            "section": "2.5rem",
            "element": "1.25rem"
        },
        "borderRadius": "0.375rem",
        "borderRadiusLg": "0.5rem",
        "shadow": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
        "shadowLg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
    }'::jsonb,
    true,
    false
) ON CONFLICT (id) DO NOTHING;

-- TechSolve Consulting - Modern tech theme with purple and cyan
INSERT INTO client_themes (
    id, client_id, name, description, theme_config, is_default, is_system_theme
) VALUES (
    'th333333-3333-3333-3333-333333333333'::uuid,
    'a3333333-3333-3333-3333-333333333333'::uuid,
    'TechSolve Modern',
    'Modern tech consulting theme with purple and cyan accents',
    '{
        "name": "TechSolve Modern",
        "colors": {
            "primary": "#7c3aed",
            "primaryHover": "#6d28d9",
            "primaryLight": "#ede9fe",
            "secondary": "#0891b2",
            "secondaryHover": "#0e7490",
            "secondaryLight": "#cffafe",
            "accent": "#06b6d4",
            "text": "#1f2937",
            "textLight": "#374151",
            "textMuted": "#6b7280",
            "background": "#ffffff",
            "backgroundLight": "#f9fafb",
            "border": "#e5e7eb",
            "error": "#ef4444",
            "success": "#10b981",
            "warning": "#f59e0b"
        },
        "typography": {
            "primary": "Inter, ui-sans-serif, system-ui, sans-serif",
            "secondary": "JetBrains Mono, ui-monospace, monospace"
        },
        "spacing": {
            "section": "3rem",
            "element": "1.5rem"
        },
        "borderRadius": "0.5rem",
        "borderRadiusLg": "0.75rem",
        "shadow": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
        "shadowLg": "0 25px 50px -12px rgb(0 0 0 / 0.25)"
    }'::jsonb,
    true,
    false
) ON CONFLICT (id) DO NOTHING;

-- FitLife Personal Training - Energetic fitness theme with green and red
INSERT INTO client_themes (
    id, client_id, name, description, theme_config, is_default, is_system_theme
) VALUES (
    'th444444-4444-4444-4444-444444444444'::uuid,
    'a4444444-4444-4444-4444-444444444444'::uuid,
    'FitLife Energy',
    'Energetic fitness theme with green and red accents',
    '{
        "name": "FitLife Energy",
        "colors": {
            "primary": "#16a34a",
            "primaryHover": "#15803d",
            "primaryLight": "#dcfce7",
            "secondary": "#dc2626",
            "secondaryHover": "#b91c1c",
            "secondaryLight": "#fecaca",
            "accent": "#eab308",
            "text": "#0f172a",
            "textLight": "#334155",
            "textMuted": "#64748b",
            "background": "#ffffff",
            "backgroundLight": "#f1f5f9",
            "border": "#cbd5e1",
            "error": "#dc2626",
            "success": "#16a34a",
            "warning": "#ea580c"
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
        "borderRadiusLg": "1rem",
        "shadow": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
        "shadowLg": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)"
    }'::jsonb,
    true,
    false
) ON CONFLICT (id) DO NOTHING;

-- Sparkle Clean Solutions - Clean, minimal theme with blue and yellow
INSERT INTO client_themes (
    id, client_id, name, description, theme_config, is_default, is_system_theme
) VALUES (
    'th555555-5555-5555-5555-555555555555'::uuid,
    'a5555555-5555-5555-5555-555555555555'::uuid,
    'Sparkle Clean',
    'Clean and minimal theme with blue and yellow accents',
    '{
        "name": "Sparkle Clean",
        "colors": {
            "primary": "#1e40af",
            "primaryHover": "#1d4ed8",
            "primaryLight": "#dbeafe",
            "secondary": "#fbbf24",
            "secondaryHover": "#f59e0b",
            "secondaryLight": "#fef3c7",
            "accent": "#06b6d4",
            "text": "#1f2937",
            "textLight": "#374151",
            "textMuted": "#9ca3af",
            "background": "#ffffff",
            "backgroundLight": "#f9fafb",
            "border": "#e5e7eb",
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
        "borderRadius": "0.25rem",
        "borderRadiusLg": "0.5rem",
        "shadow": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
        "shadowLg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
    }'::jsonb,
    true,
    false
) ON CONFLICT (id) DO NOTHING;

-- Update each form to use its client's theme
UPDATE forms SET theme_config = (
    SELECT theme_config 
    FROM client_themes 
    WHERE client_themes.client_id = forms.client_id 
    AND client_themes.is_default = true
    LIMIT 1
) WHERE EXISTS (
    SELECT 1 
    FROM client_themes 
    WHERE client_themes.client_id = forms.client_id 
    AND client_themes.is_default = true
);

-- Update the usage count for newly assigned themes
UPDATE client_themes 
SET usage_count = (
    SELECT COUNT(*) 
    FROM forms 
    WHERE forms.client_id = client_themes.client_id
), last_used_at = NOW()
WHERE is_default = true;