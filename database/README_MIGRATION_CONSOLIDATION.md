# Database Migration Consolidation

## Overview

The database migrations have been consolidated from 13+ individual migration files into 2 comprehensive migrations for easier management and deployment.

## New Consolidated Migrations

### 100_consolidated_schema.sql
**Complete database schema with all tables, indexes, triggers, and RLS policies**

- ✅ All 17 tables with complete column definitions
- ✅ All indexes for performance optimization  
- ✅ All foreign key relationships
- ✅ Comprehensive Row Level Security (RLS) policies
- ✅ Proper triggers for updated_at timestamps
- ✅ File upload system integration (`uploaded_files` table)
- ✅ Service role and anonymous user permissions
- ✅ Safe to run multiple times (uses IF NOT EXISTS)

### 101_consolidated_test_data.sql
**Complete test data for 5 business scenarios with 52 questions**

- ✅ 5 diverse business clients (dog walking, real estate, consulting, fitness, cleaning)
- ✅ 5 active forms with realistic scoring thresholds
- ✅ 52 form questions with proper input/data types and scoring rubrics
- ✅ Question options for radio/checkbox questions
- ✅ Basic client settings and admin users
- ✅ Safe to run multiple times (uses ON CONFLICT DO NOTHING)

## Key Improvements

### Row Level Security (RLS)
**All tables now have comprehensive RLS enabled:**

- **Service Role**: Full access for backend operations
- **Anonymous Users**: Limited access for survey participation only
- **Authenticated Users**: Full access for future client dashboard features
- **Default Deny**: Everything else is blocked by default

### File Upload System
**Complete integration with persistent file uploads:**

- `uploaded_files` table tracks all file metadata
- SHA256 hash verification for file integrity
- Client isolation with proper foreign key relationships
- Soft delete support with audit trail
- Direct integration with `client_settings` table

### Enhanced Data Types
**Proper typing for better validation:**

- Email fields use `email` data type
- Phone numbers use `phone` data type  
- JSON data properly typed as `jsonb`
- Numeric fields with appropriate constraints
- Timestamp fields with timezone support

## Migration Path

### For Fresh Databases
1. Run `100_consolidated_schema.sql`
2. Run `101_consolidated_test_data.sql`

### For Existing Databases  
**⚠️ IMPORTANT: Backup your database first!**

Option 1 - **Clean Slate (Recommended for Development)**:
```sql
-- Drop all existing tables (DESTRUCTIVE!)
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- Run consolidated migrations
\i 100_consolidated_schema.sql
\i 101_consolidated_test_data.sql
```

Option 2 - **Incremental (Production)**:
- Manually apply missing columns/tables from `100_consolidated_schema.sql`
- Ensure RLS policies are properly configured
- Verify all indexes exist

## Validation Queries

Use the queries in `/database/queries/` to validate your schema:

```sql
-- Check table structure
\i queries/01_schemas.sql

-- Verify constraints
\i queries/02_constraints.sql  

-- Confirm indexes
\i queries/03_indexes.sql
```

## RLS Verification

Test that RLS is working correctly:

```sql
-- Check RLS is enabled on all tables
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' AND rowsecurity = true;

-- Check policies exist
SELECT schemaname, tablename, policyname, roles, cmd
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename, policyname;

-- Test anonymous access (should only see active forms)
SET ROLE anon;
SELECT id, title, is_active FROM forms WHERE is_active = true;
RESET ROLE;
```

## Available Test Data

After running `101_consolidated_test_data.sql`, you'll have:

### Test Form IDs
- `f1111111-1111-1111-1111-111111111111` - Pawsome Dog Walking (10 questions)
- `f2222222-2222-2222-2222-222222222222` - Metro Realty Group (12 questions)  
- `f3333333-3333-3333-3333-333333333333` - TechSolve Consulting (11 questions)
- `f4444444-4444-4444-4444-444444444444` - FitLife Personal Training (10 questions)
- `f5555555-5555-5555-5555-555555555555` - Sparkle Clean Solutions (9 questions)

### Test Client ID
- `a1111111-1111-1111-1111-111111111111` - Used by mock authentication system

### Test API Endpoints
```bash
# Start a survey session
curl -X POST http://localhost:8000/api/survey/start \
  -H "Content-Type: application/json" \
  -d '{"form_id": "f1111111-1111-1111-1111-111111111111"}'

# Validate form exists
curl http://localhost:8000/api/survey/forms/f1111111-1111-1111-1111-111111111111/validate
```

## Legacy Migration Files

The following files are now **deprecated** and replaced by the consolidated migrations:

- ❌ `001_initial_schema.sql` → Use `100_consolidated_schema.sql`
- ❌ `002_populate_example_data.sql` → Use `101_consolidated_test_data.sql`  
- ❌ `003_*.sql` → Integrated into `100_consolidated_schema.sql`
- ❌ `004_*.sql` → Integrated into `100_consolidated_schema.sql`
- ❌ `005_*.sql` → Integrated into `100_consolidated_schema.sql`
- ❌ `006_*.sql` → Integrated into `100_consolidated_schema.sql`
- ❌ `007_*.sql` → Integrated into `100_consolidated_schema.sql`
- ❌ `008_uploaded_files_table.sql` → Integrated into `100_consolidated_schema.sql`

## Benefits of Consolidation

1. **Simplified Deployment**: Only 2 files to manage instead of 13+
2. **No Migration Conflicts**: No more duplicate migration numbers or overlapping changes
3. **Complete RLS Coverage**: All tables properly secured
4. **Better Documentation**: Clear schema with proper comments
5. **Easier Maintenance**: Single source of truth for schema
6. **File Upload Integration**: Persistent uploads with database tracking
7. **Production Ready**: Comprehensive security and performance optimizations

## Next Steps

1. Test the consolidated migrations on your development database
2. Verify all application functionality still works
3. Update deployment scripts to use the new migrations
4. Archive/remove the legacy migration files once verified
5. Update documentation to reference the new migration structure