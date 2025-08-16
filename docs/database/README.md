# Database Population for Dynamic Survey System

## Overview
This directory contains all scripts and documentation needed to set up a complete database with 5 diverse business scenarios for testing the dynamic survey system.

## Files

### Database Scripts
- **`001_initial_schema.sql`** - Complete database schema with all tables, indexes, constraints, and helper functions
- **`002_populate_example_data.sql`** - Populates 5 example businesses with clients, forms, and 50+ questions  
- **`005_admin_support_schema.sql`** - Admin features including client_settings and client_themes tables
- **`007_theme_customization_columns.sql`** - Adds primary_color, secondary_color, and font_family columns for easier theme management
- **`001_rollback_schema.sql`** - Safe rollback script to remove all tables (use with caution)

### Documentation
- **`business_scenarios.md`** - Detailed description of all 5 business scenarios with qualification criteria
- **`README.md`** - This file with setup instructions

### Test Scripts
- **`test_database_population.py`** - Comprehensive test suite for database population
- **`setup_and_test.py`** - Helper script to guide setup and run tests

## Business Scenarios Included

1. **Pawsome Dog Walking** - Pet services, qualification based on location, vaccination, frequency
2. **Metro Realty Group** - Real estate, qualification based on timeline, financing, budget  
3. **TechSolve Consulting** - Software consulting, qualification based on revenue, budget, timeline
4. **FitLife Personal Training** - Health & fitness, qualification based on commitment, budget, goals
5. **Sparkle Clean Solutions** - Home cleaning, qualification based on size, frequency, location

Each business includes:
- Complete client profile with background and goals
- Custom form configuration with scoring thresholds
- 8-12 industry-specific questions with scoring rubrics
- Mix of qualification, contact, and engagement questions

## Setup Instructions

### 1. Database Schema Setup
Open your Supabase SQL Editor and run:
```sql
-- Run this file to create all tables and functions
\i 001_initial_schema.sql
```

### 2. Populate Example Data  
```sql
-- Run this file to populate all 5 business scenarios
\i 002_populate_example_data.sql
```

### 3. Theme Customization Setup (Optional)
For enhanced theme management with dedicated color and font columns:
```sql
-- Run this file to add theme customization columns
\i 007_theme_customization_columns.sql
```

This migration adds:
- `primary_color` column with hex color validation
- `secondary_color` column with hex color validation  
- `font_family` column for typography customization
- Indexes for performance optimization
- Helper functions and views for theme management
- Automatic sync between dedicated columns and JSONB theme_config

### 4. Verify Setup
Run the test script:
```bash
cd /path/to/project
uv run python3 database/test_database_population.py
```

Or use the guided setup:
```bash
uv run python3 database/setup_and_test.py
```

### 4. Environment Configuration
Ensure your `.env` file contains:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_PUBLISHABLE_KEY=your_publishable_key
SUPABASE_SECRET_KEY=your_secret_key
```

## Form IDs for Testing

After setup, you can test the survey system with these form IDs:

```python
form_ids = {
    'dog_walking': 'f1111111-1111-1111-1111-111111111111',
    'real_estate': 'f2222222-2222-2222-2222-222222222222',
    'software_consulting': 'f3333333-3333-3333-3333-333333333333',
    'personal_training': 'f4444444-4444-4444-4444-444444444444',
    'home_cleaning': 'f5555555-5555-5555-5555-555555555555'
}
```

## API Testing Examples

### Start a Survey Session
```bash
curl -X POST http://localhost:8000/api/survey/start \\
  -H "Content-Type: application/json" \\
  -d '{
    "form_id": "f1111111-1111-1111-1111-111111111111",
    "utm_source": "google",
    "utm_campaign": "dog_walking_test"
  }'
```

### Submit Responses
```bash
curl -X POST http://localhost:8000/api/survey/step \\
  -H "Content-Type: application/json" \\
  -d '{
    "session_id": "your_session_id",
    "responses": [
      {
        "question_id": 1,
        "answer": "John Smith"
      }
    ]
  }'
```

## Data Structure

### Clients Table
- 5 diverse business profiles
- Complete contact information
- AI context (background, goals, target audience)

### Forms Table  
- Custom form configurations per business
- Scoring thresholds (yes/maybe/no)
- Completion message templates

### Form Questions Table
- 50+ questions across all forms
- Scoring rubrics for qualification
- Question types: text, select, boolean, textarea, email, phone
- Categories: contact, qualification, engagement, basic_info

### Expected Test Results
After successful setup, the test should show:
- ✅ Database connection successful
- ✅ All 5 businesses load correctly (questions, client info, form config)
- ✅ Scoring logic validated for all forms  
- ✅ Business scenario diversity confirmed

## Troubleshooting

### Common Issues

**"Client info load failed"**
- Ensure you ran `002_populate_example_data.sql`
- Check that form IDs match in your test

**"Connection failed"**
- Verify Supabase environment variables
- Check if database tables exist with `001_initial_schema.sql`

**"Missing fields in questions"**  
- Old data may be loading from JSON fallback
- Clear cache and ensure database has priority

### Reset Database (if needed)
```sql
-- ⚠️  WARNING: This deletes all data
\i 001_rollback_schema.sql
\i 001_initial_schema.sql  
\i 002_populate_example_data.sql
```

## Production Deployment

For production deployment:
1. Run schema migration: `001_initial_schema.sql`
2. Populate with real client data (don't use example data)
3. Set up proper environment variables
4. Enable row-level security policies if using Supabase Auth
5. Monitor performance with provided indexes

## Development Workflow

1. **Make schema changes**: Update `001_initial_schema.sql`
2. **Add new businesses**: Update `002_populate_example_data.sql`
3. **Test changes**: Run `test_database_population.py`
4. **Update documentation**: Keep `business_scenarios.md` current
5. **Validate**: Ensure all tests pass before deployment

This database setup provides a robust foundation for testing and demonstrating the dynamic survey system across multiple business verticals.