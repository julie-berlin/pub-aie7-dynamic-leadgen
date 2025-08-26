-- Test Data for Metro Realty Group (Real Estate)
-- Generated 30 realistic lead sessions with complete tracking and outcomes
-- Client: metro_realty | Form: f2222222-2222-2222-2222-222222222222 | Generated: 2025-08-24T20:19:21



-- Lead 1: Qualified - Jessica Chen
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('0c69f103-1e60-4915-9c0a-e2470a7f93af', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_001_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-16T22:19:21.045009', '2025-08-16T22:58:21.045013', '2025-08-16T22:58:21.045013', 6, true, 90, 90, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.219', '{"device_type": "desktop", "completion_time": 24}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('5d508026-2879-46b1-acbb-82f8cb941e83', '0c69f103-1e60-4915-9c0a-e2470a7f93af', 'google', 'cpc', 'luxury_homes_boston', 'property specialist', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('6eb52fc3-9637-4402-a9e0-2b13bf3f2c91', '0c69f103-1e60-4915-9c0a-e2470a7f93af', 'f2222222-2222-2222-2222-222222222222', 1, 'Jessica Chen', '{"name": "Jessica Chen"}', 10, '2025-08-16T22:19:21.045009'),
('5f43a49d-19e1-4729-8274-80d81bbbd8e4', '0c69f103-1e60-4915-9c0a-e2470a7f93af', 'f2222222-2222-2222-2222-222222222222', 2, 'jessica.chen@techcorp.com', '{"email": "jessica.chen@techcorp.com"}', 10, '2025-08-16T22:19:21.045009'),
('cb49190c-8827-4399-80cd-8aba2be1e39e', '0c69f103-1e60-4915-9c0a-e2470a7f93af', 'f2222222-2222-2222-2222-222222222222', 3, '(617) 555-1234', '{"phone": "(617) 555-1234"}', 15, '2025-08-16T22:19:21.045009'),
('64992e31-f3fc-4524-bd59-67a6ce5d98c4', '0c69f103-1e60-4915-9c0a-e2470a7f93af', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-16T22:19:21.045009'),
('bec71efa-fb13-4d33-b05f-0110a09c1c1c', '0c69f103-1e60-4915-9c0a-e2470a7f93af', 'f2222222-2222-2222-2222-222222222222', 5, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-16T22:19:21.045009'),
('a835aad9-9d34-4add-a5a6-5095a92fe298', '0c69f103-1e60-4915-9c0a-e2470a7f93af', 'f2222222-2222-2222-2222-222222222222', 6, 'pre_approved', '{"mortgage_status": "pre_approved"}', 20, '2025-08-16T22:19:21.045009'),
('1a4f4539-7a49-4dfb-bc4b-3cee473613eb', '0c69f103-1e60-4915-9c0a-e2470a7f93af', 'f2222222-2222-2222-2222-222222222222', 7, '$500k_plus', '{"price_range": "$500k_plus"}', 20, '2025-08-16T22:19:21.045009'),
('e1e2589d-7a70-4b74-b8ee-daf4a7221797', '0c69f103-1e60-4915-9c0a-e2470a7f93af', 'f2222222-2222-2222-2222-222222222222', 8, 'boston_cambridge', '{"areas": "boston_cambridge"}', 10, '2025-08-16T22:19:21.045009'),
('f90389d3-54dc-4131-9014-e78f3e45ed65', '0c69f103-1e60-4915-9c0a-e2470a7f93af', 'f2222222-2222-2222-2222-222222222222', 9, 'no', '{"first_time_buyer": "no"}', 10, '2025-08-16T22:19:21.045009'),
('96c01bd5-bcf8-4239-8970-6ee8189d1e3d', '0c69f103-1e60-4915-9c0a-e2470a7f93af', 'f2222222-2222-2222-2222-222222222222', 10, '3_bedrooms', '{"bedrooms": "3_bedrooms"}', 10, '2025-08-16T22:19:21.045009'),
('c83d171f-04c8-41f6-9973-b1cb4baf1da2', '0c69f103-1e60-4915-9c0a-e2470a7f93af', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-16T22:19:21.045009'),
('db992ba2-10e8-4a86-923a-9fd9134dffb4', '0c69f103-1e60-4915-9c0a-e2470a7f93af', 'f2222222-2222-2222-2222-222222222222', 12, 'high', '{"urgency": "high"}', 10, '2025-08-16T22:19:21.045009');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('5924e9c3-9adf-4079-a144-86b52f5207ce', '0c69f103-1e60-4915-9c0a-e2470a7f93af', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Jessica Chen", "email": "jessica.chen@techcorp.com", "phone": "(617) 555-1234"}', 90, 0.90, true, false, NULL, NULL, NULL);


-- Lead 2: Qualified - Mark Thompson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('592164d0-aab9-445f-874f-c9c3c7e28d4b', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_002_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-20T10:19:21.045315', '2025-08-20T10:36:21.045317', '2025-08-20T10:36:21.045317', 11, true, 85, 85, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.83', '{"device_type": "mobile", "completion_time": 22}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('b2a6ec52-33f1-4744-a5eb-0d37aca6ac7a', '592164d0-aab9-445f-874f-c9c3c7e28d4b', 'facebook', 'social', 'first_time_buyers', 'boston realtor', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('40a40bbd-6653-4456-8da5-da0e54eb5d37', '592164d0-aab9-445f-874f-c9c3c7e28d4b', 'f2222222-2222-2222-2222-222222222222', 1, 'Mark Thompson', '{"name": "Mark Thompson"}', 10, '2025-08-20T10:19:21.045315'),
('782ceb47-df95-4337-9793-b71e071bc851', '592164d0-aab9-445f-874f-c9c3c7e28d4b', 'f2222222-2222-2222-2222-222222222222', 2, 'mark.thompson@startup.io', '{"email": "mark.thompson@startup.io"}', 10, '2025-08-20T10:19:21.045315'),
('1a69adbb-d8c7-4621-8997-4eb4c80eab62', '592164d0-aab9-445f-874f-c9c3c7e28d4b', 'f2222222-2222-2222-2222-222222222222', 3, '(857) 555-5678', '{"phone": "(857) 555-5678"}', 15, '2025-08-20T10:19:21.045315'),
('04461375-7b4d-4900-8809-463b91ec5027', '592164d0-aab9-445f-874f-c9c3c7e28d4b', 'f2222222-2222-2222-2222-222222222222', 4, 'both', '{"buy_or_sell": "both"}', 25, '2025-08-20T10:19:21.045315'),
('aaf9ed10-95f8-4793-9671-f2e076457b58', '592164d0-aab9-445f-874f-c9c3c7e28d4b', 'f2222222-2222-2222-2222-222222222222', 5, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-20T10:19:21.045315'),
('3d71c80a-db2f-4359-a3d8-48cef8e3d999', '592164d0-aab9-445f-874f-c9c3c7e28d4b', 'f2222222-2222-2222-2222-222222222222', 6, 'in_process', '{"mortgage_status": "in_process"}', 15, '2025-08-20T10:19:21.045315'),
('49469199-bdf3-493a-9dea-4e119c9db0fa', '592164d0-aab9-445f-874f-c9c3c7e28d4b', 'f2222222-2222-2222-2222-222222222222', 7, '$300k_500k', '{"price_range": "$300k_500k"}', 25, '2025-08-20T10:19:21.045315'),
('3e6e2276-720c-4b9d-8bb5-26689658ee92', '592164d0-aab9-445f-874f-c9c3c7e28d4b', 'f2222222-2222-2222-2222-222222222222', 8, 'brookline_newton', '{"areas": "brookline_newton"}', 10, '2025-08-20T10:19:21.045315'),
('14e886b0-bdb1-437f-9620-d894be45f915', '592164d0-aab9-445f-874f-c9c3c7e28d4b', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-20T10:19:21.045315'),
('d144fd87-f2d0-4ce0-8394-00cfe8893390', '592164d0-aab9-445f-874f-c9c3c7e28d4b', 'f2222222-2222-2222-2222-222222222222', 10, '2_bedrooms', '{"bedrooms": "2_bedrooms"}', 10, '2025-08-20T10:19:21.045315'),
('c4680e4d-6b52-43cc-a954-a15154ca091c', '592164d0-aab9-445f-874f-c9c3c7e28d4b', 'f2222222-2222-2222-2222-222222222222', 11, 'yes', '{"worked_with_realtor": "yes"}', 10, '2025-08-20T10:19:21.045315'),
('db3a4f91-b5f6-4165-b257-3ed6ca2c5496', '592164d0-aab9-445f-874f-c9c3c7e28d4b', 'f2222222-2222-2222-2222-222222222222', 12, 'medium', '{"urgency": "medium"}', 10, '2025-08-20T10:19:21.045315');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('3addc71b-f967-42db-839b-295587019d42', '592164d0-aab9-445f-874f-c9c3c7e28d4b', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Mark Thompson", "email": "mark.thompson@startup.io", "phone": "(857) 555-5678"}', 85, 0.85, true, false, NULL, NULL, NULL);


-- Lead 3: Qualified - Amanda Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_003_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-23T09:19:21.045393', '2025-08-23T09:34:21.045394', '2025-08-23T09:34:21.045394', 12, true, 92, 92, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.211', '{"device_type": "desktop", "completion_time": 37}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('fce7bd8c-e171-4bce-8cc5-e55684265def', '8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'referral', 'referral', 'luxury_sellers', 'home buying agent', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('6593e021-7702-4f51-a69e-c0fc2a4075af', '8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'f2222222-2222-2222-2222-222222222222', 1, 'Amanda Rodriguez', '{"name": "Amanda Rodriguez"}', 10, '2025-08-23T09:19:21.045393'),
('cac20532-bbba-49f4-ba83-c1ed9575577a', '8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'f2222222-2222-2222-2222-222222222222', 2, 'arodriguez@lawfirm.com', '{"email": "arodriguez@lawfirm.com"}', 10, '2025-08-23T09:19:21.045393'),
('660e1383-3cce-43fc-9147-4291574b9426', '8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'f2222222-2222-2222-2222-222222222222', 3, '(617) 555-9012', '{"phone": "(617) 555-9012"}', 15, '2025-08-23T09:19:21.045393'),
('f251d249-3fd6-4265-b6ec-dedc2a4cba2f', '8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'f2222222-2222-2222-2222-222222222222', 4, 'sell', '{"buy_or_sell": "sell"}', 20, '2025-08-23T09:19:21.045393'),
('9b96f44a-9360-49ac-b40a-72120e4ca1a2', '8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'f2222222-2222-2222-2222-222222222222', 5, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-23T09:19:21.045393'),
('a973c643-c92c-4e48-b1fc-f6bede365d7b', '8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'f2222222-2222-2222-2222-222222222222', 6, 'cash', '{"mortgage_status": "cash"}', 25, '2025-08-23T09:19:21.045393'),
('5b6f999e-bcb3-4afe-aeb0-0834bd54ddba', '8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'f2222222-2222-2222-2222-222222222222', 7, '$500k_plus', '{"price_range": "$500k_plus"}', 20, '2025-08-23T09:19:21.045393'),
('b39adefd-0114-4b12-b3ba-b992a39d7a3a', '8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'f2222222-2222-2222-2222-222222222222', 8, 'boston_cambridge', '{"areas": "boston_cambridge"}', 10, '2025-08-23T09:19:21.045393'),
('0a28396f-8295-43ce-a914-4bc130cd9d42', '8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'f2222222-2222-2222-2222-222222222222', 9, 'no', '{"first_time_buyer": "no"}', 10, '2025-08-23T09:19:21.045393'),
('7ad6c9c1-1539-42ff-b82b-052fdd55bb39', '8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'f2222222-2222-2222-2222-222222222222', 10, '4_bedrooms', '{"bedrooms": "4_bedrooms"}', 10, '2025-08-23T09:19:21.045393'),
('a97790c6-fd97-46f3-b9c9-76bcbce82662', '8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-23T09:19:21.045393'),
('97926888-9e46-472b-837c-155b1df87754', '8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'f2222222-2222-2222-2222-222222222222', 12, 'high', '{"urgency": "high"}', 10, '2025-08-23T09:19:21.045393');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('010f8d57-4207-4523-8d4a-3c0607a5cdc0', '8d8a0e77-31e0-4d2d-b0bb-0540bffb054e', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Amanda Rodriguez", "email": "arodriguez@lawfirm.com", "phone": "(617) 555-9012"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 4: Unqualified - Kevin O''Brien
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('2dd93b4a-748f-4979-82e4-6e4a655c1647', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_004_unqualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-11T11:19:21.045465', '2025-08-11T11:54:21.045466', '2025-08-11T11:54:21.045466', 9, true, 35, 35, 'no', 'qualified', 'Thank you for your interest. While we may not be the best fit for your current needs, please reach out if your situation changes.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.228', '{"device_type": "mobile", "completion_time": 36}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('7bd180f1-a9fb-4589-bdf4-e62c19200147', '2dd93b4a-748f-4979-82e4-6e4a655c1647', 'organic', 'search', 'general_search', 'property specialist', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('ea5ed8bb-9666-4116-b339-35e02aa6484b', '2dd93b4a-748f-4979-82e4-6e4a655c1647', 'f2222222-2222-2222-2222-222222222222', 1, 'Kevin O''Brien', '{"name": "Kevin O''Brien"}', 10, '2025-08-11T11:19:21.045465'),
('a49202fa-d96e-4eae-b4e3-540ef2e43c62', '2dd93b4a-748f-4979-82e4-6e4a655c1647', 'f2222222-2222-2222-2222-222222222222', 2, 'kevin.obrien@email.com', '{"email": "kevin.obrien@email.com"}', 10, '2025-08-11T11:19:21.045465'),
('eccdcdfa-0cde-4721-b267-c352068790be', '2dd93b4a-748f-4979-82e4-6e4a655c1647', 'f2222222-2222-2222-2222-222222222222', 3, '(508) 555-3456', '{"phone": "(508) 555-3456"}', 15, '2025-08-11T11:19:21.045465'),
('91dda907-edcd-413b-9cb9-301a17d201fe', '2dd93b4a-748f-4979-82e4-6e4a655c1647', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-11T11:19:21.045465'),
('804a9aa2-b068-4898-b71f-f14822d81453', '2dd93b4a-748f-4979-82e4-6e4a655c1647', 'f2222222-2222-2222-2222-222222222222', 5, 'just_browsing', '{"timeline": "just_browsing"}', 0, '2025-08-11T11:19:21.045465'),
('d533662a-24ec-4f1a-bd35-b3603546afe0', '2dd93b4a-748f-4979-82e4-6e4a655c1647', 'f2222222-2222-2222-2222-222222222222', 6, 'planning_to_get', '{"mortgage_status": "planning_to_get"}', 10, '2025-08-11T11:19:21.045465'),
('e0a47d64-022b-49e6-9141-74f00e21d665', '2dd93b4a-748f-4979-82e4-6e4a655c1647', 'f2222222-2222-2222-2222-222222222222', 7, 'under_200k', '{"price_range": "under_200k"}', 5, '2025-08-11T11:19:21.045465'),
('e7798e03-091e-4f1c-94a3-e834da6a14db', '2dd93b4a-748f-4979-82e4-6e4a655c1647', 'f2222222-2222-2222-2222-222222222222', 8, 'other_metro', '{"areas": "other_metro"}', 10, '2025-08-11T11:19:21.045465'),
('e8b6853a-2ce3-4c48-9eab-09e4e3c27e97', '2dd93b4a-748f-4979-82e4-6e4a655c1647', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-11T11:19:21.045465'),
('8240e61d-f0f6-4de1-85f3-abf8e846ce0b', '2dd93b4a-748f-4979-82e4-6e4a655c1647', 'f2222222-2222-2222-2222-222222222222', 10, '1_bedroom', '{"bedrooms": "1_bedroom"}', 10, '2025-08-11T11:19:21.045465'),
('16d8c81d-78fd-4246-9dbe-399c6c4c6536', '2dd93b4a-748f-4979-82e4-6e4a655c1647', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-11T11:19:21.045465'),
('73ab9f9d-338a-4a14-b722-6104903a3f73', '2dd93b4a-748f-4979-82e4-6e4a655c1647', 'f2222222-2222-2222-2222-222222222222', 12, 'low', '{"urgency": "low"}', 10, '2025-08-11T11:19:21.045465');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('5f04d503-ad55-4532-a23b-412108b2e4fa', '2dd93b4a-748f-4979-82e4-6e4a655c1647', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'unqualified', '{"name": "Kevin O''Brien", "email": "kevin.obrien@email.com", "phone": "(508) 555-3456"}', 35, 0.35, false, false, NULL, NULL, NULL);


-- Lead 5: Maybe - Lisa Martinez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('958c7818-115a-4bd1-b73c-5751bcad790c', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_005_maybe', 'a2222222-2222-2222-2222-222222222222', '2025-08-15T23:19:21.045535', '2025-08-15T23:44:21.045536', '2025-08-15T23:44:21.045536', 12, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to match you with the right agent. Expect to hear from us within 2-3 days.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.147', '{"device_type": "desktop", "completion_time": 55}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('930c1c0b-f366-485e-a9db-c44a8742d515', '958c7818-115a-4bd1-b73c-5751bcad790c', 'google', 'cpc', 'affordable_homes', 'real estate expert', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('47f23f2b-29b0-465f-a1b9-2dbe7a24fcbd', '958c7818-115a-4bd1-b73c-5751bcad790c', 'f2222222-2222-2222-2222-222222222222', 1, 'Lisa Martinez', '{"name": "Lisa Martinez"}', 10, '2025-08-15T23:19:21.045535'),
('27a4668e-1b0e-42d3-a090-4fdaaae459ef', '958c7818-115a-4bd1-b73c-5751bcad790c', 'f2222222-2222-2222-2222-222222222222', 2, 'lisa.martinez@hospital.org', '{"email": "lisa.martinez@hospital.org"}', 10, '2025-08-15T23:19:21.045535'),
('5c03a937-4548-41e6-a116-1bbc6ffdab2c', '958c7818-115a-4bd1-b73c-5751bcad790c', 'f2222222-2222-2222-2222-222222222222', 3, '(781) 555-7890', '{"phone": "(781) 555-7890"}', 15, '2025-08-15T23:19:21.045535'),
('d430c168-0586-4db3-903a-4bffcf9a82ef', '958c7818-115a-4bd1-b73c-5751bcad790c', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-15T23:19:21.045535'),
('3ed1b379-b01c-4b65-befc-c00d38fba524', '958c7818-115a-4bd1-b73c-5751bcad790c', 'f2222222-2222-2222-2222-222222222222', 5, '6_12_months', '{"timeline": "6_12_months"}', 10, '2025-08-15T23:19:21.045535'),
('3bae09af-6e70-4bb8-9b15-4c293a6a8a8a', '958c7818-115a-4bd1-b73c-5751bcad790c', 'f2222222-2222-2222-2222-222222222222', 6, 'in_process', '{"mortgage_status": "in_process"}', 15, '2025-08-15T23:19:21.045535'),
('2556f59a-047d-4f40-a60d-3586fc55b36c', '958c7818-115a-4bd1-b73c-5751bcad790c', 'f2222222-2222-2222-2222-222222222222', 7, '$200k_300k', '{"price_range": "$200k_300k"}', 15, '2025-08-15T23:19:21.045535'),
('b2a81e6d-f031-4021-a83b-f71007a07c42', '958c7818-115a-4bd1-b73c-5751bcad790c', 'f2222222-2222-2222-2222-222222222222', 8, 'other_metro', '{"areas": "other_metro"}', 10, '2025-08-15T23:19:21.045535'),
('354a55b3-1614-4924-843b-ef14860272b5', '958c7818-115a-4bd1-b73c-5751bcad790c', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-15T23:19:21.045535'),
('c6bcd360-38cf-41d1-8247-d66e83df3639', '958c7818-115a-4bd1-b73c-5751bcad790c', 'f2222222-2222-2222-2222-222222222222', 10, '2_bedrooms', '{"bedrooms": "2_bedrooms"}', 10, '2025-08-15T23:19:21.045535'),
('1c193d42-f96c-4e64-97d8-e38406add579', '958c7818-115a-4bd1-b73c-5751bcad790c', 'f2222222-2222-2222-2222-222222222222', 11, 'yes', '{"worked_with_realtor": "yes"}', 10, '2025-08-15T23:19:21.045535'),
('347beff5-b74d-4fbb-9798-1645dd914b5a', '958c7818-115a-4bd1-b73c-5751bcad790c', 'f2222222-2222-2222-2222-222222222222', 12, 'medium', '{"urgency": "medium"}', 10, '2025-08-15T23:19:21.045535');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('4e27c76f-97c7-44d2-a1cb-e8548b22345b', '958c7818-115a-4bd1-b73c-5751bcad790c', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'maybe', '{"name": "Lisa Martinez", "email": "lisa.martinez@hospital.org", "phone": "(781) 555-7890"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 6: Qualified - Jessica_2 Chen
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('b1048dc9-9b59-42a4-9662-0022941e2eda', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_006_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-14T02:19:21.045603', '2025-08-14T02:55:21.045604', '2025-08-14T02:55:21.045604', 12, true, 90, 90, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.32', '{"device_type": "desktop", "completion_time": 35}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('62d81486-5b48-429e-aa13-7e2e7110d0ac', 'b1048dc9-9b59-42a4-9662-0022941e2eda', 'google', 'cpc', 'luxury_homes_boston', 'property specialist', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('b5672142-3384-497e-8ac8-05cd883ff380', 'b1048dc9-9b59-42a4-9662-0022941e2eda', 'f2222222-2222-2222-2222-222222222222', 1, 'Jessica_2 Chen', '{"name": "Jessica_2 Chen"}', 10, '2025-08-14T02:19:21.045603'),
('6c5183d2-1394-46b6-b530-4ba920599d7a', 'b1048dc9-9b59-42a4-9662-0022941e2eda', 'f2222222-2222-2222-2222-222222222222', 2, 'jessica.chen_2@techcorp.com', '{"email": "jessica.chen_2@techcorp.com"}', 10, '2025-08-14T02:19:21.045603'),
('93597df4-e40a-4604-8849-7d5e1689c8ab', 'b1048dc9-9b59-42a4-9662-0022941e2eda', 'f2222222-2222-2222-2222-222222222222', 3, '(617) 555-1234', '{"phone": "(617) 555-1234"}', 15, '2025-08-14T02:19:21.045603'),
('9058ec61-b829-4de9-9688-a55147a3ed6b', 'b1048dc9-9b59-42a4-9662-0022941e2eda', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-14T02:19:21.045603'),
('8308d7ff-5015-40f1-9ffe-6ffdd11db721', 'b1048dc9-9b59-42a4-9662-0022941e2eda', 'f2222222-2222-2222-2222-222222222222', 5, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-14T02:19:21.045603'),
('2d4849b9-b81b-430e-828d-cc2f64b2e52c', 'b1048dc9-9b59-42a4-9662-0022941e2eda', 'f2222222-2222-2222-2222-222222222222', 6, 'pre_approved', '{"mortgage_status": "pre_approved"}', 20, '2025-08-14T02:19:21.045603'),
('920ee010-9ad7-4225-a1c1-474032e079a3', 'b1048dc9-9b59-42a4-9662-0022941e2eda', 'f2222222-2222-2222-2222-222222222222', 7, '$500k_plus', '{"price_range": "$500k_plus"}', 20, '2025-08-14T02:19:21.045603'),
('87ca8967-3e61-46ce-8958-91e5def8f011', 'b1048dc9-9b59-42a4-9662-0022941e2eda', 'f2222222-2222-2222-2222-222222222222', 8, 'boston_cambridge', '{"areas": "boston_cambridge"}', 10, '2025-08-14T02:19:21.045603'),
('5bd9a2b7-c8cf-41e0-8f88-f28c69039858', 'b1048dc9-9b59-42a4-9662-0022941e2eda', 'f2222222-2222-2222-2222-222222222222', 9, 'no', '{"first_time_buyer": "no"}', 10, '2025-08-14T02:19:21.045603'),
('b19103c4-6a4c-4bf1-8da0-c9de76f75cde', 'b1048dc9-9b59-42a4-9662-0022941e2eda', 'f2222222-2222-2222-2222-222222222222', 10, '3_bedrooms', '{"bedrooms": "3_bedrooms"}', 10, '2025-08-14T02:19:21.045603'),
('803b944e-1d95-47be-809b-2e35adffa26a', 'b1048dc9-9b59-42a4-9662-0022941e2eda', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-14T02:19:21.045603'),
('0c665af8-3184-4af4-9404-21cf93fac8fe', 'b1048dc9-9b59-42a4-9662-0022941e2eda', 'f2222222-2222-2222-2222-222222222222', 12, 'high', '{"urgency": "high"}', 10, '2025-08-14T02:19:21.045603');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('e67c0e8c-58cd-4b0a-b250-b2606bb36107', 'b1048dc9-9b59-42a4-9662-0022941e2eda', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Jessica_2 Chen", "email": "jessica.chen_2@techcorp.com", "phone": "(617) 555-1234"}', 90, 0.90, true, false, NULL, NULL, NULL);


-- Lead 7: Qualified - Mark_2 Thompson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('53ec1875-bff7-41a0-80ec-d5792bfbc551', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_007_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-10T00:19:21.045673', '2025-08-10T00:56:21.045674', '2025-08-10T00:56:21.045674', 7, true, 85, 85, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.179', '{"device_type": "mobile", "completion_time": 21}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('91fb1564-09fa-4d85-8a5b-30def71ea4df', '53ec1875-bff7-41a0-80ec-d5792bfbc551', 'facebook', 'social', 'first_time_buyers', 'cambridge real estate', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Brookline');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('526f1dc5-f261-4b14-8b4a-ac27fcf895c9', '53ec1875-bff7-41a0-80ec-d5792bfbc551', 'f2222222-2222-2222-2222-222222222222', 1, 'Mark_2 Thompson', '{"name": "Mark_2 Thompson"}', 10, '2025-08-10T00:19:21.045673'),
('5cd2cbd1-1b1f-4c3a-b065-256f3174de55', '53ec1875-bff7-41a0-80ec-d5792bfbc551', 'f2222222-2222-2222-2222-222222222222', 2, 'mark.thompson_2@startup.io', '{"email": "mark.thompson_2@startup.io"}', 10, '2025-08-10T00:19:21.045673'),
('3869a215-dd1a-4c9a-a62f-bbb57eda92fa', '53ec1875-bff7-41a0-80ec-d5792bfbc551', 'f2222222-2222-2222-2222-222222222222', 3, '(857) 555-5678', '{"phone": "(857) 555-5678"}', 15, '2025-08-10T00:19:21.045673'),
('24b46d91-79a7-4477-af3c-48608447ee62', '53ec1875-bff7-41a0-80ec-d5792bfbc551', 'f2222222-2222-2222-2222-222222222222', 4, 'both', '{"buy_or_sell": "both"}', 25, '2025-08-10T00:19:21.045673'),
('18cff3cb-e199-4d6c-b154-7b64fa012742', '53ec1875-bff7-41a0-80ec-d5792bfbc551', 'f2222222-2222-2222-2222-222222222222', 5, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-10T00:19:21.045673'),
('a286eb26-5a42-4ae3-8f42-aaa16d90b9bc', '53ec1875-bff7-41a0-80ec-d5792bfbc551', 'f2222222-2222-2222-2222-222222222222', 6, 'in_process', '{"mortgage_status": "in_process"}', 15, '2025-08-10T00:19:21.045673'),
('233794c2-2a9f-4dc4-ab1e-34bdabbd1f2f', '53ec1875-bff7-41a0-80ec-d5792bfbc551', 'f2222222-2222-2222-2222-222222222222', 7, '$300k_500k', '{"price_range": "$300k_500k"}', 25, '2025-08-10T00:19:21.045673'),
('000d8ed5-b48f-4614-8269-cea73e9bd256', '53ec1875-bff7-41a0-80ec-d5792bfbc551', 'f2222222-2222-2222-2222-222222222222', 8, 'brookline_newton', '{"areas": "brookline_newton"}', 10, '2025-08-10T00:19:21.045673'),
('0dffab2f-23b6-45c5-bc0c-6ccbf6a66e68', '53ec1875-bff7-41a0-80ec-d5792bfbc551', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-10T00:19:21.045673'),
('a9939376-bdf5-4c45-8c52-7433fead1c32', '53ec1875-bff7-41a0-80ec-d5792bfbc551', 'f2222222-2222-2222-2222-222222222222', 10, '2_bedrooms', '{"bedrooms": "2_bedrooms"}', 10, '2025-08-10T00:19:21.045673'),
('15b5c0b1-a5a5-4307-804b-43683adc01e3', '53ec1875-bff7-41a0-80ec-d5792bfbc551', 'f2222222-2222-2222-2222-222222222222', 11, 'yes', '{"worked_with_realtor": "yes"}', 10, '2025-08-10T00:19:21.045673'),
('635f7247-1dd9-4177-a33b-f64d18fdab1b', '53ec1875-bff7-41a0-80ec-d5792bfbc551', 'f2222222-2222-2222-2222-222222222222', 12, 'medium', '{"urgency": "medium"}', 10, '2025-08-10T00:19:21.045673');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('dcd91865-3b23-49e7-b3e8-b970f1ec97e6', '53ec1875-bff7-41a0-80ec-d5792bfbc551', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Mark_2 Thompson", "email": "mark.thompson_2@startup.io", "phone": "(857) 555-5678"}', 85, 0.85, true, false, NULL, NULL, NULL);


-- Lead 8: Qualified - Amanda_2 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('a0285ea4-e2d9-497b-9025-d12840854cf1', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_008_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-22T17:19:21.045742', '2025-08-22T17:48:21.045743', '2025-08-22T17:48:21.045743', 10, true, 92, 92, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.206', '{"device_type": "desktop", "completion_time": 30}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('9a9e11ab-ca62-46a8-83db-78e80b7a5972', 'a0285ea4-e2d9-497b-9025-d12840854cf1', 'referral', 'referral', 'luxury_sellers', 'property specialist', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('599c3313-297e-4d49-b1d5-c9de8d0fa0d5', 'a0285ea4-e2d9-497b-9025-d12840854cf1', 'f2222222-2222-2222-2222-222222222222', 1, 'Amanda_2 Rodriguez', '{"name": "Amanda_2 Rodriguez"}', 10, '2025-08-22T17:19:21.045742'),
('0f5e7b57-4f63-495e-8550-4d23e689f3b9', 'a0285ea4-e2d9-497b-9025-d12840854cf1', 'f2222222-2222-2222-2222-222222222222', 2, 'arodriguez_2@lawfirm.com', '{"email": "arodriguez_2@lawfirm.com"}', 10, '2025-08-22T17:19:21.045742'),
('8961e7f8-c511-4c19-8529-3a365176a09c', 'a0285ea4-e2d9-497b-9025-d12840854cf1', 'f2222222-2222-2222-2222-222222222222', 3, '(617) 555-9012', '{"phone": "(617) 555-9012"}', 15, '2025-08-22T17:19:21.045742'),
('07720f21-8777-4c0e-95be-57ebef575e93', 'a0285ea4-e2d9-497b-9025-d12840854cf1', 'f2222222-2222-2222-2222-222222222222', 4, 'sell', '{"buy_or_sell": "sell"}', 20, '2025-08-22T17:19:21.045742'),
('42cef2e8-ec46-4119-84f9-4a8ff0e1cf20', 'a0285ea4-e2d9-497b-9025-d12840854cf1', 'f2222222-2222-2222-2222-222222222222', 5, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-22T17:19:21.045742'),
('33b10678-c45e-4c92-ad0f-bfc1ed8ff55a', 'a0285ea4-e2d9-497b-9025-d12840854cf1', 'f2222222-2222-2222-2222-222222222222', 6, 'cash', '{"mortgage_status": "cash"}', 25, '2025-08-22T17:19:21.045742'),
('dd69e91b-5865-427c-a4f8-b4123a58ac76', 'a0285ea4-e2d9-497b-9025-d12840854cf1', 'f2222222-2222-2222-2222-222222222222', 7, '$500k_plus', '{"price_range": "$500k_plus"}', 20, '2025-08-22T17:19:21.045742'),
('71b9f3f0-d36f-4418-ae0c-36a197194ab2', 'a0285ea4-e2d9-497b-9025-d12840854cf1', 'f2222222-2222-2222-2222-222222222222', 8, 'boston_cambridge', '{"areas": "boston_cambridge"}', 10, '2025-08-22T17:19:21.045742'),
('fd4e7598-6a32-4ddf-9db5-720d4a39edb3', 'a0285ea4-e2d9-497b-9025-d12840854cf1', 'f2222222-2222-2222-2222-222222222222', 9, 'no', '{"first_time_buyer": "no"}', 10, '2025-08-22T17:19:21.045742'),
('559041dc-af4e-496e-815d-74b38f21c70d', 'a0285ea4-e2d9-497b-9025-d12840854cf1', 'f2222222-2222-2222-2222-222222222222', 10, '4_bedrooms', '{"bedrooms": "4_bedrooms"}', 10, '2025-08-22T17:19:21.045742'),
('4e68ff9d-5400-49b1-89ea-85a747f4587a', 'a0285ea4-e2d9-497b-9025-d12840854cf1', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-22T17:19:21.045742'),
('46242efd-1c69-4a00-a9c5-ce85567c08f6', 'a0285ea4-e2d9-497b-9025-d12840854cf1', 'f2222222-2222-2222-2222-222222222222', 12, 'high', '{"urgency": "high"}', 10, '2025-08-22T17:19:21.045742');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('efd2efe0-4b4b-4325-95ec-3cafb53fd3e2', 'a0285ea4-e2d9-497b-9025-d12840854cf1', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Amanda_2 Rodriguez", "email": "arodriguez_2@lawfirm.com", "phone": "(617) 555-9012"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 9: Unqualified - Kevin_2 O''Brien
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_009_unqualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-14T07:19:21.045810', '2025-08-14T07:45:21.045811', '2025-08-14T07:45:21.045811', 9, true, 35, 35, 'no', 'qualified', 'Thank you for your interest. While we may not be the best fit for your current needs, please reach out if your situation changes.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.60', '{"device_type": "mobile", "completion_time": 26}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('0df4cdaf-52fb-45d8-90b8-2050ff1ea8a9', 'cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'organic', 'search', 'general_search', 'cambridge real estate', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('2fa5854a-7edf-47a3-952d-cde89f98c88e', 'cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'f2222222-2222-2222-2222-222222222222', 1, 'Kevin_2 O''Brien', '{"name": "Kevin_2 O''Brien"}', 10, '2025-08-14T07:19:21.045810'),
('e2a55980-0cda-4b0c-a7f3-085c366d59ad', 'cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'f2222222-2222-2222-2222-222222222222', 2, 'kevin.obrien_2@email.com', '{"email": "kevin.obrien_2@email.com"}', 10, '2025-08-14T07:19:21.045810'),
('ee56e9a2-ff0c-4f83-906c-b0f30dfced01', 'cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'f2222222-2222-2222-2222-222222222222', 3, '(508) 555-3456', '{"phone": "(508) 555-3456"}', 15, '2025-08-14T07:19:21.045810'),
('882cd7ed-9c10-420c-bc7b-33b10d59787a', 'cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-14T07:19:21.045810'),
('1114143f-c53c-48e7-ae31-72cbaf1dfc33', 'cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'f2222222-2222-2222-2222-222222222222', 5, 'just_browsing', '{"timeline": "just_browsing"}', 0, '2025-08-14T07:19:21.045810'),
('bcadaac7-6674-4ad0-80d7-a05b930f61e1', 'cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'f2222222-2222-2222-2222-222222222222', 6, 'planning_to_get', '{"mortgage_status": "planning_to_get"}', 10, '2025-08-14T07:19:21.045810'),
('0f86ed38-cf87-425d-93d0-04aa450e618c', 'cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'f2222222-2222-2222-2222-222222222222', 7, 'under_200k', '{"price_range": "under_200k"}', 5, '2025-08-14T07:19:21.045810'),
('f6011c5b-961b-4c44-9afc-a7932bff7edc', 'cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'f2222222-2222-2222-2222-222222222222', 8, 'other_metro', '{"areas": "other_metro"}', 10, '2025-08-14T07:19:21.045810'),
('24b5fd29-513e-440c-9b40-060cacb810b5', 'cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-14T07:19:21.045810'),
('85b09625-1a6e-455d-96f6-933878bf3b43', 'cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'f2222222-2222-2222-2222-222222222222', 10, '1_bedroom', '{"bedrooms": "1_bedroom"}', 10, '2025-08-14T07:19:21.045810'),
('1990757c-75ce-414f-a578-e19daca8c087', 'cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-14T07:19:21.045810'),
('94de3802-f64c-4c10-a005-5515ecfa0a83', 'cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'f2222222-2222-2222-2222-222222222222', 12, 'low', '{"urgency": "low"}', 10, '2025-08-14T07:19:21.045810');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('b9aec36d-d4ca-4171-a6c1-7ec2fdce3fef', 'cb8cc02c-33dc-4683-bdf7-8d2f99d0ddf5', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'unqualified', '{"name": "Kevin_2 O''Brien", "email": "kevin.obrien_2@email.com", "phone": "(508) 555-3456"}', 35, 0.35, false, false, NULL, NULL, NULL);


-- Lead 10: Maybe - Lisa_2 Martinez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_010_maybe', 'a2222222-2222-2222-2222-222222222222', '2025-08-12T18:19:21.045877', '2025-08-12T18:48:21.045878', '2025-08-12T18:48:21.045878', 11, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to match you with the right agent. Expect to hear from us within 2-3 days.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.161', '{"device_type": "desktop", "completion_time": 60}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('2b43d320-9d28-438d-ac49-2ba06f954490', '08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'google', 'cpc', 'affordable_homes', 'boston realtor', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('a4507792-0c36-4440-b5c9-dc6632a13eaf', '08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'f2222222-2222-2222-2222-222222222222', 1, 'Lisa_2 Martinez', '{"name": "Lisa_2 Martinez"}', 10, '2025-08-12T18:19:21.045877'),
('42381d28-3142-4e02-9a29-e3168b83f7c2', '08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'f2222222-2222-2222-2222-222222222222', 2, 'lisa.martinez_2@hospital.org', '{"email": "lisa.martinez_2@hospital.org"}', 10, '2025-08-12T18:19:21.045877'),
('fd2ce078-2dc4-403d-8b96-60c52fbaa8a9', '08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'f2222222-2222-2222-2222-222222222222', 3, '(781) 555-7890', '{"phone": "(781) 555-7890"}', 15, '2025-08-12T18:19:21.045877'),
('8d0dd9bb-d689-4bf6-9cd4-f45b3254e632', '08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-12T18:19:21.045877'),
('9691c6e5-1292-4be6-af47-af5fdd45101d', '08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'f2222222-2222-2222-2222-222222222222', 5, '6_12_months', '{"timeline": "6_12_months"}', 10, '2025-08-12T18:19:21.045877'),
('92c8e002-2d1c-45e3-bd6c-b9d568ffc145', '08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'f2222222-2222-2222-2222-222222222222', 6, 'in_process', '{"mortgage_status": "in_process"}', 15, '2025-08-12T18:19:21.045877'),
('80e6d447-ba68-448a-b3b1-6fe86f8dc911', '08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'f2222222-2222-2222-2222-222222222222', 7, '$200k_300k', '{"price_range": "$200k_300k"}', 15, '2025-08-12T18:19:21.045877'),
('fc059958-08c6-4e1e-84fd-b6d4a2fb6a02', '08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'f2222222-2222-2222-2222-222222222222', 8, 'other_metro', '{"areas": "other_metro"}', 10, '2025-08-12T18:19:21.045877'),
('6cd906a4-7dc5-4e32-8438-a65df5ca5b9a', '08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-12T18:19:21.045877'),
('5743e13b-89eb-41fb-8642-8499aca5522e', '08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'f2222222-2222-2222-2222-222222222222', 10, '2_bedrooms', '{"bedrooms": "2_bedrooms"}', 10, '2025-08-12T18:19:21.045877'),
('8bc4faf5-6098-49fe-8139-85b1fd8b2401', '08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'f2222222-2222-2222-2222-222222222222', 11, 'yes', '{"worked_with_realtor": "yes"}', 10, '2025-08-12T18:19:21.045877'),
('7be97013-7a65-465f-bae4-2aa6e3b1671d', '08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'f2222222-2222-2222-2222-222222222222', 12, 'medium', '{"urgency": "medium"}', 10, '2025-08-12T18:19:21.045877');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('94ec60ed-7056-435f-9dc5-c87b755cd9d1', '08efb5fc-1b24-4f9f-9e4c-ced0676e2f17', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'maybe', '{"name": "Lisa_2 Martinez", "email": "lisa.martinez_2@hospital.org", "phone": "(781) 555-7890"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 11: Qualified - Jessica_3 Chen
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('d5567085-a035-45af-bb70-69ae33792bc4', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_011_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-15T13:19:21.045943', '2025-08-15T13:57:21.045944', '2025-08-15T13:57:21.045944', 6, true, 90, 90, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.233', '{"device_type": "desktop", "completion_time": 17}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('308ee70f-1cdd-4407-8924-b046e59df077', 'd5567085-a035-45af-bb70-69ae33792bc4', 'google', 'cpc', 'luxury_homes_boston', 'cambridge real estate', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Brookline');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('2604ed24-d0cc-499b-a7e4-54e5230c8a7d', 'd5567085-a035-45af-bb70-69ae33792bc4', 'f2222222-2222-2222-2222-222222222222', 1, 'Jessica_3 Chen', '{"name": "Jessica_3 Chen"}', 10, '2025-08-15T13:19:21.045943'),
('73c93e32-0ce6-4cdd-b1f1-105ce86f37a7', 'd5567085-a035-45af-bb70-69ae33792bc4', 'f2222222-2222-2222-2222-222222222222', 2, 'jessica.chen_3@techcorp.com', '{"email": "jessica.chen_3@techcorp.com"}', 10, '2025-08-15T13:19:21.045943'),
('572bd261-f68d-4a95-aae8-680ee377dbcd', 'd5567085-a035-45af-bb70-69ae33792bc4', 'f2222222-2222-2222-2222-222222222222', 3, '(617) 555-1234', '{"phone": "(617) 555-1234"}', 15, '2025-08-15T13:19:21.045943'),
('7b18798f-0247-4963-9ec0-48268522712d', 'd5567085-a035-45af-bb70-69ae33792bc4', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-15T13:19:21.045943'),
('c1d5d9d8-c712-48b2-94bb-57cec3b1235c', 'd5567085-a035-45af-bb70-69ae33792bc4', 'f2222222-2222-2222-2222-222222222222', 5, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-15T13:19:21.045943'),
('4bd8970e-c50d-4d4a-88ee-c897be966007', 'd5567085-a035-45af-bb70-69ae33792bc4', 'f2222222-2222-2222-2222-222222222222', 6, 'pre_approved', '{"mortgage_status": "pre_approved"}', 20, '2025-08-15T13:19:21.045943'),
('089099e1-8d95-4150-9290-b45b1c3f0047', 'd5567085-a035-45af-bb70-69ae33792bc4', 'f2222222-2222-2222-2222-222222222222', 7, '$500k_plus', '{"price_range": "$500k_plus"}', 20, '2025-08-15T13:19:21.045943'),
('25259466-1bc3-4596-8866-d2c40a854e49', 'd5567085-a035-45af-bb70-69ae33792bc4', 'f2222222-2222-2222-2222-222222222222', 8, 'boston_cambridge', '{"areas": "boston_cambridge"}', 10, '2025-08-15T13:19:21.045943'),
('fe8e75d1-fd39-4755-9d08-d6ee6bc9075c', 'd5567085-a035-45af-bb70-69ae33792bc4', 'f2222222-2222-2222-2222-222222222222', 9, 'no', '{"first_time_buyer": "no"}', 10, '2025-08-15T13:19:21.045943'),
('00cef710-f52b-4d28-831a-9cb9560d54cb', 'd5567085-a035-45af-bb70-69ae33792bc4', 'f2222222-2222-2222-2222-222222222222', 10, '3_bedrooms', '{"bedrooms": "3_bedrooms"}', 10, '2025-08-15T13:19:21.045943'),
('099ce3d5-15dd-45ba-a472-9307e82e0d52', 'd5567085-a035-45af-bb70-69ae33792bc4', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-15T13:19:21.045943'),
('0f11c398-f040-4913-8e96-343abb45a14a', 'd5567085-a035-45af-bb70-69ae33792bc4', 'f2222222-2222-2222-2222-222222222222', 12, 'high', '{"urgency": "high"}', 10, '2025-08-15T13:19:21.045943');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('95100f52-7911-4839-a378-9e7c3a6e30d1', 'd5567085-a035-45af-bb70-69ae33792bc4', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Jessica_3 Chen", "email": "jessica.chen_3@techcorp.com", "phone": "(617) 555-1234"}', 90, 0.90, true, false, NULL, NULL, NULL);


-- Lead 12: Qualified - Mark_3 Thompson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('b716c631-7ab6-4bee-8de6-2662e42a46a2', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_012_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-18T05:19:21.046009', '2025-08-18T05:48:21.046010', '2025-08-18T05:48:21.046010', 6, true, 85, 85, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.211', '{"device_type": "mobile", "completion_time": 42}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('1f096a49-2055-4e3d-abbc-4f298dee86e6', 'b716c631-7ab6-4bee-8de6-2662e42a46a2', 'facebook', 'social', 'first_time_buyers', 'real estate expert', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('94f1c59e-78c3-45f6-90cb-ed3ac773d4f1', 'b716c631-7ab6-4bee-8de6-2662e42a46a2', 'f2222222-2222-2222-2222-222222222222', 1, 'Mark_3 Thompson', '{"name": "Mark_3 Thompson"}', 10, '2025-08-18T05:19:21.046009'),
('c723c7c0-dd65-42aa-b3d8-eb537ee29827', 'b716c631-7ab6-4bee-8de6-2662e42a46a2', 'f2222222-2222-2222-2222-222222222222', 2, 'mark.thompson_3@startup.io', '{"email": "mark.thompson_3@startup.io"}', 10, '2025-08-18T05:19:21.046009'),
('fd10e47a-99f4-47a7-9100-09199da96963', 'b716c631-7ab6-4bee-8de6-2662e42a46a2', 'f2222222-2222-2222-2222-222222222222', 3, '(857) 555-5678', '{"phone": "(857) 555-5678"}', 15, '2025-08-18T05:19:21.046009'),
('d4b0b4f2-1d7c-4005-a904-86c2a81e88d5', 'b716c631-7ab6-4bee-8de6-2662e42a46a2', 'f2222222-2222-2222-2222-222222222222', 4, 'both', '{"buy_or_sell": "both"}', 25, '2025-08-18T05:19:21.046009'),
('38cfcbc1-afb0-46fb-a6f9-6ab4374d8eea', 'b716c631-7ab6-4bee-8de6-2662e42a46a2', 'f2222222-2222-2222-2222-222222222222', 5, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-18T05:19:21.046009'),
('ef08ac20-6cf0-47ca-aec7-49b350bb4906', 'b716c631-7ab6-4bee-8de6-2662e42a46a2', 'f2222222-2222-2222-2222-222222222222', 6, 'in_process', '{"mortgage_status": "in_process"}', 15, '2025-08-18T05:19:21.046009'),
('95a72967-ed2a-4ee5-a6ba-acb5f61223c3', 'b716c631-7ab6-4bee-8de6-2662e42a46a2', 'f2222222-2222-2222-2222-222222222222', 7, '$300k_500k', '{"price_range": "$300k_500k"}', 25, '2025-08-18T05:19:21.046009'),
('8775f435-eeaf-4305-bc47-d9cee686206b', 'b716c631-7ab6-4bee-8de6-2662e42a46a2', 'f2222222-2222-2222-2222-222222222222', 8, 'brookline_newton', '{"areas": "brookline_newton"}', 10, '2025-08-18T05:19:21.046009'),
('5b8d5791-f4c8-4681-b898-07a052170db5', 'b716c631-7ab6-4bee-8de6-2662e42a46a2', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-18T05:19:21.046009'),
('6156873d-9076-41cb-9efe-cfcebb314a8e', 'b716c631-7ab6-4bee-8de6-2662e42a46a2', 'f2222222-2222-2222-2222-222222222222', 10, '2_bedrooms', '{"bedrooms": "2_bedrooms"}', 10, '2025-08-18T05:19:21.046009'),
('bce5d006-5904-461b-b975-3ef2d55e856f', 'b716c631-7ab6-4bee-8de6-2662e42a46a2', 'f2222222-2222-2222-2222-222222222222', 11, 'yes', '{"worked_with_realtor": "yes"}', 10, '2025-08-18T05:19:21.046009'),
('25099775-2e29-4b40-b998-2a79eda5b478', 'b716c631-7ab6-4bee-8de6-2662e42a46a2', 'f2222222-2222-2222-2222-222222222222', 12, 'medium', '{"urgency": "medium"}', 10, '2025-08-18T05:19:21.046009');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('0662979d-0c96-4cac-9ead-a7aa66b5e78f', 'b716c631-7ab6-4bee-8de6-2662e42a46a2', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Mark_3 Thompson", "email": "mark.thompson_3@startup.io", "phone": "(857) 555-5678"}', 85, 0.85, true, false, NULL, NULL, NULL);


-- Lead 13: Qualified - Amanda_3 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_013_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-23T15:19:21.046076', '2025-08-23T15:38:21.046077', '2025-08-23T15:38:21.046077', 8, true, 92, 92, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.243', '{"device_type": "desktop", "completion_time": 10}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('4c6ebde4-5c4e-46e0-a3aa-cc839ba33d18', 'bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'referral', 'referral', 'luxury_sellers', 'cambridge real estate', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('ec515dd2-6d3a-4ddb-9f2c-c7960f0eb1f6', 'bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'f2222222-2222-2222-2222-222222222222', 1, 'Amanda_3 Rodriguez', '{"name": "Amanda_3 Rodriguez"}', 10, '2025-08-23T15:19:21.046076'),
('5a2f9a68-e783-405b-9160-665b65c162e4', 'bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'f2222222-2222-2222-2222-222222222222', 2, 'arodriguez_3@lawfirm.com', '{"email": "arodriguez_3@lawfirm.com"}', 10, '2025-08-23T15:19:21.046076'),
('f85a5d3e-2f7c-40ff-b99c-b003dc6bd98e', 'bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'f2222222-2222-2222-2222-222222222222', 3, '(617) 555-9012', '{"phone": "(617) 555-9012"}', 15, '2025-08-23T15:19:21.046076'),
('5694b46d-6e54-4117-9c60-d7aef7d13a05', 'bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'f2222222-2222-2222-2222-222222222222', 4, 'sell', '{"buy_or_sell": "sell"}', 20, '2025-08-23T15:19:21.046076'),
('561e882c-7bdc-4c33-bbe8-0018a86f5c70', 'bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'f2222222-2222-2222-2222-222222222222', 5, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-23T15:19:21.046076'),
('9a76fa67-69f9-4652-b418-f03307096284', 'bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'f2222222-2222-2222-2222-222222222222', 6, 'cash', '{"mortgage_status": "cash"}', 25, '2025-08-23T15:19:21.046076'),
('983ef46d-1cee-4fa3-9256-5a03af93028c', 'bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'f2222222-2222-2222-2222-222222222222', 7, '$500k_plus', '{"price_range": "$500k_plus"}', 20, '2025-08-23T15:19:21.046076'),
('15160179-c35e-45e3-9d6a-7d0605392f2f', 'bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'f2222222-2222-2222-2222-222222222222', 8, 'boston_cambridge', '{"areas": "boston_cambridge"}', 10, '2025-08-23T15:19:21.046076'),
('7cf899e2-03ac-49ed-8abd-eef01d001f74', 'bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'f2222222-2222-2222-2222-222222222222', 9, 'no', '{"first_time_buyer": "no"}', 10, '2025-08-23T15:19:21.046076'),
('40d43188-3f29-4b6d-8017-d9c837769553', 'bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'f2222222-2222-2222-2222-222222222222', 10, '4_bedrooms', '{"bedrooms": "4_bedrooms"}', 10, '2025-08-23T15:19:21.046076'),
('3bab0ff3-f95c-4611-92d4-6eb1287b03ab', 'bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-23T15:19:21.046076'),
('2bd4fa08-e160-464a-9e6d-60764a656285', 'bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'f2222222-2222-2222-2222-222222222222', 12, 'high', '{"urgency": "high"}', 10, '2025-08-23T15:19:21.046076');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('170b5764-3ba8-4d80-a33d-77e7e8dab51d', 'bcdb31c4-5303-4951-9ff2-2b394ae468f9', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Amanda_3 Rodriguez", "email": "arodriguez_3@lawfirm.com", "phone": "(617) 555-9012"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 14: Unqualified - Kevin_3 O''Brien
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('34d0e584-aa16-4931-a621-d92b3fab8868', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_014_unqualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-11T07:19:21.046141', '2025-08-11T08:02:21.046142', '2025-08-11T08:02:21.046142', 10, true, 35, 35, 'no', 'qualified', 'Thank you for your interest. While we may not be the best fit for your current needs, please reach out if your situation changes.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.117', '{"device_type": "mobile", "completion_time": 40}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('0cc6eb55-d077-4b91-8ab1-616abd1f61ef', '34d0e584-aa16-4931-a621-d92b3fab8868', 'organic', 'search', 'general_search', 'boston realtor', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('bf85a883-ee6a-4226-b2ef-12d9c117171a', '34d0e584-aa16-4931-a621-d92b3fab8868', 'f2222222-2222-2222-2222-222222222222', 1, 'Kevin_3 O''Brien', '{"name": "Kevin_3 O''Brien"}', 10, '2025-08-11T07:19:21.046141'),
('ea6757a4-ccf5-4b0c-95e5-5bb58dc6ac09', '34d0e584-aa16-4931-a621-d92b3fab8868', 'f2222222-2222-2222-2222-222222222222', 2, 'kevin.obrien_3@email.com', '{"email": "kevin.obrien_3@email.com"}', 10, '2025-08-11T07:19:21.046141'),
('6c9ac4ba-571e-4f92-af35-d596479e268a', '34d0e584-aa16-4931-a621-d92b3fab8868', 'f2222222-2222-2222-2222-222222222222', 3, '(508) 555-3456', '{"phone": "(508) 555-3456"}', 15, '2025-08-11T07:19:21.046141'),
('182428b8-25d2-4fa4-b94a-d98502ff76cb', '34d0e584-aa16-4931-a621-d92b3fab8868', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-11T07:19:21.046141'),
('70e99f8f-8eb1-4272-ab94-20e4f9145a98', '34d0e584-aa16-4931-a621-d92b3fab8868', 'f2222222-2222-2222-2222-222222222222', 5, 'just_browsing', '{"timeline": "just_browsing"}', 0, '2025-08-11T07:19:21.046141'),
('3ca29969-e657-40bb-87ed-444a67b1e835', '34d0e584-aa16-4931-a621-d92b3fab8868', 'f2222222-2222-2222-2222-222222222222', 6, 'planning_to_get', '{"mortgage_status": "planning_to_get"}', 10, '2025-08-11T07:19:21.046141'),
('57c40519-c153-4aed-b5e1-ee6fc508f506', '34d0e584-aa16-4931-a621-d92b3fab8868', 'f2222222-2222-2222-2222-222222222222', 7, 'under_200k', '{"price_range": "under_200k"}', 5, '2025-08-11T07:19:21.046141'),
('a973ba4a-2d6f-4f97-868c-f41882854987', '34d0e584-aa16-4931-a621-d92b3fab8868', 'f2222222-2222-2222-2222-222222222222', 8, 'other_metro', '{"areas": "other_metro"}', 10, '2025-08-11T07:19:21.046141'),
('8faeab11-4d22-436a-b31a-1708c471df2e', '34d0e584-aa16-4931-a621-d92b3fab8868', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-11T07:19:21.046141'),
('2935861e-6e03-480c-b6e1-ff58e57b4ecd', '34d0e584-aa16-4931-a621-d92b3fab8868', 'f2222222-2222-2222-2222-222222222222', 10, '1_bedroom', '{"bedrooms": "1_bedroom"}', 10, '2025-08-11T07:19:21.046141'),
('91d0d9b9-faa0-4cb5-9672-3691a0838fb1', '34d0e584-aa16-4931-a621-d92b3fab8868', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-11T07:19:21.046141'),
('79c4ce7a-fcb0-4844-a864-c94e84cc291b', '34d0e584-aa16-4931-a621-d92b3fab8868', 'f2222222-2222-2222-2222-222222222222', 12, 'low', '{"urgency": "low"}', 10, '2025-08-11T07:19:21.046141');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('5c202fc2-d17b-470c-859e-39dde39efadd', '34d0e584-aa16-4931-a621-d92b3fab8868', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'unqualified', '{"name": "Kevin_3 O''Brien", "email": "kevin.obrien_3@email.com", "phone": "(508) 555-3456"}', 35, 0.35, false, false, NULL, NULL, NULL);


-- Lead 15: Maybe - Lisa_3 Martinez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_015_maybe', 'a2222222-2222-2222-2222-222222222222', '2025-08-16T00:19:21.046208', '2025-08-16T00:50:21.046209', '2025-08-16T00:50:21.046209', 7, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to match you with the right agent. Expect to hear from us within 2-3 days.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.93', '{"device_type": "desktop", "completion_time": 57}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('55bb3819-b5ea-459a-bbd5-f1f6bec1bea4', '2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'google', 'cpc', 'affordable_homes', 'home buying agent', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('43103d6b-6623-4e94-adee-643548e94477', '2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'f2222222-2222-2222-2222-222222222222', 1, 'Lisa_3 Martinez', '{"name": "Lisa_3 Martinez"}', 10, '2025-08-16T00:19:21.046208'),
('9604f9c8-3200-467d-99d4-3bbea725877e', '2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'f2222222-2222-2222-2222-222222222222', 2, 'lisa.martinez_3@hospital.org', '{"email": "lisa.martinez_3@hospital.org"}', 10, '2025-08-16T00:19:21.046208'),
('182ccd04-f895-4663-9c5a-7b11d79e4a77', '2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'f2222222-2222-2222-2222-222222222222', 3, '(781) 555-7890', '{"phone": "(781) 555-7890"}', 15, '2025-08-16T00:19:21.046208'),
('102ae6e4-e980-4058-9fcb-709dad67aee3', '2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-16T00:19:21.046208'),
('5991ebbb-e9ef-4449-a3b1-868f062cdd92', '2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'f2222222-2222-2222-2222-222222222222', 5, '6_12_months', '{"timeline": "6_12_months"}', 10, '2025-08-16T00:19:21.046208'),
('f60e56dd-0525-421c-946b-cf83b84621b6', '2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'f2222222-2222-2222-2222-222222222222', 6, 'in_process', '{"mortgage_status": "in_process"}', 15, '2025-08-16T00:19:21.046208'),
('cd3f2a7e-bdc4-47ad-97cf-71d2f921ed20', '2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'f2222222-2222-2222-2222-222222222222', 7, '$200k_300k', '{"price_range": "$200k_300k"}', 15, '2025-08-16T00:19:21.046208'),
('0ed8be00-5a00-4b78-b017-a02da19e72ce', '2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'f2222222-2222-2222-2222-222222222222', 8, 'other_metro', '{"areas": "other_metro"}', 10, '2025-08-16T00:19:21.046208'),
('e676e5d5-3944-45e0-83aa-8320a028665b', '2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-16T00:19:21.046208'),
('1f24872a-54ee-42b0-9320-af1016761c80', '2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'f2222222-2222-2222-2222-222222222222', 10, '2_bedrooms', '{"bedrooms": "2_bedrooms"}', 10, '2025-08-16T00:19:21.046208'),
('3e1d3382-90a1-484b-9d8d-90efbbb33e1c', '2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'f2222222-2222-2222-2222-222222222222', 11, 'yes', '{"worked_with_realtor": "yes"}', 10, '2025-08-16T00:19:21.046208'),
('ad7d56f7-aba2-4a69-9535-8e4bf14c193c', '2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'f2222222-2222-2222-2222-222222222222', 12, 'medium', '{"urgency": "medium"}', 10, '2025-08-16T00:19:21.046208');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('700a1c48-bd76-4050-be68-0e3d095f3a7b', '2e1d8bc1-fb7e-4d9a-b017-cf85f3e0b8bc', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'maybe', '{"name": "Lisa_3 Martinez", "email": "lisa.martinez_3@hospital.org", "phone": "(781) 555-7890"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 16: Qualified - Jessica_4 Chen
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('321304c6-d943-444b-8ec9-248c24ae82bc', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_016_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-13T06:19:21.046273', '2025-08-13T06:42:21.046274', '2025-08-13T06:42:21.046274', 11, true, 90, 90, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.76', '{"device_type": "desktop", "completion_time": 60}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('525aafe1-edbf-49ce-bfda-8d7b9a7542f4', '321304c6-d943-444b-8ec9-248c24ae82bc', 'google', 'cpc', 'luxury_homes_boston', 'real estate expert', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('132b66ea-5c10-4058-b1e3-e146116a9215', '321304c6-d943-444b-8ec9-248c24ae82bc', 'f2222222-2222-2222-2222-222222222222', 1, 'Jessica_4 Chen', '{"name": "Jessica_4 Chen"}', 10, '2025-08-13T06:19:21.046273'),
('3b55a94f-f1ea-4ae1-9434-5af9d07978f9', '321304c6-d943-444b-8ec9-248c24ae82bc', 'f2222222-2222-2222-2222-222222222222', 2, 'jessica.chen_4@techcorp.com', '{"email": "jessica.chen_4@techcorp.com"}', 10, '2025-08-13T06:19:21.046273'),
('64f325c7-1097-4809-ae80-5c0f7e078ab5', '321304c6-d943-444b-8ec9-248c24ae82bc', 'f2222222-2222-2222-2222-222222222222', 3, '(617) 555-1234', '{"phone": "(617) 555-1234"}', 15, '2025-08-13T06:19:21.046273'),
('9b3c5444-203d-4846-b19a-17c13a701792', '321304c6-d943-444b-8ec9-248c24ae82bc', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-13T06:19:21.046273'),
('d0c360b5-9493-4cd2-a790-450d1d91a770', '321304c6-d943-444b-8ec9-248c24ae82bc', 'f2222222-2222-2222-2222-222222222222', 5, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-13T06:19:21.046273'),
('3892ead4-b336-4766-bb54-ae1a63aab17d', '321304c6-d943-444b-8ec9-248c24ae82bc', 'f2222222-2222-2222-2222-222222222222', 6, 'pre_approved', '{"mortgage_status": "pre_approved"}', 20, '2025-08-13T06:19:21.046273'),
('df842524-ad1c-4de1-b5fa-acd38c39badd', '321304c6-d943-444b-8ec9-248c24ae82bc', 'f2222222-2222-2222-2222-222222222222', 7, '$500k_plus', '{"price_range": "$500k_plus"}', 20, '2025-08-13T06:19:21.046273'),
('ff0747dc-a44d-48c9-88e8-25dfa706e523', '321304c6-d943-444b-8ec9-248c24ae82bc', 'f2222222-2222-2222-2222-222222222222', 8, 'boston_cambridge', '{"areas": "boston_cambridge"}', 10, '2025-08-13T06:19:21.046273'),
('4f5dd563-e61a-4afa-b957-21b96111e23e', '321304c6-d943-444b-8ec9-248c24ae82bc', 'f2222222-2222-2222-2222-222222222222', 9, 'no', '{"first_time_buyer": "no"}', 10, '2025-08-13T06:19:21.046273'),
('0c9e3983-aa10-43d1-bc0b-9705e7fcf350', '321304c6-d943-444b-8ec9-248c24ae82bc', 'f2222222-2222-2222-2222-222222222222', 10, '3_bedrooms', '{"bedrooms": "3_bedrooms"}', 10, '2025-08-13T06:19:21.046273'),
('23c349ca-db9c-4966-b762-a513d65d45b3', '321304c6-d943-444b-8ec9-248c24ae82bc', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-13T06:19:21.046273'),
('e347590d-48db-466f-9f8c-34f477684ffd', '321304c6-d943-444b-8ec9-248c24ae82bc', 'f2222222-2222-2222-2222-222222222222', 12, 'high', '{"urgency": "high"}', 10, '2025-08-13T06:19:21.046273');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('989e162f-fabe-44b5-a3c2-5b56d1186386', '321304c6-d943-444b-8ec9-248c24ae82bc', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Jessica_4 Chen", "email": "jessica.chen_4@techcorp.com", "phone": "(617) 555-1234"}', 90, 0.90, true, false, NULL, NULL, NULL);


-- Lead 17: Qualified - Mark_4 Thompson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_017_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-22T05:19:21.046338', '2025-08-22T05:44:21.046339', '2025-08-22T05:44:21.046339', 10, true, 85, 85, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.173', '{"device_type": "mobile", "completion_time": 32}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('0aebc7cf-9c84-4a35-9fac-423e489b70e0', '7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'facebook', 'social', 'first_time_buyers', 'boston realtor', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('7233a9cf-45ec-41b9-bd3f-11df13e7ed9f', '7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'f2222222-2222-2222-2222-222222222222', 1, 'Mark_4 Thompson', '{"name": "Mark_4 Thompson"}', 10, '2025-08-22T05:19:21.046338'),
('35699808-cc14-477c-9e49-b54e8efd2529', '7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'f2222222-2222-2222-2222-222222222222', 2, 'mark.thompson_4@startup.io', '{"email": "mark.thompson_4@startup.io"}', 10, '2025-08-22T05:19:21.046338'),
('91466175-57f2-4203-8223-00abcdc71495', '7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'f2222222-2222-2222-2222-222222222222', 3, '(857) 555-5678', '{"phone": "(857) 555-5678"}', 15, '2025-08-22T05:19:21.046338'),
('e0e9091f-509d-44b4-99f8-6f7eb5fad19d', '7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'f2222222-2222-2222-2222-222222222222', 4, 'both', '{"buy_or_sell": "both"}', 25, '2025-08-22T05:19:21.046338'),
('401fa94e-5f83-4fe1-8e4e-dd2f8aaa72d5', '7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'f2222222-2222-2222-2222-222222222222', 5, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-22T05:19:21.046338'),
('e91ef06d-082c-485e-9f63-1e8d2c4442bd', '7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'f2222222-2222-2222-2222-222222222222', 6, 'in_process', '{"mortgage_status": "in_process"}', 15, '2025-08-22T05:19:21.046338'),
('977272d2-8065-406e-a59c-0ddbb3024d2b', '7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'f2222222-2222-2222-2222-222222222222', 7, '$300k_500k', '{"price_range": "$300k_500k"}', 25, '2025-08-22T05:19:21.046338'),
('289c5025-2bf3-4c15-8d23-4d5d02cfc1e4', '7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'f2222222-2222-2222-2222-222222222222', 8, 'brookline_newton', '{"areas": "brookline_newton"}', 10, '2025-08-22T05:19:21.046338'),
('9d90184f-0e41-447b-93a6-5a83d2acad61', '7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-22T05:19:21.046338'),
('b78a328d-354e-43d2-a46d-a6ff3b3409f6', '7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'f2222222-2222-2222-2222-222222222222', 10, '2_bedrooms', '{"bedrooms": "2_bedrooms"}', 10, '2025-08-22T05:19:21.046338'),
('ba239a61-211a-48ee-a52c-f124c7b2e102', '7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'f2222222-2222-2222-2222-222222222222', 11, 'yes', '{"worked_with_realtor": "yes"}', 10, '2025-08-22T05:19:21.046338'),
('8e77cf2d-7f2d-4e26-92a1-f77bf8475def', '7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'f2222222-2222-2222-2222-222222222222', 12, 'medium', '{"urgency": "medium"}', 10, '2025-08-22T05:19:21.046338');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('5c353607-a130-4a16-9a1c-4e3ace71e8d2', '7a5aff8f-771f-477d-9b6e-2b3fcfd81ae5', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Mark_4 Thompson", "email": "mark.thompson_4@startup.io", "phone": "(857) 555-5678"}', 85, 0.85, true, false, NULL, NULL, NULL);


-- Lead 18: Qualified - Amanda_4 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('d15f22aa-0137-476e-8c04-e094dd78309c', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_018_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-18T14:19:21.046407', '2025-08-18T14:54:21.046408', '2025-08-18T14:54:21.046408', 9, true, 92, 92, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.64', '{"device_type": "desktop", "completion_time": 60}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('5efe84ce-9e9c-4107-92f2-5d82b8b6e3ee', 'd15f22aa-0137-476e-8c04-e094dd78309c', 'referral', 'referral', 'luxury_sellers', 'home buying agent', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('062d92d7-e13b-4640-be0a-418e5b5ebbc2', 'd15f22aa-0137-476e-8c04-e094dd78309c', 'f2222222-2222-2222-2222-222222222222', 1, 'Amanda_4 Rodriguez', '{"name": "Amanda_4 Rodriguez"}', 10, '2025-08-18T14:19:21.046407'),
('5c08d585-b3de-41ef-b3bf-c3da0e423d48', 'd15f22aa-0137-476e-8c04-e094dd78309c', 'f2222222-2222-2222-2222-222222222222', 2, 'arodriguez_4@lawfirm.com', '{"email": "arodriguez_4@lawfirm.com"}', 10, '2025-08-18T14:19:21.046407'),
('13afb39b-7124-4edb-acc2-0cc23c53058e', 'd15f22aa-0137-476e-8c04-e094dd78309c', 'f2222222-2222-2222-2222-222222222222', 3, '(617) 555-9012', '{"phone": "(617) 555-9012"}', 15, '2025-08-18T14:19:21.046407'),
('c544ae37-146e-4e1f-a00d-c514daa78e7d', 'd15f22aa-0137-476e-8c04-e094dd78309c', 'f2222222-2222-2222-2222-222222222222', 4, 'sell', '{"buy_or_sell": "sell"}', 20, '2025-08-18T14:19:21.046407'),
('d15a20e4-dff3-4780-a07b-c5ccade89ca8', 'd15f22aa-0137-476e-8c04-e094dd78309c', 'f2222222-2222-2222-2222-222222222222', 5, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-18T14:19:21.046407'),
('0e3cd270-4229-4a94-911a-c89cc2798f3a', 'd15f22aa-0137-476e-8c04-e094dd78309c', 'f2222222-2222-2222-2222-222222222222', 6, 'cash', '{"mortgage_status": "cash"}', 25, '2025-08-18T14:19:21.046407'),
('fcedb66e-6061-4ab8-9f31-5fee68165087', 'd15f22aa-0137-476e-8c04-e094dd78309c', 'f2222222-2222-2222-2222-222222222222', 7, '$500k_plus', '{"price_range": "$500k_plus"}', 20, '2025-08-18T14:19:21.046407'),
('ba6c845a-b786-4d1f-b2fb-fe4df80c8fae', 'd15f22aa-0137-476e-8c04-e094dd78309c', 'f2222222-2222-2222-2222-222222222222', 8, 'boston_cambridge', '{"areas": "boston_cambridge"}', 10, '2025-08-18T14:19:21.046407'),
('7220df76-9212-4d4c-95df-212a4d2ef99f', 'd15f22aa-0137-476e-8c04-e094dd78309c', 'f2222222-2222-2222-2222-222222222222', 9, 'no', '{"first_time_buyer": "no"}', 10, '2025-08-18T14:19:21.046407'),
('e1b8c232-17bd-4b41-9627-1cea814fc2ba', 'd15f22aa-0137-476e-8c04-e094dd78309c', 'f2222222-2222-2222-2222-222222222222', 10, '4_bedrooms', '{"bedrooms": "4_bedrooms"}', 10, '2025-08-18T14:19:21.046407'),
('2e0627eb-0a59-411f-8389-90f9369a8a77', 'd15f22aa-0137-476e-8c04-e094dd78309c', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-18T14:19:21.046407'),
('4857fa00-5cc8-40f6-b601-2686abb74136', 'd15f22aa-0137-476e-8c04-e094dd78309c', 'f2222222-2222-2222-2222-222222222222', 12, 'high', '{"urgency": "high"}', 10, '2025-08-18T14:19:21.046407');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('1e82caf4-c06f-467b-b9a7-5bcc3e088927', 'd15f22aa-0137-476e-8c04-e094dd78309c', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Amanda_4 Rodriguez", "email": "arodriguez_4@lawfirm.com", "phone": "(617) 555-9012"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 19: Unqualified - Kevin_4 O''Brien
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('c113d503-42c8-427d-875c-668ed8a72e31', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_019_unqualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-14T13:19:21.046472', '2025-08-14T14:04:21.046473', '2025-08-14T14:04:21.046473', 12, true, 35, 35, 'no', 'qualified', 'Thank you for your interest. While we may not be the best fit for your current needs, please reach out if your situation changes.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.233', '{"device_type": "mobile", "completion_time": 40}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('b354bd17-6a05-4b82-9e04-f9e0c49521d9', 'c113d503-42c8-427d-875c-668ed8a72e31', 'organic', 'search', 'general_search', 'property specialist', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('34ec260d-0ad7-4dd0-bee5-eb0ebc773f67', 'c113d503-42c8-427d-875c-668ed8a72e31', 'f2222222-2222-2222-2222-222222222222', 1, 'Kevin_4 O''Brien', '{"name": "Kevin_4 O''Brien"}', 10, '2025-08-14T13:19:21.046472'),
('86a5086d-7b44-4cd1-9138-77d49379c1ad', 'c113d503-42c8-427d-875c-668ed8a72e31', 'f2222222-2222-2222-2222-222222222222', 2, 'kevin.obrien_4@email.com', '{"email": "kevin.obrien_4@email.com"}', 10, '2025-08-14T13:19:21.046472'),
('a5866874-3726-4822-a9f0-2400ad36360b', 'c113d503-42c8-427d-875c-668ed8a72e31', 'f2222222-2222-2222-2222-222222222222', 3, '(508) 555-3456', '{"phone": "(508) 555-3456"}', 15, '2025-08-14T13:19:21.046472'),
('83ff33ba-1468-4f33-ab89-07cf4862890c', 'c113d503-42c8-427d-875c-668ed8a72e31', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-14T13:19:21.046472'),
('9088498d-df7d-4872-9d5f-a470c60b8976', 'c113d503-42c8-427d-875c-668ed8a72e31', 'f2222222-2222-2222-2222-222222222222', 5, 'just_browsing', '{"timeline": "just_browsing"}', 0, '2025-08-14T13:19:21.046472'),
('467d0ff4-809f-4b72-91ec-fa729e208b1f', 'c113d503-42c8-427d-875c-668ed8a72e31', 'f2222222-2222-2222-2222-222222222222', 6, 'planning_to_get', '{"mortgage_status": "planning_to_get"}', 10, '2025-08-14T13:19:21.046472'),
('5eb12f01-c4db-4de1-bcef-2977ec601ccf', 'c113d503-42c8-427d-875c-668ed8a72e31', 'f2222222-2222-2222-2222-222222222222', 7, 'under_200k', '{"price_range": "under_200k"}', 5, '2025-08-14T13:19:21.046472'),
('cc079485-ae0c-4390-be51-70ab6ec1b6e8', 'c113d503-42c8-427d-875c-668ed8a72e31', 'f2222222-2222-2222-2222-222222222222', 8, 'other_metro', '{"areas": "other_metro"}', 10, '2025-08-14T13:19:21.046472'),
('94840e54-4c05-4c84-8e4b-abb6cc345837', 'c113d503-42c8-427d-875c-668ed8a72e31', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-14T13:19:21.046472'),
('6aa349b9-ceef-49f7-ae0a-4d7da143e727', 'c113d503-42c8-427d-875c-668ed8a72e31', 'f2222222-2222-2222-2222-222222222222', 10, '1_bedroom', '{"bedrooms": "1_bedroom"}', 10, '2025-08-14T13:19:21.046472'),
('9b7683e0-4be0-4697-aa8d-9384c3f3b6da', 'c113d503-42c8-427d-875c-668ed8a72e31', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-14T13:19:21.046472'),
('3eba4e2b-5459-40a7-9de6-ad7896d56b3f', 'c113d503-42c8-427d-875c-668ed8a72e31', 'f2222222-2222-2222-2222-222222222222', 12, 'low', '{"urgency": "low"}', 10, '2025-08-14T13:19:21.046472');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('c4aff2a8-bd60-49fb-b5ba-401195db9e95', 'c113d503-42c8-427d-875c-668ed8a72e31', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'unqualified', '{"name": "Kevin_4 O''Brien", "email": "kevin.obrien_4@email.com", "phone": "(508) 555-3456"}', 35, 0.35, false, false, NULL, NULL, NULL);


-- Lead 20: Maybe - Lisa_4 Martinez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('d047d95c-8b4d-4712-94f2-37fc4706712d', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_020_maybe', 'a2222222-2222-2222-2222-222222222222', '2025-08-20T12:19:21.046537', '2025-08-20T12:41:21.046538', '2025-08-20T12:41:21.046538', 8, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to match you with the right agent. Expect to hear from us within 2-3 days.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.181', '{"device_type": "desktop", "completion_time": 34}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('8052079a-91f2-4a7a-9d30-b31f2a7631fd', 'd047d95c-8b4d-4712-94f2-37fc4706712d', 'google', 'cpc', 'affordable_homes', 'boston realtor', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('2482f68b-1eb0-417a-b707-c14e190e7032', 'd047d95c-8b4d-4712-94f2-37fc4706712d', 'f2222222-2222-2222-2222-222222222222', 1, 'Lisa_4 Martinez', '{"name": "Lisa_4 Martinez"}', 10, '2025-08-20T12:19:21.046537'),
('0030b5dc-794d-4257-b970-6df6a21b1032', 'd047d95c-8b4d-4712-94f2-37fc4706712d', 'f2222222-2222-2222-2222-222222222222', 2, 'lisa.martinez_4@hospital.org', '{"email": "lisa.martinez_4@hospital.org"}', 10, '2025-08-20T12:19:21.046537'),
('ea5641d6-e13a-47dc-a18e-fb29df7b0f84', 'd047d95c-8b4d-4712-94f2-37fc4706712d', 'f2222222-2222-2222-2222-222222222222', 3, '(781) 555-7890', '{"phone": "(781) 555-7890"}', 15, '2025-08-20T12:19:21.046537'),
('ff3ea969-fbe8-4fb5-af8a-351ddd0d36a7', 'd047d95c-8b4d-4712-94f2-37fc4706712d', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-20T12:19:21.046537'),
('55754495-03ff-4a24-915f-7ac5618f51fe', 'd047d95c-8b4d-4712-94f2-37fc4706712d', 'f2222222-2222-2222-2222-222222222222', 5, '6_12_months', '{"timeline": "6_12_months"}', 10, '2025-08-20T12:19:21.046537'),
('4c0533a5-fdc3-4f9b-af1e-6d0ed97421e1', 'd047d95c-8b4d-4712-94f2-37fc4706712d', 'f2222222-2222-2222-2222-222222222222', 6, 'in_process', '{"mortgage_status": "in_process"}', 15, '2025-08-20T12:19:21.046537'),
('a996d8ce-76ee-4106-80d4-547cd7fbaccb', 'd047d95c-8b4d-4712-94f2-37fc4706712d', 'f2222222-2222-2222-2222-222222222222', 7, '$200k_300k', '{"price_range": "$200k_300k"}', 15, '2025-08-20T12:19:21.046537'),
('bcf0c13f-431f-4621-8064-b28e48ac8223', 'd047d95c-8b4d-4712-94f2-37fc4706712d', 'f2222222-2222-2222-2222-222222222222', 8, 'other_metro', '{"areas": "other_metro"}', 10, '2025-08-20T12:19:21.046537'),
('0f902b0d-e157-4992-b8e0-1371f38a3dd3', 'd047d95c-8b4d-4712-94f2-37fc4706712d', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-20T12:19:21.046537'),
('fe12178c-e453-4658-9000-faa9b7d7798f', 'd047d95c-8b4d-4712-94f2-37fc4706712d', 'f2222222-2222-2222-2222-222222222222', 10, '2_bedrooms', '{"bedrooms": "2_bedrooms"}', 10, '2025-08-20T12:19:21.046537'),
('d20a09c8-9ece-413b-842a-88ef559c953f', 'd047d95c-8b4d-4712-94f2-37fc4706712d', 'f2222222-2222-2222-2222-222222222222', 11, 'yes', '{"worked_with_realtor": "yes"}', 10, '2025-08-20T12:19:21.046537'),
('5a487996-c6cf-4265-ac3c-0457feacf64a', 'd047d95c-8b4d-4712-94f2-37fc4706712d', 'f2222222-2222-2222-2222-222222222222', 12, 'medium', '{"urgency": "medium"}', 10, '2025-08-20T12:19:21.046537');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('db639a74-349c-452b-97a4-f4a61b059772', 'd047d95c-8b4d-4712-94f2-37fc4706712d', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'maybe', '{"name": "Lisa_4 Martinez", "email": "lisa.martinez_4@hospital.org", "phone": "(781) 555-7890"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 21: Qualified - Jessica_5 Chen
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('57476498-5241-43d9-b5de-3bd9e6acd747', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_021_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-19T23:19:21.046604', '2025-08-19T23:39:21.046605', '2025-08-19T23:39:21.046605', 9, true, 90, 90, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.147', '{"device_type": "desktop", "completion_time": 59}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('16e15b96-1b11-4321-bc90-96e328df46ea', '57476498-5241-43d9-b5de-3bd9e6acd747', 'google', 'cpc', 'luxury_homes_boston', 'boston realtor', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('008515cf-e342-4e50-abad-968874a95fbe', '57476498-5241-43d9-b5de-3bd9e6acd747', 'f2222222-2222-2222-2222-222222222222', 1, 'Jessica_5 Chen', '{"name": "Jessica_5 Chen"}', 10, '2025-08-19T23:19:21.046604'),
('6a64691c-9bc6-4d88-9af2-f1fa5d247cba', '57476498-5241-43d9-b5de-3bd9e6acd747', 'f2222222-2222-2222-2222-222222222222', 2, 'jessica.chen_5@techcorp.com', '{"email": "jessica.chen_5@techcorp.com"}', 10, '2025-08-19T23:19:21.046604'),
('df1ebc18-932a-4798-9c3f-5da3398468e1', '57476498-5241-43d9-b5de-3bd9e6acd747', 'f2222222-2222-2222-2222-222222222222', 3, '(617) 555-1234', '{"phone": "(617) 555-1234"}', 15, '2025-08-19T23:19:21.046604'),
('890a2fba-63b6-4e66-8024-94562256f48a', '57476498-5241-43d9-b5de-3bd9e6acd747', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-19T23:19:21.046604'),
('88888f3f-64aa-4f9a-86ec-22627c3756f0', '57476498-5241-43d9-b5de-3bd9e6acd747', 'f2222222-2222-2222-2222-222222222222', 5, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-19T23:19:21.046604'),
('99a3942b-4ec2-496b-ba4f-5611e4553227', '57476498-5241-43d9-b5de-3bd9e6acd747', 'f2222222-2222-2222-2222-222222222222', 6, 'pre_approved', '{"mortgage_status": "pre_approved"}', 20, '2025-08-19T23:19:21.046604'),
('fb6afe10-efce-4dad-aad0-d3fb1cf98e6e', '57476498-5241-43d9-b5de-3bd9e6acd747', 'f2222222-2222-2222-2222-222222222222', 7, '$500k_plus', '{"price_range": "$500k_plus"}', 20, '2025-08-19T23:19:21.046604'),
('3c3fbb49-a08c-4137-8327-c3cf6f0cf0fd', '57476498-5241-43d9-b5de-3bd9e6acd747', 'f2222222-2222-2222-2222-222222222222', 8, 'boston_cambridge', '{"areas": "boston_cambridge"}', 10, '2025-08-19T23:19:21.046604'),
('3ec62be9-fdb0-4af0-998a-ad8e53ea23c2', '57476498-5241-43d9-b5de-3bd9e6acd747', 'f2222222-2222-2222-2222-222222222222', 9, 'no', '{"first_time_buyer": "no"}', 10, '2025-08-19T23:19:21.046604'),
('c7e4f0ac-2168-41f6-a4eb-287839ec1e11', '57476498-5241-43d9-b5de-3bd9e6acd747', 'f2222222-2222-2222-2222-222222222222', 10, '3_bedrooms', '{"bedrooms": "3_bedrooms"}', 10, '2025-08-19T23:19:21.046604'),
('becb10f0-4555-4ec7-bbf1-fa9bb3e26f83', '57476498-5241-43d9-b5de-3bd9e6acd747', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-19T23:19:21.046604'),
('dfda163f-ca26-480b-aec5-27afb52a9821', '57476498-5241-43d9-b5de-3bd9e6acd747', 'f2222222-2222-2222-2222-222222222222', 12, 'high', '{"urgency": "high"}', 10, '2025-08-19T23:19:21.046604');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('207fb935-d48a-4797-9291-7a32dc20af7f', '57476498-5241-43d9-b5de-3bd9e6acd747', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Jessica_5 Chen", "email": "jessica.chen_5@techcorp.com", "phone": "(617) 555-1234"}', 90, 0.90, true, false, NULL, NULL, NULL);


-- Lead 22: Qualified - Mark_5 Thompson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('292b2903-cd72-4e51-9a86-d871e10c02ef', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_022_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-23T03:19:21.046670', '2025-08-23T04:02:21.046671', '2025-08-23T04:02:21.046671', 7, true, 85, 85, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.127', '{"device_type": "mobile", "completion_time": 58}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('aac680a6-48fc-435d-ae56-e537b6711c50', '292b2903-cd72-4e51-9a86-d871e10c02ef', 'facebook', 'social', 'first_time_buyers', 'home buying agent', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('455786d1-80b4-41cf-b1d5-e166fbc69f95', '292b2903-cd72-4e51-9a86-d871e10c02ef', 'f2222222-2222-2222-2222-222222222222', 1, 'Mark_5 Thompson', '{"name": "Mark_5 Thompson"}', 10, '2025-08-23T03:19:21.046670'),
('fcfc928b-93c7-4a0b-bc1a-ff919ade8aa4', '292b2903-cd72-4e51-9a86-d871e10c02ef', 'f2222222-2222-2222-2222-222222222222', 2, 'mark.thompson_5@startup.io', '{"email": "mark.thompson_5@startup.io"}', 10, '2025-08-23T03:19:21.046670'),
('39efad65-1e41-45c4-89c8-dd3e59ea2757', '292b2903-cd72-4e51-9a86-d871e10c02ef', 'f2222222-2222-2222-2222-222222222222', 3, '(857) 555-5678', '{"phone": "(857) 555-5678"}', 15, '2025-08-23T03:19:21.046670'),
('d36a784d-bc25-41fb-bb6b-4dbf96a0364b', '292b2903-cd72-4e51-9a86-d871e10c02ef', 'f2222222-2222-2222-2222-222222222222', 4, 'both', '{"buy_or_sell": "both"}', 25, '2025-08-23T03:19:21.046670'),
('ad6568f4-3a66-4f04-8c89-8b2ce29ad169', '292b2903-cd72-4e51-9a86-d871e10c02ef', 'f2222222-2222-2222-2222-222222222222', 5, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-23T03:19:21.046670'),
('e9952392-17e4-405a-b6a5-8c8a03aad421', '292b2903-cd72-4e51-9a86-d871e10c02ef', 'f2222222-2222-2222-2222-222222222222', 6, 'in_process', '{"mortgage_status": "in_process"}', 15, '2025-08-23T03:19:21.046670'),
('37749136-3d46-4faa-a1b6-0235632bd00a', '292b2903-cd72-4e51-9a86-d871e10c02ef', 'f2222222-2222-2222-2222-222222222222', 7, '$300k_500k', '{"price_range": "$300k_500k"}', 25, '2025-08-23T03:19:21.046670'),
('14cf39c8-b495-4911-aefa-c4c33f592735', '292b2903-cd72-4e51-9a86-d871e10c02ef', 'f2222222-2222-2222-2222-222222222222', 8, 'brookline_newton', '{"areas": "brookline_newton"}', 10, '2025-08-23T03:19:21.046670'),
('040b4376-9d67-4a87-83a3-36996f86a9b1', '292b2903-cd72-4e51-9a86-d871e10c02ef', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-23T03:19:21.046670'),
('bf22c8c1-ec9d-4a09-8f1b-1b7882781556', '292b2903-cd72-4e51-9a86-d871e10c02ef', 'f2222222-2222-2222-2222-222222222222', 10, '2_bedrooms', '{"bedrooms": "2_bedrooms"}', 10, '2025-08-23T03:19:21.046670'),
('08bc47a3-117a-4b1a-9144-53b0199c47f1', '292b2903-cd72-4e51-9a86-d871e10c02ef', 'f2222222-2222-2222-2222-222222222222', 11, 'yes', '{"worked_with_realtor": "yes"}', 10, '2025-08-23T03:19:21.046670'),
('670358c9-45b8-42ef-b6ea-b951e9ba457e', '292b2903-cd72-4e51-9a86-d871e10c02ef', 'f2222222-2222-2222-2222-222222222222', 12, 'medium', '{"urgency": "medium"}', 10, '2025-08-23T03:19:21.046670');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('3b418dc8-2579-4d7e-b498-5385c921f3ae', '292b2903-cd72-4e51-9a86-d871e10c02ef', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Mark_5 Thompson", "email": "mark.thompson_5@startup.io", "phone": "(857) 555-5678"}', 85, 0.85, true, false, NULL, NULL, NULL);


-- Lead 23: Qualified - Amanda_5 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('f4811269-cbad-4983-a9a7-f76c14ed186b', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_023_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-11T14:19:21.046735', '2025-08-11T14:59:21.046736', '2025-08-11T14:59:21.046736', 12, true, 92, 92, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.236', '{"device_type": "desktop", "completion_time": 49}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('ad451beb-bb62-4458-8c74-c07ef33edbaa', 'f4811269-cbad-4983-a9a7-f76c14ed186b', 'referral', 'referral', 'luxury_sellers', 'home buying agent', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('6cfad282-a0c8-4c02-88fa-4178c63ad34f', 'f4811269-cbad-4983-a9a7-f76c14ed186b', 'f2222222-2222-2222-2222-222222222222', 1, 'Amanda_5 Rodriguez', '{"name": "Amanda_5 Rodriguez"}', 10, '2025-08-11T14:19:21.046735'),
('57c18e30-9c82-4f0c-accd-c76d86e89eff', 'f4811269-cbad-4983-a9a7-f76c14ed186b', 'f2222222-2222-2222-2222-222222222222', 2, 'arodriguez_5@lawfirm.com', '{"email": "arodriguez_5@lawfirm.com"}', 10, '2025-08-11T14:19:21.046735'),
('53c6a838-befb-40dd-aee9-9aaed540466d', 'f4811269-cbad-4983-a9a7-f76c14ed186b', 'f2222222-2222-2222-2222-222222222222', 3, '(617) 555-9012', '{"phone": "(617) 555-9012"}', 15, '2025-08-11T14:19:21.046735'),
('f0a4decc-506f-45ee-a2f3-a876cb742fae', 'f4811269-cbad-4983-a9a7-f76c14ed186b', 'f2222222-2222-2222-2222-222222222222', 4, 'sell', '{"buy_or_sell": "sell"}', 20, '2025-08-11T14:19:21.046735'),
('4f0e386f-6f91-4db7-a9f4-1d3f7ffbab3a', 'f4811269-cbad-4983-a9a7-f76c14ed186b', 'f2222222-2222-2222-2222-222222222222', 5, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-11T14:19:21.046735'),
('69146ed6-b97e-4712-9ec1-be30294f2842', 'f4811269-cbad-4983-a9a7-f76c14ed186b', 'f2222222-2222-2222-2222-222222222222', 6, 'cash', '{"mortgage_status": "cash"}', 25, '2025-08-11T14:19:21.046735'),
('222ca956-601f-43f1-b5a6-460d3d10614c', 'f4811269-cbad-4983-a9a7-f76c14ed186b', 'f2222222-2222-2222-2222-222222222222', 7, '$500k_plus', '{"price_range": "$500k_plus"}', 20, '2025-08-11T14:19:21.046735'),
('d0eb03d7-d648-481c-b913-8e255460b53c', 'f4811269-cbad-4983-a9a7-f76c14ed186b', 'f2222222-2222-2222-2222-222222222222', 8, 'boston_cambridge', '{"areas": "boston_cambridge"}', 10, '2025-08-11T14:19:21.046735'),
('dfabe602-7c73-40f4-9873-215592b9fc6d', 'f4811269-cbad-4983-a9a7-f76c14ed186b', 'f2222222-2222-2222-2222-222222222222', 9, 'no', '{"first_time_buyer": "no"}', 10, '2025-08-11T14:19:21.046735'),
('1808b244-43ad-41c2-afa8-d3652dbc33dc', 'f4811269-cbad-4983-a9a7-f76c14ed186b', 'f2222222-2222-2222-2222-222222222222', 10, '4_bedrooms', '{"bedrooms": "4_bedrooms"}', 10, '2025-08-11T14:19:21.046735'),
('581c55a9-5552-4b95-a1aa-fe8c402a1558', 'f4811269-cbad-4983-a9a7-f76c14ed186b', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-11T14:19:21.046735'),
('24264752-d6f3-4564-931d-7e30de0b4afb', 'f4811269-cbad-4983-a9a7-f76c14ed186b', 'f2222222-2222-2222-2222-222222222222', 12, 'high', '{"urgency": "high"}', 10, '2025-08-11T14:19:21.046735');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('b72c0bf0-d7c7-4b55-901d-fa1d2b5990f8', 'f4811269-cbad-4983-a9a7-f76c14ed186b', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Amanda_5 Rodriguez", "email": "arodriguez_5@lawfirm.com", "phone": "(617) 555-9012"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 24: Unqualified - Kevin_5 O''Brien
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_024_unqualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-22T14:19:21.046799', '2025-08-22T15:00:21.046800', '2025-08-22T15:00:21.046800', 8, true, 35, 35, 'no', 'qualified', 'Thank you for your interest. While we may not be the best fit for your current needs, please reach out if your situation changes.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.150', '{"device_type": "mobile", "completion_time": 16}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('dcaeab12-8e89-42b5-8137-13c51f07e582', 'afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'organic', 'search', 'general_search', 'cambridge real estate', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Brookline');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('c5f60cda-98d5-4aa3-9821-d14d7b16914c', 'afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'f2222222-2222-2222-2222-222222222222', 1, 'Kevin_5 O''Brien', '{"name": "Kevin_5 O''Brien"}', 10, '2025-08-22T14:19:21.046799'),
('b034844a-a85e-42c2-832c-98a191399444', 'afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'f2222222-2222-2222-2222-222222222222', 2, 'kevin.obrien_5@email.com', '{"email": "kevin.obrien_5@email.com"}', 10, '2025-08-22T14:19:21.046799'),
('ee259f7e-08bf-4c8d-9e88-401b48610546', 'afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'f2222222-2222-2222-2222-222222222222', 3, '(508) 555-3456', '{"phone": "(508) 555-3456"}', 15, '2025-08-22T14:19:21.046799'),
('d92f5ca8-b6e5-460f-83c5-adb6590bbe5f', 'afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-22T14:19:21.046799'),
('eb7a2427-27f0-4cba-a8cb-24b296c91424', 'afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'f2222222-2222-2222-2222-222222222222', 5, 'just_browsing', '{"timeline": "just_browsing"}', 0, '2025-08-22T14:19:21.046799'),
('b1ec6bcd-4dd4-45eb-b711-2725e3f61dae', 'afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'f2222222-2222-2222-2222-222222222222', 6, 'planning_to_get', '{"mortgage_status": "planning_to_get"}', 10, '2025-08-22T14:19:21.046799'),
('8b7f6483-401c-4ebd-89cf-4d6be491b857', 'afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'f2222222-2222-2222-2222-222222222222', 7, 'under_200k', '{"price_range": "under_200k"}', 5, '2025-08-22T14:19:21.046799'),
('d022d5a3-cced-492e-a878-a297df92be91', 'afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'f2222222-2222-2222-2222-222222222222', 8, 'other_metro', '{"areas": "other_metro"}', 10, '2025-08-22T14:19:21.046799'),
('643a5bac-96cc-4b83-b315-ee51a21e87bb', 'afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-22T14:19:21.046799'),
('cbf573eb-9e9d-4a4d-8f70-469bb572277b', 'afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'f2222222-2222-2222-2222-222222222222', 10, '1_bedroom', '{"bedrooms": "1_bedroom"}', 10, '2025-08-22T14:19:21.046799'),
('933913ea-3166-4dcd-bcd1-7f893595fe39', 'afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-22T14:19:21.046799'),
('307f92a4-0317-4fec-943d-2a5d45fbfe9c', 'afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'f2222222-2222-2222-2222-222222222222', 12, 'low', '{"urgency": "low"}', 10, '2025-08-22T14:19:21.046799');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('75f2f885-ed9d-4060-88c0-1d051899bca5', 'afd66fdc-6340-4af8-9c99-5b8b9ea598bb', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'unqualified', '{"name": "Kevin_5 O''Brien", "email": "kevin.obrien_5@email.com", "phone": "(508) 555-3456"}', 35, 0.35, false, false, NULL, NULL, NULL);


-- Lead 25: Maybe - Lisa_5 Martinez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_025_maybe', 'a2222222-2222-2222-2222-222222222222', '2025-08-24T07:19:21.046866', '2025-08-24T07:50:21.046866', '2025-08-24T07:50:21.046866', 7, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to match you with the right agent. Expect to hear from us within 2-3 days.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.136', '{"device_type": "desktop", "completion_time": 28}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('b20c8025-52df-40c7-9a42-179a93835d46', '831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'google', 'cpc', 'affordable_homes', 'cambridge real estate', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('7b4664cc-8d5e-4007-bd55-45ce869609c6', '831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'f2222222-2222-2222-2222-222222222222', 1, 'Lisa_5 Martinez', '{"name": "Lisa_5 Martinez"}', 10, '2025-08-24T07:19:21.046866'),
('37193d06-8655-4b4a-880e-94cee6c3a068', '831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'f2222222-2222-2222-2222-222222222222', 2, 'lisa.martinez_5@hospital.org', '{"email": "lisa.martinez_5@hospital.org"}', 10, '2025-08-24T07:19:21.046866'),
('9bd3d14f-e37b-4e91-9570-4d7217195594', '831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'f2222222-2222-2222-2222-222222222222', 3, '(781) 555-7890', '{"phone": "(781) 555-7890"}', 15, '2025-08-24T07:19:21.046866'),
('ba892bf7-6cd8-4c5f-a5a2-f8eccd37a6f8', '831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-24T07:19:21.046866'),
('e0533fcf-8142-40f7-8e76-3c3ab8c41abe', '831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'f2222222-2222-2222-2222-222222222222', 5, '6_12_months', '{"timeline": "6_12_months"}', 10, '2025-08-24T07:19:21.046866'),
('48a56f78-fa88-42ec-b4ef-5a17860d576e', '831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'f2222222-2222-2222-2222-222222222222', 6, 'in_process', '{"mortgage_status": "in_process"}', 15, '2025-08-24T07:19:21.046866'),
('5ac6ffb7-4d62-408b-ba1d-981ce0215fcb', '831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'f2222222-2222-2222-2222-222222222222', 7, '$200k_300k', '{"price_range": "$200k_300k"}', 15, '2025-08-24T07:19:21.046866'),
('0b50d2c4-ab16-42a0-b79d-1794d534139c', '831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'f2222222-2222-2222-2222-222222222222', 8, 'other_metro', '{"areas": "other_metro"}', 10, '2025-08-24T07:19:21.046866'),
('621d20b9-e25f-4279-aa4d-16b8b961d176', '831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-24T07:19:21.046866'),
('81c81799-d617-4692-bf19-fd5c62f3a349', '831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'f2222222-2222-2222-2222-222222222222', 10, '2_bedrooms', '{"bedrooms": "2_bedrooms"}', 10, '2025-08-24T07:19:21.046866'),
('edb52768-85ea-4bcd-9a22-7eedc4f28b6f', '831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'f2222222-2222-2222-2222-222222222222', 11, 'yes', '{"worked_with_realtor": "yes"}', 10, '2025-08-24T07:19:21.046866'),
('68e07986-ddb8-4777-a70f-68d0e42f3e98', '831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'f2222222-2222-2222-2222-222222222222', 12, 'medium', '{"urgency": "medium"}', 10, '2025-08-24T07:19:21.046866');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('600a65d9-026a-4105-8d6d-784746e2d0b9', '831fae0c-a9a0-4841-a3c3-5d49f8f79d71', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'maybe', '{"name": "Lisa_5 Martinez", "email": "lisa.martinez_5@hospital.org", "phone": "(781) 555-7890"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 26: Qualified - Jessica_6 Chen
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_026_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-15T17:19:21.046930', '2025-08-15T18:01:21.046931', '2025-08-15T18:01:21.046931', 10, true, 90, 90, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.47', '{"device_type": "desktop", "completion_time": 43}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('0e42d4d7-4c5c-41a2-adae-5bba32671152', 'aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'google', 'cpc', 'luxury_homes_boston', 'cambridge real estate', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('39e02e7f-7f78-4ed8-ba47-5222f00b9039', 'aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'f2222222-2222-2222-2222-222222222222', 1, 'Jessica_6 Chen', '{"name": "Jessica_6 Chen"}', 10, '2025-08-15T17:19:21.046930'),
('6d1da8c3-5b8f-42e0-ab1a-4de2ebf9b4b2', 'aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'f2222222-2222-2222-2222-222222222222', 2, 'jessica.chen_6@techcorp.com', '{"email": "jessica.chen_6@techcorp.com"}', 10, '2025-08-15T17:19:21.046930'),
('4469616a-ca89-4c7e-8a96-4a42cfcd586c', 'aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'f2222222-2222-2222-2222-222222222222', 3, '(617) 555-1234', '{"phone": "(617) 555-1234"}', 15, '2025-08-15T17:19:21.046930'),
('1c1e5844-642f-4f11-8400-412402c37c19', 'aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-15T17:19:21.046930'),
('943bc692-33b2-4cf2-9c38-409d07166e40', 'aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'f2222222-2222-2222-2222-222222222222', 5, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-15T17:19:21.046930'),
('74141c0d-2573-4265-8261-78a3c61cf9cd', 'aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'f2222222-2222-2222-2222-222222222222', 6, 'pre_approved', '{"mortgage_status": "pre_approved"}', 20, '2025-08-15T17:19:21.046930'),
('7e7720af-2d0e-4ecc-a9d7-714a70ccebc2', 'aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'f2222222-2222-2222-2222-222222222222', 7, '$500k_plus', '{"price_range": "$500k_plus"}', 20, '2025-08-15T17:19:21.046930'),
('9c9ca690-d001-4240-91b3-6352824a588b', 'aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'f2222222-2222-2222-2222-222222222222', 8, 'boston_cambridge', '{"areas": "boston_cambridge"}', 10, '2025-08-15T17:19:21.046930'),
('6d20816e-3d98-4f8e-8506-b762302eefe6', 'aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'f2222222-2222-2222-2222-222222222222', 9, 'no', '{"first_time_buyer": "no"}', 10, '2025-08-15T17:19:21.046930'),
('fb8cf1f2-fad3-4747-a674-8b6a56e4e37e', 'aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'f2222222-2222-2222-2222-222222222222', 10, '3_bedrooms', '{"bedrooms": "3_bedrooms"}', 10, '2025-08-15T17:19:21.046930'),
('7ca8cf45-2ff8-4cd1-b873-591f4f7ea7e8', 'aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-15T17:19:21.046930'),
('b1d76c41-7a1d-4152-919c-0b06d47dbfd7', 'aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'f2222222-2222-2222-2222-222222222222', 12, 'high', '{"urgency": "high"}', 10, '2025-08-15T17:19:21.046930');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('288bd213-c9d5-49ee-8288-2e3a7f720889', 'aec5fc53-b06f-4551-9f45-4d3a293ec4da', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Jessica_6 Chen", "email": "jessica.chen_6@techcorp.com", "phone": "(617) 555-1234"}', 90, 0.90, true, false, NULL, NULL, NULL);


-- Lead 27: Qualified - Mark_6 Thompson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('188a9091-a413-49af-980b-f56cb0de4e75', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_027_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-18T02:19:21.046995', '2025-08-18T02:52:21.046996', '2025-08-18T02:52:21.046996', 9, true, 85, 85, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.141', '{"device_type": "mobile", "completion_time": 52}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('436f45c0-d1cf-4141-ac3e-8a9d4931d54d', '188a9091-a413-49af-980b-f56cb0de4e75', 'facebook', 'social', 'first_time_buyers', 'property specialist', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('86985871-92dc-4ea8-93e7-05a484cb2c9e', '188a9091-a413-49af-980b-f56cb0de4e75', 'f2222222-2222-2222-2222-222222222222', 1, 'Mark_6 Thompson', '{"name": "Mark_6 Thompson"}', 10, '2025-08-18T02:19:21.046995'),
('e48de9ea-773b-4f2b-8ad0-1a0844292eb7', '188a9091-a413-49af-980b-f56cb0de4e75', 'f2222222-2222-2222-2222-222222222222', 2, 'mark.thompson_6@startup.io', '{"email": "mark.thompson_6@startup.io"}', 10, '2025-08-18T02:19:21.046995'),
('0b9b7569-2547-4901-a84f-dc6f4b899c77', '188a9091-a413-49af-980b-f56cb0de4e75', 'f2222222-2222-2222-2222-222222222222', 3, '(857) 555-5678', '{"phone": "(857) 555-5678"}', 15, '2025-08-18T02:19:21.046995'),
('32506aa7-11e8-4c6e-b97b-8ac8c1a9b8e0', '188a9091-a413-49af-980b-f56cb0de4e75', 'f2222222-2222-2222-2222-222222222222', 4, 'both', '{"buy_or_sell": "both"}', 25, '2025-08-18T02:19:21.046995'),
('2f57389d-f818-4826-b119-38957ae263f0', '188a9091-a413-49af-980b-f56cb0de4e75', 'f2222222-2222-2222-2222-222222222222', 5, '3_6_months', '{"timeline": "3_6_months"}', 20, '2025-08-18T02:19:21.046995'),
('4d3bc1e6-749f-406a-846b-44e7671eb044', '188a9091-a413-49af-980b-f56cb0de4e75', 'f2222222-2222-2222-2222-222222222222', 6, 'in_process', '{"mortgage_status": "in_process"}', 15, '2025-08-18T02:19:21.046995'),
('9c113429-734a-4ef4-aaf1-4619bb7f401f', '188a9091-a413-49af-980b-f56cb0de4e75', 'f2222222-2222-2222-2222-222222222222', 7, '$300k_500k', '{"price_range": "$300k_500k"}', 25, '2025-08-18T02:19:21.046995'),
('768a184b-8239-46e2-a93a-f2674561b69a', '188a9091-a413-49af-980b-f56cb0de4e75', 'f2222222-2222-2222-2222-222222222222', 8, 'brookline_newton', '{"areas": "brookline_newton"}', 10, '2025-08-18T02:19:21.046995'),
('28358878-191b-441c-9dfa-d1111cae3d90', '188a9091-a413-49af-980b-f56cb0de4e75', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-18T02:19:21.046995'),
('67775069-24a0-4119-9f38-c88f522d7e41', '188a9091-a413-49af-980b-f56cb0de4e75', 'f2222222-2222-2222-2222-222222222222', 10, '2_bedrooms', '{"bedrooms": "2_bedrooms"}', 10, '2025-08-18T02:19:21.046995'),
('2861cd74-fbd4-4743-8f58-56792f639b39', '188a9091-a413-49af-980b-f56cb0de4e75', 'f2222222-2222-2222-2222-222222222222', 11, 'yes', '{"worked_with_realtor": "yes"}', 10, '2025-08-18T02:19:21.046995'),
('cebd4ea7-7ecd-4c3d-9ca0-963e948d9cd7', '188a9091-a413-49af-980b-f56cb0de4e75', 'f2222222-2222-2222-2222-222222222222', 12, 'medium', '{"urgency": "medium"}', 10, '2025-08-18T02:19:21.046995');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('ec22c29c-7027-4779-ab26-94270d4ecada', '188a9091-a413-49af-980b-f56cb0de4e75', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Mark_6 Thompson", "email": "mark.thompson_6@startup.io", "phone": "(857) 555-5678"}', 85, 0.85, true, false, NULL, NULL, NULL);


-- Lead 28: Qualified - Amanda_6 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('ce8f69b5-a391-4941-a419-66b1237ecd8e', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_028_qualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-23T03:19:21.047059', '2025-08-23T04:00:21.047060', '2025-08-23T04:00:21.047060', 8, true, 92, 92, 'yes', 'qualified', 'Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.20', '{"device_type": "desktop", "completion_time": 22}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('828d0a60-c90a-4730-bd71-dbe537ce684c', 'ce8f69b5-a391-4941-a419-66b1237ecd8e', 'referral', 'referral', 'luxury_sellers', 'property specialist', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('76c899ee-bafa-487c-86ad-d0abd7dce596', 'ce8f69b5-a391-4941-a419-66b1237ecd8e', 'f2222222-2222-2222-2222-222222222222', 1, 'Amanda_6 Rodriguez', '{"name": "Amanda_6 Rodriguez"}', 10, '2025-08-23T03:19:21.047059'),
('89337f19-753a-4738-ac57-3896eb200766', 'ce8f69b5-a391-4941-a419-66b1237ecd8e', 'f2222222-2222-2222-2222-222222222222', 2, 'arodriguez_6@lawfirm.com', '{"email": "arodriguez_6@lawfirm.com"}', 10, '2025-08-23T03:19:21.047059'),
('e322156a-ca65-410c-a0ed-f017ba183122', 'ce8f69b5-a391-4941-a419-66b1237ecd8e', 'f2222222-2222-2222-2222-222222222222', 3, '(617) 555-9012', '{"phone": "(617) 555-9012"}', 15, '2025-08-23T03:19:21.047059'),
('b21340ee-df5f-4cda-9b0a-ffd131fbfe3f', 'ce8f69b5-a391-4941-a419-66b1237ecd8e', 'f2222222-2222-2222-2222-222222222222', 4, 'sell', '{"buy_or_sell": "sell"}', 20, '2025-08-23T03:19:21.047059'),
('78f86eff-39cb-4233-ae9e-f5d8338d1db9', 'ce8f69b5-a391-4941-a419-66b1237ecd8e', 'f2222222-2222-2222-2222-222222222222', 5, 'within_3_months', '{"timeline": "within_3_months"}', 25, '2025-08-23T03:19:21.047059'),
('305067de-71d6-443e-9a50-e40e98eeaac8', 'ce8f69b5-a391-4941-a419-66b1237ecd8e', 'f2222222-2222-2222-2222-222222222222', 6, 'cash', '{"mortgage_status": "cash"}', 25, '2025-08-23T03:19:21.047059'),
('7b2c2fb3-7202-4a5d-b2d1-cc496d14b685', 'ce8f69b5-a391-4941-a419-66b1237ecd8e', 'f2222222-2222-2222-2222-222222222222', 7, '$500k_plus', '{"price_range": "$500k_plus"}', 20, '2025-08-23T03:19:21.047059'),
('4c1e5fd1-a7e4-4c31-a31a-d0bb9c8fd018', 'ce8f69b5-a391-4941-a419-66b1237ecd8e', 'f2222222-2222-2222-2222-222222222222', 8, 'boston_cambridge', '{"areas": "boston_cambridge"}', 10, '2025-08-23T03:19:21.047059'),
('c74857b9-111a-4ddb-b10f-aeaf447b9c66', 'ce8f69b5-a391-4941-a419-66b1237ecd8e', 'f2222222-2222-2222-2222-222222222222', 9, 'no', '{"first_time_buyer": "no"}', 10, '2025-08-23T03:19:21.047059'),
('a84c400c-f834-4120-8023-92f0b0488f8b', 'ce8f69b5-a391-4941-a419-66b1237ecd8e', 'f2222222-2222-2222-2222-222222222222', 10, '4_bedrooms', '{"bedrooms": "4_bedrooms"}', 10, '2025-08-23T03:19:21.047059'),
('4343d6e7-c5b5-40ea-8ea9-78c4d4d42bfc', 'ce8f69b5-a391-4941-a419-66b1237ecd8e', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-23T03:19:21.047059'),
('c72260d0-001a-473b-92e8-24664c8be70b', 'ce8f69b5-a391-4941-a419-66b1237ecd8e', 'f2222222-2222-2222-2222-222222222222', 12, 'high', '{"urgency": "high"}', 10, '2025-08-23T03:19:21.047059');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('88c84f59-5c55-492b-86e0-cbe101bd7699', 'ce8f69b5-a391-4941-a419-66b1237ecd8e', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'qualified', '{"name": "Amanda_6 Rodriguez", "email": "arodriguez_6@lawfirm.com", "phone": "(617) 555-9012"}', 92, 0.92, true, false, NULL, NULL, NULL);


-- Lead 29: Unqualified - Kevin_6 O''Brien
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('02b4dc7e-b96f-473b-9aac-62527dda7316', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_029_unqualified', 'a2222222-2222-2222-2222-222222222222', '2025-08-22T12:19:21.047124', '2025-08-22T12:54:21.047125', '2025-08-22T12:54:21.047125', 7, true, 35, 35, 'no', 'qualified', 'Thank you for your interest. While we may not be the best fit for your current needs, please reach out if your situation changes.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.130', '{"device_type": "mobile", "completion_time": 25}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('58a6e444-8f8d-44d7-9428-1292ac96dd5f', '02b4dc7e-b96f-473b-9aac-62527dda7316', 'organic', 'search', 'general_search', 'boston realtor', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('9c67d3e1-5fdb-43aa-bcab-d4e80d9aa822', '02b4dc7e-b96f-473b-9aac-62527dda7316', 'f2222222-2222-2222-2222-222222222222', 1, 'Kevin_6 O''Brien', '{"name": "Kevin_6 O''Brien"}', 10, '2025-08-22T12:19:21.047124'),
('5b88036c-5912-4c6a-a17c-eb868dd511f8', '02b4dc7e-b96f-473b-9aac-62527dda7316', 'f2222222-2222-2222-2222-222222222222', 2, 'kevin.obrien_6@email.com', '{"email": "kevin.obrien_6@email.com"}', 10, '2025-08-22T12:19:21.047124'),
('cbd085b6-8619-4b40-b4d7-718712126b7e', '02b4dc7e-b96f-473b-9aac-62527dda7316', 'f2222222-2222-2222-2222-222222222222', 3, '(508) 555-3456', '{"phone": "(508) 555-3456"}', 15, '2025-08-22T12:19:21.047124'),
('01a7711e-db90-4a64-bfec-ab111b75db4c', '02b4dc7e-b96f-473b-9aac-62527dda7316', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-22T12:19:21.047124'),
('a6a01d9f-095c-45ff-8baa-9bb60625f649', '02b4dc7e-b96f-473b-9aac-62527dda7316', 'f2222222-2222-2222-2222-222222222222', 5, 'just_browsing', '{"timeline": "just_browsing"}', 0, '2025-08-22T12:19:21.047124'),
('19bd3921-9295-490e-9bff-5f2e7a9b2593', '02b4dc7e-b96f-473b-9aac-62527dda7316', 'f2222222-2222-2222-2222-222222222222', 6, 'planning_to_get', '{"mortgage_status": "planning_to_get"}', 10, '2025-08-22T12:19:21.047124'),
('1378b88f-76a8-4d32-8e4e-778a2db9d728', '02b4dc7e-b96f-473b-9aac-62527dda7316', 'f2222222-2222-2222-2222-222222222222', 7, 'under_200k', '{"price_range": "under_200k"}', 5, '2025-08-22T12:19:21.047124'),
('0b86b73a-795f-455a-ab7c-befcccc95660', '02b4dc7e-b96f-473b-9aac-62527dda7316', 'f2222222-2222-2222-2222-222222222222', 8, 'other_metro', '{"areas": "other_metro"}', 10, '2025-08-22T12:19:21.047124'),
('13d66abe-2d36-4a36-8694-8ca0f0da8ea9', '02b4dc7e-b96f-473b-9aac-62527dda7316', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-22T12:19:21.047124'),
('f3775f86-e7bc-4a07-93f1-c2f124ec66ae', '02b4dc7e-b96f-473b-9aac-62527dda7316', 'f2222222-2222-2222-2222-222222222222', 10, '1_bedroom', '{"bedrooms": "1_bedroom"}', 10, '2025-08-22T12:19:21.047124'),
('598526d8-7eb1-4b3e-af61-fa5df2e10e75', '02b4dc7e-b96f-473b-9aac-62527dda7316', 'f2222222-2222-2222-2222-222222222222', 11, 'no', '{"worked_with_realtor": "no"}', 10, '2025-08-22T12:19:21.047124'),
('5e8d0c3c-5b74-4f5a-b71c-f034299d1f5b', '02b4dc7e-b96f-473b-9aac-62527dda7316', 'f2222222-2222-2222-2222-222222222222', 12, 'low', '{"urgency": "low"}', 10, '2025-08-22T12:19:21.047124');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('6e2e2378-0d72-415a-8c2c-2eaff4763f8d', '02b4dc7e-b96f-473b-9aac-62527dda7316', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'unqualified', '{"name": "Kevin_6 O''Brien", "email": "kevin.obrien_6@email.com", "phone": "(508) 555-3456"}', 35, 0.35, false, false, NULL, NULL, NULL);


-- Lead 30: Maybe - Lisa_6 Martinez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'f2222222-2222-2222-2222-222222222222', 'metro_realty_030_maybe', 'a2222222-2222-2222-2222-222222222222', '2025-08-17T05:19:21.047190', '2025-08-17T06:00:21.047190', '2025-08-17T06:00:21.047190', 12, true, 65, 65, 'maybe', 'qualified', 'Thank you for your interest! We are reviewing your requirements to match you with the right agent. Expect to hear from us within 2-3 days.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.221', '{"device_type": "desktop", "completion_time": 26}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('5462ee50-4475-4af7-810e-278bed635467', '41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'google', 'cpc', 'affordable_homes', 'boston realtor', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('2bf40995-2fca-4ed9-932b-f794b7f43d26', '41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'f2222222-2222-2222-2222-222222222222', 1, 'Lisa_6 Martinez', '{"name": "Lisa_6 Martinez"}', 10, '2025-08-17T05:19:21.047190'),
('8e149c46-199f-4baa-8563-5b4695b70e90', '41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'f2222222-2222-2222-2222-222222222222', 2, 'lisa.martinez_6@hospital.org', '{"email": "lisa.martinez_6@hospital.org"}', 10, '2025-08-17T05:19:21.047190'),
('cb8b46f6-dbe6-4fd6-8348-81363644b688', '41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'f2222222-2222-2222-2222-222222222222', 3, '(781) 555-7890', '{"phone": "(781) 555-7890"}', 15, '2025-08-17T05:19:21.047190'),
('ef55889f-7c53-4fa5-8416-ec08eb49f01e', '41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'f2222222-2222-2222-2222-222222222222', 4, 'buy', '{"buy_or_sell": "buy"}', 15, '2025-08-17T05:19:21.047190'),
('d2592552-0a96-4588-9795-b3a040e51320', '41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'f2222222-2222-2222-2222-222222222222', 5, '6_12_months', '{"timeline": "6_12_months"}', 10, '2025-08-17T05:19:21.047190'),
('011bc5ce-23f2-4748-879f-241fee1c5f08', '41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'f2222222-2222-2222-2222-222222222222', 6, 'in_process', '{"mortgage_status": "in_process"}', 15, '2025-08-17T05:19:21.047190'),
('29b8ab70-3f22-42b3-a4f4-3fd5ba256297', '41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'f2222222-2222-2222-2222-222222222222', 7, '$200k_300k', '{"price_range": "$200k_300k"}', 15, '2025-08-17T05:19:21.047190'),
('45f997bb-120c-46a6-b066-b9a9c645d292', '41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'f2222222-2222-2222-2222-222222222222', 8, 'other_metro', '{"areas": "other_metro"}', 10, '2025-08-17T05:19:21.047190'),
('287b7d98-d41e-4196-b910-7433b3a21144', '41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'f2222222-2222-2222-2222-222222222222', 9, 'yes', '{"first_time_buyer": "yes"}', 10, '2025-08-17T05:19:21.047190'),
('32699ea7-53a0-4bed-90dd-2e22770e61e7', '41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'f2222222-2222-2222-2222-222222222222', 10, '2_bedrooms', '{"bedrooms": "2_bedrooms"}', 10, '2025-08-17T05:19:21.047190'),
('152d4a29-6f6d-4504-af46-9d0a5dd6b66a', '41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'f2222222-2222-2222-2222-222222222222', 11, 'yes', '{"worked_with_realtor": "yes"}', 10, '2025-08-17T05:19:21.047190'),
('70f93fe4-a8fd-4e78-ab3a-1940306e4318', '41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'f2222222-2222-2222-2222-222222222222', 12, 'medium', '{"urgency": "medium"}', 10, '2025-08-17T05:19:21.047190');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('db4fb3c2-40c5-4ab4-84e9-4d0bc0fceb96', '41a6ca18-2d5f-4515-bdce-d5be9f7b1301', 'a2222222-2222-2222-2222-222222222222', 'f2222222-2222-2222-2222-222222222222', 'maybe', '{"name": "Lisa_6 Martinez", "email": "lisa.martinez_6@hospital.org", "phone": "(781) 555-7890"}', 65, 0.65, true, false, NULL, NULL, NULL);


SELECT 'Generated 30 realistic lead sessions for metro_realty!' as status;

