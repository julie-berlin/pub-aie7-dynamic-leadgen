-- Migration 102: Rename business_name to legal_name
-- Changes business_name column to legal_name for better clarity
-- name = display name (e.g., "Pawsome Dog Walking")
-- legal_name = legal business name (e.g., "Pawsome Dog Walking Services LLC")

-- Rename the column
ALTER TABLE clients 
RENAME COLUMN business_name TO legal_name;

-- Add a comment for clarity
COMMENT ON COLUMN clients.name IS 'Display name for the business (used in UI)';
COMMENT ON COLUMN clients.legal_name IS 'Legal business name (for contracts, legal documents)';