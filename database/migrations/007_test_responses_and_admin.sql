-- Migration 007: Add test responses and admin users for complete test data
-- This adds the missing responses data and creates admin users for testing

-- ==== ENSURE ADMIN_USERS TABLE EXISTS WITH REQUIRED COLUMNS ====
-- First ensure the admin_users table exists with the columns we need

-- Add first_name column if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'admin_users' AND column_name = 'first_name') THEN
        ALTER TABLE admin_users ADD COLUMN first_name TEXT DEFAULT 'Admin';
    END IF;
END $$;

-- Add last_name column if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'admin_users' AND column_name = 'last_name') THEN
        ALTER TABLE admin_users ADD COLUMN last_name TEXT DEFAULT 'User';
    END IF;
END $$;

-- Add email_verified column if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'admin_users' AND column_name = 'email_verified') THEN
        ALTER TABLE admin_users ADD COLUMN email_verified BOOLEAN DEFAULT true;
    END IF;
END $$;

-- Remove the old 'name' column if it exists (we use first_name + last_name instead)
DO $$ 
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns 
              WHERE table_name = 'admin_users' AND column_name = 'name') THEN
        ALTER TABLE admin_users DROP COLUMN name;
    END IF;
END $$;

-- Update role check constraint to ensure it accepts the correct values
DO $$
BEGIN
    -- Drop existing constraint if it exists and recreate with correct values
    IF EXISTS (
        SELECT 1 FROM information_schema.check_constraints 
        WHERE constraint_name = 'admin_users_role_check'
    ) THEN
        ALTER TABLE admin_users DROP CONSTRAINT admin_users_role_check;
    END IF;
    
    -- Add the correct role constraint
    ALTER TABLE admin_users ADD CONSTRAINT admin_users_role_check 
    CHECK (role IN ('owner', 'admin', 'editor', 'viewer'));
EXCEPTION
    WHEN duplicate_object THEN
        -- Constraint already exists with correct definition, continue
        NULL;
END $$;

-- Note: tracking_data table has duplicate session_ids, so we'll skip ON CONFLICT for UTM data

-- ==== ADMIN USERS FOR TEST CLIENTS ====
-- Create admin users for each test client so they can see their leads

INSERT INTO admin_users (
    id,
    client_id,
    email,
    password_hash,
    first_name,
    last_name,
    role,
    permissions,
    is_active,
    email_verified
) VALUES
-- Admin for Pawsome Dog Walking
('ad111111-1111-1111-1111-111111111111'::uuid, 'a1111111-1111-1111-1111-111111111111'::uuid,
 'admin@pawsome.test', 'fab7109c90206b33cac42ab3e19bebc7:096328863005a2c7288547252435f2d866518f213af31adb058a15229c78bafe', -- password: secret
 'Darlene', 'Demo', 'owner', 
 '["forms:read", "forms:write", "analytics:read", "leads:read", "leads:write", "settings:read", "settings:write"]'::jsonb,
 true, true),

-- Admin for Metro Realty
('ad222222-2222-2222-2222-222222222222'::uuid, 'a2222222-2222-2222-2222-222222222222'::uuid,
 'admin@metrorealty.test', 'fab7109c90206b33cac42ab3e19bebc7:096328863005a2c7288547252435f2d866518f213af31adb058a15229c78bafe',
 'Michael', 'Thompson', 'owner',
 '["forms:read", "forms:write", "analytics:read", "leads:read", "leads:write", "settings:read", "settings:write"]'::jsonb,
 true, true),

-- Admin for TechSolve Consulting
('ad333333-3333-3333-3333-333333333333'::uuid, 'a3333333-3333-3333-3333-333333333333'::uuid,
 'admin@techsolve.test', 'fab7109c90206b33cac42ab3e19bebc7:096328863005a2c7288547252435f2d866518f213af31adb058a15229c78bafe',
 'Sarah', 'Chen', 'owner',
 '["forms:read", "forms:write", "analytics:read", "leads:read", "leads:write", "settings:read", "settings:write"]'::jsonb,
 true, true),

-- Admin for FitLife Personal Training
('ad444444-4444-4444-4444-444444444444'::uuid, 'a4444444-4444-4444-4444-444444444444'::uuid,
 'admin@fitlife.test', 'fab7109c90206b33cac42ab3e19bebc7:096328863005a2c7288547252435f2d866518f213af31adb058a15229c78bafe',
 'Jason', 'Martinez', 'owner',
 '["forms:read", "forms:write", "analytics:read", "leads:read", "leads:write", "settings:read", "settings:write"]'::jsonb,
 true, true),

-- Admin for Sparkle Clean Solutions
('ad555555-5555-5555-5555-555555555555'::uuid, 'a5555555-5555-5555-5555-555555555555'::uuid,
 'admin@sparkleclean.test', 'fab7109c90206b33cac42ab3e19bebc7:096328863005a2c7288547252435f2d866518f213af31adb058a15229c78bafe',
 'Maria', 'Rodriguez', 'owner',
 '["forms:read", "forms:write", "analytics:read", "leads:read", "leads:write", "settings:read", "settings:write"]'::jsonb,
 true, true)
ON CONFLICT (email) DO NOTHING;

-- ==== RESPONSES DATA FOR QUALIFIED LEADS ====
-- Add responses for the test lead sessions so they appear in the admin interface

-- Dog Walking Lead 1 (sess_dw_001) - Qualified lead
INSERT INTO responses (session_id, question_id, question_text, phrased_question, answer, step, data_type, is_required, score_awarded) VALUES
('sess_dw_001', 1, 'What is your name?', 'Hi there! What should we call you?', 'John Smith', 1, 'text', true, 0),
('sess_dw_001', 2, 'What is your dog''s name and breed?', 'Tell us about your furry friend!', 'Max, Golden Retriever', 1, 'text', false, 5),
('sess_dw_001', 3, 'Where do you live?', 'What neighborhood are you in?', 'Downtown Boston, near Common', 2, 'text', true, 30),
('sess_dw_001', 4, 'How often do you need dog walking?', 'How often would Max need walks?', 'Daily (5+ times/week)', 2, 'text', true, 25),
('sess_dw_001', 5, 'Is your dog up to date on vaccinations?', 'Is Max up to date on all vaccinations?', 'yes', 3, 'boolean', true, 20),
('sess_dw_001', 9, 'What is your email?', 'What''s your email address?', 'john.smith@email.com', 4, 'text', true, 0),
('sess_dw_001', 10, 'What is your phone?', 'Best phone number to reach you?', '617-555-0123', 4, 'text', true, 0);

-- Dog Walking Lead 2 (sess_dw_002) - Qualified lead
INSERT INTO responses (session_id, question_id, question_text, phrased_question, answer, step, data_type, is_required, score_awarded) VALUES
('sess_dw_002', 1, 'What is your name?', 'Hi! What''s your name?', 'Sarah Johnson', 1, 'text', true, 0),
('sess_dw_002', 2, 'What is your dog''s name and breed?', 'Tell us about your pup!', 'Buddy and Luna, both Labs', 1, 'text', false, 5),
('sess_dw_002', 3, 'Where do you live?', 'What area are you located?', 'Back Bay, Boston', 2, 'text', true, 30),
('sess_dw_002', 4, 'How often do you need dog walking?', 'How often do Buddy and Luna need walks?', 'Daily (5+ times/week)', 2, 'text', true, 25),
('sess_dw_002', 5, 'Is your dog up to date on vaccinations?', 'Are both dogs vaccinated?', 'yes', 3, 'boolean', true, 20),
('sess_dw_002', 6, 'Can your dog be walked with others?', 'Do they play well with other dogs?', 'Yes, loves other dogs', 3, 'text', false, 15),
('sess_dw_002', 9, 'What is your email?', 'Email address?', 'sarah.j@email.com', 4, 'text', true, 0);

-- Dog Walking Lead 3 (sess_dw_003) - Maybe lead
INSERT INTO responses (session_id, question_id, question_text, phrased_question, answer, step, data_type, is_required, score_awarded) VALUES
('sess_dw_003', 1, 'What is your name?', 'What''s your name?', 'Mike Chen', 1, 'text', true, 0),
('sess_dw_003', 2, 'What is your dog''s name and breed?', 'Tell us about your dog', 'Charlie, Beagle', 1, 'text', false, 5),
('sess_dw_003', 3, 'Where do you live?', 'Your location?', 'Cambridge, near MIT', 2, 'text', true, 20),
('sess_dw_003', 4, 'How often do you need dog walking?', 'Walk frequency needed?', 'Occasional (1-2 times/week)', 2, 'text', true, 10),
('sess_dw_003', 5, 'Is your dog up to date on vaccinations?', 'Vaccinations current?', 'yes', 3, 'boolean', true, 20),
('sess_dw_003', 9, 'What is your email?', 'Email?', 'mike.c@email.com', 4, 'text', true, 0);

-- Real Estate Lead 1 (sess_re_001) - Qualified lead
INSERT INTO responses (session_id, question_id, question_text, phrased_question, answer, step, data_type, is_required, score_awarded) VALUES
('sess_re_001', 1, 'Are you looking to buy or sell?', 'Are you buying or selling?', 'Buy', 1, 'text', true, 10),
('sess_re_001', 2, 'What is your timeline?', 'When are you looking to move?', 'Soon (1-3 months)', 1, 'text', true, 25),
('sess_re_001', 3, 'What is your budget?', 'What''s your price range?', '$500K-$750K', 2, 'text', false, 20),
('sess_re_001', 4, 'Are you pre-approved?', 'Do you have mortgage pre-approval?', 'Yes, fully pre-approved', 2, 'text', false, 25),
('sess_re_001', 6, 'Which areas are you considering?', 'Preferred neighborhoods?', 'Brooklyn Heights, Park Slope', 3, 'text', true, 10),
('sess_re_001', 9, 'What is your name?', 'Your full name?', 'Jennifer Williams', 4, 'text', true, 0),
('sess_re_001', 10, 'What is your email?', 'Email address?', 'jen.williams@email.com', 4, 'text', true, 0),
('sess_re_001', 11, 'What is your phone?', 'Phone number?', '917-555-0456', 4, 'text', true, 0);

-- Tech Consulting Lead 1 (sess_tc_001) - Qualified lead
INSERT INTO responses (session_id, question_id, question_text, phrased_question, answer, step, data_type, is_required, score_awarded) VALUES
('sess_tc_001', 1, 'Company name and industry?', 'Tell us about your company', 'FinanceFlow Inc, Financial Services', 1, 'text', true, 5),
('sess_tc_001', 2, 'Annual revenue?', 'Company size (revenue)?', '$5M-$20M', 1, 'text', true, 30),
('sess_tc_001', 3, 'Number of employees?', 'How many employees?', '51-200', 2, 'text', false, 25),
('sess_tc_001', 4, 'Technology challenges?', 'What challenges are you facing?', 'Need to migrate legacy systems to cloud, improve data analytics', 2, 'text', true, 10),
('sess_tc_001', 5, 'Project budget?', 'Budget for this project?', '$100K-$250K', 3, 'text', true, 35),
('sess_tc_001', 6, 'Timeline?', 'When do you need to start?', 'Immediately', 3, 'text', true, 30),
('sess_tc_001', 9, 'Your name and title?', 'Your name and role?', 'David Park, CTO', 4, 'text', true, 0),
('sess_tc_001', 10, 'Business email?', 'Email address?', 'david.park@financeflow.com', 4, 'text', true, 0);

-- Fitness Training Lead 1 (sess_ft_001) - Qualified lead
INSERT INTO responses (session_id, question_id, question_text, phrased_question, answer, step, data_type, is_required, score_awarded) VALUES
('sess_ft_001', 1, 'Fitness goals?', 'What are your fitness goals?', 'Weight loss', 1, 'text', true, 20),
('sess_ft_001', 2, 'Training frequency?', 'How often can you train?', '3 days', 1, 'text', true, 20),
('sess_ft_001', 3, 'Monthly budget?', 'Budget for training?', '$400-$600', 2, 'text', true, 20),
('sess_ft_001', 5, 'Current activity level?', 'How active are you now?', 'Lightly active', 3, 'text', false, 5),
('sess_ft_001', 8, 'Your name?', 'What''s your name?', 'Emily Rodriguez', 4, 'text', true, 0),
('sess_ft_001', 9, 'Email?', 'Email address?', 'emily.r@email.com', 4, 'text', true, 0),
('sess_ft_001', 10, 'Phone?', 'Phone number?', '617-555-0789', 4, 'text', true, 0);

-- Cleaning Service Lead 1 (sess_cs_001) - Qualified lead
INSERT INTO responses (session_id, question_id, question_text, phrased_question, answer, step, data_type, is_required, score_awarded) VALUES
('sess_cs_001', 1, 'Home size?', 'How big is your home?', '2000-3000 sq ft', 1, 'text', true, 25),
('sess_cs_001', 2, 'Bedrooms and bathrooms?', 'How many beds/baths?', '3 bedrooms, 2 bathrooms', 1, 'text', true, 5),
('sess_cs_001', 3, 'Cleaning frequency?', 'How often do you need cleaning?', 'Bi-weekly', 2, 'text', true, 25),
('sess_cs_001', 4, 'Budget per cleaning?', 'Budget per visit?', '$150-$200', 2, 'text', true, 25),
('sess_cs_001', 5, 'Location?', 'What neighborhood?', 'Queens, Astoria', 3, 'text', true, 20),
('sess_cs_001', 8, 'Your name?', 'What''s your name?', 'Robert Brown', 4, 'text', true, 0),
('sess_cs_001', 9, 'Contact info?', 'Email and phone?', 'robert.b@email.com, 718-555-0234', 4, 'text', true, 0);

-- ==== UPDATE UTM TRACKING DATA ====
-- Add some UTM tracking data for better analytics

-- Insert tracking data only if sessions don't already have tracking data
INSERT INTO tracking_data (session_id, utm_source, utm_medium, utm_campaign, referrer, landing_page) 
SELECT * FROM (VALUES
  ('sess_dw_001', 'google', 'cpc', 'dog_walking_boston', 'https://google.com', '/forms/dog-walking'),
  ('sess_dw_002', 'facebook', 'social', 'pet_services_q4', 'https://facebook.com', '/forms/dog-walking'),
  ('sess_dw_003', 'yelp', 'referral', 'local_services', 'https://yelp.com', '/forms/dog-walking'),
  ('sess_re_001', 'zillow', 'referral', 'real_estate_leads', 'https://zillow.com', '/forms/real-estate'),
  ('sess_tc_001', 'linkedin', 'social', 'b2b_consulting', 'https://linkedin.com', '/forms/tech-consulting'),
  ('sess_ft_001', 'instagram', 'social', 'fitness_transformation', 'https://instagram.com', '/forms/personal-training'),
  ('sess_cs_001', 'google', 'organic', null, 'https://google.com', '/forms/cleaning-service')
) AS new_data(session_id, utm_source, utm_medium, utm_campaign, referrer, landing_page)
WHERE NOT EXISTS (
  SELECT 1 FROM tracking_data WHERE tracking_data.session_id = new_data.session_id
);

-- ==== VERIFICATION QUERIES ====

SELECT 'Test Admin Users Created:' as info, COUNT(*) as count FROM admin_users WHERE email LIKE '%@%.test';
SELECT 'Test Responses Created:' as info, COUNT(*) as count FROM responses WHERE session_id LIKE 'sess_%';
SELECT 'Test UTM Data Created:' as info, COUNT(*) as count FROM tracking_data WHERE session_id LIKE 'sess_%';

-- Show summary by form
SELECT 
    f.title as form_name,
    COUNT(DISTINCT ls.session_id) as total_sessions,
    COUNT(DISTINCT r.session_id) as sessions_with_responses,
    COUNT(DISTINCT CASE WHEN ls.lead_status = 'yes' THEN ls.session_id END) as qualified_leads,
    COUNT(DISTINCT CASE WHEN ls.lead_status = 'maybe' THEN ls.session_id END) as maybe_leads,
    COUNT(DISTINCT CASE WHEN ls.lead_status = 'no' THEN ls.session_id END) as unqualified_leads
FROM forms f
LEFT JOIN lead_sessions ls ON f.id = ls.form_id
LEFT JOIN responses r ON ls.session_id = r.session_id
WHERE f.client_id IN (
    'a1111111-1111-1111-1111-111111111111',
    'a2222222-2222-2222-2222-222222222222',
    'a3333333-3333-3333-3333-333333333333',
    'a4444444-4444-4444-4444-444444444444',
    'a5555555-5555-5555-5555-555555555555'
)
GROUP BY f.title
ORDER BY f.title;