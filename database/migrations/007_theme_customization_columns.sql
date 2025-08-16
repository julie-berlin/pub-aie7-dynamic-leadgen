-- Migration 007: Theme Customization Columns
-- Adds dedicated columns for primary/secondary colors and font family to client_themes table
-- This provides easier querying and direct access to commonly used theme properties
-- while preserving the existing JSONB theme_config for complex configurations

-- Add dedicated color and font columns to client_themes table
ALTER TABLE client_themes ADD COLUMN IF NOT EXISTS primary_color TEXT DEFAULT '#3B82F6';
ALTER TABLE client_themes ADD COLUMN IF NOT EXISTS secondary_color TEXT DEFAULT '#64748B';
ALTER TABLE client_themes ADD COLUMN IF NOT EXISTS font_family TEXT DEFAULT 'Inter, system-ui, sans-serif';

-- Add validation constraints for color values (hex format)
ALTER TABLE client_themes ADD CONSTRAINT check_primary_color_format 
    CHECK (primary_color ~ '^#[0-9A-Fa-f]{6}$' OR primary_color ~ '^#[0-9A-Fa-f]{3}$');
    
ALTER TABLE client_themes ADD CONSTRAINT check_secondary_color_format 
    CHECK (secondary_color ~ '^#[0-9A-Fa-f]{6}$' OR secondary_color ~ '^#[0-9A-Fa-f]{3}$');

-- Create index for color-based queries
CREATE INDEX IF NOT EXISTS idx_client_themes_colors ON client_themes(primary_color, secondary_color);
CREATE INDEX IF NOT EXISTS idx_client_themes_font ON client_themes(font_family);

-- Function to extract colors and font from existing theme_config JSONB
-- This helps migrate existing themes to use the new columns
CREATE OR REPLACE FUNCTION extract_theme_properties_to_columns()
RETURNS VOID AS $$
BEGIN
    -- Update existing themes to populate new columns from theme_config JSONB
    UPDATE client_themes 
    SET 
        primary_color = COALESCE(theme_config->'colors'->>'primary', primary_color),
        secondary_color = COALESCE(theme_config->'colors'->>'secondary', secondary_color),
        font_family = COALESCE(theme_config->'typography'->>'fontFamily', font_family)
    WHERE theme_config IS NOT NULL 
    AND jsonb_typeof(theme_config) = 'object';
    
    RAISE NOTICE 'Updated % theme records with extracted color and font properties', 
        (SELECT COUNT(*) FROM client_themes WHERE theme_config IS NOT NULL);
END;
$$ LANGUAGE plpgsql;

-- Run the extraction function to populate new columns for existing themes
SELECT extract_theme_properties_to_columns();

-- Function to sync dedicated columns back to theme_config when columns are updated
-- This ensures backwards compatibility with systems that read from theme_config
CREATE OR REPLACE FUNCTION sync_theme_columns_to_config()
RETURNS TRIGGER AS $$
BEGIN
    -- Update theme_config to include the new column values
    NEW.theme_config = jsonb_set(
        jsonb_set(
            jsonb_set(
                COALESCE(NEW.theme_config, '{}'),
                '{colors,primary}', 
                to_jsonb(NEW.primary_color)
            ),
            '{colors,secondary}', 
            to_jsonb(NEW.secondary_color)
        ),
        '{typography,fontFamily}', 
        to_jsonb(NEW.font_family)
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to keep theme_config in sync with dedicated columns
DROP TRIGGER IF EXISTS sync_theme_columns_trigger ON client_themes;
CREATE TRIGGER sync_theme_columns_trigger 
    BEFORE INSERT OR UPDATE ON client_themes
    FOR EACH ROW EXECUTE FUNCTION sync_theme_columns_to_config();

-- Create a view that provides a unified interface for theme data
CREATE OR REPLACE VIEW theme_summary AS
SELECT 
    id,
    client_id,
    name,
    description,
    primary_color,
    secondary_color,
    font_family,
    is_default,
    is_system_theme,
    theme_config,
    created_at,
    updated_at,
    -- Extract additional colors from theme_config for convenience
    theme_config->'colors'->>'accent' as accent_color,
    theme_config->'colors'->>'background' as background_color,
    theme_config->'colors'->>'surface' as surface_color,
    -- Extract typography details (fix the nested JSONB access)
    theme_config->'typography'->'fontSize'->>'base' as base_font_size,
    theme_config->'typography'->'fontWeight'->>'normal' as normal_font_weight
FROM client_themes;

-- Add helper function to create a new theme with basic customization
CREATE OR REPLACE FUNCTION create_custom_theme(
    p_client_id UUID,
    p_name TEXT,
    p_description TEXT DEFAULT NULL,
    p_primary_color TEXT DEFAULT '#3B82F6',
    p_secondary_color TEXT DEFAULT '#64748B', 
    p_font_family TEXT DEFAULT 'Inter, system-ui, sans-serif'
)
RETURNS UUID AS $$
DECLARE
    theme_id UUID;
BEGIN
    INSERT INTO client_themes (
        client_id,
        name,
        description,
        primary_color,
        secondary_color,
        font_family,
        theme_config
    ) VALUES (
        p_client_id,
        p_name,
        p_description,
        p_primary_color,
        p_secondary_color,
        p_font_family,
        jsonb_build_object(
            'colors', jsonb_build_object(
                'primary', p_primary_color,
                'secondary', p_secondary_color,
                'accent', '#10B981',
                'background', '#FFFFFF',
                'surface', '#F8FAFC',
                'text', jsonb_build_object(
                    'primary', '#1E293B',
                    'secondary', '#64748B',
                    'light', '#94A3B8'
                ),
                'border', '#E2E8F0',
                'success', '#10B981',
                'warning', '#F59E0B',
                'error', '#EF4444'
            ),
            'typography', jsonb_build_object(
                'fontFamily', p_font_family,
                'fontSize', jsonb_build_object(
                    'base', '16px',
                    'heading', '24px',
                    'small', '14px'
                ),
                'fontWeight', jsonb_build_object(
                    'normal', 400,
                    'medium', 500,
                    'semibold', 600,
                    'bold', 700
                )
            ),
            'spacing', jsonb_build_object(
                'section', '2rem',
                'element', '1rem',
                'compact', '0.5rem'
            ),
            'borderRadius', '0.5rem',
            'borderRadiusLg', '0.75rem',
            'shadow', '0 1px 3px 0 rgb(0 0 0 / 0.1)',
            'shadowLg', '0 10px 15px -3px rgb(0 0 0 / 0.1)'
        )
    )
    RETURNING id INTO theme_id;
    
    RETURN theme_id;
END;
$$ LANGUAGE plpgsql;

-- Migration verification function
CREATE OR REPLACE FUNCTION verify_theme_customization_migration()
RETURNS TABLE(
    column_name TEXT,
    column_exists BOOLEAN,
    constraint_exists BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        cols.column_name::TEXT,
        EXISTS(
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = 'client_themes' 
            AND information_schema.columns.column_name = cols.column_name
        ) AS column_exists,
        EXISTS(
            SELECT 1 FROM information_schema.constraint_column_usage ccu
            JOIN information_schema.table_constraints tc ON ccu.constraint_name = tc.constraint_name
            WHERE tc.table_name = 'client_themes' 
            AND ccu.column_name = cols.column_name
        ) AS constraint_exists
    FROM (
        VALUES ('primary_color'), ('secondary_color'), ('font_family')
    ) AS cols(column_name);
END;
$$ LANGUAGE plpgsql;

-- Run verification
SELECT 'Theme customization columns migration completed!' as status;
SELECT * FROM verify_theme_customization_migration();