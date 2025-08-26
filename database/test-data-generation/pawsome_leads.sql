-- Test Data for Pawsome Dog Walking (Pet Services)
-- Generated 30 realistic lead sessions with complete tracking and outcomes
-- Client: pawsome | Form: f1111111-1111-1111-1111-111111111111 | Generated: 2025-08-26T11:20:42



-- Lead 1: Qualified - Emily Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('1df0fdf1-8fae-4996-af01-ed058d69b1a6', 'f1111111-1111-1111-1111-111111111111', 'pawsome_001_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-17T06:20:42.253063', '2025-08-17T06:46:42.253275', '2025-08-17T06:46:42.253275', 9, true, 95, 95, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.202', '{"device_type": "desktop", "completion_time": 15}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('25977ed3-c887-403e-a794-bd19763136e7', '1df0fdf1-8fae-4996-af01-ed058d69b1a6', 'google', 'cpc', 'premium_dog_walking', 'professional dog walking', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('2685f9cd-b462-4c2d-b050-50980e591280', '1df0fdf1-8fae-4996-af01-ed058d69b1a6', 'f1111111-1111-1111-1111-111111111111', 1, 'Emily Rodriguez', '{"name": "Emily Rodriguez"}', 10, '2025-08-17T06:20:42.253063'),
('2bddfe84-5c42-4337-829a-19ef75a78da7', '1df0fdf1-8fae-4996-af01-ed058d69b1a6', 'f1111111-1111-1111-1111-111111111111', 2, 'emily.rodriguez@mit.edu', '{"email": "emily.rodriguez@mit.edu"}', 10, '2025-08-17T06:20:42.253063'),
('8b2c4d58-9707-4388-be9f-1eaf3faf7212', '1df0fdf1-8fae-4996-af01-ed058d69b1a6', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0192', '{"phone": "(617) 555-0192"}', 15, '2025-08-17T06:20:42.253063'),
('146c1f8d-a996-432d-b31a-512a209cc11f', '1df0fdf1-8fae-4996-af01-ed058d69b1a6', 'f1111111-1111-1111-1111-111111111111', 4, 'German Shepherd', '{"dog_breed": "German Shepherd"}', 20, '2025-08-17T06:20:42.253063'),
('9d26d36d-2724-4a9f-949c-e782868ba7b8', '1df0fdf1-8fae-4996-af01-ed058d69b1a6', 'f1111111-1111-1111-1111-111111111111', 5, '5', '{"dog_age": "5"}', 10, '2025-08-17T06:20:42.253063'),
('1278fccf-97da-4dde-bc40-fad085d47bb9', '1df0fdf1-8fae-4996-af01-ed058d69b1a6', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-17T06:20:42.253063'),
('f918d29c-23d2-432e-8322-a07acc704a61', '1df0fdf1-8fae-4996-af01-ed058d69b1a6', 'f1111111-1111-1111-1111-111111111111', 7, '5_plus', '{"walks_per_week": "5_plus"}', 25, '2025-08-17T06:20:42.253063'),
('9c98db84-7e40-4fb2-b223-b5afed743c3f', '1df0fdf1-8fae-4996-af01-ed058d69b1a6', 'f1111111-1111-1111-1111-111111111111', 8, '1234 Mass Ave, Cambridge', '{"address": "1234 Mass Ave, Cambridge"}', 10, '2025-08-17T06:20:42.253063'),
('21075ba7-d578-4499-812d-0c3473159829', '1df0fdf1-8fae-4996-af01-ed058d69b1a6', 'f1111111-1111-1111-1111-111111111111', 9, '25_35', '{"budget": "25_35"}', 25, '2025-08-17T06:20:42.253063');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('bc46025e-31c7-4096-b4fe-1b067d89f4a9', '1df0fdf1-8fae-4996-af01-ed058d69b1a6', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Emily Rodriguez", "email": "emily.rodriguez@mit.edu", "phone": "(617) 555-0192"}', 95, 0.95, true, false, NULL, NULL, NULL);


-- Lead 2: Maybe - David Park
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('03216c48-17dc-4c43-b6d7-c3f3c2d88a0f', 'f1111111-1111-1111-1111-111111111111', 'pawsome_002_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-19T03:20:42.253383', '2025-08-19T04:00:42.253385', '2025-08-19T04:00:42.253385', 8, true, 65, 65, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.141', '{"device_type": "mobile", "completion_time": 26}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('0556e5fa-b2f7-4136-b82a-033d6261f8d5', '03216c48-17dc-4c43-b6d7-c3f3c2d88a0f', 'facebook', 'social', 'local_dog_services', 'local dog walker', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('6facfa78-193b-4935-a43d-d6e277706bf6', '03216c48-17dc-4c43-b6d7-c3f3c2d88a0f', 'f1111111-1111-1111-1111-111111111111', 1, 'David Park', '{"name": "David Park"}', 10, '2025-08-19T03:20:42.253383'),
('dcdcfff6-edff-442c-a8f5-8529d5ae8ff6', '03216c48-17dc-4c43-b6d7-c3f3c2d88a0f', 'f1111111-1111-1111-1111-111111111111', 2, 'david.park@gmail.com', '{"email": "david.park@gmail.com"}', 10, '2025-08-19T03:20:42.253383'),
('52980ec3-7f6e-478b-94b5-56c9db85da6e', '03216c48-17dc-4c43-b6d7-c3f3c2d88a0f', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0283', '{"phone": "(617) 555-0283"}', 15, '2025-08-19T03:20:42.253383'),
('78839f0e-f1a3-40d6-a5a9-e5b79deeca08', '03216c48-17dc-4c43-b6d7-c3f3c2d88a0f', 'f1111111-1111-1111-1111-111111111111', 4, 'Beagle', '{"dog_breed": "Beagle"}', 15, '2025-08-19T03:20:42.253383'),
('6dc324ea-3f19-41cb-9fc0-e1b4334d24f0', '03216c48-17dc-4c43-b6d7-c3f3c2d88a0f', 'f1111111-1111-1111-1111-111111111111', 5, '8', '{"dog_age": "8"}', 10, '2025-08-19T03:20:42.253383'),
('89272dc3-ae1f-4ff5-bb2b-f7762b2de775', '03216c48-17dc-4c43-b6d7-c3f3c2d88a0f', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-19T03:20:42.253383'),
('cf325db3-72f3-4a34-a722-16d2c532cddb', '03216c48-17dc-4c43-b6d7-c3f3c2d88a0f', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-19T03:20:42.253383'),
('aeb202e1-9292-49bb-9abf-61b53fbf8e4e', '03216c48-17dc-4c43-b6d7-c3f3c2d88a0f', 'f1111111-1111-1111-1111-111111111111', 8, 'Somerville near Davis Square', '{"address": "Somerville near Davis Square"}', 10, '2025-08-19T03:20:42.253383');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('80f7c37b-cc90-4821-95cc-0f30bc99c552', '03216c48-17dc-4c43-b6d7-c3f3c2d88a0f', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "David Park", "email": "david.park@gmail.com", "phone": "(617) 555-0283"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 3: Qualified - Sarah Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('9c900d38-0a42-423b-9f6a-5a946b619189', 'f1111111-1111-1111-1111-111111111111', 'pawsome_003_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-18T22:20:42.253446', '2025-08-18T22:59:42.253447', '2025-08-18T22:59:42.253447', 6, true, 88, 88, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.96', '{"device_type": "mobile", "completion_time": 20}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('fd5cb6c9-1e6b-4386-a672-8adeb70dc4ca', '9c900d38-0a42-423b-9f6a-5a946b619189', 'google', 'cpc', 'harvard_students', 'dog walker near me', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('843053d1-5db3-450e-b93b-8693e30006f4', '9c900d38-0a42-423b-9f6a-5a946b619189', 'f1111111-1111-1111-1111-111111111111', 1, 'Sarah Kim', '{"name": "Sarah Kim"}', 10, '2025-08-18T22:20:42.253446'),
('aed8351d-8409-4ae0-96a5-10fc344e47bc', '9c900d38-0a42-423b-9f6a-5a946b619189', 'f1111111-1111-1111-1111-111111111111', 2, 'sarah.kim@harvard.edu', '{"email": "sarah.kim@harvard.edu"}', 10, '2025-08-18T22:20:42.253446'),
('cdb4c505-cf36-44b6-b016-7c0ebf63dce1', '9c900d38-0a42-423b-9f6a-5a946b619189', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0374', '{"phone": "(617) 555-0374"}', 15, '2025-08-18T22:20:42.253446'),
('67dda748-3961-4439-9e73-77d8cfaacd8c', '9c900d38-0a42-423b-9f6a-5a946b619189', 'f1111111-1111-1111-1111-111111111111', 4, 'Golden Retriever', '{"dog_breed": "Golden Retriever"}', 20, '2025-08-18T22:20:42.253446'),
('0879d58c-680f-4b51-900d-7ca732edd48e', '9c900d38-0a42-423b-9f6a-5a946b619189', 'f1111111-1111-1111-1111-111111111111', 5, '3', '{"dog_age": "3"}', 10, '2025-08-18T22:20:42.253446'),
('2915f81e-fce8-4049-b6fb-3fb55ddcf89d', '9c900d38-0a42-423b-9f6a-5a946b619189', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-18T22:20:42.253446'),
('a4323d6a-7cf4-4938-ad35-c379583bdabf', '9c900d38-0a42-423b-9f6a-5a946b619189', 'f1111111-1111-1111-1111-111111111111', 7, '3_4', '{"walks_per_week": "3_4"}', 20, '2025-08-18T22:20:42.253446'),
('9284ba26-944c-49d7-996c-256b2dc32e30', '9c900d38-0a42-423b-9f6a-5a946b619189', 'f1111111-1111-1111-1111-111111111111', 8, 'Harvard Square area', '{"address": "Harvard Square area"}', 10, '2025-08-18T22:20:42.253446'),
('5e612b74-8e4f-4a78-b992-9832914b96b1', '9c900d38-0a42-423b-9f6a-5a946b619189', 'f1111111-1111-1111-1111-111111111111', 9, '20_30', '{"budget": "20_30"}', 20, '2025-08-18T22:20:42.253446');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('d0722d31-690b-4e90-b440-4282f4ab15e3', '9c900d38-0a42-423b-9f6a-5a946b619189', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Sarah Kim", "email": "sarah.kim@harvard.edu", "phone": "(617) 555-0374"}', 88, 0.88, true, false, NULL, NULL, NULL);


-- Lead 4: Unqualified - Mike Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('c31d7874-c13c-4e78-9cf4-3f111556cbbd', 'f1111111-1111-1111-1111-111111111111', 'pawsome_004_unqualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-12T08:20:42.253508', '2025-08-12T08:52:42.253509', '2025-08-12T08:52:42.253509', 9, true, 25, 25, 'no', 'qualified', 'Thank you for your interest. We may not be the best fit, but please reach out if your needs change.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.41', '{"device_type": "desktop", "completion_time": 34}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('7250c41a-3c31-4e33-9159-17802b01063a', 'c31d7874-c13c-4e78-9cf4-3f111556cbbd', 'organic', 'search', 'pawsome_general', 'dog walker near me', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('66534eee-68fa-431a-ad98-5e3d4fd5edd6', 'c31d7874-c13c-4e78-9cf4-3f111556cbbd', 'f1111111-1111-1111-1111-111111111111', 1, 'Mike Johnson', '{"name": "Mike Johnson"}', 10, '2025-08-12T08:20:42.253508'),
('0808c860-e711-492b-96bc-27bd2103e609', 'c31d7874-c13c-4e78-9cf4-3f111556cbbd', 'f1111111-1111-1111-1111-111111111111', 2, 'mjohnson.work@outlook.com', '{"email": "mjohnson.work@outlook.com"}', 10, '2025-08-12T08:20:42.253508'),
('b5508029-c371-4e2e-96b2-b488f8b4c47d', 'c31d7874-c13c-4e78-9cf4-3f111556cbbd', 'f1111111-1111-1111-1111-111111111111', 4, 'Pit Bull Mix', '{"dog_breed": "Pit Bull Mix"}', 5, '2025-08-12T08:20:42.253508'),
('eba644dc-c58f-4be6-85b9-98c5890a197a', 'c31d7874-c13c-4e78-9cf4-3f111556cbbd', 'f1111111-1111-1111-1111-111111111111', 5, '2', '{"dog_age": "2"}', 10, '2025-08-12T08:20:42.253508'),
('0a780348-2888-4fbe-9ba3-f49f5b086887', 'c31d7874-c13c-4e78-9cf4-3f111556cbbd', 'f1111111-1111-1111-1111-111111111111', 6, 'rarely', '{"behavior": "rarely"}', -10, '2025-08-12T08:20:42.253508'),
('20479929-988b-4502-be9d-2739b1fe0e7e', 'c31d7874-c13c-4e78-9cf4-3f111556cbbd', 'f1111111-1111-1111-1111-111111111111', 7, '1', '{"walks_per_week": "1"}', 5, '2025-08-12T08:20:42.253508'),
('b8c0e397-0d09-456d-b432-b6408c87852f', 'c31d7874-c13c-4e78-9cf4-3f111556cbbd', 'f1111111-1111-1111-1111-111111111111', 8, 'Dorchester', '{"address": "Dorchester"}', 10, '2025-08-12T08:20:42.253508'),
('5ad3d678-66e4-4a20-81a7-2a7d06fc92e2', 'c31d7874-c13c-4e78-9cf4-3f111556cbbd', 'f1111111-1111-1111-1111-111111111111', 9, 'under_15', '{"budget": "under_15"}', 0, '2025-08-12T08:20:42.253508');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('0a0d6615-2dc2-420a-91da-375949d1a338', 'c31d7874-c13c-4e78-9cf4-3f111556cbbd', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'unqualified', '{"name": "Mike Johnson", "email": "mjohnson.work@outlook.com"}', 25, 0.25, false, false, NULL, NULL, NULL);


-- Lead 5: Maybe - Jennifer Walsh
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('2739a112-1f77-48b0-a667-453b1ab2696c', 'f1111111-1111-1111-1111-111111111111', 'pawsome_005_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-14T15:20:42.253564', '2025-08-14T16:00:42.253565', '2025-08-14T16:00:42.253565', 8, true, 60, 60, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.14', '{"device_type": "mobile", "completion_time": 23}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('ac668405-3310-4cef-8267-8c073d3c31e5', '2739a112-1f77-48b0-a667-453b1ab2696c', 'facebook', 'social', 'medford_pet_owners', 'dog walking cambridge', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('46814ec9-ab37-4906-a44b-721450ad0c20', '2739a112-1f77-48b0-a667-453b1ab2696c', 'f1111111-1111-1111-1111-111111111111', 1, 'Jennifer Walsh', '{"name": "Jennifer Walsh"}', 10, '2025-08-14T15:20:42.253564'),
('99df74e5-fd4c-4b3f-a404-99b28d8927f8', '2739a112-1f77-48b0-a667-453b1ab2696c', 'f1111111-1111-1111-1111-111111111111', 2, 'jwalsh.home@gmail.com', '{"email": "jwalsh.home@gmail.com"}', 10, '2025-08-14T15:20:42.253564'),
('f6f522e8-6506-40a7-9776-4eb9ec88e629', '2739a112-1f77-48b0-a667-453b1ab2696c', 'f1111111-1111-1111-1111-111111111111', 4, 'Lab Mix', '{"dog_breed": "Lab Mix"}', 10, '2025-08-14T15:20:42.253564'),
('8ed4af18-88d5-46df-b1d2-bf42ee9aba9d', '2739a112-1f77-48b0-a667-453b1ab2696c', 'f1111111-1111-1111-1111-111111111111', 5, '6', '{"dog_age": "6"}', 10, '2025-08-14T15:20:42.253564'),
('9e35119e-a300-4b4c-9e8a-bb9a886efc67', '2739a112-1f77-48b0-a667-453b1ab2696c', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-14T15:20:42.253564'),
('1305bba3-a937-45c9-a771-55dbf267d7e1', '2739a112-1f77-48b0-a667-453b1ab2696c', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-14T15:20:42.253564'),
('4bd12615-29ed-4923-8c6d-5a527ce27ced', '2739a112-1f77-48b0-a667-453b1ab2696c', 'f1111111-1111-1111-1111-111111111111', 8, 'Medford Square area', '{"address": "Medford Square area"}', 10, '2025-08-14T15:20:42.253564');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('18c5e59d-15fe-49b2-91b7-be9157971b9e', '2739a112-1f77-48b0-a667-453b1ab2696c', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "Jennifer Walsh", "email": "jwalsh.home@gmail.com"}', 60, 0.60, true, false, NULL, NULL, NULL);


-- Lead 6: Qualified - Emily_2 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('b7dd8168-b5c2-4bb2-bf8e-77b6d75ba943', 'f1111111-1111-1111-1111-111111111111', 'pawsome_006_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-13T13:20:42.253614', '2025-08-13T13:36:42.253615', '2025-08-13T13:36:42.253615', 8, true, 95, 95, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.106', '{"device_type": "desktop", "completion_time": 18}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('2c2e8be5-11c7-4ee3-b8bf-b08096b65680', 'b7dd8168-b5c2-4bb2-bf8e-77b6d75ba943', 'google', 'cpc', 'premium_dog_walking', 'dog walking cambridge', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('f2683019-67f3-4d9f-b892-f064c5098451', 'b7dd8168-b5c2-4bb2-bf8e-77b6d75ba943', 'f1111111-1111-1111-1111-111111111111', 1, 'Emily_2 Rodriguez', '{"name": "Emily_2 Rodriguez"}', 10, '2025-08-13T13:20:42.253614'),
('2eb7d218-73b1-4681-a594-1bdb561ab620', 'b7dd8168-b5c2-4bb2-bf8e-77b6d75ba943', 'f1111111-1111-1111-1111-111111111111', 2, 'emily.rodriguez_2@mit.edu', '{"email": "emily.rodriguez_2@mit.edu"}', 10, '2025-08-13T13:20:42.253614'),
('0f178845-f4fe-4eb3-a58f-e4e1cafe0d71', 'b7dd8168-b5c2-4bb2-bf8e-77b6d75ba943', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0192', '{"phone": "(617) 555-0192"}', 15, '2025-08-13T13:20:42.253614'),
('10f7bbc4-b5ef-4514-81b6-c5de0f7a1a9b', 'b7dd8168-b5c2-4bb2-bf8e-77b6d75ba943', 'f1111111-1111-1111-1111-111111111111', 4, 'German Shepherd', '{"dog_breed": "German Shepherd"}', 20, '2025-08-13T13:20:42.253614'),
('26884bb5-0709-4ef8-bcb8-24599dd27828', 'b7dd8168-b5c2-4bb2-bf8e-77b6d75ba943', 'f1111111-1111-1111-1111-111111111111', 5, '5', '{"dog_age": "5"}', 10, '2025-08-13T13:20:42.253614'),
('c5f4e883-d32b-4c02-8f17-49cf73ebaf9e', 'b7dd8168-b5c2-4bb2-bf8e-77b6d75ba943', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-13T13:20:42.253614'),
('6c2f4c51-3d9a-4c2f-b904-b3ad6490274d', 'b7dd8168-b5c2-4bb2-bf8e-77b6d75ba943', 'f1111111-1111-1111-1111-111111111111', 7, '5_plus', '{"walks_per_week": "5_plus"}', 25, '2025-08-13T13:20:42.253614'),
('8aeec71f-caca-42f0-9eb6-88ea2757d540', 'b7dd8168-b5c2-4bb2-bf8e-77b6d75ba943', 'f1111111-1111-1111-1111-111111111111', 8, '1234 Mass Ave, Cambridge', '{"address": "1234 Mass Ave, Cambridge"}', 10, '2025-08-13T13:20:42.253614'),
('b63e0eaa-eb6b-4749-9453-a00027b6bb50', 'b7dd8168-b5c2-4bb2-bf8e-77b6d75ba943', 'f1111111-1111-1111-1111-111111111111', 9, '25_35', '{"budget": "25_35"}', 25, '2025-08-13T13:20:42.253614');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('8e961f3d-be28-484b-84c8-08458486b3fe', 'b7dd8168-b5c2-4bb2-bf8e-77b6d75ba943', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Emily_2 Rodriguez", "email": "emily.rodriguez_2@mit.edu", "phone": "(617) 555-0192"}', 95, 0.95, true, false, NULL, NULL, NULL);


-- Lead 7: Maybe - David_2 Park
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('0869f627-4e9a-456f-871f-f75f23b11aaa', 'f1111111-1111-1111-1111-111111111111', 'pawsome_007_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-18T09:20:42.253677', '2025-08-18T09:55:42.253678', '2025-08-18T09:55:42.253678', 8, true, 65, 65, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.68', '{"device_type": "mobile", "completion_time": 45}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('b0baa2eb-9574-4aad-9e8f-4bdf17b709ed', '0869f627-4e9a-456f-871f-f75f23b11aaa', 'facebook', 'social', 'local_dog_services', 'local dog walker', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('4f970140-dff6-44b5-96e4-d5ed79e920ba', '0869f627-4e9a-456f-871f-f75f23b11aaa', 'f1111111-1111-1111-1111-111111111111', 1, 'David_2 Park', '{"name": "David_2 Park"}', 10, '2025-08-18T09:20:42.253677'),
('aac593d7-4c60-48cb-846d-e9c76388d108', '0869f627-4e9a-456f-871f-f75f23b11aaa', 'f1111111-1111-1111-1111-111111111111', 2, 'david.park_2@gmail.com', '{"email": "david.park_2@gmail.com"}', 10, '2025-08-18T09:20:42.253677'),
('f5f3d687-4599-4e43-9191-c02ac9e78744', '0869f627-4e9a-456f-871f-f75f23b11aaa', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0283', '{"phone": "(617) 555-0283"}', 15, '2025-08-18T09:20:42.253677'),
('f05392b4-43a1-42bb-a129-53953c79a465', '0869f627-4e9a-456f-871f-f75f23b11aaa', 'f1111111-1111-1111-1111-111111111111', 4, 'Beagle', '{"dog_breed": "Beagle"}', 15, '2025-08-18T09:20:42.253677'),
('861ff6ca-9e18-4a1d-940a-9a7fa5a884a7', '0869f627-4e9a-456f-871f-f75f23b11aaa', 'f1111111-1111-1111-1111-111111111111', 5, '8', '{"dog_age": "8"}', 10, '2025-08-18T09:20:42.253677'),
('9f562cda-cc06-4b79-8d5c-239c21682bb7', '0869f627-4e9a-456f-871f-f75f23b11aaa', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-18T09:20:42.253677'),
('419036ce-cd65-4205-acd5-6c2ff21542a3', '0869f627-4e9a-456f-871f-f75f23b11aaa', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-18T09:20:42.253677'),
('2ba81f0a-d789-44f3-8157-a2eaf9299a77', '0869f627-4e9a-456f-871f-f75f23b11aaa', 'f1111111-1111-1111-1111-111111111111', 8, 'Somerville near Davis Square', '{"address": "Somerville near Davis Square"}', 10, '2025-08-18T09:20:42.253677');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('12af2178-3d17-4434-ad65-8f1ad274a603', '0869f627-4e9a-456f-871f-f75f23b11aaa', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "David_2 Park", "email": "david.park_2@gmail.com", "phone": "(617) 555-0283"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 8: Qualified - Sarah_2 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('74536b68-cf5e-48bf-9c97-9d1487d6d7f6', 'f1111111-1111-1111-1111-111111111111', 'pawsome_008_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-18T00:20:42.253729', '2025-08-18T00:46:42.253729', '2025-08-18T00:46:42.253729', 8, true, 88, 88, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.162', '{"device_type": "mobile", "completion_time": 30}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('9f53d90c-8329-48c3-8453-46b85010ec4a', '74536b68-cf5e-48bf-9c97-9d1487d6d7f6', 'google', 'cpc', 'harvard_students', 'dog walking cambridge', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('32c06344-fabf-4f66-87f8-c18d0a04e226', '74536b68-cf5e-48bf-9c97-9d1487d6d7f6', 'f1111111-1111-1111-1111-111111111111', 1, 'Sarah_2 Kim', '{"name": "Sarah_2 Kim"}', 10, '2025-08-18T00:20:42.253729'),
('ebf79ef1-1094-447d-a7bd-9f0657efac2d', '74536b68-cf5e-48bf-9c97-9d1487d6d7f6', 'f1111111-1111-1111-1111-111111111111', 2, 'sarah.kim_2@harvard.edu', '{"email": "sarah.kim_2@harvard.edu"}', 10, '2025-08-18T00:20:42.253729'),
('8dc800f0-5798-4d26-8de5-99729f2be8c1', '74536b68-cf5e-48bf-9c97-9d1487d6d7f6', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0374', '{"phone": "(617) 555-0374"}', 15, '2025-08-18T00:20:42.253729'),
('f52aeb13-2283-46c5-9428-18176f6212e3', '74536b68-cf5e-48bf-9c97-9d1487d6d7f6', 'f1111111-1111-1111-1111-111111111111', 4, 'Golden Retriever', '{"dog_breed": "Golden Retriever"}', 20, '2025-08-18T00:20:42.253729'),
('7f08523a-832a-4291-837f-51ea20297a70', '74536b68-cf5e-48bf-9c97-9d1487d6d7f6', 'f1111111-1111-1111-1111-111111111111', 5, '3', '{"dog_age": "3"}', 10, '2025-08-18T00:20:42.253729'),
('45cd2e2b-8d22-4665-b9bb-7d822a3ef2d7', '74536b68-cf5e-48bf-9c97-9d1487d6d7f6', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-18T00:20:42.253729'),
('d64ab5ad-dd07-4f23-9dd5-7c6c44be9f68', '74536b68-cf5e-48bf-9c97-9d1487d6d7f6', 'f1111111-1111-1111-1111-111111111111', 7, '3_4', '{"walks_per_week": "3_4"}', 20, '2025-08-18T00:20:42.253729'),
('0efccb7e-6b2d-4e0c-adb1-231e9e4b75d6', '74536b68-cf5e-48bf-9c97-9d1487d6d7f6', 'f1111111-1111-1111-1111-111111111111', 8, 'Harvard Square area', '{"address": "Harvard Square area"}', 10, '2025-08-18T00:20:42.253729'),
('f2553b56-5216-4804-a7d9-d5e08925acaa', '74536b68-cf5e-48bf-9c97-9d1487d6d7f6', 'f1111111-1111-1111-1111-111111111111', 9, '20_30', '{"budget": "20_30"}', 20, '2025-08-18T00:20:42.253729');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('86441b34-8dd3-4237-8cb4-4095556f1a23', '74536b68-cf5e-48bf-9c97-9d1487d6d7f6', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Sarah_2 Kim", "email": "sarah.kim_2@harvard.edu", "phone": "(617) 555-0374"}', 88, 0.88, true, false, NULL, NULL, NULL);


-- Lead 9: Unqualified - Mike_2 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('bfc57f11-86dc-4677-9950-ae88c02a252f', 'f1111111-1111-1111-1111-111111111111', 'pawsome_009_unqualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-18T06:20:42.253779', '2025-08-18T06:35:42.253780', '2025-08-18T06:35:42.253780', 7, true, 25, 25, 'no', 'qualified', 'Thank you for your interest. We may not be the best fit, but please reach out if your needs change.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.100', '{"device_type": "desktop", "completion_time": 17}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('f5319c2e-5465-4e8f-95aa-78d9916d608b', 'bfc57f11-86dc-4677-9950-ae88c02a252f', 'organic', 'search', 'pawsome_general', 'professional dog walking', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('c172c370-4706-46fe-ba4c-65da260387e2', 'bfc57f11-86dc-4677-9950-ae88c02a252f', 'f1111111-1111-1111-1111-111111111111', 1, 'Mike_2 Johnson', '{"name": "Mike_2 Johnson"}', 10, '2025-08-18T06:20:42.253779'),
('c43f7df5-a452-4163-92b3-a5521b466a97', 'bfc57f11-86dc-4677-9950-ae88c02a252f', 'f1111111-1111-1111-1111-111111111111', 2, 'mjohnson.work_2@outlook.com', '{"email": "mjohnson.work_2@outlook.com"}', 10, '2025-08-18T06:20:42.253779'),
('e358114a-1666-44cf-867f-8b46d3b5631a', 'bfc57f11-86dc-4677-9950-ae88c02a252f', 'f1111111-1111-1111-1111-111111111111', 4, 'Pit Bull Mix', '{"dog_breed": "Pit Bull Mix"}', 5, '2025-08-18T06:20:42.253779'),
('a1c6f7e5-77ae-40b1-b384-c7b5f063bb27', 'bfc57f11-86dc-4677-9950-ae88c02a252f', 'f1111111-1111-1111-1111-111111111111', 5, '2', '{"dog_age": "2"}', 10, '2025-08-18T06:20:42.253779'),
('2eeb38b8-efa3-4384-a00b-b247085fcef7', 'bfc57f11-86dc-4677-9950-ae88c02a252f', 'f1111111-1111-1111-1111-111111111111', 6, 'rarely', '{"behavior": "rarely"}', -10, '2025-08-18T06:20:42.253779'),
('b4ab596b-9856-4ad8-9548-41102a71c47d', 'bfc57f11-86dc-4677-9950-ae88c02a252f', 'f1111111-1111-1111-1111-111111111111', 7, '1', '{"walks_per_week": "1"}', 5, '2025-08-18T06:20:42.253779'),
('84a4977c-8c5e-45e4-87ad-3d82c5efcfbc', 'bfc57f11-86dc-4677-9950-ae88c02a252f', 'f1111111-1111-1111-1111-111111111111', 8, 'Dorchester', '{"address": "Dorchester"}', 10, '2025-08-18T06:20:42.253779'),
('e174b712-58de-4286-8873-8208746b50d4', 'bfc57f11-86dc-4677-9950-ae88c02a252f', 'f1111111-1111-1111-1111-111111111111', 9, 'under_15', '{"budget": "under_15"}', 0, '2025-08-18T06:20:42.253779');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('23b80445-20a9-4c40-8e1f-3f035ba266ad', 'bfc57f11-86dc-4677-9950-ae88c02a252f', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'unqualified', '{"name": "Mike_2 Johnson", "email": "mjohnson.work_2@outlook.com"}', 25, 0.25, false, false, NULL, NULL, NULL);


-- Lead 10: Maybe - Jennifer_2 Walsh
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('6bbfb61d-459a-4a83-bdf5-3e106442ea11', 'f1111111-1111-1111-1111-111111111111', 'pawsome_010_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-15T23:20:42.253827', '2025-08-15T23:46:42.253828', '2025-08-15T23:46:42.253828', 8, true, 60, 60, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.247', '{"device_type": "mobile", "completion_time": 34}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('a04e0ef0-9a0f-4a30-9828-d23d0ebfeb2a', '6bbfb61d-459a-4a83-bdf5-3e106442ea11', 'facebook', 'social', 'medford_pet_owners', 'dog walking cambridge', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('553486b5-0c5e-405b-9a4f-3efaab90a5ee', '6bbfb61d-459a-4a83-bdf5-3e106442ea11', 'f1111111-1111-1111-1111-111111111111', 1, 'Jennifer_2 Walsh', '{"name": "Jennifer_2 Walsh"}', 10, '2025-08-15T23:20:42.253827'),
('116917df-d909-424d-9405-982d6c4a88a7', '6bbfb61d-459a-4a83-bdf5-3e106442ea11', 'f1111111-1111-1111-1111-111111111111', 2, 'jwalsh.home_2@gmail.com', '{"email": "jwalsh.home_2@gmail.com"}', 10, '2025-08-15T23:20:42.253827'),
('f533ccbe-e66c-405d-bf53-201cc68ac70a', '6bbfb61d-459a-4a83-bdf5-3e106442ea11', 'f1111111-1111-1111-1111-111111111111', 4, 'Lab Mix', '{"dog_breed": "Lab Mix"}', 10, '2025-08-15T23:20:42.253827'),
('d6e65eda-e26a-4862-99f0-00a4e91553cc', '6bbfb61d-459a-4a83-bdf5-3e106442ea11', 'f1111111-1111-1111-1111-111111111111', 5, '6', '{"dog_age": "6"}', 10, '2025-08-15T23:20:42.253827'),
('3bfed878-da6a-4dcf-b709-ba0f6d789fce', '6bbfb61d-459a-4a83-bdf5-3e106442ea11', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-15T23:20:42.253827'),
('8f7275df-216f-40e9-afec-4bbf1cb39c19', '6bbfb61d-459a-4a83-bdf5-3e106442ea11', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-15T23:20:42.253827'),
('ba639526-d56c-4318-a5be-5257554f916d', '6bbfb61d-459a-4a83-bdf5-3e106442ea11', 'f1111111-1111-1111-1111-111111111111', 8, 'Medford Square area', '{"address": "Medford Square area"}', 10, '2025-08-15T23:20:42.253827');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('4575bf81-d57d-4fc0-b197-dc8b11bae59e', '6bbfb61d-459a-4a83-bdf5-3e106442ea11', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "Jennifer_2 Walsh", "email": "jwalsh.home_2@gmail.com"}', 60, 0.60, true, false, NULL, NULL, NULL);


-- Lead 11: Qualified - Emily_3 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('aed1a945-e2f1-4eeb-994a-52c1bd92bfe2', 'f1111111-1111-1111-1111-111111111111', 'pawsome_011_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-13T21:20:42.253876', '2025-08-13T21:44:42.253877', '2025-08-13T21:44:42.253877', 8, true, 95, 95, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.180', '{"device_type": "desktop", "completion_time": 30}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('42dfee6f-b7bb-4142-8ad3-ef889dcb9410', 'aed1a945-e2f1-4eeb-994a-52c1bd92bfe2', 'google', 'cpc', 'premium_dog_walking', 'dog walking cambridge', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('6dfdfa1b-ff1a-4555-a6a4-a90aec55178b', 'aed1a945-e2f1-4eeb-994a-52c1bd92bfe2', 'f1111111-1111-1111-1111-111111111111', 1, 'Emily_3 Rodriguez', '{"name": "Emily_3 Rodriguez"}', 10, '2025-08-13T21:20:42.253876'),
('cc817d39-10ab-49d0-94e2-3e78f6e1686b', 'aed1a945-e2f1-4eeb-994a-52c1bd92bfe2', 'f1111111-1111-1111-1111-111111111111', 2, 'emily.rodriguez_3@mit.edu', '{"email": "emily.rodriguez_3@mit.edu"}', 10, '2025-08-13T21:20:42.253876'),
('308e67c7-65c7-41ac-af9c-badf5118cf2f', 'aed1a945-e2f1-4eeb-994a-52c1bd92bfe2', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0192', '{"phone": "(617) 555-0192"}', 15, '2025-08-13T21:20:42.253876'),
('7a0949a5-a8b6-429e-a028-b8945ee38ce3', 'aed1a945-e2f1-4eeb-994a-52c1bd92bfe2', 'f1111111-1111-1111-1111-111111111111', 4, 'German Shepherd', '{"dog_breed": "German Shepherd"}', 20, '2025-08-13T21:20:42.253876'),
('ccc4afc5-a4f6-41a5-84d1-e391ee9bfc1b', 'aed1a945-e2f1-4eeb-994a-52c1bd92bfe2', 'f1111111-1111-1111-1111-111111111111', 5, '5', '{"dog_age": "5"}', 10, '2025-08-13T21:20:42.253876'),
('a1cecf66-2d51-4fb4-8b55-d676bf42e2e8', 'aed1a945-e2f1-4eeb-994a-52c1bd92bfe2', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-13T21:20:42.253876'),
('82a9bc64-37dd-4b1e-b718-8418d25f0cb9', 'aed1a945-e2f1-4eeb-994a-52c1bd92bfe2', 'f1111111-1111-1111-1111-111111111111', 7, '5_plus', '{"walks_per_week": "5_plus"}', 25, '2025-08-13T21:20:42.253876'),
('77827964-7a9e-4386-8339-65298e2f5c4d', 'aed1a945-e2f1-4eeb-994a-52c1bd92bfe2', 'f1111111-1111-1111-1111-111111111111', 8, '1234 Mass Ave, Cambridge', '{"address": "1234 Mass Ave, Cambridge"}', 10, '2025-08-13T21:20:42.253876'),
('2f86a74d-889e-45d2-b312-d099f8d5786d', 'aed1a945-e2f1-4eeb-994a-52c1bd92bfe2', 'f1111111-1111-1111-1111-111111111111', 9, '25_35', '{"budget": "25_35"}', 25, '2025-08-13T21:20:42.253876');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('f8d19b00-5b01-4a71-a6df-93a1a472fddf', 'aed1a945-e2f1-4eeb-994a-52c1bd92bfe2', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Emily_3 Rodriguez", "email": "emily.rodriguez_3@mit.edu", "phone": "(617) 555-0192"}', 95, 0.95, true, false, NULL, NULL, NULL);


-- Lead 12: Maybe - David_3 Park
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('89f49259-01e2-4d51-8d82-7f96cdb592c0', 'f1111111-1111-1111-1111-111111111111', 'pawsome_012_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-12T08:20:42.253930', '2025-08-12T08:45:42.253931', '2025-08-12T08:45:42.253931', 8, true, 65, 65, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.87', '{"device_type": "mobile", "completion_time": 12}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('8da9ad8c-4c72-485d-8035-8fc8d59ffc6f', '89f49259-01e2-4d51-8d82-7f96cdb592c0', 'facebook', 'social', 'local_dog_services', 'dog walker near me', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('6c395f03-7d78-49c0-b758-4254e12f3220', '89f49259-01e2-4d51-8d82-7f96cdb592c0', 'f1111111-1111-1111-1111-111111111111', 1, 'David_3 Park', '{"name": "David_3 Park"}', 10, '2025-08-12T08:20:42.253930'),
('7fcbf043-2c9f-4e45-a8b1-77a94a09c2d1', '89f49259-01e2-4d51-8d82-7f96cdb592c0', 'f1111111-1111-1111-1111-111111111111', 2, 'david.park_3@gmail.com', '{"email": "david.park_3@gmail.com"}', 10, '2025-08-12T08:20:42.253930'),
('31f91d94-7a06-474c-bb84-2a93a62e75c4', '89f49259-01e2-4d51-8d82-7f96cdb592c0', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0283', '{"phone": "(617) 555-0283"}', 15, '2025-08-12T08:20:42.253930'),
('d86ff4f7-7a68-4759-9c38-2c584da1dc28', '89f49259-01e2-4d51-8d82-7f96cdb592c0', 'f1111111-1111-1111-1111-111111111111', 4, 'Beagle', '{"dog_breed": "Beagle"}', 15, '2025-08-12T08:20:42.253930'),
('c7b6d326-b47d-4761-8b6b-e305dcbb3144', '89f49259-01e2-4d51-8d82-7f96cdb592c0', 'f1111111-1111-1111-1111-111111111111', 5, '8', '{"dog_age": "8"}', 10, '2025-08-12T08:20:42.253930'),
('0d7fe127-87db-40eb-bbcd-67a080dcea6b', '89f49259-01e2-4d51-8d82-7f96cdb592c0', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-12T08:20:42.253930'),
('afd9b278-d3cb-4652-ab13-514509aa00c1', '89f49259-01e2-4d51-8d82-7f96cdb592c0', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-12T08:20:42.253930'),
('dfbe886d-6ec8-426d-b7ba-eeae4ac17ca2', '89f49259-01e2-4d51-8d82-7f96cdb592c0', 'f1111111-1111-1111-1111-111111111111', 8, 'Somerville near Davis Square', '{"address": "Somerville near Davis Square"}', 10, '2025-08-12T08:20:42.253930');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('471974d9-a816-499c-9523-d51ce1fb38fb', '89f49259-01e2-4d51-8d82-7f96cdb592c0', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "David_3 Park", "email": "david.park_3@gmail.com", "phone": "(617) 555-0283"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 13: Qualified - Sarah_3 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('0d843ab3-2221-4fd0-8674-b16b9b141338', 'f1111111-1111-1111-1111-111111111111', 'pawsome_013_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-12T00:20:42.253979', '2025-08-12T01:04:42.253980', '2025-08-12T01:04:42.253980', 9, true, 88, 88, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.12', '{"device_type": "mobile", "completion_time": 30}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('f2580f32-77c5-45e9-9c88-65c781385adb', '0d843ab3-2221-4fd0-8674-b16b9b141338', 'google', 'cpc', 'harvard_students', 'pet walking services', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('28da3a35-1316-4c1c-90d5-1956122f3f34', '0d843ab3-2221-4fd0-8674-b16b9b141338', 'f1111111-1111-1111-1111-111111111111', 1, 'Sarah_3 Kim', '{"name": "Sarah_3 Kim"}', 10, '2025-08-12T00:20:42.253979'),
('3a6dd830-c6e9-4b75-8e46-205fcc67716d', '0d843ab3-2221-4fd0-8674-b16b9b141338', 'f1111111-1111-1111-1111-111111111111', 2, 'sarah.kim_3@harvard.edu', '{"email": "sarah.kim_3@harvard.edu"}', 10, '2025-08-12T00:20:42.253979'),
('503d93bc-83e4-4027-8a91-d9c865df4bb6', '0d843ab3-2221-4fd0-8674-b16b9b141338', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0374', '{"phone": "(617) 555-0374"}', 15, '2025-08-12T00:20:42.253979'),
('cf443487-80c5-4a0e-81e4-d37218197e6a', '0d843ab3-2221-4fd0-8674-b16b9b141338', 'f1111111-1111-1111-1111-111111111111', 4, 'Golden Retriever', '{"dog_breed": "Golden Retriever"}', 20, '2025-08-12T00:20:42.253979'),
('833beed9-2f7a-4be5-a6a1-3c2fb36d67a2', '0d843ab3-2221-4fd0-8674-b16b9b141338', 'f1111111-1111-1111-1111-111111111111', 5, '3', '{"dog_age": "3"}', 10, '2025-08-12T00:20:42.253979'),
('0ab65c65-cb05-44e4-9c15-7b97c57f06e0', '0d843ab3-2221-4fd0-8674-b16b9b141338', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-12T00:20:42.253979'),
('a46ac9c1-92dd-40f6-acdf-1897bbae408e', '0d843ab3-2221-4fd0-8674-b16b9b141338', 'f1111111-1111-1111-1111-111111111111', 7, '3_4', '{"walks_per_week": "3_4"}', 20, '2025-08-12T00:20:42.253979'),
('caa6c6ab-7804-4c1e-8f88-8c648dddb8e0', '0d843ab3-2221-4fd0-8674-b16b9b141338', 'f1111111-1111-1111-1111-111111111111', 8, 'Harvard Square area', '{"address": "Harvard Square area"}', 10, '2025-08-12T00:20:42.253979'),
('d9db8d78-e294-4fca-beb7-54f974d4a17f', '0d843ab3-2221-4fd0-8674-b16b9b141338', 'f1111111-1111-1111-1111-111111111111', 9, '20_30', '{"budget": "20_30"}', 20, '2025-08-12T00:20:42.253979');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('62e6dabc-6a16-4c7d-b60d-f4522da2d685', '0d843ab3-2221-4fd0-8674-b16b9b141338', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Sarah_3 Kim", "email": "sarah.kim_3@harvard.edu", "phone": "(617) 555-0374"}', 88, 0.88, true, false, NULL, NULL, NULL);


-- Lead 14: Unqualified - Mike_3 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('08638a27-d640-4e63-bf0d-c396e65cb235', 'f1111111-1111-1111-1111-111111111111', 'pawsome_014_unqualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-24T13:20:42.254033', '2025-08-24T14:05:42.254034', '2025-08-24T14:05:42.254034', 8, true, 25, 25, 'no', 'qualified', 'Thank you for your interest. We may not be the best fit, but please reach out if your needs change.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.44', '{"device_type": "desktop", "completion_time": 26}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('9f2cf69b-e8eb-4941-b21d-2cf94e49f350', '08638a27-d640-4e63-bf0d-c396e65cb235', 'organic', 'search', 'pawsome_general', 'professional dog walking', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('9a9af97d-f84e-465a-98a5-a65ff2331986', '08638a27-d640-4e63-bf0d-c396e65cb235', 'f1111111-1111-1111-1111-111111111111', 1, 'Mike_3 Johnson', '{"name": "Mike_3 Johnson"}', 10, '2025-08-24T13:20:42.254033'),
('da00a206-d6c9-46bc-89cd-9a47db64f7b6', '08638a27-d640-4e63-bf0d-c396e65cb235', 'f1111111-1111-1111-1111-111111111111', 2, 'mjohnson.work_3@outlook.com', '{"email": "mjohnson.work_3@outlook.com"}', 10, '2025-08-24T13:20:42.254033'),
('7fb75a2a-2660-42a2-8a2e-1a4b9fb1a8bd', '08638a27-d640-4e63-bf0d-c396e65cb235', 'f1111111-1111-1111-1111-111111111111', 4, 'Pit Bull Mix', '{"dog_breed": "Pit Bull Mix"}', 5, '2025-08-24T13:20:42.254033'),
('c1c1d7e8-a6fe-4dec-a094-853d8b9d6dc6', '08638a27-d640-4e63-bf0d-c396e65cb235', 'f1111111-1111-1111-1111-111111111111', 5, '2', '{"dog_age": "2"}', 10, '2025-08-24T13:20:42.254033'),
('662862c4-8a5b-4144-9bc9-c7483e5c0a56', '08638a27-d640-4e63-bf0d-c396e65cb235', 'f1111111-1111-1111-1111-111111111111', 6, 'rarely', '{"behavior": "rarely"}', -10, '2025-08-24T13:20:42.254033'),
('a21062ed-5c00-40e0-b872-bc41f2e286a2', '08638a27-d640-4e63-bf0d-c396e65cb235', 'f1111111-1111-1111-1111-111111111111', 7, '1', '{"walks_per_week": "1"}', 5, '2025-08-24T13:20:42.254033'),
('95395050-10de-493f-8e13-7ffcffb57955', '08638a27-d640-4e63-bf0d-c396e65cb235', 'f1111111-1111-1111-1111-111111111111', 8, 'Dorchester', '{"address": "Dorchester"}', 10, '2025-08-24T13:20:42.254033'),
('1937681d-854d-4c67-b295-0f0c56240033', '08638a27-d640-4e63-bf0d-c396e65cb235', 'f1111111-1111-1111-1111-111111111111', 9, 'under_15', '{"budget": "under_15"}', 0, '2025-08-24T13:20:42.254033');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('a9253060-5165-49b3-9f23-59caa5740f04', '08638a27-d640-4e63-bf0d-c396e65cb235', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'unqualified', '{"name": "Mike_3 Johnson", "email": "mjohnson.work_3@outlook.com"}', 25, 0.25, false, false, NULL, NULL, NULL);


-- Lead 15: Maybe - Jennifer_3 Walsh
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('a002e077-c569-44c0-afe4-1d245dc9133e', 'f1111111-1111-1111-1111-111111111111', 'pawsome_015_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-13T18:20:42.254084', '2025-08-13T18:41:42.254084', '2025-08-13T18:41:42.254084', 8, true, 60, 60, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.83', '{"device_type": "mobile", "completion_time": 60}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('37f9af3c-1137-4b48-8ba1-0125f977b48c', 'a002e077-c569-44c0-afe4-1d245dc9133e', 'facebook', 'social', 'medford_pet_owners', 'pet walking services', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('374a40af-6cbe-4897-96f9-8c29590772aa', 'a002e077-c569-44c0-afe4-1d245dc9133e', 'f1111111-1111-1111-1111-111111111111', 1, 'Jennifer_3 Walsh', '{"name": "Jennifer_3 Walsh"}', 10, '2025-08-13T18:20:42.254084'),
('c672039b-a908-4aca-8550-80daab638587', 'a002e077-c569-44c0-afe4-1d245dc9133e', 'f1111111-1111-1111-1111-111111111111', 2, 'jwalsh.home_3@gmail.com', '{"email": "jwalsh.home_3@gmail.com"}', 10, '2025-08-13T18:20:42.254084'),
('5b55ad4f-bc77-47e0-9eea-1fd8c872a0d7', 'a002e077-c569-44c0-afe4-1d245dc9133e', 'f1111111-1111-1111-1111-111111111111', 4, 'Lab Mix', '{"dog_breed": "Lab Mix"}', 10, '2025-08-13T18:20:42.254084'),
('5b4ca60e-4d1e-473f-b940-24ac01866e52', 'a002e077-c569-44c0-afe4-1d245dc9133e', 'f1111111-1111-1111-1111-111111111111', 5, '6', '{"dog_age": "6"}', 10, '2025-08-13T18:20:42.254084'),
('bbcf3633-5a08-49c7-9db0-d11994637b52', 'a002e077-c569-44c0-afe4-1d245dc9133e', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-13T18:20:42.254084'),
('457b1861-1471-4c78-8962-cbed506ac064', 'a002e077-c569-44c0-afe4-1d245dc9133e', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-13T18:20:42.254084'),
('759e9f66-588d-40a7-8ef1-7f7ac79ac722', 'a002e077-c569-44c0-afe4-1d245dc9133e', 'f1111111-1111-1111-1111-111111111111', 8, 'Medford Square area', '{"address": "Medford Square area"}', 10, '2025-08-13T18:20:42.254084');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('4fef2503-af46-4f89-9d95-9572d81968ed', 'a002e077-c569-44c0-afe4-1d245dc9133e', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "Jennifer_3 Walsh", "email": "jwalsh.home_3@gmail.com"}', 60, 0.60, true, false, NULL, NULL, NULL);


-- Lead 16: Qualified - Emily_4 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('676fb007-9c46-49a1-8537-b216f88e3e37', 'f1111111-1111-1111-1111-111111111111', 'pawsome_016_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-23T01:20:42.254129', '2025-08-23T01:38:42.254130', '2025-08-23T01:38:42.254130', 9, true, 95, 95, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.245', '{"device_type": "desktop", "completion_time": 35}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('44099589-785c-4da5-9164-28251b2f1877', '676fb007-9c46-49a1-8537-b216f88e3e37', 'google', 'cpc', 'premium_dog_walking', 'dog walker near me', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('e0cf8cc0-03b0-45df-941b-ba32431b9cc5', '676fb007-9c46-49a1-8537-b216f88e3e37', 'f1111111-1111-1111-1111-111111111111', 1, 'Emily_4 Rodriguez', '{"name": "Emily_4 Rodriguez"}', 10, '2025-08-23T01:20:42.254129'),
('be4e953e-1ea0-4953-8518-61c4a67f0cfb', '676fb007-9c46-49a1-8537-b216f88e3e37', 'f1111111-1111-1111-1111-111111111111', 2, 'emily.rodriguez_4@mit.edu', '{"email": "emily.rodriguez_4@mit.edu"}', 10, '2025-08-23T01:20:42.254129'),
('813b8b15-80b8-4f1a-a33f-f7e528194df8', '676fb007-9c46-49a1-8537-b216f88e3e37', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0192', '{"phone": "(617) 555-0192"}', 15, '2025-08-23T01:20:42.254129'),
('fafe54ee-ab45-424b-8afa-c38329fca955', '676fb007-9c46-49a1-8537-b216f88e3e37', 'f1111111-1111-1111-1111-111111111111', 4, 'German Shepherd', '{"dog_breed": "German Shepherd"}', 20, '2025-08-23T01:20:42.254129'),
('8dbe13e1-5b87-436d-abcc-9e64bac2eac3', '676fb007-9c46-49a1-8537-b216f88e3e37', 'f1111111-1111-1111-1111-111111111111', 5, '5', '{"dog_age": "5"}', 10, '2025-08-23T01:20:42.254129'),
('86df586e-816f-4e58-b55d-03e57c517423', '676fb007-9c46-49a1-8537-b216f88e3e37', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-23T01:20:42.254129'),
('3a31c0e6-2d5a-4400-80c5-dfb248f9c399', '676fb007-9c46-49a1-8537-b216f88e3e37', 'f1111111-1111-1111-1111-111111111111', 7, '5_plus', '{"walks_per_week": "5_plus"}', 25, '2025-08-23T01:20:42.254129'),
('63659474-3839-4160-a71e-567128d87a3b', '676fb007-9c46-49a1-8537-b216f88e3e37', 'f1111111-1111-1111-1111-111111111111', 8, '1234 Mass Ave, Cambridge', '{"address": "1234 Mass Ave, Cambridge"}', 10, '2025-08-23T01:20:42.254129'),
('4859facd-ca2a-4e2c-9f10-a0f003602fdc', '676fb007-9c46-49a1-8537-b216f88e3e37', 'f1111111-1111-1111-1111-111111111111', 9, '25_35', '{"budget": "25_35"}', 25, '2025-08-23T01:20:42.254129');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('296efffa-16d5-4068-ab9e-fa41901a57dd', '676fb007-9c46-49a1-8537-b216f88e3e37', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Emily_4 Rodriguez", "email": "emily.rodriguez_4@mit.edu", "phone": "(617) 555-0192"}', 95, 0.95, true, false, NULL, NULL, NULL);


-- Lead 17: Maybe - David_4 Park
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('c660feb5-0a49-4349-81ea-6776866eed48', 'f1111111-1111-1111-1111-111111111111', 'pawsome_017_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-20T01:20:42.254182', '2025-08-20T01:53:42.254183', '2025-08-20T01:53:42.254183', 8, true, 65, 65, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.174', '{"device_type": "mobile", "completion_time": 60}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('d701bb8c-c75c-4ba1-ab2e-1939139f72f8', 'c660feb5-0a49-4349-81ea-6776866eed48', 'facebook', 'social', 'local_dog_services', 'professional dog walking', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('e6932255-9a18-497c-946b-7046593687cc', 'c660feb5-0a49-4349-81ea-6776866eed48', 'f1111111-1111-1111-1111-111111111111', 1, 'David_4 Park', '{"name": "David_4 Park"}', 10, '2025-08-20T01:20:42.254182'),
('baeba084-3dfc-4a59-a906-78a7e635b8c9', 'c660feb5-0a49-4349-81ea-6776866eed48', 'f1111111-1111-1111-1111-111111111111', 2, 'david.park_4@gmail.com', '{"email": "david.park_4@gmail.com"}', 10, '2025-08-20T01:20:42.254182'),
('a2d0e376-29fc-44dc-9c88-a13d1f83cd77', 'c660feb5-0a49-4349-81ea-6776866eed48', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0283', '{"phone": "(617) 555-0283"}', 15, '2025-08-20T01:20:42.254182'),
('ca215e5c-ce1e-44bf-aea2-d0120589d1a9', 'c660feb5-0a49-4349-81ea-6776866eed48', 'f1111111-1111-1111-1111-111111111111', 4, 'Beagle', '{"dog_breed": "Beagle"}', 15, '2025-08-20T01:20:42.254182'),
('1fedd1d4-59d5-4ef0-ad9b-998a9a6c0d8e', 'c660feb5-0a49-4349-81ea-6776866eed48', 'f1111111-1111-1111-1111-111111111111', 5, '8', '{"dog_age": "8"}', 10, '2025-08-20T01:20:42.254182'),
('cfb18583-2e04-440c-bed0-7f4eca58859d', 'c660feb5-0a49-4349-81ea-6776866eed48', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-20T01:20:42.254182'),
('5fcc5322-5912-4e6e-9bd4-baa695d6c255', 'c660feb5-0a49-4349-81ea-6776866eed48', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-20T01:20:42.254182'),
('c1ef2667-1eb6-457c-9463-71be8fd56473', 'c660feb5-0a49-4349-81ea-6776866eed48', 'f1111111-1111-1111-1111-111111111111', 8, 'Somerville near Davis Square', '{"address": "Somerville near Davis Square"}', 10, '2025-08-20T01:20:42.254182');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('167b3bb6-cb2d-4291-8a67-a6fbb521cfb6', 'c660feb5-0a49-4349-81ea-6776866eed48', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "David_4 Park", "email": "david.park_4@gmail.com", "phone": "(617) 555-0283"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 18: Qualified - Sarah_4 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('f0d4518d-7aa4-4467-b51a-8317f94387da', 'f1111111-1111-1111-1111-111111111111', 'pawsome_018_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-14T13:20:42.254231', '2025-08-14T13:43:42.254232', '2025-08-14T13:43:42.254232', 9, true, 88, 88, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.190', '{"device_type": "mobile", "completion_time": 54}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('91486bf5-e748-4524-8c9b-92bb5603ac7d', 'f0d4518d-7aa4-4467-b51a-8317f94387da', 'google', 'cpc', 'harvard_students', 'pet walking services', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('7a7b4da7-7be3-44a3-a8e9-63f884a69592', 'f0d4518d-7aa4-4467-b51a-8317f94387da', 'f1111111-1111-1111-1111-111111111111', 1, 'Sarah_4 Kim', '{"name": "Sarah_4 Kim"}', 10, '2025-08-14T13:20:42.254231'),
('36a35aa9-0837-499f-93d8-f96e4d6bd281', 'f0d4518d-7aa4-4467-b51a-8317f94387da', 'f1111111-1111-1111-1111-111111111111', 2, 'sarah.kim_4@harvard.edu', '{"email": "sarah.kim_4@harvard.edu"}', 10, '2025-08-14T13:20:42.254231'),
('e7ee6d91-2c1c-4d0f-8aa9-b6fedaa675e5', 'f0d4518d-7aa4-4467-b51a-8317f94387da', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0374', '{"phone": "(617) 555-0374"}', 15, '2025-08-14T13:20:42.254231'),
('25254b3e-32e5-4f66-98c4-16b027d09abc', 'f0d4518d-7aa4-4467-b51a-8317f94387da', 'f1111111-1111-1111-1111-111111111111', 4, 'Golden Retriever', '{"dog_breed": "Golden Retriever"}', 20, '2025-08-14T13:20:42.254231'),
('a6eeeb97-df5e-49c4-b60e-b96daf9449dd', 'f0d4518d-7aa4-4467-b51a-8317f94387da', 'f1111111-1111-1111-1111-111111111111', 5, '3', '{"dog_age": "3"}', 10, '2025-08-14T13:20:42.254231'),
('5659405b-bcac-4936-ad77-9e807f6a33cd', 'f0d4518d-7aa4-4467-b51a-8317f94387da', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-14T13:20:42.254231'),
('ef6297fb-1428-46a4-8c13-1f286375abfc', 'f0d4518d-7aa4-4467-b51a-8317f94387da', 'f1111111-1111-1111-1111-111111111111', 7, '3_4', '{"walks_per_week": "3_4"}', 20, '2025-08-14T13:20:42.254231'),
('43c61864-23f5-4c2c-bfa4-ea6d4fe880d5', 'f0d4518d-7aa4-4467-b51a-8317f94387da', 'f1111111-1111-1111-1111-111111111111', 8, 'Harvard Square area', '{"address": "Harvard Square area"}', 10, '2025-08-14T13:20:42.254231'),
('3c60790f-c445-4f44-ba84-e7e64d506727', 'f0d4518d-7aa4-4467-b51a-8317f94387da', 'f1111111-1111-1111-1111-111111111111', 9, '20_30', '{"budget": "20_30"}', 20, '2025-08-14T13:20:42.254231');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('a2904edd-9ec3-4400-8bd9-7ffaff4e2296', 'f0d4518d-7aa4-4467-b51a-8317f94387da', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Sarah_4 Kim", "email": "sarah.kim_4@harvard.edu", "phone": "(617) 555-0374"}', 88, 0.88, true, false, NULL, NULL, NULL);


-- Lead 19: Unqualified - Mike_4 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('09f9cd7e-6c9b-4a68-bd14-c58d91153712', 'f1111111-1111-1111-1111-111111111111', 'pawsome_019_unqualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-24T12:20:42.254284', '2025-08-24T12:55:42.254284', '2025-08-24T12:55:42.254284', 9, true, 25, 25, 'no', 'qualified', 'Thank you for your interest. We may not be the best fit, but please reach out if your needs change.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.233', '{"device_type": "desktop", "completion_time": 14}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('3a00c70d-f45f-46f0-9c16-644658d0fcd1', '09f9cd7e-6c9b-4a68-bd14-c58d91153712', 'organic', 'search', 'pawsome_general', 'local dog walker', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('8d44cf26-0e46-474c-9f6d-e321791bcdce', '09f9cd7e-6c9b-4a68-bd14-c58d91153712', 'f1111111-1111-1111-1111-111111111111', 1, 'Mike_4 Johnson', '{"name": "Mike_4 Johnson"}', 10, '2025-08-24T12:20:42.254284'),
('adce980c-ba69-4e92-92a5-9380cbd6da0c', '09f9cd7e-6c9b-4a68-bd14-c58d91153712', 'f1111111-1111-1111-1111-111111111111', 2, 'mjohnson.work_4@outlook.com', '{"email": "mjohnson.work_4@outlook.com"}', 10, '2025-08-24T12:20:42.254284'),
('c98cda97-e01f-4c18-b05b-3006e3da8771', '09f9cd7e-6c9b-4a68-bd14-c58d91153712', 'f1111111-1111-1111-1111-111111111111', 4, 'Pit Bull Mix', '{"dog_breed": "Pit Bull Mix"}', 5, '2025-08-24T12:20:42.254284'),
('fd2b84c1-4b05-4fa3-b0ee-5066883e14eb', '09f9cd7e-6c9b-4a68-bd14-c58d91153712', 'f1111111-1111-1111-1111-111111111111', 5, '2', '{"dog_age": "2"}', 10, '2025-08-24T12:20:42.254284'),
('efdb09e8-1080-45f0-a260-1939d050e5ea', '09f9cd7e-6c9b-4a68-bd14-c58d91153712', 'f1111111-1111-1111-1111-111111111111', 6, 'rarely', '{"behavior": "rarely"}', -10, '2025-08-24T12:20:42.254284'),
('cfbdcf33-3a4d-4c45-993c-5d2925cf8278', '09f9cd7e-6c9b-4a68-bd14-c58d91153712', 'f1111111-1111-1111-1111-111111111111', 7, '1', '{"walks_per_week": "1"}', 5, '2025-08-24T12:20:42.254284'),
('e3676d19-6605-4924-862b-5f6dc24c4d52', '09f9cd7e-6c9b-4a68-bd14-c58d91153712', 'f1111111-1111-1111-1111-111111111111', 8, 'Dorchester', '{"address": "Dorchester"}', 10, '2025-08-24T12:20:42.254284'),
('6c0eb448-1871-49fa-b46f-1b8427c76292', '09f9cd7e-6c9b-4a68-bd14-c58d91153712', 'f1111111-1111-1111-1111-111111111111', 9, 'under_15', '{"budget": "under_15"}', 0, '2025-08-24T12:20:42.254284');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('b5802751-f462-40d4-b313-6315e6b66fbc', '09f9cd7e-6c9b-4a68-bd14-c58d91153712', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'unqualified', '{"name": "Mike_4 Johnson", "email": "mjohnson.work_4@outlook.com"}', 25, 0.25, false, false, NULL, NULL, NULL);


-- Lead 20: Maybe - Jennifer_4 Walsh
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('444144c1-741b-43ae-9069-62ecb1d2970b', 'f1111111-1111-1111-1111-111111111111', 'pawsome_020_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-20T09:20:42.254336', '2025-08-20T09:52:42.254337', '2025-08-20T09:52:42.254337', 7, true, 60, 60, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.77', '{"device_type": "mobile", "completion_time": 31}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('ac8f2d72-25a1-47b6-ac9c-043afe125056', '444144c1-741b-43ae-9069-62ecb1d2970b', 'facebook', 'social', 'medford_pet_owners', 'professional dog walking', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Brookline');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('e31a7ea9-b22c-4114-9b21-8ac1e3009f46', '444144c1-741b-43ae-9069-62ecb1d2970b', 'f1111111-1111-1111-1111-111111111111', 1, 'Jennifer_4 Walsh', '{"name": "Jennifer_4 Walsh"}', 10, '2025-08-20T09:20:42.254336'),
('7ec59ca4-59be-4cd3-b80c-a34deb3512b0', '444144c1-741b-43ae-9069-62ecb1d2970b', 'f1111111-1111-1111-1111-111111111111', 2, 'jwalsh.home_4@gmail.com', '{"email": "jwalsh.home_4@gmail.com"}', 10, '2025-08-20T09:20:42.254336'),
('06818a1a-434c-4389-8f8d-61390ca73d65', '444144c1-741b-43ae-9069-62ecb1d2970b', 'f1111111-1111-1111-1111-111111111111', 4, 'Lab Mix', '{"dog_breed": "Lab Mix"}', 10, '2025-08-20T09:20:42.254336'),
('967c68ae-cca1-4d20-82ef-68a6e82d2944', '444144c1-741b-43ae-9069-62ecb1d2970b', 'f1111111-1111-1111-1111-111111111111', 5, '6', '{"dog_age": "6"}', 10, '2025-08-20T09:20:42.254336'),
('c33e682e-4b15-46bc-9045-14a53a7c4f47', '444144c1-741b-43ae-9069-62ecb1d2970b', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-20T09:20:42.254336'),
('79edf23d-0f3c-4ba8-aadc-1d1ad0aa67a0', '444144c1-741b-43ae-9069-62ecb1d2970b', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-20T09:20:42.254336'),
('d38d5103-ff0c-4f77-a07e-146d12f451fe', '444144c1-741b-43ae-9069-62ecb1d2970b', 'f1111111-1111-1111-1111-111111111111', 8, 'Medford Square area', '{"address": "Medford Square area"}', 10, '2025-08-20T09:20:42.254336');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('6c368c5b-66e5-47db-a930-3dc3372e9880', '444144c1-741b-43ae-9069-62ecb1d2970b', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "Jennifer_4 Walsh", "email": "jwalsh.home_4@gmail.com"}', 60, 0.60, true, false, NULL, NULL, NULL);


-- Lead 21: Qualified - Emily_5 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('48d21fb6-932c-4227-825a-d4a327784337', 'f1111111-1111-1111-1111-111111111111', 'pawsome_021_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-25T04:20:42.254382', '2025-08-25T04:57:42.254383', '2025-08-25T04:57:42.254383', 6, true, 95, 95, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.136', '{"device_type": "desktop", "completion_time": 21}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('2bfdd682-be7a-4449-8521-f90883e0bd7d', '48d21fb6-932c-4227-825a-d4a327784337', 'google', 'cpc', 'premium_dog_walking', 'pet walking services', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('5e64e3ae-39cf-4ce4-8ea7-b3856fc019a0', '48d21fb6-932c-4227-825a-d4a327784337', 'f1111111-1111-1111-1111-111111111111', 1, 'Emily_5 Rodriguez', '{"name": "Emily_5 Rodriguez"}', 10, '2025-08-25T04:20:42.254382'),
('1a0d1d53-eb3d-4b99-9aab-c6f2a3ed7aa2', '48d21fb6-932c-4227-825a-d4a327784337', 'f1111111-1111-1111-1111-111111111111', 2, 'emily.rodriguez_5@mit.edu', '{"email": "emily.rodriguez_5@mit.edu"}', 10, '2025-08-25T04:20:42.254382'),
('a065ea6f-2704-4728-96ed-4539f7011316', '48d21fb6-932c-4227-825a-d4a327784337', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0192', '{"phone": "(617) 555-0192"}', 15, '2025-08-25T04:20:42.254382'),
('06aa71b6-f916-4dae-b7be-55a8a2ca2437', '48d21fb6-932c-4227-825a-d4a327784337', 'f1111111-1111-1111-1111-111111111111', 4, 'German Shepherd', '{"dog_breed": "German Shepherd"}', 20, '2025-08-25T04:20:42.254382'),
('5d19358d-9575-48df-9a5f-724387c4b70a', '48d21fb6-932c-4227-825a-d4a327784337', 'f1111111-1111-1111-1111-111111111111', 5, '5', '{"dog_age": "5"}', 10, '2025-08-25T04:20:42.254382'),
('ebfc5f17-1dc1-4825-8396-a407862e8916', '48d21fb6-932c-4227-825a-d4a327784337', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-25T04:20:42.254382'),
('87676826-e329-4bf5-b9f4-7119f222576b', '48d21fb6-932c-4227-825a-d4a327784337', 'f1111111-1111-1111-1111-111111111111', 7, '5_plus', '{"walks_per_week": "5_plus"}', 25, '2025-08-25T04:20:42.254382'),
('0bc3feac-2a8b-45a6-929f-d9205db0e02a', '48d21fb6-932c-4227-825a-d4a327784337', 'f1111111-1111-1111-1111-111111111111', 8, '1234 Mass Ave, Cambridge', '{"address": "1234 Mass Ave, Cambridge"}', 10, '2025-08-25T04:20:42.254382'),
('7ad5b054-10dc-4e01-8685-fdd1f5465ac2', '48d21fb6-932c-4227-825a-d4a327784337', 'f1111111-1111-1111-1111-111111111111', 9, '25_35', '{"budget": "25_35"}', 25, '2025-08-25T04:20:42.254382');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('0d43d19d-2036-4e18-84fe-e4fa043b04ed', '48d21fb6-932c-4227-825a-d4a327784337', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Emily_5 Rodriguez", "email": "emily.rodriguez_5@mit.edu", "phone": "(617) 555-0192"}', 95, 0.95, true, false, NULL, NULL, NULL);


-- Lead 22: Maybe - David_5 Park
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('c9771a8b-cd45-4255-b631-cad3c55f5413', 'f1111111-1111-1111-1111-111111111111', 'pawsome_022_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-15T06:20:42.254434', '2025-08-15T06:37:42.254434', '2025-08-15T06:37:42.254434', 6, true, 65, 65, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.135', '{"device_type": "mobile", "completion_time": 60}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('a2d5a36d-e9b6-4439-927c-b6452d6030a6', 'c9771a8b-cd45-4255-b631-cad3c55f5413', 'facebook', 'social', 'local_dog_services', 'pet walking services', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('0571b763-fca9-4a90-bc56-7967e73c5745', 'c9771a8b-cd45-4255-b631-cad3c55f5413', 'f1111111-1111-1111-1111-111111111111', 1, 'David_5 Park', '{"name": "David_5 Park"}', 10, '2025-08-15T06:20:42.254434'),
('a8f46d92-67f9-4d3b-ab59-153918a40a92', 'c9771a8b-cd45-4255-b631-cad3c55f5413', 'f1111111-1111-1111-1111-111111111111', 2, 'david.park_5@gmail.com', '{"email": "david.park_5@gmail.com"}', 10, '2025-08-15T06:20:42.254434'),
('5900d918-ec58-4eb8-b149-17e10161a99b', 'c9771a8b-cd45-4255-b631-cad3c55f5413', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0283', '{"phone": "(617) 555-0283"}', 15, '2025-08-15T06:20:42.254434'),
('59809497-bc39-426e-bb4a-da3123e85b9c', 'c9771a8b-cd45-4255-b631-cad3c55f5413', 'f1111111-1111-1111-1111-111111111111', 4, 'Beagle', '{"dog_breed": "Beagle"}', 15, '2025-08-15T06:20:42.254434'),
('308c917e-e068-4cc8-be20-9beb837462d2', 'c9771a8b-cd45-4255-b631-cad3c55f5413', 'f1111111-1111-1111-1111-111111111111', 5, '8', '{"dog_age": "8"}', 10, '2025-08-15T06:20:42.254434'),
('b652c817-32c6-415b-931f-c1b5c953d2ab', 'c9771a8b-cd45-4255-b631-cad3c55f5413', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-15T06:20:42.254434'),
('a6be64a8-b989-4527-94a0-a6c968f37044', 'c9771a8b-cd45-4255-b631-cad3c55f5413', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-15T06:20:42.254434'),
('04835285-f729-49c3-9728-0618412052c3', 'c9771a8b-cd45-4255-b631-cad3c55f5413', 'f1111111-1111-1111-1111-111111111111', 8, 'Somerville near Davis Square', '{"address": "Somerville near Davis Square"}', 10, '2025-08-15T06:20:42.254434');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('1e407b5e-5ee9-4b1c-93a5-3211f3cb3e76', 'c9771a8b-cd45-4255-b631-cad3c55f5413', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "David_5 Park", "email": "david.park_5@gmail.com", "phone": "(617) 555-0283"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 23: Qualified - Sarah_5 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('2f37c5f1-5c3a-4aac-8cbb-24bbd93cdd16', 'f1111111-1111-1111-1111-111111111111', 'pawsome_023_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-12T22:20:42.254477', '2025-08-12T22:44:42.254478', '2025-08-12T22:44:42.254478', 9, true, 88, 88, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.41', '{"device_type": "mobile", "completion_time": 51}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('734f1e7f-020a-452c-b354-4958447f6969', '2f37c5f1-5c3a-4aac-8cbb-24bbd93cdd16', 'google', 'cpc', 'harvard_students', 'professional dog walking', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('dc8faf12-7be4-47a1-b7e4-934cfda6250d', '2f37c5f1-5c3a-4aac-8cbb-24bbd93cdd16', 'f1111111-1111-1111-1111-111111111111', 1, 'Sarah_5 Kim', '{"name": "Sarah_5 Kim"}', 10, '2025-08-12T22:20:42.254477'),
('25407a56-6002-4de2-8622-5de11246730f', '2f37c5f1-5c3a-4aac-8cbb-24bbd93cdd16', 'f1111111-1111-1111-1111-111111111111', 2, 'sarah.kim_5@harvard.edu', '{"email": "sarah.kim_5@harvard.edu"}', 10, '2025-08-12T22:20:42.254477'),
('b49a16b3-6478-410f-896c-74f5e84758ea', '2f37c5f1-5c3a-4aac-8cbb-24bbd93cdd16', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0374', '{"phone": "(617) 555-0374"}', 15, '2025-08-12T22:20:42.254477'),
('8d5a623f-6c36-4366-9e9e-274ad336e801', '2f37c5f1-5c3a-4aac-8cbb-24bbd93cdd16', 'f1111111-1111-1111-1111-111111111111', 4, 'Golden Retriever', '{"dog_breed": "Golden Retriever"}', 20, '2025-08-12T22:20:42.254477'),
('94046f1c-340f-4406-babd-786ea529ea12', '2f37c5f1-5c3a-4aac-8cbb-24bbd93cdd16', 'f1111111-1111-1111-1111-111111111111', 5, '3', '{"dog_age": "3"}', 10, '2025-08-12T22:20:42.254477'),
('ca4353d9-ecd1-4fe6-99dd-44561e7c90a4', '2f37c5f1-5c3a-4aac-8cbb-24bbd93cdd16', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-12T22:20:42.254477'),
('73a07c5f-0476-47a2-a7a3-f805f5ad7ae9', '2f37c5f1-5c3a-4aac-8cbb-24bbd93cdd16', 'f1111111-1111-1111-1111-111111111111', 7, '3_4', '{"walks_per_week": "3_4"}', 20, '2025-08-12T22:20:42.254477'),
('2ac40cee-36f0-4f69-97dd-3402a17f1f6c', '2f37c5f1-5c3a-4aac-8cbb-24bbd93cdd16', 'f1111111-1111-1111-1111-111111111111', 8, 'Harvard Square area', '{"address": "Harvard Square area"}', 10, '2025-08-12T22:20:42.254477'),
('c26c3275-54eb-480d-b3b4-6d2460c5878d', '2f37c5f1-5c3a-4aac-8cbb-24bbd93cdd16', 'f1111111-1111-1111-1111-111111111111', 9, '20_30', '{"budget": "20_30"}', 20, '2025-08-12T22:20:42.254477');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('c963c13e-6652-4d46-a625-c4f109680061', '2f37c5f1-5c3a-4aac-8cbb-24bbd93cdd16', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Sarah_5 Kim", "email": "sarah.kim_5@harvard.edu", "phone": "(617) 555-0374"}', 88, 0.88, true, false, NULL, NULL, NULL);


-- Lead 24: Unqualified - Mike_5 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('ccbc9284-18b1-4b35-854c-b080f97804c1', 'f1111111-1111-1111-1111-111111111111', 'pawsome_024_unqualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-23T13:20:42.254525', '2025-08-23T13:48:42.254525', '2025-08-23T13:48:42.254525', 9, true, 25, 25, 'no', 'qualified', 'Thank you for your interest. We may not be the best fit, but please reach out if your needs change.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.248', '{"device_type": "desktop", "completion_time": 53}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('a5d34efd-d39b-4bb7-9b4a-1ef5e60f322d', 'ccbc9284-18b1-4b35-854c-b080f97804c1', 'organic', 'search', 'pawsome_general', 'dog walking cambridge', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('0300613b-e598-4580-8324-ad6d30536c8a', 'ccbc9284-18b1-4b35-854c-b080f97804c1', 'f1111111-1111-1111-1111-111111111111', 1, 'Mike_5 Johnson', '{"name": "Mike_5 Johnson"}', 10, '2025-08-23T13:20:42.254525'),
('bee6d019-dc39-444e-9a6c-a83a934ce12f', 'ccbc9284-18b1-4b35-854c-b080f97804c1', 'f1111111-1111-1111-1111-111111111111', 2, 'mjohnson.work_5@outlook.com', '{"email": "mjohnson.work_5@outlook.com"}', 10, '2025-08-23T13:20:42.254525'),
('40425321-0ebf-40c7-b05a-e54f2967742c', 'ccbc9284-18b1-4b35-854c-b080f97804c1', 'f1111111-1111-1111-1111-111111111111', 4, 'Pit Bull Mix', '{"dog_breed": "Pit Bull Mix"}', 5, '2025-08-23T13:20:42.254525'),
('227d8074-2514-42c2-9bcc-113af3dd9650', 'ccbc9284-18b1-4b35-854c-b080f97804c1', 'f1111111-1111-1111-1111-111111111111', 5, '2', '{"dog_age": "2"}', 10, '2025-08-23T13:20:42.254525'),
('02b09a3c-b38c-4ce4-9715-a74dbfc90c40', 'ccbc9284-18b1-4b35-854c-b080f97804c1', 'f1111111-1111-1111-1111-111111111111', 6, 'rarely', '{"behavior": "rarely"}', -10, '2025-08-23T13:20:42.254525'),
('ac62437a-5b2e-4dac-be06-948fa76365e9', 'ccbc9284-18b1-4b35-854c-b080f97804c1', 'f1111111-1111-1111-1111-111111111111', 7, '1', '{"walks_per_week": "1"}', 5, '2025-08-23T13:20:42.254525'),
('2616380b-1bab-4271-9cd1-76181c59de7b', 'ccbc9284-18b1-4b35-854c-b080f97804c1', 'f1111111-1111-1111-1111-111111111111', 8, 'Dorchester', '{"address": "Dorchester"}', 10, '2025-08-23T13:20:42.254525'),
('af5778bf-5f06-4c6f-9965-5e2c870ea7a0', 'ccbc9284-18b1-4b35-854c-b080f97804c1', 'f1111111-1111-1111-1111-111111111111', 9, 'under_15', '{"budget": "under_15"}', 0, '2025-08-23T13:20:42.254525');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('e22ba3ac-3b3b-4c5c-a11d-fa29635ff4db', 'ccbc9284-18b1-4b35-854c-b080f97804c1', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'unqualified', '{"name": "Mike_5 Johnson", "email": "mjohnson.work_5@outlook.com"}', 25, 0.25, false, false, NULL, NULL, NULL);


-- Lead 25: Maybe - Jennifer_5 Walsh
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('d7256266-2559-499d-a7a1-3fc8a9192952', 'f1111111-1111-1111-1111-111111111111', 'pawsome_025_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-23T02:20:42.254569', '2025-08-23T03:04:42.254569', '2025-08-23T03:04:42.254569', 6, true, 60, 60, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.214', '{"device_type": "mobile", "completion_time": 56}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('51277f07-6f33-4dac-95ed-a6ff7dd69794', 'd7256266-2559-499d-a7a1-3fc8a9192952', 'facebook', 'social', 'medford_pet_owners', 'pet walking services', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Newton');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('44bf56b9-7239-4da3-af1d-96f0fab1f8bc', 'd7256266-2559-499d-a7a1-3fc8a9192952', 'f1111111-1111-1111-1111-111111111111', 1, 'Jennifer_5 Walsh', '{"name": "Jennifer_5 Walsh"}', 10, '2025-08-23T02:20:42.254569'),
('7bb28d2d-0f07-4ade-af47-0ed5ec41f4df', 'd7256266-2559-499d-a7a1-3fc8a9192952', 'f1111111-1111-1111-1111-111111111111', 2, 'jwalsh.home_5@gmail.com', '{"email": "jwalsh.home_5@gmail.com"}', 10, '2025-08-23T02:20:42.254569'),
('6a22162f-310a-4a4b-8f00-f9c473c636a8', 'd7256266-2559-499d-a7a1-3fc8a9192952', 'f1111111-1111-1111-1111-111111111111', 4, 'Lab Mix', '{"dog_breed": "Lab Mix"}', 10, '2025-08-23T02:20:42.254569'),
('5b0b8012-1d4f-468b-bf3f-f248fa941fbb', 'd7256266-2559-499d-a7a1-3fc8a9192952', 'f1111111-1111-1111-1111-111111111111', 5, '6', '{"dog_age": "6"}', 10, '2025-08-23T02:20:42.254569'),
('805255ee-1cad-42f3-b941-635d1eda16f1', 'd7256266-2559-499d-a7a1-3fc8a9192952', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-23T02:20:42.254569'),
('901652d7-c971-4c90-bee0-b8e4adb0664d', 'd7256266-2559-499d-a7a1-3fc8a9192952', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-23T02:20:42.254569'),
('8d4a7084-ecda-46d3-81aa-1f312db8d16c', 'd7256266-2559-499d-a7a1-3fc8a9192952', 'f1111111-1111-1111-1111-111111111111', 8, 'Medford Square area', '{"address": "Medford Square area"}', 10, '2025-08-23T02:20:42.254569');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('bd4d6e79-2031-48e2-bc64-5edca8a241ba', 'd7256266-2559-499d-a7a1-3fc8a9192952', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "Jennifer_5 Walsh", "email": "jwalsh.home_5@gmail.com"}', 60, 0.60, true, false, NULL, NULL, NULL);


-- Lead 26: Qualified - Emily_6 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('5710bca4-034c-409a-84a7-662e22448145', 'f1111111-1111-1111-1111-111111111111', 'pawsome_026_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-21T08:20:42.254609', '2025-08-21T08:36:42.254610', '2025-08-21T08:36:42.254610', 9, true, 95, 95, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.81', '{"device_type": "desktop", "completion_time": 18}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('a47d3f2f-02ab-4333-9412-17062455c160', '5710bca4-034c-409a-84a7-662e22448145', 'google', 'cpc', 'premium_dog_walking', 'professional dog walking', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('8d921e18-4b9a-4908-a735-4d16e4013b02', '5710bca4-034c-409a-84a7-662e22448145', 'f1111111-1111-1111-1111-111111111111', 1, 'Emily_6 Rodriguez', '{"name": "Emily_6 Rodriguez"}', 10, '2025-08-21T08:20:42.254609'),
('b7afedec-222d-4344-a747-b25879fb4ce2', '5710bca4-034c-409a-84a7-662e22448145', 'f1111111-1111-1111-1111-111111111111', 2, 'emily.rodriguez_6@mit.edu', '{"email": "emily.rodriguez_6@mit.edu"}', 10, '2025-08-21T08:20:42.254609'),
('116cb3c1-f9ec-4700-9c26-f9f6150ce635', '5710bca4-034c-409a-84a7-662e22448145', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0192', '{"phone": "(617) 555-0192"}', 15, '2025-08-21T08:20:42.254609'),
('55980e81-c067-4b4f-91ee-c7f104b3df3c', '5710bca4-034c-409a-84a7-662e22448145', 'f1111111-1111-1111-1111-111111111111', 4, 'German Shepherd', '{"dog_breed": "German Shepherd"}', 20, '2025-08-21T08:20:42.254609'),
('fe16c3e3-0df1-45a9-b259-ae6cdcfff99a', '5710bca4-034c-409a-84a7-662e22448145', 'f1111111-1111-1111-1111-111111111111', 5, '5', '{"dog_age": "5"}', 10, '2025-08-21T08:20:42.254609'),
('7775d310-a19e-4b8b-93f7-f0befe356047', '5710bca4-034c-409a-84a7-662e22448145', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-21T08:20:42.254609'),
('9ed69b0d-07d3-4114-b8ed-172b9af35883', '5710bca4-034c-409a-84a7-662e22448145', 'f1111111-1111-1111-1111-111111111111', 7, '5_plus', '{"walks_per_week": "5_plus"}', 25, '2025-08-21T08:20:42.254609'),
('eb17df29-bfa0-4c70-b7d3-fadfed52cfd2', '5710bca4-034c-409a-84a7-662e22448145', 'f1111111-1111-1111-1111-111111111111', 8, '1234 Mass Ave, Cambridge', '{"address": "1234 Mass Ave, Cambridge"}', 10, '2025-08-21T08:20:42.254609'),
('ad8302b4-e44d-41c8-9aa5-8a88da930dec', '5710bca4-034c-409a-84a7-662e22448145', 'f1111111-1111-1111-1111-111111111111', 9, '25_35', '{"budget": "25_35"}', 25, '2025-08-21T08:20:42.254609');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('7e9ffc19-2013-40b0-b62c-7feb570db34d', '5710bca4-034c-409a-84a7-662e22448145', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Emily_6 Rodriguez", "email": "emily.rodriguez_6@mit.edu", "phone": "(617) 555-0192"}', 95, 0.95, true, false, NULL, NULL, NULL);


-- Lead 27: Maybe - David_6 Park
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('501abaaa-dd43-42ad-a0c2-e7af3103b5b1', 'f1111111-1111-1111-1111-111111111111', 'pawsome_027_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-26T07:20:42.254660', '2025-08-26T07:58:42.254661', '2025-08-26T07:58:42.254661', 8, true, 65, 65, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.198', '{"device_type": "mobile", "completion_time": 56}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('3ba02f88-7bfd-4a9b-a155-2a40a6e5b511', '501abaaa-dd43-42ad-a0c2-e7af3103b5b1', 'facebook', 'social', 'local_dog_services', 'professional dog walking', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('441acc04-c4dc-4edf-96b1-65b52956db6f', '501abaaa-dd43-42ad-a0c2-e7af3103b5b1', 'f1111111-1111-1111-1111-111111111111', 1, 'David_6 Park', '{"name": "David_6 Park"}', 10, '2025-08-26T07:20:42.254660'),
('733879d9-c286-4cd7-b469-c8956d7716a5', '501abaaa-dd43-42ad-a0c2-e7af3103b5b1', 'f1111111-1111-1111-1111-111111111111', 2, 'david.park_6@gmail.com', '{"email": "david.park_6@gmail.com"}', 10, '2025-08-26T07:20:42.254660'),
('eddf697a-ae34-48eb-882b-320d43e5f690', '501abaaa-dd43-42ad-a0c2-e7af3103b5b1', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0283', '{"phone": "(617) 555-0283"}', 15, '2025-08-26T07:20:42.254660'),
('b5f051db-ac0b-4f9d-9455-9ae7fe377bf0', '501abaaa-dd43-42ad-a0c2-e7af3103b5b1', 'f1111111-1111-1111-1111-111111111111', 4, 'Beagle', '{"dog_breed": "Beagle"}', 15, '2025-08-26T07:20:42.254660'),
('7fe342a6-bf2c-4ab8-92bd-b6c4b2ae8a92', '501abaaa-dd43-42ad-a0c2-e7af3103b5b1', 'f1111111-1111-1111-1111-111111111111', 5, '8', '{"dog_age": "8"}', 10, '2025-08-26T07:20:42.254660'),
('ad9634fe-f4e0-4c16-b56f-4e89cb6ae553', '501abaaa-dd43-42ad-a0c2-e7af3103b5b1', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-26T07:20:42.254660'),
('26bf13dd-047f-4eda-88da-23e6dac11901', '501abaaa-dd43-42ad-a0c2-e7af3103b5b1', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-26T07:20:42.254660'),
('79b23950-1faf-4316-be97-7d424673c6dd', '501abaaa-dd43-42ad-a0c2-e7af3103b5b1', 'f1111111-1111-1111-1111-111111111111', 8, 'Somerville near Davis Square', '{"address": "Somerville near Davis Square"}', 10, '2025-08-26T07:20:42.254660');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('9a882cea-158a-45ca-b940-68ff564d4a1d', '501abaaa-dd43-42ad-a0c2-e7af3103b5b1', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "David_6 Park", "email": "david.park_6@gmail.com", "phone": "(617) 555-0283"}', 65, 0.65, true, false, NULL, NULL, NULL);


-- Lead 28: Qualified - Sarah_6 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('597289dd-7ecf-414d-9088-c895438efc66', 'f1111111-1111-1111-1111-111111111111', 'pawsome_028_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-18T01:20:42.254703', '2025-08-18T01:42:42.254704', '2025-08-18T01:42:42.254704', 6, true, 88, 88, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.152', '{"device_type": "mobile", "completion_time": 15}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('94f529fb-cdab-4f22-9e77-509ea78b1931', '597289dd-7ecf-414d-9088-c895438efc66', 'google', 'cpc', 'harvard_students', 'local dog walker', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('95413e86-74e8-4bc4-b0e0-27c104fb17ba', '597289dd-7ecf-414d-9088-c895438efc66', 'f1111111-1111-1111-1111-111111111111', 1, 'Sarah_6 Kim', '{"name": "Sarah_6 Kim"}', 10, '2025-08-18T01:20:42.254703'),
('ab692714-e610-4db3-b2fa-d7d5d658171a', '597289dd-7ecf-414d-9088-c895438efc66', 'f1111111-1111-1111-1111-111111111111', 2, 'sarah.kim_6@harvard.edu', '{"email": "sarah.kim_6@harvard.edu"}', 10, '2025-08-18T01:20:42.254703'),
('7ec41c19-a0c3-40c1-962c-2e2c150a00cb', '597289dd-7ecf-414d-9088-c895438efc66', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0374', '{"phone": "(617) 555-0374"}', 15, '2025-08-18T01:20:42.254703'),
('daa48c5c-458b-474a-977d-9e09f6583cda', '597289dd-7ecf-414d-9088-c895438efc66', 'f1111111-1111-1111-1111-111111111111', 4, 'Golden Retriever', '{"dog_breed": "Golden Retriever"}', 20, '2025-08-18T01:20:42.254703'),
('54af5118-f687-42a7-8703-68882f37ed07', '597289dd-7ecf-414d-9088-c895438efc66', 'f1111111-1111-1111-1111-111111111111', 5, '3', '{"dog_age": "3"}', 10, '2025-08-18T01:20:42.254703'),
('6e3d0b1b-8e27-4c98-8148-23f6ed2c46d2', '597289dd-7ecf-414d-9088-c895438efc66', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-18T01:20:42.254703'),
('4a11fc01-029b-405f-92d5-97698b41e7a4', '597289dd-7ecf-414d-9088-c895438efc66', 'f1111111-1111-1111-1111-111111111111', 7, '3_4', '{"walks_per_week": "3_4"}', 20, '2025-08-18T01:20:42.254703'),
('d4c3d4be-5781-40e7-9033-57ad16b10833', '597289dd-7ecf-414d-9088-c895438efc66', 'f1111111-1111-1111-1111-111111111111', 8, 'Harvard Square area', '{"address": "Harvard Square area"}', 10, '2025-08-18T01:20:42.254703'),
('03bb112b-7c47-45b1-af51-cde9f0318f84', '597289dd-7ecf-414d-9088-c895438efc66', 'f1111111-1111-1111-1111-111111111111', 9, '20_30', '{"budget": "20_30"}', 20, '2025-08-18T01:20:42.254703');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('a3ede0aa-c101-451c-8d24-c5c6b23357c6', '597289dd-7ecf-414d-9088-c895438efc66', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Sarah_6 Kim", "email": "sarah.kim_6@harvard.edu", "phone": "(617) 555-0374"}', 88, 0.88, true, false, NULL, NULL, NULL);


-- Lead 29: Unqualified - Mike_6 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('3b84d1a9-60e4-4666-b818-ea59b29062ff', 'f1111111-1111-1111-1111-111111111111', 'pawsome_029_unqualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-14T09:20:42.254749', '2025-08-14T09:52:42.254750', '2025-08-14T09:52:42.254750', 8, true, 25, 25, 'no', 'qualified', 'Thank you for your interest. We may not be the best fit, but please reach out if your needs change.', 'active', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', '192.168.1.47', '{"device_type": "desktop", "completion_time": 17}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('4f827eef-5b0c-47e9-8936-cc8ea3cccfaf', '3b84d1a9-60e4-4666-b818-ea59b29062ff', 'organic', 'search', 'pawsome_general', 'local dog walker', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Lexington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('30cb599e-491c-41c7-975f-a44102137c78', '3b84d1a9-60e4-4666-b818-ea59b29062ff', 'f1111111-1111-1111-1111-111111111111', 1, 'Mike_6 Johnson', '{"name": "Mike_6 Johnson"}', 10, '2025-08-14T09:20:42.254749'),
('35838837-171a-4d4b-a1fb-d79ac9257695', '3b84d1a9-60e4-4666-b818-ea59b29062ff', 'f1111111-1111-1111-1111-111111111111', 2, 'mjohnson.work_6@outlook.com', '{"email": "mjohnson.work_6@outlook.com"}', 10, '2025-08-14T09:20:42.254749'),
('83b7113f-c4dc-461f-8d75-325d2938a131', '3b84d1a9-60e4-4666-b818-ea59b29062ff', 'f1111111-1111-1111-1111-111111111111', 4, 'Pit Bull Mix', '{"dog_breed": "Pit Bull Mix"}', 5, '2025-08-14T09:20:42.254749'),
('5c4429bb-7d28-4a75-b48b-62e3986ea7b3', '3b84d1a9-60e4-4666-b818-ea59b29062ff', 'f1111111-1111-1111-1111-111111111111', 5, '2', '{"dog_age": "2"}', 10, '2025-08-14T09:20:42.254749'),
('a08edc69-a40d-464f-a891-4fb3b5a66194', '3b84d1a9-60e4-4666-b818-ea59b29062ff', 'f1111111-1111-1111-1111-111111111111', 6, 'rarely', '{"behavior": "rarely"}', -10, '2025-08-14T09:20:42.254749'),
('be854c62-56cd-422d-98c4-2f0272847273', '3b84d1a9-60e4-4666-b818-ea59b29062ff', 'f1111111-1111-1111-1111-111111111111', 7, '1', '{"walks_per_week": "1"}', 5, '2025-08-14T09:20:42.254749'),
('ff39e24e-f161-4c63-8416-33b3e6e4bf42', '3b84d1a9-60e4-4666-b818-ea59b29062ff', 'f1111111-1111-1111-1111-111111111111', 8, 'Dorchester', '{"address": "Dorchester"}', 10, '2025-08-14T09:20:42.254749'),
('1c4a4903-0de6-4078-89d5-211d1ea2202b', '3b84d1a9-60e4-4666-b818-ea59b29062ff', 'f1111111-1111-1111-1111-111111111111', 9, 'under_15', '{"budget": "under_15"}', 0, '2025-08-14T09:20:42.254749');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('08dc8e2b-06ee-4ea7-a249-09abb4ec52ab', '3b84d1a9-60e4-4666-b818-ea59b29062ff', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'unqualified', '{"name": "Mike_6 Johnson", "email": "mjohnson.work_6@outlook.com"}', 25, 0.25, false, false, NULL, NULL, NULL);


-- Lead 30: Maybe - Jennifer_6 Walsh
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('5f85a4de-9d5e-4b2b-8963-a579e1b48bec', 'f1111111-1111-1111-1111-111111111111', 'pawsome_030_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-23T12:20:42.254793', '2025-08-23T12:37:42.254794', '2025-08-23T12:37:42.254794', 9, true, 60, 60, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.234', '{"device_type": "mobile", "completion_time": 49}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('85c94f17-5ee3-41f1-a53b-e0e097b36b19', '5f85a4de-9d5e-4b2b-8963-a579e1b48bec', 'facebook', 'social', 'medford_pet_owners', 'local dog walker', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('4e3d681e-bca1-4998-95ae-367de3778a86', '5f85a4de-9d5e-4b2b-8963-a579e1b48bec', 'f1111111-1111-1111-1111-111111111111', 1, 'Jennifer_6 Walsh', '{"name": "Jennifer_6 Walsh"}', 10, '2025-08-23T12:20:42.254793'),
('d8b68a93-ba73-41ab-876d-a8dd9c99f4fc', '5f85a4de-9d5e-4b2b-8963-a579e1b48bec', 'f1111111-1111-1111-1111-111111111111', 2, 'jwalsh.home_6@gmail.com', '{"email": "jwalsh.home_6@gmail.com"}', 10, '2025-08-23T12:20:42.254793'),
('d175fd51-f8d3-4f2a-b94c-7d58ecb85a22', '5f85a4de-9d5e-4b2b-8963-a579e1b48bec', 'f1111111-1111-1111-1111-111111111111', 4, 'Lab Mix', '{"dog_breed": "Lab Mix"}', 10, '2025-08-23T12:20:42.254793'),
('4d6cff32-78f3-4447-8639-b98e41a2b379', '5f85a4de-9d5e-4b2b-8963-a579e1b48bec', 'f1111111-1111-1111-1111-111111111111', 5, '6', '{"dog_age": "6"}', 10, '2025-08-23T12:20:42.254793'),
('ded1b726-b05f-4423-944d-5d528bfbea72', '5f85a4de-9d5e-4b2b-8963-a579e1b48bec', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-23T12:20:42.254793'),
('57fb426f-d1b2-4368-86fb-e1d35e29f381', '5f85a4de-9d5e-4b2b-8963-a579e1b48bec', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-23T12:20:42.254793'),
('46c924e3-b25f-4ca3-8103-18668326d704', '5f85a4de-9d5e-4b2b-8963-a579e1b48bec', 'f1111111-1111-1111-1111-111111111111', 8, 'Medford Square area', '{"address": "Medford Square area"}', 10, '2025-08-23T12:20:42.254793');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('53ac7454-c984-40ad-81a1-a5c639491a5d', '5f85a4de-9d5e-4b2b-8963-a579e1b48bec', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "Jennifer_6 Walsh", "email": "jwalsh.home_6@gmail.com"}', 60, 0.60, true, false, NULL, NULL, NULL);


SELECT 'Generated 30 realistic lead sessions for pawsome!' as status;

