-- Test Data for FitLife Personal Training (Health & Fitness)
-- Generated 30 realistic lead sessions with complete tracking and outcomes
-- Client: fitlife | Form: f4444444-4444-4444-4444-444444444444 | Generated: 2025-08-24T20:19:27



-- Lead 1: Qualified - Rachel Green
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('7c6f2e5c-22d3-4020-b016-535409ab06d1', 'f4444444-4444-4444-4444-444444444444', 'fitlife_001_qualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-14T08:19:27.398258', '2025-08-14T08:54:27.398266', '2025-08-14T08:54:27.398266', 6, true, 88, 88, 'yes', 'qualified', 'Great news! You are an excellent candidate for our personal training programs. We will contact you within 24 hours to schedule your consultation.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.142', '{"device_type": "mobile", "completion_time": 50}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('f7725886-418e-4022-a1e4-96fc8d366994', '7c6f2e5c-22d3-4020-b016-535409ab06d1', 'instagram', 'social', 'transformation_stories', 'strength training', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('05df0cf5-b0ad-4256-a3ac-7b3b4a098b10', '7c6f2e5c-22d3-4020-b016-535409ab06d1', 'f4444444-4444-4444-4444-444444444444', 1, 'Rachel Green', '{"name": "Rachel Green"}', 10, '2025-08-14T08:19:27.398258'),
('2a988f68-8a38-48c0-a7ee-b7c85b6a436d', '7c6f2e5c-22d3-4020-b016-535409ab06d1', 'f4444444-4444-4444-4444-444444444444', 2, 'rachel.green@consulting.com', '{"email": "rachel.green@consulting.com"}', 10, '2025-08-14T08:19:27.398258'),
('dbff3535-2921-4ba2-9c8c-900cdb32ba98', '7c6f2e5c-22d3-4020-b016-535409ab06d1', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-3691', '{"phone": "(617) 555-3691"}', 15, '2025-08-14T08:19:27.398258'),
('9719557f-67a5-4de4-916e-38c59b137ca5', '7c6f2e5c-22d3-4020-b016-535409ab06d1', 'f4444444-4444-4444-4444-444444444444', 4, 'weight_loss', '{"fitness_goals": "weight_loss"}', 10, '2025-08-14T08:19:27.398258'),
('75a7a55b-d5fe-40f7-b812-023078168144', '7c6f2e5c-22d3-4020-b016-535409ab06d1', 'f4444444-4444-4444-4444-444444444444', 5, 'beginner', '{"experience_level": "beginner"}', 10, '2025-08-14T08:19:27.398258'),
('f72576d7-a046-4ab2-99b0-bd46bd52cee0', '7c6f2e5c-22d3-4020-b016-535409ab06d1', 'f4444444-4444-4444-4444-444444444444', 6, 'mornings', '{"availability": "mornings"}', 10, '2025-08-14T08:19:27.398258'),
('a07103f7-b574-4eb4-8cfe-d4c5c99f7a54', '7c6f2e5c-22d3-4020-b016-535409ab06d1', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-14T08:19:27.398258'),
('ba9dabb7-1932-44b9-b169-8c069c94e017', '7c6f2e5c-22d3-4020-b016-535409ab06d1', 'f4444444-4444-4444-4444-444444444444', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-14T08:19:27.398258'),
('097771d9-a4fe-436c-98fb-64e7cf90f56a', '7c6f2e5c-22d3-4020-b016-535409ab06d1', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-14T08:19:27.398258'),
('15183067-b592-4d8a-b02f-6f1ef1280ab6', '7c6f2e5c-22d3-4020-b016-535409ab06d1', 'f4444444-4444-4444-4444-444444444444', 10, 'asap', '{"timeline": "asap"}', 25, '2025-08-14T08:19:27.398258');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('709ac7af-c299-43b0-bbbb-33e4c39d4adc', '7c6f2e5c-22d3-4020-b016-535409ab06d1', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'qualified', '{"name": "Rachel Green", "email": "rachel.green@consulting.com", "phone": "(617) 555-3691"}', 88, 0.88, true, false, NULL, NULL, NULL);


-- Lead 2: Qualified - Steve Rogers
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('92fb413e-9bb9-4881-b363-7c3c182a168b', 'f4444444-4444-4444-4444-444444444444', 'fitlife_002_qualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-16T23:19:27.398379', '2025-08-16T23:48:27.398381', '2025-08-16T23:48:27.398381', 8, true, 92, 92, 'yes', 'qualified', 'Great news! You are an excellent candidate for our personal training programs. We will contact you within 24 hours to schedule your consultation.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.203', '{"device_type": "desktop", "completion_time": 29}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('f3584e25-2818-406d-b19f-a1d3f6ecb919', '92fb413e-9bb9-4881-b363-7c3c182a168b', 'google', 'cpc', 'strength_training', 'weight loss trainer', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('6a1cba15-758a-4625-b627-f6c43c8db80a', '92fb413e-9bb9-4881-b363-7c3c182a168b', 'f4444444-4444-4444-4444-444444444444', 1, 'Steve Rogers', '{"name": "Steve Rogers"}', 10, '2025-08-16T23:19:27.398379'),
('77c9f05b-75aa-4164-b2f4-bffd4330cae9', '92fb413e-9bb9-4881-b363-7c3c182a168b', 'f4444444-4444-4444-4444-444444444444', 2, 'steve.rogers@military.gov', '{"email": "steve.rogers@military.gov"}', 10, '2025-08-16T23:19:27.398379'),
('e79aa459-f418-4998-b9d3-ce979a7c1fe4', '92fb413e-9bb9-4881-b363-7c3c182a168b', 'f4444444-4444-4444-4444-444444444444', 3, '(857) 555-7410', '{"phone": "(857) 555-7410"}', 15, '2025-08-16T23:19:27.398379'),
('541f8b2f-8742-4c81-8885-f4e014c17054', '92fb413e-9bb9-4881-b363-7c3c182a168b', 'f4444444-4444-4444-4444-444444444444', 4, 'strength_building', '{"fitness_goals": "strength_building"}', 10, '2025-08-16T23:19:27.398379'),
('b0d2e931-0818-44a3-87c6-8b6a84615f27', '92fb413e-9bb9-4881-b363-7c3c182a168b', 'f4444444-4444-4444-4444-444444444444', 5, 'intermediate', '{"experience_level": "intermediate"}', 10, '2025-08-16T23:19:27.398379'),
('b1ed4de6-4161-4fdb-bc93-d653b0702079', '92fb413e-9bb9-4881-b363-7c3c182a168b', 'f4444444-4444-4444-4444-444444444444', 6, 'evenings', '{"availability": "evenings"}', 10, '2025-08-16T23:19:27.398379'),
('c85580a0-8419-42d4-ac40-af3bdaf8659b', '92fb413e-9bb9-4881-b363-7c3c182a168b', 'f4444444-4444-4444-4444-444444444444', 7, 'home', '{"preferred_location": "home"}', 10, '2025-08-16T23:19:27.398379'),
('20c72dff-6338-40fd-8362-b181a471f645', '92fb413e-9bb9-4881-b363-7c3c182a168b', 'f4444444-4444-4444-4444-444444444444', 8, '$150_200', '{"budget": "$150_200"}', 25, '2025-08-16T23:19:27.398379'),
('73afe2bb-a270-4b23-8820-b6d89bb29dc0', '92fb413e-9bb9-4881-b363-7c3c182a168b', 'f4444444-4444-4444-4444-444444444444', 9, 'minor_injury', '{"health_conditions": "minor_injury"}', 10, '2025-08-16T23:19:27.398379'),
('19c169d0-980b-4b5c-bdca-8bdef604c22d', '92fb413e-9bb9-4881-b363-7c3c182a168b', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-16T23:19:27.398379');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('cb0b52fc-2821-41af-adbb-3e7a1d3cb374', '92fb413e-9bb9-4881-b363-7c3c182a168b', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'qualified', '{"name": "Steve Rogers", "email": "steve.rogers@military.gov", "phone": "(857) 555-7410"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 3: Maybe - Monica Bellucci
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('dced8a5d-4266-4d00-bd70-6397e59e3fc2', 'f4444444-4444-4444-4444-444444444444', 'fitlife_003_maybe', 'a4444444-4444-4444-4444-444444444444', '2025-08-15T08:19:27.398449', '2025-08-15T08:34:27.398450', '2025-08-15T08:34:27.398450', 10, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest in FitLife! We are reviewing your fitness goals to create the best training plan. Expect to hear from us soon.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.239', '{"device_type": "mobile", "completion_time": 19}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('ea5595ab-dc2a-4654-9d8f-ff036796ac45', 'dced8a5d-4266-4d00-bd70-6397e59e3fc2', 'facebook', 'social', 'group_fitness', 'personal fitness', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('f1648f4e-e017-4baa-bbb3-02c8c972e9cf', 'dced8a5d-4266-4d00-bd70-6397e59e3fc2', 'f4444444-4444-4444-4444-444444444444', 1, 'Monica Bellucci', '{"name": "Monica Bellucci"}', 10, '2025-08-15T08:19:27.398449'),
('c856a503-94c2-4ec8-8fa3-6911aa724a99', 'dced8a5d-4266-4d00-bd70-6397e59e3fc2', 'f4444444-4444-4444-4444-444444444444', 2, 'monica.bellucci@fashion.com', '{"email": "monica.bellucci@fashion.com"}', 10, '2025-08-15T08:19:27.398449'),
('39c590d1-aba8-429e-8489-bcab9294ad88', 'dced8a5d-4266-4d00-bd70-6397e59e3fc2', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-8520', '{"phone": "(617) 555-8520"}', 15, '2025-08-15T08:19:27.398449'),
('83d4340d-9951-4c11-bee6-94bf78eb914a', 'dced8a5d-4266-4d00-bd70-6397e59e3fc2', 'f4444444-4444-4444-4444-444444444444', 4, 'general_fitness', '{"fitness_goals": "general_fitness"}', 10, '2025-08-15T08:19:27.398449'),
('87a6124b-3699-4c26-95dc-9cee9b735e1f', 'dced8a5d-4266-4d00-bd70-6397e59e3fc2', 'f4444444-4444-4444-4444-444444444444', 5, 'intermediate', '{"experience_level": "intermediate"}', 10, '2025-08-15T08:19:27.398449'),
('440eac2a-e2da-4016-b443-26116f32c713', 'dced8a5d-4266-4d00-bd70-6397e59e3fc2', 'f4444444-4444-4444-4444-444444444444', 6, 'flexible', '{"availability": "flexible"}', 10, '2025-08-15T08:19:27.398449'),
('0d597547-bdec-42b8-8c2e-9b1791b6bdef', 'dced8a5d-4266-4d00-bd70-6397e59e3fc2', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-15T08:19:27.398449'),
('e6c85546-08ac-4a55-9d3f-ccfe80e589a3', 'dced8a5d-4266-4d00-bd70-6397e59e3fc2', 'f4444444-4444-4444-4444-444444444444', 8, '$75_100', '{"budget": "$75_100"}', 15, '2025-08-15T08:19:27.398449'),
('46ef8479-6426-4a27-b8d4-375ac4b0e65c', 'dced8a5d-4266-4d00-bd70-6397e59e3fc2', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-15T08:19:27.398449'),
('de8c9458-86f5-422b-aadc-ff0e684d3494', 'dced8a5d-4266-4d00-bd70-6397e59e3fc2', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-15T08:19:27.398449');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('7ab687bf-ce8f-4aab-a440-6666c3ac3bd9', 'dced8a5d-4266-4d00-bd70-6397e59e3fc2', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'maybe', '{"name": "Monica Bellucci", "email": "monica.bellucci@fashion.com", "phone": "(617) 555-8520"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 4: Unqualified - Peter Parker
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('a03523cd-edb3-4ba0-894e-0d04be063f54', 'f4444444-4444-4444-4444-444444444444', 'fitlife_004_unqualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-23T05:19:27.398513', '2025-08-23T05:36:27.398514', '2025-08-23T05:36:27.398514', 6, true, 35, 35, 'no', 'qualified', 'Thank you for considering FitLife. While our current programs may not be the right fit, we wish you success in your fitness journey.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.244', '{"device_type": "mobile", "completion_time": 14}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('7b431ebe-abda-4981-a9bf-622aaba7bc7a', 'a03523cd-edb3-4ba0-894e-0d04be063f54', 'organic', 'search', 'student_fitness', 'personal trainer boston', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('b5efd6eb-56dd-422a-9a31-b381ed997606', 'a03523cd-edb3-4ba0-894e-0d04be063f54', 'f4444444-4444-4444-4444-444444444444', 1, 'Peter Parker', '{"name": "Peter Parker"}', 10, '2025-08-23T05:19:27.398513'),
('25f13c66-52e4-447f-98f6-d076781da2b8', 'a03523cd-edb3-4ba0-894e-0d04be063f54', 'f4444444-4444-4444-4444-444444444444', 2, 'peter.parker@university.edu', '{"email": "peter.parker@university.edu"}', 10, '2025-08-23T05:19:27.398513'),
('2e7700a2-8ea2-4aba-a84d-fccc013522fc', 'a03523cd-edb3-4ba0-894e-0d04be063f54', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-9630', '{"phone": "(617) 555-9630"}', 15, '2025-08-23T05:19:27.398513'),
('6057c875-6da8-46a1-880a-8f7fe75bd33d', 'a03523cd-edb3-4ba0-894e-0d04be063f54', 'f4444444-4444-4444-4444-444444444444', 4, 'athletic_performance', '{"fitness_goals": "athletic_performance"}', 10, '2025-08-23T05:19:27.398513'),
('4b85f378-1c30-4f60-9bd6-9f8ba5ddf4a5', 'a03523cd-edb3-4ba0-894e-0d04be063f54', 'f4444444-4444-4444-4444-444444444444', 5, 'advanced', '{"experience_level": "advanced"}', 10, '2025-08-23T05:19:27.398513'),
('c71f327b-a049-44b5-95c5-549a4ad75996', 'a03523cd-edb3-4ba0-894e-0d04be063f54', 'f4444444-4444-4444-4444-444444444444', 6, 'afternoons', '{"availability": "afternoons"}', 10, '2025-08-23T05:19:27.398513'),
('a087e341-c525-4fa7-a91c-6ea1fbf2e9e2', 'a03523cd-edb3-4ba0-894e-0d04be063f54', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-23T05:19:27.398513'),
('c9dacb82-98c4-4f67-af00-b30a68ac337c', 'a03523cd-edb3-4ba0-894e-0d04be063f54', 'f4444444-4444-4444-4444-444444444444', 8, 'under_75', '{"budget": "under_75"}', 5, '2025-08-23T05:19:27.398513'),
('c5197faa-47d4-44a1-98c6-7c508b72591e', 'a03523cd-edb3-4ba0-894e-0d04be063f54', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-23T05:19:27.398513'),
('ef4edd4b-eb9e-43d4-a607-7d6d0aa495fb', 'a03523cd-edb3-4ba0-894e-0d04be063f54', 'f4444444-4444-4444-4444-444444444444', 10, 'just_exploring', '{"timeline": "just_exploring"}', 0, '2025-08-23T05:19:27.398513');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('7624c5a9-d45b-4bfd-a564-51bc756af517', 'a03523cd-edb3-4ba0-894e-0d04be063f54', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'unqualified', '{"name": "Peter Parker", "email": "peter.parker@university.edu", "phone": "(617) 555-9630"}', 35, 0.35, false, false, NULL, NULL, NULL);


-- Lead 5: Maybe - Diana Prince
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('64abcad7-6f5f-4089-a323-b6608df93d99', 'f4444444-4444-4444-4444-444444444444', 'fitlife_005_maybe', 'a4444444-4444-4444-4444-444444444444', '2025-08-12T11:19:27.398572', '2025-08-12T11:38:27.398573', '2025-08-12T11:38:27.398573', 9, true, 70, 70, 'maybe', 'qualified', 'Thank you for your interest in FitLife! We are reviewing your fitness goals to create the best training plan. Expect to hear from us soon.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.69', '{"device_type": "desktop", "completion_time": 15}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('e65175ff-d96f-4783-b89b-fc2f02e6a9d2', '64abcad7-6f5f-4089-a323-b6608df93d99', 'referral', 'referral', 'specialized_training', 'personal fitness', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('fbf621c4-eebb-4eb6-a992-a39231134cea', '64abcad7-6f5f-4089-a323-b6608df93d99', 'f4444444-4444-4444-4444-444444444444', 1, 'Diana Prince', '{"name": "Diana Prince"}', 10, '2025-08-12T11:19:27.398572'),
('7544c3a9-773c-4914-b4e8-3eb3f27e7c78', '64abcad7-6f5f-4089-a323-b6608df93d99', 'f4444444-4444-4444-4444-444444444444', 2, 'diana.prince@embassy.gov', '{"email": "diana.prince@embassy.gov"}', 10, '2025-08-12T11:19:27.398572'),
('f38d35f6-4166-4540-97e7-262aba03c3c6', '64abcad7-6f5f-4089-a323-b6608df93d99', 'f4444444-4444-4444-4444-444444444444', 3, '(781) 555-1470', '{"phone": "(781) 555-1470"}', 15, '2025-08-12T11:19:27.398572'),
('aacbfe53-8682-4bee-b28a-9f4a2d0838ed', '64abcad7-6f5f-4089-a323-b6608df93d99', 'f4444444-4444-4444-4444-444444444444', 4, 'martial_arts', '{"fitness_goals": "martial_arts"}', 10, '2025-08-12T11:19:27.398572'),
('e2f29b8e-5d8b-4321-aee6-43b00285ffac', '64abcad7-6f5f-4089-a323-b6608df93d99', 'f4444444-4444-4444-4444-444444444444', 5, 'advanced', '{"experience_level": "advanced"}', 10, '2025-08-12T11:19:27.398572'),
('4bff9ad7-1d8c-4956-8482-90e8c740ceb2', '64abcad7-6f5f-4089-a323-b6608df93d99', 'f4444444-4444-4444-4444-444444444444', 6, 'evenings', '{"availability": "evenings"}', 10, '2025-08-12T11:19:27.398572'),
('74cfcd61-d9d1-486b-860b-528fb353391b', '64abcad7-6f5f-4089-a323-b6608df93d99', 'f4444444-4444-4444-4444-444444444444', 7, 'home', '{"preferred_location": "home"}', 10, '2025-08-12T11:19:27.398572'),
('99292b90-23c3-48d4-af36-d5f399231930', '64abcad7-6f5f-4089-a323-b6608df93d99', 'f4444444-4444-4444-4444-444444444444', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-12T11:19:27.398572'),
('c3d0e520-995a-4854-8c72-bb1c56c6d809', '64abcad7-6f5f-4089-a323-b6608df93d99', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-12T11:19:27.398572'),
('4f0f3ab1-8917-42be-842d-14be35caf452', '64abcad7-6f5f-4089-a323-b6608df93d99', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-12T11:19:27.398572');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('ac224ff2-6425-4f9c-9f51-36c5840122d3', '64abcad7-6f5f-4089-a323-b6608df93d99', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'maybe', '{"name": "Diana Prince", "email": "diana.prince@embassy.gov", "phone": "(781) 555-1470"}', 70, 0.70, true, false, NULL, NULL, NULL);


-- Lead 6: Qualified - Rachel_2 Green
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('d0358580-2c38-4cc2-bdeb-ddb4974025d6', 'f4444444-4444-4444-4444-444444444444', 'fitlife_006_qualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-15T06:19:27.398632', '2025-08-15T06:58:27.398633', '2025-08-15T06:58:27.398633', 8, true, 88, 88, 'yes', 'qualified', 'Great news! You are an excellent candidate for our personal training programs. We will contact you within 24 hours to schedule your consultation.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.183', '{"device_type": "mobile", "completion_time": 32}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('5b82469e-4ab8-4ea8-9637-a5c5adfc3141', 'd0358580-2c38-4cc2-bdeb-ddb4974025d6', 'instagram', 'social', 'transformation_stories', 'personal fitness', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Brookline');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('0d16c044-eaf5-4352-97c7-31a4ab57a4d7', 'd0358580-2c38-4cc2-bdeb-ddb4974025d6', 'f4444444-4444-4444-4444-444444444444', 1, 'Rachel_2 Green', '{"name": "Rachel_2 Green"}', 10, '2025-08-15T06:19:27.398632'),
('ec4077cf-b467-4c72-80b7-5d2397ee1b05', 'd0358580-2c38-4cc2-bdeb-ddb4974025d6', 'f4444444-4444-4444-4444-444444444444', 2, 'rachel.green_2@consulting.com', '{"email": "rachel.green_2@consulting.com"}', 10, '2025-08-15T06:19:27.398632'),
('8c23d798-741d-4606-bd2f-d22abcdee62b', 'd0358580-2c38-4cc2-bdeb-ddb4974025d6', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-3691', '{"phone": "(617) 555-3691"}', 15, '2025-08-15T06:19:27.398632'),
('c2b91972-f42c-420d-ae93-fd441d14ee44', 'd0358580-2c38-4cc2-bdeb-ddb4974025d6', 'f4444444-4444-4444-4444-444444444444', 4, 'weight_loss', '{"fitness_goals": "weight_loss"}', 10, '2025-08-15T06:19:27.398632'),
('6285c4c4-a76d-4eab-9015-219a9b4bddaf', 'd0358580-2c38-4cc2-bdeb-ddb4974025d6', 'f4444444-4444-4444-4444-444444444444', 5, 'beginner', '{"experience_level": "beginner"}', 10, '2025-08-15T06:19:27.398632'),
('fe82d9e7-bf7e-49e2-bd0e-4220ddd79be9', 'd0358580-2c38-4cc2-bdeb-ddb4974025d6', 'f4444444-4444-4444-4444-444444444444', 6, 'mornings', '{"availability": "mornings"}', 10, '2025-08-15T06:19:27.398632'),
('edd0b95f-9861-4ff4-af81-a2a227d97453', 'd0358580-2c38-4cc2-bdeb-ddb4974025d6', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-15T06:19:27.398632'),
('6e7d0a93-8f83-450e-a5d7-8b67306a3d51', 'd0358580-2c38-4cc2-bdeb-ddb4974025d6', 'f4444444-4444-4444-4444-444444444444', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-15T06:19:27.398632'),
('b7e1442b-1c99-4178-ad97-da462e0b0ece', 'd0358580-2c38-4cc2-bdeb-ddb4974025d6', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-15T06:19:27.398632'),
('3f8b616e-7fac-4606-acc9-c5d8fa66fe29', 'd0358580-2c38-4cc2-bdeb-ddb4974025d6', 'f4444444-4444-4444-4444-444444444444', 10, 'asap', '{"timeline": "asap"}', 25, '2025-08-15T06:19:27.398632');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('8cc00e4a-8c97-4e35-959e-4b2345ae822d', 'd0358580-2c38-4cc2-bdeb-ddb4974025d6', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'qualified', '{"name": "Rachel_2 Green", "email": "rachel.green_2@consulting.com", "phone": "(617) 555-3691"}', 88, 0.88, true, false, NULL, NULL, NULL);


-- Lead 7: Qualified - Steve_2 Rogers
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('b18f8c11-4917-4abf-8cb4-312de5950703', 'f4444444-4444-4444-4444-444444444444', 'fitlife_007_qualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-19T14:19:27.398694', '2025-08-19T14:44:27.398694', '2025-08-19T14:44:27.398694', 9, true, 92, 92, 'yes', 'qualified', 'Great news! You are an excellent candidate for our personal training programs. We will contact you within 24 hours to schedule your consultation.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.144', '{"device_type": "desktop", "completion_time": 14}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('a47396fe-9752-453e-8d15-71fdb402702a', 'b18f8c11-4917-4abf-8cb4-312de5950703', 'google', 'cpc', 'strength_training', 'strength training', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Brookline');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('b327816d-4fd5-43ad-9941-006fbd2afc2b', 'b18f8c11-4917-4abf-8cb4-312de5950703', 'f4444444-4444-4444-4444-444444444444', 1, 'Steve_2 Rogers', '{"name": "Steve_2 Rogers"}', 10, '2025-08-19T14:19:27.398694'),
('ff9c86a7-8290-4fc6-bf2a-d2e748b82422', 'b18f8c11-4917-4abf-8cb4-312de5950703', 'f4444444-4444-4444-4444-444444444444', 2, 'steve.rogers_2@military.gov', '{"email": "steve.rogers_2@military.gov"}', 10, '2025-08-19T14:19:27.398694'),
('f0b51dfc-47b4-4707-9dff-5ffa05852811', 'b18f8c11-4917-4abf-8cb4-312de5950703', 'f4444444-4444-4444-4444-444444444444', 3, '(857) 555-7410', '{"phone": "(857) 555-7410"}', 15, '2025-08-19T14:19:27.398694'),
('97bc7e70-7e00-4e54-8da0-fbfd1ccb25b3', 'b18f8c11-4917-4abf-8cb4-312de5950703', 'f4444444-4444-4444-4444-444444444444', 4, 'strength_building', '{"fitness_goals": "strength_building"}', 10, '2025-08-19T14:19:27.398694'),
('bcba9352-52ac-464a-9dae-2e621cdc3811', 'b18f8c11-4917-4abf-8cb4-312de5950703', 'f4444444-4444-4444-4444-444444444444', 5, 'intermediate', '{"experience_level": "intermediate"}', 10, '2025-08-19T14:19:27.398694'),
('80ff1899-2bc1-4c00-b587-714e9e530965', 'b18f8c11-4917-4abf-8cb4-312de5950703', 'f4444444-4444-4444-4444-444444444444', 6, 'evenings', '{"availability": "evenings"}', 10, '2025-08-19T14:19:27.398694'),
('acd7cf78-872c-4604-bb1a-35c8791a98a4', 'b18f8c11-4917-4abf-8cb4-312de5950703', 'f4444444-4444-4444-4444-444444444444', 7, 'home', '{"preferred_location": "home"}', 10, '2025-08-19T14:19:27.398694'),
('0096e494-f368-487c-be0d-89c8b7dce3f6', 'b18f8c11-4917-4abf-8cb4-312de5950703', 'f4444444-4444-4444-4444-444444444444', 8, '$150_200', '{"budget": "$150_200"}', 25, '2025-08-19T14:19:27.398694'),
('f0168117-2913-429d-82c7-99aa34bdabb0', 'b18f8c11-4917-4abf-8cb4-312de5950703', 'f4444444-4444-4444-4444-444444444444', 9, 'minor_injury', '{"health_conditions": "minor_injury"}', 10, '2025-08-19T14:19:27.398694'),
('be1e096f-c68b-4a1d-a852-c077e186cbe3', 'b18f8c11-4917-4abf-8cb4-312de5950703', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-19T14:19:27.398694');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('772edf70-1fb5-4c53-b915-ef0ea805966f', 'b18f8c11-4917-4abf-8cb4-312de5950703', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'qualified', '{"name": "Steve_2 Rogers", "email": "steve.rogers_2@military.gov", "phone": "(857) 555-7410"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 8: Maybe - Monica_2 Bellucci
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('54b88514-926d-42d6-a8a0-0acf8070af4f', 'f4444444-4444-4444-4444-444444444444', 'fitlife_008_maybe', 'a4444444-4444-4444-4444-444444444444', '2025-08-23T15:19:27.398754', '2025-08-23T15:52:27.398755', '2025-08-23T15:52:27.398755', 6, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest in FitLife! We are reviewing your fitness goals to create the best training plan. Expect to hear from us soon.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.167', '{"device_type": "mobile", "completion_time": 43}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('3f950fbc-09a6-402c-b9da-a1a54e31dacb', '54b88514-926d-42d6-a8a0-0acf8070af4f', 'facebook', 'social', 'group_fitness', 'personal fitness', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('cfd84c5c-02f5-4d12-9af7-6591db3315c8', '54b88514-926d-42d6-a8a0-0acf8070af4f', 'f4444444-4444-4444-4444-444444444444', 1, 'Monica_2 Bellucci', '{"name": "Monica_2 Bellucci"}', 10, '2025-08-23T15:19:27.398754'),
('22ee70e7-5ac3-4a10-86a3-469770d9b7e1', '54b88514-926d-42d6-a8a0-0acf8070af4f', 'f4444444-4444-4444-4444-444444444444', 2, 'monica.bellucci_2@fashion.com', '{"email": "monica.bellucci_2@fashion.com"}', 10, '2025-08-23T15:19:27.398754'),
('8906ae92-761f-4b73-91cc-d6eee52cf5b0', '54b88514-926d-42d6-a8a0-0acf8070af4f', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-8520', '{"phone": "(617) 555-8520"}', 15, '2025-08-23T15:19:27.398754'),
('c566f601-3af2-4869-8e1b-f1225ab0666f', '54b88514-926d-42d6-a8a0-0acf8070af4f', 'f4444444-4444-4444-4444-444444444444', 4, 'general_fitness', '{"fitness_goals": "general_fitness"}', 10, '2025-08-23T15:19:27.398754'),
('10d760e4-6439-42ae-904e-ee896fe76155', '54b88514-926d-42d6-a8a0-0acf8070af4f', 'f4444444-4444-4444-4444-444444444444', 5, 'intermediate', '{"experience_level": "intermediate"}', 10, '2025-08-23T15:19:27.398754'),
('5037c0f1-7c2f-4f73-a511-45437109386a', '54b88514-926d-42d6-a8a0-0acf8070af4f', 'f4444444-4444-4444-4444-444444444444', 6, 'flexible', '{"availability": "flexible"}', 10, '2025-08-23T15:19:27.398754'),
('1d1f52be-def1-44e4-9582-75aba17510b0', '54b88514-926d-42d6-a8a0-0acf8070af4f', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-23T15:19:27.398754'),
('c2aa337a-3e33-48b5-9fc3-50d50444fd5c', '54b88514-926d-42d6-a8a0-0acf8070af4f', 'f4444444-4444-4444-4444-444444444444', 8, '$75_100', '{"budget": "$75_100"}', 15, '2025-08-23T15:19:27.398754'),
('89afb5fb-6e55-4187-a4f1-994c607dd854', '54b88514-926d-42d6-a8a0-0acf8070af4f', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-23T15:19:27.398754'),
('7ef1e244-43af-4d1a-9051-9d5bb003f51e', '54b88514-926d-42d6-a8a0-0acf8070af4f', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-23T15:19:27.398754');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('60fd6681-0bfb-40f7-875a-3c1182f80338', '54b88514-926d-42d6-a8a0-0acf8070af4f', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'maybe', '{"name": "Monica_2 Bellucci", "email": "monica.bellucci_2@fashion.com", "phone": "(617) 555-8520"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 9: Unqualified - Peter_2 Parker
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('ccb8c734-821a-4c87-8f2d-cecaea265427', 'f4444444-4444-4444-4444-444444444444', 'fitlife_009_unqualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-17T09:19:27.398812', '2025-08-17T09:46:27.398813', '2025-08-17T09:46:27.398813', 8, true, 35, 35, 'no', 'qualified', 'Thank you for considering FitLife. While our current programs may not be the right fit, we wish you success in your fitness journey.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.159', '{"device_type": "mobile", "completion_time": 33}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('1b76c54d-70b5-48d3-b191-9933c698a3f5', 'ccb8c734-821a-4c87-8f2d-cecaea265427', 'organic', 'search', 'student_fitness', 'fitness coach', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('a67198d3-9ad8-4c85-8da9-524244ab5d49', 'ccb8c734-821a-4c87-8f2d-cecaea265427', 'f4444444-4444-4444-4444-444444444444', 1, 'Peter_2 Parker', '{"name": "Peter_2 Parker"}', 10, '2025-08-17T09:19:27.398812'),
('6d4c1711-cc53-41a4-94a6-aac83c532c74', 'ccb8c734-821a-4c87-8f2d-cecaea265427', 'f4444444-4444-4444-4444-444444444444', 2, 'peter.parker_2@university.edu', '{"email": "peter.parker_2@university.edu"}', 10, '2025-08-17T09:19:27.398812'),
('f67247e7-3de2-456e-97d9-4c012270e5a9', 'ccb8c734-821a-4c87-8f2d-cecaea265427', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-9630', '{"phone": "(617) 555-9630"}', 15, '2025-08-17T09:19:27.398812'),
('601ebe30-ee49-4576-bda7-40200e15e195', 'ccb8c734-821a-4c87-8f2d-cecaea265427', 'f4444444-4444-4444-4444-444444444444', 4, 'athletic_performance', '{"fitness_goals": "athletic_performance"}', 10, '2025-08-17T09:19:27.398812'),
('3a5b9139-3d14-42f8-bedb-219c4a7a2546', 'ccb8c734-821a-4c87-8f2d-cecaea265427', 'f4444444-4444-4444-4444-444444444444', 5, 'advanced', '{"experience_level": "advanced"}', 10, '2025-08-17T09:19:27.398812'),
('b93049b1-909a-4efa-af81-a57fca719b4d', 'ccb8c734-821a-4c87-8f2d-cecaea265427', 'f4444444-4444-4444-4444-444444444444', 6, 'afternoons', '{"availability": "afternoons"}', 10, '2025-08-17T09:19:27.398812'),
('60df2202-c0e6-435c-aa00-99ce1863dbfa', 'ccb8c734-821a-4c87-8f2d-cecaea265427', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-17T09:19:27.398812'),
('93f18763-176d-4bc9-a69e-276a05cb664d', 'ccb8c734-821a-4c87-8f2d-cecaea265427', 'f4444444-4444-4444-4444-444444444444', 8, 'under_75', '{"budget": "under_75"}', 5, '2025-08-17T09:19:27.398812'),
('201b3fdf-1503-4432-b586-a63cf39066f7', 'ccb8c734-821a-4c87-8f2d-cecaea265427', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-17T09:19:27.398812'),
('2883f9a9-d83d-440b-a53d-91d67b839ea8', 'ccb8c734-821a-4c87-8f2d-cecaea265427', 'f4444444-4444-4444-4444-444444444444', 10, 'just_exploring', '{"timeline": "just_exploring"}', 0, '2025-08-17T09:19:27.398812');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('14fcbe8e-fda9-4cfc-aee0-a4e1cad9ee7b', 'ccb8c734-821a-4c87-8f2d-cecaea265427', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'unqualified', '{"name": "Peter_2 Parker", "email": "peter.parker_2@university.edu", "phone": "(617) 555-9630"}', 35, 0.35, false, false, NULL, NULL, NULL);


-- Lead 10: Maybe - Diana_2 Prince
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('8c352753-b313-4022-bea0-6f41c1f77d6a', 'f4444444-4444-4444-4444-444444444444', 'fitlife_010_maybe', 'a4444444-4444-4444-4444-444444444444', '2025-08-14T03:19:27.398869', '2025-08-14T03:47:27.398870', '2025-08-14T03:47:27.398870', 9, true, 70, 70, 'maybe', 'qualified', 'Thank you for your interest in FitLife! We are reviewing your fitness goals to create the best training plan. Expect to hear from us soon.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.221', '{"device_type": "desktop", "completion_time": 17}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('6e64b5c2-95f4-418a-b9fb-b85c28553bba', '8c352753-b313-4022-bea0-6f41c1f77d6a', 'referral', 'referral', 'specialized_training', 'personal trainer boston', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('db5fb11b-bd3c-4d7c-832a-802daa65692b', '8c352753-b313-4022-bea0-6f41c1f77d6a', 'f4444444-4444-4444-4444-444444444444', 1, 'Diana_2 Prince', '{"name": "Diana_2 Prince"}', 10, '2025-08-14T03:19:27.398869'),
('d4e06ba9-f48e-4f6a-9fbe-a114d189dfe7', '8c352753-b313-4022-bea0-6f41c1f77d6a', 'f4444444-4444-4444-4444-444444444444', 2, 'diana.prince_2@embassy.gov', '{"email": "diana.prince_2@embassy.gov"}', 10, '2025-08-14T03:19:27.398869'),
('b8c4cffb-4d3a-4789-8945-e94ea9a26c6b', '8c352753-b313-4022-bea0-6f41c1f77d6a', 'f4444444-4444-4444-4444-444444444444', 3, '(781) 555-1470', '{"phone": "(781) 555-1470"}', 15, '2025-08-14T03:19:27.398869'),
('d3657557-3098-4fb9-b8be-0a247131ee97', '8c352753-b313-4022-bea0-6f41c1f77d6a', 'f4444444-4444-4444-4444-444444444444', 4, 'martial_arts', '{"fitness_goals": "martial_arts"}', 10, '2025-08-14T03:19:27.398869'),
('6b359b0f-0bdd-4f00-9e76-62bb8ca87658', '8c352753-b313-4022-bea0-6f41c1f77d6a', 'f4444444-4444-4444-4444-444444444444', 5, 'advanced', '{"experience_level": "advanced"}', 10, '2025-08-14T03:19:27.398869'),
('5f7c828b-f21a-4fb8-8df8-648217724ef8', '8c352753-b313-4022-bea0-6f41c1f77d6a', 'f4444444-4444-4444-4444-444444444444', 6, 'evenings', '{"availability": "evenings"}', 10, '2025-08-14T03:19:27.398869'),
('2d228cd0-f333-4c15-817d-b29e8cab03c3', '8c352753-b313-4022-bea0-6f41c1f77d6a', 'f4444444-4444-4444-4444-444444444444', 7, 'home', '{"preferred_location": "home"}', 10, '2025-08-14T03:19:27.398869'),
('48cf67af-7695-4f71-845a-fe711928234f', '8c352753-b313-4022-bea0-6f41c1f77d6a', 'f4444444-4444-4444-4444-444444444444', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-14T03:19:27.398869'),
('fbc9d9b4-a448-48fa-bb64-e2854d880a69', '8c352753-b313-4022-bea0-6f41c1f77d6a', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-14T03:19:27.398869'),
('e50be9ed-f530-46b5-8080-5798fa9b3af0', '8c352753-b313-4022-bea0-6f41c1f77d6a', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-14T03:19:27.398869');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('b674664e-6f28-48f4-9f57-a1a8c55506f1', '8c352753-b313-4022-bea0-6f41c1f77d6a', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'maybe', '{"name": "Diana_2 Prince", "email": "diana.prince_2@embassy.gov", "phone": "(781) 555-1470"}', 70, 0.70, true, false, NULL, NULL, NULL);


-- Lead 11: Qualified - Rachel_3 Green
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('e220dea9-7dc7-446a-a65e-87d79335e003', 'f4444444-4444-4444-4444-444444444444', 'fitlife_011_qualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-11T12:19:27.398928', '2025-08-11T13:04:27.398929', '2025-08-11T13:04:27.398929', 6, true, 88, 88, 'yes', 'qualified', 'Great news! You are an excellent candidate for our personal training programs. We will contact you within 24 hours to schedule your consultation.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.191', '{"device_type": "mobile", "completion_time": 30}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('67e3954c-3000-4a6c-9cc6-07808a012b90', 'e220dea9-7dc7-446a-a65e-87d79335e003', 'instagram', 'social', 'transformation_stories', 'personal trainer boston', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('2a5aea49-7837-433b-89f4-79aae12956ac', 'e220dea9-7dc7-446a-a65e-87d79335e003', 'f4444444-4444-4444-4444-444444444444', 1, 'Rachel_3 Green', '{"name": "Rachel_3 Green"}', 10, '2025-08-11T12:19:27.398928'),
('2722bb9f-39ef-4566-b6fc-aa04dfb97ff4', 'e220dea9-7dc7-446a-a65e-87d79335e003', 'f4444444-4444-4444-4444-444444444444', 2, 'rachel.green_3@consulting.com', '{"email": "rachel.green_3@consulting.com"}', 10, '2025-08-11T12:19:27.398928'),
('694b3431-4a31-43e7-bf53-6a6f05083f04', 'e220dea9-7dc7-446a-a65e-87d79335e003', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-3691', '{"phone": "(617) 555-3691"}', 15, '2025-08-11T12:19:27.398928'),
('3ef9c4a6-dd20-47d1-a3bc-ce0038da7027', 'e220dea9-7dc7-446a-a65e-87d79335e003', 'f4444444-4444-4444-4444-444444444444', 4, 'weight_loss', '{"fitness_goals": "weight_loss"}', 10, '2025-08-11T12:19:27.398928'),
('a7c97f02-a069-437d-99a1-2281c842362a', 'e220dea9-7dc7-446a-a65e-87d79335e003', 'f4444444-4444-4444-4444-444444444444', 5, 'beginner', '{"experience_level": "beginner"}', 10, '2025-08-11T12:19:27.398928'),
('ce871c68-5acf-4c05-aba7-40cac134befa', 'e220dea9-7dc7-446a-a65e-87d79335e003', 'f4444444-4444-4444-4444-444444444444', 6, 'mornings', '{"availability": "mornings"}', 10, '2025-08-11T12:19:27.398928'),
('8288bc8e-1907-4094-ab12-de0911cedbb8', 'e220dea9-7dc7-446a-a65e-87d79335e003', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-11T12:19:27.398928'),
('edaa7a85-d2bc-4f88-9744-67830dd16169', 'e220dea9-7dc7-446a-a65e-87d79335e003', 'f4444444-4444-4444-4444-444444444444', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-11T12:19:27.398928'),
('67dffb78-ce07-421a-a615-8c429a870899', 'e220dea9-7dc7-446a-a65e-87d79335e003', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-11T12:19:27.398928'),
('4b80c9e2-8596-4d55-905f-4ef1f990ed1a', 'e220dea9-7dc7-446a-a65e-87d79335e003', 'f4444444-4444-4444-4444-444444444444', 10, 'asap', '{"timeline": "asap"}', 25, '2025-08-11T12:19:27.398928');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('918ca9c5-cdab-402d-b099-ccf3407977f1', 'e220dea9-7dc7-446a-a65e-87d79335e003', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'qualified', '{"name": "Rachel_3 Green", "email": "rachel.green_3@consulting.com", "phone": "(617) 555-3691"}', 88, 0.88, true, false, NULL, NULL, NULL);


-- Lead 12: Qualified - Steve_3 Rogers
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('7cd8c8db-90b7-4460-9c35-670eff8e1149', 'f4444444-4444-4444-4444-444444444444', 'fitlife_012_qualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-10T03:19:27.398986', '2025-08-10T03:43:27.398987', '2025-08-10T03:43:27.398987', 8, true, 92, 92, 'yes', 'qualified', 'Great news! You are an excellent candidate for our personal training programs. We will contact you within 24 hours to schedule your consultation.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.182', '{"device_type": "desktop", "completion_time": 32}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('2676103a-aeee-4af5-aa54-95fbfdfaba19', '7cd8c8db-90b7-4460-9c35-670eff8e1149', 'google', 'cpc', 'strength_training', 'weight loss trainer', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('9f1537f3-9150-4eba-9705-5e4d5524c8d2', '7cd8c8db-90b7-4460-9c35-670eff8e1149', 'f4444444-4444-4444-4444-444444444444', 1, 'Steve_3 Rogers', '{"name": "Steve_3 Rogers"}', 10, '2025-08-10T03:19:27.398986'),
('0d9aa451-7d41-4067-8d70-f04d45e79182', '7cd8c8db-90b7-4460-9c35-670eff8e1149', 'f4444444-4444-4444-4444-444444444444', 2, 'steve.rogers_3@military.gov', '{"email": "steve.rogers_3@military.gov"}', 10, '2025-08-10T03:19:27.398986'),
('0fac8364-af2c-4aee-876f-3574ff9678d2', '7cd8c8db-90b7-4460-9c35-670eff8e1149', 'f4444444-4444-4444-4444-444444444444', 3, '(857) 555-7410', '{"phone": "(857) 555-7410"}', 15, '2025-08-10T03:19:27.398986'),
('7b5b3809-393f-477d-8849-1dd4216d5c85', '7cd8c8db-90b7-4460-9c35-670eff8e1149', 'f4444444-4444-4444-4444-444444444444', 4, 'strength_building', '{"fitness_goals": "strength_building"}', 10, '2025-08-10T03:19:27.398986'),
('bf8e2b0f-5c29-4461-9ac1-77b7fcdca185', '7cd8c8db-90b7-4460-9c35-670eff8e1149', 'f4444444-4444-4444-4444-444444444444', 5, 'intermediate', '{"experience_level": "intermediate"}', 10, '2025-08-10T03:19:27.398986'),
('09ef9760-3f7c-4d10-a3b1-01211b4d519b', '7cd8c8db-90b7-4460-9c35-670eff8e1149', 'f4444444-4444-4444-4444-444444444444', 6, 'evenings', '{"availability": "evenings"}', 10, '2025-08-10T03:19:27.398986'),
('69277af3-96df-4231-b9a6-a0f02e43098a', '7cd8c8db-90b7-4460-9c35-670eff8e1149', 'f4444444-4444-4444-4444-444444444444', 7, 'home', '{"preferred_location": "home"}', 10, '2025-08-10T03:19:27.398986'),
('f66df2e5-e6de-4e27-8f2e-e2c652343dc7', '7cd8c8db-90b7-4460-9c35-670eff8e1149', 'f4444444-4444-4444-4444-444444444444', 8, '$150_200', '{"budget": "$150_200"}', 25, '2025-08-10T03:19:27.398986'),
('8a691a6a-7b0d-42ad-a8e1-6c497bb260cc', '7cd8c8db-90b7-4460-9c35-670eff8e1149', 'f4444444-4444-4444-4444-444444444444', 9, 'minor_injury', '{"health_conditions": "minor_injury"}', 10, '2025-08-10T03:19:27.398986'),
('cbece527-5fa5-4b62-a90f-1943d4f87d06', '7cd8c8db-90b7-4460-9c35-670eff8e1149', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-10T03:19:27.398986');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('a0b38083-591c-476a-8493-fb71abe6bbde', '7cd8c8db-90b7-4460-9c35-670eff8e1149', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'qualified', '{"name": "Steve_3 Rogers", "email": "steve.rogers_3@military.gov", "phone": "(857) 555-7410"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 13: Maybe - Monica_3 Bellucci
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('eecdd12e-9ef0-403a-ad54-fc504a9b1533', 'f4444444-4444-4444-4444-444444444444', 'fitlife_013_maybe', 'a4444444-4444-4444-4444-444444444444', '2025-08-23T07:19:27.399044', '2025-08-23T08:00:27.399045', '2025-08-23T08:00:27.399045', 9, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest in FitLife! We are reviewing your fitness goals to create the best training plan. Expect to hear from us soon.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.223', '{"device_type": "mobile", "completion_time": 40}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('0bf27d60-79cf-497a-87f1-511d256538f3', 'eecdd12e-9ef0-403a-ad54-fc504a9b1533', 'facebook', 'social', 'group_fitness', 'strength training', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('1e40a96e-2e3e-43f0-a167-997e53635940', 'eecdd12e-9ef0-403a-ad54-fc504a9b1533', 'f4444444-4444-4444-4444-444444444444', 1, 'Monica_3 Bellucci', '{"name": "Monica_3 Bellucci"}', 10, '2025-08-23T07:19:27.399044'),
('903faf0f-ae6d-4bca-a011-5ef25b5f0fbd', 'eecdd12e-9ef0-403a-ad54-fc504a9b1533', 'f4444444-4444-4444-4444-444444444444', 2, 'monica.bellucci_3@fashion.com', '{"email": "monica.bellucci_3@fashion.com"}', 10, '2025-08-23T07:19:27.399044'),
('27425bbf-3841-4a78-97d6-271aa79661ed', 'eecdd12e-9ef0-403a-ad54-fc504a9b1533', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-8520', '{"phone": "(617) 555-8520"}', 15, '2025-08-23T07:19:27.399044'),
('5906fd10-333e-4e12-83d7-fab0f144e851', 'eecdd12e-9ef0-403a-ad54-fc504a9b1533', 'f4444444-4444-4444-4444-444444444444', 4, 'general_fitness', '{"fitness_goals": "general_fitness"}', 10, '2025-08-23T07:19:27.399044'),
('50113f88-8485-4923-a2b2-ccd9f79c8fae', 'eecdd12e-9ef0-403a-ad54-fc504a9b1533', 'f4444444-4444-4444-4444-444444444444', 5, 'intermediate', '{"experience_level": "intermediate"}', 10, '2025-08-23T07:19:27.399044'),
('e157657b-420a-453f-a4b1-7cd9c60ed48a', 'eecdd12e-9ef0-403a-ad54-fc504a9b1533', 'f4444444-4444-4444-4444-444444444444', 6, 'flexible', '{"availability": "flexible"}', 10, '2025-08-23T07:19:27.399044'),
('ecb3dc64-cd71-4d67-9833-83a0a7625ecb', 'eecdd12e-9ef0-403a-ad54-fc504a9b1533', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-23T07:19:27.399044'),
('d672014b-352d-4dbb-b18e-6cef1dd38bc3', 'eecdd12e-9ef0-403a-ad54-fc504a9b1533', 'f4444444-4444-4444-4444-444444444444', 8, '$75_100', '{"budget": "$75_100"}', 15, '2025-08-23T07:19:27.399044'),
('c52a64d9-79db-472b-8c34-a2e2c3e3a701', 'eecdd12e-9ef0-403a-ad54-fc504a9b1533', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-23T07:19:27.399044'),
('c2a3bb3f-c781-4fd3-9a48-05f726d67c6a', 'eecdd12e-9ef0-403a-ad54-fc504a9b1533', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-23T07:19:27.399044');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('1002b970-b3a4-4b44-998c-c3b3191edc52', 'eecdd12e-9ef0-403a-ad54-fc504a9b1533', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'maybe', '{"name": "Monica_3 Bellucci", "email": "monica.bellucci_3@fashion.com", "phone": "(617) 555-8520"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 14: Unqualified - Peter_3 Parker
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('a4cc070c-07a3-43bb-b45f-e363e00c2864', 'f4444444-4444-4444-4444-444444444444', 'fitlife_014_unqualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-15T13:19:27.399101', '2025-08-15T13:45:27.399102', '2025-08-15T13:45:27.399102', 7, true, 35, 35, 'no', 'qualified', 'Thank you for considering FitLife. While our current programs may not be the right fit, we wish you success in your fitness journey.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.34', '{"device_type": "mobile", "completion_time": 49}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('58dae075-4a06-44bb-a16d-d1d6239666d0', 'a4cc070c-07a3-43bb-b45f-e363e00c2864', 'organic', 'search', 'student_fitness', 'strength training', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Brookline');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('9dbc4391-1ee7-4e03-bc5d-3249da2fe865', 'a4cc070c-07a3-43bb-b45f-e363e00c2864', 'f4444444-4444-4444-4444-444444444444', 1, 'Peter_3 Parker', '{"name": "Peter_3 Parker"}', 10, '2025-08-15T13:19:27.399101'),
('eeb5d3df-757a-49d5-890b-ac82be477d3f', 'a4cc070c-07a3-43bb-b45f-e363e00c2864', 'f4444444-4444-4444-4444-444444444444', 2, 'peter.parker_3@university.edu', '{"email": "peter.parker_3@university.edu"}', 10, '2025-08-15T13:19:27.399101'),
('15dd4e80-63d7-4de4-a4c6-54458ab50982', 'a4cc070c-07a3-43bb-b45f-e363e00c2864', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-9630', '{"phone": "(617) 555-9630"}', 15, '2025-08-15T13:19:27.399101'),
('be9c0384-c357-4128-bf47-5f299d0e3c4b', 'a4cc070c-07a3-43bb-b45f-e363e00c2864', 'f4444444-4444-4444-4444-444444444444', 4, 'athletic_performance', '{"fitness_goals": "athletic_performance"}', 10, '2025-08-15T13:19:27.399101'),
('6450537a-64dd-437c-ba9b-031e3dca935f', 'a4cc070c-07a3-43bb-b45f-e363e00c2864', 'f4444444-4444-4444-4444-444444444444', 5, 'advanced', '{"experience_level": "advanced"}', 10, '2025-08-15T13:19:27.399101'),
('d40a58f4-d9d0-4cd7-a805-09a4295892e5', 'a4cc070c-07a3-43bb-b45f-e363e00c2864', 'f4444444-4444-4444-4444-444444444444', 6, 'afternoons', '{"availability": "afternoons"}', 10, '2025-08-15T13:19:27.399101'),
('9af01c73-196b-4a7e-aae8-2010cd6ceb20', 'a4cc070c-07a3-43bb-b45f-e363e00c2864', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-15T13:19:27.399101'),
('b1f4efac-ac50-45b2-ad31-fc35a796185d', 'a4cc070c-07a3-43bb-b45f-e363e00c2864', 'f4444444-4444-4444-4444-444444444444', 8, 'under_75', '{"budget": "under_75"}', 5, '2025-08-15T13:19:27.399101'),
('186e2b9b-5876-4d37-aa39-70fca3497486', 'a4cc070c-07a3-43bb-b45f-e363e00c2864', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-15T13:19:27.399101'),
('78a40ce6-f89a-42eb-93b2-4a83f50c4b6c', 'a4cc070c-07a3-43bb-b45f-e363e00c2864', 'f4444444-4444-4444-4444-444444444444', 10, 'just_exploring', '{"timeline": "just_exploring"}', 0, '2025-08-15T13:19:27.399101');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('fdcadfd0-ec6f-4a7f-a857-5bdb5f198b7f', 'a4cc070c-07a3-43bb-b45f-e363e00c2864', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'unqualified', '{"name": "Peter_3 Parker", "email": "peter.parker_3@university.edu", "phone": "(617) 555-9630"}', 35, 0.35, false, false, NULL, NULL, NULL);


-- Lead 15: Maybe - Diana_3 Prince
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('88aadb4c-8f0d-4362-80fb-b730a3633082', 'f4444444-4444-4444-4444-444444444444', 'fitlife_015_maybe', 'a4444444-4444-4444-4444-444444444444', '2025-08-10T11:19:27.399161', '2025-08-10T12:01:27.399162', '2025-08-10T12:01:27.399162', 10, true, 70, 70, 'maybe', 'qualified', 'Thank you for your interest in FitLife! We are reviewing your fitness goals to create the best training plan. Expect to hear from us soon.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.114', '{"device_type": "desktop", "completion_time": 15}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('967021b9-048d-4bea-ba83-e79353f8a2de', '88aadb4c-8f0d-4362-80fb-b730a3633082', 'referral', 'referral', 'specialized_training', 'fitness coach', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('83bb622d-59c0-4ac7-8c8f-88cde02cb594', '88aadb4c-8f0d-4362-80fb-b730a3633082', 'f4444444-4444-4444-4444-444444444444', 1, 'Diana_3 Prince', '{"name": "Diana_3 Prince"}', 10, '2025-08-10T11:19:27.399161'),
('9d4bb4f1-2762-4db8-aafa-23f3284062d5', '88aadb4c-8f0d-4362-80fb-b730a3633082', 'f4444444-4444-4444-4444-444444444444', 2, 'diana.prince_3@embassy.gov', '{"email": "diana.prince_3@embassy.gov"}', 10, '2025-08-10T11:19:27.399161'),
('cfbcc4b8-4754-42fb-b11f-8a2c32baef34', '88aadb4c-8f0d-4362-80fb-b730a3633082', 'f4444444-4444-4444-4444-444444444444', 3, '(781) 555-1470', '{"phone": "(781) 555-1470"}', 15, '2025-08-10T11:19:27.399161'),
('9db25b4e-4cf1-4f38-8f1b-feb59ae15a81', '88aadb4c-8f0d-4362-80fb-b730a3633082', 'f4444444-4444-4444-4444-444444444444', 4, 'martial_arts', '{"fitness_goals": "martial_arts"}', 10, '2025-08-10T11:19:27.399161'),
('f2e78a8a-42e8-4242-829f-b2aa2eb79809', '88aadb4c-8f0d-4362-80fb-b730a3633082', 'f4444444-4444-4444-4444-444444444444', 5, 'advanced', '{"experience_level": "advanced"}', 10, '2025-08-10T11:19:27.399161'),
('d5205d9c-20c0-4162-aeda-5a4adebeac01', '88aadb4c-8f0d-4362-80fb-b730a3633082', 'f4444444-4444-4444-4444-444444444444', 6, 'evenings', '{"availability": "evenings"}', 10, '2025-08-10T11:19:27.399161'),
('6f037fde-11a2-422d-a49a-69f96f5159c8', '88aadb4c-8f0d-4362-80fb-b730a3633082', 'f4444444-4444-4444-4444-444444444444', 7, 'home', '{"preferred_location": "home"}', 10, '2025-08-10T11:19:27.399161'),
('2f77e3c8-ba98-4c13-8bcf-162a5b6a2454', '88aadb4c-8f0d-4362-80fb-b730a3633082', 'f4444444-4444-4444-4444-444444444444', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-10T11:19:27.399161'),
('a6291990-7484-4065-af5e-f99021c268d8', '88aadb4c-8f0d-4362-80fb-b730a3633082', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-10T11:19:27.399161'),
('6acf536a-30de-4c1a-9561-1ade2ffc3a3d', '88aadb4c-8f0d-4362-80fb-b730a3633082', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-10T11:19:27.399161');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('c47e7901-1d70-4fdb-a7c3-b4554e53ca8f', '88aadb4c-8f0d-4362-80fb-b730a3633082', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'maybe', '{"name": "Diana_3 Prince", "email": "diana.prince_3@embassy.gov", "phone": "(781) 555-1470"}', 70, 0.70, true, false, NULL, NULL, NULL);


-- Lead 16: Qualified - Rachel_4 Green
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('0ece790b-7e17-4f99-9702-c80e0977410c', 'f4444444-4444-4444-4444-444444444444', 'fitlife_016_qualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-19T06:19:27.399218', '2025-08-19T06:51:27.399219', '2025-08-19T06:51:27.399219', 6, true, 88, 88, 'yes', 'qualified', 'Great news! You are an excellent candidate for our personal training programs. We will contact you within 24 hours to schedule your consultation.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.93', '{"device_type": "mobile", "completion_time": 14}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('0785c92b-6ab7-4e9f-8b45-21897195f640', '0ece790b-7e17-4f99-9702-c80e0977410c', 'instagram', 'social', 'transformation_stories', 'personal fitness', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('28185c09-748b-4d66-bf9b-8283441bc974', '0ece790b-7e17-4f99-9702-c80e0977410c', 'f4444444-4444-4444-4444-444444444444', 1, 'Rachel_4 Green', '{"name": "Rachel_4 Green"}', 10, '2025-08-19T06:19:27.399218'),
('5fd6eb33-f0b9-4c20-9e4a-de379b851e46', '0ece790b-7e17-4f99-9702-c80e0977410c', 'f4444444-4444-4444-4444-444444444444', 2, 'rachel.green_4@consulting.com', '{"email": "rachel.green_4@consulting.com"}', 10, '2025-08-19T06:19:27.399218'),
('d3ad57de-892b-487a-8294-52eca0c79e61', '0ece790b-7e17-4f99-9702-c80e0977410c', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-3691', '{"phone": "(617) 555-3691"}', 15, '2025-08-19T06:19:27.399218'),
('a665321d-da84-41ad-b727-fb9033a514f0', '0ece790b-7e17-4f99-9702-c80e0977410c', 'f4444444-4444-4444-4444-444444444444', 4, 'weight_loss', '{"fitness_goals": "weight_loss"}', 10, '2025-08-19T06:19:27.399218'),
('852b984a-23cb-4ec0-8e15-d01427f8c541', '0ece790b-7e17-4f99-9702-c80e0977410c', 'f4444444-4444-4444-4444-444444444444', 5, 'beginner', '{"experience_level": "beginner"}', 10, '2025-08-19T06:19:27.399218'),
('09320237-6e08-437b-b75d-741f4584815e', '0ece790b-7e17-4f99-9702-c80e0977410c', 'f4444444-4444-4444-4444-444444444444', 6, 'mornings', '{"availability": "mornings"}', 10, '2025-08-19T06:19:27.399218'),
('6bff1d10-b5a2-40c3-b843-79eb170c6595', '0ece790b-7e17-4f99-9702-c80e0977410c', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-19T06:19:27.399218'),
('b0311390-0e53-4745-b208-951ac5f57509', '0ece790b-7e17-4f99-9702-c80e0977410c', 'f4444444-4444-4444-4444-444444444444', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-19T06:19:27.399218'),
('8d07ffa9-8c26-4d6b-be70-e27500195c18', '0ece790b-7e17-4f99-9702-c80e0977410c', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-19T06:19:27.399218'),
('3a5da4ea-cc60-46a4-83f7-e585f11e5675', '0ece790b-7e17-4f99-9702-c80e0977410c', 'f4444444-4444-4444-4444-444444444444', 10, 'asap', '{"timeline": "asap"}', 25, '2025-08-19T06:19:27.399218');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('9d4fe5d8-87c7-485a-b9b5-fb8a0b95ec2e', '0ece790b-7e17-4f99-9702-c80e0977410c', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'qualified', '{"name": "Rachel_4 Green", "email": "rachel.green_4@consulting.com", "phone": "(617) 555-3691"}', 88, 0.88, true, false, NULL, NULL, NULL);


-- Lead 17: Qualified - Steve_4 Rogers
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('cce4a468-587c-485a-bdd7-eec46a9d2765', 'f4444444-4444-4444-4444-444444444444', 'fitlife_017_qualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-22T19:19:27.399278', '2025-08-22T19:37:27.399279', '2025-08-22T19:37:27.399279', 10, true, 92, 92, 'yes', 'qualified', 'Great news! You are an excellent candidate for our personal training programs. We will contact you within 24 hours to schedule your consultation.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.204', '{"device_type": "desktop", "completion_time": 44}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('c9d74b56-e4d9-4c8d-bb1b-41cfbb5c8183', 'cce4a468-587c-485a-bdd7-eec46a9d2765', 'google', 'cpc', 'strength_training', 'fitness coach', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('738d1213-5805-4465-b4ca-338555a5f49b', 'cce4a468-587c-485a-bdd7-eec46a9d2765', 'f4444444-4444-4444-4444-444444444444', 1, 'Steve_4 Rogers', '{"name": "Steve_4 Rogers"}', 10, '2025-08-22T19:19:27.399278'),
('372fc5c3-e383-45dd-8860-8ea3e5a9fe0e', 'cce4a468-587c-485a-bdd7-eec46a9d2765', 'f4444444-4444-4444-4444-444444444444', 2, 'steve.rogers_4@military.gov', '{"email": "steve.rogers_4@military.gov"}', 10, '2025-08-22T19:19:27.399278'),
('82288a93-12de-4429-8f26-236778d45b31', 'cce4a468-587c-485a-bdd7-eec46a9d2765', 'f4444444-4444-4444-4444-444444444444', 3, '(857) 555-7410', '{"phone": "(857) 555-7410"}', 15, '2025-08-22T19:19:27.399278'),
('9cc163c8-bf9c-4a48-9add-623afeb2d926', 'cce4a468-587c-485a-bdd7-eec46a9d2765', 'f4444444-4444-4444-4444-444444444444', 4, 'strength_building', '{"fitness_goals": "strength_building"}', 10, '2025-08-22T19:19:27.399278'),
('167459b0-bd64-477e-91d6-5f1f8a0007f9', 'cce4a468-587c-485a-bdd7-eec46a9d2765', 'f4444444-4444-4444-4444-444444444444', 5, 'intermediate', '{"experience_level": "intermediate"}', 10, '2025-08-22T19:19:27.399278'),
('831bd681-fa58-48aa-80a7-82bbe9cc2518', 'cce4a468-587c-485a-bdd7-eec46a9d2765', 'f4444444-4444-4444-4444-444444444444', 6, 'evenings', '{"availability": "evenings"}', 10, '2025-08-22T19:19:27.399278'),
('6d0eec55-0b32-45da-b729-a973e24f3458', 'cce4a468-587c-485a-bdd7-eec46a9d2765', 'f4444444-4444-4444-4444-444444444444', 7, 'home', '{"preferred_location": "home"}', 10, '2025-08-22T19:19:27.399278'),
('b3439e9f-7f67-4ad7-8bee-4f40b30facf9', 'cce4a468-587c-485a-bdd7-eec46a9d2765', 'f4444444-4444-4444-4444-444444444444', 8, '$150_200', '{"budget": "$150_200"}', 25, '2025-08-22T19:19:27.399278'),
('0eae6d5b-6238-42bc-8f09-d6aac9f36d10', 'cce4a468-587c-485a-bdd7-eec46a9d2765', 'f4444444-4444-4444-4444-444444444444', 9, 'minor_injury', '{"health_conditions": "minor_injury"}', 10, '2025-08-22T19:19:27.399278'),
('7d8f8a8e-35ea-46cd-aba5-2e7916eda68d', 'cce4a468-587c-485a-bdd7-eec46a9d2765', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-22T19:19:27.399278');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('a815a4d7-ad72-4c97-9128-a7b5c51dee90', 'cce4a468-587c-485a-bdd7-eec46a9d2765', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'qualified', '{"name": "Steve_4 Rogers", "email": "steve.rogers_4@military.gov", "phone": "(857) 555-7410"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 18: Maybe - Monica_4 Bellucci
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('2e43cf30-b520-47bb-8ed9-6b53238dd1f9', 'f4444444-4444-4444-4444-444444444444', 'fitlife_018_maybe', 'a4444444-4444-4444-4444-444444444444', '2025-08-23T00:19:27.399334', '2025-08-23T01:02:27.399335', '2025-08-23T01:02:27.399335', 6, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest in FitLife! We are reviewing your fitness goals to create the best training plan. Expect to hear from us soon.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.163', '{"device_type": "mobile", "completion_time": 41}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('7f5aa2c8-411d-4db1-af1b-f15d183132c2', '2e43cf30-b520-47bb-8ed9-6b53238dd1f9', 'facebook', 'social', 'group_fitness', 'fitness coach', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('9ac32904-5840-45fc-a2ff-928e3377c966', '2e43cf30-b520-47bb-8ed9-6b53238dd1f9', 'f4444444-4444-4444-4444-444444444444', 1, 'Monica_4 Bellucci', '{"name": "Monica_4 Bellucci"}', 10, '2025-08-23T00:19:27.399334'),
('9a232c99-3bb8-4f5a-ba29-3178873ebc95', '2e43cf30-b520-47bb-8ed9-6b53238dd1f9', 'f4444444-4444-4444-4444-444444444444', 2, 'monica.bellucci_4@fashion.com', '{"email": "monica.bellucci_4@fashion.com"}', 10, '2025-08-23T00:19:27.399334'),
('b0a96305-a1e0-4bbd-9347-8a62aee6cbf2', '2e43cf30-b520-47bb-8ed9-6b53238dd1f9', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-8520', '{"phone": "(617) 555-8520"}', 15, '2025-08-23T00:19:27.399334'),
('9bb67da9-4cdf-46e9-aaba-ba3cda7c7f6d', '2e43cf30-b520-47bb-8ed9-6b53238dd1f9', 'f4444444-4444-4444-4444-444444444444', 4, 'general_fitness', '{"fitness_goals": "general_fitness"}', 10, '2025-08-23T00:19:27.399334'),
('1a2377ca-b89c-4c01-a4eb-059d84c9d7c5', '2e43cf30-b520-47bb-8ed9-6b53238dd1f9', 'f4444444-4444-4444-4444-444444444444', 5, 'intermediate', '{"experience_level": "intermediate"}', 10, '2025-08-23T00:19:27.399334'),
('2777bae6-068c-4503-8f7a-ecccf0a8b93a', '2e43cf30-b520-47bb-8ed9-6b53238dd1f9', 'f4444444-4444-4444-4444-444444444444', 6, 'flexible', '{"availability": "flexible"}', 10, '2025-08-23T00:19:27.399334'),
('b015b0b6-e334-4b40-92fb-5d5b1ba895ff', '2e43cf30-b520-47bb-8ed9-6b53238dd1f9', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-23T00:19:27.399334'),
('c1f81c5b-803f-4261-8760-2f5f5ae74942', '2e43cf30-b520-47bb-8ed9-6b53238dd1f9', 'f4444444-4444-4444-4444-444444444444', 8, '$75_100', '{"budget": "$75_100"}', 15, '2025-08-23T00:19:27.399334'),
('1e3386dc-de91-4a6f-96c4-2d22126a8cbb', '2e43cf30-b520-47bb-8ed9-6b53238dd1f9', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-23T00:19:27.399334'),
('0603ff0b-2bbf-4863-838a-c9ff63af62b0', '2e43cf30-b520-47bb-8ed9-6b53238dd1f9', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-23T00:19:27.399334');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('7ff292e9-d003-4369-b631-4c8da25d2c46', '2e43cf30-b520-47bb-8ed9-6b53238dd1f9', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'maybe', '{"name": "Monica_4 Bellucci", "email": "monica.bellucci_4@fashion.com", "phone": "(617) 555-8520"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 19: Unqualified - Peter_4 Parker
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('7758d5c0-fb43-481c-bee6-cc028cfa47d3', 'f4444444-4444-4444-4444-444444444444', 'fitlife_019_unqualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-21T06:19:27.399394', '2025-08-21T06:44:27.399395', '2025-08-21T06:44:27.399395', 10, true, 35, 35, 'no', 'qualified', 'Thank you for considering FitLife. While our current programs may not be the right fit, we wish you success in your fitness journey.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.168', '{"device_type": "mobile", "completion_time": 52}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('89bd803b-a1b5-4dc0-9f30-4e64f6eb30ab', '7758d5c0-fb43-481c-bee6-cc028cfa47d3', 'organic', 'search', 'student_fitness', 'personal fitness', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('3e526e42-01b8-4f01-9e3f-25a6aabdfb82', '7758d5c0-fb43-481c-bee6-cc028cfa47d3', 'f4444444-4444-4444-4444-444444444444', 1, 'Peter_4 Parker', '{"name": "Peter_4 Parker"}', 10, '2025-08-21T06:19:27.399394'),
('0df5efb2-b3cd-4f86-957b-eabe407e0d63', '7758d5c0-fb43-481c-bee6-cc028cfa47d3', 'f4444444-4444-4444-4444-444444444444', 2, 'peter.parker_4@university.edu', '{"email": "peter.parker_4@university.edu"}', 10, '2025-08-21T06:19:27.399394'),
('ebf84600-d4ed-4609-9aa2-2a2a37d72d59', '7758d5c0-fb43-481c-bee6-cc028cfa47d3', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-9630', '{"phone": "(617) 555-9630"}', 15, '2025-08-21T06:19:27.399394'),
('7003e131-257c-4b5b-81a9-bfaa9e82ab7b', '7758d5c0-fb43-481c-bee6-cc028cfa47d3', 'f4444444-4444-4444-4444-444444444444', 4, 'athletic_performance', '{"fitness_goals": "athletic_performance"}', 10, '2025-08-21T06:19:27.399394'),
('1685e013-197f-4cbc-b7fc-62440aba9046', '7758d5c0-fb43-481c-bee6-cc028cfa47d3', 'f4444444-4444-4444-4444-444444444444', 5, 'advanced', '{"experience_level": "advanced"}', 10, '2025-08-21T06:19:27.399394'),
('312d012d-7d37-433a-a7b2-94ee73065f6d', '7758d5c0-fb43-481c-bee6-cc028cfa47d3', 'f4444444-4444-4444-4444-444444444444', 6, 'afternoons', '{"availability": "afternoons"}', 10, '2025-08-21T06:19:27.399394'),
('43b9c7bc-3aab-47c2-8d40-6ba811b394f3', '7758d5c0-fb43-481c-bee6-cc028cfa47d3', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-21T06:19:27.399394'),
('a852e740-8a47-4d4b-9e5a-1f96e9208045', '7758d5c0-fb43-481c-bee6-cc028cfa47d3', 'f4444444-4444-4444-4444-444444444444', 8, 'under_75', '{"budget": "under_75"}', 5, '2025-08-21T06:19:27.399394'),
('12c04094-c01c-4bae-b9a2-528ced2196e4', '7758d5c0-fb43-481c-bee6-cc028cfa47d3', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-21T06:19:27.399394'),
('b4363c58-604f-4937-96c2-2d4b63025407', '7758d5c0-fb43-481c-bee6-cc028cfa47d3', 'f4444444-4444-4444-4444-444444444444', 10, 'just_exploring', '{"timeline": "just_exploring"}', 0, '2025-08-21T06:19:27.399394');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('00506149-a9f2-485d-8c9b-4362be5e1f11', '7758d5c0-fb43-481c-bee6-cc028cfa47d3', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'unqualified', '{"name": "Peter_4 Parker", "email": "peter.parker_4@university.edu", "phone": "(617) 555-9630"}', 35, 0.35, false, false, NULL, NULL, NULL);


-- Lead 20: Maybe - Diana_4 Prince
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('7cd332ca-9582-4414-98c3-eea8654705a9', 'f4444444-4444-4444-4444-444444444444', 'fitlife_020_maybe', 'a4444444-4444-4444-4444-444444444444', '2025-08-22T11:19:27.399454', '2025-08-22T11:41:27.399455', '2025-08-22T11:41:27.399455', 9, true, 70, 70, 'maybe', 'qualified', 'Thank you for your interest in FitLife! We are reviewing your fitness goals to create the best training plan. Expect to hear from us soon.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.165', '{"device_type": "desktop", "completion_time": 51}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('d8797932-c048-4886-87cf-ef5dc162c342', '7cd332ca-9582-4414-98c3-eea8654705a9', 'referral', 'referral', 'specialized_training', 'fitness coach', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('4011b549-0038-4eb2-97f2-6a4c2af5d995', '7cd332ca-9582-4414-98c3-eea8654705a9', 'f4444444-4444-4444-4444-444444444444', 1, 'Diana_4 Prince', '{"name": "Diana_4 Prince"}', 10, '2025-08-22T11:19:27.399454'),
('58f29479-9617-410d-9dc7-5708d19cef3b', '7cd332ca-9582-4414-98c3-eea8654705a9', 'f4444444-4444-4444-4444-444444444444', 2, 'diana.prince_4@embassy.gov', '{"email": "diana.prince_4@embassy.gov"}', 10, '2025-08-22T11:19:27.399454'),
('bee0151a-4ddb-4c7d-84c0-2f47ad716450', '7cd332ca-9582-4414-98c3-eea8654705a9', 'f4444444-4444-4444-4444-444444444444', 3, '(781) 555-1470', '{"phone": "(781) 555-1470"}', 15, '2025-08-22T11:19:27.399454'),
('4c8ad017-533b-492b-8ea7-cffbd8d69897', '7cd332ca-9582-4414-98c3-eea8654705a9', 'f4444444-4444-4444-4444-444444444444', 4, 'martial_arts', '{"fitness_goals": "martial_arts"}', 10, '2025-08-22T11:19:27.399454'),
('d9323bb6-8911-4d08-afe4-16653489dcce', '7cd332ca-9582-4414-98c3-eea8654705a9', 'f4444444-4444-4444-4444-444444444444', 5, 'advanced', '{"experience_level": "advanced"}', 10, '2025-08-22T11:19:27.399454'),
('a030cb41-a7f7-4e61-a6e5-67c34cddc644', '7cd332ca-9582-4414-98c3-eea8654705a9', 'f4444444-4444-4444-4444-444444444444', 6, 'evenings', '{"availability": "evenings"}', 10, '2025-08-22T11:19:27.399454'),
('79c4d08b-22b4-4eda-acd1-eb19ea010a2b', '7cd332ca-9582-4414-98c3-eea8654705a9', 'f4444444-4444-4444-4444-444444444444', 7, 'home', '{"preferred_location": "home"}', 10, '2025-08-22T11:19:27.399454'),
('cfb4080e-9dc1-4dd6-98e4-6194114412b2', '7cd332ca-9582-4414-98c3-eea8654705a9', 'f4444444-4444-4444-4444-444444444444', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-22T11:19:27.399454'),
('eeb2bcf9-9887-4bee-9ed6-6b578b6f3e08', '7cd332ca-9582-4414-98c3-eea8654705a9', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-22T11:19:27.399454'),
('9094c1f6-fff4-4a46-ba1f-829f54dcb099', '7cd332ca-9582-4414-98c3-eea8654705a9', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-22T11:19:27.399454');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('558d4e69-f663-460a-aef4-5846a88c5ce4', '7cd332ca-9582-4414-98c3-eea8654705a9', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'maybe', '{"name": "Diana_4 Prince", "email": "diana.prince_4@embassy.gov", "phone": "(781) 555-1470"}', 70, 0.70, true, false, NULL, NULL, NULL);


-- Lead 21: Qualified - Rachel_5 Green
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('ea0f67c4-6dd1-4add-813c-2aad8e33376b', 'f4444444-4444-4444-4444-444444444444', 'fitlife_021_qualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-23T17:19:27.399510', '2025-08-23T17:37:27.399511', '2025-08-23T17:37:27.399511', 10, true, 88, 88, 'yes', 'qualified', 'Great news! You are an excellent candidate for our personal training programs. We will contact you within 24 hours to schedule your consultation.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.131', '{"device_type": "mobile", "completion_time": 50}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('08c696cf-e14d-475e-857c-0f8b125c4f66', 'ea0f67c4-6dd1-4add-813c-2aad8e33376b', 'instagram', 'social', 'transformation_stories', 'personal fitness', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('0e37f30b-148b-461e-bd69-645ec6a63f7b', 'ea0f67c4-6dd1-4add-813c-2aad8e33376b', 'f4444444-4444-4444-4444-444444444444', 1, 'Rachel_5 Green', '{"name": "Rachel_5 Green"}', 10, '2025-08-23T17:19:27.399510'),
('98e3e545-31da-4730-b4bc-a460260ac953', 'ea0f67c4-6dd1-4add-813c-2aad8e33376b', 'f4444444-4444-4444-4444-444444444444', 2, 'rachel.green_5@consulting.com', '{"email": "rachel.green_5@consulting.com"}', 10, '2025-08-23T17:19:27.399510'),
('bc730f3b-e8be-4d58-97d9-ca82939f45de', 'ea0f67c4-6dd1-4add-813c-2aad8e33376b', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-3691', '{"phone": "(617) 555-3691"}', 15, '2025-08-23T17:19:27.399510'),
('d05d757a-138a-483c-854a-3fa63829e80d', 'ea0f67c4-6dd1-4add-813c-2aad8e33376b', 'f4444444-4444-4444-4444-444444444444', 4, 'weight_loss', '{"fitness_goals": "weight_loss"}', 10, '2025-08-23T17:19:27.399510'),
('e7046686-340f-445e-a8bd-49cbe5f10f6a', 'ea0f67c4-6dd1-4add-813c-2aad8e33376b', 'f4444444-4444-4444-4444-444444444444', 5, 'beginner', '{"experience_level": "beginner"}', 10, '2025-08-23T17:19:27.399510'),
('f883892e-f08c-45fe-b0c6-fda2a4c90000', 'ea0f67c4-6dd1-4add-813c-2aad8e33376b', 'f4444444-4444-4444-4444-444444444444', 6, 'mornings', '{"availability": "mornings"}', 10, '2025-08-23T17:19:27.399510'),
('d3a03666-2738-4663-81d4-eccac805683c', 'ea0f67c4-6dd1-4add-813c-2aad8e33376b', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-23T17:19:27.399510'),
('675944b2-b236-4002-8eaa-93bd578840b7', 'ea0f67c4-6dd1-4add-813c-2aad8e33376b', 'f4444444-4444-4444-4444-444444444444', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-23T17:19:27.399510'),
('42a92489-b849-42f5-bf47-c424e07ca555', 'ea0f67c4-6dd1-4add-813c-2aad8e33376b', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-23T17:19:27.399510'),
('0471487e-271d-4661-99a1-555db0fdf279', 'ea0f67c4-6dd1-4add-813c-2aad8e33376b', 'f4444444-4444-4444-4444-444444444444', 10, 'asap', '{"timeline": "asap"}', 25, '2025-08-23T17:19:27.399510');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('898c4038-75a2-42e0-81db-0ed6f98daf96', 'ea0f67c4-6dd1-4add-813c-2aad8e33376b', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'qualified', '{"name": "Rachel_5 Green", "email": "rachel.green_5@consulting.com", "phone": "(617) 555-3691"}', 88, 0.88, true, false, NULL, NULL, NULL);


-- Lead 22: Qualified - Steve_5 Rogers
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('5d3062d2-8e91-4321-8546-2afba90ed97d', 'f4444444-4444-4444-4444-444444444444', 'fitlife_022_qualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-20T02:19:27.399566', '2025-08-20T03:00:27.399567', '2025-08-20T03:00:27.399567', 8, true, 92, 92, 'yes', 'qualified', 'Great news! You are an excellent candidate for our personal training programs. We will contact you within 24 hours to schedule your consultation.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.34', '{"device_type": "desktop", "completion_time": 50}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('8b8851c0-4524-4dbe-976b-115976114abb', '5d3062d2-8e91-4321-8546-2afba90ed97d', 'google', 'cpc', 'strength_training', 'weight loss trainer', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('bc49edc8-4f41-44ac-bd1a-124640e30bbf', '5d3062d2-8e91-4321-8546-2afba90ed97d', 'f4444444-4444-4444-4444-444444444444', 1, 'Steve_5 Rogers', '{"name": "Steve_5 Rogers"}', 10, '2025-08-20T02:19:27.399566'),
('f71e6383-12e5-44f8-9492-3ac44ba24758', '5d3062d2-8e91-4321-8546-2afba90ed97d', 'f4444444-4444-4444-4444-444444444444', 2, 'steve.rogers_5@military.gov', '{"email": "steve.rogers_5@military.gov"}', 10, '2025-08-20T02:19:27.399566'),
('d3cd4f73-8351-4869-8212-1071117f8aeb', '5d3062d2-8e91-4321-8546-2afba90ed97d', 'f4444444-4444-4444-4444-444444444444', 3, '(857) 555-7410', '{"phone": "(857) 555-7410"}', 15, '2025-08-20T02:19:27.399566'),
('ed82487c-9e03-4ca7-ab1e-233758f82959', '5d3062d2-8e91-4321-8546-2afba90ed97d', 'f4444444-4444-4444-4444-444444444444', 4, 'strength_building', '{"fitness_goals": "strength_building"}', 10, '2025-08-20T02:19:27.399566'),
('3271bb13-2794-48df-a857-5a22f8d6c0ec', '5d3062d2-8e91-4321-8546-2afba90ed97d', 'f4444444-4444-4444-4444-444444444444', 5, 'intermediate', '{"experience_level": "intermediate"}', 10, '2025-08-20T02:19:27.399566'),
('9a6056bf-85e4-4d4b-968f-b0fefbbc4f93', '5d3062d2-8e91-4321-8546-2afba90ed97d', 'f4444444-4444-4444-4444-444444444444', 6, 'evenings', '{"availability": "evenings"}', 10, '2025-08-20T02:19:27.399566'),
('811df909-ba39-4e8b-a356-a627cf8c1edf', '5d3062d2-8e91-4321-8546-2afba90ed97d', 'f4444444-4444-4444-4444-444444444444', 7, 'home', '{"preferred_location": "home"}', 10, '2025-08-20T02:19:27.399566'),
('0842263d-d6df-41d1-a06c-87e43ad0a851', '5d3062d2-8e91-4321-8546-2afba90ed97d', 'f4444444-4444-4444-4444-444444444444', 8, '$150_200', '{"budget": "$150_200"}', 25, '2025-08-20T02:19:27.399566'),
('51ea54df-4869-4dd3-8aeb-a1d1a6686f6d', '5d3062d2-8e91-4321-8546-2afba90ed97d', 'f4444444-4444-4444-4444-444444444444', 9, 'minor_injury', '{"health_conditions": "minor_injury"}', 10, '2025-08-20T02:19:27.399566'),
('09409419-cb8e-47f5-8140-1a228cdfd37f', '5d3062d2-8e91-4321-8546-2afba90ed97d', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-20T02:19:27.399566');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('66727d21-f397-4ed2-87d6-6ce52443bb8d', '5d3062d2-8e91-4321-8546-2afba90ed97d', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'qualified', '{"name": "Steve_5 Rogers", "email": "steve.rogers_5@military.gov", "phone": "(857) 555-7410"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 23: Maybe - Monica_5 Bellucci
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('ddf19c89-96e7-4adb-a3be-17b5c742a28c', 'f4444444-4444-4444-4444-444444444444', 'fitlife_023_maybe', 'a4444444-4444-4444-4444-444444444444', '2025-08-22T03:19:27.399625', '2025-08-22T03:50:27.399626', '2025-08-22T03:50:27.399626', 7, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest in FitLife! We are reviewing your fitness goals to create the best training plan. Expect to hear from us soon.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.103', '{"device_type": "mobile", "completion_time": 42}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('4f8e97bc-123b-4b8a-be7a-3f2ef375481f', 'ddf19c89-96e7-4adb-a3be-17b5c742a28c', 'facebook', 'social', 'group_fitness', 'strength training', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('b393a374-9613-4faa-a57e-24e98c67ae0f', 'ddf19c89-96e7-4adb-a3be-17b5c742a28c', 'f4444444-4444-4444-4444-444444444444', 1, 'Monica_5 Bellucci', '{"name": "Monica_5 Bellucci"}', 10, '2025-08-22T03:19:27.399625'),
('9bcac220-743c-4831-9c29-d749baf53d20', 'ddf19c89-96e7-4adb-a3be-17b5c742a28c', 'f4444444-4444-4444-4444-444444444444', 2, 'monica.bellucci_5@fashion.com', '{"email": "monica.bellucci_5@fashion.com"}', 10, '2025-08-22T03:19:27.399625'),
('577ab244-8e46-4bc1-87b7-4affbee4f5bc', 'ddf19c89-96e7-4adb-a3be-17b5c742a28c', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-8520', '{"phone": "(617) 555-8520"}', 15, '2025-08-22T03:19:27.399625'),
('b0e1a647-ff9e-40ad-813e-b5314b49f7c0', 'ddf19c89-96e7-4adb-a3be-17b5c742a28c', 'f4444444-4444-4444-4444-444444444444', 4, 'general_fitness', '{"fitness_goals": "general_fitness"}', 10, '2025-08-22T03:19:27.399625'),
('886f83f8-ff7a-43c4-8e78-8121cc8c843f', 'ddf19c89-96e7-4adb-a3be-17b5c742a28c', 'f4444444-4444-4444-4444-444444444444', 5, 'intermediate', '{"experience_level": "intermediate"}', 10, '2025-08-22T03:19:27.399625'),
('b2af384a-a159-469a-b626-64117fefcf53', 'ddf19c89-96e7-4adb-a3be-17b5c742a28c', 'f4444444-4444-4444-4444-444444444444', 6, 'flexible', '{"availability": "flexible"}', 10, '2025-08-22T03:19:27.399625'),
('f365940a-0a0a-407d-91ad-7f1461ea67a5', 'ddf19c89-96e7-4adb-a3be-17b5c742a28c', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-22T03:19:27.399625'),
('394952f1-2d48-4a07-b99e-0f541a709374', 'ddf19c89-96e7-4adb-a3be-17b5c742a28c', 'f4444444-4444-4444-4444-444444444444', 8, '$75_100', '{"budget": "$75_100"}', 15, '2025-08-22T03:19:27.399625'),
('152413c4-af62-47ab-b268-c736b5268be3', 'ddf19c89-96e7-4adb-a3be-17b5c742a28c', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-22T03:19:27.399625'),
('d4b2af30-6b2d-4997-98cd-abc60da1d8f8', 'ddf19c89-96e7-4adb-a3be-17b5c742a28c', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-22T03:19:27.399625');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('a210ce9c-b2a0-42d6-bfe6-0878e1ebb3fc', 'ddf19c89-96e7-4adb-a3be-17b5c742a28c', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'maybe', '{"name": "Monica_5 Bellucci", "email": "monica.bellucci_5@fashion.com", "phone": "(617) 555-8520"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 24: Unqualified - Peter_5 Parker
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('d635e984-e3bb-49a9-aeb7-75efc8439cc8', 'f4444444-4444-4444-4444-444444444444', 'fitlife_024_unqualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-12T12:19:27.399682', '2025-08-12T12:41:27.399683', '2025-08-12T12:41:27.399683', 8, true, 35, 35, 'no', 'qualified', 'Thank you for considering FitLife. While our current programs may not be the right fit, we wish you success in your fitness journey.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.171', '{"device_type": "mobile", "completion_time": 32}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('26bd1ea7-da5f-4ea9-b2b2-c1997bd55c6f', 'd635e984-e3bb-49a9-aeb7-75efc8439cc8', 'organic', 'search', 'student_fitness', 'personal fitness', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('59056908-c807-4fd6-b33a-c32f3ce6a283', 'd635e984-e3bb-49a9-aeb7-75efc8439cc8', 'f4444444-4444-4444-4444-444444444444', 1, 'Peter_5 Parker', '{"name": "Peter_5 Parker"}', 10, '2025-08-12T12:19:27.399682'),
('e8a1a167-efb8-496b-b03a-f81ed90aebe6', 'd635e984-e3bb-49a9-aeb7-75efc8439cc8', 'f4444444-4444-4444-4444-444444444444', 2, 'peter.parker_5@university.edu', '{"email": "peter.parker_5@university.edu"}', 10, '2025-08-12T12:19:27.399682'),
('0f441d64-2bbc-4c3e-afe9-e282d4bfe3e3', 'd635e984-e3bb-49a9-aeb7-75efc8439cc8', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-9630', '{"phone": "(617) 555-9630"}', 15, '2025-08-12T12:19:27.399682'),
('e6597af5-9e67-4bc2-9635-3e7c682931c2', 'd635e984-e3bb-49a9-aeb7-75efc8439cc8', 'f4444444-4444-4444-4444-444444444444', 4, 'athletic_performance', '{"fitness_goals": "athletic_performance"}', 10, '2025-08-12T12:19:27.399682'),
('10f31783-1443-497a-a90e-f27989424dd5', 'd635e984-e3bb-49a9-aeb7-75efc8439cc8', 'f4444444-4444-4444-4444-444444444444', 5, 'advanced', '{"experience_level": "advanced"}', 10, '2025-08-12T12:19:27.399682'),
('ba33517d-a759-4529-8a6f-d85dbc95454d', 'd635e984-e3bb-49a9-aeb7-75efc8439cc8', 'f4444444-4444-4444-4444-444444444444', 6, 'afternoons', '{"availability": "afternoons"}', 10, '2025-08-12T12:19:27.399682'),
('7a194d8e-149e-441f-b130-4868cd69b5dc', 'd635e984-e3bb-49a9-aeb7-75efc8439cc8', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-12T12:19:27.399682'),
('0f6bef55-e703-4856-8322-7a2bf65cdb9e', 'd635e984-e3bb-49a9-aeb7-75efc8439cc8', 'f4444444-4444-4444-4444-444444444444', 8, 'under_75', '{"budget": "under_75"}', 5, '2025-08-12T12:19:27.399682'),
('ed481c9b-776c-418a-9121-9580fd106c26', 'd635e984-e3bb-49a9-aeb7-75efc8439cc8', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-12T12:19:27.399682'),
('fe05b4fc-a7b0-4fc0-8292-ee50b2a54f8e', 'd635e984-e3bb-49a9-aeb7-75efc8439cc8', 'f4444444-4444-4444-4444-444444444444', 10, 'just_exploring', '{"timeline": "just_exploring"}', 0, '2025-08-12T12:19:27.399682');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('519cde78-17db-4f42-8053-883afcb20a25', 'd635e984-e3bb-49a9-aeb7-75efc8439cc8', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'unqualified', '{"name": "Peter_5 Parker", "email": "peter.parker_5@university.edu", "phone": "(617) 555-9630"}', 35, 0.35, false, false, NULL, NULL, NULL);


-- Lead 25: Maybe - Diana_5 Prince
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('de2a0110-9e7c-4a5d-80fc-52c53ac3e767', 'f4444444-4444-4444-4444-444444444444', 'fitlife_025_maybe', 'a4444444-4444-4444-4444-444444444444', '2025-08-19T02:19:27.399738', '2025-08-19T03:02:27.399739', '2025-08-19T03:02:27.399739', 8, true, 70, 70, 'maybe', 'qualified', 'Thank you for your interest in FitLife! We are reviewing your fitness goals to create the best training plan. Expect to hear from us soon.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.55', '{"device_type": "desktop", "completion_time": 11}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('53b5d76c-b6b1-4ca7-a369-edf26d36704f', 'de2a0110-9e7c-4a5d-80fc-52c53ac3e767', 'referral', 'referral', 'specialized_training', 'fitness coach', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('87e05734-ec1c-4a83-a7b2-ef0eac5bc526', 'de2a0110-9e7c-4a5d-80fc-52c53ac3e767', 'f4444444-4444-4444-4444-444444444444', 1, 'Diana_5 Prince', '{"name": "Diana_5 Prince"}', 10, '2025-08-19T02:19:27.399738'),
('c64a19e7-3c72-402e-b463-0d23049e54a0', 'de2a0110-9e7c-4a5d-80fc-52c53ac3e767', 'f4444444-4444-4444-4444-444444444444', 2, 'diana.prince_5@embassy.gov', '{"email": "diana.prince_5@embassy.gov"}', 10, '2025-08-19T02:19:27.399738'),
('9881899c-3bcf-41e3-b42b-570a1e1aef8d', 'de2a0110-9e7c-4a5d-80fc-52c53ac3e767', 'f4444444-4444-4444-4444-444444444444', 3, '(781) 555-1470', '{"phone": "(781) 555-1470"}', 15, '2025-08-19T02:19:27.399738'),
('3da3035c-f582-4a23-aa75-2573a78169bd', 'de2a0110-9e7c-4a5d-80fc-52c53ac3e767', 'f4444444-4444-4444-4444-444444444444', 4, 'martial_arts', '{"fitness_goals": "martial_arts"}', 10, '2025-08-19T02:19:27.399738'),
('46ba0e00-90c0-4f36-832b-3a9f5c8a90da', 'de2a0110-9e7c-4a5d-80fc-52c53ac3e767', 'f4444444-4444-4444-4444-444444444444', 5, 'advanced', '{"experience_level": "advanced"}', 10, '2025-08-19T02:19:27.399738'),
('2e51990d-bfc8-4b31-9516-01755d757d04', 'de2a0110-9e7c-4a5d-80fc-52c53ac3e767', 'f4444444-4444-4444-4444-444444444444', 6, 'evenings', '{"availability": "evenings"}', 10, '2025-08-19T02:19:27.399738'),
('7386c69c-0747-4839-9b8d-a8a524bfc5ea', 'de2a0110-9e7c-4a5d-80fc-52c53ac3e767', 'f4444444-4444-4444-4444-444444444444', 7, 'home', '{"preferred_location": "home"}', 10, '2025-08-19T02:19:27.399738'),
('0f2527d4-85ca-4cfa-a3ea-51c14de6cbc3', 'de2a0110-9e7c-4a5d-80fc-52c53ac3e767', 'f4444444-4444-4444-4444-444444444444', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-19T02:19:27.399738'),
('4ebcb1fb-f998-4292-a6a5-0948f3e6530f', 'de2a0110-9e7c-4a5d-80fc-52c53ac3e767', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-19T02:19:27.399738'),
('af517bdf-df78-4f7b-a44b-2d1533d9e8da', 'de2a0110-9e7c-4a5d-80fc-52c53ac3e767', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-19T02:19:27.399738');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('2eeda55a-471b-4705-af32-3928abe9a923', 'de2a0110-9e7c-4a5d-80fc-52c53ac3e767', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'maybe', '{"name": "Diana_5 Prince", "email": "diana.prince_5@embassy.gov", "phone": "(781) 555-1470"}', 70, 0.70, true, false, NULL, NULL, NULL);


-- Lead 26: Qualified - Rachel_6 Green
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('d6c9b3c0-6fb4-4efd-9226-ed60c8225256', 'f4444444-4444-4444-4444-444444444444', 'fitlife_026_qualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-14T17:19:27.399795', '2025-08-14T18:00:27.399795', '2025-08-14T18:00:27.399795', 10, true, 88, 88, 'yes', 'qualified', 'Great news! You are an excellent candidate for our personal training programs. We will contact you within 24 hours to schedule your consultation.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.247', '{"device_type": "mobile", "completion_time": 25}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('943e7231-a9d4-4a2a-9468-a175b35cc05d', 'd6c9b3c0-6fb4-4efd-9226-ed60c8225256', 'instagram', 'social', 'transformation_stories', 'personal trainer boston', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('e34ab1b6-6128-471e-9715-41dddc821627', 'd6c9b3c0-6fb4-4efd-9226-ed60c8225256', 'f4444444-4444-4444-4444-444444444444', 1, 'Rachel_6 Green', '{"name": "Rachel_6 Green"}', 10, '2025-08-14T17:19:27.399795'),
('0d4840d7-801e-48bf-b6b3-b13e077e164d', 'd6c9b3c0-6fb4-4efd-9226-ed60c8225256', 'f4444444-4444-4444-4444-444444444444', 2, 'rachel.green_6@consulting.com', '{"email": "rachel.green_6@consulting.com"}', 10, '2025-08-14T17:19:27.399795'),
('e058599a-9eff-4595-bd75-5fe35b95f414', 'd6c9b3c0-6fb4-4efd-9226-ed60c8225256', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-3691', '{"phone": "(617) 555-3691"}', 15, '2025-08-14T17:19:27.399795'),
('615e6dfb-21d0-4f93-af9f-4031a7e37d9d', 'd6c9b3c0-6fb4-4efd-9226-ed60c8225256', 'f4444444-4444-4444-4444-444444444444', 4, 'weight_loss', '{"fitness_goals": "weight_loss"}', 10, '2025-08-14T17:19:27.399795'),
('b28f9808-4e2c-4ddc-ab3b-48d2bf21364b', 'd6c9b3c0-6fb4-4efd-9226-ed60c8225256', 'f4444444-4444-4444-4444-444444444444', 5, 'beginner', '{"experience_level": "beginner"}', 10, '2025-08-14T17:19:27.399795'),
('a68e95ca-d583-4a7a-bd7e-5d9f457dd43d', 'd6c9b3c0-6fb4-4efd-9226-ed60c8225256', 'f4444444-4444-4444-4444-444444444444', 6, 'mornings', '{"availability": "mornings"}', 10, '2025-08-14T17:19:27.399795'),
('a155466d-1eab-4cca-87e9-a752424d41aa', 'd6c9b3c0-6fb4-4efd-9226-ed60c8225256', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-14T17:19:27.399795'),
('6a2959a3-6eed-43b8-8840-69f525bfce40', 'd6c9b3c0-6fb4-4efd-9226-ed60c8225256', 'f4444444-4444-4444-4444-444444444444', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-14T17:19:27.399795'),
('df951233-0b06-46b7-9acd-8a25e23802a3', 'd6c9b3c0-6fb4-4efd-9226-ed60c8225256', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-14T17:19:27.399795'),
('b2bf9289-5753-4128-a89b-82ee0fe4e0ac', 'd6c9b3c0-6fb4-4efd-9226-ed60c8225256', 'f4444444-4444-4444-4444-444444444444', 10, 'asap', '{"timeline": "asap"}', 25, '2025-08-14T17:19:27.399795');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('7b1669bf-afb4-4e6d-9463-05ad3c15558a', 'd6c9b3c0-6fb4-4efd-9226-ed60c8225256', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'qualified', '{"name": "Rachel_6 Green", "email": "rachel.green_6@consulting.com", "phone": "(617) 555-3691"}', 88, 0.88, true, false, NULL, NULL, NULL);


-- Lead 27: Qualified - Steve_6 Rogers
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('35ba5174-7516-4450-a4f0-6f07bb82d2dd', 'f4444444-4444-4444-4444-444444444444', 'fitlife_027_qualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-15T19:19:27.399854', '2025-08-15T19:55:27.399855', '2025-08-15T19:55:27.399855', 7, true, 92, 92, 'yes', 'qualified', 'Great news! You are an excellent candidate for our personal training programs. We will contact you within 24 hours to schedule your consultation.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.248', '{"device_type": "desktop", "completion_time": 42}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('f4cd59f0-0b0f-449a-b7f9-fcb6b8545f81', '35ba5174-7516-4450-a4f0-6f07bb82d2dd', 'google', 'cpc', 'strength_training', 'weight loss trainer', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('dfa6ea47-1582-48d5-9c5a-0bae173201ff', '35ba5174-7516-4450-a4f0-6f07bb82d2dd', 'f4444444-4444-4444-4444-444444444444', 1, 'Steve_6 Rogers', '{"name": "Steve_6 Rogers"}', 10, '2025-08-15T19:19:27.399854'),
('7ff7ff0d-8cac-4cb8-8519-6ecda58c66fb', '35ba5174-7516-4450-a4f0-6f07bb82d2dd', 'f4444444-4444-4444-4444-444444444444', 2, 'steve.rogers_6@military.gov', '{"email": "steve.rogers_6@military.gov"}', 10, '2025-08-15T19:19:27.399854'),
('e452d3ee-a4ec-4933-a0bf-69366a5ed5e6', '35ba5174-7516-4450-a4f0-6f07bb82d2dd', 'f4444444-4444-4444-4444-444444444444', 3, '(857) 555-7410', '{"phone": "(857) 555-7410"}', 15, '2025-08-15T19:19:27.399854'),
('952b4127-282d-4770-8ed0-1a46d78e0a86', '35ba5174-7516-4450-a4f0-6f07bb82d2dd', 'f4444444-4444-4444-4444-444444444444', 4, 'strength_building', '{"fitness_goals": "strength_building"}', 10, '2025-08-15T19:19:27.399854'),
('89df6088-c1e7-45a8-8974-8b54c0d3aa04', '35ba5174-7516-4450-a4f0-6f07bb82d2dd', 'f4444444-4444-4444-4444-444444444444', 5, 'intermediate', '{"experience_level": "intermediate"}', 10, '2025-08-15T19:19:27.399854'),
('c248b788-2666-47bd-8749-62bd9aa7f5c1', '35ba5174-7516-4450-a4f0-6f07bb82d2dd', 'f4444444-4444-4444-4444-444444444444', 6, 'evenings', '{"availability": "evenings"}', 10, '2025-08-15T19:19:27.399854'),
('a150d294-0ea3-45d2-93be-708c45bb75db', '35ba5174-7516-4450-a4f0-6f07bb82d2dd', 'f4444444-4444-4444-4444-444444444444', 7, 'home', '{"preferred_location": "home"}', 10, '2025-08-15T19:19:27.399854'),
('64d75d5e-e8bf-4db5-a64d-13176948ae3a', '35ba5174-7516-4450-a4f0-6f07bb82d2dd', 'f4444444-4444-4444-4444-444444444444', 8, '$150_200', '{"budget": "$150_200"}', 25, '2025-08-15T19:19:27.399854'),
('0cd04843-e4d5-4a33-828d-f23de9ef4bbf', '35ba5174-7516-4450-a4f0-6f07bb82d2dd', 'f4444444-4444-4444-4444-444444444444', 9, 'minor_injury', '{"health_conditions": "minor_injury"}', 10, '2025-08-15T19:19:27.399854'),
('cc47637f-273a-447b-8e9b-83b5d76bcda0', '35ba5174-7516-4450-a4f0-6f07bb82d2dd', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-15T19:19:27.399854');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('e6c47858-eb02-4504-b45f-8dabf1062e69', '35ba5174-7516-4450-a4f0-6f07bb82d2dd', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'qualified', '{"name": "Steve_6 Rogers", "email": "steve.rogers_6@military.gov", "phone": "(857) 555-7410"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 28: Maybe - Monica_6 Bellucci
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('e1722246-6656-4862-a9e0-079072065124', 'f4444444-4444-4444-4444-444444444444', 'fitlife_028_maybe', 'a4444444-4444-4444-4444-444444444444', '2025-08-23T19:19:27.399911', '2025-08-23T19:53:27.399912', '2025-08-23T19:53:27.399912', 9, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest in FitLife! We are reviewing your fitness goals to create the best training plan. Expect to hear from us soon.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.215', '{"device_type": "mobile", "completion_time": 49}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('b2228327-33be-4acf-ad3b-20f3c1927194', 'e1722246-6656-4862-a9e0-079072065124', 'facebook', 'social', 'group_fitness', 'strength training', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('71f6350d-2c79-4b0c-a4e1-36a50c7253d9', 'e1722246-6656-4862-a9e0-079072065124', 'f4444444-4444-4444-4444-444444444444', 1, 'Monica_6 Bellucci', '{"name": "Monica_6 Bellucci"}', 10, '2025-08-23T19:19:27.399911'),
('5b3dc19d-d703-4fa3-bd4c-04259ce653b5', 'e1722246-6656-4862-a9e0-079072065124', 'f4444444-4444-4444-4444-444444444444', 2, 'monica.bellucci_6@fashion.com', '{"email": "monica.bellucci_6@fashion.com"}', 10, '2025-08-23T19:19:27.399911'),
('f2687027-baad-40f6-a6b5-db5ef466a263', 'e1722246-6656-4862-a9e0-079072065124', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-8520', '{"phone": "(617) 555-8520"}', 15, '2025-08-23T19:19:27.399911'),
('eea6be31-233e-4513-87a6-4eef17ea0811', 'e1722246-6656-4862-a9e0-079072065124', 'f4444444-4444-4444-4444-444444444444', 4, 'general_fitness', '{"fitness_goals": "general_fitness"}', 10, '2025-08-23T19:19:27.399911'),
('694615e6-84d7-43aa-8e42-b61a736672bb', 'e1722246-6656-4862-a9e0-079072065124', 'f4444444-4444-4444-4444-444444444444', 5, 'intermediate', '{"experience_level": "intermediate"}', 10, '2025-08-23T19:19:27.399911'),
('7699d104-bdfe-4986-9675-09bea67a3445', 'e1722246-6656-4862-a9e0-079072065124', 'f4444444-4444-4444-4444-444444444444', 6, 'flexible', '{"availability": "flexible"}', 10, '2025-08-23T19:19:27.399911'),
('04da91b8-9e50-4365-b9c7-920b4136078c', 'e1722246-6656-4862-a9e0-079072065124', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-23T19:19:27.399911'),
('3d8e4f97-abdd-4566-9a37-6fc60b66bfcb', 'e1722246-6656-4862-a9e0-079072065124', 'f4444444-4444-4444-4444-444444444444', 8, '$75_100', '{"budget": "$75_100"}', 15, '2025-08-23T19:19:27.399911'),
('19a0dab2-a3a9-44ca-ade4-139b67f927fe', 'e1722246-6656-4862-a9e0-079072065124', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-23T19:19:27.399911'),
('893361d5-8c5d-449c-8079-5dcbbb4fcef3', 'e1722246-6656-4862-a9e0-079072065124', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-23T19:19:27.399911');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('0fb67789-c51d-412a-889d-ec34a63b38dd', 'e1722246-6656-4862-a9e0-079072065124', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'maybe', '{"name": "Monica_6 Bellucci", "email": "monica.bellucci_6@fashion.com", "phone": "(617) 555-8520"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 29: Unqualified - Peter_6 Parker
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('bb9cd304-db54-4766-bfc3-a70eff80985b', 'f4444444-4444-4444-4444-444444444444', 'fitlife_029_unqualified', 'a4444444-4444-4444-4444-444444444444', '2025-08-10T18:19:27.399968', '2025-08-10T18:54:27.399969', '2025-08-10T18:54:27.399969', 7, true, 35, 35, 'no', 'qualified', 'Thank you for considering FitLife. While our current programs may not be the right fit, we wish you success in your fitness journey.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.58', '{"device_type": "mobile", "completion_time": 48}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('c7e15be3-0e49-4468-bd01-154b2b4b5333', 'bb9cd304-db54-4766-bfc3-a70eff80985b', 'organic', 'search', 'student_fitness', 'personal fitness', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('d08f8bba-8982-4315-b2e4-161f717feb5a', 'bb9cd304-db54-4766-bfc3-a70eff80985b', 'f4444444-4444-4444-4444-444444444444', 1, 'Peter_6 Parker', '{"name": "Peter_6 Parker"}', 10, '2025-08-10T18:19:27.399968'),
('864318b7-a7e9-4c49-8511-65fb435b2523', 'bb9cd304-db54-4766-bfc3-a70eff80985b', 'f4444444-4444-4444-4444-444444444444', 2, 'peter.parker_6@university.edu', '{"email": "peter.parker_6@university.edu"}', 10, '2025-08-10T18:19:27.399968'),
('b2f8bd5c-afee-4f9b-aec2-641a96a99260', 'bb9cd304-db54-4766-bfc3-a70eff80985b', 'f4444444-4444-4444-4444-444444444444', 3, '(617) 555-9630', '{"phone": "(617) 555-9630"}', 15, '2025-08-10T18:19:27.399968'),
('29eff566-05a6-4621-a6f7-b048bd68a59a', 'bb9cd304-db54-4766-bfc3-a70eff80985b', 'f4444444-4444-4444-4444-444444444444', 4, 'athletic_performance', '{"fitness_goals": "athletic_performance"}', 10, '2025-08-10T18:19:27.399968'),
('e1d8d6d4-8127-4889-9c9a-48886950d278', 'bb9cd304-db54-4766-bfc3-a70eff80985b', 'f4444444-4444-4444-4444-444444444444', 5, 'advanced', '{"experience_level": "advanced"}', 10, '2025-08-10T18:19:27.399968'),
('313bdc36-65f9-4ae7-be2d-da73895e8e5d', 'bb9cd304-db54-4766-bfc3-a70eff80985b', 'f4444444-4444-4444-4444-444444444444', 6, 'afternoons', '{"availability": "afternoons"}', 10, '2025-08-10T18:19:27.399968'),
('1873f19a-6268-499c-aa86-15c4f39e75b8', 'bb9cd304-db54-4766-bfc3-a70eff80985b', 'f4444444-4444-4444-4444-444444444444', 7, 'gym', '{"preferred_location": "gym"}', 10, '2025-08-10T18:19:27.399968'),
('b5025f93-17f0-4c0f-9bcf-dfa4aa5dade0', 'bb9cd304-db54-4766-bfc3-a70eff80985b', 'f4444444-4444-4444-4444-444444444444', 8, 'under_75', '{"budget": "under_75"}', 5, '2025-08-10T18:19:27.399968'),
('77b99ab1-9a9d-4da2-b9e1-59b2742ff591', 'bb9cd304-db54-4766-bfc3-a70eff80985b', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-10T18:19:27.399968'),
('c93849a8-483b-4a3b-9494-73e2e47093d0', 'bb9cd304-db54-4766-bfc3-a70eff80985b', 'f4444444-4444-4444-4444-444444444444', 10, 'just_exploring', '{"timeline": "just_exploring"}', 0, '2025-08-10T18:19:27.399968');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('6123838c-29e1-442b-bcd7-eba062e5cd78', 'bb9cd304-db54-4766-bfc3-a70eff80985b', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'unqualified', '{"name": "Peter_6 Parker", "email": "peter.parker_6@university.edu", "phone": "(617) 555-9630"}', 35, 0.35, false, false, NULL, NULL, NULL);


-- Lead 30: Maybe - Diana_6 Prince
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('278fe630-57bc-4e42-a452-84241596e5a5', 'f4444444-4444-4444-4444-444444444444', 'fitlife_030_maybe', 'a4444444-4444-4444-4444-444444444444', '2025-08-21T14:19:27.400024', '2025-08-21T14:50:27.400025', '2025-08-21T14:50:27.400025', 7, true, 70, 70, 'maybe', 'qualified', 'Thank you for your interest in FitLife! We are reviewing your fitness goals to create the best training plan. Expect to hear from us soon.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.142', '{"device_type": "desktop", "completion_time": 31}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('aa0c367e-5ff7-4686-a855-17402bc15368', '278fe630-57bc-4e42-a452-84241596e5a5', 'referral', 'referral', 'specialized_training', 'personal trainer boston', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('854a2c50-f0af-41c5-8bd1-34ca1c30aa3b', '278fe630-57bc-4e42-a452-84241596e5a5', 'f4444444-4444-4444-4444-444444444444', 1, 'Diana_6 Prince', '{"name": "Diana_6 Prince"}', 10, '2025-08-21T14:19:27.400024'),
('c75a077e-3e79-4d79-b0b4-404995870d6f', '278fe630-57bc-4e42-a452-84241596e5a5', 'f4444444-4444-4444-4444-444444444444', 2, 'diana.prince_6@embassy.gov', '{"email": "diana.prince_6@embassy.gov"}', 10, '2025-08-21T14:19:27.400024'),
('5fde6299-9ab0-400f-9bad-efddf7dca0e9', '278fe630-57bc-4e42-a452-84241596e5a5', 'f4444444-4444-4444-4444-444444444444', 3, '(781) 555-1470', '{"phone": "(781) 555-1470"}', 15, '2025-08-21T14:19:27.400024'),
('31a8d052-3aa0-4fe3-b3a3-166a8101070c', '278fe630-57bc-4e42-a452-84241596e5a5', 'f4444444-4444-4444-4444-444444444444', 4, 'martial_arts', '{"fitness_goals": "martial_arts"}', 10, '2025-08-21T14:19:27.400024'),
('20373854-fa32-453d-8a03-16cd36045c0b', '278fe630-57bc-4e42-a452-84241596e5a5', 'f4444444-4444-4444-4444-444444444444', 5, 'advanced', '{"experience_level": "advanced"}', 10, '2025-08-21T14:19:27.400024'),
('174fec3e-f27b-451b-bb89-b49ca21e4471', '278fe630-57bc-4e42-a452-84241596e5a5', 'f4444444-4444-4444-4444-444444444444', 6, 'evenings', '{"availability": "evenings"}', 10, '2025-08-21T14:19:27.400024'),
('20e26c1c-1838-4bf2-af19-1ad9641f9e38', '278fe630-57bc-4e42-a452-84241596e5a5', 'f4444444-4444-4444-4444-444444444444', 7, 'home', '{"preferred_location": "home"}', 10, '2025-08-21T14:19:27.400024'),
('3a23d490-df11-481e-8c21-45b827bd81ea', '278fe630-57bc-4e42-a452-84241596e5a5', 'f4444444-4444-4444-4444-444444444444', 8, '$100_150', '{"budget": "$100_150"}', 20, '2025-08-21T14:19:27.400024'),
('0f2e8a21-1780-4eca-b342-b296d3b66cf9', '278fe630-57bc-4e42-a452-84241596e5a5', 'f4444444-4444-4444-4444-444444444444', 9, 'none', '{"health_conditions": "none"}', 10, '2025-08-21T14:19:27.400024'),
('ca256452-84f0-44aa-b231-c4ce694eb922', '278fe630-57bc-4e42-a452-84241596e5a5', 'f4444444-4444-4444-4444-444444444444', 10, 'within_month', '{"timeline": "within_month"}', 20, '2025-08-21T14:19:27.400024');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('2edd8e1d-c473-4e97-8614-879429c6573c', '278fe630-57bc-4e42-a452-84241596e5a5', 'a4444444-4444-4444-4444-444444444444', 'f4444444-4444-4444-4444-444444444444', 'maybe', '{"name": "Diana_6 Prince", "email": "diana.prince_6@embassy.gov", "phone": "(781) 555-1470"}', 70, 0.70, true, false, NULL, NULL, NULL);


SELECT 'Generated 30 realistic lead sessions for fitlife!' as status;

