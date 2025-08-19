-- Realistic test data for lead_sessions and lead_outcomes tables
-- This creates data spanning the last 90 days for analytics and testing

-- ==== LEAD SESSIONS DATA ====

INSERT INTO lead_sessions (
    id,
    form_id,
    session_id,
    client_id,
    started_at,
    last_updated,
    completed_at,
    step,
    completed,
    current_score,
    final_score,
    lead_status,
    completion_type,
    completion_message,
    abandonment_status,
    abandonment_risk,
    last_activity_timestamp,
    time_on_step,
    hesitation_indicators,
    created_at,
    updated_at
) VALUES

-- ==== DOG WALKING SERVICE (f1111111) ====
-- High quality leads
('00000001-0000-0000-0000-000000000001'::uuid, 'f1111111-1111-1111-1111-111111111111'::uuid, 'sess_dw_001', 'a1111111-1111-1111-1111-111111111111'::uuid, 
 NOW() - INTERVAL '2 hours', NOW() - INTERVAL '10 minutes', NOW() - INTERVAL '10 minutes', 8, true, 
 85, 85, 'yes', 'qualified', 'Perfect! We''d love to walk your well-behaved Golden Retriever daily. Our Psychology background helps us understand dog behavior perfectly.', 
 'active', 0.20, NOW() - INTERVAL '10 minutes', 45, 1, NOW() - INTERVAL '2 hours', NOW() - INTERVAL '10 minutes'),

('00000002-0000-0000-0000-000000000002'::uuid, 'f1111111-1111-1111-1111-111111111111'::uuid, 'sess_dw_002', 'a1111111-1111-1111-1111-111111111111'::uuid, 
 NOW() - INTERVAL '5 hours', NOW() - INTERVAL '3 hours', NOW() - INTERVAL '3 hours', 7, true, 
 92, 92, 'yes', 'qualified', 'Excellent! Your energetic Labrador sounds perfect for our regular walking service. We love active dogs!', 
 'active', 0.15, NOW() - INTERVAL '3 hours', 32, 0, NOW() - INTERVAL '5 hours', NOW() - INTERVAL '3 hours'),

-- Maybe leads  
('00000003-0000-0000-0000-000000000003'::uuid, 'f1111111-1111-1111-1111-111111111111'::uuid, 'sess_dw_003', 'a1111111-1111-1111-1111-111111111111'::uuid, 
 NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day', 6, true, 
 68, 68, 'maybe', 'qualified_fallback', 'We understand budget constraints. Let''s discuss flexible options that might work for your Beagle''s needs.', 
 'active', 0.25, NOW() - INTERVAL '1 day', 78, 2, NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),

('00000004-0000-0000-0000-000000000004'::uuid, 'f1111111-1111-1111-1111-111111111111'::uuid, 'sess_dw_004', 'a1111111-1111-1111-1111-111111111111'::uuid, 
 NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days', 5, true, 
 55, 55, 'maybe', 'qualified_fallback', 'Your mixed breed sounds lovely. We''d be happy to do a trial walk to see how they interact with other dogs.', 
 'active', 0.30, NOW() - INTERVAL '2 days', 95, 3, NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),

-- Poor quality/abandoned leads
('00000005-0000-0000-0000-000000000005'::uuid, 'f1111111-1111-1111-1111-111111111111'::uuid, 'sess_dw_005', 'a1111111-1111-1111-1111-111111111111'::uuid, 
 NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days', 4, true, 
 25, 25, 'no', 'unqualified', 'Thank you for your interest. Unfortunately, we require up-to-date vaccinations for all dogs in our care for everyone''s safety.', 
 'active', 0.35, NOW() - INTERVAL '3 days', 120, 4, NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),

('00000006-0000-0000-0000-000000000006'::uuid, 'f1111111-1111-1111-1111-111111111111'::uuid, 'sess_dw_006', 'a1111111-1111-1111-1111-111111111111'::uuid, 
 NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days', NULL, 3, false, 
 15, 0, 'unknown', 'abandoned', NULL, 
 'abandoned', 0.95, NOW() - INTERVAL '4 days', 45, 1, NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'),

-- ==== REAL ESTATE FORM (f2222222) ====
('00000007-0000-0000-0000-000000000007'::uuid, 'f2222222-2222-2222-2222-222222222222'::uuid, 'sess_re_001', 'a2222222-2222-2222-2222-222222222222'::uuid, 
 NOW() - INTERVAL '1 week', NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days', 9, true, 
 88, 88, 'yes', 'qualified', 'Fantastic! With your budget and timeline, we have several perfect properties in Brooklyn Heights. Let''s schedule a viewing!', 
 'active', 0.18, NOW() - INTERVAL '6 days', 65, 2, NOW() - INTERVAL '1 week', NOW() - INTERVAL '6 days'),

('00000008-0000-0000-0000-000000000008'::uuid, 'f2222222-2222-2222-2222-222222222222'::uuid, 'sess_re_002', 'a2222222-2222-2222-2222-222222222222'::uuid, 
 NOW() - INTERVAL '1 week 2 days', NOW() - INTERVAL '1 week 1 day', NOW() - INTERVAL '1 week 1 day', 8, true, 
 72, 72, 'maybe', 'qualified_fallback', 'We understand you''re exploring options. Let''s keep in touch as the market is moving quickly in Manhattan.', 
 'active', 0.22, NOW() - INTERVAL '1 week 1 day', 105, 3, NOW() - INTERVAL '1 week 2 days', NOW() - INTERVAL '1 week 1 day'),

-- ==== TECH CONSULTING FORM (f3333333) ====
('00000009-0000-0000-0000-000000000009'::uuid, 'f3333333-3333-3333-3333-333333333333'::uuid, 'sess_tc_001', 'a3333333-3333-3333-3333-333333333333'::uuid, 
 NOW() - INTERVAL '2 weeks', NOW() - INTERVAL '10 days', NOW() - INTERVAL '10 days', 10, true, 
 95, 95, 'yes', 'qualified', 'Excellent! Your cloud migration project aligns perfectly with our expertise. We''ve successfully completed 50+ similar migrations.', 
 'active', 0.12, NOW() - INTERVAL '10 days', 55, 1, NOW() - INTERVAL '2 weeks', NOW() - INTERVAL '10 days'),

('00000010-0000-0000-0000-000000000010'::uuid, 'f3333333-3333-3333-3333-333333333333'::uuid, 'sess_tc_002', 'a3333333-3333-3333-3333-333333333333'::uuid, 
 NOW() - INTERVAL '2 weeks 3 days', NOW() - INTERVAL '2 weeks 2 days', NULL, 4, false, 
 30, 0, 'unknown', 'abandoned', NULL, 
 'abandoned', 0.92, NOW() - INTERVAL '2 weeks 2 days', 25, 0, NOW() - INTERVAL '2 weeks 3 days', NOW() - INTERVAL '2 weeks 2 days'),

-- ==== FITNESS TRAINING FORM (f4444444) ====
('00000011-0000-0000-0000-000000000011'::uuid, 'f4444444-4444-4444-4444-444444444444'::uuid, 'sess_ft_001', 'a4444444-4444-4444-4444-444444444444'::uuid, 
 NOW() - INTERVAL '3 weeks', NOW() - INTERVAL '2 weeks 5 days', NOW() - INTERVAL '2 weeks 5 days', 7, true, 
 82, 82, 'yes', 'qualified', 'Perfect! Your fitness goals are exactly what we specialize in. Let''s start with a complimentary assessment session.', 
 'active', 0.19, NOW() - INTERVAL '2 weeks 5 days', 70, 2, NOW() - INTERVAL '3 weeks', NOW() - INTERVAL '2 weeks 5 days'),

('00000012-0000-0000-0000-000000000012'::uuid, 'f4444444-4444-4444-4444-444444444444'::uuid, 'sess_ft_002', 'a4444444-4444-4444-4444-444444444444'::uuid, 
 NOW() - INTERVAL '1 month', NOW() - INTERVAL '3 weeks 2 days', NOW() - INTERVAL '3 weeks 2 days', 6, true, 
 48, 48, 'maybe', 'qualified_fallback', 'We offer flexible scheduling and payment plans. Let''s discuss options that work with your busy lifestyle.', 
 'active', 0.35, NOW() - INTERVAL '3 weeks 2 days', 135, 4, NOW() - INTERVAL '1 month', NOW() - INTERVAL '3 weeks 2 days'),

-- ==== CLEANING SERVICE FORM (f5555555) ====
('00000013-0000-0000-0000-000000000013'::uuid, 'f5555555-5555-5555-5555-555555555555'::uuid, 'sess_cs_001', 'a5555555-5555-5555-5555-555555555555'::uuid, 
 NOW() - INTERVAL '1 month 1 week', NOW() - INTERVAL '1 month 2 days', NOW() - INTERVAL '1 month 2 days', 8, true, 
 78, 78, 'yes', 'qualified', 'Wonderful! Your 3-bedroom home in Queens is perfect for our bi-weekly deep cleaning service. We use eco-friendly products exclusively.', 
 'active', 0.21, NOW() - INTERVAL '1 month 2 days', 52, 1, NOW() - INTERVAL '1 month 1 week', NOW() - INTERVAL '1 month 2 days'),

('00000014-0000-0000-0000-000000000014'::uuid, 'f5555555-5555-5555-5555-555555555555'::uuid, 'sess_cs_002', 'a5555555-5555-5555-5555-555555555555'::uuid, 
 NOW() - INTERVAL '1 month 2 weeks', NOW() - INTERVAL '1 month 1 week 3 days', NOW() - INTERVAL '1 month 1 week 3 days', 5, true, 
 35, 35, 'no', 'unqualified', 'Thank you for your interest. Unfortunately, our service area doesn''t currently extend to Staten Island, but we''re expanding soon!', 
 'active', 0.28, NOW() - INTERVAL '1 month 1 week 3 days', 85, 2, NOW() - INTERVAL '1 month 2 weeks', NOW() - INTERVAL '1 month 1 week 3 days'),

-- More recent activity for better analytics
('00000015-0000-0000-0000-000000000015'::uuid, 'f1111111-1111-1111-1111-111111111111'::uuid, 'sess_dw_recent_001', 'a1111111-1111-1111-1111-111111111111'::uuid, 
 NOW() - INTERVAL '12 hours', NOW() - INTERVAL '4 hours', NOW() - INTERVAL '4 hours', 6, true, 
 76, 76, 'yes', 'qualified', 'Great! Your French Bulldog sounds adorable. We''re experienced with the special needs of flat-faced breeds.', 
 'active', 0.24, NOW() - INTERVAL '4 hours', 88, 3, NOW() - INTERVAL '12 hours', NOW() - INTERVAL '4 hours'),

('00000016-0000-0000-0000-000000000016'::uuid, 'f2222222-2222-2222-2222-222222222222'::uuid, 'sess_re_recent_001', 'a2222222-2222-2222-2222-222222222222'::uuid, 
 NOW() - INTERVAL '8 hours', NOW() - INTERVAL '2 hours', NULL, 5, false, 
 42, 0, 'unknown', 'abandoned', NULL, 
 'abandoned', 0.88, NOW() - INTERVAL '2 hours', 35, 1, NOW() - INTERVAL '8 hours', NOW() - INTERVAL '2 hours'),

('00000017-0000-0000-0000-000000000017'::uuid, 'f3333333-3333-3333-3333-333333333333'::uuid, 'sess_tc_recent_001', 'a3333333-3333-3333-3333-333333333333'::uuid, 
 NOW() - INTERVAL '6 hours', NOW() - INTERVAL '30 minutes', NOW() - INTERVAL '30 minutes', 9, true, 
 91, 91, 'yes', 'qualified', 'Outstanding! Your SaaS platform modernization project is exactly our specialty. We''ve helped 15+ companies achieve similar transformations.', 
 'active', 0.15, NOW() - INTERVAL '30 minutes', 42, 0, NOW() - INTERVAL '6 hours', NOW() - INTERVAL '30 minutes'),

-- High-activity day with multiple leads
('00000018-0000-0000-0000-000000000018'::uuid, 'f4444444-4444-4444-4444-444444444444'::uuid, 'sess_ft_today_001', 'a4444444-4444-4444-4444-444444444444'::uuid, 
 NOW() - INTERVAL '3 hours', NOW() - INTERVAL '1 hour', NOW() - INTERVAL '1 hour', 7, true, 
 85, 85, 'yes', 'qualified', 'Perfect timing! Our January transformation program starts next week. Your goals align perfectly with our proven methodology.', 
 'active', 0.18, NOW() - INTERVAL '1 hour', 55, 1, NOW() - INTERVAL '3 hours', NOW() - INTERVAL '1 hour'),

('00000019-0000-0000-0000-000000000019'::uuid, 'f5555555-5555-5555-5555-555555555555'::uuid, 'sess_cs_today_001', 'a5555555-5555-5555-5555-555555555555'::uuid, 
 NOW() - INTERVAL '2 hours', NOW() - INTERVAL '45 minutes', NOW() - INTERVAL '45 minutes', 6, true, 
 62, 62, 'maybe', 'qualified_fallback', 'We understand move-out cleaning can be stressful. Let us handle the details so you can focus on your relocation.', 
 'active', 0.26, NOW() - INTERVAL '45 minutes', 75, 2, NOW() - INTERVAL '2 hours', NOW() - INTERVAL '45 minutes'),

('00000020-0000-0000-0000-000000000020'::uuid, 'f1111111-1111-1111-1111-111111111111'::uuid, 'sess_dw_today_002', 'a1111111-1111-1111-1111-111111111111'::uuid, 
 NOW() - INTERVAL '1 hour', NOW() - INTERVAL '15 minutes', NULL, 3, false, 
 20, 0, 'unknown', 'at_risk', NULL, 
 'at_risk', 0.65, NOW() - INTERVAL '15 minutes', 12, 0, NOW() - INTERVAL '1 hour', NOW() - INTERVAL '15 minutes');

-- ==== LEAD OUTCOMES DATA ====

INSERT INTO lead_outcomes (
    id,
    session_id,
    form_id,
    actual_conversion,
    predicted_conversion,
    conversion_date,
    conversion_value,
    conversion_type,
    prediction_accuracy,
    notes,
    feedback_score,
    created_at
) VALUES

-- Successful conversions (predicted correctly)
('10000001-0000-0000-0000-000000000001'::uuid, 'sess_dw_001', 'f1111111-1111-1111-1111-111111111111'::uuid, 
 true, true, NOW() - INTERVAL '9 minutes', 320.00, 'monthly_contract', true, 
 'Client signed up for daily walks. Excellent match - dog is well-behaved Golden Retriever as predicted.', 9, NOW() - INTERVAL '8 minutes'),

('10000002-0000-0000-0000-000000000002'::uuid, 'sess_dw_002', 'f1111111-1111-1111-1111-111111111111'::uuid, 
 true, true, NOW() - INTERVAL '2 hours 45 minutes', 240.00, 'weekly_contract', true, 
 'Started with 4x/week service for energetic Labrador. Client very satisfied with our approach.', 10, NOW() - INTERVAL '2 hours 30 minutes'),

('10000003-0000-0000-0000-000000000003'::uuid, 'sess_re_001', 'f2222222-2222-2222-2222-222222222222'::uuid, 
 true, true, NOW() - INTERVAL '5 days 12 hours', 8500.00, 'commission', true, 
 'Closed on Brooklyn Heights condo. Client appreciated our knowledge of the neighborhood.', 9, NOW() - INTERVAL '5 days'),

('10000004-0000-0000-0000-000000000004'::uuid, 'sess_tc_001', 'f3333333-3333-3333-3333-333333333333'::uuid, 
 true, true, NOW() - INTERVAL '9 days 6 hours', 45000.00, 'project_contract', true, 
 'Major cloud migration project. Exactly the type of technical challenge we excel at.', 10, NOW() - INTERVAL '9 days'),

('10000005-0000-0000-0000-000000000005'::uuid, 'sess_ft_001', 'f4444444-4444-4444-4444-444444444444'::uuid, 
 true, true, NOW() - INTERVAL '2 weeks 4 days 12 hours', 1200.00, 'package_purchase', true, 
 'Client committed to 6-month transformation program. Very motivated and realistic goals.', 9, NOW() - INTERVAL '2 weeks 4 days'),

('10000006-0000-0000-0000-000000000006'::uuid, 'sess_cs_001', 'f5555555-5555-5555-5555-555555555555'::uuid, 
 true, true, NOW() - INTERVAL '1 month 1 day 18 hours', 520.00, 'recurring_service', true, 
 'Bi-weekly cleaning service for 3BR Queens home. Perfect fit for our eco-friendly approach.', 8, NOW() - INTERVAL '1 month 1 day'),

-- Maybe leads that converted (system underestimated)
('10000007-0000-0000-0000-000000000007'::uuid, 'sess_dw_003', 'f1111111-1111-1111-1111-111111111111'::uuid, 
 true, false, NOW() - INTERVAL '23 hours', 160.00, 'trial_package', false, 
 'Client decided to try 2x/week after initially being budget-conscious. Started with trial package.', 7, NOW() - INTERVAL '22 hours'),

('10000008-0000-0000-0000-000000000008'::uuid, 'sess_re_002', 'f2222222-2222-2222-2222-222222222222'::uuid, 
 true, false, NOW() - INTERVAL '1 week 18 hours', 6200.00, 'commission', false, 
 'Client found financing solution and purchased Manhattan apartment. Persistence paid off.', 8, NOW() - INTERVAL '1 week 12 hours'),

('10000009-0000-0000-0000-000000000009'::uuid, 'sess_ft_002', 'f4444444-4444-4444-4444-444444444444'::uuid, 
 true, false, NOW() - INTERVAL '3 weeks 1 day 6 hours', 800.00, 'flexible_plan', false, 
 'Client chose flexible payment plan we offered. Started with 3-month program.', 8, NOW() - INTERVAL '3 weeks 1 day'),

-- Failed conversions (predicted correctly)
('10000010-0000-0000-0000-000000000010'::uuid, 'sess_dw_005', 'f1111111-1111-1111-1111-111111111111'::uuid, 
 false, false, NULL, 0.00, 'no_conversion', true, 
 'Dog not vaccinated as predicted. Cannot provide service without proper vaccination records.', 3, NOW() - INTERVAL '3 days'),

('10000011-0000-0000-0000-000000000011'::uuid, 'sess_cs_002', 'f5555555-5555-5555-5555-555555555555'::uuid, 
 false, false, NULL, 0.00, 'out_of_area', true, 
 'Location outside service area as indicated in survey. Referred to local competitor.', 4, NOW() - INTERVAL '1 month 1 week 2 days'),

-- Failed conversions (prediction was wrong - system was too optimistic)
('10000012-0000-0000-0000-000000000012'::uuid, 'sess_dw_015', 'f1111111-1111-1111-1111-111111111111'::uuid, 
 false, true, NULL, 0.00, 'no_response', false, 
 'Client seemed very interested but never responded to follow-up. May have found another service.', 2, NOW() - INTERVAL '3 hours'),

('10000013-0000-0000-0000-000000000013'::uuid, 'sess_tc_recent_001', 'f3333333-3333-3333-3333-333333333333'::uuid, 
 false, true, NULL, 0.00, 'budget_constraints', false, 
 'Client loved our proposal but budget was approved for different vendor. Cost was primary factor.', 5, NOW() - INTERVAL '25 minutes'),

-- Recent conversion (today's success)
('10000014-0000-0000-0000-000000000014'::uuid, 'sess_ft_today_001', 'f4444444-4444-4444-4444-444444444444'::uuid, 
 true, true, NOW() - INTERVAL '30 minutes', 1800.00, 'premium_package', true, 
 'Immediate conversion! Client ready to start January transformation program. Excellent prospect identification.', 10, NOW() - INTERVAL '25 minutes');