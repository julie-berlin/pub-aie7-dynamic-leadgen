-- Migration 107: Add is_active column to admin_users table
-- Add is_active field and set all existing users to active

-- Add the is_active column with default value of true
ALTER TABLE admin_users 
ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true NOT NULL;

-- Set all existing users to active
UPDATE admin_users 
SET is_active = true 
WHERE is_active IS NULL;

-- Add index for performance
CREATE INDEX IF NOT EXISTS idx_admin_users_is_active ON admin_users(is_active);

-- Add comment
COMMENT ON COLUMN admin_users.is_active IS 'Whether the admin user account is active and can log in';