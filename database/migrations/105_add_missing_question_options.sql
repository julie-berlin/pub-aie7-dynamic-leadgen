-- Migration 105: Add Missing Question Options
-- Adds options for all radio, select, and checkbox questions that are missing them
-- Based on scoring rubrics and business logic from question_options.csv analysis

-- ==== FITLIFE PERSONAL TRAINING OPTIONS ====

-- Question 3: What is your primary fitness goal?
-- Scoring: Weight loss: +25, Strength building: +25, Injury recovery: +20, General fitness: +10
UPDATE form_questions
SET options = '[
    {"value": "weight_loss", "label": "Weight loss"},
    {"value": "strength_building", "label": "Strength building"},
    {"value": "injury_recovery", "label": "Injury recovery"},
    {"value": "general_fitness", "label": "General fitness"}
]'::jsonb
WHERE form_id = 'f4444444-4444-4444-4444-444444444444'::uuid AND question_id = 3;

-- Question 4: How many sessions per week are you interested in?
-- Scoring: 3+ sessions: +25, 2 sessions: +20, 1 session: +10
UPDATE form_questions
SET options = '[
    {"value": "3_plus", "label": "3+ sessions per week"},
    {"value": "2_sessions", "label": "2 sessions per week"},
    {"value": "1_session", "label": "1 session per week"}
]'::jsonb
WHERE form_id = 'f4444444-4444-4444-4444-444444444444'::uuid AND question_id = 4;

-- Question 5: What is your current fitness level?
-- Scoring: Beginner: +20, Intermediate: +15, Advanced: +5
UPDATE form_questions
SET options = '[
    {"value": "beginner", "label": "Beginner"},
    {"value": "intermediate", "label": "Intermediate"},
    {"value": "advanced", "label": "Advanced"}
]'::jsonb
WHERE form_id = 'f4444444-4444-4444-4444-444444444444'::uuid AND question_id = 5;

-- Question 6: Have you worked with a personal trainer before?
-- Scoring: No: +15, Yes, positive experience: +10, Yes, negative experience: +5
UPDATE form_questions
SET options = '[
    {"value": "no", "label": "No, this would be my first time"},
    {"value": "yes_positive", "label": "Yes, had a positive experience"},
    {"value": "yes_negative", "label": "Yes, but had a negative experience"}
]'::jsonb
WHERE form_id = 'f4444444-4444-4444-4444-444444444444'::uuid AND question_id = 6;

-- Question 7: What is your budget per session?
-- Scoring: $75+: +20, $50-75: +15, $30-50: +10, Under $30: +0
UPDATE form_questions
SET options = '[
    {"value": "75_plus", "label": "$75 or more per session"},
    {"value": "50_75", "label": "$50-75 per session"},
    {"value": "30_50", "label": "$30-50 per session"},
    {"value": "under_30", "label": "Under $30 per session"}
]'::jsonb
WHERE form_id = 'f4444444-4444-4444-4444-444444444444'::uuid AND question_id = 7;

-- Question 8: Do you have any injuries or physical limitations?
-- Scoring: Minor/old injuries: +15, Current injuries: +20, No injuries: +10
UPDATE form_questions
SET options = '[
    {"value": "no_injuries", "label": "No injuries or limitations"},
    {"value": "minor_old", "label": "Minor or old injuries (healed)"},
    {"value": "current_injuries", "label": "Current injuries or limitations"}
]'::jsonb
WHERE form_id = 'f4444444-4444-4444-4444-444444444444'::uuid AND question_id = 8;

-- Question 9: How motivated are you to stick with a fitness program?
-- Scoring: Very motivated: +25, Motivated: +15, Somewhat motivated: +5, Need motivation: +0
UPDATE form_questions
SET options = '[
    {"value": "very_motivated", "label": "Very motivated - I''m committed to change"},
    {"value": "motivated", "label": "Motivated - ready to put in the work"},
    {"value": "somewhat_motivated", "label": "Somewhat motivated - need some guidance"},
    {"value": "need_motivation", "label": "I need help staying motivated"}
]'::jsonb
WHERE form_id = 'f4444444-4444-4444-4444-444444444444'::uuid AND question_id = 9;

-- Question 10: When would you like to start training?
-- Scoring: This week: +20, Within 2 weeks: +15, This month: +10, Not sure: +0
UPDATE form_questions
SET options = '[
    {"value": "this_week", "label": "This week"},
    {"value": "within_2_weeks", "label": "Within 2 weeks"},
    {"value": "this_month", "label": "This month"},
    {"value": "not_sure", "label": "Not sure yet"}
]'::jsonb
WHERE form_id = 'f4444444-4444-4444-4444-444444444444'::uuid AND question_id = 10;

-- ==== METRO REALTY GROUP OPTIONS ====

-- Question 4: Are you looking to buy or sell?
-- Scoring: Buy: +15, Sell: +20, Both: +25
UPDATE form_questions
SET options = '[
    {"value": "buy", "label": "Buy a home"},
    {"value": "sell", "label": "Sell my home"},
    {"value": "both", "label": "Both buy and sell"}
]'::jsonb
WHERE form_id = 'f2222222-2222-2222-2222-222222222222'::uuid AND question_id = 4;

-- Question 5: What is your timeline?
-- Scoring: Within 3 months: +25, 3-6 months: +20, 6-12 months: +10, Just browsing: +0
UPDATE form_questions
SET options = '[
    {"value": "within_3_months", "label": "Within 3 months"},
    {"value": "3_6_months", "label": "3-6 months"},
    {"value": "6_12_months", "label": "6-12 months"},
    {"value": "just_browsing", "label": "Just browsing/exploring"}
]'::jsonb
WHERE form_id = 'f2222222-2222-2222-2222-222222222222'::uuid AND question_id = 5;

-- Question 6: Do you have pre-approval for a mortgage?
-- Scoring: Yes: +20, In process: +15, Planning to get: +10, No/Cash: +25
UPDATE form_questions
SET options = '[
    {"value": "yes_preapproved", "label": "Yes, I have pre-approval"},
    {"value": "in_process", "label": "In process of getting pre-approval"},
    {"value": "planning", "label": "Planning to get pre-approval"},
    {"value": "no_cash", "label": "No (paying cash) or not needed"}
]'::jsonb
WHERE form_id = 'f2222222-2222-2222-2222-222222222222'::uuid AND question_id = 6;

-- Question 7: What is your price range?
-- Scoring: $500K+: +20, $300K-500K: +25, $200K-300K: +15, Under $200K: +5
UPDATE form_questions
SET options = '[
    {"value": "500k_plus", "label": "$500K or more"},
    {"value": "300k_500k", "label": "$300K - $500K"},
    {"value": "200k_300k", "label": "$200K - $300K"},
    {"value": "under_200k", "label": "Under $200K"}
]'::jsonb
WHERE form_id = 'f2222222-2222-2222-2222-222222222222'::uuid AND question_id = 7;

-- Question 8: Which areas interest you most? (checkbox)
-- Scoring: Boston/Cambridge/Somerville: +20, Brookline/Newton: +15, Other metro: +10
UPDATE form_questions
SET options = '[
    {"value": "boston", "label": "Boston"},
    {"value": "cambridge", "label": "Cambridge"},
    {"value": "somerville", "label": "Somerville"},
    {"value": "brookline", "label": "Brookline"},
    {"value": "newton", "label": "Newton"},
    {"value": "other_metro", "label": "Other Boston metro area"}
]'::jsonb
WHERE form_id = 'f2222222-2222-2222-2222-222222222222'::uuid AND question_id = 8;

-- Question 9: Is this your first home purchase?
-- Scoring: Yes: +20 (specialization match), No: +10
UPDATE form_questions
SET options = '[
    {"value": "yes_first_time", "label": "Yes, this is my first home purchase"},
    {"value": "no_experienced", "label": "No, I have bought/sold before"}
]'::jsonb
WHERE form_id = 'f2222222-2222-2222-2222-222222222222'::uuid AND question_id = 9;

-- Question 10: How many bedrooms do you need?
-- Scoring: 2-4 bedrooms: +10, 1 bedroom: +5, 5+: +5
UPDATE form_questions
SET options = '[
    {"value": "1_bedroom", "label": "1 bedroom"},
    {"value": "2_bedrooms", "label": "2 bedrooms"},
    {"value": "3_bedrooms", "label": "3 bedrooms"},
    {"value": "4_bedrooms", "label": "4 bedrooms"},
    {"value": "5_plus", "label": "5+ bedrooms"}
]'::jsonb
WHERE form_id = 'f2222222-2222-2222-2222-222222222222'::uuid AND question_id = 10;

-- Question 11: Have you worked with a realtor before?
-- Scoring: No: +15, Yes, different agent: +10, Yes, same agent: +5
UPDATE form_questions
SET options = '[
    {"value": "no", "label": "No, this would be my first time"},
    {"value": "yes_different", "label": "Yes, with a different agent"},
    {"value": "yes_same", "label": "Yes, with the same agent"}
]'::jsonb
WHERE form_id = 'f2222222-2222-2222-2222-222222222222'::uuid AND question_id = 11;

-- Question 12: What is most important to you in an agent?
-- Scoring: Local expertise: +20, Responsiveness: +15, Experience: +10, Negotiation: +10
UPDATE form_questions
SET options = '[
    {"value": "local_expertise", "label": "Local market expertise"},
    {"value": "responsiveness", "label": "Quick responsiveness"},
    {"value": "experience", "label": "Years of experience"},
    {"value": "negotiation", "label": "Strong negotiation skills"}
]'::jsonb
WHERE form_id = 'f2222222-2222-2222-2222-222222222222'::uuid AND question_id = 12;

-- ==== SPARKLE CLEAN SOLUTIONS OPTIONS ====

-- Question 3: What type of home do you have?
-- Scoring: House: +20, Large apartment: +15, Small apartment: +10
UPDATE form_questions
SET options = '[
    {"value": "house", "label": "House"},
    {"value": "large_apartment", "label": "Large apartment (3+ rooms)"},
    {"value": "small_apartment", "label": "Small apartment (1-2 rooms)"}
]'::jsonb
WHERE form_id = 'f5555555-5555-5555-5555-555555555555'::uuid AND question_id = 3;

-- Question 4: How many bedrooms and bathrooms?
-- Scoring: 3+ bed, 2+ bath: +20, 2 bed, 1-2 bath: +15, 1 bed, 1 bath: +10
UPDATE form_questions
SET options = '[
    {"value": "3bed_2plus_bath", "label": "3+ bedrooms, 2+ bathrooms"},
    {"value": "2bed_1_2bath", "label": "2 bedrooms, 1-2 bathrooms"},
    {"value": "1bed_1bath", "label": "1 bedroom, 1 bathroom"}
]'::jsonb
WHERE form_id = 'f5555555-5555-5555-5555-555555555555'::uuid AND question_id = 4;

-- Question 5: How often would you like cleaning service?
-- Scoring: Weekly: +25, Bi-weekly: +20, Monthly: +10, One-time: +5
UPDATE form_questions
SET options = '[
    {"value": "weekly", "label": "Weekly"},
    {"value": "bi_weekly", "label": "Bi-weekly (every 2 weeks)"},
    {"value": "monthly", "label": "Monthly"},
    {"value": "one_time", "label": "One-time cleaning"}
]'::jsonb
WHERE form_id = 'f5555555-5555-5555-5555-555555555555'::uuid AND question_id = 5;

-- Question 7: Do you prefer eco-friendly cleaning products?
-- Scoring: Strongly prefer: +15, Prefer: +10, No preference: +5
UPDATE form_questions
SET options = '[
    {"value": "strongly_prefer", "label": "Strongly prefer eco-friendly products"},
    {"value": "prefer", "label": "Prefer eco-friendly when possible"},
    {"value": "no_preference", "label": "No strong preference"}
]'::jsonb
WHERE form_id = 'f5555555-5555-5555-5555-555555555555'::uuid AND question_id = 7;

-- Question 8: What is your budget per cleaning?
-- Scoring: $150+: +20, $100-150: +15, $75-100: +10, Under $75: +5
UPDATE form_questions
SET options = '[
    {"value": "150_plus", "label": "$150 or more per cleaning"},
    {"value": "100_150", "label": "$100-150 per cleaning"},
    {"value": "75_100", "label": "$75-100 per cleaning"},
    {"value": "under_75", "label": "Under $75 per cleaning"}
]'::jsonb
WHERE form_id = 'f5555555-5555-5555-5555-555555555555'::uuid AND question_id = 8;

-- Question 9: When would you like to start service?
-- Scoring: This week: +15, Within 2 weeks: +10, This month: +5, Not sure: +0
UPDATE form_questions
SET options = '[
    {"value": "this_week", "label": "This week"},
    {"value": "within_2_weeks", "label": "Within 2 weeks"},
    {"value": "this_month", "label": "This month"},
    {"value": "not_sure", "label": "Not sure yet"}
]'::jsonb
WHERE form_id = 'f5555555-5555-5555-5555-555555555555'::uuid AND question_id = 9;

-- ==== TECHSOLVE CONSULTING OPTIONS ====

-- Question 4: What type of project do you need help with? (checkbox)
-- Scoring: Web development: +20, Mobile app: +15, Cloud migration: +25, DevOps: +20, Other: +5
UPDATE form_questions
SET options = '[
    {"value": "web_development", "label": "Web application development"},
    {"value": "mobile_app", "label": "Mobile app development"},
    {"value": "cloud_migration", "label": "Cloud migration/architecture"},
    {"value": "devops", "label": "DevOps and automation"},
    {"value": "system_modernization", "label": "Legacy system modernization"},
    {"value": "api_integration", "label": "API development/integration"},
    {"value": "other", "label": "Other technical consulting"}
]'::jsonb
WHERE form_id = 'f3333333-3333-3333-3333-333333333333'::uuid AND question_id = 4;

-- Question 5: What is your project timeline?
-- Scoring: ASAP: +25, 1-3 months: +20, 3-6 months: +15, 6+ months: +5
UPDATE form_questions
SET options = '[
    {"value": "asap", "label": "ASAP (urgent)"},
    {"value": "1_3_months", "label": "1-3 months"},
    {"value": "3_6_months", "label": "3-6 months"},
    {"value": "6_plus_months", "label": "6+ months"}
]'::jsonb
WHERE form_id = 'f3333333-3333-3333-3333-333333333333'::uuid AND question_id = 5;

-- Question 6: What is your approximate budget range?
-- Scoring: $25K+: +25, $10K-25K: +20, $5K-10K: +15, Under $5K: +5
UPDATE form_questions
SET options = '[
    {"value": "25k_plus", "label": "$25K or more"},
    {"value": "10k_25k", "label": "$10K - $25K"},
    {"value": "5k_10k", "label": "$5K - $10K"},
    {"value": "under_5k", "label": "Under $5K"}
]'::jsonb
WHERE form_id = 'f3333333-3333-3333-3333-333333333333'::uuid AND question_id = 6;

-- Question 7: Do you have existing technical team members?
-- Scoring: No technical team: +20, Small team: +15, Large team: +5
UPDATE form_questions
SET options = '[
    {"value": "no_technical_team", "label": "No technical team"},
    {"value": "small_team", "label": "Small technical team (1-3 people)"},
    {"value": "large_team", "label": "Large technical team (4+ people)"}
]'::jsonb
WHERE form_id = 'f3333333-3333-3333-3333-333333333333'::uuid AND question_id = 7;

-- Question 8: How many employees does your company have?
-- Scoring: 10-100: +25, 5-10: +20, 100-500: +10, Under 5: +5, 500+: +0
UPDATE form_questions
SET options = '[
    {"value": "10_100", "label": "10-100 employees"},
    {"value": "5_10", "label": "5-10 employees"},
    {"value": "100_500", "label": "100-500 employees"},
    {"value": "under_5", "label": "Under 5 employees"},
    {"value": "500_plus", "label": "500+ employees"}
]'::jsonb
WHERE form_id = 'f3333333-3333-3333-3333-333333333333'::uuid AND question_id = 8;

-- Question 9: Is this project clearly defined?
-- Scoring: Very clear requirements: +20, Mostly clear: +15, Somewhat clear: +10, Need help defining: +5
UPDATE form_questions
SET options = '[
    {"value": "very_clear", "label": "Very clear - detailed requirements ready"},
    {"value": "mostly_clear", "label": "Mostly clear - minor details to work out"},
    {"value": "somewhat_clear", "label": "Somewhat clear - general idea but needs refinement"},
    {"value": "need_help", "label": "Need help defining the requirements"}
]'::jsonb
WHERE form_id = 'f3333333-3333-3333-3333-333333333333'::uuid AND question_id = 9;

-- Question 10: Are you the decision maker for this project?
-- Scoring: Yes, final decision: +20, Yes, with approval: +15, Influence decision: +10, Just researching: +5
UPDATE form_questions
SET options = '[
    {"value": "final_decision", "label": "Yes, I make the final decision"},
    {"value": "with_approval", "label": "Yes, but need approval from others"},
    {"value": "influence", "label": "I influence the decision"},
    {"value": "researching", "label": "Just researching options"}
]'::jsonb
WHERE form_id = 'f3333333-3333-3333-3333-333333333333'::uuid AND question_id = 10;

-- ==== VERIFICATION QUERY ====
-- Run this to verify all radio/select/checkbox questions now have options
SELECT 
    c.name as client_name,
    f.title as form_title,
    fq.question_id,
    fq.input_type,
    CASE 
        WHEN fq.options IS NULL THEN 'Missing Options (NULL)'
        WHEN jsonb_array_length(fq.options) = 0 THEN 'Missing Options (Empty)'
        ELSE CONCAT('Has ', jsonb_array_length(fq.options), ' options')
    END as options_status
FROM form_questions fq
JOIN forms f ON fq.form_id = f.id  
JOIN clients c ON f.client_id = c.id
WHERE fq.input_type IN ('radio', 'select', 'checkbox')
ORDER BY c.name, f.title, fq.question_order;

-- Migration complete
SELECT 'Migration 105: Question options added successfully!' as status;