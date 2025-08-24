-- Debug script to check existing schema
-- Run this to see what columns exist in your tables

-- Check form_questions table structure
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'form_questions' 
ORDER BY ordinal_position;

-- Check if form_questions table exists at all
SELECT table_name 
FROM information_schema.tables 
WHERE table_name = 'form_questions' AND table_schema = 'public';

-- Check all table names in public schema
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;