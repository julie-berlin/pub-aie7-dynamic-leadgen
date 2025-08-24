-- Migration 008: Uploaded Files Table for File Metadata Tracking
-- Adds comprehensive file metadata tracking for uploaded assets like logos and favicons
-- Safe to run multiple times - uses IF NOT EXISTS

-- ==== FILE METADATA TRACKING SCHEMA ====

-- Uploaded files table to track all uploaded assets
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

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_uploaded_files_client_id ON uploaded_files(client_id);
CREATE INDEX IF NOT EXISTS idx_uploaded_files_type ON uploaded_files(file_type);
CREATE INDEX IF NOT EXISTS idx_uploaded_files_active ON uploaded_files(client_id, is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_uploaded_files_hash ON uploaded_files(file_hash); -- For duplicate detection

-- Add unique constraint to prevent duplicate files per client
CREATE UNIQUE INDEX IF NOT EXISTS idx_uploaded_files_unique_per_client 
    ON uploaded_files(client_id, file_type, filename) 
    WHERE is_active = true;

-- Create trigger for updated_at timestamp
CREATE OR REPLACE FUNCTION update_uploaded_files_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_uploaded_files_updated_at ON uploaded_files;
CREATE TRIGGER update_uploaded_files_updated_at 
    BEFORE UPDATE ON uploaded_files 
    FOR EACH ROW EXECUTE FUNCTION update_uploaded_files_updated_at();

-- ==== FOREIGN KEY RELATIONSHIPS ====

-- Add foreign key reference from client_settings to uploaded_files for logo
DO $$ 
BEGIN
    -- Add logo_file_id column to client_settings if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'client_settings' AND column_name = 'logo_file_id') THEN
        ALTER TABLE client_settings ADD COLUMN logo_file_id UUID REFERENCES uploaded_files(id) ON DELETE SET NULL;
    END IF;
    
    -- Add favicon_file_id column to client_settings if it doesn't exist  
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'client_settings' AND column_name = 'favicon_file_id') THEN
        ALTER TABLE client_settings ADD COLUMN favicon_file_id UUID REFERENCES uploaded_files(id) ON DELETE SET NULL;
    END IF;
END $$;

-- Add indexes for the new foreign key columns
CREATE INDEX IF NOT EXISTS idx_client_settings_logo_file_id ON client_settings(logo_file_id);
CREATE INDEX IF NOT EXISTS idx_client_settings_favicon_file_id ON client_settings(favicon_file_id);

-- Add comment for documentation
COMMENT ON TABLE uploaded_files IS 'Tracks metadata for all uploaded files including logos, favicons, and other assets';
COMMENT ON COLUMN uploaded_files.file_hash IS 'SHA256 hash of file content for integrity verification and duplicate detection';
COMMENT ON COLUMN uploaded_files.storage_path IS 'Relative path from uploads directory, e.g. clients/{client_id}/logos/{filename}';
COMMENT ON COLUMN uploaded_files.is_active IS 'Soft delete flag - false when file is deleted but record is kept for audit';