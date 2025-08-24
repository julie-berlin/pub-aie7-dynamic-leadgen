-- Migration 106: Drop unused company_logo_url column from clients table
-- 
-- This migration removes the legacy company_logo_url column from the clients table
-- since we now use client_settings.logo_url as the single source of truth for logos.

-- Drop the unused company_logo_url column
ALTER TABLE clients DROP COLUMN IF EXISTS company_logo_url;

-- Add a comment explaining the change
COMMENT ON TABLE clients IS 'Client business information. Logo URLs are stored in client_settings table.';