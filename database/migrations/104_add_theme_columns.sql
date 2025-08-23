-- Migration 104: Add missing theme columns to client_themes table
-- Add columns that the theme API expects but are missing from the schema

-- Add primary_color column
ALTER TABLE client_themes 
ADD COLUMN IF NOT EXISTS primary_color TEXT DEFAULT '#3b82f6';

-- Add secondary_color column  
ALTER TABLE client_themes 
ADD COLUMN IF NOT EXISTS secondary_color TEXT DEFAULT '#6b7280';

-- Add font_family column
ALTER TABLE client_themes 
ADD COLUMN IF NOT EXISTS font_family TEXT DEFAULT 'Inter, system-ui, sans-serif';

-- Add comments for documentation
COMMENT ON COLUMN client_themes.primary_color IS 'Primary brand color for the theme (hex format)';
COMMENT ON COLUMN client_themes.secondary_color IS 'Secondary brand color for the theme (hex format)';
COMMENT ON COLUMN client_themes.font_family IS 'Font family for the theme typography';

-- Create an index on primary_color for potential filtering
CREATE INDEX IF NOT EXISTS idx_client_themes_primary_color ON client_themes(primary_color);