-- Test Data for Sparkle Clean Solutions (Home Cleaning)
-- Generated 30 realistic lead sessions with complete tracking and outcomes
-- Client: sparkle_clean | Form: f5555555-5555-5555-5555-555555555555 | Generated: 2025-08-24T20:19:32



-- Lead 1: Qualified - Helen Smith
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('c1c8aaca-7345-4a6a-b061-d3df1a026e4a', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_001_qualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-22T06:19:32.007054', '2025-08-22T06:44:32.007060', '2025-08-22T06:44:32.007060', 8, true, 90, 90, 'yes', 'qualified', 'Perfect! Your cleaning needs match our services perfectly. We will contact you within 24 hours to schedule your first appointment.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.63', '{"device_type": "desktop", "completion_time": 38}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('16a67e5e-703f-46df-86ca-3ca1e7613541', 'c1c8aaca-7345-4a6a-b061-d3df1a026e4a', 'google', 'cpc', 'luxury_home_cleaning', 'residential cleaning', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('17c6959f-fe7f-4101-b6d6-1b1fe2f2d72a', 'c1c8aaca-7345-4a6a-b061-d3df1a026e4a', 'f5555555-5555-5555-5555-555555555555', 1, 'Helen Smith', '{"name": "Helen Smith"}', 10, '2025-08-22T06:19:32.007054'),
('d30aaa46-d366-458b-8c96-17c0f65ca801', 'c1c8aaca-7345-4a6a-b061-d3df1a026e4a', 'f5555555-5555-5555-5555-555555555555', 2, 'helen.smith@lawfirm.com', '{"email": "helen.smith@lawfirm.com"}', 10, '2025-08-22T06:19:32.007054'),
('e05dad9d-561c-4e20-aa4a-8c3b639a7420', 'c1c8aaca-7345-4a6a-b061-d3df1a026e4a', 'f5555555-5555-5555-5555-555555555555', 3, '(617) 555-2580', '{"phone": "(617) 555-2580"}', 15, '2025-08-22T06:19:32.007054'),
('6a3436b0-d776-4ff6-a38f-51731508329f', 'c1c8aaca-7345-4a6a-b061-d3df1a026e4a', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-22T06:19:32.007054'),
('fc758a89-7e0a-4838-80a4-9672352b8a9f', 'c1c8aaca-7345-4a6a-b061-d3df1a026e4a', 'f5555555-5555-5555-5555-555555555555', 5, 'large_4plus_bed', '{"home_size": "large_4plus_bed"}', 20, '2025-08-22T06:19:32.007054'),
('fd75f72e-56c6-4bb7-98ac-a0135845572e', 'c1c8aaca-7345-4a6a-b061-d3df1a026e4a', 'f5555555-5555-5555-5555-555555555555', 6, 'weekly', '{"frequency": "weekly"}', 25, '2025-08-22T06:19:32.007054'),
('3d616e87-244f-4f65-b773-64293e6f13ac', 'c1c8aaca-7345-4a6a-b061-d3df1a026e4a', 'f5555555-5555-5555-5555-555555555555', 7, 'pet_friendly', '{"special_requirements": "pet_friendly"}', 10, '2025-08-22T06:19:32.007054'),
('55f15d46-650b-4ca6-b1bd-83a538a579e7', 'c1c8aaca-7345-4a6a-b061-d3df1a026e4a', 'f5555555-5555-5555-5555-555555555555', 8, '$150_plus', '{"budget": "$150_plus"}', 25, '2025-08-22T06:19:32.007054'),
('fc20d886-d601-4367-873e-88d7e979d363', 'c1c8aaca-7345-4a6a-b061-d3df1a026e4a', 'f5555555-5555-5555-5555-555555555555', 9, 'cambridge', '{"location": "cambridge"}', 10, '2025-08-22T06:19:32.007054');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('312128f9-7a36-4a93-a4ca-54e2f8f0e02e', 'c1c8aaca-7345-4a6a-b061-d3df1a026e4a', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'qualified', '{"name": "Helen Smith", "email": "helen.smith@lawfirm.com", "phone": "(617) 555-2580"}', 90, 0.90, true, false, NULL, NULL, NULL);


-- Lead 2: Qualified - Carlos Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('e71033bc-1f33-4d44-b8c9-7e49bc186303', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_002_qualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-17T09:19:32.007161', '2025-08-17T09:51:32.007163', '2025-08-17T09:51:32.007163', 6, true, 82, 82, 'yes', 'qualified', 'Perfect! Your cleaning needs match our services perfectly. We will contact you within 24 hours to schedule your first appointment.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.82', '{"device_type": "mobile", "completion_time": 26}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('50a5aa7a-3fda-4daf-a289-486f0e1b61fe', 'e71033bc-1f33-4d44-b8c9-7e49bc186303', 'yelp', 'referral', 'deep_clean_specialists', 'residential cleaning', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('f6d02b67-6fa6-4ac7-93c4-f1557b851ac6', 'e71033bc-1f33-4d44-b8c9-7e49bc186303', 'f5555555-5555-5555-5555-555555555555', 1, 'Carlos Rodriguez', '{"name": "Carlos Rodriguez"}', 10, '2025-08-17T09:19:32.007161'),
('385e41e7-12d3-4cb4-bb48-6d3654ab1505', 'e71033bc-1f33-4d44-b8c9-7e49bc186303', 'f5555555-5555-5555-5555-555555555555', 2, 'carlos.rodriguez@tech.com', '{"email": "carlos.rodriguez@tech.com"}', 10, '2025-08-17T09:19:32.007161'),
('ccded8d2-5943-468a-a886-f8ecaf94680c', 'e71033bc-1f33-4d44-b8c9-7e49bc186303', 'f5555555-5555-5555-5555-555555555555', 3, '(857) 555-3691', '{"phone": "(857) 555-3691"}', 15, '2025-08-17T09:19:32.007161'),
('79919e18-7ece-4ead-bffe-6ac1c5e34bf9', 'e71033bc-1f33-4d44-b8c9-7e49bc186303', 'f5555555-5555-5555-5555-555555555555', 4, 'deep_cleaning', '{"service_type": "deep_cleaning"}', 10, '2025-08-17T09:19:32.007161'),
('0d0c35c3-8fba-4f8e-a9a9-4139d395f1a2', 'e71033bc-1f33-4d44-b8c9-7e49bc186303', 'f5555555-5555-5555-5555-555555555555', 5, 'medium_2_3_bed', '{"home_size": "medium_2_3_bed"}', 15, '2025-08-17T09:19:32.007161'),
('dd4f1afc-b70c-4361-99ce-88ee413535ae', 'e71033bc-1f33-4d44-b8c9-7e49bc186303', 'f5555555-5555-5555-5555-555555555555', 6, 'one_time', '{"frequency": "one_time"}', 10, '2025-08-17T09:19:32.007161'),
('359b6d23-a309-46ee-b5b9-90f5979997d4', 'e71033bc-1f33-4d44-b8c9-7e49bc186303', 'f5555555-5555-5555-5555-555555555555', 7, 'eco_friendly', '{"special_requirements": "eco_friendly"}', 10, '2025-08-17T09:19:32.007161'),
('ca030a3f-a353-4207-9e9a-16469d8fd150', 'e71033bc-1f33-4d44-b8c9-7e49bc186303', 'f5555555-5555-5555-5555-555555555555', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-17T09:19:32.007161'),
('614c6e7e-8a4d-4628-b5d4-27b1011a0934', 'e71033bc-1f33-4d44-b8c9-7e49bc186303', 'f5555555-5555-5555-5555-555555555555', 9, 'somerville', '{"location": "somerville"}', 10, '2025-08-17T09:19:32.007161');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('95161bd8-5e80-43a5-8a27-24381a923319', 'e71033bc-1f33-4d44-b8c9-7e49bc186303', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'qualified', '{"name": "Carlos Rodriguez", "email": "carlos.rodriguez@tech.com", "phone": "(857) 555-3691"}', 82, 0.82, true, false, NULL, NULL, NULL);


-- Lead 3: Maybe - Betty Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('d67e7a0b-948f-4416-8fc1-0ca49738fe32', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_003_maybe', 'a5555555-5555-5555-5555-555555555555', '2025-08-16T07:19:32.007227', '2025-08-16T07:45:32.007229', '2025-08-16T07:45:32.007229', 7, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to provide the best cleaning solution. We will be in touch soon.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.171', '{"device_type": "desktop", "completion_time": 56}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('0be067cf-8f5b-41ac-9e4e-9b8c76601e6b', 'd67e7a0b-948f-4416-8fc1-0ca49738fe32', 'facebook', 'social', 'apartment_cleaning', 'home cleaning boston', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('c101a8b1-ceb3-4b92-9848-ed62e6025582', 'd67e7a0b-948f-4416-8fc1-0ca49738fe32', 'f5555555-5555-5555-5555-555555555555', 1, 'Betty Johnson', '{"name": "Betty Johnson"}', 10, '2025-08-16T07:19:32.007227'),
('f65865e0-0035-4c73-914d-92fd43ed36a2', 'd67e7a0b-948f-4416-8fc1-0ca49738fe32', 'f5555555-5555-5555-5555-555555555555', 2, 'betty.johnson@email.com', '{"email": "betty.johnson@email.com"}', 10, '2025-08-16T07:19:32.007227'),
('a08689a5-94d8-4b15-ba29-3f61349c0b3d', 'd67e7a0b-948f-4416-8fc1-0ca49738fe32', 'f5555555-5555-5555-5555-555555555555', 3, '(617) 555-4702', '{"phone": "(617) 555-4702"}', 15, '2025-08-16T07:19:32.007227'),
('a3544a7d-7fb1-45b2-84c9-b4187fbbbf1d', 'd67e7a0b-948f-4416-8fc1-0ca49738fe32', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-16T07:19:32.007227'),
('bcf32e66-1050-4a93-b5b5-3c3d874f8d35', 'd67e7a0b-948f-4416-8fc1-0ca49738fe32', 'f5555555-5555-5555-5555-555555555555', 5, 'small_1_bed', '{"home_size": "small_1_bed"}', 10, '2025-08-16T07:19:32.007227'),
('0c5de6ad-9fe9-4aa5-a310-62d6f6f68f25', 'd67e7a0b-948f-4416-8fc1-0ca49738fe32', 'f5555555-5555-5555-5555-555555555555', 6, 'bi_weekly', '{"frequency": "bi_weekly"}', 20, '2025-08-16T07:19:32.007227'),
('567e8482-ee57-4ec6-bdef-91e721129889', 'd67e7a0b-948f-4416-8fc1-0ca49738fe32', 'f5555555-5555-5555-5555-555555555555', 7, 'none', '{"special_requirements": "none"}', 10, '2025-08-16T07:19:32.007227'),
('d444f786-d8d3-457d-825f-cf75d5ebaced', 'd67e7a0b-948f-4416-8fc1-0ca49738fe32', 'f5555555-5555-5555-5555-555555555555', 8, '$75_100', '{"budget": "$75_100"}', 15, '2025-08-16T07:19:32.007227'),
('7ef31bb1-96f8-4d82-bbeb-ec155217ef52', 'd67e7a0b-948f-4416-8fc1-0ca49738fe32', 'f5555555-5555-5555-5555-555555555555', 9, 'boston', '{"location": "boston"}', 10, '2025-08-16T07:19:32.007227');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('ff9b9a22-3b1d-440e-be8e-c8dc99254792', 'd67e7a0b-948f-4416-8fc1-0ca49738fe32', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'maybe', '{"name": "Betty Johnson", "email": "betty.johnson@email.com", "phone": "(617) 555-4702"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 4: Unqualified - Gary Wilson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('760c4f58-3635-4358-ada5-4a61a972a0c6', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_004_unqualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-23T00:19:32.007479', '2025-08-23T00:39:32.007483', '2025-08-23T00:39:32.007483', 7, true, 30, 30, 'no', 'qualified', 'Thank you for considering Sparkle Clean. While we may not be able to accommodate your specific needs, feel free to reach out in the future.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.131', '{"device_type": "mobile", "completion_time": 60}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('f99ac21d-18f6-4bc6-9491-f5cdbce27549', '760c4f58-3635-4358-ada5-4a61a972a0c6', 'organic', 'search', 'budget_cleaning', 'residential cleaning', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('bd4d933a-968e-4ad9-b4e4-74f4044dad26', '760c4f58-3635-4358-ada5-4a61a972a0c6', 'f5555555-5555-5555-5555-555555555555', 1, 'Gary Wilson', '{"name": "Gary Wilson"}', 10, '2025-08-23T00:19:32.007479'),
('4795632b-f074-41ec-9893-3f16d36d1b88', '760c4f58-3635-4358-ada5-4a61a972a0c6', 'f5555555-5555-5555-5555-555555555555', 2, 'gary.wilson@startup.co', '{"email": "gary.wilson@startup.co"}', 10, '2025-08-23T00:19:32.007479'),
('41028910-871f-4ba8-8c70-c1884af53412', '760c4f58-3635-4358-ada5-4a61a972a0c6', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-23T00:19:32.007479'),
('01de8ced-92ff-4bd8-827e-1b7d62b1d710', '760c4f58-3635-4358-ada5-4a61a972a0c6', 'f5555555-5555-5555-5555-555555555555', 5, 'small_1_bed', '{"home_size": "small_1_bed"}', 10, '2025-08-23T00:19:32.007479'),
('c35d292d-70f0-4533-8dd8-7fdbe80f035f', '760c4f58-3635-4358-ada5-4a61a972a0c6', 'f5555555-5555-5555-5555-555555555555', 6, 'monthly', '{"frequency": "monthly"}', 15, '2025-08-23T00:19:32.007479'),
('6b904da2-f59c-4df0-b37d-efb5e5f4cc8a', '760c4f58-3635-4358-ada5-4a61a972a0c6', 'f5555555-5555-5555-5555-555555555555', 7, 'none', '{"special_requirements": "none"}', 10, '2025-08-23T00:19:32.007479'),
('13c53580-2dad-42f9-b0f9-204f30fa7513', '760c4f58-3635-4358-ada5-4a61a972a0c6', 'f5555555-5555-5555-5555-555555555555', 8, 'under_75', '{"budget": "under_75"}', 5, '2025-08-23T00:19:32.007479'),
('27a052ea-c4a6-4779-8f2a-3d70095a743a', '760c4f58-3635-4358-ada5-4a61a972a0c6', 'f5555555-5555-5555-5555-555555555555', 9, 'other', '{"location": "other"}', 10, '2025-08-23T00:19:32.007479');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('61d526fd-ce7d-4e69-a278-158407aa6621', '760c4f58-3635-4358-ada5-4a61a972a0c6', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'unqualified', '{"name": "Gary Wilson", "email": "gary.wilson@startup.co"}', 30, 0.30, false, false, NULL, NULL, NULL);


-- Lead 5: Maybe - Maria Santos
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('226cfea8-cb6e-4abe-9424-a0d18a14ba58', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_005_maybe', 'a5555555-5555-5555-5555-555555555555', '2025-08-11T00:19:32.007549', '2025-08-11T00:37:32.007550', '2025-08-11T00:37:32.007550', 8, true, 70, 70, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to provide the best cleaning solution. We will be in touch soon.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.47', '{"device_type": "desktop", "completion_time": 58}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('be439556-0005-4fdd-8598-58323f7024a3', '226cfea8-cb6e-4abe-9424-a0d18a14ba58', 'referral', 'referral', 'move_cleaning', 'home cleaning boston', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('afb51ca9-547d-41de-9116-f7622c3f9bfe', '226cfea8-cb6e-4abe-9424-a0d18a14ba58', 'f5555555-5555-5555-5555-555555555555', 1, 'Maria Santos', '{"name": "Maria Santos"}', 10, '2025-08-11T00:19:32.007549'),
('09bc4c1c-32e8-46ab-b619-38a7792d5529', '226cfea8-cb6e-4abe-9424-a0d18a14ba58', 'f5555555-5555-5555-5555-555555555555', 2, 'maria.santos@hospital.org', '{"email": "maria.santos@hospital.org"}', 10, '2025-08-11T00:19:32.007549'),
('d1d58db0-d0c6-4116-97aa-986626e0d7f8', '226cfea8-cb6e-4abe-9424-a0d18a14ba58', 'f5555555-5555-5555-5555-555555555555', 3, '(781) 555-5813', '{"phone": "(781) 555-5813"}', 15, '2025-08-11T00:19:32.007549'),
('cc1dcfc3-ca5a-45a4-9a41-225062aea230', '226cfea8-cb6e-4abe-9424-a0d18a14ba58', 'f5555555-5555-5555-5555-555555555555', 4, 'move_in_out', '{"service_type": "move_in_out"}', 10, '2025-08-11T00:19:32.007549'),
('643a1565-f4f8-4502-85fc-a2c0df33db35', '226cfea8-cb6e-4abe-9424-a0d18a14ba58', 'f5555555-5555-5555-5555-555555555555', 5, 'medium_2_3_bed', '{"home_size": "medium_2_3_bed"}', 15, '2025-08-11T00:19:32.007549'),
('c01f27bc-04f3-43af-b640-064c3dbd63e5', '226cfea8-cb6e-4abe-9424-a0d18a14ba58', 'f5555555-5555-5555-5555-555555555555', 6, 'one_time', '{"frequency": "one_time"}', 10, '2025-08-11T00:19:32.007549'),
('bef4bc13-e4d8-4e99-9505-7a1b40872055', '226cfea8-cb6e-4abe-9424-a0d18a14ba58', 'f5555555-5555-5555-5555-555555555555', 7, 'eco_friendly', '{"special_requirements": "eco_friendly"}', 10, '2025-08-11T00:19:32.007549'),
('7a1e058c-27ec-4040-bb68-529f7a31d461', '226cfea8-cb6e-4abe-9424-a0d18a14ba58', 'f5555555-5555-5555-5555-555555555555', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-11T00:19:32.007549'),
('0254af9d-7c0c-4e41-b883-07afcdee12e4', '226cfea8-cb6e-4abe-9424-a0d18a14ba58', 'f5555555-5555-5555-5555-555555555555', 9, 'brookline', '{"location": "brookline"}', 10, '2025-08-11T00:19:32.007549');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('027156a2-a3be-41cd-af10-6af03373268f', '226cfea8-cb6e-4abe-9424-a0d18a14ba58', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'maybe', '{"name": "Maria Santos", "email": "maria.santos@hospital.org", "phone": "(781) 555-5813"}', 70, 0.70, true, false, NULL, NULL, NULL);


-- Lead 6: Qualified - Helen_2 Smith
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('e51105b4-8b7f-435e-9de8-ae1622a1f33b', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_006_qualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-12T16:19:32.007613', '2025-08-12T16:34:32.007615', '2025-08-12T16:34:32.007615', 8, true, 90, 90, 'yes', 'qualified', 'Perfect! Your cleaning needs match our services perfectly. We will contact you within 24 hours to schedule your first appointment.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.19', '{"device_type": "desktop", "completion_time": 11}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('17b4274a-f659-46b8-ac3b-fb64d15b9ae8', 'e51105b4-8b7f-435e-9de8-ae1622a1f33b', 'google', 'cpc', 'luxury_home_cleaning', 'professional cleaners', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('73bec0fe-a021-4f63-879e-9d21a315dd6d', 'e51105b4-8b7f-435e-9de8-ae1622a1f33b', 'f5555555-5555-5555-5555-555555555555', 1, 'Helen_2 Smith', '{"name": "Helen_2 Smith"}', 10, '2025-08-12T16:19:32.007613'),
('dee95257-d294-446e-b9a6-f24e6b7f7e35', 'e51105b4-8b7f-435e-9de8-ae1622a1f33b', 'f5555555-5555-5555-5555-555555555555', 2, 'helen.smith_2@lawfirm.com', '{"email": "helen.smith_2@lawfirm.com"}', 10, '2025-08-12T16:19:32.007613'),
('711452b4-21cf-4d02-9cf3-3d089848d1ee', 'e51105b4-8b7f-435e-9de8-ae1622a1f33b', 'f5555555-5555-5555-5555-555555555555', 3, '(617) 555-2580', '{"phone": "(617) 555-2580"}', 15, '2025-08-12T16:19:32.007613'),
('0b443de3-8e36-44fa-b081-53be39fe6430', 'e51105b4-8b7f-435e-9de8-ae1622a1f33b', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-12T16:19:32.007613'),
('bae9513b-9c1a-43c2-a5b8-4d0e0ed8c0c5', 'e51105b4-8b7f-435e-9de8-ae1622a1f33b', 'f5555555-5555-5555-5555-555555555555', 5, 'large_4plus_bed', '{"home_size": "large_4plus_bed"}', 20, '2025-08-12T16:19:32.007613'),
('7e0eeac3-71cb-4031-8e17-9bb008a8ad21', 'e51105b4-8b7f-435e-9de8-ae1622a1f33b', 'f5555555-5555-5555-5555-555555555555', 6, 'weekly', '{"frequency": "weekly"}', 25, '2025-08-12T16:19:32.007613'),
('b256cb0e-7faf-421d-bb4c-a3054200e1c5', 'e51105b4-8b7f-435e-9de8-ae1622a1f33b', 'f5555555-5555-5555-5555-555555555555', 7, 'pet_friendly', '{"special_requirements": "pet_friendly"}', 10, '2025-08-12T16:19:32.007613'),
('7165ebc0-cea4-4779-b466-51f9358067ae', 'e51105b4-8b7f-435e-9de8-ae1622a1f33b', 'f5555555-5555-5555-5555-555555555555', 8, '$150_plus', '{"budget": "$150_plus"}', 25, '2025-08-12T16:19:32.007613'),
('3584bf17-5654-4797-8e2f-3d3d89af1653', 'e51105b4-8b7f-435e-9de8-ae1622a1f33b', 'f5555555-5555-5555-5555-555555555555', 9, 'cambridge', '{"location": "cambridge"}', 10, '2025-08-12T16:19:32.007613');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('f9b739d0-f2ae-411d-9664-54ed691b296c', 'e51105b4-8b7f-435e-9de8-ae1622a1f33b', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'qualified', '{"name": "Helen_2 Smith", "email": "helen.smith_2@lawfirm.com", "phone": "(617) 555-2580"}', 90, 0.90, true, false, NULL, NULL, NULL);


-- Lead 7: Qualified - Carlos_2 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('3c0f00c6-b671-43ab-9bab-afa7cbce6a55', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_007_qualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-14T21:19:32.007676', '2025-08-14T22:03:32.007677', '2025-08-14T22:03:32.007677', 8, true, 82, 82, 'yes', 'qualified', 'Perfect! Your cleaning needs match our services perfectly. We will contact you within 24 hours to schedule your first appointment.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.194', '{"device_type": "mobile", "completion_time": 19}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('a6637280-0dc5-4fbd-8c9f-932d7140be28', '3c0f00c6-b671-43ab-9bab-afa7cbce6a55', 'yelp', 'referral', 'deep_clean_specialists', 'house cleaning service', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('fd3068b6-22b0-4ff6-b3b4-c317fc9182e2', '3c0f00c6-b671-43ab-9bab-afa7cbce6a55', 'f5555555-5555-5555-5555-555555555555', 1, 'Carlos_2 Rodriguez', '{"name": "Carlos_2 Rodriguez"}', 10, '2025-08-14T21:19:32.007676'),
('95a9445b-6968-4346-98e8-f6a5a263a4fb', '3c0f00c6-b671-43ab-9bab-afa7cbce6a55', 'f5555555-5555-5555-5555-555555555555', 2, 'carlos.rodriguez_2@tech.com', '{"email": "carlos.rodriguez_2@tech.com"}', 10, '2025-08-14T21:19:32.007676'),
('0712c1c8-0d42-48cf-8fea-d8cc80f77225', '3c0f00c6-b671-43ab-9bab-afa7cbce6a55', 'f5555555-5555-5555-5555-555555555555', 3, '(857) 555-3691', '{"phone": "(857) 555-3691"}', 15, '2025-08-14T21:19:32.007676'),
('ed5530bc-b0c5-4a93-bac7-65818bebe48b', '3c0f00c6-b671-43ab-9bab-afa7cbce6a55', 'f5555555-5555-5555-5555-555555555555', 4, 'deep_cleaning', '{"service_type": "deep_cleaning"}', 10, '2025-08-14T21:19:32.007676'),
('a175d380-0b7e-473d-b29d-fdb4871cf67e', '3c0f00c6-b671-43ab-9bab-afa7cbce6a55', 'f5555555-5555-5555-5555-555555555555', 5, 'medium_2_3_bed', '{"home_size": "medium_2_3_bed"}', 15, '2025-08-14T21:19:32.007676'),
('df70df56-79b4-44ec-bad6-9d0961e16428', '3c0f00c6-b671-43ab-9bab-afa7cbce6a55', 'f5555555-5555-5555-5555-555555555555', 6, 'one_time', '{"frequency": "one_time"}', 10, '2025-08-14T21:19:32.007676'),
('13a06d25-ee39-490d-99a1-19de80e1a7b1', '3c0f00c6-b671-43ab-9bab-afa7cbce6a55', 'f5555555-5555-5555-5555-555555555555', 7, 'eco_friendly', '{"special_requirements": "eco_friendly"}', 10, '2025-08-14T21:19:32.007676'),
('e4f1c8d9-6f87-47b6-a264-77c4f64bb837', '3c0f00c6-b671-43ab-9bab-afa7cbce6a55', 'f5555555-5555-5555-5555-555555555555', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-14T21:19:32.007676'),
('e5d2bc56-2973-4c72-95b5-18dabbbc288d', '3c0f00c6-b671-43ab-9bab-afa7cbce6a55', 'f5555555-5555-5555-5555-555555555555', 9, 'somerville', '{"location": "somerville"}', 10, '2025-08-14T21:19:32.007676');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('12279528-d84d-4594-86ca-ad911102a3c5', '3c0f00c6-b671-43ab-9bab-afa7cbce6a55', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'qualified', '{"name": "Carlos_2 Rodriguez", "email": "carlos.rodriguez_2@tech.com", "phone": "(857) 555-3691"}', 82, 0.82, true, false, NULL, NULL, NULL);


-- Lead 8: Maybe - Betty_2 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('24efe055-1872-4361-b30a-383716436c23', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_008_maybe', 'a5555555-5555-5555-5555-555555555555', '2025-08-17T09:19:32.007735', '2025-08-17T10:03:32.007736', '2025-08-17T10:03:32.007736', 7, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to provide the best cleaning solution. We will be in touch soon.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.203', '{"device_type": "desktop", "completion_time": 48}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('ddcb445e-dd6f-479c-b959-30a87b0eeca1', '24efe055-1872-4361-b30a-383716436c23', 'facebook', 'social', 'apartment_cleaning', 'professional cleaners', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('b90ed1ee-5309-4e73-b66c-35b3176bffe3', '24efe055-1872-4361-b30a-383716436c23', 'f5555555-5555-5555-5555-555555555555', 1, 'Betty_2 Johnson', '{"name": "Betty_2 Johnson"}', 10, '2025-08-17T09:19:32.007735'),
('1e71a7b0-0ccc-4b3f-923f-cdb0c30b3534', '24efe055-1872-4361-b30a-383716436c23', 'f5555555-5555-5555-5555-555555555555', 2, 'betty.johnson_2@email.com', '{"email": "betty.johnson_2@email.com"}', 10, '2025-08-17T09:19:32.007735'),
('ce7552d4-6a9f-4d57-9079-c5f204272a9d', '24efe055-1872-4361-b30a-383716436c23', 'f5555555-5555-5555-5555-555555555555', 3, '(617) 555-4702', '{"phone": "(617) 555-4702"}', 15, '2025-08-17T09:19:32.007735'),
('265983d8-4392-4a8e-aed6-050aacc9daa7', '24efe055-1872-4361-b30a-383716436c23', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-17T09:19:32.007735'),
('70c1108a-f749-406b-b28a-d1ebb553eee0', '24efe055-1872-4361-b30a-383716436c23', 'f5555555-5555-5555-5555-555555555555', 5, 'small_1_bed', '{"home_size": "small_1_bed"}', 10, '2025-08-17T09:19:32.007735'),
('bbdf72bc-f831-4b98-9da0-b07c8f4edca3', '24efe055-1872-4361-b30a-383716436c23', 'f5555555-5555-5555-5555-555555555555', 6, 'bi_weekly', '{"frequency": "bi_weekly"}', 20, '2025-08-17T09:19:32.007735'),
('f513ebeb-582d-46b9-aa68-80ea652bbf66', '24efe055-1872-4361-b30a-383716436c23', 'f5555555-5555-5555-5555-555555555555', 7, 'none', '{"special_requirements": "none"}', 10, '2025-08-17T09:19:32.007735'),
('fc19a59b-6325-4577-9253-4241c1786694', '24efe055-1872-4361-b30a-383716436c23', 'f5555555-5555-5555-5555-555555555555', 8, '$75_100', '{"budget": "$75_100"}', 15, '2025-08-17T09:19:32.007735'),
('68e48b65-5472-4f2a-8c20-af3fcc08f2fb', '24efe055-1872-4361-b30a-383716436c23', 'f5555555-5555-5555-5555-555555555555', 9, 'boston', '{"location": "boston"}', 10, '2025-08-17T09:19:32.007735');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('13ae1c4d-5598-421e-afb0-e639ee45dda6', '24efe055-1872-4361-b30a-383716436c23', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'maybe', '{"name": "Betty_2 Johnson", "email": "betty.johnson_2@email.com", "phone": "(617) 555-4702"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 9: Unqualified - Gary_2 Wilson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('25c43343-5149-4d22-9257-58601a85ac89', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_009_unqualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-24T14:19:32.007790', '2025-08-24T14:41:32.007791', '2025-08-24T14:41:32.007791', 8, true, 30, 30, 'no', 'qualified', 'Thank you for considering Sparkle Clean. While we may not be able to accommodate your specific needs, feel free to reach out in the future.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.147', '{"device_type": "mobile", "completion_time": 57}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('e67ab020-a248-4206-a3f0-9b3d7dfb1821', '25c43343-5149-4d22-9257-58601a85ac89', 'organic', 'search', 'budget_cleaning', 'cleaning service cambridge', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('b2106dc3-ac18-4292-8e0a-fe3fd184fe4c', '25c43343-5149-4d22-9257-58601a85ac89', 'f5555555-5555-5555-5555-555555555555', 1, 'Gary_2 Wilson', '{"name": "Gary_2 Wilson"}', 10, '2025-08-24T14:19:32.007790'),
('da8832c2-f0e9-409f-b59e-aa91fb63324b', '25c43343-5149-4d22-9257-58601a85ac89', 'f5555555-5555-5555-5555-555555555555', 2, 'gary.wilson_2@startup.co', '{"email": "gary.wilson_2@startup.co"}', 10, '2025-08-24T14:19:32.007790'),
('158d9668-f562-4b6f-a1d8-23d36a87fd2e', '25c43343-5149-4d22-9257-58601a85ac89', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-24T14:19:32.007790'),
('8052d4b3-1942-4be3-b105-2a91d9e808be', '25c43343-5149-4d22-9257-58601a85ac89', 'f5555555-5555-5555-5555-555555555555', 5, 'small_1_bed', '{"home_size": "small_1_bed"}', 10, '2025-08-24T14:19:32.007790'),
('94316b42-5cd8-4215-a3e4-7bbc7d0ef48c', '25c43343-5149-4d22-9257-58601a85ac89', 'f5555555-5555-5555-5555-555555555555', 6, 'monthly', '{"frequency": "monthly"}', 15, '2025-08-24T14:19:32.007790'),
('73d8d1e4-1347-4768-ad00-e23ef708311a', '25c43343-5149-4d22-9257-58601a85ac89', 'f5555555-5555-5555-5555-555555555555', 7, 'none', '{"special_requirements": "none"}', 10, '2025-08-24T14:19:32.007790'),
('d074283b-b999-496b-835d-853ac14748b4', '25c43343-5149-4d22-9257-58601a85ac89', 'f5555555-5555-5555-5555-555555555555', 8, 'under_75', '{"budget": "under_75"}', 5, '2025-08-24T14:19:32.007790'),
('e1b621bd-8606-43f8-83fe-d2c226fbda09', '25c43343-5149-4d22-9257-58601a85ac89', 'f5555555-5555-5555-5555-555555555555', 9, 'other', '{"location": "other"}', 10, '2025-08-24T14:19:32.007790');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('2e903ea1-44c8-4b53-98bb-244be4ff63e1', '25c43343-5149-4d22-9257-58601a85ac89', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'unqualified', '{"name": "Gary_2 Wilson", "email": "gary.wilson_2@startup.co"}', 30, 0.30, false, false, NULL, NULL, NULL);


-- Lead 10: Maybe - Maria_2 Santos
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('dc67ab49-92d0-42e0-b2d4-db97ff9da39c', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_010_maybe', 'a5555555-5555-5555-5555-555555555555', '2025-08-18T04:19:32.007839', '2025-08-18T04:47:32.007840', '2025-08-18T04:47:32.007840', 7, true, 70, 70, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to provide the best cleaning solution. We will be in touch soon.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.97', '{"device_type": "desktop", "completion_time": 58}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('2e6db527-7a61-4f57-bf80-ae00658e2b9a', 'dc67ab49-92d0-42e0-b2d4-db97ff9da39c', 'referral', 'referral', 'move_cleaning', 'cleaning service cambridge', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('cc71cc3d-196b-48d2-b92d-2844ba98cc80', 'dc67ab49-92d0-42e0-b2d4-db97ff9da39c', 'f5555555-5555-5555-5555-555555555555', 1, 'Maria_2 Santos', '{"name": "Maria_2 Santos"}', 10, '2025-08-18T04:19:32.007839'),
('62260b58-b5a9-41f5-b7a0-1c53341dd076', 'dc67ab49-92d0-42e0-b2d4-db97ff9da39c', 'f5555555-5555-5555-5555-555555555555', 2, 'maria.santos_2@hospital.org', '{"email": "maria.santos_2@hospital.org"}', 10, '2025-08-18T04:19:32.007839'),
('1d6016c2-f1dd-46c0-b33b-dc5544fdff78', 'dc67ab49-92d0-42e0-b2d4-db97ff9da39c', 'f5555555-5555-5555-5555-555555555555', 3, '(781) 555-5813', '{"phone": "(781) 555-5813"}', 15, '2025-08-18T04:19:32.007839'),
('3c6c28f6-f7db-4921-a6e5-ece5b98b42cb', 'dc67ab49-92d0-42e0-b2d4-db97ff9da39c', 'f5555555-5555-5555-5555-555555555555', 4, 'move_in_out', '{"service_type": "move_in_out"}', 10, '2025-08-18T04:19:32.007839'),
('9217ec57-cc7d-4cb8-a757-315fcee80a27', 'dc67ab49-92d0-42e0-b2d4-db97ff9da39c', 'f5555555-5555-5555-5555-555555555555', 5, 'medium_2_3_bed', '{"home_size": "medium_2_3_bed"}', 15, '2025-08-18T04:19:32.007839'),
('7c61c62f-7713-4498-8b56-5b1ba5140412', 'dc67ab49-92d0-42e0-b2d4-db97ff9da39c', 'f5555555-5555-5555-5555-555555555555', 6, 'one_time', '{"frequency": "one_time"}', 10, '2025-08-18T04:19:32.007839'),
('7ea138be-08fc-484b-838b-f76bdf5ee8ea', 'dc67ab49-92d0-42e0-b2d4-db97ff9da39c', 'f5555555-5555-5555-5555-555555555555', 7, 'eco_friendly', '{"special_requirements": "eco_friendly"}', 10, '2025-08-18T04:19:32.007839'),
('565356f2-b22c-4873-a393-3743308349f9', 'dc67ab49-92d0-42e0-b2d4-db97ff9da39c', 'f5555555-5555-5555-5555-555555555555', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-18T04:19:32.007839'),
('5f5e6cd5-617e-48f9-88a5-ba4355e32a1a', 'dc67ab49-92d0-42e0-b2d4-db97ff9da39c', 'f5555555-5555-5555-5555-555555555555', 9, 'brookline', '{"location": "brookline"}', 10, '2025-08-18T04:19:32.007839');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('65c6a25e-1cdd-464a-a33b-6fca7ccaa345', 'dc67ab49-92d0-42e0-b2d4-db97ff9da39c', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'maybe', '{"name": "Maria_2 Santos", "email": "maria.santos_2@hospital.org", "phone": "(781) 555-5813"}', 70, 0.70, true, false, NULL, NULL, NULL);


-- Lead 11: Qualified - Helen_3 Smith
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('f430eca3-f5aa-43e4-835f-4a9794bc50be', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_011_qualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-22T03:19:32.007888', '2025-08-22T03:56:32.007889', '2025-08-22T03:56:32.007889', 9, true, 90, 90, 'yes', 'qualified', 'Perfect! Your cleaning needs match our services perfectly. We will contact you within 24 hours to schedule your first appointment.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.144', '{"device_type": "desktop", "completion_time": 40}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('78524550-ca7a-4d8e-9667-03d9a18f9813', 'f430eca3-f5aa-43e4-835f-4a9794bc50be', 'google', 'cpc', 'luxury_home_cleaning', 'house cleaning service', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('0ae22423-6be9-45dd-966c-d0413d2a6484', 'f430eca3-f5aa-43e4-835f-4a9794bc50be', 'f5555555-5555-5555-5555-555555555555', 1, 'Helen_3 Smith', '{"name": "Helen_3 Smith"}', 10, '2025-08-22T03:19:32.007888'),
('2dddf34c-f612-4884-bd36-71c6cdc12dc8', 'f430eca3-f5aa-43e4-835f-4a9794bc50be', 'f5555555-5555-5555-5555-555555555555', 2, 'helen.smith_3@lawfirm.com', '{"email": "helen.smith_3@lawfirm.com"}', 10, '2025-08-22T03:19:32.007888'),
('90948e61-dc04-4a59-b84e-e68de9fe6bc9', 'f430eca3-f5aa-43e4-835f-4a9794bc50be', 'f5555555-5555-5555-5555-555555555555', 3, '(617) 555-2580', '{"phone": "(617) 555-2580"}', 15, '2025-08-22T03:19:32.007888'),
('882dc955-ee42-495c-977e-91e4f71f8ed8', 'f430eca3-f5aa-43e4-835f-4a9794bc50be', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-22T03:19:32.007888'),
('8495e627-8f73-4fe1-966e-2c3785b4403c', 'f430eca3-f5aa-43e4-835f-4a9794bc50be', 'f5555555-5555-5555-5555-555555555555', 5, 'large_4plus_bed', '{"home_size": "large_4plus_bed"}', 20, '2025-08-22T03:19:32.007888'),
('1f83f2bd-9dab-40d9-9e41-e179845f3ee7', 'f430eca3-f5aa-43e4-835f-4a9794bc50be', 'f5555555-5555-5555-5555-555555555555', 6, 'weekly', '{"frequency": "weekly"}', 25, '2025-08-22T03:19:32.007888'),
('8bf3e30e-2d71-4542-9d7b-b2840a7349ae', 'f430eca3-f5aa-43e4-835f-4a9794bc50be', 'f5555555-5555-5555-5555-555555555555', 7, 'pet_friendly', '{"special_requirements": "pet_friendly"}', 10, '2025-08-22T03:19:32.007888'),
('5de29923-7763-4f60-87d1-f37461ef3e05', 'f430eca3-f5aa-43e4-835f-4a9794bc50be', 'f5555555-5555-5555-5555-555555555555', 8, '$150_plus', '{"budget": "$150_plus"}', 25, '2025-08-22T03:19:32.007888'),
('7b7045bc-65dc-43f1-b716-fa7d9fe9e094', 'f430eca3-f5aa-43e4-835f-4a9794bc50be', 'f5555555-5555-5555-5555-555555555555', 9, 'cambridge', '{"location": "cambridge"}', 10, '2025-08-22T03:19:32.007888');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('f6fe670b-1811-48a8-9bf1-822147ad927e', 'f430eca3-f5aa-43e4-835f-4a9794bc50be', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'qualified', '{"name": "Helen_3 Smith", "email": "helen.smith_3@lawfirm.com", "phone": "(617) 555-2580"}', 90, 0.90, true, false, NULL, NULL, NULL);


-- Lead 12: Qualified - Carlos_3 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('ef7004b7-15f0-4135-9113-69e45513d4a9', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_012_qualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-21T09:19:32.007940', '2025-08-21T09:38:32.007941', '2025-08-21T09:38:32.007941', 8, true, 82, 82, 'yes', 'qualified', 'Perfect! Your cleaning needs match our services perfectly. We will contact you within 24 hours to schedule your first appointment.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.89', '{"device_type": "mobile", "completion_time": 29}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('d8a7aa4d-7b58-4530-9a18-64da1459b65b', 'ef7004b7-15f0-4135-9113-69e45513d4a9', 'yelp', 'referral', 'deep_clean_specialists', 'cleaning service cambridge', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('5bb420f8-b726-4076-bcf3-98e7d4f8041f', 'ef7004b7-15f0-4135-9113-69e45513d4a9', 'f5555555-5555-5555-5555-555555555555', 1, 'Carlos_3 Rodriguez', '{"name": "Carlos_3 Rodriguez"}', 10, '2025-08-21T09:19:32.007940'),
('f15fa5fc-615b-4d5e-8a21-c244b841cfb1', 'ef7004b7-15f0-4135-9113-69e45513d4a9', 'f5555555-5555-5555-5555-555555555555', 2, 'carlos.rodriguez_3@tech.com', '{"email": "carlos.rodriguez_3@tech.com"}', 10, '2025-08-21T09:19:32.007940'),
('c95d043d-e433-4796-a6e0-6f168eca08e5', 'ef7004b7-15f0-4135-9113-69e45513d4a9', 'f5555555-5555-5555-5555-555555555555', 3, '(857) 555-3691', '{"phone": "(857) 555-3691"}', 15, '2025-08-21T09:19:32.007940'),
('d2e07814-401d-48bc-9af4-23f130935dda', 'ef7004b7-15f0-4135-9113-69e45513d4a9', 'f5555555-5555-5555-5555-555555555555', 4, 'deep_cleaning', '{"service_type": "deep_cleaning"}', 10, '2025-08-21T09:19:32.007940'),
('edb13152-5beb-441b-ab6f-8482ba04d060', 'ef7004b7-15f0-4135-9113-69e45513d4a9', 'f5555555-5555-5555-5555-555555555555', 5, 'medium_2_3_bed', '{"home_size": "medium_2_3_bed"}', 15, '2025-08-21T09:19:32.007940'),
('b763c09d-eec1-44bb-901c-0655b8f41828', 'ef7004b7-15f0-4135-9113-69e45513d4a9', 'f5555555-5555-5555-5555-555555555555', 6, 'one_time', '{"frequency": "one_time"}', 10, '2025-08-21T09:19:32.007940'),
('6a817f4f-919a-4ab4-872f-8f37d331c128', 'ef7004b7-15f0-4135-9113-69e45513d4a9', 'f5555555-5555-5555-5555-555555555555', 7, 'eco_friendly', '{"special_requirements": "eco_friendly"}', 10, '2025-08-21T09:19:32.007940'),
('94267786-cc90-43eb-afbd-28d5f8ecc959', 'ef7004b7-15f0-4135-9113-69e45513d4a9', 'f5555555-5555-5555-5555-555555555555', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-21T09:19:32.007940'),
('d65c2977-33a6-47be-ae0d-2dd0370690b1', 'ef7004b7-15f0-4135-9113-69e45513d4a9', 'f5555555-5555-5555-5555-555555555555', 9, 'somerville', '{"location": "somerville"}', 10, '2025-08-21T09:19:32.007940');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('bd84e290-55e9-419b-a993-bdc69fdb1576', 'ef7004b7-15f0-4135-9113-69e45513d4a9', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'qualified', '{"name": "Carlos_3 Rodriguez", "email": "carlos.rodriguez_3@tech.com", "phone": "(857) 555-3691"}', 82, 0.82, true, false, NULL, NULL, NULL);


-- Lead 13: Maybe - Betty_3 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('f93a5b77-6972-4e46-8414-f289a3a6837e', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_013_maybe', 'a5555555-5555-5555-5555-555555555555', '2025-08-18T10:19:32.007990', '2025-08-18T10:43:32.007991', '2025-08-18T10:43:32.007991', 7, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to provide the best cleaning solution. We will be in touch soon.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.182', '{"device_type": "desktop", "completion_time": 48}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('b872a60b-d834-43d8-880f-95629942c08a', 'f93a5b77-6972-4e46-8414-f289a3a6837e', 'facebook', 'social', 'apartment_cleaning', 'residential cleaning', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('7fba2ed4-cbe7-4d5b-975d-0728526d3b25', 'f93a5b77-6972-4e46-8414-f289a3a6837e', 'f5555555-5555-5555-5555-555555555555', 1, 'Betty_3 Johnson', '{"name": "Betty_3 Johnson"}', 10, '2025-08-18T10:19:32.007990'),
('7caea744-ad23-45bd-881e-1e04b2ab9467', 'f93a5b77-6972-4e46-8414-f289a3a6837e', 'f5555555-5555-5555-5555-555555555555', 2, 'betty.johnson_3@email.com', '{"email": "betty.johnson_3@email.com"}', 10, '2025-08-18T10:19:32.007990'),
('7ed80122-e116-44f5-9268-b557756055c8', 'f93a5b77-6972-4e46-8414-f289a3a6837e', 'f5555555-5555-5555-5555-555555555555', 3, '(617) 555-4702', '{"phone": "(617) 555-4702"}', 15, '2025-08-18T10:19:32.007990'),
('088b349f-3d65-4726-8720-8e085a8954d6', 'f93a5b77-6972-4e46-8414-f289a3a6837e', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-18T10:19:32.007990'),
('6aa16a83-d57b-4c61-8134-3564f088b449', 'f93a5b77-6972-4e46-8414-f289a3a6837e', 'f5555555-5555-5555-5555-555555555555', 5, 'small_1_bed', '{"home_size": "small_1_bed"}', 10, '2025-08-18T10:19:32.007990'),
('5265ab23-5ba1-4b82-a781-32602ac30667', 'f93a5b77-6972-4e46-8414-f289a3a6837e', 'f5555555-5555-5555-5555-555555555555', 6, 'bi_weekly', '{"frequency": "bi_weekly"}', 20, '2025-08-18T10:19:32.007990'),
('24560394-661d-4377-84f0-b0a16ddedd40', 'f93a5b77-6972-4e46-8414-f289a3a6837e', 'f5555555-5555-5555-5555-555555555555', 7, 'none', '{"special_requirements": "none"}', 10, '2025-08-18T10:19:32.007990'),
('0fab0b72-96bf-4254-b8cd-7174e3b1b7b9', 'f93a5b77-6972-4e46-8414-f289a3a6837e', 'f5555555-5555-5555-5555-555555555555', 8, '$75_100', '{"budget": "$75_100"}', 15, '2025-08-18T10:19:32.007990'),
('9e8433f0-0fd2-492d-a482-0c8369f76d01', 'f93a5b77-6972-4e46-8414-f289a3a6837e', 'f5555555-5555-5555-5555-555555555555', 9, 'boston', '{"location": "boston"}', 10, '2025-08-18T10:19:32.007990');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('b87c4e0b-6110-44d1-86ae-eff01532deb2', 'f93a5b77-6972-4e46-8414-f289a3a6837e', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'maybe', '{"name": "Betty_3 Johnson", "email": "betty.johnson_3@email.com", "phone": "(617) 555-4702"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 14: Unqualified - Gary_3 Wilson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('bc96c434-1389-4a14-812b-c736ecaa2d4c', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_014_unqualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-20T06:19:32.008038', '2025-08-20T06:42:32.008039', '2025-08-20T06:42:32.008039', 6, true, 30, 30, 'no', 'qualified', 'Thank you for considering Sparkle Clean. While we may not be able to accommodate your specific needs, feel free to reach out in the future.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.50', '{"device_type": "mobile", "completion_time": 19}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('a455c2a4-4e0a-43c2-a3c0-648129af6248', 'bc96c434-1389-4a14-812b-c736ecaa2d4c', 'organic', 'search', 'budget_cleaning', 'home cleaning boston', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('1566a7f2-5007-4c7e-9c1c-8eab4c135f98', 'bc96c434-1389-4a14-812b-c736ecaa2d4c', 'f5555555-5555-5555-5555-555555555555', 1, 'Gary_3 Wilson', '{"name": "Gary_3 Wilson"}', 10, '2025-08-20T06:19:32.008038'),
('1a3c2c44-d799-4fe1-811d-8a95a78e7a0d', 'bc96c434-1389-4a14-812b-c736ecaa2d4c', 'f5555555-5555-5555-5555-555555555555', 2, 'gary.wilson_3@startup.co', '{"email": "gary.wilson_3@startup.co"}', 10, '2025-08-20T06:19:32.008038'),
('dafbc169-fc3d-47be-aa28-59fd66b7240c', 'bc96c434-1389-4a14-812b-c736ecaa2d4c', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-20T06:19:32.008038'),
('1fbd2193-73cd-4b73-87ec-724dba289f6c', 'bc96c434-1389-4a14-812b-c736ecaa2d4c', 'f5555555-5555-5555-5555-555555555555', 5, 'small_1_bed', '{"home_size": "small_1_bed"}', 10, '2025-08-20T06:19:32.008038'),
('93560753-d3aa-4f50-909c-ee44adf85746', 'bc96c434-1389-4a14-812b-c736ecaa2d4c', 'f5555555-5555-5555-5555-555555555555', 6, 'monthly', '{"frequency": "monthly"}', 15, '2025-08-20T06:19:32.008038'),
('ec8ce6af-fd12-4fe6-9878-ddb01f0db7db', 'bc96c434-1389-4a14-812b-c736ecaa2d4c', 'f5555555-5555-5555-5555-555555555555', 7, 'none', '{"special_requirements": "none"}', 10, '2025-08-20T06:19:32.008038'),
('54028933-9715-4eda-98d0-29ddcfc5b7c3', 'bc96c434-1389-4a14-812b-c736ecaa2d4c', 'f5555555-5555-5555-5555-555555555555', 8, 'under_75', '{"budget": "under_75"}', 5, '2025-08-20T06:19:32.008038'),
('2babce69-766b-48f5-8d6c-7898eb42e4c4', 'bc96c434-1389-4a14-812b-c736ecaa2d4c', 'f5555555-5555-5555-5555-555555555555', 9, 'other', '{"location": "other"}', 10, '2025-08-20T06:19:32.008038');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('4bff4cdb-d702-40ce-8061-e59204ba3f8b', 'bc96c434-1389-4a14-812b-c736ecaa2d4c', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'unqualified', '{"name": "Gary_3 Wilson", "email": "gary.wilson_3@startup.co"}', 30, 0.30, false, false, NULL, NULL, NULL);


-- Lead 15: Maybe - Maria_3 Santos
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('c413e56a-9ec5-47cf-9e8f-6affcf86ed1c', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_015_maybe', 'a5555555-5555-5555-5555-555555555555', '2025-08-12T10:19:32.008084', '2025-08-12T10:34:32.008084', '2025-08-12T10:34:32.008084', 8, true, 70, 70, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to provide the best cleaning solution. We will be in touch soon.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.152', '{"device_type": "desktop", "completion_time": 57}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('31edbe0d-78e5-4bb3-ae19-87008da8aa96', 'c413e56a-9ec5-47cf-9e8f-6affcf86ed1c', 'referral', 'referral', 'move_cleaning', 'house cleaning service', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('2e15825e-321b-4124-9ea3-42ed7d15bf67', 'c413e56a-9ec5-47cf-9e8f-6affcf86ed1c', 'f5555555-5555-5555-5555-555555555555', 1, 'Maria_3 Santos', '{"name": "Maria_3 Santos"}', 10, '2025-08-12T10:19:32.008084'),
('9a1b146a-e349-4171-bed7-8bfab5f35de5', 'c413e56a-9ec5-47cf-9e8f-6affcf86ed1c', 'f5555555-5555-5555-5555-555555555555', 2, 'maria.santos_3@hospital.org', '{"email": "maria.santos_3@hospital.org"}', 10, '2025-08-12T10:19:32.008084'),
('1b7b1c78-c7b5-44ee-8a0c-6960059222c9', 'c413e56a-9ec5-47cf-9e8f-6affcf86ed1c', 'f5555555-5555-5555-5555-555555555555', 3, '(781) 555-5813', '{"phone": "(781) 555-5813"}', 15, '2025-08-12T10:19:32.008084'),
('2bdc5804-3af6-4616-af78-42aa2da4fc32', 'c413e56a-9ec5-47cf-9e8f-6affcf86ed1c', 'f5555555-5555-5555-5555-555555555555', 4, 'move_in_out', '{"service_type": "move_in_out"}', 10, '2025-08-12T10:19:32.008084'),
('7ca6173f-7800-4a2b-835a-0c1c876aa857', 'c413e56a-9ec5-47cf-9e8f-6affcf86ed1c', 'f5555555-5555-5555-5555-555555555555', 5, 'medium_2_3_bed', '{"home_size": "medium_2_3_bed"}', 15, '2025-08-12T10:19:32.008084'),
('732d5cfb-9be8-44f0-852f-d22eb4101c38', 'c413e56a-9ec5-47cf-9e8f-6affcf86ed1c', 'f5555555-5555-5555-5555-555555555555', 6, 'one_time', '{"frequency": "one_time"}', 10, '2025-08-12T10:19:32.008084'),
('17068967-c249-43d6-a527-027be473cf96', 'c413e56a-9ec5-47cf-9e8f-6affcf86ed1c', 'f5555555-5555-5555-5555-555555555555', 7, 'eco_friendly', '{"special_requirements": "eco_friendly"}', 10, '2025-08-12T10:19:32.008084'),
('dd5bbf99-930a-493d-b93b-47da7e8e8fe9', 'c413e56a-9ec5-47cf-9e8f-6affcf86ed1c', 'f5555555-5555-5555-5555-555555555555', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-12T10:19:32.008084'),
('559f18d1-5fb1-4baa-8407-2af50e4510ff', 'c413e56a-9ec5-47cf-9e8f-6affcf86ed1c', 'f5555555-5555-5555-5555-555555555555', 9, 'brookline', '{"location": "brookline"}', 10, '2025-08-12T10:19:32.008084');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('7ba49771-1fd3-4349-8509-45c76be98877', 'c413e56a-9ec5-47cf-9e8f-6affcf86ed1c', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'maybe', '{"name": "Maria_3 Santos", "email": "maria.santos_3@hospital.org", "phone": "(781) 555-5813"}', 70, 0.70, true, false, NULL, NULL, NULL);


-- Lead 16: Qualified - Helen_4 Smith
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('2cdb18aa-d5d8-4ae5-9526-f9f7100e5404', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_016_qualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-19T16:19:32.008132', '2025-08-19T16:43:32.008133', '2025-08-19T16:43:32.008133', 6, true, 90, 90, 'yes', 'qualified', 'Perfect! Your cleaning needs match our services perfectly. We will contact you within 24 hours to schedule your first appointment.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.38', '{"device_type": "desktop", "completion_time": 58}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('843fb1cd-73fb-4547-946d-4b5361b3a0f2', '2cdb18aa-d5d8-4ae5-9526-f9f7100e5404', 'google', 'cpc', 'luxury_home_cleaning', 'professional cleaners', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('3aa85721-98b4-4223-b7e8-579ce845ef9d', '2cdb18aa-d5d8-4ae5-9526-f9f7100e5404', 'f5555555-5555-5555-5555-555555555555', 1, 'Helen_4 Smith', '{"name": "Helen_4 Smith"}', 10, '2025-08-19T16:19:32.008132'),
('4215e48e-fa29-49f6-830b-d16869ab596b', '2cdb18aa-d5d8-4ae5-9526-f9f7100e5404', 'f5555555-5555-5555-5555-555555555555', 2, 'helen.smith_4@lawfirm.com', '{"email": "helen.smith_4@lawfirm.com"}', 10, '2025-08-19T16:19:32.008132'),
('92cc8d01-9291-49b6-a02e-f2a99962c5d6', '2cdb18aa-d5d8-4ae5-9526-f9f7100e5404', 'f5555555-5555-5555-5555-555555555555', 3, '(617) 555-2580', '{"phone": "(617) 555-2580"}', 15, '2025-08-19T16:19:32.008132'),
('5cb71afc-344e-41a9-9a1e-ab0716623ca1', '2cdb18aa-d5d8-4ae5-9526-f9f7100e5404', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-19T16:19:32.008132'),
('3b31ebb2-5f2d-46bc-85ef-cf522443e339', '2cdb18aa-d5d8-4ae5-9526-f9f7100e5404', 'f5555555-5555-5555-5555-555555555555', 5, 'large_4plus_bed', '{"home_size": "large_4plus_bed"}', 20, '2025-08-19T16:19:32.008132'),
('b92ff614-75b2-4ae1-b083-29994f02822c', '2cdb18aa-d5d8-4ae5-9526-f9f7100e5404', 'f5555555-5555-5555-5555-555555555555', 6, 'weekly', '{"frequency": "weekly"}', 25, '2025-08-19T16:19:32.008132'),
('eda4bbfa-e0fa-4532-91d0-24ed8a349353', '2cdb18aa-d5d8-4ae5-9526-f9f7100e5404', 'f5555555-5555-5555-5555-555555555555', 7, 'pet_friendly', '{"special_requirements": "pet_friendly"}', 10, '2025-08-19T16:19:32.008132'),
('a90236fc-b97b-4ad8-9dc8-69e384ce7795', '2cdb18aa-d5d8-4ae5-9526-f9f7100e5404', 'f5555555-5555-5555-5555-555555555555', 8, '$150_plus', '{"budget": "$150_plus"}', 25, '2025-08-19T16:19:32.008132'),
('a8fe49bf-b2f7-471e-952a-922fc97bae72', '2cdb18aa-d5d8-4ae5-9526-f9f7100e5404', 'f5555555-5555-5555-5555-555555555555', 9, 'cambridge', '{"location": "cambridge"}', 10, '2025-08-19T16:19:32.008132');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('ff996eee-2bdb-42bb-a3d0-d24f42b42c7b', '2cdb18aa-d5d8-4ae5-9526-f9f7100e5404', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'qualified', '{"name": "Helen_4 Smith", "email": "helen.smith_4@lawfirm.com", "phone": "(617) 555-2580"}', 90, 0.90, true, false, NULL, NULL, NULL);


-- Lead 17: Qualified - Carlos_4 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('3a2c0d02-f6e1-4519-9364-8b3f580bb7db', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_017_qualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-19T22:19:32.008193', '2025-08-19T22:41:32.008194', '2025-08-19T22:41:32.008194', 6, true, 82, 82, 'yes', 'qualified', 'Perfect! Your cleaning needs match our services perfectly. We will contact you within 24 hours to schedule your first appointment.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.76', '{"device_type": "mobile", "completion_time": 59}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('9cedf280-3fe2-4fda-82b0-380eb828b22e', '3a2c0d02-f6e1-4519-9364-8b3f580bb7db', 'yelp', 'referral', 'deep_clean_specialists', 'home cleaning boston', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('9395c3af-77fa-47d7-8f83-1eddb8a89d99', '3a2c0d02-f6e1-4519-9364-8b3f580bb7db', 'f5555555-5555-5555-5555-555555555555', 1, 'Carlos_4 Rodriguez', '{"name": "Carlos_4 Rodriguez"}', 10, '2025-08-19T22:19:32.008193'),
('697e5530-2f77-44ef-b64b-9fca110aa720', '3a2c0d02-f6e1-4519-9364-8b3f580bb7db', 'f5555555-5555-5555-5555-555555555555', 2, 'carlos.rodriguez_4@tech.com', '{"email": "carlos.rodriguez_4@tech.com"}', 10, '2025-08-19T22:19:32.008193'),
('128cf15f-6be3-431f-87b2-6727122999ce', '3a2c0d02-f6e1-4519-9364-8b3f580bb7db', 'f5555555-5555-5555-5555-555555555555', 3, '(857) 555-3691', '{"phone": "(857) 555-3691"}', 15, '2025-08-19T22:19:32.008193'),
('6049bf81-01d9-482a-b937-9e942a61e87b', '3a2c0d02-f6e1-4519-9364-8b3f580bb7db', 'f5555555-5555-5555-5555-555555555555', 4, 'deep_cleaning', '{"service_type": "deep_cleaning"}', 10, '2025-08-19T22:19:32.008193'),
('0109cb95-4ee2-4e7b-a1a8-920b140dcccf', '3a2c0d02-f6e1-4519-9364-8b3f580bb7db', 'f5555555-5555-5555-5555-555555555555', 5, 'medium_2_3_bed', '{"home_size": "medium_2_3_bed"}', 15, '2025-08-19T22:19:32.008193'),
('39e83d19-16f3-470b-b9e7-5a44dfb2dd44', '3a2c0d02-f6e1-4519-9364-8b3f580bb7db', 'f5555555-5555-5555-5555-555555555555', 6, 'one_time', '{"frequency": "one_time"}', 10, '2025-08-19T22:19:32.008193'),
('12dd7578-984a-4a42-927b-76b5ce5f08b3', '3a2c0d02-f6e1-4519-9364-8b3f580bb7db', 'f5555555-5555-5555-5555-555555555555', 7, 'eco_friendly', '{"special_requirements": "eco_friendly"}', 10, '2025-08-19T22:19:32.008193'),
('e6bbc496-7691-46fe-aa20-f3f3f6d82ac1', '3a2c0d02-f6e1-4519-9364-8b3f580bb7db', 'f5555555-5555-5555-5555-555555555555', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-19T22:19:32.008193'),
('682d0eb0-02af-4543-9ae6-4ca986614a39', '3a2c0d02-f6e1-4519-9364-8b3f580bb7db', 'f5555555-5555-5555-5555-555555555555', 9, 'somerville', '{"location": "somerville"}', 10, '2025-08-19T22:19:32.008193');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('1e81092d-1590-4b5a-ada1-df58548a8aec', '3a2c0d02-f6e1-4519-9364-8b3f580bb7db', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'qualified', '{"name": "Carlos_4 Rodriguez", "email": "carlos.rodriguez_4@tech.com", "phone": "(857) 555-3691"}', 82, 0.82, true, false, NULL, NULL, NULL);


-- Lead 18: Maybe - Betty_4 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('a1e1728e-a9b2-4dc0-9831-53b9fb59bf3b', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_018_maybe', 'a5555555-5555-5555-5555-555555555555', '2025-08-24T18:19:32.008241', '2025-08-24T18:39:32.008242', '2025-08-24T18:39:32.008242', 7, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to provide the best cleaning solution. We will be in touch soon.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.175', '{"device_type": "desktop", "completion_time": 38}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('25b70629-8f29-4b6d-ad68-aec65c1a8093', 'a1e1728e-a9b2-4dc0-9831-53b9fb59bf3b', 'facebook', 'social', 'apartment_cleaning', 'house cleaning service', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('8ad027a0-6b23-460f-8032-378fa0544057', 'a1e1728e-a9b2-4dc0-9831-53b9fb59bf3b', 'f5555555-5555-5555-5555-555555555555', 1, 'Betty_4 Johnson', '{"name": "Betty_4 Johnson"}', 10, '2025-08-24T18:19:32.008241'),
('f36738e0-3d84-4b4a-843c-4f50875686cb', 'a1e1728e-a9b2-4dc0-9831-53b9fb59bf3b', 'f5555555-5555-5555-5555-555555555555', 2, 'betty.johnson_4@email.com', '{"email": "betty.johnson_4@email.com"}', 10, '2025-08-24T18:19:32.008241'),
('d27c92ef-7074-44c4-8c3c-7ed17b8ccf18', 'a1e1728e-a9b2-4dc0-9831-53b9fb59bf3b', 'f5555555-5555-5555-5555-555555555555', 3, '(617) 555-4702', '{"phone": "(617) 555-4702"}', 15, '2025-08-24T18:19:32.008241'),
('0d78f335-a8ac-42c3-89f4-572f1bed9a76', 'a1e1728e-a9b2-4dc0-9831-53b9fb59bf3b', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-24T18:19:32.008241'),
('5fd4b41c-4d2d-4554-a1b3-7eee68e27e8e', 'a1e1728e-a9b2-4dc0-9831-53b9fb59bf3b', 'f5555555-5555-5555-5555-555555555555', 5, 'small_1_bed', '{"home_size": "small_1_bed"}', 10, '2025-08-24T18:19:32.008241'),
('865dda1d-d3d6-4b68-9cc4-9d6d1f7417b7', 'a1e1728e-a9b2-4dc0-9831-53b9fb59bf3b', 'f5555555-5555-5555-5555-555555555555', 6, 'bi_weekly', '{"frequency": "bi_weekly"}', 20, '2025-08-24T18:19:32.008241'),
('ba57ead3-e661-4675-bd36-92bc254ca5ac', 'a1e1728e-a9b2-4dc0-9831-53b9fb59bf3b', 'f5555555-5555-5555-5555-555555555555', 7, 'none', '{"special_requirements": "none"}', 10, '2025-08-24T18:19:32.008241'),
('5753d2d8-b2d6-4879-b41c-aecb8c3e46e0', 'a1e1728e-a9b2-4dc0-9831-53b9fb59bf3b', 'f5555555-5555-5555-5555-555555555555', 8, '$75_100', '{"budget": "$75_100"}', 15, '2025-08-24T18:19:32.008241'),
('42695951-2eaf-4d07-9686-4f7ef8388c16', 'a1e1728e-a9b2-4dc0-9831-53b9fb59bf3b', 'f5555555-5555-5555-5555-555555555555', 9, 'boston', '{"location": "boston"}', 10, '2025-08-24T18:19:32.008241');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('1039715d-779a-450c-8911-58041309b4c3', 'a1e1728e-a9b2-4dc0-9831-53b9fb59bf3b', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'maybe', '{"name": "Betty_4 Johnson", "email": "betty.johnson_4@email.com", "phone": "(617) 555-4702"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 19: Unqualified - Gary_4 Wilson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('5bf73561-4a8a-45e5-94cf-25ee5e35da4a', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_019_unqualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-10T14:19:32.008289', '2025-08-10T14:56:32.008289', '2025-08-10T14:56:32.008289', 8, true, 30, 30, 'no', 'qualified', 'Thank you for considering Sparkle Clean. While we may not be able to accommodate your specific needs, feel free to reach out in the future.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.194', '{"device_type": "mobile", "completion_time": 50}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('f706fe33-1ab7-4b4e-90fb-9e09c6f298f2', '5bf73561-4a8a-45e5-94cf-25ee5e35da4a', 'organic', 'search', 'budget_cleaning', 'home cleaning boston', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('ac7ff35b-7802-4775-8b54-ccbeb76d1378', '5bf73561-4a8a-45e5-94cf-25ee5e35da4a', 'f5555555-5555-5555-5555-555555555555', 1, 'Gary_4 Wilson', '{"name": "Gary_4 Wilson"}', 10, '2025-08-10T14:19:32.008289'),
('f825621c-76c9-45d2-8fde-2577ab5d96c9', '5bf73561-4a8a-45e5-94cf-25ee5e35da4a', 'f5555555-5555-5555-5555-555555555555', 2, 'gary.wilson_4@startup.co', '{"email": "gary.wilson_4@startup.co"}', 10, '2025-08-10T14:19:32.008289'),
('42b6a2d9-828f-4746-8ee9-8b0c73c80e4b', '5bf73561-4a8a-45e5-94cf-25ee5e35da4a', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-10T14:19:32.008289'),
('fb1a99b4-1617-4287-9621-0cd0f7ad8811', '5bf73561-4a8a-45e5-94cf-25ee5e35da4a', 'f5555555-5555-5555-5555-555555555555', 5, 'small_1_bed', '{"home_size": "small_1_bed"}', 10, '2025-08-10T14:19:32.008289'),
('f0fffc35-a8d8-4bf3-a7a5-527773332742', '5bf73561-4a8a-45e5-94cf-25ee5e35da4a', 'f5555555-5555-5555-5555-555555555555', 6, 'monthly', '{"frequency": "monthly"}', 15, '2025-08-10T14:19:32.008289'),
('f0e8f321-a077-44e7-b909-eeca348bcee4', '5bf73561-4a8a-45e5-94cf-25ee5e35da4a', 'f5555555-5555-5555-5555-555555555555', 7, 'none', '{"special_requirements": "none"}', 10, '2025-08-10T14:19:32.008289'),
('4260834d-2dfc-4e4f-b40f-bdac64696f6f', '5bf73561-4a8a-45e5-94cf-25ee5e35da4a', 'f5555555-5555-5555-5555-555555555555', 8, 'under_75', '{"budget": "under_75"}', 5, '2025-08-10T14:19:32.008289'),
('cbf65486-aa04-41c3-be30-0ee55674fd74', '5bf73561-4a8a-45e5-94cf-25ee5e35da4a', 'f5555555-5555-5555-5555-555555555555', 9, 'other', '{"location": "other"}', 10, '2025-08-10T14:19:32.008289');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('32c448b0-d6fc-40d3-a2f8-6e0c3c0d4a83', '5bf73561-4a8a-45e5-94cf-25ee5e35da4a', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'unqualified', '{"name": "Gary_4 Wilson", "email": "gary.wilson_4@startup.co"}', 30, 0.30, false, false, NULL, NULL, NULL);


-- Lead 20: Maybe - Maria_4 Santos
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('6393e240-eab9-4917-b170-5fe1f6d7770e', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_020_maybe', 'a5555555-5555-5555-5555-555555555555', '2025-08-21T13:19:32.008333', '2025-08-21T13:42:32.008334', '2025-08-21T13:42:32.008334', 6, true, 70, 70, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to provide the best cleaning solution. We will be in touch soon.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.54', '{"device_type": "desktop", "completion_time": 30}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('29e2cf9b-7f36-4854-9052-f7ff7acf9b70', '6393e240-eab9-4917-b170-5fe1f6d7770e', 'referral', 'referral', 'move_cleaning', 'professional cleaners', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('adc91666-af91-442b-a416-4ed9017f02fb', '6393e240-eab9-4917-b170-5fe1f6d7770e', 'f5555555-5555-5555-5555-555555555555', 1, 'Maria_4 Santos', '{"name": "Maria_4 Santos"}', 10, '2025-08-21T13:19:32.008333'),
('be86babf-fe96-4220-abb8-94417d750e99', '6393e240-eab9-4917-b170-5fe1f6d7770e', 'f5555555-5555-5555-5555-555555555555', 2, 'maria.santos_4@hospital.org', '{"email": "maria.santos_4@hospital.org"}', 10, '2025-08-21T13:19:32.008333'),
('bd670d78-436f-4f60-b12b-ac4eb0d093fb', '6393e240-eab9-4917-b170-5fe1f6d7770e', 'f5555555-5555-5555-5555-555555555555', 3, '(781) 555-5813', '{"phone": "(781) 555-5813"}', 15, '2025-08-21T13:19:32.008333'),
('1e1d4473-c410-4999-bb66-4fb1215277b4', '6393e240-eab9-4917-b170-5fe1f6d7770e', 'f5555555-5555-5555-5555-555555555555', 4, 'move_in_out', '{"service_type": "move_in_out"}', 10, '2025-08-21T13:19:32.008333'),
('2c1ea476-b895-4f7a-9a15-74e9af6d3651', '6393e240-eab9-4917-b170-5fe1f6d7770e', 'f5555555-5555-5555-5555-555555555555', 5, 'medium_2_3_bed', '{"home_size": "medium_2_3_bed"}', 15, '2025-08-21T13:19:32.008333'),
('83e81b6a-5a1c-4ed4-bec4-48eb427fddc1', '6393e240-eab9-4917-b170-5fe1f6d7770e', 'f5555555-5555-5555-5555-555555555555', 6, 'one_time', '{"frequency": "one_time"}', 10, '2025-08-21T13:19:32.008333'),
('16e3c195-cbe9-43fb-95c8-11d5f64be1ce', '6393e240-eab9-4917-b170-5fe1f6d7770e', 'f5555555-5555-5555-5555-555555555555', 7, 'eco_friendly', '{"special_requirements": "eco_friendly"}', 10, '2025-08-21T13:19:32.008333'),
('2d1e0228-0760-42ef-912d-b8f5661c8279', '6393e240-eab9-4917-b170-5fe1f6d7770e', 'f5555555-5555-5555-5555-555555555555', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-21T13:19:32.008333'),
('122e0f90-899f-4401-adfc-11c0ced92dda', '6393e240-eab9-4917-b170-5fe1f6d7770e', 'f5555555-5555-5555-5555-555555555555', 9, 'brookline', '{"location": "brookline"}', 10, '2025-08-21T13:19:32.008333');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('b6279254-97eb-4cd8-ab87-8e1a9789c864', '6393e240-eab9-4917-b170-5fe1f6d7770e', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'maybe', '{"name": "Maria_4 Santos", "email": "maria.santos_4@hospital.org", "phone": "(781) 555-5813"}', 70, 0.70, true, false, NULL, NULL, NULL);


-- Lead 21: Qualified - Helen_5 Smith
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('5563d12e-808d-4c7d-b830-d96d02d66340', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_021_qualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-15T06:19:32.008382', '2025-08-15T06:53:32.008383', '2025-08-15T06:53:32.008383', 6, true, 90, 90, 'yes', 'qualified', 'Perfect! Your cleaning needs match our services perfectly. We will contact you within 24 hours to schedule your first appointment.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.113', '{"device_type": "desktop", "completion_time": 58}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('2c89aed6-7670-4277-a98e-231519348bd5', '5563d12e-808d-4c7d-b830-d96d02d66340', 'google', 'cpc', 'luxury_home_cleaning', 'professional cleaners', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('76b64cc8-e55f-4b81-b5e5-abead33dc490', '5563d12e-808d-4c7d-b830-d96d02d66340', 'f5555555-5555-5555-5555-555555555555', 1, 'Helen_5 Smith', '{"name": "Helen_5 Smith"}', 10, '2025-08-15T06:19:32.008382'),
('e8bd720e-d926-424d-8fc5-83d5ab35af81', '5563d12e-808d-4c7d-b830-d96d02d66340', 'f5555555-5555-5555-5555-555555555555', 2, 'helen.smith_5@lawfirm.com', '{"email": "helen.smith_5@lawfirm.com"}', 10, '2025-08-15T06:19:32.008382'),
('4e73ad4c-07f6-4c0c-bd39-5419df56ec44', '5563d12e-808d-4c7d-b830-d96d02d66340', 'f5555555-5555-5555-5555-555555555555', 3, '(617) 555-2580', '{"phone": "(617) 555-2580"}', 15, '2025-08-15T06:19:32.008382'),
('e0bd5da9-b738-48ca-bd1c-00b886f080b4', '5563d12e-808d-4c7d-b830-d96d02d66340', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-15T06:19:32.008382'),
('10eb568d-1b49-4e8c-adfb-42f7ef60f163', '5563d12e-808d-4c7d-b830-d96d02d66340', 'f5555555-5555-5555-5555-555555555555', 5, 'large_4plus_bed', '{"home_size": "large_4plus_bed"}', 20, '2025-08-15T06:19:32.008382'),
('8eb23dc5-0298-488e-af03-e47ec821247f', '5563d12e-808d-4c7d-b830-d96d02d66340', 'f5555555-5555-5555-5555-555555555555', 6, 'weekly', '{"frequency": "weekly"}', 25, '2025-08-15T06:19:32.008382'),
('4fc844ce-e4fb-4f87-bb84-ebe95f8edc5b', '5563d12e-808d-4c7d-b830-d96d02d66340', 'f5555555-5555-5555-5555-555555555555', 7, 'pet_friendly', '{"special_requirements": "pet_friendly"}', 10, '2025-08-15T06:19:32.008382'),
('0f892a50-bb96-4cab-8659-29f25cf67009', '5563d12e-808d-4c7d-b830-d96d02d66340', 'f5555555-5555-5555-5555-555555555555', 8, '$150_plus', '{"budget": "$150_plus"}', 25, '2025-08-15T06:19:32.008382'),
('c8374d80-b5ef-4e6a-9a6e-68f71161862f', '5563d12e-808d-4c7d-b830-d96d02d66340', 'f5555555-5555-5555-5555-555555555555', 9, 'cambridge', '{"location": "cambridge"}', 10, '2025-08-15T06:19:32.008382');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('45cd47b2-6faf-43e3-877a-31e460a3f398', '5563d12e-808d-4c7d-b830-d96d02d66340', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'qualified', '{"name": "Helen_5 Smith", "email": "helen.smith_5@lawfirm.com", "phone": "(617) 555-2580"}', 90, 0.90, true, false, NULL, NULL, NULL);


-- Lead 22: Qualified - Carlos_5 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('866422c6-1efd-4f97-a151-0f30a249bda6', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_022_qualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-18T16:19:32.008434', '2025-08-18T16:41:32.008435', '2025-08-18T16:41:32.008435', 7, true, 82, 82, 'yes', 'qualified', 'Perfect! Your cleaning needs match our services perfectly. We will contact you within 24 hours to schedule your first appointment.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.125', '{"device_type": "mobile", "completion_time": 47}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('06e857eb-aba6-4668-8e05-e8d39a5ca4e6', '866422c6-1efd-4f97-a151-0f30a249bda6', 'yelp', 'referral', 'deep_clean_specialists', 'residential cleaning', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('1f59474c-ed36-414e-a44c-accb15f235de', '866422c6-1efd-4f97-a151-0f30a249bda6', 'f5555555-5555-5555-5555-555555555555', 1, 'Carlos_5 Rodriguez', '{"name": "Carlos_5 Rodriguez"}', 10, '2025-08-18T16:19:32.008434'),
('3efee912-38f7-4def-963b-fd786d988397', '866422c6-1efd-4f97-a151-0f30a249bda6', 'f5555555-5555-5555-5555-555555555555', 2, 'carlos.rodriguez_5@tech.com', '{"email": "carlos.rodriguez_5@tech.com"}', 10, '2025-08-18T16:19:32.008434'),
('e4c99b5e-587f-4e4b-a7d6-3e25b724e59f', '866422c6-1efd-4f97-a151-0f30a249bda6', 'f5555555-5555-5555-5555-555555555555', 3, '(857) 555-3691', '{"phone": "(857) 555-3691"}', 15, '2025-08-18T16:19:32.008434'),
('dff7f3f6-a03c-4f6a-aab6-45e14e36be54', '866422c6-1efd-4f97-a151-0f30a249bda6', 'f5555555-5555-5555-5555-555555555555', 4, 'deep_cleaning', '{"service_type": "deep_cleaning"}', 10, '2025-08-18T16:19:32.008434'),
('93368b9a-dfe5-42ce-941d-a917c614107c', '866422c6-1efd-4f97-a151-0f30a249bda6', 'f5555555-5555-5555-5555-555555555555', 5, 'medium_2_3_bed', '{"home_size": "medium_2_3_bed"}', 15, '2025-08-18T16:19:32.008434'),
('730c62c0-0b05-4746-80b5-7b786252d2f6', '866422c6-1efd-4f97-a151-0f30a249bda6', 'f5555555-5555-5555-5555-555555555555', 6, 'one_time', '{"frequency": "one_time"}', 10, '2025-08-18T16:19:32.008434'),
('8812f2a3-45a1-49f3-b595-82075df0097e', '866422c6-1efd-4f97-a151-0f30a249bda6', 'f5555555-5555-5555-5555-555555555555', 7, 'eco_friendly', '{"special_requirements": "eco_friendly"}', 10, '2025-08-18T16:19:32.008434'),
('a181d2e4-b55c-4a25-8410-9b6a7fafcc54', '866422c6-1efd-4f97-a151-0f30a249bda6', 'f5555555-5555-5555-5555-555555555555', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-18T16:19:32.008434'),
('c775c3b8-1f99-4f96-9a8c-24677556898c', '866422c6-1efd-4f97-a151-0f30a249bda6', 'f5555555-5555-5555-5555-555555555555', 9, 'somerville', '{"location": "somerville"}', 10, '2025-08-18T16:19:32.008434');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('c1a6a5e2-6657-4826-9b7c-961835b3780a', '866422c6-1efd-4f97-a151-0f30a249bda6', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'qualified', '{"name": "Carlos_5 Rodriguez", "email": "carlos.rodriguez_5@tech.com", "phone": "(857) 555-3691"}', 82, 0.82, true, false, NULL, NULL, NULL);


-- Lead 23: Maybe - Betty_5 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('b60cb517-5ad9-4544-9b9a-4b7ca4dfb9a7', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_023_maybe', 'a5555555-5555-5555-5555-555555555555', '2025-08-20T03:19:32.008488', '2025-08-20T04:03:32.008489', '2025-08-20T04:03:32.008489', 8, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to provide the best cleaning solution. We will be in touch soon.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.212', '{"device_type": "desktop", "completion_time": 56}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('66e47662-553a-477f-83ff-67b4852ba45f', 'b60cb517-5ad9-4544-9b9a-4b7ca4dfb9a7', 'facebook', 'social', 'apartment_cleaning', 'cleaning service cambridge', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('02111316-2868-4dc4-88f6-00bd15caf622', 'b60cb517-5ad9-4544-9b9a-4b7ca4dfb9a7', 'f5555555-5555-5555-5555-555555555555', 1, 'Betty_5 Johnson', '{"name": "Betty_5 Johnson"}', 10, '2025-08-20T03:19:32.008488'),
('da3e8d28-7084-4ced-84e7-90d5cf056412', 'b60cb517-5ad9-4544-9b9a-4b7ca4dfb9a7', 'f5555555-5555-5555-5555-555555555555', 2, 'betty.johnson_5@email.com', '{"email": "betty.johnson_5@email.com"}', 10, '2025-08-20T03:19:32.008488'),
('49e3256f-9dae-4e33-94d7-ae9133e60ab5', 'b60cb517-5ad9-4544-9b9a-4b7ca4dfb9a7', 'f5555555-5555-5555-5555-555555555555', 3, '(617) 555-4702', '{"phone": "(617) 555-4702"}', 15, '2025-08-20T03:19:32.008488'),
('ffbef181-ee38-4a4a-aeeb-5183a8b24afe', 'b60cb517-5ad9-4544-9b9a-4b7ca4dfb9a7', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-20T03:19:32.008488'),
('a0df18f8-d6a3-43d3-b4d7-d9f539a9e021', 'b60cb517-5ad9-4544-9b9a-4b7ca4dfb9a7', 'f5555555-5555-5555-5555-555555555555', 5, 'small_1_bed', '{"home_size": "small_1_bed"}', 10, '2025-08-20T03:19:32.008488'),
('cbc1ffd2-4d2f-48e1-930d-f17d810a8a87', 'b60cb517-5ad9-4544-9b9a-4b7ca4dfb9a7', 'f5555555-5555-5555-5555-555555555555', 6, 'bi_weekly', '{"frequency": "bi_weekly"}', 20, '2025-08-20T03:19:32.008488'),
('253470a0-4405-4277-a338-738f765b0c8a', 'b60cb517-5ad9-4544-9b9a-4b7ca4dfb9a7', 'f5555555-5555-5555-5555-555555555555', 7, 'none', '{"special_requirements": "none"}', 10, '2025-08-20T03:19:32.008488'),
('147ea970-faeb-4c34-a933-fe38c537c96b', 'b60cb517-5ad9-4544-9b9a-4b7ca4dfb9a7', 'f5555555-5555-5555-5555-555555555555', 8, '$75_100', '{"budget": "$75_100"}', 15, '2025-08-20T03:19:32.008488'),
('1a598adc-40f9-443d-8420-a1eeca0818ad', 'b60cb517-5ad9-4544-9b9a-4b7ca4dfb9a7', 'f5555555-5555-5555-5555-555555555555', 9, 'boston', '{"location": "boston"}', 10, '2025-08-20T03:19:32.008488');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('5941468d-f617-4649-ac71-ac9f4c03c8e1', 'b60cb517-5ad9-4544-9b9a-4b7ca4dfb9a7', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'maybe', '{"name": "Betty_5 Johnson", "email": "betty.johnson_5@email.com", "phone": "(617) 555-4702"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 24: Unqualified - Gary_5 Wilson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('ab5c9c67-29dd-470e-a966-87aaf062790a', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_024_unqualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-10T17:19:32.008541', '2025-08-10T17:34:32.008542', '2025-08-10T17:34:32.008542', 7, true, 30, 30, 'no', 'qualified', 'Thank you for considering Sparkle Clean. While we may not be able to accommodate your specific needs, feel free to reach out in the future.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.172', '{"device_type": "mobile", "completion_time": 55}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('0a740a7e-0f71-403e-8b85-415c03b6ef48', 'ab5c9c67-29dd-470e-a966-87aaf062790a', 'organic', 'search', 'budget_cleaning', 'residential cleaning', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('6bc8a5b1-0556-47c5-a8b9-2b533edfaad8', 'ab5c9c67-29dd-470e-a966-87aaf062790a', 'f5555555-5555-5555-5555-555555555555', 1, 'Gary_5 Wilson', '{"name": "Gary_5 Wilson"}', 10, '2025-08-10T17:19:32.008541'),
('9661c16a-a7ce-4451-8d9d-b87f67fe92b8', 'ab5c9c67-29dd-470e-a966-87aaf062790a', 'f5555555-5555-5555-5555-555555555555', 2, 'gary.wilson_5@startup.co', '{"email": "gary.wilson_5@startup.co"}', 10, '2025-08-10T17:19:32.008541'),
('623f6828-6838-4885-ba5f-27309cf03db9', 'ab5c9c67-29dd-470e-a966-87aaf062790a', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-10T17:19:32.008541'),
('66d66d2c-31eb-4734-8d28-52bcac9800b4', 'ab5c9c67-29dd-470e-a966-87aaf062790a', 'f5555555-5555-5555-5555-555555555555', 5, 'small_1_bed', '{"home_size": "small_1_bed"}', 10, '2025-08-10T17:19:32.008541'),
('a9f5fa90-b311-4bca-a4d4-4db9ceaffd44', 'ab5c9c67-29dd-470e-a966-87aaf062790a', 'f5555555-5555-5555-5555-555555555555', 6, 'monthly', '{"frequency": "monthly"}', 15, '2025-08-10T17:19:32.008541'),
('05f30a89-86b2-451d-87c5-f0acdc3c9623', 'ab5c9c67-29dd-470e-a966-87aaf062790a', 'f5555555-5555-5555-5555-555555555555', 7, 'none', '{"special_requirements": "none"}', 10, '2025-08-10T17:19:32.008541'),
('a99cd40f-ad64-442c-b547-282686280b98', 'ab5c9c67-29dd-470e-a966-87aaf062790a', 'f5555555-5555-5555-5555-555555555555', 8, 'under_75', '{"budget": "under_75"}', 5, '2025-08-10T17:19:32.008541'),
('8d536e01-2331-41df-b218-ab85351be602', 'ab5c9c67-29dd-470e-a966-87aaf062790a', 'f5555555-5555-5555-5555-555555555555', 9, 'other', '{"location": "other"}', 10, '2025-08-10T17:19:32.008541');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('61f87880-b65a-4942-b9db-89d51f0bdc6f', 'ab5c9c67-29dd-470e-a966-87aaf062790a', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'unqualified', '{"name": "Gary_5 Wilson", "email": "gary.wilson_5@startup.co"}', 30, 0.30, false, false, NULL, NULL, NULL);


-- Lead 25: Maybe - Maria_5 Santos
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('e97643ac-7638-4c16-afa2-f1ce81c2308f', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_025_maybe', 'a5555555-5555-5555-5555-555555555555', '2025-08-12T16:19:32.008591', '2025-08-12T16:53:32.008593', '2025-08-12T16:53:32.008593', 9, true, 70, 70, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to provide the best cleaning solution. We will be in touch soon.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.197', '{"device_type": "desktop", "completion_time": 10}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('5272721b-63b4-4d1a-9216-a13a38412457', 'e97643ac-7638-4c16-afa2-f1ce81c2308f', 'referral', 'referral', 'move_cleaning', 'professional cleaners', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Brookline');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('1e093352-0aa1-4c5c-a623-6e600b42794e', 'e97643ac-7638-4c16-afa2-f1ce81c2308f', 'f5555555-5555-5555-5555-555555555555', 1, 'Maria_5 Santos', '{"name": "Maria_5 Santos"}', 10, '2025-08-12T16:19:32.008591'),
('a5e92ece-47fb-4c00-915d-0e7ea9be5f59', 'e97643ac-7638-4c16-afa2-f1ce81c2308f', 'f5555555-5555-5555-5555-555555555555', 2, 'maria.santos_5@hospital.org', '{"email": "maria.santos_5@hospital.org"}', 10, '2025-08-12T16:19:32.008591'),
('c2723fca-560d-4911-b89c-2294f9bb2009', 'e97643ac-7638-4c16-afa2-f1ce81c2308f', 'f5555555-5555-5555-5555-555555555555', 3, '(781) 555-5813', '{"phone": "(781) 555-5813"}', 15, '2025-08-12T16:19:32.008591'),
('3d0479eb-79f4-4681-b63b-3dcf223ba12f', 'e97643ac-7638-4c16-afa2-f1ce81c2308f', 'f5555555-5555-5555-5555-555555555555', 4, 'move_in_out', '{"service_type": "move_in_out"}', 10, '2025-08-12T16:19:32.008591'),
('33d45f6f-3fe9-4c45-8387-bebe4da0bbf4', 'e97643ac-7638-4c16-afa2-f1ce81c2308f', 'f5555555-5555-5555-5555-555555555555', 5, 'medium_2_3_bed', '{"home_size": "medium_2_3_bed"}', 15, '2025-08-12T16:19:32.008591'),
('848d1f32-4a58-4b75-9fb8-823d07e2acf5', 'e97643ac-7638-4c16-afa2-f1ce81c2308f', 'f5555555-5555-5555-5555-555555555555', 6, 'one_time', '{"frequency": "one_time"}', 10, '2025-08-12T16:19:32.008591'),
('49d35de1-dc93-4a00-be9d-b6f39c58bec5', 'e97643ac-7638-4c16-afa2-f1ce81c2308f', 'f5555555-5555-5555-5555-555555555555', 7, 'eco_friendly', '{"special_requirements": "eco_friendly"}', 10, '2025-08-12T16:19:32.008591'),
('6797ef79-bf10-4f7c-98fa-39465a4b78fd', 'e97643ac-7638-4c16-afa2-f1ce81c2308f', 'f5555555-5555-5555-5555-555555555555', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-12T16:19:32.008591'),
('26fd09f4-d1ac-4c25-8151-432b297447f1', 'e97643ac-7638-4c16-afa2-f1ce81c2308f', 'f5555555-5555-5555-5555-555555555555', 9, 'brookline', '{"location": "brookline"}', 10, '2025-08-12T16:19:32.008591');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('81fca311-ed7a-4e21-a863-1990369a4d0a', 'e97643ac-7638-4c16-afa2-f1ce81c2308f', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'maybe', '{"name": "Maria_5 Santos", "email": "maria.santos_5@hospital.org", "phone": "(781) 555-5813"}', 70, 0.70, true, false, NULL, NULL, NULL);


-- Lead 26: Qualified - Helen_6 Smith
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('52b16aa5-069a-4c38-9caf-78bf83cef9a8', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_026_qualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-12T14:19:32.008644', '2025-08-12T14:52:32.008645', '2025-08-12T14:52:32.008645', 6, true, 90, 90, 'yes', 'qualified', 'Perfect! Your cleaning needs match our services perfectly. We will contact you within 24 hours to schedule your first appointment.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.141', '{"device_type": "desktop", "completion_time": 14}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('d668f6e9-a879-4d57-8f76-4fe5d0175ef2', '52b16aa5-069a-4c38-9caf-78bf83cef9a8', 'google', 'cpc', 'luxury_home_cleaning', 'house cleaning service', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('b510e643-b8a9-4d1c-a952-b65984362c6d', '52b16aa5-069a-4c38-9caf-78bf83cef9a8', 'f5555555-5555-5555-5555-555555555555', 1, 'Helen_6 Smith', '{"name": "Helen_6 Smith"}', 10, '2025-08-12T14:19:32.008644'),
('93df19c2-685e-4660-8ce3-912f3010ac10', '52b16aa5-069a-4c38-9caf-78bf83cef9a8', 'f5555555-5555-5555-5555-555555555555', 2, 'helen.smith_6@lawfirm.com', '{"email": "helen.smith_6@lawfirm.com"}', 10, '2025-08-12T14:19:32.008644'),
('f945b0b7-cee8-413e-9632-a850264d85a9', '52b16aa5-069a-4c38-9caf-78bf83cef9a8', 'f5555555-5555-5555-5555-555555555555', 3, '(617) 555-2580', '{"phone": "(617) 555-2580"}', 15, '2025-08-12T14:19:32.008644'),
('7f7e98fd-2f07-4b1f-a13f-2500281d74bd', '52b16aa5-069a-4c38-9caf-78bf83cef9a8', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-12T14:19:32.008644'),
('5dfb511e-553b-4a71-b476-98201cd06c27', '52b16aa5-069a-4c38-9caf-78bf83cef9a8', 'f5555555-5555-5555-5555-555555555555', 5, 'large_4plus_bed', '{"home_size": "large_4plus_bed"}', 20, '2025-08-12T14:19:32.008644'),
('fd3cd4a7-0ef5-462b-9d95-8c53850ac6a1', '52b16aa5-069a-4c38-9caf-78bf83cef9a8', 'f5555555-5555-5555-5555-555555555555', 6, 'weekly', '{"frequency": "weekly"}', 25, '2025-08-12T14:19:32.008644'),
('2bae8c55-8056-4597-b05f-74a44c862d33', '52b16aa5-069a-4c38-9caf-78bf83cef9a8', 'f5555555-5555-5555-5555-555555555555', 7, 'pet_friendly', '{"special_requirements": "pet_friendly"}', 10, '2025-08-12T14:19:32.008644'),
('b0d51fd5-e2e9-44d8-bddc-304ecfafc75d', '52b16aa5-069a-4c38-9caf-78bf83cef9a8', 'f5555555-5555-5555-5555-555555555555', 8, '$150_plus', '{"budget": "$150_plus"}', 25, '2025-08-12T14:19:32.008644'),
('e4766373-7992-46a1-9496-530cf07e4d91', '52b16aa5-069a-4c38-9caf-78bf83cef9a8', 'f5555555-5555-5555-5555-555555555555', 9, 'cambridge', '{"location": "cambridge"}', 10, '2025-08-12T14:19:32.008644');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('625960a9-b2ec-4821-9b3f-32b61747d7a3', '52b16aa5-069a-4c38-9caf-78bf83cef9a8', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'qualified', '{"name": "Helen_6 Smith", "email": "helen.smith_6@lawfirm.com", "phone": "(617) 555-2580"}', 90, 0.90, true, false, NULL, NULL, NULL);


-- Lead 27: Qualified - Carlos_6 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('49c7b71c-79d7-49a7-b52e-7faa8b875816', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_027_qualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-22T02:19:32.008708', '2025-08-22T02:37:32.008709', '2025-08-22T02:37:32.008709', 9, true, 82, 82, 'yes', 'qualified', 'Perfect! Your cleaning needs match our services perfectly. We will contact you within 24 hours to schedule your first appointment.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.147', '{"device_type": "mobile", "completion_time": 45}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('233f9ff8-49b1-47bd-8e9c-6025d906d72e', '49c7b71c-79d7-49a7-b52e-7faa8b875816', 'yelp', 'referral', 'deep_clean_specialists', 'residential cleaning', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('20c6bee6-5894-45b2-bc4f-1a4c9c1f3868', '49c7b71c-79d7-49a7-b52e-7faa8b875816', 'f5555555-5555-5555-5555-555555555555', 1, 'Carlos_6 Rodriguez', '{"name": "Carlos_6 Rodriguez"}', 10, '2025-08-22T02:19:32.008708'),
('9587d386-1421-419a-8410-232837ea16cd', '49c7b71c-79d7-49a7-b52e-7faa8b875816', 'f5555555-5555-5555-5555-555555555555', 2, 'carlos.rodriguez_6@tech.com', '{"email": "carlos.rodriguez_6@tech.com"}', 10, '2025-08-22T02:19:32.008708'),
('79c5d3e9-eff0-4583-ba8c-263cfec2390b', '49c7b71c-79d7-49a7-b52e-7faa8b875816', 'f5555555-5555-5555-5555-555555555555', 3, '(857) 555-3691', '{"phone": "(857) 555-3691"}', 15, '2025-08-22T02:19:32.008708'),
('9ead3d8d-8b65-4602-b2c6-29505c061805', '49c7b71c-79d7-49a7-b52e-7faa8b875816', 'f5555555-5555-5555-5555-555555555555', 4, 'deep_cleaning', '{"service_type": "deep_cleaning"}', 10, '2025-08-22T02:19:32.008708'),
('4bf440c9-74fe-4af8-aa63-59b8edba1730', '49c7b71c-79d7-49a7-b52e-7faa8b875816', 'f5555555-5555-5555-5555-555555555555', 5, 'medium_2_3_bed', '{"home_size": "medium_2_3_bed"}', 15, '2025-08-22T02:19:32.008708'),
('826c0976-12aa-41fe-99c4-9c0e88bbe492', '49c7b71c-79d7-49a7-b52e-7faa8b875816', 'f5555555-5555-5555-5555-555555555555', 6, 'one_time', '{"frequency": "one_time"}', 10, '2025-08-22T02:19:32.008708'),
('ae721d8e-d6ac-4fdd-b349-43a715bf065d', '49c7b71c-79d7-49a7-b52e-7faa8b875816', 'f5555555-5555-5555-5555-555555555555', 7, 'eco_friendly', '{"special_requirements": "eco_friendly"}', 10, '2025-08-22T02:19:32.008708'),
('74d37fb4-d7bd-4b6a-8863-dc9ddce4ecce', '49c7b71c-79d7-49a7-b52e-7faa8b875816', 'f5555555-5555-5555-5555-555555555555', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-22T02:19:32.008708'),
('5600ea57-6e90-45c8-a066-a2ca491caa57', '49c7b71c-79d7-49a7-b52e-7faa8b875816', 'f5555555-5555-5555-5555-555555555555', 9, 'somerville', '{"location": "somerville"}', 10, '2025-08-22T02:19:32.008708');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('e3ee14e4-1599-4cd6-a7c4-b3ff802f4095', '49c7b71c-79d7-49a7-b52e-7faa8b875816', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'qualified', '{"name": "Carlos_6 Rodriguez", "email": "carlos.rodriguez_6@tech.com", "phone": "(857) 555-3691"}', 82, 0.82, true, false, NULL, NULL, NULL);


-- Lead 28: Maybe - Betty_6 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('fb1ae008-c2a8-4378-b318-ca41d2345ef8', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_028_maybe', 'a5555555-5555-5555-5555-555555555555', '2025-08-12T18:19:32.008765', '2025-08-12T18:37:32.008766', '2025-08-12T18:37:32.008766', 6, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to provide the best cleaning solution. We will be in touch soon.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.73', '{"device_type": "desktop", "completion_time": 22}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('fd8a7959-9ce2-4a46-ba99-56cf79993277', 'fb1ae008-c2a8-4378-b318-ca41d2345ef8', 'facebook', 'social', 'apartment_cleaning', 'home cleaning boston', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('1f284f5c-d956-4317-97c7-940ba5bec1f3', 'fb1ae008-c2a8-4378-b318-ca41d2345ef8', 'f5555555-5555-5555-5555-555555555555', 1, 'Betty_6 Johnson', '{"name": "Betty_6 Johnson"}', 10, '2025-08-12T18:19:32.008765'),
('2cb42e5d-7688-4a1a-b5c5-ff8df0aa272e', 'fb1ae008-c2a8-4378-b318-ca41d2345ef8', 'f5555555-5555-5555-5555-555555555555', 2, 'betty.johnson_6@email.com', '{"email": "betty.johnson_6@email.com"}', 10, '2025-08-12T18:19:32.008765'),
('9fbec81c-3c3a-4e51-a224-91b0cfba68cc', 'fb1ae008-c2a8-4378-b318-ca41d2345ef8', 'f5555555-5555-5555-5555-555555555555', 3, '(617) 555-4702', '{"phone": "(617) 555-4702"}', 15, '2025-08-12T18:19:32.008765'),
('ffe2cac4-8f2c-46d7-847a-7b93183ef097', 'fb1ae008-c2a8-4378-b318-ca41d2345ef8', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-12T18:19:32.008765'),
('4fa84682-3521-46e3-9c49-2718327fbdcb', 'fb1ae008-c2a8-4378-b318-ca41d2345ef8', 'f5555555-5555-5555-5555-555555555555', 5, 'small_1_bed', '{"home_size": "small_1_bed"}', 10, '2025-08-12T18:19:32.008765'),
('2d7590c3-d3d8-43a5-bd62-a6f33f4a00ca', 'fb1ae008-c2a8-4378-b318-ca41d2345ef8', 'f5555555-5555-5555-5555-555555555555', 6, 'bi_weekly', '{"frequency": "bi_weekly"}', 20, '2025-08-12T18:19:32.008765'),
('54f3101c-2571-47ce-ad98-158ebd961465', 'fb1ae008-c2a8-4378-b318-ca41d2345ef8', 'f5555555-5555-5555-5555-555555555555', 7, 'none', '{"special_requirements": "none"}', 10, '2025-08-12T18:19:32.008765'),
('d02ad17c-0c0a-46aa-9531-c4c4188db244', 'fb1ae008-c2a8-4378-b318-ca41d2345ef8', 'f5555555-5555-5555-5555-555555555555', 8, '$75_100', '{"budget": "$75_100"}', 15, '2025-08-12T18:19:32.008765'),
('410ff844-852d-47a2-8aff-7be2f22fcb1f', 'fb1ae008-c2a8-4378-b318-ca41d2345ef8', 'f5555555-5555-5555-5555-555555555555', 9, 'boston', '{"location": "boston"}', 10, '2025-08-12T18:19:32.008765');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('8400038b-c6f3-4e18-8721-eef30f73ec01', 'fb1ae008-c2a8-4378-b318-ca41d2345ef8', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'maybe', '{"name": "Betty_6 Johnson", "email": "betty.johnson_6@email.com", "phone": "(617) 555-4702"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 29: Unqualified - Gary_6 Wilson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('62957999-890d-46e0-a34a-df65420be1de', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_029_unqualified', 'a5555555-5555-5555-5555-555555555555', '2025-08-16T07:19:32.008815', '2025-08-16T08:02:32.008815', '2025-08-16T08:02:32.008815', 9, true, 30, 30, 'no', 'qualified', 'Thank you for considering Sparkle Clean. While we may not be able to accommodate your specific needs, feel free to reach out in the future.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.32', '{"device_type": "mobile", "completion_time": 30}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('cdb7632f-7d8c-42f7-9620-05a7cb5f93db', '62957999-890d-46e0-a34a-df65420be1de', 'organic', 'search', 'budget_cleaning', 'cleaning service cambridge', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('500645ce-f3a7-44f2-b870-b0a27e586728', '62957999-890d-46e0-a34a-df65420be1de', 'f5555555-5555-5555-5555-555555555555', 1, 'Gary_6 Wilson', '{"name": "Gary_6 Wilson"}', 10, '2025-08-16T07:19:32.008815'),
('a7c09dda-d043-49dc-ab6b-de2c5a40bd89', '62957999-890d-46e0-a34a-df65420be1de', 'f5555555-5555-5555-5555-555555555555', 2, 'gary.wilson_6@startup.co', '{"email": "gary.wilson_6@startup.co"}', 10, '2025-08-16T07:19:32.008815'),
('965a977d-24fa-40fa-97b5-d4cdd3c4968c', '62957999-890d-46e0-a34a-df65420be1de', 'f5555555-5555-5555-5555-555555555555', 4, 'regular_cleaning', '{"service_type": "regular_cleaning"}', 10, '2025-08-16T07:19:32.008815'),
('6fe47072-1ee2-406b-841a-d44e2294c9de', '62957999-890d-46e0-a34a-df65420be1de', 'f5555555-5555-5555-5555-555555555555', 5, 'small_1_bed', '{"home_size": "small_1_bed"}', 10, '2025-08-16T07:19:32.008815'),
('bd11cba5-0082-404e-b778-d21eb386ee46', '62957999-890d-46e0-a34a-df65420be1de', 'f5555555-5555-5555-5555-555555555555', 6, 'monthly', '{"frequency": "monthly"}', 15, '2025-08-16T07:19:32.008815'),
('9c175861-df08-49e5-908f-ff494e1ad917', '62957999-890d-46e0-a34a-df65420be1de', 'f5555555-5555-5555-5555-555555555555', 7, 'none', '{"special_requirements": "none"}', 10, '2025-08-16T07:19:32.008815'),
('166a5233-c9b3-45c2-9414-dc41f7c44c0e', '62957999-890d-46e0-a34a-df65420be1de', 'f5555555-5555-5555-5555-555555555555', 8, 'under_75', '{"budget": "under_75"}', 5, '2025-08-16T07:19:32.008815'),
('ee21319d-245d-40c9-a491-b6aa198402c1', '62957999-890d-46e0-a34a-df65420be1de', 'f5555555-5555-5555-5555-555555555555', 9, 'other', '{"location": "other"}', 10, '2025-08-16T07:19:32.008815');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('282dcf05-d745-4a53-b1db-7177f631b8ff', '62957999-890d-46e0-a34a-df65420be1de', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'unqualified', '{"name": "Gary_6 Wilson", "email": "gary.wilson_6@startup.co"}', 30, 0.30, false, false, NULL, NULL, NULL);


-- Lead 30: Maybe - Maria_6 Santos
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('e9794703-7994-4810-b0d9-6d5cf81adccc', 'f5555555-5555-5555-5555-555555555555', 'sparkle_clean_030_maybe', 'a5555555-5555-5555-5555-555555555555', '2025-08-12T17:19:32.008860', '2025-08-12T17:38:32.008861', '2025-08-12T17:38:32.008861', 8, true, 70, 70, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to provide the best cleaning solution. We will be in touch soon.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.179', '{"device_type": "desktop", "completion_time": 41}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('f3879e59-53b2-4a45-8407-a52f4710fd87', 'e9794703-7994-4810-b0d9-6d5cf81adccc', 'referral', 'referral', 'move_cleaning', 'home cleaning boston', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('47aea328-a26f-46ee-b35f-9791e01bd0c3', 'e9794703-7994-4810-b0d9-6d5cf81adccc', 'f5555555-5555-5555-5555-555555555555', 1, 'Maria_6 Santos', '{"name": "Maria_6 Santos"}', 10, '2025-08-12T17:19:32.008860'),
('e3dc7042-becb-44cc-8d58-e82d6827840f', 'e9794703-7994-4810-b0d9-6d5cf81adccc', 'f5555555-5555-5555-5555-555555555555', 2, 'maria.santos_6@hospital.org', '{"email": "maria.santos_6@hospital.org"}', 10, '2025-08-12T17:19:32.008860'),
('459d754c-3e68-4875-8902-3c672e48e85e', 'e9794703-7994-4810-b0d9-6d5cf81adccc', 'f5555555-5555-5555-5555-555555555555', 3, '(781) 555-5813', '{"phone": "(781) 555-5813"}', 15, '2025-08-12T17:19:32.008860'),
('85d11920-03e0-450f-bf85-9a07b1afd64d', 'e9794703-7994-4810-b0d9-6d5cf81adccc', 'f5555555-5555-5555-5555-555555555555', 4, 'move_in_out', '{"service_type": "move_in_out"}', 10, '2025-08-12T17:19:32.008860'),
('82f112f0-acbb-4d77-8dfb-4db1cd304d3a', 'e9794703-7994-4810-b0d9-6d5cf81adccc', 'f5555555-5555-5555-5555-555555555555', 5, 'medium_2_3_bed', '{"home_size": "medium_2_3_bed"}', 15, '2025-08-12T17:19:32.008860'),
('95b799ce-fb62-40bd-8a58-857b7ebc640c', 'e9794703-7994-4810-b0d9-6d5cf81adccc', 'f5555555-5555-5555-5555-555555555555', 6, 'one_time', '{"frequency": "one_time"}', 10, '2025-08-12T17:19:32.008860'),
('ae96971f-56c0-488b-8372-b23bc23e2dc9', 'e9794703-7994-4810-b0d9-6d5cf81adccc', 'f5555555-5555-5555-5555-555555555555', 7, 'eco_friendly', '{"special_requirements": "eco_friendly"}', 10, '2025-08-12T17:19:32.008860'),
('4f4e86cc-084f-4e16-82dd-ac0abc2ee02a', 'e9794703-7994-4810-b0d9-6d5cf81adccc', 'f5555555-5555-5555-5555-555555555555', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-12T17:19:32.008860'),
('5248e8ee-24e7-47de-993a-412d69f471f9', 'e9794703-7994-4810-b0d9-6d5cf81adccc', 'f5555555-5555-5555-5555-555555555555', 9, 'brookline', '{"location": "brookline"}', 10, '2025-08-12T17:19:32.008860');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('66bd636d-4f9b-4c76-8aa5-8316b69e3cab', 'e9794703-7994-4810-b0d9-6d5cf81adccc', 'a5555555-5555-5555-5555-555555555555', 'f5555555-5555-5555-5555-555555555555', 'maybe', '{"name": "Maria_6 Santos", "email": "maria.santos_6@hospital.org", "phone": "(781) 555-5813"}', 70, 0.70, true, false, NULL, NULL, NULL);


SELECT 'Generated 30 realistic lead sessions for sparkle_clean!' as status;

