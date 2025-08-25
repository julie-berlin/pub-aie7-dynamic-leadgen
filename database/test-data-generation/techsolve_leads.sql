-- Test Data for TechSolve Consulting (Software Consulting)
-- Generated 30 realistic lead sessions with complete tracking and outcomes
-- Client: techsolve | Form: f3333333-3333-3333-3333-333333333333 | Generated: 2025-08-24T20:19:36



-- Lead 1: Qualified - Robert Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('aecd4655-c952-4c14-a6ed-fed86e441bce', 'f3333333-3333-3333-3333-333333333333', 'techsolve_001_qualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-20T05:19:36.886491', '2025-08-20T05:50:36.886497', '2025-08-20T05:50:36.886497', 6, true, 92, 92, 'yes', 'qualified', 'Perfect! Your technology challenges align well with our expertise. Our senior consultant will reach out within 24 hours to discuss your project.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.115', '{"device_type": "desktop", "completion_time": 28}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('7ce2d889-3037-43ae-b7b2-9afb9a565b9d', 'aecd4655-c952-4c14-a6ed-fed86e441bce', 'linkedin', 'social', 'enterprise_solutions', 'IT consulting boston', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('de671d3b-753f-4248-8cdf-21ba8660f715', 'aecd4655-c952-4c14-a6ed-fed86e441bce', 'f3333333-3333-3333-3333-333333333333', 1, 'Robert Kim', '{"name": "Robert Kim"}', 10, '2025-08-20T05:19:36.886491'),
('1bbfbe48-80a7-4eb0-a867-4ea3eee50ee9', 'aecd4655-c952-4c14-a6ed-fed86e441bce', 'f3333333-3333-3333-3333-333333333333', 2, 'robert.kim@enterprise.com', '{"email": "robert.kim@enterprise.com"}', 10, '2025-08-20T05:19:36.886491'),
('618c7438-c0cb-4072-9203-f103c5ecea3b', 'aecd4655-c952-4c14-a6ed-fed86e441bce', 'f3333333-3333-3333-3333-333333333333', 3, '(617) 555-2468', '{"phone": "(617) 555-2468"}', 15, '2025-08-20T05:19:36.886491'),
('1eb7afdd-f5f1-4cb0-9a23-193a222f3f94', 'aecd4655-c952-4c14-a6ed-fed86e441bce', 'f3333333-3333-3333-3333-333333333333', 4, '50_200_employees', '{"company_size": "50_200_employees"}', 25, '2025-08-20T05:19:36.886491'),
('ab29a558-5240-4529-a82d-22a327905ea2', 'aecd4655-c952-4c14-a6ed-fed86e441bce', 'f3333333-3333-3333-3333-333333333333', 5, 'legacy_systems', '{"tech_challenges": "legacy_systems"}', 10, '2025-08-20T05:19:36.886491'),
('c9b171ac-7994-40ba-9141-71a2b9c7c31a', 'aecd4655-c952-4c14-a6ed-fed86e441bce', 'f3333333-3333-3333-3333-333333333333', 6, '$50k_100k', '{"budget_range": "$50k_100k"}', 20, '2025-08-20T05:19:36.886491'),
('08547226-39d5-4314-9d45-33070c46fff6', 'aecd4655-c952-4c14-a6ed-fed86e441bce', 'f3333333-3333-3333-3333-333333333333', 7, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-20T05:19:36.886491'),
('806b908c-6fc5-45ae-8028-29b98b5897f6', 'aecd4655-c952-4c14-a6ed-fed86e441bce', 'f3333333-3333-3333-3333-333333333333', 8, 'mixed_cloud_onprem', '{"current_setup": "mixed_cloud_onprem"}', 10, '2025-08-20T05:19:36.886491'),
('b230bcd6-7735-4026-9119-3d77fbc6a190', 'aecd4655-c952-4c14-a6ed-fed86e441bce', 'f3333333-3333-3333-3333-333333333333', 9, 'yes', '{"decision_maker": "yes"}', 20, '2025-08-20T05:19:36.886491'),
('1c65be56-020f-49af-9698-a97ceb3d26a0', 'aecd4655-c952-4c14-a6ed-fed86e441bce', 'f3333333-3333-3333-3333-333333333333', 10, 'manufacturing', '{"industry": "manufacturing"}', 10, '2025-08-20T05:19:36.886491'),
('b3f6a658-6ec6-4203-8296-344a57b1cded', 'aecd4655-c952-4c14-a6ed-fed86e441bce', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_good', '{"previous_consulting": "yes_good"}', 10, '2025-08-20T05:19:36.886491');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('165a078d-43f7-49a0-9918-d94e593e6703', 'aecd4655-c952-4c14-a6ed-fed86e441bce', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'qualified', '{"name": "Robert Kim", "email": "robert.kim@enterprise.com", "phone": "(617) 555-2468"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 2: Qualified - Patricia Davis
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('da403ec0-89d8-416c-9906-e57cf706e4ab', 'f3333333-3333-3333-3333-333333333333', 'techsolve_002_qualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-19T19:19:36.886603', '2025-08-19T19:51:36.886605', '2025-08-19T19:51:36.886605', 6, true, 78, 78, 'yes', 'qualified', 'Perfect! Your technology challenges align well with our expertise. Our senior consultant will reach out within 24 hours to discuss your project.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.120', '{"device_type": "desktop", "completion_time": 17}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('7e53831b-d990-491f-b17a-ec106200ac4c', 'da403ec0-89d8-416c-9906-e57cf706e4ab', 'google', 'cpc', 'small_business_tech', 'IT consulting boston', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('e16e7b8d-9ae8-425a-b4eb-637a1d4bbf2b', 'da403ec0-89d8-416c-9906-e57cf706e4ab', 'f3333333-3333-3333-3333-333333333333', 1, 'Patricia Davis', '{"name": "Patricia Davis"}', 10, '2025-08-19T19:19:36.886603'),
('c7a394ce-ec6b-4080-ae84-69d85e54adfd', 'da403ec0-89d8-416c-9906-e57cf706e4ab', 'f3333333-3333-3333-3333-333333333333', 2, 'p.davis@retailchain.com', '{"email": "p.davis@retailchain.com"}', 10, '2025-08-19T19:19:36.886603'),
('6666cd98-0b27-4a68-9231-ac8b25aae105', 'da403ec0-89d8-416c-9906-e57cf706e4ab', 'f3333333-3333-3333-3333-333333333333', 3, '(857) 555-1357', '{"phone": "(857) 555-1357"}', 15, '2025-08-19T19:19:36.886603'),
('38f26050-f3ad-41fd-bfb5-f7856efceee3', 'da403ec0-89d8-416c-9906-e57cf706e4ab', 'f3333333-3333-3333-3333-333333333333', 4, '10_50_employees', '{"company_size": "10_50_employees"}', 20, '2025-08-19T19:19:36.886603'),
('32c42e5d-fabb-4ffc-84fc-d8f59f5a680f', 'da403ec0-89d8-416c-9906-e57cf706e4ab', 'f3333333-3333-3333-3333-333333333333', 5, 'data_management', '{"tech_challenges": "data_management"}', 10, '2025-08-19T19:19:36.886603'),
('5c67dff7-0fb0-4192-a95c-83806ff23be8', 'da403ec0-89d8-416c-9906-e57cf706e4ab', 'f3333333-3333-3333-3333-333333333333', 6, '$25k_50k', '{"budget_range": "$25k_50k"}', 15, '2025-08-19T19:19:36.886603'),
('7d11f229-08ec-468c-8b26-0345d84c0ffd', 'da403ec0-89d8-416c-9906-e57cf706e4ab', 'f3333333-3333-3333-3333-333333333333', 7, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-19T19:19:36.886603'),
('f6ece426-92c0-45ea-b85c-690ca629d151', 'da403ec0-89d8-416c-9906-e57cf706e4ab', 'f3333333-3333-3333-3333-333333333333', 8, 'mostly_cloud', '{"current_setup": "mostly_cloud"}', 10, '2025-08-19T19:19:36.886603'),
('de829bf5-8780-46ae-9075-383c60a0d685', 'da403ec0-89d8-416c-9906-e57cf706e4ab', 'f3333333-3333-3333-3333-333333333333', 9, 'shared', '{"decision_maker": "shared"}', 15, '2025-08-19T19:19:36.886603'),
('838b478f-a748-4238-87d4-21683c3d2841', 'da403ec0-89d8-416c-9906-e57cf706e4ab', 'f3333333-3333-3333-3333-333333333333', 10, 'retail', '{"industry": "retail"}', 10, '2025-08-19T19:19:36.886603'),
('789853f9-51d2-48f7-ad22-94c2697fb9aa', 'da403ec0-89d8-416c-9906-e57cf706e4ab', 'f3333333-3333-3333-3333-333333333333', 11, 'no', '{"previous_consulting": "no"}', 10, '2025-08-19T19:19:36.886603');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('0fd2b036-b44f-4dfc-9d53-a17d5f854398', 'da403ec0-89d8-416c-9906-e57cf706e4ab', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'qualified', '{"name": "Patricia Davis", "email": "p.davis@retailchain.com", "phone": "(857) 555-1357"}', 78, 0.78, true, false, NULL, NULL, NULL);


-- Lead 3: Maybe - James Wilson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('13ffe368-5536-4019-97da-d2561dd1ed6d', 'f3333333-3333-3333-3333-333333333333', 'techsolve_003_maybe', 'a3333333-3333-3333-3333-333333333333', '2025-08-12T21:19:36.886680', '2025-08-12T21:45:36.886681', '2025-08-12T21:45:36.886681', 9, true, 45, 45, 'maybe', 'qualified', 'Thanks for your inquiry! We are evaluating how we can best support your technology needs. Our team will be in touch within a few days.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.182', '{"device_type": "mobile", "completion_time": 52}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('dbdcacb7-58e9-4fe6-914a-b1eeee90ee41', '13ffe368-5536-4019-97da-d2561dd1ed6d', 'organic', 'search', 'nonprofit_solutions', 'IT consulting boston', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('30e5013a-870e-41f0-bae1-3b6a95fc706b', '13ffe368-5536-4019-97da-d2561dd1ed6d', 'f3333333-3333-3333-3333-333333333333', 1, 'James Wilson', '{"name": "James Wilson"}', 10, '2025-08-12T21:19:36.886680'),
('7d2c1349-e7aa-45e6-bb97-57c06971ee18', '13ffe368-5536-4019-97da-d2561dd1ed6d', 'f3333333-3333-3333-3333-333333333333', 2, 'james.wilson@nonprofit.org', '{"email": "james.wilson@nonprofit.org"}', 10, '2025-08-12T21:19:36.886680'),
('25fe0933-15f1-4dbd-8130-00bea26486d9', '13ffe368-5536-4019-97da-d2561dd1ed6d', 'f3333333-3333-3333-3333-333333333333', 3, '(617) 555-8024', '{"phone": "(617) 555-8024"}', 15, '2025-08-12T21:19:36.886680'),
('b57f38a4-12d4-40c7-b8eb-de86ae688291', '13ffe368-5536-4019-97da-d2561dd1ed6d', 'f3333333-3333-3333-3333-333333333333', 4, 'under_10', '{"company_size": "under_10"}', 10, '2025-08-12T21:19:36.886680'),
('290f0345-f00f-4f1c-8a3f-27e7e43a302f', '13ffe368-5536-4019-97da-d2561dd1ed6d', 'f3333333-3333-3333-3333-333333333333', 5, 'security', '{"tech_challenges": "security"}', 10, '2025-08-12T21:19:36.886680'),
('0ced5b87-4674-4eb1-a8ec-1c42b3f2bb52', '13ffe368-5536-4019-97da-d2561dd1ed6d', 'f3333333-3333-3333-3333-333333333333', 6, 'under_25k', '{"budget_range": "under_25k"}', 5, '2025-08-12T21:19:36.886680'),
('8b22f83a-933f-4099-8b77-10c5829dbdc7', '13ffe368-5536-4019-97da-d2561dd1ed6d', 'f3333333-3333-3333-3333-333333333333', 7, '6_12_months', '{"timeline": "6_12_months"}', 10, '2025-08-12T21:19:36.886680'),
('8542a0d8-4b4d-4bd8-be02-2f6cef3345f0', '13ffe368-5536-4019-97da-d2561dd1ed6d', 'f3333333-3333-3333-3333-333333333333', 8, 'mostly_onprem', '{"current_setup": "mostly_onprem"}', 10, '2025-08-12T21:19:36.886680'),
('21eea2b1-170c-4536-8dd5-bda79ca946f4', '13ffe368-5536-4019-97da-d2561dd1ed6d', 'f3333333-3333-3333-3333-333333333333', 9, 'no', '{"decision_maker": "no"}', 5, '2025-08-12T21:19:36.886680'),
('01aa43b5-c79c-4c1b-af18-cc31564877ad', '13ffe368-5536-4019-97da-d2561dd1ed6d', 'f3333333-3333-3333-3333-333333333333', 10, 'nonprofit', '{"industry": "nonprofit"}', 10, '2025-08-12T21:19:36.886680'),
('e3639b70-dd18-4f54-a87e-6e8c0d46bd97', '13ffe368-5536-4019-97da-d2561dd1ed6d', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_mixed', '{"previous_consulting": "yes_mixed"}', 10, '2025-08-12T21:19:36.886680');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('6e7f6dd0-76f0-4112-adef-c6a3ebc400bf', '13ffe368-5536-4019-97da-d2561dd1ed6d', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'maybe', '{"name": "James Wilson", "email": "james.wilson@nonprofit.org", "phone": "(617) 555-8024"}', 45, 0.45, true, false, NULL, NULL, NULL);


-- Lead 4: Unqualified - Michelle Brown
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('d488ed4c-fe0b-496a-b09a-c2460ec1d21b', 'f3333333-3333-3333-3333-333333333333', 'techsolve_004_unqualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-22T11:19:36.886748', '2025-08-22T11:57:36.886749', '2025-08-22T11:57:36.886749', 6, true, 30, 30, 'no', 'qualified', 'Thank you for considering TechSolve. While your current requirements may not align with our services, feel free to contact us in the future.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.52', '{"device_type": "mobile", "completion_time": 31}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('4a1b2e1e-9ddd-491c-b3fe-da84053c78fe', 'd488ed4c-fe0b-496a-b09a-c2460ec1d21b', 'organic', 'search', 'startup_resources', 'technology solutions', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('381cd06b-0012-4e90-865c-febbf03933fa', 'd488ed4c-fe0b-496a-b09a-c2460ec1d21b', 'f3333333-3333-3333-3333-333333333333', 1, 'Michelle Brown', '{"name": "Michelle Brown"}', 10, '2025-08-22T11:19:36.886748'),
('62bff8ad-8ce8-43c3-865c-6984607adaea', 'd488ed4c-fe0b-496a-b09a-c2460ec1d21b', 'f3333333-3333-3333-3333-333333333333', 2, 'mbrown@startup.co', '{"email": "mbrown@startup.co"}', 10, '2025-08-22T11:19:36.886748'),
('0b558105-7427-4a86-a926-471041da05b9', 'd488ed4c-fe0b-496a-b09a-c2460ec1d21b', 'f3333333-3333-3333-3333-333333333333', 4, 'under_10', '{"company_size": "under_10"}', 10, '2025-08-22T11:19:36.886748'),
('b5b6935b-a777-4d40-acb2-9160c8aadcfd', 'd488ed4c-fe0b-496a-b09a-c2460ec1d21b', 'f3333333-3333-3333-3333-333333333333', 5, 'scaling', '{"tech_challenges": "scaling"}', 10, '2025-08-22T11:19:36.886748'),
('86d21e24-6d83-4abf-8c4d-f83288b3ed07', 'd488ed4c-fe0b-496a-b09a-c2460ec1d21b', 'f3333333-3333-3333-3333-333333333333', 6, 'under_25k', '{"budget_range": "under_25k"}', 5, '2025-08-22T11:19:36.886748'),
('236c0fb2-f783-4c2a-85fc-3dd0e5200c93', 'd488ed4c-fe0b-496a-b09a-c2460ec1d21b', 'f3333333-3333-3333-3333-333333333333', 7, 'just_exploring', '{"timeline": "just_exploring"}', 0, '2025-08-22T11:19:36.886748'),
('81dd1ddf-a9a1-4ea2-ad2e-3bf00bfb4e8d', 'd488ed4c-fe0b-496a-b09a-c2460ec1d21b', 'f3333333-3333-3333-3333-333333333333', 8, 'all_cloud', '{"current_setup": "all_cloud"}', 10, '2025-08-22T11:19:36.886748'),
('9b4bed5b-487a-4220-bff6-497dee70a171', 'd488ed4c-fe0b-496a-b09a-c2460ec1d21b', 'f3333333-3333-3333-3333-333333333333', 9, 'yes', '{"decision_maker": "yes"}', 20, '2025-08-22T11:19:36.886748'),
('80e6da40-0286-40e9-9132-5c1199aaf92a', 'd488ed4c-fe0b-496a-b09a-c2460ec1d21b', 'f3333333-3333-3333-3333-333333333333', 10, 'technology', '{"industry": "technology"}', 10, '2025-08-22T11:19:36.886748'),
('5e2d7cc5-7e50-44b4-a028-aa3e8f4286a1', 'd488ed4c-fe0b-496a-b09a-c2460ec1d21b', 'f3333333-3333-3333-3333-333333333333', 11, 'no', '{"previous_consulting": "no"}', 10, '2025-08-22T11:19:36.886748');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('7983b6aa-169e-48b3-85f8-842e147991df', 'd488ed4c-fe0b-496a-b09a-c2460ec1d21b', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'unqualified', '{"name": "Michelle Brown", "email": "mbrown@startup.co"}', 30, 0.30, false, false, NULL, NULL, NULL);


-- Lead 5: Maybe - Thomas Anderson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('b6dd68d1-66ed-4972-a41e-41bcc7539af7', 'f3333333-3333-3333-3333-333333333333', 'techsolve_005_maybe', 'a3333333-3333-3333-3333-333333333333', '2025-08-13T18:19:36.886810', '2025-08-13T18:39:36.886812', '2025-08-13T18:39:36.886812', 8, true, 68, 68, 'maybe', 'qualified', 'Thanks for your inquiry! We are evaluating how we can best support your technology needs. Our team will be in touch within a few days.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.130', '{"device_type": "desktop", "completion_time": 18}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('0abbf1bc-e5f4-4056-a4f2-a876481c1fa0', 'b6dd68d1-66ed-4972-a41e-41bcc7539af7', 'referral', 'referral', 'healthcare_tech', 'technology solutions', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('4543e1cd-2d63-4bf0-a246-6285ece1c79f', 'b6dd68d1-66ed-4972-a41e-41bcc7539af7', 'f3333333-3333-3333-3333-333333333333', 1, 'Thomas Anderson', '{"name": "Thomas Anderson"}', 10, '2025-08-13T18:19:36.886810'),
('e9f60d18-d355-4308-8334-5fff5f0645ba', 'b6dd68d1-66ed-4972-a41e-41bcc7539af7', 'f3333333-3333-3333-3333-333333333333', 2, 'tanderson@midcorp.com', '{"email": "tanderson@midcorp.com"}', 10, '2025-08-13T18:19:36.886810'),
('77f968cb-fb4a-4f9f-a705-bc342b2950db', 'b6dd68d1-66ed-4972-a41e-41bcc7539af7', 'f3333333-3333-3333-3333-333333333333', 3, '(508) 555-4680', '{"phone": "(508) 555-4680"}', 15, '2025-08-13T18:19:36.886810'),
('5808d1ce-d66b-451f-9adb-8cb55a2e274c', 'b6dd68d1-66ed-4972-a41e-41bcc7539af7', 'f3333333-3333-3333-3333-333333333333', 4, '10_50_employees', '{"company_size": "10_50_employees"}', 20, '2025-08-13T18:19:36.886810'),
('ebc1d8fa-7cd9-485a-8621-2790b6f00d8d', 'b6dd68d1-66ed-4972-a41e-41bcc7539af7', 'f3333333-3333-3333-3333-333333333333', 5, 'integration', '{"tech_challenges": "integration"}', 10, '2025-08-13T18:19:36.886810'),
('d14337f3-68b6-4c17-8b02-1b8cfcdaa0d4', 'b6dd68d1-66ed-4972-a41e-41bcc7539af7', 'f3333333-3333-3333-3333-333333333333', 6, '$25k_50k', '{"budget_range": "$25k_50k"}', 15, '2025-08-13T18:19:36.886810'),
('5b2325c2-3d34-45ec-9bd1-1ed2e0f70531', 'b6dd68d1-66ed-4972-a41e-41bcc7539af7', 'f3333333-3333-3333-3333-333333333333', 7, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-13T18:19:36.886810'),
('fc217b03-f794-4199-92e9-24a0da66dcc5', 'b6dd68d1-66ed-4972-a41e-41bcc7539af7', 'f3333333-3333-3333-3333-333333333333', 8, 'mixed_cloud_onprem', '{"current_setup": "mixed_cloud_onprem"}', 10, '2025-08-13T18:19:36.886810'),
('f227c834-9f07-4148-abf8-5f254660b8f1', 'b6dd68d1-66ed-4972-a41e-41bcc7539af7', 'f3333333-3333-3333-3333-333333333333', 9, 'shared', '{"decision_maker": "shared"}', 15, '2025-08-13T18:19:36.886810'),
('ba3a8540-620c-4292-a30a-6bf428ef32fb', 'b6dd68d1-66ed-4972-a41e-41bcc7539af7', 'f3333333-3333-3333-3333-333333333333', 10, 'healthcare', '{"industry": "healthcare"}', 10, '2025-08-13T18:19:36.886810'),
('fc13cfcc-0c9b-4bad-9405-965740ff9974', 'b6dd68d1-66ed-4972-a41e-41bcc7539af7', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_good', '{"previous_consulting": "yes_good"}', 10, '2025-08-13T18:19:36.886810');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('bf61ed23-708c-4053-a744-876846a332d8', 'b6dd68d1-66ed-4972-a41e-41bcc7539af7', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'maybe', '{"name": "Thomas Anderson", "email": "tanderson@midcorp.com", "phone": "(508) 555-4680"}', 68, 0.68, true, false, NULL, NULL, NULL);


-- Lead 6: Qualified - Robert_2 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('16d69c80-f512-49dd-a7a8-59dbd27f0029', 'f3333333-3333-3333-3333-333333333333', 'techsolve_006_qualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-09T21:19:36.886875', '2025-08-09T21:46:36.886876', '2025-08-09T21:46:36.886876', 6, true, 92, 92, 'yes', 'qualified', 'Perfect! Your technology challenges align well with our expertise. Our senior consultant will reach out within 24 hours to discuss your project.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.30', '{"device_type": "desktop", "completion_time": 32}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('23727e52-9333-4502-a07c-be97a1003849', '16d69c80-f512-49dd-a7a8-59dbd27f0029', 'linkedin', 'social', 'enterprise_solutions', 'tech support services', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('5c190b17-31be-4011-abb6-b3fb66177510', '16d69c80-f512-49dd-a7a8-59dbd27f0029', 'f3333333-3333-3333-3333-333333333333', 1, 'Robert_2 Kim', '{"name": "Robert_2 Kim"}', 10, '2025-08-09T21:19:36.886875'),
('f7045589-6ad4-4fb9-81c1-fa2772512ab5', '16d69c80-f512-49dd-a7a8-59dbd27f0029', 'f3333333-3333-3333-3333-333333333333', 2, 'robert.kim_2@enterprise.com', '{"email": "robert.kim_2@enterprise.com"}', 10, '2025-08-09T21:19:36.886875'),
('1bfcdffa-2967-4d84-a31b-dad27b8dbaff', '16d69c80-f512-49dd-a7a8-59dbd27f0029', 'f3333333-3333-3333-3333-333333333333', 3, '(617) 555-2468', '{"phone": "(617) 555-2468"}', 15, '2025-08-09T21:19:36.886875'),
('9c95fdfb-e003-4b16-8eac-9911108f8ae6', '16d69c80-f512-49dd-a7a8-59dbd27f0029', 'f3333333-3333-3333-3333-333333333333', 4, '50_200_employees', '{"company_size": "50_200_employees"}', 25, '2025-08-09T21:19:36.886875'),
('b18e45a2-6b40-45ef-bffc-e8b5a5555104', '16d69c80-f512-49dd-a7a8-59dbd27f0029', 'f3333333-3333-3333-3333-333333333333', 5, 'legacy_systems', '{"tech_challenges": "legacy_systems"}', 10, '2025-08-09T21:19:36.886875'),
('36b9176b-866d-4b5c-874d-b44200df187e', '16d69c80-f512-49dd-a7a8-59dbd27f0029', 'f3333333-3333-3333-3333-333333333333', 6, '$50k_100k', '{"budget_range": "$50k_100k"}', 20, '2025-08-09T21:19:36.886875'),
('84632bbb-7e5c-4cb8-a337-e2873237ee8b', '16d69c80-f512-49dd-a7a8-59dbd27f0029', 'f3333333-3333-3333-3333-333333333333', 7, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-09T21:19:36.886875'),
('d2a87e01-9008-42c9-bd1c-1e6ae21746da', '16d69c80-f512-49dd-a7a8-59dbd27f0029', 'f3333333-3333-3333-3333-333333333333', 8, 'mixed_cloud_onprem', '{"current_setup": "mixed_cloud_onprem"}', 10, '2025-08-09T21:19:36.886875'),
('29ba3563-4e7c-4e1b-9df2-0c03ce14bd4a', '16d69c80-f512-49dd-a7a8-59dbd27f0029', 'f3333333-3333-3333-3333-333333333333', 9, 'yes', '{"decision_maker": "yes"}', 20, '2025-08-09T21:19:36.886875'),
('b8d04d5e-77da-47fe-a6cc-f206b35e3a1b', '16d69c80-f512-49dd-a7a8-59dbd27f0029', 'f3333333-3333-3333-3333-333333333333', 10, 'manufacturing', '{"industry": "manufacturing"}', 10, '2025-08-09T21:19:36.886875'),
('3b050dbe-e0b0-4cab-a080-8a1913fc4e6c', '16d69c80-f512-49dd-a7a8-59dbd27f0029', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_good', '{"previous_consulting": "yes_good"}', 10, '2025-08-09T21:19:36.886875');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('6d1bd754-444f-4f7d-a2c5-b162e60e4c69', '16d69c80-f512-49dd-a7a8-59dbd27f0029', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'qualified', '{"name": "Robert_2 Kim", "email": "robert.kim_2@enterprise.com", "phone": "(617) 555-2468"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 7: Qualified - Patricia_2 Davis
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('7e7d6e54-a24e-4d17-83d6-d1cc5e6018dc', 'f3333333-3333-3333-3333-333333333333', 'techsolve_007_qualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-21T17:19:36.886942', '2025-08-21T17:38:36.886943', '2025-08-21T17:38:36.886943', 9, true, 78, 78, 'yes', 'qualified', 'Perfect! Your technology challenges align well with our expertise. Our senior consultant will reach out within 24 hours to discuss your project.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.92', '{"device_type": "desktop", "completion_time": 56}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('0449e393-5e79-4e44-9fe0-a74b972d229f', '7e7d6e54-a24e-4d17-83d6-d1cc5e6018dc', 'google', 'cpc', 'small_business_tech', 'digital transformation', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('5814daef-0914-4087-9851-5fe5e6363eab', '7e7d6e54-a24e-4d17-83d6-d1cc5e6018dc', 'f3333333-3333-3333-3333-333333333333', 1, 'Patricia_2 Davis', '{"name": "Patricia_2 Davis"}', 10, '2025-08-21T17:19:36.886942'),
('46572e89-6217-41fd-bde0-089f8cb835db', '7e7d6e54-a24e-4d17-83d6-d1cc5e6018dc', 'f3333333-3333-3333-3333-333333333333', 2, 'p.davis_2@retailchain.com', '{"email": "p.davis_2@retailchain.com"}', 10, '2025-08-21T17:19:36.886942'),
('8680e707-a294-47af-bf91-398aad321880', '7e7d6e54-a24e-4d17-83d6-d1cc5e6018dc', 'f3333333-3333-3333-3333-333333333333', 3, '(857) 555-1357', '{"phone": "(857) 555-1357"}', 15, '2025-08-21T17:19:36.886942'),
('d6497936-905e-488c-8973-c5fc3b61e698', '7e7d6e54-a24e-4d17-83d6-d1cc5e6018dc', 'f3333333-3333-3333-3333-333333333333', 4, '10_50_employees', '{"company_size": "10_50_employees"}', 20, '2025-08-21T17:19:36.886942'),
('2128e191-d4f9-42be-93b0-6b9f9acebc9b', '7e7d6e54-a24e-4d17-83d6-d1cc5e6018dc', 'f3333333-3333-3333-3333-333333333333', 5, 'data_management', '{"tech_challenges": "data_management"}', 10, '2025-08-21T17:19:36.886942'),
('1854c2d6-d4f9-4e56-9486-26e1f290c3a7', '7e7d6e54-a24e-4d17-83d6-d1cc5e6018dc', 'f3333333-3333-3333-3333-333333333333', 6, '$25k_50k', '{"budget_range": "$25k_50k"}', 15, '2025-08-21T17:19:36.886942'),
('52e56676-44e8-4b56-8a4e-73cef6975cc2', '7e7d6e54-a24e-4d17-83d6-d1cc5e6018dc', 'f3333333-3333-3333-3333-333333333333', 7, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-21T17:19:36.886942'),
('a1ef53f3-fe1c-4823-b9fd-77034a5387ec', '7e7d6e54-a24e-4d17-83d6-d1cc5e6018dc', 'f3333333-3333-3333-3333-333333333333', 8, 'mostly_cloud', '{"current_setup": "mostly_cloud"}', 10, '2025-08-21T17:19:36.886942'),
('607cc865-70d2-43b9-ab26-5ec88cca96e9', '7e7d6e54-a24e-4d17-83d6-d1cc5e6018dc', 'f3333333-3333-3333-3333-333333333333', 9, 'shared', '{"decision_maker": "shared"}', 15, '2025-08-21T17:19:36.886942'),
('1a8aa7a6-3fe7-40f1-bbf5-12c352547c97', '7e7d6e54-a24e-4d17-83d6-d1cc5e6018dc', 'f3333333-3333-3333-3333-333333333333', 10, 'retail', '{"industry": "retail"}', 10, '2025-08-21T17:19:36.886942'),
('8c9f0d97-47fa-4d12-9eae-97def9d1d2ff', '7e7d6e54-a24e-4d17-83d6-d1cc5e6018dc', 'f3333333-3333-3333-3333-333333333333', 11, 'no', '{"previous_consulting": "no"}', 10, '2025-08-21T17:19:36.886942');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('d2302ea4-2e77-4565-bb09-f80bfc914596', '7e7d6e54-a24e-4d17-83d6-d1cc5e6018dc', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'qualified', '{"name": "Patricia_2 Davis", "email": "p.davis_2@retailchain.com", "phone": "(857) 555-1357"}', 78, 0.78, true, false, NULL, NULL, NULL);


-- Lead 8: Maybe - James_2 Wilson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('98797b53-9993-41f2-aaea-1ec2cb5b06ff', 'f3333333-3333-3333-3333-333333333333', 'techsolve_008_maybe', 'a3333333-3333-3333-3333-333333333333', '2025-08-17T06:19:36.887007', '2025-08-17T06:36:36.887008', '2025-08-17T06:36:36.887008', 6, true, 45, 45, 'maybe', 'qualified', 'Thanks for your inquiry! We are evaluating how we can best support your technology needs. Our team will be in touch within a few days.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.230', '{"device_type": "mobile", "completion_time": 38}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('eff8d248-f645-4120-ab16-7261057ed611', '98797b53-9993-41f2-aaea-1ec2cb5b06ff', 'organic', 'search', 'nonprofit_solutions', 'digital transformation', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('d8820023-8274-44ae-ac0e-0ed4a0b0f902', '98797b53-9993-41f2-aaea-1ec2cb5b06ff', 'f3333333-3333-3333-3333-333333333333', 1, 'James_2 Wilson', '{"name": "James_2 Wilson"}', 10, '2025-08-17T06:19:36.887007'),
('8c2766eb-2514-4d11-941f-a70ae395cbe8', '98797b53-9993-41f2-aaea-1ec2cb5b06ff', 'f3333333-3333-3333-3333-333333333333', 2, 'james.wilson_2@nonprofit.org', '{"email": "james.wilson_2@nonprofit.org"}', 10, '2025-08-17T06:19:36.887007'),
('ab0775e1-1420-4d74-80c3-a1d31e2a6c2c', '98797b53-9993-41f2-aaea-1ec2cb5b06ff', 'f3333333-3333-3333-3333-333333333333', 3, '(617) 555-8024', '{"phone": "(617) 555-8024"}', 15, '2025-08-17T06:19:36.887007'),
('48738b87-3a31-4acd-a9bd-ff7fdccfd8a8', '98797b53-9993-41f2-aaea-1ec2cb5b06ff', 'f3333333-3333-3333-3333-333333333333', 4, 'under_10', '{"company_size": "under_10"}', 10, '2025-08-17T06:19:36.887007'),
('4fbdb856-3b7b-46df-80cb-94904ca8064d', '98797b53-9993-41f2-aaea-1ec2cb5b06ff', 'f3333333-3333-3333-3333-333333333333', 5, 'security', '{"tech_challenges": "security"}', 10, '2025-08-17T06:19:36.887007'),
('ff07bf38-fa86-40d1-acf7-cdfb999fcafe', '98797b53-9993-41f2-aaea-1ec2cb5b06ff', 'f3333333-3333-3333-3333-333333333333', 6, 'under_25k', '{"budget_range": "under_25k"}', 5, '2025-08-17T06:19:36.887007'),
('700440ca-d106-47b4-9fd0-9be5ab19c609', '98797b53-9993-41f2-aaea-1ec2cb5b06ff', 'f3333333-3333-3333-3333-333333333333', 7, '6_12_months', '{"timeline": "6_12_months"}', 10, '2025-08-17T06:19:36.887007'),
('604cbf2d-33be-4a02-a105-09887900147a', '98797b53-9993-41f2-aaea-1ec2cb5b06ff', 'f3333333-3333-3333-3333-333333333333', 8, 'mostly_onprem', '{"current_setup": "mostly_onprem"}', 10, '2025-08-17T06:19:36.887007'),
('106ded72-f771-46c7-8172-92587d854226', '98797b53-9993-41f2-aaea-1ec2cb5b06ff', 'f3333333-3333-3333-3333-333333333333', 9, 'no', '{"decision_maker": "no"}', 5, '2025-08-17T06:19:36.887007'),
('9ade4f71-8f9b-40ad-92c4-e2e701f9dad6', '98797b53-9993-41f2-aaea-1ec2cb5b06ff', 'f3333333-3333-3333-3333-333333333333', 10, 'nonprofit', '{"industry": "nonprofit"}', 10, '2025-08-17T06:19:36.887007'),
('b5747859-b0c8-403f-b3e5-44edb6e680f9', '98797b53-9993-41f2-aaea-1ec2cb5b06ff', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_mixed', '{"previous_consulting": "yes_mixed"}', 10, '2025-08-17T06:19:36.887007');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('70df7832-c7b8-4f8e-b4ab-a086a92f1c0a', '98797b53-9993-41f2-aaea-1ec2cb5b06ff', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'maybe', '{"name": "James_2 Wilson", "email": "james.wilson_2@nonprofit.org", "phone": "(617) 555-8024"}', 45, 0.45, true, false, NULL, NULL, NULL);


-- Lead 9: Unqualified - Michelle_2 Brown
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('79642fd6-15b1-467b-922e-306fa07349e3', 'f3333333-3333-3333-3333-333333333333', 'techsolve_009_unqualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-18T14:19:36.887070', '2025-08-18T14:39:36.887071', '2025-08-18T14:39:36.887071', 11, true, 30, 30, 'no', 'qualified', 'Thank you for considering TechSolve. While your current requirements may not align with our services, feel free to contact us in the future.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.112', '{"device_type": "mobile", "completion_time": 24}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('b1811e07-d5ce-4a80-9024-f6d1caeebe6d', '79642fd6-15b1-467b-922e-306fa07349e3', 'organic', 'search', 'startup_resources', 'software consulting', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('e3f0cc94-c6b5-451b-ac42-f32ce2020eb9', '79642fd6-15b1-467b-922e-306fa07349e3', 'f3333333-3333-3333-3333-333333333333', 1, 'Michelle_2 Brown', '{"name": "Michelle_2 Brown"}', 10, '2025-08-18T14:19:36.887070'),
('37ecf779-51fa-4a2d-bc07-9cf7e190f7c1', '79642fd6-15b1-467b-922e-306fa07349e3', 'f3333333-3333-3333-3333-333333333333', 2, 'mbrown_2@startup.co', '{"email": "mbrown_2@startup.co"}', 10, '2025-08-18T14:19:36.887070'),
('d4630262-c873-4109-9cd3-00e5ce71360d', '79642fd6-15b1-467b-922e-306fa07349e3', 'f3333333-3333-3333-3333-333333333333', 4, 'under_10', '{"company_size": "under_10"}', 10, '2025-08-18T14:19:36.887070'),
('56fc4a3e-f33d-441a-89d1-a2a5605b3d14', '79642fd6-15b1-467b-922e-306fa07349e3', 'f3333333-3333-3333-3333-333333333333', 5, 'scaling', '{"tech_challenges": "scaling"}', 10, '2025-08-18T14:19:36.887070'),
('0db3130f-f065-40fc-ae6d-6bc1774ce454', '79642fd6-15b1-467b-922e-306fa07349e3', 'f3333333-3333-3333-3333-333333333333', 6, 'under_25k', '{"budget_range": "under_25k"}', 5, '2025-08-18T14:19:36.887070'),
('c6b44931-c1ee-40b2-a388-835f1283a794', '79642fd6-15b1-467b-922e-306fa07349e3', 'f3333333-3333-3333-3333-333333333333', 7, 'just_exploring', '{"timeline": "just_exploring"}', 0, '2025-08-18T14:19:36.887070'),
('634ee95f-66bf-44c3-8d53-4ddec662053e', '79642fd6-15b1-467b-922e-306fa07349e3', 'f3333333-3333-3333-3333-333333333333', 8, 'all_cloud', '{"current_setup": "all_cloud"}', 10, '2025-08-18T14:19:36.887070'),
('0db7595d-4e58-4b24-93a8-6f71b20fc3c6', '79642fd6-15b1-467b-922e-306fa07349e3', 'f3333333-3333-3333-3333-333333333333', 9, 'yes', '{"decision_maker": "yes"}', 20, '2025-08-18T14:19:36.887070'),
('d8c136f5-0f97-4ff2-82b6-cfe659de8a47', '79642fd6-15b1-467b-922e-306fa07349e3', 'f3333333-3333-3333-3333-333333333333', 10, 'technology', '{"industry": "technology"}', 10, '2025-08-18T14:19:36.887070'),
('98b7d7a7-4409-4c33-ae83-60899b0f7060', '79642fd6-15b1-467b-922e-306fa07349e3', 'f3333333-3333-3333-3333-333333333333', 11, 'no', '{"previous_consulting": "no"}', 10, '2025-08-18T14:19:36.887070');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('2183a1f9-c98a-4465-9c4d-b16c2bbe803b', '79642fd6-15b1-467b-922e-306fa07349e3', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'unqualified', '{"name": "Michelle_2 Brown", "email": "mbrown_2@startup.co"}', 30, 0.30, false, false, NULL, NULL, NULL);


-- Lead 10: Maybe - Thomas_2 Anderson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('76bf1edb-157c-4bff-b39c-2da609568533', 'f3333333-3333-3333-3333-333333333333', 'techsolve_010_maybe', 'a3333333-3333-3333-3333-333333333333', '2025-08-17T21:19:36.887131', '2025-08-17T22:00:36.887132', '2025-08-17T22:00:36.887132', 8, true, 68, 68, 'maybe', 'qualified', 'Thanks for your inquiry! We are evaluating how we can best support your technology needs. Our team will be in touch within a few days.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.204', '{"device_type": "desktop", "completion_time": 41}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('9c93d929-87fb-4426-a305-d200165ddb74', '76bf1edb-157c-4bff-b39c-2da609568533', 'referral', 'referral', 'healthcare_tech', 'tech support services', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('7d44cfbd-bea0-47ac-be7c-9f1b9a51a866', '76bf1edb-157c-4bff-b39c-2da609568533', 'f3333333-3333-3333-3333-333333333333', 1, 'Thomas_2 Anderson', '{"name": "Thomas_2 Anderson"}', 10, '2025-08-17T21:19:36.887131'),
('8e0f4ee1-7461-4bcd-9ce3-07300c008b1f', '76bf1edb-157c-4bff-b39c-2da609568533', 'f3333333-3333-3333-3333-333333333333', 2, 'tanderson_2@midcorp.com', '{"email": "tanderson_2@midcorp.com"}', 10, '2025-08-17T21:19:36.887131'),
('1cfcefc0-3107-4b67-b14a-23bbd58f6a98', '76bf1edb-157c-4bff-b39c-2da609568533', 'f3333333-3333-3333-3333-333333333333', 3, '(508) 555-4680', '{"phone": "(508) 555-4680"}', 15, '2025-08-17T21:19:36.887131'),
('aaae73ad-5977-4652-9717-cc596673828b', '76bf1edb-157c-4bff-b39c-2da609568533', 'f3333333-3333-3333-3333-333333333333', 4, '10_50_employees', '{"company_size": "10_50_employees"}', 20, '2025-08-17T21:19:36.887131'),
('2096870c-9768-4295-8fbb-41b4438ba5d6', '76bf1edb-157c-4bff-b39c-2da609568533', 'f3333333-3333-3333-3333-333333333333', 5, 'integration', '{"tech_challenges": "integration"}', 10, '2025-08-17T21:19:36.887131'),
('b7db1e18-23ba-4448-a9a2-068ee21fbcb2', '76bf1edb-157c-4bff-b39c-2da609568533', 'f3333333-3333-3333-3333-333333333333', 6, '$25k_50k', '{"budget_range": "$25k_50k"}', 15, '2025-08-17T21:19:36.887131'),
('8f89bf0c-a492-4547-95b7-f2a25743a68b', '76bf1edb-157c-4bff-b39c-2da609568533', 'f3333333-3333-3333-3333-333333333333', 7, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-17T21:19:36.887131'),
('b5aef09e-31a9-4b35-9940-26d94b250fa1', '76bf1edb-157c-4bff-b39c-2da609568533', 'f3333333-3333-3333-3333-333333333333', 8, 'mixed_cloud_onprem', '{"current_setup": "mixed_cloud_onprem"}', 10, '2025-08-17T21:19:36.887131'),
('614c900e-d383-4ebc-849a-5b959e669c2f', '76bf1edb-157c-4bff-b39c-2da609568533', 'f3333333-3333-3333-3333-333333333333', 9, 'shared', '{"decision_maker": "shared"}', 15, '2025-08-17T21:19:36.887131'),
('a5c74763-ca46-42af-9369-6f9349c79beb', '76bf1edb-157c-4bff-b39c-2da609568533', 'f3333333-3333-3333-3333-333333333333', 10, 'healthcare', '{"industry": "healthcare"}', 10, '2025-08-17T21:19:36.887131'),
('acdce7bd-5379-4625-9806-986cfd1d956a', '76bf1edb-157c-4bff-b39c-2da609568533', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_good', '{"previous_consulting": "yes_good"}', 10, '2025-08-17T21:19:36.887131');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('03af3be6-63f9-4b98-9089-69e5c0d2fb14', '76bf1edb-157c-4bff-b39c-2da609568533', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'maybe', '{"name": "Thomas_2 Anderson", "email": "tanderson_2@midcorp.com", "phone": "(508) 555-4680"}', 68, 0.68, true, false, NULL, NULL, NULL);


-- Lead 11: Qualified - Robert_3 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('56b08a65-82a9-4d74-94d8-826c2e4b8eca', 'f3333333-3333-3333-3333-333333333333', 'techsolve_011_qualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-11T05:19:36.887195', '2025-08-11T05:45:36.887196', '2025-08-11T05:45:36.887196', 9, true, 92, 92, 'yes', 'qualified', 'Perfect! Your technology challenges align well with our expertise. Our senior consultant will reach out within 24 hours to discuss your project.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.87', '{"device_type": "desktop", "completion_time": 32}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('eb2f5c33-e9b2-49b4-ab28-3b3b2746e13f', '56b08a65-82a9-4d74-94d8-826c2e4b8eca', 'linkedin', 'social', 'enterprise_solutions', 'software consulting', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('b282adf5-28f6-4610-97bc-dd955c04e92f', '56b08a65-82a9-4d74-94d8-826c2e4b8eca', 'f3333333-3333-3333-3333-333333333333', 1, 'Robert_3 Kim', '{"name": "Robert_3 Kim"}', 10, '2025-08-11T05:19:36.887195'),
('d058c7d1-57f8-4b53-b760-7b2f3ef5d1c3', '56b08a65-82a9-4d74-94d8-826c2e4b8eca', 'f3333333-3333-3333-3333-333333333333', 2, 'robert.kim_3@enterprise.com', '{"email": "robert.kim_3@enterprise.com"}', 10, '2025-08-11T05:19:36.887195'),
('17c74fbd-70c1-4af3-9dee-093603aa838b', '56b08a65-82a9-4d74-94d8-826c2e4b8eca', 'f3333333-3333-3333-3333-333333333333', 3, '(617) 555-2468', '{"phone": "(617) 555-2468"}', 15, '2025-08-11T05:19:36.887195'),
('14565379-5abf-47f1-bd48-d42cf79b5606', '56b08a65-82a9-4d74-94d8-826c2e4b8eca', 'f3333333-3333-3333-3333-333333333333', 4, '50_200_employees', '{"company_size": "50_200_employees"}', 25, '2025-08-11T05:19:36.887195'),
('2fcc42d2-7af8-47e4-b5bb-c0498cfee819', '56b08a65-82a9-4d74-94d8-826c2e4b8eca', 'f3333333-3333-3333-3333-333333333333', 5, 'legacy_systems', '{"tech_challenges": "legacy_systems"}', 10, '2025-08-11T05:19:36.887195'),
('ad2745f8-dd51-4c7e-9ed4-df0b73b09035', '56b08a65-82a9-4d74-94d8-826c2e4b8eca', 'f3333333-3333-3333-3333-333333333333', 6, '$50k_100k', '{"budget_range": "$50k_100k"}', 20, '2025-08-11T05:19:36.887195'),
('ae294229-6b20-49e7-87ca-681de353487a', '56b08a65-82a9-4d74-94d8-826c2e4b8eca', 'f3333333-3333-3333-3333-333333333333', 7, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-11T05:19:36.887195'),
('9333e04c-7d59-499c-aa31-c422b751e6c1', '56b08a65-82a9-4d74-94d8-826c2e4b8eca', 'f3333333-3333-3333-3333-333333333333', 8, 'mixed_cloud_onprem', '{"current_setup": "mixed_cloud_onprem"}', 10, '2025-08-11T05:19:36.887195'),
('f478090c-2a40-44b3-8053-6fbfa0156e50', '56b08a65-82a9-4d74-94d8-826c2e4b8eca', 'f3333333-3333-3333-3333-333333333333', 9, 'yes', '{"decision_maker": "yes"}', 20, '2025-08-11T05:19:36.887195'),
('d730268d-a010-4405-980b-64085a903f73', '56b08a65-82a9-4d74-94d8-826c2e4b8eca', 'f3333333-3333-3333-3333-333333333333', 10, 'manufacturing', '{"industry": "manufacturing"}', 10, '2025-08-11T05:19:36.887195'),
('90d785c7-d180-450d-8065-7212aa88d50e', '56b08a65-82a9-4d74-94d8-826c2e4b8eca', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_good', '{"previous_consulting": "yes_good"}', 10, '2025-08-11T05:19:36.887195');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('21feba70-157b-43da-b52f-fd3844b711bf', '56b08a65-82a9-4d74-94d8-826c2e4b8eca', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'qualified', '{"name": "Robert_3 Kim", "email": "robert.kim_3@enterprise.com", "phone": "(617) 555-2468"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 12: Qualified - Patricia_3 Davis
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('a608ea0d-d174-4635-ae6d-2af9b0f87a1d', 'f3333333-3333-3333-3333-333333333333', 'techsolve_012_qualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-18T23:19:36.887259', '2025-08-18T23:46:36.887260', '2025-08-18T23:46:36.887260', 10, true, 78, 78, 'yes', 'qualified', 'Perfect! Your technology challenges align well with our expertise. Our senior consultant will reach out within 24 hours to discuss your project.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.185', '{"device_type": "desktop", "completion_time": 13}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('8f508e1d-b9c6-46ba-a6be-4540c9e62550', 'a608ea0d-d174-4635-ae6d-2af9b0f87a1d', 'google', 'cpc', 'small_business_tech', 'software consulting', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('ce4aaa33-fa69-459f-b714-63ea133d70df', 'a608ea0d-d174-4635-ae6d-2af9b0f87a1d', 'f3333333-3333-3333-3333-333333333333', 1, 'Patricia_3 Davis', '{"name": "Patricia_3 Davis"}', 10, '2025-08-18T23:19:36.887259'),
('3fd51884-0c20-45ba-9042-4bdde0b4efc0', 'a608ea0d-d174-4635-ae6d-2af9b0f87a1d', 'f3333333-3333-3333-3333-333333333333', 2, 'p.davis_3@retailchain.com', '{"email": "p.davis_3@retailchain.com"}', 10, '2025-08-18T23:19:36.887259'),
('041c8e57-ead0-4914-9d5f-a303a810dcc1', 'a608ea0d-d174-4635-ae6d-2af9b0f87a1d', 'f3333333-3333-3333-3333-333333333333', 3, '(857) 555-1357', '{"phone": "(857) 555-1357"}', 15, '2025-08-18T23:19:36.887259'),
('bb266405-0326-4f4b-bd33-179f63ddb8bb', 'a608ea0d-d174-4635-ae6d-2af9b0f87a1d', 'f3333333-3333-3333-3333-333333333333', 4, '10_50_employees', '{"company_size": "10_50_employees"}', 20, '2025-08-18T23:19:36.887259'),
('8c63ab11-7cf5-4934-ad5e-6a1fc90721cb', 'a608ea0d-d174-4635-ae6d-2af9b0f87a1d', 'f3333333-3333-3333-3333-333333333333', 5, 'data_management', '{"tech_challenges": "data_management"}', 10, '2025-08-18T23:19:36.887259'),
('8ffd92cf-ee9a-4046-a554-89bc876d201e', 'a608ea0d-d174-4635-ae6d-2af9b0f87a1d', 'f3333333-3333-3333-3333-333333333333', 6, '$25k_50k', '{"budget_range": "$25k_50k"}', 15, '2025-08-18T23:19:36.887259'),
('9b8823dd-e671-4aae-a316-9e48336b1ecb', 'a608ea0d-d174-4635-ae6d-2af9b0f87a1d', 'f3333333-3333-3333-3333-333333333333', 7, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-18T23:19:36.887259'),
('13ed64cd-2ebe-4f1f-acb9-a9c15c8ef446', 'a608ea0d-d174-4635-ae6d-2af9b0f87a1d', 'f3333333-3333-3333-3333-333333333333', 8, 'mostly_cloud', '{"current_setup": "mostly_cloud"}', 10, '2025-08-18T23:19:36.887259'),
('8fdf0e62-9db4-4339-8a75-ff7b7958d2f1', 'a608ea0d-d174-4635-ae6d-2af9b0f87a1d', 'f3333333-3333-3333-3333-333333333333', 9, 'shared', '{"decision_maker": "shared"}', 15, '2025-08-18T23:19:36.887259'),
('c33f65c9-562e-4af9-929a-0ee564b5c341', 'a608ea0d-d174-4635-ae6d-2af9b0f87a1d', 'f3333333-3333-3333-3333-333333333333', 10, 'retail', '{"industry": "retail"}', 10, '2025-08-18T23:19:36.887259'),
('1900cb8b-4aca-4e53-bac8-7d0faa513d0f', 'a608ea0d-d174-4635-ae6d-2af9b0f87a1d', 'f3333333-3333-3333-3333-333333333333', 11, 'no', '{"previous_consulting": "no"}', 10, '2025-08-18T23:19:36.887259');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('6da4ce11-48b6-4435-adc2-63d97eda76d4', 'a608ea0d-d174-4635-ae6d-2af9b0f87a1d', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'qualified', '{"name": "Patricia_3 Davis", "email": "p.davis_3@retailchain.com", "phone": "(857) 555-1357"}', 78, 0.78, true, false, NULL, NULL, NULL);


-- Lead 13: Maybe - James_3 Wilson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('1f057f75-697f-45aa-91a0-2c75f6d89f64', 'f3333333-3333-3333-3333-333333333333', 'techsolve_013_maybe', 'a3333333-3333-3333-3333-333333333333', '2025-08-21T08:19:36.887322', '2025-08-21T08:46:36.887323', '2025-08-21T08:46:36.887323', 6, true, 45, 45, 'maybe', 'qualified', 'Thanks for your inquiry! We are evaluating how we can best support your technology needs. Our team will be in touch within a few days.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.20', '{"device_type": "mobile", "completion_time": 39}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('f8d177a1-292f-4a4d-b4c8-ea5897b90e83', '1f057f75-697f-45aa-91a0-2c75f6d89f64', 'organic', 'search', 'nonprofit_solutions', 'digital transformation', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('53030b95-abdc-4e48-9613-d5fa187a96df', '1f057f75-697f-45aa-91a0-2c75f6d89f64', 'f3333333-3333-3333-3333-333333333333', 1, 'James_3 Wilson', '{"name": "James_3 Wilson"}', 10, '2025-08-21T08:19:36.887322'),
('8d14385b-1ed9-43e0-8c92-6835205f6a34', '1f057f75-697f-45aa-91a0-2c75f6d89f64', 'f3333333-3333-3333-3333-333333333333', 2, 'james.wilson_3@nonprofit.org', '{"email": "james.wilson_3@nonprofit.org"}', 10, '2025-08-21T08:19:36.887322'),
('9ce1ce0d-6478-4264-aef6-b06063d0c132', '1f057f75-697f-45aa-91a0-2c75f6d89f64', 'f3333333-3333-3333-3333-333333333333', 3, '(617) 555-8024', '{"phone": "(617) 555-8024"}', 15, '2025-08-21T08:19:36.887322'),
('c8b4b41f-7fd2-4a34-8188-249aab618455', '1f057f75-697f-45aa-91a0-2c75f6d89f64', 'f3333333-3333-3333-3333-333333333333', 4, 'under_10', '{"company_size": "under_10"}', 10, '2025-08-21T08:19:36.887322'),
('c7b3e53f-a2f3-48a6-9654-64fe1008ed61', '1f057f75-697f-45aa-91a0-2c75f6d89f64', 'f3333333-3333-3333-3333-333333333333', 5, 'security', '{"tech_challenges": "security"}', 10, '2025-08-21T08:19:36.887322'),
('fbe3824c-012d-4aa8-a9b4-8e4d8ff7204e', '1f057f75-697f-45aa-91a0-2c75f6d89f64', 'f3333333-3333-3333-3333-333333333333', 6, 'under_25k', '{"budget_range": "under_25k"}', 5, '2025-08-21T08:19:36.887322'),
('5ab7ed4d-f7dd-4208-b1d8-b21556a78c43', '1f057f75-697f-45aa-91a0-2c75f6d89f64', 'f3333333-3333-3333-3333-333333333333', 7, '6_12_months', '{"timeline": "6_12_months"}', 10, '2025-08-21T08:19:36.887322'),
('4b4bcbe5-63c9-4787-8918-87dcd768fd77', '1f057f75-697f-45aa-91a0-2c75f6d89f64', 'f3333333-3333-3333-3333-333333333333', 8, 'mostly_onprem', '{"current_setup": "mostly_onprem"}', 10, '2025-08-21T08:19:36.887322'),
('93042ed5-37e4-4623-b247-32d81355efa7', '1f057f75-697f-45aa-91a0-2c75f6d89f64', 'f3333333-3333-3333-3333-333333333333', 9, 'no', '{"decision_maker": "no"}', 5, '2025-08-21T08:19:36.887322'),
('58ff38ab-aed9-435f-a29a-de10ef3e5c72', '1f057f75-697f-45aa-91a0-2c75f6d89f64', 'f3333333-3333-3333-3333-333333333333', 10, 'nonprofit', '{"industry": "nonprofit"}', 10, '2025-08-21T08:19:36.887322'),
('91f2d807-5874-44fc-a159-d82532546c3a', '1f057f75-697f-45aa-91a0-2c75f6d89f64', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_mixed', '{"previous_consulting": "yes_mixed"}', 10, '2025-08-21T08:19:36.887322');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('1399ca68-5f54-438b-894d-e9c87da2ddb0', '1f057f75-697f-45aa-91a0-2c75f6d89f64', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'maybe', '{"name": "James_3 Wilson", "email": "james.wilson_3@nonprofit.org", "phone": "(617) 555-8024"}', 45, 0.45, true, false, NULL, NULL, NULL);


-- Lead 14: Unqualified - Michelle_3 Brown
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('d8ffa277-a14d-47b7-9fc9-e2160a6504bf', 'f3333333-3333-3333-3333-333333333333', 'techsolve_014_unqualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-16T07:19:36.887385', '2025-08-16T08:03:36.887386', '2025-08-16T08:03:36.887386', 10, true, 30, 30, 'no', 'qualified', 'Thank you for considering TechSolve. While your current requirements may not align with our services, feel free to contact us in the future.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.158', '{"device_type": "mobile", "completion_time": 34}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('ced52ab2-9478-4913-b993-fd73067f4b14', 'd8ffa277-a14d-47b7-9fc9-e2160a6504bf', 'organic', 'search', 'startup_resources', 'software consulting', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('42b75c79-f12d-42f0-bd3c-0f8c0b5826db', 'd8ffa277-a14d-47b7-9fc9-e2160a6504bf', 'f3333333-3333-3333-3333-333333333333', 1, 'Michelle_3 Brown', '{"name": "Michelle_3 Brown"}', 10, '2025-08-16T07:19:36.887385'),
('6974d9d4-2706-4dd7-a6d3-2169e1f0162f', 'd8ffa277-a14d-47b7-9fc9-e2160a6504bf', 'f3333333-3333-3333-3333-333333333333', 2, 'mbrown_3@startup.co', '{"email": "mbrown_3@startup.co"}', 10, '2025-08-16T07:19:36.887385'),
('daf0913f-0856-49fb-b052-0550240987e6', 'd8ffa277-a14d-47b7-9fc9-e2160a6504bf', 'f3333333-3333-3333-3333-333333333333', 4, 'under_10', '{"company_size": "under_10"}', 10, '2025-08-16T07:19:36.887385'),
('59bffec2-6149-47ca-bf1a-900911c5ccf2', 'd8ffa277-a14d-47b7-9fc9-e2160a6504bf', 'f3333333-3333-3333-3333-333333333333', 5, 'scaling', '{"tech_challenges": "scaling"}', 10, '2025-08-16T07:19:36.887385'),
('7dcb1383-192f-4c48-9bd5-1128d9dbb93b', 'd8ffa277-a14d-47b7-9fc9-e2160a6504bf', 'f3333333-3333-3333-3333-333333333333', 6, 'under_25k', '{"budget_range": "under_25k"}', 5, '2025-08-16T07:19:36.887385'),
('f4abc7a2-5838-4749-9e6a-ef936490e47a', 'd8ffa277-a14d-47b7-9fc9-e2160a6504bf', 'f3333333-3333-3333-3333-333333333333', 7, 'just_exploring', '{"timeline": "just_exploring"}', 0, '2025-08-16T07:19:36.887385'),
('3fc008de-5c46-45c8-b0e2-173480f5ad73', 'd8ffa277-a14d-47b7-9fc9-e2160a6504bf', 'f3333333-3333-3333-3333-333333333333', 8, 'all_cloud', '{"current_setup": "all_cloud"}', 10, '2025-08-16T07:19:36.887385'),
('f76fdcb1-4f1b-43b9-bda7-c9d4e7a59c2f', 'd8ffa277-a14d-47b7-9fc9-e2160a6504bf', 'f3333333-3333-3333-3333-333333333333', 9, 'yes', '{"decision_maker": "yes"}', 20, '2025-08-16T07:19:36.887385'),
('c3fd8365-c33a-44ef-be72-9385b698ac99', 'd8ffa277-a14d-47b7-9fc9-e2160a6504bf', 'f3333333-3333-3333-3333-333333333333', 10, 'technology', '{"industry": "technology"}', 10, '2025-08-16T07:19:36.887385'),
('ee7f27d0-1ea5-4be8-8c8d-7790ffb3f85e', 'd8ffa277-a14d-47b7-9fc9-e2160a6504bf', 'f3333333-3333-3333-3333-333333333333', 11, 'no', '{"previous_consulting": "no"}', 10, '2025-08-16T07:19:36.887385');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('f6892ef2-d5d2-4d2b-a1c6-1b90fd718203', 'd8ffa277-a14d-47b7-9fc9-e2160a6504bf', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'unqualified', '{"name": "Michelle_3 Brown", "email": "mbrown_3@startup.co"}', 30, 0.30, false, false, NULL, NULL, NULL);


-- Lead 15: Maybe - Thomas_3 Anderson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('63581b0d-0750-44cd-b038-138b0bdbc93c', 'f3333333-3333-3333-3333-333333333333', 'techsolve_015_maybe', 'a3333333-3333-3333-3333-333333333333', '2025-08-13T15:19:36.887444', '2025-08-13T15:59:36.887445', '2025-08-13T15:59:36.887445', 6, true, 68, 68, 'maybe', 'qualified', 'Thanks for your inquiry! We are evaluating how we can best support your technology needs. Our team will be in touch within a few days.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.218', '{"device_type": "desktop", "completion_time": 52}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('38f94b88-691c-4616-bb70-f156f2dfc60b', '63581b0d-0750-44cd-b038-138b0bdbc93c', 'referral', 'referral', 'healthcare_tech', 'software consulting', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('a9f2422a-707c-444b-a68b-74a29a1d5021', '63581b0d-0750-44cd-b038-138b0bdbc93c', 'f3333333-3333-3333-3333-333333333333', 1, 'Thomas_3 Anderson', '{"name": "Thomas_3 Anderson"}', 10, '2025-08-13T15:19:36.887444'),
('29f75d31-7b41-4ba6-9f2e-317e21c62a74', '63581b0d-0750-44cd-b038-138b0bdbc93c', 'f3333333-3333-3333-3333-333333333333', 2, 'tanderson_3@midcorp.com', '{"email": "tanderson_3@midcorp.com"}', 10, '2025-08-13T15:19:36.887444'),
('42bbb212-13b7-4928-b2d5-aafe901e6ecd', '63581b0d-0750-44cd-b038-138b0bdbc93c', 'f3333333-3333-3333-3333-333333333333', 3, '(508) 555-4680', '{"phone": "(508) 555-4680"}', 15, '2025-08-13T15:19:36.887444'),
('c8a81e1b-d78c-48ec-b176-b4650bb98183', '63581b0d-0750-44cd-b038-138b0bdbc93c', 'f3333333-3333-3333-3333-333333333333', 4, '10_50_employees', '{"company_size": "10_50_employees"}', 20, '2025-08-13T15:19:36.887444'),
('632a9525-a978-4f6d-badf-ccd3588c8998', '63581b0d-0750-44cd-b038-138b0bdbc93c', 'f3333333-3333-3333-3333-333333333333', 5, 'integration', '{"tech_challenges": "integration"}', 10, '2025-08-13T15:19:36.887444'),
('d3a54b8f-eeda-47e8-aeca-e4883c45c34a', '63581b0d-0750-44cd-b038-138b0bdbc93c', 'f3333333-3333-3333-3333-333333333333', 6, '$25k_50k', '{"budget_range": "$25k_50k"}', 15, '2025-08-13T15:19:36.887444'),
('b940aa5e-6e35-450c-8bf4-ba7c4832c4af', '63581b0d-0750-44cd-b038-138b0bdbc93c', 'f3333333-3333-3333-3333-333333333333', 7, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-13T15:19:36.887444'),
('6e357f6c-8ac4-4b34-9c6a-a816d62f56cf', '63581b0d-0750-44cd-b038-138b0bdbc93c', 'f3333333-3333-3333-3333-333333333333', 8, 'mixed_cloud_onprem', '{"current_setup": "mixed_cloud_onprem"}', 10, '2025-08-13T15:19:36.887444'),
('8eeb3a56-2050-4078-bd62-a58b7d623cd2', '63581b0d-0750-44cd-b038-138b0bdbc93c', 'f3333333-3333-3333-3333-333333333333', 9, 'shared', '{"decision_maker": "shared"}', 15, '2025-08-13T15:19:36.887444'),
('e4e084b4-e171-4ac2-ada8-d259c7a079a4', '63581b0d-0750-44cd-b038-138b0bdbc93c', 'f3333333-3333-3333-3333-333333333333', 10, 'healthcare', '{"industry": "healthcare"}', 10, '2025-08-13T15:19:36.887444'),
('6dcd8540-137b-436f-91be-6196fac5387c', '63581b0d-0750-44cd-b038-138b0bdbc93c', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_good', '{"previous_consulting": "yes_good"}', 10, '2025-08-13T15:19:36.887444');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('b461f953-7ddc-4bf2-9563-e8e5548fd76f', '63581b0d-0750-44cd-b038-138b0bdbc93c', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'maybe', '{"name": "Thomas_3 Anderson", "email": "tanderson_3@midcorp.com", "phone": "(508) 555-4680"}', 68, 0.68, true, false, NULL, NULL, NULL);


-- Lead 16: Qualified - Robert_4 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('b34eb893-cab1-46a6-a1f5-6b635461c286', 'f3333333-3333-3333-3333-333333333333', 'techsolve_016_qualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-16T01:19:36.887508', '2025-08-16T02:01:36.887509', '2025-08-16T02:01:36.887509', 7, true, 92, 92, 'yes', 'qualified', 'Perfect! Your technology challenges align well with our expertise. Our senior consultant will reach out within 24 hours to discuss your project.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.10', '{"device_type": "desktop", "completion_time": 19}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('29943ae2-3efc-4c7b-9113-a438c9e40187', 'b34eb893-cab1-46a6-a1f5-6b635461c286', 'linkedin', 'social', 'enterprise_solutions', 'IT consulting boston', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('2676a6c8-c6fe-4bc5-94b5-2a285f509b6c', 'b34eb893-cab1-46a6-a1f5-6b635461c286', 'f3333333-3333-3333-3333-333333333333', 1, 'Robert_4 Kim', '{"name": "Robert_4 Kim"}', 10, '2025-08-16T01:19:36.887508'),
('7d1d5d90-5cfe-4aa7-9bec-f88e73aaf78f', 'b34eb893-cab1-46a6-a1f5-6b635461c286', 'f3333333-3333-3333-3333-333333333333', 2, 'robert.kim_4@enterprise.com', '{"email": "robert.kim_4@enterprise.com"}', 10, '2025-08-16T01:19:36.887508'),
('8c77ad3d-8777-4101-b6b1-b10bc73a1fe7', 'b34eb893-cab1-46a6-a1f5-6b635461c286', 'f3333333-3333-3333-3333-333333333333', 3, '(617) 555-2468', '{"phone": "(617) 555-2468"}', 15, '2025-08-16T01:19:36.887508'),
('6ae92780-4b91-491e-bf04-c4db40a439c9', 'b34eb893-cab1-46a6-a1f5-6b635461c286', 'f3333333-3333-3333-3333-333333333333', 4, '50_200_employees', '{"company_size": "50_200_employees"}', 25, '2025-08-16T01:19:36.887508'),
('572fcc12-3ec0-4ffd-9cd1-83fb32fef1ac', 'b34eb893-cab1-46a6-a1f5-6b635461c286', 'f3333333-3333-3333-3333-333333333333', 5, 'legacy_systems', '{"tech_challenges": "legacy_systems"}', 10, '2025-08-16T01:19:36.887508'),
('9574d4f0-ab78-4173-83f7-2927027fa7fe', 'b34eb893-cab1-46a6-a1f5-6b635461c286', 'f3333333-3333-3333-3333-333333333333', 6, '$50k_100k', '{"budget_range": "$50k_100k"}', 20, '2025-08-16T01:19:36.887508'),
('fdc46cd8-c2f9-437a-9762-dc19d21a38d6', 'b34eb893-cab1-46a6-a1f5-6b635461c286', 'f3333333-3333-3333-3333-333333333333', 7, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-16T01:19:36.887508'),
('5f19640d-8cc8-4899-834a-7f69dcf2c203', 'b34eb893-cab1-46a6-a1f5-6b635461c286', 'f3333333-3333-3333-3333-333333333333', 8, 'mixed_cloud_onprem', '{"current_setup": "mixed_cloud_onprem"}', 10, '2025-08-16T01:19:36.887508'),
('02912ca3-b114-41a9-a317-0a80d09ab28e', 'b34eb893-cab1-46a6-a1f5-6b635461c286', 'f3333333-3333-3333-3333-333333333333', 9, 'yes', '{"decision_maker": "yes"}', 20, '2025-08-16T01:19:36.887508'),
('9208b481-afe2-4cc9-a472-0c71ef74d1fa', 'b34eb893-cab1-46a6-a1f5-6b635461c286', 'f3333333-3333-3333-3333-333333333333', 10, 'manufacturing', '{"industry": "manufacturing"}', 10, '2025-08-16T01:19:36.887508'),
('78a98e1c-f8a3-4f84-8457-730a5fc8d703', 'b34eb893-cab1-46a6-a1f5-6b635461c286', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_good', '{"previous_consulting": "yes_good"}', 10, '2025-08-16T01:19:36.887508');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('40f97213-1573-41d1-83e9-b3e013d256a1', 'b34eb893-cab1-46a6-a1f5-6b635461c286', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'qualified', '{"name": "Robert_4 Kim", "email": "robert.kim_4@enterprise.com", "phone": "(617) 555-2468"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 17: Qualified - Patricia_4 Davis
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('d31b6703-87dd-4c1a-b4c9-667fc8f2eb6e', 'f3333333-3333-3333-3333-333333333333', 'techsolve_017_qualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-15T08:19:36.887570', '2025-08-15T08:40:36.887571', '2025-08-15T08:40:36.887571', 9, true, 78, 78, 'yes', 'qualified', 'Perfect! Your technology challenges align well with our expertise. Our senior consultant will reach out within 24 hours to discuss your project.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.212', '{"device_type": "desktop", "completion_time": 33}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('fe330ac9-ac7e-458a-b306-0c1b20534bce', 'd31b6703-87dd-4c1a-b4c9-667fc8f2eb6e', 'google', 'cpc', 'small_business_tech', 'digital transformation', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('9f98d576-3013-4e54-b0f1-bdd6c8a8c205', 'd31b6703-87dd-4c1a-b4c9-667fc8f2eb6e', 'f3333333-3333-3333-3333-333333333333', 1, 'Patricia_4 Davis', '{"name": "Patricia_4 Davis"}', 10, '2025-08-15T08:19:36.887570'),
('2db4bcd1-2647-4c81-b510-38042770a8fd', 'd31b6703-87dd-4c1a-b4c9-667fc8f2eb6e', 'f3333333-3333-3333-3333-333333333333', 2, 'p.davis_4@retailchain.com', '{"email": "p.davis_4@retailchain.com"}', 10, '2025-08-15T08:19:36.887570'),
('0f469a1d-cf33-453b-ae47-bac7708c28f9', 'd31b6703-87dd-4c1a-b4c9-667fc8f2eb6e', 'f3333333-3333-3333-3333-333333333333', 3, '(857) 555-1357', '{"phone": "(857) 555-1357"}', 15, '2025-08-15T08:19:36.887570'),
('6a5cab83-e017-4928-acb2-7a17c6ca4976', 'd31b6703-87dd-4c1a-b4c9-667fc8f2eb6e', 'f3333333-3333-3333-3333-333333333333', 4, '10_50_employees', '{"company_size": "10_50_employees"}', 20, '2025-08-15T08:19:36.887570'),
('4942b68b-9db9-4e00-a7e0-11c231df4d63', 'd31b6703-87dd-4c1a-b4c9-667fc8f2eb6e', 'f3333333-3333-3333-3333-333333333333', 5, 'data_management', '{"tech_challenges": "data_management"}', 10, '2025-08-15T08:19:36.887570'),
('199478d1-0f94-47ac-bd7b-cd07ba91c890', 'd31b6703-87dd-4c1a-b4c9-667fc8f2eb6e', 'f3333333-3333-3333-3333-333333333333', 6, '$25k_50k', '{"budget_range": "$25k_50k"}', 15, '2025-08-15T08:19:36.887570'),
('f975e833-899c-4f92-b8ab-a0f0dbfe051a', 'd31b6703-87dd-4c1a-b4c9-667fc8f2eb6e', 'f3333333-3333-3333-3333-333333333333', 7, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-15T08:19:36.887570'),
('d2e9cb54-f8c4-4209-92f8-2471233fda55', 'd31b6703-87dd-4c1a-b4c9-667fc8f2eb6e', 'f3333333-3333-3333-3333-333333333333', 8, 'mostly_cloud', '{"current_setup": "mostly_cloud"}', 10, '2025-08-15T08:19:36.887570'),
('b0ab2157-5620-42b8-a89c-9789c5551fb6', 'd31b6703-87dd-4c1a-b4c9-667fc8f2eb6e', 'f3333333-3333-3333-3333-333333333333', 9, 'shared', '{"decision_maker": "shared"}', 15, '2025-08-15T08:19:36.887570'),
('eb3089c4-0525-48c5-9e5f-e5b59d4940b7', 'd31b6703-87dd-4c1a-b4c9-667fc8f2eb6e', 'f3333333-3333-3333-3333-333333333333', 10, 'retail', '{"industry": "retail"}', 10, '2025-08-15T08:19:36.887570'),
('eb454560-c26e-45a2-8481-09d973f81013', 'd31b6703-87dd-4c1a-b4c9-667fc8f2eb6e', 'f3333333-3333-3333-3333-333333333333', 11, 'no', '{"previous_consulting": "no"}', 10, '2025-08-15T08:19:36.887570');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('074cf322-a410-49ba-a77f-db687b19eb22', 'd31b6703-87dd-4c1a-b4c9-667fc8f2eb6e', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'qualified', '{"name": "Patricia_4 Davis", "email": "p.davis_4@retailchain.com", "phone": "(857) 555-1357"}', 78, 0.78, true, false, NULL, NULL, NULL);


-- Lead 18: Maybe - James_4 Wilson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('44c58e24-0950-4f22-aa7e-cea293b20041', 'f3333333-3333-3333-3333-333333333333', 'techsolve_018_maybe', 'a3333333-3333-3333-3333-333333333333', '2025-08-16T12:19:36.887632', '2025-08-16T12:53:36.887633', '2025-08-16T12:53:36.887633', 7, true, 45, 45, 'maybe', 'qualified', 'Thanks for your inquiry! We are evaluating how we can best support your technology needs. Our team will be in touch within a few days.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.196', '{"device_type": "mobile", "completion_time": 43}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('780c33e0-6e3b-454b-8ffd-e1314bf7ae6d', '44c58e24-0950-4f22-aa7e-cea293b20041', 'organic', 'search', 'nonprofit_solutions', 'IT consulting boston', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('54209c61-1111-45d3-870c-d82953ffcdc3', '44c58e24-0950-4f22-aa7e-cea293b20041', 'f3333333-3333-3333-3333-333333333333', 1, 'James_4 Wilson', '{"name": "James_4 Wilson"}', 10, '2025-08-16T12:19:36.887632'),
('466efac4-abb6-4ffe-83ab-db4d131ec9da', '44c58e24-0950-4f22-aa7e-cea293b20041', 'f3333333-3333-3333-3333-333333333333', 2, 'james.wilson_4@nonprofit.org', '{"email": "james.wilson_4@nonprofit.org"}', 10, '2025-08-16T12:19:36.887632'),
('e3c07491-d1ff-41df-b9e5-e518c639e610', '44c58e24-0950-4f22-aa7e-cea293b20041', 'f3333333-3333-3333-3333-333333333333', 3, '(617) 555-8024', '{"phone": "(617) 555-8024"}', 15, '2025-08-16T12:19:36.887632'),
('6ab7199c-2595-4902-b619-70e4a1cf7f40', '44c58e24-0950-4f22-aa7e-cea293b20041', 'f3333333-3333-3333-3333-333333333333', 4, 'under_10', '{"company_size": "under_10"}', 10, '2025-08-16T12:19:36.887632'),
('0ffce432-2180-4af2-9389-2420694bce7f', '44c58e24-0950-4f22-aa7e-cea293b20041', 'f3333333-3333-3333-3333-333333333333', 5, 'security', '{"tech_challenges": "security"}', 10, '2025-08-16T12:19:36.887632'),
('f3daffef-173e-4df9-87cc-d3ab0c07594e', '44c58e24-0950-4f22-aa7e-cea293b20041', 'f3333333-3333-3333-3333-333333333333', 6, 'under_25k', '{"budget_range": "under_25k"}', 5, '2025-08-16T12:19:36.887632'),
('b9993be0-87c0-43fd-a5d7-3dd406f5c54a', '44c58e24-0950-4f22-aa7e-cea293b20041', 'f3333333-3333-3333-3333-333333333333', 7, '6_12_months', '{"timeline": "6_12_months"}', 10, '2025-08-16T12:19:36.887632'),
('94ad311c-151c-4a3f-a0d2-431b705ccfcc', '44c58e24-0950-4f22-aa7e-cea293b20041', 'f3333333-3333-3333-3333-333333333333', 8, 'mostly_onprem', '{"current_setup": "mostly_onprem"}', 10, '2025-08-16T12:19:36.887632'),
('d1afe823-0b9f-420d-a9c0-6e980e2d7347', '44c58e24-0950-4f22-aa7e-cea293b20041', 'f3333333-3333-3333-3333-333333333333', 9, 'no', '{"decision_maker": "no"}', 5, '2025-08-16T12:19:36.887632'),
('e84bf798-a5c3-43ed-8309-b652e7a3f502', '44c58e24-0950-4f22-aa7e-cea293b20041', 'f3333333-3333-3333-3333-333333333333', 10, 'nonprofit', '{"industry": "nonprofit"}', 10, '2025-08-16T12:19:36.887632'),
('fafb23b5-1bbb-4b75-bea9-ba7a48375d9f', '44c58e24-0950-4f22-aa7e-cea293b20041', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_mixed', '{"previous_consulting": "yes_mixed"}', 10, '2025-08-16T12:19:36.887632');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('bba95935-c2ed-4451-81c5-2674221433ca', '44c58e24-0950-4f22-aa7e-cea293b20041', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'maybe', '{"name": "James_4 Wilson", "email": "james.wilson_4@nonprofit.org", "phone": "(617) 555-8024"}', 45, 0.45, true, false, NULL, NULL, NULL);


-- Lead 19: Unqualified - Michelle_4 Brown
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('b4ac6e59-9a93-41b9-957a-82e999d72cc3', 'f3333333-3333-3333-3333-333333333333', 'techsolve_019_unqualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-20T10:19:36.887695', '2025-08-20T10:54:36.887696', '2025-08-20T10:54:36.887696', 7, true, 30, 30, 'no', 'qualified', 'Thank you for considering TechSolve. While your current requirements may not align with our services, feel free to contact us in the future.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.250', '{"device_type": "mobile", "completion_time": 45}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('bfc628e7-e27b-44d6-b128-4eccafaffbbb', 'b4ac6e59-9a93-41b9-957a-82e999d72cc3', 'organic', 'search', 'startup_resources', 'digital transformation', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('5264213b-2e7e-4de6-a5aa-2a8fe84aad49', 'b4ac6e59-9a93-41b9-957a-82e999d72cc3', 'f3333333-3333-3333-3333-333333333333', 1, 'Michelle_4 Brown', '{"name": "Michelle_4 Brown"}', 10, '2025-08-20T10:19:36.887695'),
('9f5dfa97-ee52-4aab-ac9a-cdab04e76be0', 'b4ac6e59-9a93-41b9-957a-82e999d72cc3', 'f3333333-3333-3333-3333-333333333333', 2, 'mbrown_4@startup.co', '{"email": "mbrown_4@startup.co"}', 10, '2025-08-20T10:19:36.887695'),
('e86bbd34-dd73-4429-8873-eae448bf23bc', 'b4ac6e59-9a93-41b9-957a-82e999d72cc3', 'f3333333-3333-3333-3333-333333333333', 4, 'under_10', '{"company_size": "under_10"}', 10, '2025-08-20T10:19:36.887695'),
('1ab47ca3-4b57-46c7-9440-4697c27cf1f9', 'b4ac6e59-9a93-41b9-957a-82e999d72cc3', 'f3333333-3333-3333-3333-333333333333', 5, 'scaling', '{"tech_challenges": "scaling"}', 10, '2025-08-20T10:19:36.887695'),
('546c2c25-e45e-41f8-98d9-30881354ede5', 'b4ac6e59-9a93-41b9-957a-82e999d72cc3', 'f3333333-3333-3333-3333-333333333333', 6, 'under_25k', '{"budget_range": "under_25k"}', 5, '2025-08-20T10:19:36.887695'),
('badc9132-3795-476a-b557-f887ebbb52e0', 'b4ac6e59-9a93-41b9-957a-82e999d72cc3', 'f3333333-3333-3333-3333-333333333333', 7, 'just_exploring', '{"timeline": "just_exploring"}', 0, '2025-08-20T10:19:36.887695'),
('8159eeaf-16de-4aaa-938c-077198c94d7c', 'b4ac6e59-9a93-41b9-957a-82e999d72cc3', 'f3333333-3333-3333-3333-333333333333', 8, 'all_cloud', '{"current_setup": "all_cloud"}', 10, '2025-08-20T10:19:36.887695'),
('bcdfab12-6907-48de-a730-03fb1219a6ac', 'b4ac6e59-9a93-41b9-957a-82e999d72cc3', 'f3333333-3333-3333-3333-333333333333', 9, 'yes', '{"decision_maker": "yes"}', 20, '2025-08-20T10:19:36.887695'),
('ff685833-2244-4af1-9596-41923c2f8d5e', 'b4ac6e59-9a93-41b9-957a-82e999d72cc3', 'f3333333-3333-3333-3333-333333333333', 10, 'technology', '{"industry": "technology"}', 10, '2025-08-20T10:19:36.887695'),
('0609f659-7556-42c4-9949-e3011c95c2cb', 'b4ac6e59-9a93-41b9-957a-82e999d72cc3', 'f3333333-3333-3333-3333-333333333333', 11, 'no', '{"previous_consulting": "no"}', 10, '2025-08-20T10:19:36.887695');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('5af79a47-1b5d-4af4-ab2a-45ea0cfa5f5e', 'b4ac6e59-9a93-41b9-957a-82e999d72cc3', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'unqualified', '{"name": "Michelle_4 Brown", "email": "mbrown_4@startup.co"}', 30, 0.30, false, false, NULL, NULL, NULL);


-- Lead 20: Maybe - Thomas_4 Anderson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('198614ff-575b-4115-807f-0869ed896b99', 'f3333333-3333-3333-3333-333333333333', 'techsolve_020_maybe', 'a3333333-3333-3333-3333-333333333333', '2025-08-12T13:19:36.887755', '2025-08-12T13:48:36.887756', '2025-08-12T13:48:36.887756', 9, true, 68, 68, 'maybe', 'qualified', 'Thanks for your inquiry! We are evaluating how we can best support your technology needs. Our team will be in touch within a few days.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.163', '{"device_type": "desktop", "completion_time": 15}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('ce740658-c39b-496a-8625-e0af8fe24c70', '198614ff-575b-4115-807f-0869ed896b99', 'referral', 'referral', 'healthcare_tech', 'software consulting', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('4025ec3d-9b1f-43b4-addc-d5a73ea21b2d', '198614ff-575b-4115-807f-0869ed896b99', 'f3333333-3333-3333-3333-333333333333', 1, 'Thomas_4 Anderson', '{"name": "Thomas_4 Anderson"}', 10, '2025-08-12T13:19:36.887755'),
('7c16123c-ae5d-4461-9b09-da37391adce2', '198614ff-575b-4115-807f-0869ed896b99', 'f3333333-3333-3333-3333-333333333333', 2, 'tanderson_4@midcorp.com', '{"email": "tanderson_4@midcorp.com"}', 10, '2025-08-12T13:19:36.887755'),
('f02476a9-d7d7-400e-afaf-c0128d3d82db', '198614ff-575b-4115-807f-0869ed896b99', 'f3333333-3333-3333-3333-333333333333', 3, '(508) 555-4680', '{"phone": "(508) 555-4680"}', 15, '2025-08-12T13:19:36.887755'),
('c369df1b-0e7f-49ed-98d0-2b862127e32f', '198614ff-575b-4115-807f-0869ed896b99', 'f3333333-3333-3333-3333-333333333333', 4, '10_50_employees', '{"company_size": "10_50_employees"}', 20, '2025-08-12T13:19:36.887755'),
('74f92fd1-5a75-4887-a0e9-e4f30c5fabc7', '198614ff-575b-4115-807f-0869ed896b99', 'f3333333-3333-3333-3333-333333333333', 5, 'integration', '{"tech_challenges": "integration"}', 10, '2025-08-12T13:19:36.887755'),
('63ae7b8f-abc3-432f-a281-9ffc04dd7009', '198614ff-575b-4115-807f-0869ed896b99', 'f3333333-3333-3333-3333-333333333333', 6, '$25k_50k', '{"budget_range": "$25k_50k"}', 15, '2025-08-12T13:19:36.887755'),
('5d27e647-6063-4e55-a5dc-c05f39b8648a', '198614ff-575b-4115-807f-0869ed896b99', 'f3333333-3333-3333-3333-333333333333', 7, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-12T13:19:36.887755'),
('51e5230e-1dcf-4955-9875-0d17826f3e40', '198614ff-575b-4115-807f-0869ed896b99', 'f3333333-3333-3333-3333-333333333333', 8, 'mixed_cloud_onprem', '{"current_setup": "mixed_cloud_onprem"}', 10, '2025-08-12T13:19:36.887755'),
('2ff8ef48-6061-4068-8487-2b910e5f6db2', '198614ff-575b-4115-807f-0869ed896b99', 'f3333333-3333-3333-3333-333333333333', 9, 'shared', '{"decision_maker": "shared"}', 15, '2025-08-12T13:19:36.887755'),
('a4b70d44-f5aa-4b41-9abf-820c2149aa68', '198614ff-575b-4115-807f-0869ed896b99', 'f3333333-3333-3333-3333-333333333333', 10, 'healthcare', '{"industry": "healthcare"}', 10, '2025-08-12T13:19:36.887755'),
('3242cf99-ee02-47bd-91c5-87fc4406773d', '198614ff-575b-4115-807f-0869ed896b99', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_good', '{"previous_consulting": "yes_good"}', 10, '2025-08-12T13:19:36.887755');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('7099f37b-b87d-4333-be14-70623fb8e03b', '198614ff-575b-4115-807f-0869ed896b99', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'maybe', '{"name": "Thomas_4 Anderson", "email": "tanderson_4@midcorp.com", "phone": "(508) 555-4680"}', 68, 0.68, true, false, NULL, NULL, NULL);


-- Lead 21: Qualified - Robert_5 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('b64022a6-5bc2-488b-bf39-245abae6ef51', 'f3333333-3333-3333-3333-333333333333', 'techsolve_021_qualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-10T01:19:36.887817', '2025-08-10T01:41:36.887818', '2025-08-10T01:41:36.887818', 6, true, 92, 92, 'yes', 'qualified', 'Perfect! Your technology challenges align well with our expertise. Our senior consultant will reach out within 24 hours to discuss your project.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.141', '{"device_type": "desktop", "completion_time": 51}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('5d6bc2cd-31d4-44ab-8837-e89508eb54cc', 'b64022a6-5bc2-488b-bf39-245abae6ef51', 'linkedin', 'social', 'enterprise_solutions', 'software consulting', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('784d67b0-d42b-4722-b03d-6890b8eef2af', 'b64022a6-5bc2-488b-bf39-245abae6ef51', 'f3333333-3333-3333-3333-333333333333', 1, 'Robert_5 Kim', '{"name": "Robert_5 Kim"}', 10, '2025-08-10T01:19:36.887817'),
('76021bd5-688d-47cc-aba3-b07166a24cb1', 'b64022a6-5bc2-488b-bf39-245abae6ef51', 'f3333333-3333-3333-3333-333333333333', 2, 'robert.kim_5@enterprise.com', '{"email": "robert.kim_5@enterprise.com"}', 10, '2025-08-10T01:19:36.887817'),
('5096f4a2-755f-44e3-9b9d-4372f9a7d615', 'b64022a6-5bc2-488b-bf39-245abae6ef51', 'f3333333-3333-3333-3333-333333333333', 3, '(617) 555-2468', '{"phone": "(617) 555-2468"}', 15, '2025-08-10T01:19:36.887817'),
('03fd7345-d7c1-4c7a-8546-73d87e065ed2', 'b64022a6-5bc2-488b-bf39-245abae6ef51', 'f3333333-3333-3333-3333-333333333333', 4, '50_200_employees', '{"company_size": "50_200_employees"}', 25, '2025-08-10T01:19:36.887817'),
('3e11d322-5d45-48ce-b564-7dd5b4603d55', 'b64022a6-5bc2-488b-bf39-245abae6ef51', 'f3333333-3333-3333-3333-333333333333', 5, 'legacy_systems', '{"tech_challenges": "legacy_systems"}', 10, '2025-08-10T01:19:36.887817'),
('29c082e7-748e-4bbe-8f9c-c744b34939bf', 'b64022a6-5bc2-488b-bf39-245abae6ef51', 'f3333333-3333-3333-3333-333333333333', 6, '$50k_100k', '{"budget_range": "$50k_100k"}', 20, '2025-08-10T01:19:36.887817'),
('afc29829-7960-40f8-87ec-95f987c75f73', 'b64022a6-5bc2-488b-bf39-245abae6ef51', 'f3333333-3333-3333-3333-333333333333', 7, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-10T01:19:36.887817'),
('522f4e45-1b43-4306-a399-915d72d56072', 'b64022a6-5bc2-488b-bf39-245abae6ef51', 'f3333333-3333-3333-3333-333333333333', 8, 'mixed_cloud_onprem', '{"current_setup": "mixed_cloud_onprem"}', 10, '2025-08-10T01:19:36.887817'),
('adfd4e92-5756-4975-940e-4c8455b2199d', 'b64022a6-5bc2-488b-bf39-245abae6ef51', 'f3333333-3333-3333-3333-333333333333', 9, 'yes', '{"decision_maker": "yes"}', 20, '2025-08-10T01:19:36.887817'),
('8b45ee8f-6101-4990-b166-53f3390fbac4', 'b64022a6-5bc2-488b-bf39-245abae6ef51', 'f3333333-3333-3333-3333-333333333333', 10, 'manufacturing', '{"industry": "manufacturing"}', 10, '2025-08-10T01:19:36.887817'),
('dfba67bb-73f9-4fde-bf95-86896bd86058', 'b64022a6-5bc2-488b-bf39-245abae6ef51', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_good', '{"previous_consulting": "yes_good"}', 10, '2025-08-10T01:19:36.887817');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('a65ab6c3-4429-4472-ac66-2f087150a0c2', 'b64022a6-5bc2-488b-bf39-245abae6ef51', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'qualified', '{"name": "Robert_5 Kim", "email": "robert.kim_5@enterprise.com", "phone": "(617) 555-2468"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 22: Qualified - Patricia_5 Davis
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('b0dc7c3e-0784-4e7f-bd97-e904e9f80790', 'f3333333-3333-3333-3333-333333333333', 'techsolve_022_qualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-12T10:19:36.887879', '2025-08-12T10:35:36.887879', '2025-08-12T10:35:36.887879', 7, true, 78, 78, 'yes', 'qualified', 'Perfect! Your technology challenges align well with our expertise. Our senior consultant will reach out within 24 hours to discuss your project.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.105', '{"device_type": "desktop", "completion_time": 16}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('da66587e-8689-42ce-8da0-ca726fa5d017', 'b0dc7c3e-0784-4e7f-bd97-e904e9f80790', 'google', 'cpc', 'small_business_tech', 'digital transformation', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('f64a49a3-f891-4f5d-9c87-698221c5ea4d', 'b0dc7c3e-0784-4e7f-bd97-e904e9f80790', 'f3333333-3333-3333-3333-333333333333', 1, 'Patricia_5 Davis', '{"name": "Patricia_5 Davis"}', 10, '2025-08-12T10:19:36.887879'),
('72267528-343e-4db8-9d6b-002702845c18', 'b0dc7c3e-0784-4e7f-bd97-e904e9f80790', 'f3333333-3333-3333-3333-333333333333', 2, 'p.davis_5@retailchain.com', '{"email": "p.davis_5@retailchain.com"}', 10, '2025-08-12T10:19:36.887879'),
('000e2a4b-e769-4628-8a7d-ac2e64ec4867', 'b0dc7c3e-0784-4e7f-bd97-e904e9f80790', 'f3333333-3333-3333-3333-333333333333', 3, '(857) 555-1357', '{"phone": "(857) 555-1357"}', 15, '2025-08-12T10:19:36.887879'),
('a5f1ad68-70f4-4487-8b60-9920573bfa5d', 'b0dc7c3e-0784-4e7f-bd97-e904e9f80790', 'f3333333-3333-3333-3333-333333333333', 4, '10_50_employees', '{"company_size": "10_50_employees"}', 20, '2025-08-12T10:19:36.887879'),
('67360667-248a-43d7-97b6-bfc569b4a98a', 'b0dc7c3e-0784-4e7f-bd97-e904e9f80790', 'f3333333-3333-3333-3333-333333333333', 5, 'data_management', '{"tech_challenges": "data_management"}', 10, '2025-08-12T10:19:36.887879'),
('098fb3d0-bc8e-47c0-b3af-e9e4d21f6fc3', 'b0dc7c3e-0784-4e7f-bd97-e904e9f80790', 'f3333333-3333-3333-3333-333333333333', 6, '$25k_50k', '{"budget_range": "$25k_50k"}', 15, '2025-08-12T10:19:36.887879'),
('6101d7c4-a0fb-49de-b9c1-455d4f09b701', 'b0dc7c3e-0784-4e7f-bd97-e904e9f80790', 'f3333333-3333-3333-3333-333333333333', 7, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-12T10:19:36.887879'),
('8a9e01d6-a929-415f-80a1-0be09a4f5983', 'b0dc7c3e-0784-4e7f-bd97-e904e9f80790', 'f3333333-3333-3333-3333-333333333333', 8, 'mostly_cloud', '{"current_setup": "mostly_cloud"}', 10, '2025-08-12T10:19:36.887879'),
('a091c8c5-0a9e-4238-b482-c8ba25f40b9a', 'b0dc7c3e-0784-4e7f-bd97-e904e9f80790', 'f3333333-3333-3333-3333-333333333333', 9, 'shared', '{"decision_maker": "shared"}', 15, '2025-08-12T10:19:36.887879'),
('e15ba7ab-7f68-4a34-a861-9e0e3899f8fb', 'b0dc7c3e-0784-4e7f-bd97-e904e9f80790', 'f3333333-3333-3333-3333-333333333333', 10, 'retail', '{"industry": "retail"}', 10, '2025-08-12T10:19:36.887879'),
('125465e2-4a80-42ef-93a4-c4108ce4ef9d', 'b0dc7c3e-0784-4e7f-bd97-e904e9f80790', 'f3333333-3333-3333-3333-333333333333', 11, 'no', '{"previous_consulting": "no"}', 10, '2025-08-12T10:19:36.887879');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('7fcbb8b0-c383-4376-b472-e94204f29912', 'b0dc7c3e-0784-4e7f-bd97-e904e9f80790', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'qualified', '{"name": "Patricia_5 Davis", "email": "p.davis_5@retailchain.com", "phone": "(857) 555-1357"}', 78, 0.78, true, false, NULL, NULL, NULL);


-- Lead 23: Maybe - James_5 Wilson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('16057824-8ae3-422d-a898-998bcc80ba95', 'f3333333-3333-3333-3333-333333333333', 'techsolve_023_maybe', 'a3333333-3333-3333-3333-333333333333', '2025-08-23T07:19:36.887940', '2025-08-23T08:00:36.887941', '2025-08-23T08:00:36.887941', 7, true, 45, 45, 'maybe', 'qualified', 'Thanks for your inquiry! We are evaluating how we can best support your technology needs. Our team will be in touch within a few days.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.37', '{"device_type": "mobile", "completion_time": 11}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('02d2a78d-19cd-4217-9498-d838add51b0c', '16057824-8ae3-422d-a898-998bcc80ba95', 'organic', 'search', 'nonprofit_solutions', 'digital transformation', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('da62e708-16b7-452a-b72d-27fc6154ba8c', '16057824-8ae3-422d-a898-998bcc80ba95', 'f3333333-3333-3333-3333-333333333333', 1, 'James_5 Wilson', '{"name": "James_5 Wilson"}', 10, '2025-08-23T07:19:36.887940'),
('8d5aea9d-da3a-4729-8b7b-883c9e446024', '16057824-8ae3-422d-a898-998bcc80ba95', 'f3333333-3333-3333-3333-333333333333', 2, 'james.wilson_5@nonprofit.org', '{"email": "james.wilson_5@nonprofit.org"}', 10, '2025-08-23T07:19:36.887940'),
('9549d991-b4fe-4bc7-b520-7909faeea5cd', '16057824-8ae3-422d-a898-998bcc80ba95', 'f3333333-3333-3333-3333-333333333333', 3, '(617) 555-8024', '{"phone": "(617) 555-8024"}', 15, '2025-08-23T07:19:36.887940'),
('c6181df7-0bda-4ba4-a0c5-ab18a3605206', '16057824-8ae3-422d-a898-998bcc80ba95', 'f3333333-3333-3333-3333-333333333333', 4, 'under_10', '{"company_size": "under_10"}', 10, '2025-08-23T07:19:36.887940'),
('871ea5ce-43b0-486e-b196-bf2dc108ffbc', '16057824-8ae3-422d-a898-998bcc80ba95', 'f3333333-3333-3333-3333-333333333333', 5, 'security', '{"tech_challenges": "security"}', 10, '2025-08-23T07:19:36.887940'),
('88cc1e5d-91b0-4539-92d1-6f698e0ecccf', '16057824-8ae3-422d-a898-998bcc80ba95', 'f3333333-3333-3333-3333-333333333333', 6, 'under_25k', '{"budget_range": "under_25k"}', 5, '2025-08-23T07:19:36.887940'),
('67f3d6cc-8ff3-48a1-9661-63dcf75462bb', '16057824-8ae3-422d-a898-998bcc80ba95', 'f3333333-3333-3333-3333-333333333333', 7, '6_12_months', '{"timeline": "6_12_months"}', 10, '2025-08-23T07:19:36.887940'),
('48aa483e-6abc-4f9a-a289-b8b93d68eca9', '16057824-8ae3-422d-a898-998bcc80ba95', 'f3333333-3333-3333-3333-333333333333', 8, 'mostly_onprem', '{"current_setup": "mostly_onprem"}', 10, '2025-08-23T07:19:36.887940'),
('0490d7e0-e821-4627-a437-305ad80e32ec', '16057824-8ae3-422d-a898-998bcc80ba95', 'f3333333-3333-3333-3333-333333333333', 9, 'no', '{"decision_maker": "no"}', 5, '2025-08-23T07:19:36.887940'),
('ea95acc0-8749-4db7-85be-91b1399ffcba', '16057824-8ae3-422d-a898-998bcc80ba95', 'f3333333-3333-3333-3333-333333333333', 10, 'nonprofit', '{"industry": "nonprofit"}', 10, '2025-08-23T07:19:36.887940'),
('bfdf8bf2-8953-4c83-b4be-72ad3373dfd4', '16057824-8ae3-422d-a898-998bcc80ba95', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_mixed', '{"previous_consulting": "yes_mixed"}', 10, '2025-08-23T07:19:36.887940');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('699506cc-1d93-4567-8836-bee710e3ceac', '16057824-8ae3-422d-a898-998bcc80ba95', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'maybe', '{"name": "James_5 Wilson", "email": "james.wilson_5@nonprofit.org", "phone": "(617) 555-8024"}', 45, 0.45, true, false, NULL, NULL, NULL);


-- Lead 24: Unqualified - Michelle_5 Brown
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('20a06d7f-13ff-4b79-8970-3b02a5da2dc2', 'f3333333-3333-3333-3333-333333333333', 'techsolve_024_unqualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-17T13:19:36.888003', '2025-08-17T13:43:36.888004', '2025-08-17T13:43:36.888004', 11, true, 30, 30, 'no', 'qualified', 'Thank you for considering TechSolve. While your current requirements may not align with our services, feel free to contact us in the future.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.222', '{"device_type": "mobile", "completion_time": 22}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('a11a3cbe-c0e1-4923-bd22-f59e3f16a52b', '20a06d7f-13ff-4b79-8970-3b02a5da2dc2', 'organic', 'search', 'startup_resources', 'digital transformation', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('4beab896-dc1b-4d1c-b554-5d3f039a7e52', '20a06d7f-13ff-4b79-8970-3b02a5da2dc2', 'f3333333-3333-3333-3333-333333333333', 1, 'Michelle_5 Brown', '{"name": "Michelle_5 Brown"}', 10, '2025-08-17T13:19:36.888003'),
('1942f64c-a2f6-46ae-aa2c-c2fbd3c82354', '20a06d7f-13ff-4b79-8970-3b02a5da2dc2', 'f3333333-3333-3333-3333-333333333333', 2, 'mbrown_5@startup.co', '{"email": "mbrown_5@startup.co"}', 10, '2025-08-17T13:19:36.888003'),
('d3f6946b-715d-43ed-85ce-e19d071d453a', '20a06d7f-13ff-4b79-8970-3b02a5da2dc2', 'f3333333-3333-3333-3333-333333333333', 4, 'under_10', '{"company_size": "under_10"}', 10, '2025-08-17T13:19:36.888003'),
('2e77f265-1647-4fd4-950d-6b891cc97ec8', '20a06d7f-13ff-4b79-8970-3b02a5da2dc2', 'f3333333-3333-3333-3333-333333333333', 5, 'scaling', '{"tech_challenges": "scaling"}', 10, '2025-08-17T13:19:36.888003'),
('79262cb2-6586-4271-af6d-79652e825c83', '20a06d7f-13ff-4b79-8970-3b02a5da2dc2', 'f3333333-3333-3333-3333-333333333333', 6, 'under_25k', '{"budget_range": "under_25k"}', 5, '2025-08-17T13:19:36.888003'),
('91bfe443-dc8c-4154-973b-107febcf7c8e', '20a06d7f-13ff-4b79-8970-3b02a5da2dc2', 'f3333333-3333-3333-3333-333333333333', 7, 'just_exploring', '{"timeline": "just_exploring"}', 0, '2025-08-17T13:19:36.888003'),
('0d9fc3a8-857c-47a5-b6ad-7727a7074a89', '20a06d7f-13ff-4b79-8970-3b02a5da2dc2', 'f3333333-3333-3333-3333-333333333333', 8, 'all_cloud', '{"current_setup": "all_cloud"}', 10, '2025-08-17T13:19:36.888003'),
('320cac13-196c-41b8-89bb-fbcdda20d60e', '20a06d7f-13ff-4b79-8970-3b02a5da2dc2', 'f3333333-3333-3333-3333-333333333333', 9, 'yes', '{"decision_maker": "yes"}', 20, '2025-08-17T13:19:36.888003'),
('2f8471e7-ad27-4c7c-b20a-bcc7d768b528', '20a06d7f-13ff-4b79-8970-3b02a5da2dc2', 'f3333333-3333-3333-3333-333333333333', 10, 'technology', '{"industry": "technology"}', 10, '2025-08-17T13:19:36.888003'),
('e09a45dc-ba86-420c-8c3a-6ab60c93fc23', '20a06d7f-13ff-4b79-8970-3b02a5da2dc2', 'f3333333-3333-3333-3333-333333333333', 11, 'no', '{"previous_consulting": "no"}', 10, '2025-08-17T13:19:36.888003');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('bf157555-21a0-4527-9795-abe6413d3bdc', '20a06d7f-13ff-4b79-8970-3b02a5da2dc2', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'unqualified', '{"name": "Michelle_5 Brown", "email": "mbrown_5@startup.co"}', 30, 0.30, false, false, NULL, NULL, NULL);


-- Lead 25: Maybe - Thomas_5 Anderson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('e6a3aada-67a0-4573-b7ab-d1dde76e2fd5', 'f3333333-3333-3333-3333-333333333333', 'techsolve_025_maybe', 'a3333333-3333-3333-3333-333333333333', '2025-08-11T01:19:36.888061', '2025-08-11T01:47:36.888062', '2025-08-11T01:47:36.888062', 7, true, 68, 68, 'maybe', 'qualified', 'Thanks for your inquiry! We are evaluating how we can best support your technology needs. Our team will be in touch within a few days.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.163', '{"device_type": "desktop", "completion_time": 56}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('0f37aeae-9212-4608-8d3b-2a6787e13d97', 'e6a3aada-67a0-4573-b7ab-d1dde76e2fd5', 'referral', 'referral', 'healthcare_tech', 'tech support services', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('2d274aa2-52fa-4ca1-a7ec-e5c049f5b258', 'e6a3aada-67a0-4573-b7ab-d1dde76e2fd5', 'f3333333-3333-3333-3333-333333333333', 1, 'Thomas_5 Anderson', '{"name": "Thomas_5 Anderson"}', 10, '2025-08-11T01:19:36.888061'),
('4d25d386-0d23-4715-8bb3-2d6e15deb542', 'e6a3aada-67a0-4573-b7ab-d1dde76e2fd5', 'f3333333-3333-3333-3333-333333333333', 2, 'tanderson_5@midcorp.com', '{"email": "tanderson_5@midcorp.com"}', 10, '2025-08-11T01:19:36.888061'),
('1e135689-d262-49ee-a189-f9ac808feb6f', 'e6a3aada-67a0-4573-b7ab-d1dde76e2fd5', 'f3333333-3333-3333-3333-333333333333', 3, '(508) 555-4680', '{"phone": "(508) 555-4680"}', 15, '2025-08-11T01:19:36.888061'),
('8cd244fc-3bc1-4ae9-b246-b1d36ea0a6a6', 'e6a3aada-67a0-4573-b7ab-d1dde76e2fd5', 'f3333333-3333-3333-3333-333333333333', 4, '10_50_employees', '{"company_size": "10_50_employees"}', 20, '2025-08-11T01:19:36.888061'),
('fab73d13-8125-4315-a553-43e185cf7992', 'e6a3aada-67a0-4573-b7ab-d1dde76e2fd5', 'f3333333-3333-3333-3333-333333333333', 5, 'integration', '{"tech_challenges": "integration"}', 10, '2025-08-11T01:19:36.888061'),
('7a03fe15-b8ae-432f-a2ac-5a043c4b3b51', 'e6a3aada-67a0-4573-b7ab-d1dde76e2fd5', 'f3333333-3333-3333-3333-333333333333', 6, '$25k_50k', '{"budget_range": "$25k_50k"}', 15, '2025-08-11T01:19:36.888061'),
('39b33560-afcd-4240-82bf-ab8a9e054745', 'e6a3aada-67a0-4573-b7ab-d1dde76e2fd5', 'f3333333-3333-3333-3333-333333333333', 7, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-11T01:19:36.888061'),
('b02116c8-246d-4d53-b2a0-b099875861ad', 'e6a3aada-67a0-4573-b7ab-d1dde76e2fd5', 'f3333333-3333-3333-3333-333333333333', 8, 'mixed_cloud_onprem', '{"current_setup": "mixed_cloud_onprem"}', 10, '2025-08-11T01:19:36.888061'),
('4601e84a-ec9d-4ecc-9443-b46e3bbf70ae', 'e6a3aada-67a0-4573-b7ab-d1dde76e2fd5', 'f3333333-3333-3333-3333-333333333333', 9, 'shared', '{"decision_maker": "shared"}', 15, '2025-08-11T01:19:36.888061'),
('6c36a98e-c724-48d5-97b1-b37c51b1948a', 'e6a3aada-67a0-4573-b7ab-d1dde76e2fd5', 'f3333333-3333-3333-3333-333333333333', 10, 'healthcare', '{"industry": "healthcare"}', 10, '2025-08-11T01:19:36.888061'),
('4ac7751a-75c5-4749-a8df-b613f65a1933', 'e6a3aada-67a0-4573-b7ab-d1dde76e2fd5', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_good', '{"previous_consulting": "yes_good"}', 10, '2025-08-11T01:19:36.888061');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('736f553b-e38b-4855-9059-705d1f1e0e2d', 'e6a3aada-67a0-4573-b7ab-d1dde76e2fd5', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'maybe', '{"name": "Thomas_5 Anderson", "email": "tanderson_5@midcorp.com", "phone": "(508) 555-4680"}', 68, 0.68, true, false, NULL, NULL, NULL);


-- Lead 26: Qualified - Robert_6 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('5b180bbe-61c5-4be1-8753-3c8e350e4253', 'f3333333-3333-3333-3333-333333333333', 'techsolve_026_qualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-22T15:19:36.888123', '2025-08-22T16:04:36.888124', '2025-08-22T16:04:36.888124', 8, true, 92, 92, 'yes', 'qualified', 'Perfect! Your technology challenges align well with our expertise. Our senior consultant will reach out within 24 hours to discuss your project.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.249', '{"device_type": "desktop", "completion_time": 30}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('44779dce-5c07-4982-9ac1-1ed81b01377e', '5b180bbe-61c5-4be1-8753-3c8e350e4253', 'linkedin', 'social', 'enterprise_solutions', 'technology solutions', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('f738cfd5-3fb4-424c-bfed-f5452904c820', '5b180bbe-61c5-4be1-8753-3c8e350e4253', 'f3333333-3333-3333-3333-333333333333', 1, 'Robert_6 Kim', '{"name": "Robert_6 Kim"}', 10, '2025-08-22T15:19:36.888123'),
('eb47429a-d4f2-4c73-aa0b-947855bc6294', '5b180bbe-61c5-4be1-8753-3c8e350e4253', 'f3333333-3333-3333-3333-333333333333', 2, 'robert.kim_6@enterprise.com', '{"email": "robert.kim_6@enterprise.com"}', 10, '2025-08-22T15:19:36.888123'),
('43f053af-5aef-4f94-9943-06c0e83dc196', '5b180bbe-61c5-4be1-8753-3c8e350e4253', 'f3333333-3333-3333-3333-333333333333', 3, '(617) 555-2468', '{"phone": "(617) 555-2468"}', 15, '2025-08-22T15:19:36.888123'),
('2defa813-58af-4d0f-80cc-1d1f5df40e63', '5b180bbe-61c5-4be1-8753-3c8e350e4253', 'f3333333-3333-3333-3333-333333333333', 4, '50_200_employees', '{"company_size": "50_200_employees"}', 25, '2025-08-22T15:19:36.888123'),
('4740ed0e-beeb-4351-bc4b-e933cea3c48f', '5b180bbe-61c5-4be1-8753-3c8e350e4253', 'f3333333-3333-3333-3333-333333333333', 5, 'legacy_systems', '{"tech_challenges": "legacy_systems"}', 10, '2025-08-22T15:19:36.888123'),
('b386edac-db3e-4691-b5b0-0d804c25bf4a', '5b180bbe-61c5-4be1-8753-3c8e350e4253', 'f3333333-3333-3333-3333-333333333333', 6, '$50k_100k', '{"budget_range": "$50k_100k"}', 20, '2025-08-22T15:19:36.888123'),
('72200b1a-53cb-410e-8084-9647a3484a38', '5b180bbe-61c5-4be1-8753-3c8e350e4253', 'f3333333-3333-3333-3333-333333333333', 7, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-22T15:19:36.888123'),
('81e67304-b8a8-42d4-ac6a-8e5dccc2d057', '5b180bbe-61c5-4be1-8753-3c8e350e4253', 'f3333333-3333-3333-3333-333333333333', 8, 'mixed_cloud_onprem', '{"current_setup": "mixed_cloud_onprem"}', 10, '2025-08-22T15:19:36.888123'),
('ce4dfd5b-cd6f-43cb-8c66-6d2888a533a4', '5b180bbe-61c5-4be1-8753-3c8e350e4253', 'f3333333-3333-3333-3333-333333333333', 9, 'yes', '{"decision_maker": "yes"}', 20, '2025-08-22T15:19:36.888123'),
('e45edc31-cc12-4bb9-ada6-290fe910db4b', '5b180bbe-61c5-4be1-8753-3c8e350e4253', 'f3333333-3333-3333-3333-333333333333', 10, 'manufacturing', '{"industry": "manufacturing"}', 10, '2025-08-22T15:19:36.888123'),
('0685813a-595b-47e2-93ad-f657bf77b1fa', '5b180bbe-61c5-4be1-8753-3c8e350e4253', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_good', '{"previous_consulting": "yes_good"}', 10, '2025-08-22T15:19:36.888123');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('73c74718-1200-41ec-8c3c-96d410143ce2', '5b180bbe-61c5-4be1-8753-3c8e350e4253', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'qualified', '{"name": "Robert_6 Kim", "email": "robert.kim_6@enterprise.com", "phone": "(617) 555-2468"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 27: Qualified - Patricia_6 Davis
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('edf0859a-1878-47ca-964d-dc33ce8187a8', 'f3333333-3333-3333-3333-333333333333', 'techsolve_027_qualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-22T21:19:36.888185', '2025-08-22T22:02:36.888186', '2025-08-22T22:02:36.888186', 6, true, 78, 78, 'yes', 'qualified', 'Perfect! Your technology challenges align well with our expertise. Our senior consultant will reach out within 24 hours to discuss your project.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.131', '{"device_type": "desktop", "completion_time": 60}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('a625e7e4-cdd3-4eba-8de0-97aebe772d45', 'edf0859a-1878-47ca-964d-dc33ce8187a8', 'google', 'cpc', 'small_business_tech', 'IT consulting boston', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Brookline');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('7dc4ca34-86ff-4106-8225-e81f08f70fd8', 'edf0859a-1878-47ca-964d-dc33ce8187a8', 'f3333333-3333-3333-3333-333333333333', 1, 'Patricia_6 Davis', '{"name": "Patricia_6 Davis"}', 10, '2025-08-22T21:19:36.888185'),
('0bdc5dd9-8c5b-4cf3-8996-463798f2b4d5', 'edf0859a-1878-47ca-964d-dc33ce8187a8', 'f3333333-3333-3333-3333-333333333333', 2, 'p.davis_6@retailchain.com', '{"email": "p.davis_6@retailchain.com"}', 10, '2025-08-22T21:19:36.888185'),
('28d217e9-e730-4982-b509-6ea22f7f5e8a', 'edf0859a-1878-47ca-964d-dc33ce8187a8', 'f3333333-3333-3333-3333-333333333333', 3, '(857) 555-1357', '{"phone": "(857) 555-1357"}', 15, '2025-08-22T21:19:36.888185'),
('595bc2fb-29f3-46ef-862f-db6a9202e64c', 'edf0859a-1878-47ca-964d-dc33ce8187a8', 'f3333333-3333-3333-3333-333333333333', 4, '10_50_employees', '{"company_size": "10_50_employees"}', 20, '2025-08-22T21:19:36.888185'),
('9a77d8e7-b28f-4a4e-8b8d-f7e56cd9e325', 'edf0859a-1878-47ca-964d-dc33ce8187a8', 'f3333333-3333-3333-3333-333333333333', 5, 'data_management', '{"tech_challenges": "data_management"}', 10, '2025-08-22T21:19:36.888185'),
('77ab4482-746f-4c20-ae0d-658d2664c2cb', 'edf0859a-1878-47ca-964d-dc33ce8187a8', 'f3333333-3333-3333-3333-333333333333', 6, '$25k_50k', '{"budget_range": "$25k_50k"}', 15, '2025-08-22T21:19:36.888185'),
('bf111756-30fc-4e46-ae0e-928a57d7000b', 'edf0859a-1878-47ca-964d-dc33ce8187a8', 'f3333333-3333-3333-3333-333333333333', 7, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-22T21:19:36.888185'),
('413a01bd-4845-4817-a631-4122e06b964c', 'edf0859a-1878-47ca-964d-dc33ce8187a8', 'f3333333-3333-3333-3333-333333333333', 8, 'mostly_cloud', '{"current_setup": "mostly_cloud"}', 10, '2025-08-22T21:19:36.888185'),
('344427e8-8d41-4508-b170-482ada636594', 'edf0859a-1878-47ca-964d-dc33ce8187a8', 'f3333333-3333-3333-3333-333333333333', 9, 'shared', '{"decision_maker": "shared"}', 15, '2025-08-22T21:19:36.888185'),
('ddb0daf2-bc5e-4c4c-81da-8394f336a27b', 'edf0859a-1878-47ca-964d-dc33ce8187a8', 'f3333333-3333-3333-3333-333333333333', 10, 'retail', '{"industry": "retail"}', 10, '2025-08-22T21:19:36.888185'),
('f61d10a4-f4e0-4e9a-bb33-4cb31046574a', 'edf0859a-1878-47ca-964d-dc33ce8187a8', 'f3333333-3333-3333-3333-333333333333', 11, 'no', '{"previous_consulting": "no"}', 10, '2025-08-22T21:19:36.888185');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('524e3865-5634-4c92-a2d0-a1fd5ffdd402', 'edf0859a-1878-47ca-964d-dc33ce8187a8', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'qualified', '{"name": "Patricia_6 Davis", "email": "p.davis_6@retailchain.com", "phone": "(857) 555-1357"}', 78, 0.78, true, false, NULL, NULL, NULL);


-- Lead 28: Maybe - James_6 Wilson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('d66a2a18-b229-4f50-8ad7-e4c49f9b8b9e', 'f3333333-3333-3333-3333-333333333333', 'techsolve_028_maybe', 'a3333333-3333-3333-3333-333333333333', '2025-08-22T09:19:36.888249', '2025-08-22T09:47:36.888249', '2025-08-22T09:47:36.888249', 9, true, 45, 45, 'maybe', 'qualified', 'Thanks for your inquiry! We are evaluating how we can best support your technology needs. Our team will be in touch within a few days.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.109', '{"device_type": "mobile", "completion_time": 40}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('ea31385f-249b-4c3e-8b40-b180cd72701f', 'd66a2a18-b229-4f50-8ad7-e4c49f9b8b9e', 'organic', 'search', 'nonprofit_solutions', 'digital transformation', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('54f6916e-8c51-42dd-95eb-6dc92dcd1732', 'd66a2a18-b229-4f50-8ad7-e4c49f9b8b9e', 'f3333333-3333-3333-3333-333333333333', 1, 'James_6 Wilson', '{"name": "James_6 Wilson"}', 10, '2025-08-22T09:19:36.888249'),
('5f8a7998-a2fb-4df0-9fc9-1f07f6574dea', 'd66a2a18-b229-4f50-8ad7-e4c49f9b8b9e', 'f3333333-3333-3333-3333-333333333333', 2, 'james.wilson_6@nonprofit.org', '{"email": "james.wilson_6@nonprofit.org"}', 10, '2025-08-22T09:19:36.888249'),
('d50985a2-e119-4989-85a3-9d35eb3246f0', 'd66a2a18-b229-4f50-8ad7-e4c49f9b8b9e', 'f3333333-3333-3333-3333-333333333333', 3, '(617) 555-8024', '{"phone": "(617) 555-8024"}', 15, '2025-08-22T09:19:36.888249'),
('bdb53de4-ca22-4489-94d1-5a7c23e39589', 'd66a2a18-b229-4f50-8ad7-e4c49f9b8b9e', 'f3333333-3333-3333-3333-333333333333', 4, 'under_10', '{"company_size": "under_10"}', 10, '2025-08-22T09:19:36.888249'),
('e74c62a0-8573-47fc-b5e8-ad7afc4fb228', 'd66a2a18-b229-4f50-8ad7-e4c49f9b8b9e', 'f3333333-3333-3333-3333-333333333333', 5, 'security', '{"tech_challenges": "security"}', 10, '2025-08-22T09:19:36.888249'),
('4fa6243e-1dc3-4c03-861f-487aa38e9bff', 'd66a2a18-b229-4f50-8ad7-e4c49f9b8b9e', 'f3333333-3333-3333-3333-333333333333', 6, 'under_25k', '{"budget_range": "under_25k"}', 5, '2025-08-22T09:19:36.888249'),
('fccc6a8f-d804-4ec6-84a6-132b1dedc725', 'd66a2a18-b229-4f50-8ad7-e4c49f9b8b9e', 'f3333333-3333-3333-3333-333333333333', 7, '6_12_months', '{"timeline": "6_12_months"}', 10, '2025-08-22T09:19:36.888249'),
('2ddf17a8-6592-445f-80d8-72471422a71b', 'd66a2a18-b229-4f50-8ad7-e4c49f9b8b9e', 'f3333333-3333-3333-3333-333333333333', 8, 'mostly_onprem', '{"current_setup": "mostly_onprem"}', 10, '2025-08-22T09:19:36.888249'),
('a0424194-7c20-4551-b8e5-0addfc5414ef', 'd66a2a18-b229-4f50-8ad7-e4c49f9b8b9e', 'f3333333-3333-3333-3333-333333333333', 9, 'no', '{"decision_maker": "no"}', 5, '2025-08-22T09:19:36.888249'),
('7dcba28c-eea1-44d4-917a-9c7ef0ce9331', 'd66a2a18-b229-4f50-8ad7-e4c49f9b8b9e', 'f3333333-3333-3333-3333-333333333333', 10, 'nonprofit', '{"industry": "nonprofit"}', 10, '2025-08-22T09:19:36.888249'),
('99ecca1c-c1b3-4300-b65e-093673d14aec', 'd66a2a18-b229-4f50-8ad7-e4c49f9b8b9e', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_mixed', '{"previous_consulting": "yes_mixed"}', 10, '2025-08-22T09:19:36.888249');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('f0189ac9-8b95-4dbb-90bb-596380678570', 'd66a2a18-b229-4f50-8ad7-e4c49f9b8b9e', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'maybe', '{"name": "James_6 Wilson", "email": "james.wilson_6@nonprofit.org", "phone": "(617) 555-8024"}', 45, 0.45, true, false, NULL, NULL, NULL);


-- Lead 29: Unqualified - Michelle_6 Brown
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('b09c4973-4fb8-4258-9314-398f8c942c45', 'f3333333-3333-3333-3333-333333333333', 'techsolve_029_unqualified', 'a3333333-3333-3333-3333-333333333333', '2025-08-20T10:19:36.888310', '2025-08-20T10:58:36.888310', '2025-08-20T10:58:36.888310', 7, true, 30, 30, 'no', 'qualified', 'Thank you for considering TechSolve. While your current requirements may not align with our services, feel free to contact us in the future.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.60', '{"device_type": "mobile", "completion_time": 11}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('7804d63e-bbe4-4ac7-b328-b754a2061962', 'b09c4973-4fb8-4258-9314-398f8c942c45', 'organic', 'search', 'startup_resources', 'IT consulting boston', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('755dda2e-aff8-4432-bb89-fe7a10414eaf', 'b09c4973-4fb8-4258-9314-398f8c942c45', 'f3333333-3333-3333-3333-333333333333', 1, 'Michelle_6 Brown', '{"name": "Michelle_6 Brown"}', 10, '2025-08-20T10:19:36.888310'),
('ec450eb0-9887-42ca-a954-56621aba92c2', 'b09c4973-4fb8-4258-9314-398f8c942c45', 'f3333333-3333-3333-3333-333333333333', 2, 'mbrown_6@startup.co', '{"email": "mbrown_6@startup.co"}', 10, '2025-08-20T10:19:36.888310'),
('1eac107f-f363-4816-a197-65ade80fd7b2', 'b09c4973-4fb8-4258-9314-398f8c942c45', 'f3333333-3333-3333-3333-333333333333', 4, 'under_10', '{"company_size": "under_10"}', 10, '2025-08-20T10:19:36.888310'),
('0442d819-091c-4288-9231-e7a929e7e347', 'b09c4973-4fb8-4258-9314-398f8c942c45', 'f3333333-3333-3333-3333-333333333333', 5, 'scaling', '{"tech_challenges": "scaling"}', 10, '2025-08-20T10:19:36.888310'),
('dfbe52f8-794b-416a-aed4-3be7bef7ffe5', 'b09c4973-4fb8-4258-9314-398f8c942c45', 'f3333333-3333-3333-3333-333333333333', 6, 'under_25k', '{"budget_range": "under_25k"}', 5, '2025-08-20T10:19:36.888310'),
('f171a5f8-9de1-4e95-914a-b9bdcf1de3ae', 'b09c4973-4fb8-4258-9314-398f8c942c45', 'f3333333-3333-3333-3333-333333333333', 7, 'just_exploring', '{"timeline": "just_exploring"}', 0, '2025-08-20T10:19:36.888310'),
('1dd84596-977b-4ef5-81e4-84b275991022', 'b09c4973-4fb8-4258-9314-398f8c942c45', 'f3333333-3333-3333-3333-333333333333', 8, 'all_cloud', '{"current_setup": "all_cloud"}', 10, '2025-08-20T10:19:36.888310'),
('e9b85eac-0d5e-4577-988a-97d42bea0b8c', 'b09c4973-4fb8-4258-9314-398f8c942c45', 'f3333333-3333-3333-3333-333333333333', 9, 'yes', '{"decision_maker": "yes"}', 20, '2025-08-20T10:19:36.888310'),
('903695b5-3080-4f7b-b1a7-63214842ea3e', 'b09c4973-4fb8-4258-9314-398f8c942c45', 'f3333333-3333-3333-3333-333333333333', 10, 'technology', '{"industry": "technology"}', 10, '2025-08-20T10:19:36.888310'),
('f9a683ab-1d57-419f-a495-ab9c5c56502d', 'b09c4973-4fb8-4258-9314-398f8c942c45', 'f3333333-3333-3333-3333-333333333333', 11, 'no', '{"previous_consulting": "no"}', 10, '2025-08-20T10:19:36.888310');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('4e886bf2-7b81-40d0-9835-fac148e82485', 'b09c4973-4fb8-4258-9314-398f8c942c45', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'unqualified', '{"name": "Michelle_6 Brown", "email": "mbrown_6@startup.co"}', 30, 0.30, false, false, NULL, NULL, NULL);


-- Lead 30: Maybe - Thomas_6 Anderson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('55b7e9e1-a1fc-4df8-bdcd-90f79cee72a5', 'f3333333-3333-3333-3333-333333333333', 'techsolve_030_maybe', 'a3333333-3333-3333-3333-333333333333', '2025-08-23T11:19:36.888366', '2025-08-23T11:38:36.888367', '2025-08-23T11:38:36.888367', 7, true, 68, 68, 'maybe', 'qualified', 'Thanks for your inquiry! We are evaluating how we can best support your technology needs. Our team will be in touch within a few days.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.142', '{"device_type": "desktop", "completion_time": 48}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('d3c97d3a-d0e1-4807-b400-0d0b214e4ab3', '55b7e9e1-a1fc-4df8-bdcd-90f79cee72a5', 'referral', 'referral', 'healthcare_tech', 'IT consulting boston', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('90377186-cf53-41ac-b161-961913fd31b4', '55b7e9e1-a1fc-4df8-bdcd-90f79cee72a5', 'f3333333-3333-3333-3333-333333333333', 1, 'Thomas_6 Anderson', '{"name": "Thomas_6 Anderson"}', 10, '2025-08-23T11:19:36.888366'),
('060da721-338e-4a48-a587-4826d69b9b76', '55b7e9e1-a1fc-4df8-bdcd-90f79cee72a5', 'f3333333-3333-3333-3333-333333333333', 2, 'tanderson_6@midcorp.com', '{"email": "tanderson_6@midcorp.com"}', 10, '2025-08-23T11:19:36.888366'),
('b7b52cdd-c341-4f7b-907d-643648d7720b', '55b7e9e1-a1fc-4df8-bdcd-90f79cee72a5', 'f3333333-3333-3333-3333-333333333333', 3, '(508) 555-4680', '{"phone": "(508) 555-4680"}', 15, '2025-08-23T11:19:36.888366'),
('cfdd68cb-72b4-41da-b912-2aaa3c93043e', '55b7e9e1-a1fc-4df8-bdcd-90f79cee72a5', 'f3333333-3333-3333-3333-333333333333', 4, '10_50_employees', '{"company_size": "10_50_employees"}', 20, '2025-08-23T11:19:36.888366'),
('176cda03-12b8-474a-8957-7624ff2c5322', '55b7e9e1-a1fc-4df8-bdcd-90f79cee72a5', 'f3333333-3333-3333-3333-333333333333', 5, 'integration', '{"tech_challenges": "integration"}', 10, '2025-08-23T11:19:36.888366'),
('20d87a92-f2fa-496f-87c1-47bc2048074c', '55b7e9e1-a1fc-4df8-bdcd-90f79cee72a5', 'f3333333-3333-3333-3333-333333333333', 6, '$25k_50k', '{"budget_range": "$25k_50k"}', 15, '2025-08-23T11:19:36.888366'),
('e42cda18-828f-451e-9758-312319ee1897', '55b7e9e1-a1fc-4df8-bdcd-90f79cee72a5', 'f3333333-3333-3333-3333-333333333333', 7, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-23T11:19:36.888366'),
('07e2b408-89eb-4472-a378-ca1247b29a0d', '55b7e9e1-a1fc-4df8-bdcd-90f79cee72a5', 'f3333333-3333-3333-3333-333333333333', 8, 'mixed_cloud_onprem', '{"current_setup": "mixed_cloud_onprem"}', 10, '2025-08-23T11:19:36.888366'),
('7620f103-029f-4c5a-853f-84165921c0bd', '55b7e9e1-a1fc-4df8-bdcd-90f79cee72a5', 'f3333333-3333-3333-3333-333333333333', 9, 'shared', '{"decision_maker": "shared"}', 15, '2025-08-23T11:19:36.888366'),
('54456300-3964-4c0c-b4db-324bdb816683', '55b7e9e1-a1fc-4df8-bdcd-90f79cee72a5', 'f3333333-3333-3333-3333-333333333333', 10, 'healthcare', '{"industry": "healthcare"}', 10, '2025-08-23T11:19:36.888366'),
('f068c8e7-645e-409e-beae-a29789952a9f', '55b7e9e1-a1fc-4df8-bdcd-90f79cee72a5', 'f3333333-3333-3333-3333-333333333333', 11, 'yes_good', '{"previous_consulting": "yes_good"}', 10, '2025-08-23T11:19:36.888366');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('e374970a-06f7-4406-9685-405da92901bc', '55b7e9e1-a1fc-4df8-bdcd-90f79cee72a5', 'a3333333-3333-3333-3333-333333333333', 'f3333333-3333-3333-3333-333333333333', 'maybe', '{"name": "Thomas_6 Anderson", "email": "tanderson_6@midcorp.com", "phone": "(508) 555-4680"}', 68, 0.68, true, false, NULL, NULL, NULL);


SELECT 'Generated 30 realistic lead sessions for techsolve!' as status;

