-- Generated realistic lead sessions for Pawsome Dog Walking
-- Run this script to generate 30 diverse leads


-- Lead 1: Qualified - Emily Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('e2e5d915-f406-4c0e-963c-c2a2d93c8394', 'f1111111-1111-1111-1111-111111111111', 'sess_001_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-17T22:47:53.370911', '2025-08-17T23:20:53.370923', '2025-08-17T23:20:53.370923', 9, true, 95, 95, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.215', '{"device_type": "desktop", "completion_time": 56}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('3b9bad8c-e859-43c9-8e43-c36cacd36c88', 'e2e5d915-f406-4c0e-963c-c2a2d93c8394', 'google', 'cpc', 'premium_dog_walking', 'professional dog walking', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('5b1058f1-e38d-4162-ba71-744a608f9fab', 'e2e5d915-f406-4c0e-963c-c2a2d93c8394', 'f1111111-1111-1111-1111-111111111111', 1, 'Emily Rodriguez', '{"name": "Emily Rodriguez"}', 10, '2025-08-17T22:47:53.370911'),
('5098c359-799f-4352-ba1c-53f6f78e6ce3', 'e2e5d915-f406-4c0e-963c-c2a2d93c8394', 'f1111111-1111-1111-1111-111111111111', 2, 'emily.rodriguez@mit.edu', '{"email": "emily.rodriguez@mit.edu"}', 10, '2025-08-17T22:47:53.370911'),
('459fe0be-74c1-4f0e-a33f-9ee315cf2d10', 'e2e5d915-f406-4c0e-963c-c2a2d93c8394', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0192', '{"phone": "(617) 555-0192"}', 15, '2025-08-17T22:47:53.370911'),
('929c6e2b-7cfe-47f0-8340-b81e36d00ee1', 'e2e5d915-f406-4c0e-963c-c2a2d93c8394', 'f1111111-1111-1111-1111-111111111111', 4, 'German Shepherd', '{"dog_breed": "German Shepherd"}', 20, '2025-08-17T22:47:53.370911'),
('e7d4715c-13ff-41a9-8307-a90a9c6eb395', 'e2e5d915-f406-4c0e-963c-c2a2d93c8394', 'f1111111-1111-1111-1111-111111111111', 5, '5', '{"dog_age": "5"}', 15, '2025-08-17T22:47:53.370911'),
('2ed8e077-5c79-4a7e-81da-53922c652a26', 'e2e5d915-f406-4c0e-963c-c2a2d93c8394', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-17T22:47:53.370911'),
('6138256b-cb07-4d0a-9f9d-8cd80578804c', 'e2e5d915-f406-4c0e-963c-c2a2d93c8394', 'f1111111-1111-1111-1111-111111111111', 7, '5_plus', '{"walks_per_week": "5_plus"}', 25, '2025-08-17T22:47:53.370911'),
('1f132937-8774-454a-9e85-c4bf81495829', 'e2e5d915-f406-4c0e-963c-c2a2d93c8394', 'f1111111-1111-1111-1111-111111111111', 8, '1234 Mass Ave, Cambridge', '{"address": "1234 Mass Ave, Cambridge"}', 20, '2025-08-17T22:47:53.370911'),
('ff2d7d6f-3f26-499a-a187-b6d30c2995e6', 'e2e5d915-f406-4c0e-963c-c2a2d93c8394', 'f1111111-1111-1111-1111-111111111111', 9, '25_35', '{"budget": "25_35"}', 25, '2025-08-17T22:47:53.370911');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('26e1cac9-af24-47f6-9009-5c51654d6f91', 'e2e5d915-f406-4c0e-963c-c2a2d93c8394', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Emily Rodriguez", "email": "emily.rodriguez@mit.edu", "phone": "(617) 555-0192"}', 95, 0.95, true);


-- Lead 2: Maybe - David Park
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('809116ef-7a84-41a3-982a-b5b47d70f8a4', 'f1111111-1111-1111-1111-111111111111', 'sess_002_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-21T15:47:53.371014', '2025-08-21T16:20:53.371016', '2025-08-21T16:20:53.371016', 6, true, 65, 65, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.18', '{"device_type": "mobile", "completion_time": 26}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('06d1795a-b3ff-4df9-96cd-32fb0a39e861', '809116ef-7a84-41a3-982a-b5b47d70f8a4', 'facebook', 'social', 'local_dog_services', 'local dog walker', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('c0310082-0298-418d-9c74-b986aa36376b', '809116ef-7a84-41a3-982a-b5b47d70f8a4', 'f1111111-1111-1111-1111-111111111111', 1, 'David Park', '{"name": "David Park"}', 10, '2025-08-21T15:47:53.371014'),
('41427d84-430f-4d98-b13d-c66616e2467b', '809116ef-7a84-41a3-982a-b5b47d70f8a4', 'f1111111-1111-1111-1111-111111111111', 2, 'david.park@gmail.com', '{"email": "david.park@gmail.com"}', 10, '2025-08-21T15:47:53.371014'),
('80c709bb-7889-4f91-aba9-c5e4e2e4b61f', '809116ef-7a84-41a3-982a-b5b47d70f8a4', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0283', '{"phone": "(617) 555-0283"}', 15, '2025-08-21T15:47:53.371014'),
('222fe3e4-66fc-490e-944d-18fec9719ad8', '809116ef-7a84-41a3-982a-b5b47d70f8a4', 'f1111111-1111-1111-1111-111111111111', 4, 'Beagle', '{"dog_breed": "Beagle"}', 15, '2025-08-21T15:47:53.371014'),
('8aa81848-04cb-4866-8d19-cd4cce0030fa', '809116ef-7a84-41a3-982a-b5b47d70f8a4', 'f1111111-1111-1111-1111-111111111111', 5, '8', '{"dog_age": "8"}', 15, '2025-08-21T15:47:53.371014'),
('40a63b76-54f8-4a92-876b-c3e05e52a25f', '809116ef-7a84-41a3-982a-b5b47d70f8a4', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-21T15:47:53.371014'),
('98bc26ff-1aa7-4b92-8937-f633dccf0fa5', '809116ef-7a84-41a3-982a-b5b47d70f8a4', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-21T15:47:53.371014'),
('80415134-092b-4340-b5f7-e25eb6f5b84c', '809116ef-7a84-41a3-982a-b5b47d70f8a4', 'f1111111-1111-1111-1111-111111111111', 8, 'Somerville near Davis Square', '{"address": "Somerville near Davis Square"}', 20, '2025-08-21T15:47:53.371014');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('51cbb2cf-bc10-46f2-9d00-e2248b7cd409', '809116ef-7a84-41a3-982a-b5b47d70f8a4', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "David Park", "email": "david.park@gmail.com", "phone": "(617) 555-0283"}', 65, 0.65, true);


-- Lead 3: Qualified - Sarah Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('296f1ad3-e5b2-429e-92c2-56d9786eca5b', 'f1111111-1111-1111-1111-111111111111', 'sess_003_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-21T17:47:53.371069', '2025-08-21T18:28:53.371070', '2025-08-21T18:28:53.371070', 6, true, 88, 88, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.24', '{"device_type": "mobile", "completion_time": 31}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('140af2b5-1b57-4793-9371-f06518fd7583', '296f1ad3-e5b2-429e-92c2-56d9786eca5b', 'google', 'cpc', 'harvard_students', 'dog walking cambridge', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('15bd082b-97ae-42c5-ba99-31607c960130', '296f1ad3-e5b2-429e-92c2-56d9786eca5b', 'f1111111-1111-1111-1111-111111111111', 1, 'Sarah Kim', '{"name": "Sarah Kim"}', 10, '2025-08-21T17:47:53.371069'),
('8d4dc18d-ca69-47a6-ac71-9c2d91b312c6', '296f1ad3-e5b2-429e-92c2-56d9786eca5b', 'f1111111-1111-1111-1111-111111111111', 2, 'sarah.kim@harvard.edu', '{"email": "sarah.kim@harvard.edu"}', 10, '2025-08-21T17:47:53.371069'),
('a78ddeba-04a5-4295-b5cc-97782d59be85', '296f1ad3-e5b2-429e-92c2-56d9786eca5b', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0374', '{"phone": "(617) 555-0374"}', 15, '2025-08-21T17:47:53.371069'),
('1617554d-70b2-4cfe-859a-6eb97c65c860', '296f1ad3-e5b2-429e-92c2-56d9786eca5b', 'f1111111-1111-1111-1111-111111111111', 4, 'Golden Retriever', '{"dog_breed": "Golden Retriever"}', 20, '2025-08-21T17:47:53.371069'),
('288a5c5b-1e70-4521-8fa3-b87de5f8748a', '296f1ad3-e5b2-429e-92c2-56d9786eca5b', 'f1111111-1111-1111-1111-111111111111', 5, '3', '{"dog_age": "3"}', 15, '2025-08-21T17:47:53.371069'),
('116af1c5-92bd-47f1-94d6-7d1360c9f04e', '296f1ad3-e5b2-429e-92c2-56d9786eca5b', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-21T17:47:53.371069'),
('38e0fcd9-0573-4e26-a5fa-0a885b6f1ed1', '296f1ad3-e5b2-429e-92c2-56d9786eca5b', 'f1111111-1111-1111-1111-111111111111', 7, '3_4', '{"walks_per_week": "3_4"}', 20, '2025-08-21T17:47:53.371069'),
('b2debd50-e303-4901-9f2f-4f4e63b4ccd8', '296f1ad3-e5b2-429e-92c2-56d9786eca5b', 'f1111111-1111-1111-1111-111111111111', 8, 'Harvard Square area', '{"address": "Harvard Square area"}', 20, '2025-08-21T17:47:53.371069'),
('f4f7b97b-46ca-4cbd-9955-01b2a7982ad1', '296f1ad3-e5b2-429e-92c2-56d9786eca5b', 'f1111111-1111-1111-1111-111111111111', 9, '20_30', '{"budget": "20_30"}', 20, '2025-08-21T17:47:53.371069');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('b89f5739-7a44-43f9-955b-5994d9a5854b', '296f1ad3-e5b2-429e-92c2-56d9786eca5b', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Sarah Kim", "email": "sarah.kim@harvard.edu", "phone": "(617) 555-0374"}', 88, 0.88, true);


-- Lead 4: Unqualified - Mike Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('87af5e36-1c65-40a2-9885-a86413625107', 'f1111111-1111-1111-1111-111111111111', 'sess_004_unqualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-22T17:47:53.371122', '2025-08-22T18:32:53.371123', '2025-08-22T18:32:53.371123', 9, true, 25, 25, 'no', 'qualified', 'Thank you for your interest. We may not be the best fit, but please reach out if your needs change.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.19', '{"device_type": "desktop", "completion_time": 38}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('8ac67d27-73bb-4605-86ba-0d6274a50ae4', '87af5e36-1c65-40a2-9885-a86413625107', 'organic', 'search', 'dog_walking_general', 'local dog walker', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('cbcb1762-5faa-424a-8d3c-6c2c16e76dd5', '87af5e36-1c65-40a2-9885-a86413625107', 'f1111111-1111-1111-1111-111111111111', 1, 'Mike Johnson', '{"name": "Mike Johnson"}', 10, '2025-08-22T17:47:53.371122'),
('7b031a2c-d275-4513-8f56-c7d8c5cdb16b', '87af5e36-1c65-40a2-9885-a86413625107', 'f1111111-1111-1111-1111-111111111111', 2, 'mjohnson.work@outlook.com', '{"email": "mjohnson.work@outlook.com"}', 10, '2025-08-22T17:47:53.371122'),
('d159bfcc-accc-4be2-a04d-4898c5079409', '87af5e36-1c65-40a2-9885-a86413625107', 'f1111111-1111-1111-1111-111111111111', 4, 'Pit Bull Mix', '{"dog_breed": "Pit Bull Mix"}', 5, '2025-08-22T17:47:53.371122'),
('b431400a-7484-428e-aef4-80369161dce5', '87af5e36-1c65-40a2-9885-a86413625107', 'f1111111-1111-1111-1111-111111111111', 5, '2', '{"dog_age": "2"}', 15, '2025-08-22T17:47:53.371122'),
('3c6912f7-1c54-4088-a30b-7d843262ca77', '87af5e36-1c65-40a2-9885-a86413625107', 'f1111111-1111-1111-1111-111111111111', 6, 'rarely', '{"behavior": "rarely"}', -10, '2025-08-22T17:47:53.371122'),
('f9203b74-21a1-4801-a70c-17162626336b', '87af5e36-1c65-40a2-9885-a86413625107', 'f1111111-1111-1111-1111-111111111111', 7, '1', '{"walks_per_week": "1"}', 5, '2025-08-22T17:47:53.371122'),
('405da3df-f451-430f-b98d-bde84855f358', '87af5e36-1c65-40a2-9885-a86413625107', 'f1111111-1111-1111-1111-111111111111', 8, 'Dorchester', '{"address": "Dorchester"}', 20, '2025-08-22T17:47:53.371122'),
('11f5ad9a-d816-45a9-8683-8469e7da02e7', '87af5e36-1c65-40a2-9885-a86413625107', 'f1111111-1111-1111-1111-111111111111', 9, 'under_15', '{"budget": "under_15"}', 0, '2025-08-22T17:47:53.371122');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('e659b4d0-7488-433a-aab3-dd6e3957d68a', '87af5e36-1c65-40a2-9885-a86413625107', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'unqualified', '{"name": "Mike Johnson", "email": "mjohnson.work@outlook.com"}', 25, 0.25, false);


-- Lead 5: Maybe - Jennifer Walsh
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('24883b72-be79-43c5-a824-eb060be17e38', 'f1111111-1111-1111-1111-111111111111', 'sess_005_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-20T04:47:53.371171', '2025-08-20T05:30:53.371172', '2025-08-20T05:30:53.371172', 6, true, 60, 60, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.240', '{"device_type": "mobile", "completion_time": 36}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('6d20aac3-d170-4cf6-9879-7f64aad9a20b', '24883b72-be79-43c5-a824-eb060be17e38', 'facebook', 'social', 'medford_pet_owners', 'dog walking cambridge', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('d910b356-1a82-45a3-95dd-0f2e785ff09c', '24883b72-be79-43c5-a824-eb060be17e38', 'f1111111-1111-1111-1111-111111111111', 1, 'Jennifer Walsh', '{"name": "Jennifer Walsh"}', 10, '2025-08-20T04:47:53.371171'),
('a4b14662-f9e1-49aa-9bb2-0f857ff1bb7d', '24883b72-be79-43c5-a824-eb060be17e38', 'f1111111-1111-1111-1111-111111111111', 2, 'jwalsh.home@gmail.com', '{"email": "jwalsh.home@gmail.com"}', 10, '2025-08-20T04:47:53.371171'),
('03f80213-17cb-4820-9ba5-a6baeac3add4', '24883b72-be79-43c5-a824-eb060be17e38', 'f1111111-1111-1111-1111-111111111111', 4, 'Lab Mix', '{"dog_breed": "Lab Mix"}', 10, '2025-08-20T04:47:53.371171'),
('89de629b-0ce6-4513-a184-e39d32b72383', '24883b72-be79-43c5-a824-eb060be17e38', 'f1111111-1111-1111-1111-111111111111', 5, '6', '{"dog_age": "6"}', 15, '2025-08-20T04:47:53.371171'),
('a8180b53-ebb8-4cec-8611-2b1749397faa', '24883b72-be79-43c5-a824-eb060be17e38', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-20T04:47:53.371171'),
('dd4bf90f-a356-4abd-a147-6fcf985a8401', '24883b72-be79-43c5-a824-eb060be17e38', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-20T04:47:53.371171'),
('6f21a319-c60a-4b8c-9964-e5405b3ee3aa', '24883b72-be79-43c5-a824-eb060be17e38', 'f1111111-1111-1111-1111-111111111111', 8, 'Medford Square area', '{"address": "Medford Square area"}', 20, '2025-08-20T04:47:53.371171');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('cb71af79-dff7-4ac7-8efb-48824a60f804', '24883b72-be79-43c5-a824-eb060be17e38', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "Jennifer Walsh", "email": "jwalsh.home@gmail.com"}', 60, 0.60, true);


-- Lead 6: Qualified - Emily_2 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('de6d0d3f-885b-4e91-b652-985e4e2f3206', 'f1111111-1111-1111-1111-111111111111', 'sess_006_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-23T18:47:53.371214', '2025-08-23T19:09:53.371215', '2025-08-23T19:09:53.371215', 6, true, 95, 95, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.227', '{"device_type": "desktop", "completion_time": 49}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('935c13ae-1058-4edc-98f3-4c96e460b2b3', 'de6d0d3f-885b-4e91-b652-985e4e2f3206', 'google', 'cpc', 'premium_dog_walking', 'local dog walker', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('57fa5cbd-0341-42e8-b3c2-808fab9a2f87', 'de6d0d3f-885b-4e91-b652-985e4e2f3206', 'f1111111-1111-1111-1111-111111111111', 1, 'Emily_2 Rodriguez', '{"name": "Emily_2 Rodriguez"}', 10, '2025-08-23T18:47:53.371214'),
('8ef2579e-23c8-4990-b431-fc348a643cb1', 'de6d0d3f-885b-4e91-b652-985e4e2f3206', 'f1111111-1111-1111-1111-111111111111', 2, 'emily.rodriguez_2@mit.edu', '{"email": "emily.rodriguez_2@mit.edu"}', 10, '2025-08-23T18:47:53.371214'),
('93fff432-df3a-4aae-b19f-1aeef58eb286', 'de6d0d3f-885b-4e91-b652-985e4e2f3206', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0192', '{"phone": "(617) 555-0192"}', 15, '2025-08-23T18:47:53.371214'),
('71601a5f-aadb-4b20-8b83-f9ff65d47e3e', 'de6d0d3f-885b-4e91-b652-985e4e2f3206', 'f1111111-1111-1111-1111-111111111111', 4, 'German Shepherd', '{"dog_breed": "German Shepherd"}', 20, '2025-08-23T18:47:53.371214'),
('559cf116-4878-48ce-b417-19abcfcb1c6f', 'de6d0d3f-885b-4e91-b652-985e4e2f3206', 'f1111111-1111-1111-1111-111111111111', 5, '5', '{"dog_age": "5"}', 15, '2025-08-23T18:47:53.371214'),
('1e432207-f9be-454a-8292-96987ef91cdf', 'de6d0d3f-885b-4e91-b652-985e4e2f3206', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-23T18:47:53.371214'),
('5be62dc9-afe0-47cc-abe7-8a41be7815bf', 'de6d0d3f-885b-4e91-b652-985e4e2f3206', 'f1111111-1111-1111-1111-111111111111', 7, '5_plus', '{"walks_per_week": "5_plus"}', 25, '2025-08-23T18:47:53.371214'),
('eaf3705f-bcce-478f-b3f7-a073a9d70a07', 'de6d0d3f-885b-4e91-b652-985e4e2f3206', 'f1111111-1111-1111-1111-111111111111', 8, '1234 Mass Ave, Cambridge', '{"address": "1234 Mass Ave, Cambridge"}', 20, '2025-08-23T18:47:53.371214'),
('f5bd3f51-51f7-4312-b629-ab5f503f9120', 'de6d0d3f-885b-4e91-b652-985e4e2f3206', 'f1111111-1111-1111-1111-111111111111', 9, '25_35', '{"budget": "25_35"}', 25, '2025-08-23T18:47:53.371214');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('8f4e23f6-a5f2-40b0-82fb-c4805c671697', 'de6d0d3f-885b-4e91-b652-985e4e2f3206', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Emily_2 Rodriguez", "email": "emily.rodriguez_2@mit.edu", "phone": "(617) 555-0192"}', 95, 0.95, true);


-- Lead 7: Maybe - David_2 Park
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('9ccfb64b-da09-47cd-b1b5-85e5c0dc8385', 'f1111111-1111-1111-1111-111111111111', 'sess_007_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-23T20:47:53.371266', '2025-08-23T21:19:53.371267', '2025-08-23T21:19:53.371267', 6, true, 65, 65, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.197', '{"device_type": "mobile", "completion_time": 40}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('2c98b9ae-b967-4a25-a7ca-c796bf9306a0', '9ccfb64b-da09-47cd-b1b5-85e5c0dc8385', 'facebook', 'social', 'local_dog_services', 'pet walking services', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('60cda5a8-50ef-4699-a8bf-1b45101a1d67', '9ccfb64b-da09-47cd-b1b5-85e5c0dc8385', 'f1111111-1111-1111-1111-111111111111', 1, 'David_2 Park', '{"name": "David_2 Park"}', 10, '2025-08-23T20:47:53.371266'),
('cc07044f-b75d-4fca-8410-302aca78684f', '9ccfb64b-da09-47cd-b1b5-85e5c0dc8385', 'f1111111-1111-1111-1111-111111111111', 2, 'david.park_2@gmail.com', '{"email": "david.park_2@gmail.com"}', 10, '2025-08-23T20:47:53.371266'),
('37656a00-0323-4ee1-ac23-aac1f37d15f2', '9ccfb64b-da09-47cd-b1b5-85e5c0dc8385', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0283', '{"phone": "(617) 555-0283"}', 15, '2025-08-23T20:47:53.371266'),
('4354379b-aa75-41f9-a129-0a6d78837322', '9ccfb64b-da09-47cd-b1b5-85e5c0dc8385', 'f1111111-1111-1111-1111-111111111111', 4, 'Beagle', '{"dog_breed": "Beagle"}', 15, '2025-08-23T20:47:53.371266'),
('cfd8ad7f-7ad9-4184-a0b5-817f930acdea', '9ccfb64b-da09-47cd-b1b5-85e5c0dc8385', 'f1111111-1111-1111-1111-111111111111', 5, '8', '{"dog_age": "8"}', 15, '2025-08-23T20:47:53.371266'),
('b062bd17-2e75-4c81-a3ce-a8a8e9bea49d', '9ccfb64b-da09-47cd-b1b5-85e5c0dc8385', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-23T20:47:53.371266'),
('87fa265d-c7ee-4a14-a429-976ccdc60ace', '9ccfb64b-da09-47cd-b1b5-85e5c0dc8385', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-23T20:47:53.371266'),
('c9d7496b-cfae-49e2-830c-aecf2ca38984', '9ccfb64b-da09-47cd-b1b5-85e5c0dc8385', 'f1111111-1111-1111-1111-111111111111', 8, 'Somerville near Davis Square', '{"address": "Somerville near Davis Square"}', 20, '2025-08-23T20:47:53.371266');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('9ae322c4-91df-439a-97fa-8a884e46612d', '9ccfb64b-da09-47cd-b1b5-85e5c0dc8385', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "David_2 Park", "email": "david.park_2@gmail.com", "phone": "(617) 555-0283"}', 65, 0.65, true);


-- Lead 8: Qualified - Sarah_2 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('e5515bc2-d3a9-4f47-b654-ab5a77adf7ff', 'f1111111-1111-1111-1111-111111111111', 'sess_008_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-20T09:47:53.371313', '2025-08-20T10:06:53.371314', '2025-08-20T10:06:53.371314', 7, true, 88, 88, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.237', '{"device_type": "mobile", "completion_time": 52}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('61dd7126-f304-4357-9e12-e658e35763ab', 'e5515bc2-d3a9-4f47-b654-ab5a77adf7ff', 'google', 'cpc', 'harvard_students', 'pet walking services', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('aa2e0e54-1933-4bb4-9d1d-6cfe2f2b9e5a', 'e5515bc2-d3a9-4f47-b654-ab5a77adf7ff', 'f1111111-1111-1111-1111-111111111111', 1, 'Sarah_2 Kim', '{"name": "Sarah_2 Kim"}', 10, '2025-08-20T09:47:53.371313'),
('f4cb8328-2f09-4661-8051-27d8f6433943', 'e5515bc2-d3a9-4f47-b654-ab5a77adf7ff', 'f1111111-1111-1111-1111-111111111111', 2, 'sarah.kim_2@harvard.edu', '{"email": "sarah.kim_2@harvard.edu"}', 10, '2025-08-20T09:47:53.371313'),
('e943659a-18ed-4d0c-893f-7935902e0ea6', 'e5515bc2-d3a9-4f47-b654-ab5a77adf7ff', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0374', '{"phone": "(617) 555-0374"}', 15, '2025-08-20T09:47:53.371313'),
('4ba24053-82b6-4ddd-b740-c48c6888b297', 'e5515bc2-d3a9-4f47-b654-ab5a77adf7ff', 'f1111111-1111-1111-1111-111111111111', 4, 'Golden Retriever', '{"dog_breed": "Golden Retriever"}', 20, '2025-08-20T09:47:53.371313'),
('525f2b2f-5833-4795-9987-33a06517d9de', 'e5515bc2-d3a9-4f47-b654-ab5a77adf7ff', 'f1111111-1111-1111-1111-111111111111', 5, '3', '{"dog_age": "3"}', 15, '2025-08-20T09:47:53.371313'),
('e1018080-169f-4198-b496-497613e08983', 'e5515bc2-d3a9-4f47-b654-ab5a77adf7ff', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-20T09:47:53.371313'),
('b9c4015e-5e0b-4241-b6ee-bedbd5ba97be', 'e5515bc2-d3a9-4f47-b654-ab5a77adf7ff', 'f1111111-1111-1111-1111-111111111111', 7, '3_4', '{"walks_per_week": "3_4"}', 20, '2025-08-20T09:47:53.371313'),
('9c9e7537-0a62-4722-b5c7-4537841533e6', 'e5515bc2-d3a9-4f47-b654-ab5a77adf7ff', 'f1111111-1111-1111-1111-111111111111', 8, 'Harvard Square area', '{"address": "Harvard Square area"}', 20, '2025-08-20T09:47:53.371313'),
('73cf1109-cf69-4206-ab4e-ed0d8404673f', 'e5515bc2-d3a9-4f47-b654-ab5a77adf7ff', 'f1111111-1111-1111-1111-111111111111', 9, '20_30', '{"budget": "20_30"}', 20, '2025-08-20T09:47:53.371313');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('567b7383-158b-4b36-9b3d-890237f489e3', 'e5515bc2-d3a9-4f47-b654-ab5a77adf7ff', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Sarah_2 Kim", "email": "sarah.kim_2@harvard.edu", "phone": "(617) 555-0374"}', 88, 0.88, true);


-- Lead 9: Unqualified - Mike_2 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('91782a70-40a9-4e11-9f9f-183ab8b23148', 'f1111111-1111-1111-1111-111111111111', 'sess_009_unqualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-19T16:47:53.371361', '2025-08-19T17:13:53.371362', '2025-08-19T17:13:53.371362', 6, true, 25, 25, 'no', 'qualified', 'Thank you for your interest. We may not be the best fit, but please reach out if your needs change.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.164', '{"device_type": "desktop", "completion_time": 50}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('6b284283-b077-4e1e-8604-383934c2e64e', '91782a70-40a9-4e11-9f9f-183ab8b23148', 'organic', 'search', 'dog_walking_general', 'dog walker near me', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('358c6caf-89f1-4285-b622-7883899f2d71', '91782a70-40a9-4e11-9f9f-183ab8b23148', 'f1111111-1111-1111-1111-111111111111', 1, 'Mike_2 Johnson', '{"name": "Mike_2 Johnson"}', 10, '2025-08-19T16:47:53.371361'),
('aaf92507-7dff-42ce-b054-2ff39de39afa', '91782a70-40a9-4e11-9f9f-183ab8b23148', 'f1111111-1111-1111-1111-111111111111', 2, 'mjohnson.work_2@outlook.com', '{"email": "mjohnson.work_2@outlook.com"}', 10, '2025-08-19T16:47:53.371361'),
('9cf677fc-eaba-4f6b-bb7d-478f6342ba65', '91782a70-40a9-4e11-9f9f-183ab8b23148', 'f1111111-1111-1111-1111-111111111111', 4, 'Pit Bull Mix', '{"dog_breed": "Pit Bull Mix"}', 5, '2025-08-19T16:47:53.371361'),
('de11ed53-2e45-4fbb-8ccb-c41f549a70d9', '91782a70-40a9-4e11-9f9f-183ab8b23148', 'f1111111-1111-1111-1111-111111111111', 5, '2', '{"dog_age": "2"}', 15, '2025-08-19T16:47:53.371361'),
('572bf980-b7ec-44f7-a7d0-78085ded69f4', '91782a70-40a9-4e11-9f9f-183ab8b23148', 'f1111111-1111-1111-1111-111111111111', 6, 'rarely', '{"behavior": "rarely"}', -10, '2025-08-19T16:47:53.371361'),
('aa0bfbdb-7b8f-4375-9cf8-301352be1a21', '91782a70-40a9-4e11-9f9f-183ab8b23148', 'f1111111-1111-1111-1111-111111111111', 7, '1', '{"walks_per_week": "1"}', 5, '2025-08-19T16:47:53.371361'),
('e0e0447e-2f53-4d28-b22e-3a23152c62db', '91782a70-40a9-4e11-9f9f-183ab8b23148', 'f1111111-1111-1111-1111-111111111111', 8, 'Dorchester', '{"address": "Dorchester"}', 20, '2025-08-19T16:47:53.371361'),
('486d5ef4-831c-47a7-ad98-c7806045d235', '91782a70-40a9-4e11-9f9f-183ab8b23148', 'f1111111-1111-1111-1111-111111111111', 9, 'under_15', '{"budget": "under_15"}', 0, '2025-08-19T16:47:53.371361');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('16514cb4-2e73-4616-b338-96b0a13f8a49', '91782a70-40a9-4e11-9f9f-183ab8b23148', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'unqualified', '{"name": "Mike_2 Johnson", "email": "mjohnson.work_2@outlook.com"}', 25, 0.25, false);


-- Lead 10: Maybe - Jennifer_2 Walsh
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('bc8375b2-be77-4160-8a1d-5a783c4409a3', 'f1111111-1111-1111-1111-111111111111', 'sess_010_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-19T09:47:53.371405', '2025-08-19T10:26:53.371406', '2025-08-19T10:26:53.371406', 7, true, 60, 60, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.62', '{"device_type": "mobile", "completion_time": 21}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('fa6d1d72-5ffd-42e8-b5fc-4843c9b552ae', 'bc8375b2-be77-4160-8a1d-5a783c4409a3', 'facebook', 'social', 'medford_pet_owners', 'professional dog walking', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('7e876050-3ed8-48f0-99b8-369f1ea3e208', 'bc8375b2-be77-4160-8a1d-5a783c4409a3', 'f1111111-1111-1111-1111-111111111111', 1, 'Jennifer_2 Walsh', '{"name": "Jennifer_2 Walsh"}', 10, '2025-08-19T09:47:53.371405'),
('e4ec1474-3629-4765-80e0-1051cd4d81b2', 'bc8375b2-be77-4160-8a1d-5a783c4409a3', 'f1111111-1111-1111-1111-111111111111', 2, 'jwalsh.home_2@gmail.com', '{"email": "jwalsh.home_2@gmail.com"}', 10, '2025-08-19T09:47:53.371405'),
('a187bbcc-6755-427b-a7ee-542e702911c3', 'bc8375b2-be77-4160-8a1d-5a783c4409a3', 'f1111111-1111-1111-1111-111111111111', 4, 'Lab Mix', '{"dog_breed": "Lab Mix"}', 10, '2025-08-19T09:47:53.371405'),
('8869e3af-d9e9-43c2-b50e-67aa7c2e3afa', 'bc8375b2-be77-4160-8a1d-5a783c4409a3', 'f1111111-1111-1111-1111-111111111111', 5, '6', '{"dog_age": "6"}', 15, '2025-08-19T09:47:53.371405'),
('0dde65ea-b948-4f58-91e6-c4d7747df530', 'bc8375b2-be77-4160-8a1d-5a783c4409a3', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-19T09:47:53.371405'),
('10660177-773c-48ee-b0b3-738ba6ebd828', 'bc8375b2-be77-4160-8a1d-5a783c4409a3', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-19T09:47:53.371405'),
('ca5cd4b8-facc-4c45-9cd7-ac144477709b', 'bc8375b2-be77-4160-8a1d-5a783c4409a3', 'f1111111-1111-1111-1111-111111111111', 8, 'Medford Square area', '{"address": "Medford Square area"}', 20, '2025-08-19T09:47:53.371405');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('1a9aaa21-9228-49df-bf60-db84851ff35e', 'bc8375b2-be77-4160-8a1d-5a783c4409a3', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "Jennifer_2 Walsh", "email": "jwalsh.home_2@gmail.com"}', 60, 0.60, true);


-- Lead 11: Qualified - Emily_3 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('5b9a0ffd-875c-4160-b7ea-56f3ee42769a', 'f1111111-1111-1111-1111-111111111111', 'sess_011_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-20T11:47:53.371446', '2025-08-20T12:31:53.371447', '2025-08-20T12:31:53.371447', 6, true, 95, 95, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.69', '{"device_type": "desktop", "completion_time": 29}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('d79156b1-3bb8-4004-a17d-787977e31394', '5b9a0ffd-875c-4160-b7ea-56f3ee42769a', 'google', 'cpc', 'premium_dog_walking', 'professional dog walking', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('f40359a0-53ed-482d-860e-e874d00b5d3d', '5b9a0ffd-875c-4160-b7ea-56f3ee42769a', 'f1111111-1111-1111-1111-111111111111', 1, 'Emily_3 Rodriguez', '{"name": "Emily_3 Rodriguez"}', 10, '2025-08-20T11:47:53.371446'),
('418594d7-d61f-4c2f-b6dd-01da9b84fa94', '5b9a0ffd-875c-4160-b7ea-56f3ee42769a', 'f1111111-1111-1111-1111-111111111111', 2, 'emily.rodriguez_3@mit.edu', '{"email": "emily.rodriguez_3@mit.edu"}', 10, '2025-08-20T11:47:53.371446'),
('15566429-dfee-48bb-b3f6-fbec0a5fbac0', '5b9a0ffd-875c-4160-b7ea-56f3ee42769a', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0192', '{"phone": "(617) 555-0192"}', 15, '2025-08-20T11:47:53.371446'),
('84d983b2-9283-4e93-9414-d9da71690355', '5b9a0ffd-875c-4160-b7ea-56f3ee42769a', 'f1111111-1111-1111-1111-111111111111', 4, 'German Shepherd', '{"dog_breed": "German Shepherd"}', 20, '2025-08-20T11:47:53.371446'),
('76f56752-501d-4de3-97cd-c301745772eb', '5b9a0ffd-875c-4160-b7ea-56f3ee42769a', 'f1111111-1111-1111-1111-111111111111', 5, '5', '{"dog_age": "5"}', 15, '2025-08-20T11:47:53.371446'),
('f547cec0-74a4-4376-b921-2adcbf3d82a6', '5b9a0ffd-875c-4160-b7ea-56f3ee42769a', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-20T11:47:53.371446'),
('eb8dcf11-674e-46d3-b834-512c64447244', '5b9a0ffd-875c-4160-b7ea-56f3ee42769a', 'f1111111-1111-1111-1111-111111111111', 7, '5_plus', '{"walks_per_week": "5_plus"}', 25, '2025-08-20T11:47:53.371446'),
('a01c5155-a4f8-4023-b76d-72ffc76c9fc8', '5b9a0ffd-875c-4160-b7ea-56f3ee42769a', 'f1111111-1111-1111-1111-111111111111', 8, '1234 Mass Ave, Cambridge', '{"address": "1234 Mass Ave, Cambridge"}', 20, '2025-08-20T11:47:53.371446'),
('a757c822-fe42-4efb-a611-5257158ae60b', '5b9a0ffd-875c-4160-b7ea-56f3ee42769a', 'f1111111-1111-1111-1111-111111111111', 9, '25_35', '{"budget": "25_35"}', 25, '2025-08-20T11:47:53.371446');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('839cbc7c-bd23-4fbd-8942-5933ab9780fd', '5b9a0ffd-875c-4160-b7ea-56f3ee42769a', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Emily_3 Rodriguez", "email": "emily.rodriguez_3@mit.edu", "phone": "(617) 555-0192"}', 95, 0.95, true);


-- Lead 12: Maybe - David_3 Park
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('66902cf6-c92d-44b7-bdb4-0f715c0c55a4', 'f1111111-1111-1111-1111-111111111111', 'sess_012_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-24T02:47:53.371494', '2025-08-24T03:31:53.371495', '2025-08-24T03:31:53.371495', 8, true, 65, 65, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.78', '{"device_type": "mobile", "completion_time": 47}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('c210a815-bc40-4f80-9b71-556d6190ab70', '66902cf6-c92d-44b7-bdb4-0f715c0c55a4', 'facebook', 'social', 'local_dog_services', 'dog walker near me', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('7a713158-57b4-4a54-bbed-bf7b12ef6fbf', '66902cf6-c92d-44b7-bdb4-0f715c0c55a4', 'f1111111-1111-1111-1111-111111111111', 1, 'David_3 Park', '{"name": "David_3 Park"}', 10, '2025-08-24T02:47:53.371494'),
('138000c6-5daa-4bdf-b668-b86837127f9d', '66902cf6-c92d-44b7-bdb4-0f715c0c55a4', 'f1111111-1111-1111-1111-111111111111', 2, 'david.park_3@gmail.com', '{"email": "david.park_3@gmail.com"}', 10, '2025-08-24T02:47:53.371494'),
('3de2bb6c-bb0a-4aa6-8c13-679733387b17', '66902cf6-c92d-44b7-bdb4-0f715c0c55a4', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0283', '{"phone": "(617) 555-0283"}', 15, '2025-08-24T02:47:53.371494'),
('22130665-1815-41fd-b889-c5f3b79f7d42', '66902cf6-c92d-44b7-bdb4-0f715c0c55a4', 'f1111111-1111-1111-1111-111111111111', 4, 'Beagle', '{"dog_breed": "Beagle"}', 15, '2025-08-24T02:47:53.371494'),
('6744f5c1-d29a-43d5-a569-fd76d64dcd0b', '66902cf6-c92d-44b7-bdb4-0f715c0c55a4', 'f1111111-1111-1111-1111-111111111111', 5, '8', '{"dog_age": "8"}', 15, '2025-08-24T02:47:53.371494'),
('15b5ee47-0241-4227-879f-ea4ab8d53e63', '66902cf6-c92d-44b7-bdb4-0f715c0c55a4', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-24T02:47:53.371494'),
('d700bdfc-607c-4f27-af86-92de5adf716f', '66902cf6-c92d-44b7-bdb4-0f715c0c55a4', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-24T02:47:53.371494'),
('8e1b39b8-30dc-44a5-b615-cc69ca44d354', '66902cf6-c92d-44b7-bdb4-0f715c0c55a4', 'f1111111-1111-1111-1111-111111111111', 8, 'Somerville near Davis Square', '{"address": "Somerville near Davis Square"}', 20, '2025-08-24T02:47:53.371494');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('87e948a7-52d6-44b2-8f2d-c93e5bf267d3', '66902cf6-c92d-44b7-bdb4-0f715c0c55a4', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "David_3 Park", "email": "david.park_3@gmail.com", "phone": "(617) 555-0283"}', 65, 0.65, true);


-- Lead 13: Qualified - Sarah_3 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('84f5990e-ce92-4f08-b5f4-9189735e460b', 'f1111111-1111-1111-1111-111111111111', 'sess_013_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-19T06:47:53.371538', '2025-08-19T07:06:53.371539', '2025-08-19T07:06:53.371539', 7, true, 88, 88, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.52', '{"device_type": "mobile", "completion_time": 50}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('c5f26a78-dec9-4336-b0fd-95e914b0c91b', '84f5990e-ce92-4f08-b5f4-9189735e460b', 'google', 'cpc', 'harvard_students', 'pet walking services', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('c88c79d8-314b-48e2-ac90-844dcec0e89b', '84f5990e-ce92-4f08-b5f4-9189735e460b', 'f1111111-1111-1111-1111-111111111111', 1, 'Sarah_3 Kim', '{"name": "Sarah_3 Kim"}', 10, '2025-08-19T06:47:53.371538'),
('7434541b-06d2-4fdf-a7d6-a33c31240289', '84f5990e-ce92-4f08-b5f4-9189735e460b', 'f1111111-1111-1111-1111-111111111111', 2, 'sarah.kim_3@harvard.edu', '{"email": "sarah.kim_3@harvard.edu"}', 10, '2025-08-19T06:47:53.371538'),
('994fa457-59b0-4eaf-b7ad-cf2f1bca202a', '84f5990e-ce92-4f08-b5f4-9189735e460b', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0374', '{"phone": "(617) 555-0374"}', 15, '2025-08-19T06:47:53.371538'),
('93ce769d-a9c8-4211-ba79-b3c7a852b72d', '84f5990e-ce92-4f08-b5f4-9189735e460b', 'f1111111-1111-1111-1111-111111111111', 4, 'Golden Retriever', '{"dog_breed": "Golden Retriever"}', 20, '2025-08-19T06:47:53.371538'),
('5a911871-a7c2-4abc-8644-74d0131cdd8d', '84f5990e-ce92-4f08-b5f4-9189735e460b', 'f1111111-1111-1111-1111-111111111111', 5, '3', '{"dog_age": "3"}', 15, '2025-08-19T06:47:53.371538'),
('2de36107-5ba7-4d20-8e64-f036a7e806ba', '84f5990e-ce92-4f08-b5f4-9189735e460b', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-19T06:47:53.371538'),
('c6792615-e5f1-4b1a-b388-333d6e17d8d7', '84f5990e-ce92-4f08-b5f4-9189735e460b', 'f1111111-1111-1111-1111-111111111111', 7, '3_4', '{"walks_per_week": "3_4"}', 20, '2025-08-19T06:47:53.371538'),
('d8cf1c01-1975-4683-a5db-e40938c49c09', '84f5990e-ce92-4f08-b5f4-9189735e460b', 'f1111111-1111-1111-1111-111111111111', 8, 'Harvard Square area', '{"address": "Harvard Square area"}', 20, '2025-08-19T06:47:53.371538'),
('5d47bb30-761e-42e9-97eb-2b5a08cff29e', '84f5990e-ce92-4f08-b5f4-9189735e460b', 'f1111111-1111-1111-1111-111111111111', 9, '20_30', '{"budget": "20_30"}', 20, '2025-08-19T06:47:53.371538');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('b4f2d47d-e054-4146-90a3-f4ab2edf8674', '84f5990e-ce92-4f08-b5f4-9189735e460b', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Sarah_3 Kim", "email": "sarah.kim_3@harvard.edu", "phone": "(617) 555-0374"}', 88, 0.88, true);


-- Lead 14: Unqualified - Mike_3 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('4f0fe9ca-28a2-441a-ae06-a92066be5102', 'f1111111-1111-1111-1111-111111111111', 'sess_014_unqualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-24T04:47:53.371584', '2025-08-24T05:12:53.371585', '2025-08-24T05:12:53.371585', 8, true, 25, 25, 'no', 'qualified', 'Thank you for your interest. We may not be the best fit, but please reach out if your needs change.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.54', '{"device_type": "desktop", "completion_time": 57}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('52e6df8b-aa1c-4342-8cb0-10f9536931d3', '4f0fe9ca-28a2-441a-ae06-a92066be5102', 'organic', 'search', 'dog_walking_general', 'dog walking cambridge', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('a7b03a0e-0e20-4d71-9006-f4ee4513c3aa', '4f0fe9ca-28a2-441a-ae06-a92066be5102', 'f1111111-1111-1111-1111-111111111111', 1, 'Mike_3 Johnson', '{"name": "Mike_3 Johnson"}', 10, '2025-08-24T04:47:53.371584'),
('ff0ea12e-b2bd-4607-9384-a76584951b54', '4f0fe9ca-28a2-441a-ae06-a92066be5102', 'f1111111-1111-1111-1111-111111111111', 2, 'mjohnson.work_3@outlook.com', '{"email": "mjohnson.work_3@outlook.com"}', 10, '2025-08-24T04:47:53.371584'),
('6ddacea0-8e56-4a90-a8d9-fc2e774efd4d', '4f0fe9ca-28a2-441a-ae06-a92066be5102', 'f1111111-1111-1111-1111-111111111111', 4, 'Pit Bull Mix', '{"dog_breed": "Pit Bull Mix"}', 5, '2025-08-24T04:47:53.371584'),
('3dadcf5a-4931-4fba-9bb2-a139ae9a4435', '4f0fe9ca-28a2-441a-ae06-a92066be5102', 'f1111111-1111-1111-1111-111111111111', 5, '2', '{"dog_age": "2"}', 15, '2025-08-24T04:47:53.371584'),
('3e3e8b0a-74af-4774-8dfc-a712e91946ac', '4f0fe9ca-28a2-441a-ae06-a92066be5102', 'f1111111-1111-1111-1111-111111111111', 6, 'rarely', '{"behavior": "rarely"}', -10, '2025-08-24T04:47:53.371584'),
('7a7c76d2-86cc-4706-b892-9441e14e9353', '4f0fe9ca-28a2-441a-ae06-a92066be5102', 'f1111111-1111-1111-1111-111111111111', 7, '1', '{"walks_per_week": "1"}', 5, '2025-08-24T04:47:53.371584'),
('953a28a4-092b-4f1c-82a0-de4cb831900e', '4f0fe9ca-28a2-441a-ae06-a92066be5102', 'f1111111-1111-1111-1111-111111111111', 8, 'Dorchester', '{"address": "Dorchester"}', 20, '2025-08-24T04:47:53.371584'),
('759cb751-5e44-401c-8a99-6e5e8c9ed7ce', '4f0fe9ca-28a2-441a-ae06-a92066be5102', 'f1111111-1111-1111-1111-111111111111', 9, 'under_15', '{"budget": "under_15"}', 0, '2025-08-24T04:47:53.371584');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('fb8f8aa2-620e-46bf-951d-391f3874ac5d', '4f0fe9ca-28a2-441a-ae06-a92066be5102', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'unqualified', '{"name": "Mike_3 Johnson", "email": "mjohnson.work_3@outlook.com"}', 25, 0.25, false);


-- Lead 15: Maybe - Jennifer_3 Walsh
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('bd32e99a-a998-4302-9535-932ea9fdd86a', 'f1111111-1111-1111-1111-111111111111', 'sess_015_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-22T09:47:53.371627', '2025-08-22T10:20:53.371628', '2025-08-22T10:20:53.371628', 8, true, 60, 60, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.74', '{"device_type": "mobile", "completion_time": 60}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('300073c6-ee8b-49d3-9274-8a3a5fb51349', 'bd32e99a-a998-4302-9535-932ea9fdd86a', 'facebook', 'social', 'medford_pet_owners', 'local dog walker', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('34c3adad-286d-4cb7-8d0f-27009d1e74e1', 'bd32e99a-a998-4302-9535-932ea9fdd86a', 'f1111111-1111-1111-1111-111111111111', 1, 'Jennifer_3 Walsh', '{"name": "Jennifer_3 Walsh"}', 10, '2025-08-22T09:47:53.371627'),
('772bb524-423b-4543-95c1-6ac16d575217', 'bd32e99a-a998-4302-9535-932ea9fdd86a', 'f1111111-1111-1111-1111-111111111111', 2, 'jwalsh.home_3@gmail.com', '{"email": "jwalsh.home_3@gmail.com"}', 10, '2025-08-22T09:47:53.371627'),
('50e4313f-4927-48b6-a419-3d638c03e1c9', 'bd32e99a-a998-4302-9535-932ea9fdd86a', 'f1111111-1111-1111-1111-111111111111', 4, 'Lab Mix', '{"dog_breed": "Lab Mix"}', 10, '2025-08-22T09:47:53.371627'),
('5677b660-9b4f-48e9-af68-92f93a8df316', 'bd32e99a-a998-4302-9535-932ea9fdd86a', 'f1111111-1111-1111-1111-111111111111', 5, '6', '{"dog_age": "6"}', 15, '2025-08-22T09:47:53.371627'),
('8cc241c2-b60d-462c-aca2-ce34dc9e6403', 'bd32e99a-a998-4302-9535-932ea9fdd86a', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-22T09:47:53.371627'),
('02780601-821c-4974-a4be-be9eb1b525a0', 'bd32e99a-a998-4302-9535-932ea9fdd86a', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-22T09:47:53.371627'),
('16343b9f-7a5b-41be-a3f3-c20848ebcd1a', 'bd32e99a-a998-4302-9535-932ea9fdd86a', 'f1111111-1111-1111-1111-111111111111', 8, 'Medford Square area', '{"address": "Medford Square area"}', 20, '2025-08-22T09:47:53.371627');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('fd0e7da8-c8e3-4d8f-b732-0049105b69ce', 'bd32e99a-a998-4302-9535-932ea9fdd86a', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "Jennifer_3 Walsh", "email": "jwalsh.home_3@gmail.com"}', 60, 0.60, true);


-- Lead 16: Qualified - Emily_4 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('d6e40222-44c6-4f72-9142-f9da11904a2c', 'f1111111-1111-1111-1111-111111111111', 'sess_016_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-23T20:47:53.371668', '2025-08-23T21:13:53.371669', '2025-08-23T21:13:53.371669', 9, true, 95, 95, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.238', '{"device_type": "desktop", "completion_time": 18}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('3148c5d2-58c6-4873-90e0-21f0f11d7d62', 'd6e40222-44c6-4f72-9142-f9da11904a2c', 'google', 'cpc', 'premium_dog_walking', 'local dog walker', 'desktop', 'Firefox', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('aa71f461-96c8-45fe-bfb4-77e114e5bdb7', 'd6e40222-44c6-4f72-9142-f9da11904a2c', 'f1111111-1111-1111-1111-111111111111', 1, 'Emily_4 Rodriguez', '{"name": "Emily_4 Rodriguez"}', 10, '2025-08-23T20:47:53.371668'),
('346a2867-7660-4a68-b769-1e7bad5d4314', 'd6e40222-44c6-4f72-9142-f9da11904a2c', 'f1111111-1111-1111-1111-111111111111', 2, 'emily.rodriguez_4@mit.edu', '{"email": "emily.rodriguez_4@mit.edu"}', 10, '2025-08-23T20:47:53.371668'),
('f8c350f2-810b-4d7c-ae6b-51097c3f3016', 'd6e40222-44c6-4f72-9142-f9da11904a2c', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0192', '{"phone": "(617) 555-0192"}', 15, '2025-08-23T20:47:53.371668'),
('eaecbc73-70e5-4c14-9fd5-cb5eb39ad26b', 'd6e40222-44c6-4f72-9142-f9da11904a2c', 'f1111111-1111-1111-1111-111111111111', 4, 'German Shepherd', '{"dog_breed": "German Shepherd"}', 20, '2025-08-23T20:47:53.371668'),
('d04205dc-8d97-409c-9d32-af6743980b9a', 'd6e40222-44c6-4f72-9142-f9da11904a2c', 'f1111111-1111-1111-1111-111111111111', 5, '5', '{"dog_age": "5"}', 15, '2025-08-23T20:47:53.371668'),
('36943594-dca7-47f6-afcf-1d8290f99453', 'd6e40222-44c6-4f72-9142-f9da11904a2c', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-23T20:47:53.371668'),
('31c26545-231f-4864-b113-0b3916c12208', 'd6e40222-44c6-4f72-9142-f9da11904a2c', 'f1111111-1111-1111-1111-111111111111', 7, '5_plus', '{"walks_per_week": "5_plus"}', 25, '2025-08-23T20:47:53.371668'),
('40f7b54c-496e-4e86-8d2c-61a578060c3e', 'd6e40222-44c6-4f72-9142-f9da11904a2c', 'f1111111-1111-1111-1111-111111111111', 8, '1234 Mass Ave, Cambridge', '{"address": "1234 Mass Ave, Cambridge"}', 20, '2025-08-23T20:47:53.371668'),
('4843857a-f6e7-4913-8fa6-f18b77d89e99', 'd6e40222-44c6-4f72-9142-f9da11904a2c', 'f1111111-1111-1111-1111-111111111111', 9, '25_35', '{"budget": "25_35"}', 25, '2025-08-23T20:47:53.371668');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('fb9bdb27-b2e4-44ef-89e5-a69bc18a2647', 'd6e40222-44c6-4f72-9142-f9da11904a2c', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Emily_4 Rodriguez", "email": "emily.rodriguez_4@mit.edu", "phone": "(617) 555-0192"}', 95, 0.95, true);


-- Lead 17: Maybe - David_4 Park
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('5662656d-12f7-496c-949b-f09c082c82e7', 'f1111111-1111-1111-1111-111111111111', 'sess_017_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-19T07:47:53.371716', '2025-08-19T08:22:53.371717', '2025-08-19T08:22:53.371717', 8, true, 65, 65, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.160', '{"device_type": "mobile", "completion_time": 59}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('6f815329-6fbb-4336-ba01-cabc6806c801', '5662656d-12f7-496c-949b-f09c082c82e7', 'facebook', 'social', 'local_dog_services', 'dog walking cambridge', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Medford');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('5483d7e1-b1eb-48d2-8a27-bc2e97a5098c', '5662656d-12f7-496c-949b-f09c082c82e7', 'f1111111-1111-1111-1111-111111111111', 1, 'David_4 Park', '{"name": "David_4 Park"}', 10, '2025-08-19T07:47:53.371716'),
('fd4ba02d-ae00-44ef-a534-8f5d721565da', '5662656d-12f7-496c-949b-f09c082c82e7', 'f1111111-1111-1111-1111-111111111111', 2, 'david.park_4@gmail.com', '{"email": "david.park_4@gmail.com"}', 10, '2025-08-19T07:47:53.371716'),
('cdc26611-558b-4b76-b95a-4ad533ef28b4', '5662656d-12f7-496c-949b-f09c082c82e7', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0283', '{"phone": "(617) 555-0283"}', 15, '2025-08-19T07:47:53.371716'),
('f54d2c8c-4578-486e-92bb-1b4b6bff2472', '5662656d-12f7-496c-949b-f09c082c82e7', 'f1111111-1111-1111-1111-111111111111', 4, 'Beagle', '{"dog_breed": "Beagle"}', 15, '2025-08-19T07:47:53.371716'),
('de0aa442-fe1e-4401-b93a-42e4c8e0e9ab', '5662656d-12f7-496c-949b-f09c082c82e7', 'f1111111-1111-1111-1111-111111111111', 5, '8', '{"dog_age": "8"}', 15, '2025-08-19T07:47:53.371716'),
('29701f18-c130-4122-9337-a47ae2c8f002', '5662656d-12f7-496c-949b-f09c082c82e7', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-19T07:47:53.371716'),
('c90d81eb-8b2e-4d3e-b03b-426adf4c444a', '5662656d-12f7-496c-949b-f09c082c82e7', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-19T07:47:53.371716'),
('1e548c0a-a218-4ea2-9a2a-b15a217e10cb', '5662656d-12f7-496c-949b-f09c082c82e7', 'f1111111-1111-1111-1111-111111111111', 8, 'Somerville near Davis Square', '{"address": "Somerville near Davis Square"}', 20, '2025-08-19T07:47:53.371716');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('204798ec-f122-406f-8801-5cd633f79396', '5662656d-12f7-496c-949b-f09c082c82e7', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "David_4 Park", "email": "david.park_4@gmail.com", "phone": "(617) 555-0283"}', 65, 0.65, true);


-- Lead 18: Qualified - Sarah_4 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('5010aed0-39cf-4d4c-acc6-216f14fa92fe', 'f1111111-1111-1111-1111-111111111111', 'sess_018_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-19T06:47:53.371760', '2025-08-19T07:07:53.371761', '2025-08-19T07:07:53.371761', 7, true, 88, 88, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.223', '{"device_type": "mobile", "completion_time": 46}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('3e94724a-3056-4b9e-8182-efac9126a432', '5010aed0-39cf-4d4c-acc6-216f14fa92fe', 'google', 'cpc', 'harvard_students', 'dog walking cambridge', 'mobile', 'Firefox', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('e661f733-5d99-4391-be32-b4d8f08b210d', '5010aed0-39cf-4d4c-acc6-216f14fa92fe', 'f1111111-1111-1111-1111-111111111111', 1, 'Sarah_4 Kim', '{"name": "Sarah_4 Kim"}', 10, '2025-08-19T06:47:53.371760'),
('d86cdb68-9cdd-49ec-b1e3-8eb19256467a', '5010aed0-39cf-4d4c-acc6-216f14fa92fe', 'f1111111-1111-1111-1111-111111111111', 2, 'sarah.kim_4@harvard.edu', '{"email": "sarah.kim_4@harvard.edu"}', 10, '2025-08-19T06:47:53.371760'),
('6d1b3cc8-eb95-44e8-b7f4-631c4d5a5534', '5010aed0-39cf-4d4c-acc6-216f14fa92fe', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0374', '{"phone": "(617) 555-0374"}', 15, '2025-08-19T06:47:53.371760'),
('7958d137-4ad4-44f9-9cc8-f97b858302b7', '5010aed0-39cf-4d4c-acc6-216f14fa92fe', 'f1111111-1111-1111-1111-111111111111', 4, 'Golden Retriever', '{"dog_breed": "Golden Retriever"}', 20, '2025-08-19T06:47:53.371760'),
('dabe751d-e0d4-407a-b0f1-ab5f7185ccad', '5010aed0-39cf-4d4c-acc6-216f14fa92fe', 'f1111111-1111-1111-1111-111111111111', 5, '3', '{"dog_age": "3"}', 15, '2025-08-19T06:47:53.371760'),
('6dc99054-dbfd-4446-a6ca-79b930ea8dcc', '5010aed0-39cf-4d4c-acc6-216f14fa92fe', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-19T06:47:53.371760'),
('07d722c3-1115-4afb-863e-583676294004', '5010aed0-39cf-4d4c-acc6-216f14fa92fe', 'f1111111-1111-1111-1111-111111111111', 7, '3_4', '{"walks_per_week": "3_4"}', 20, '2025-08-19T06:47:53.371760'),
('586c3d8c-cc9a-4da6-a1d9-ac27f20882e7', '5010aed0-39cf-4d4c-acc6-216f14fa92fe', 'f1111111-1111-1111-1111-111111111111', 8, 'Harvard Square area', '{"address": "Harvard Square area"}', 20, '2025-08-19T06:47:53.371760'),
('653dbe84-707a-4df0-92b3-d06d0ae44789', '5010aed0-39cf-4d4c-acc6-216f14fa92fe', 'f1111111-1111-1111-1111-111111111111', 9, '20_30', '{"budget": "20_30"}', 20, '2025-08-19T06:47:53.371760');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('207a8f88-d676-4f3d-8b9c-1a0f425b2a24', '5010aed0-39cf-4d4c-acc6-216f14fa92fe', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Sarah_4 Kim", "email": "sarah.kim_4@harvard.edu", "phone": "(617) 555-0374"}', 88, 0.88, true);


-- Lead 19: Unqualified - Mike_4 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('ff794209-eef1-406e-a31b-9f49b78edccd', 'f1111111-1111-1111-1111-111111111111', 'sess_019_unqualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-21T23:47:53.371810', '2025-08-22T00:20:53.371811', '2025-08-22T00:20:53.371811', 8, true, 25, 25, 'no', 'qualified', 'Thank you for your interest. We may not be the best fit, but please reach out if your needs change.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.198', '{"device_type": "desktop", "completion_time": 22}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('37d5f8f4-60d9-4fb2-bd03-68e5cbf82271', 'ff794209-eef1-406e-a31b-9f49b78edccd', 'organic', 'search', 'dog_walking_general', 'local dog walker', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Brookline');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('f0259b93-1212-45d1-9b27-1cf06afdecbe', 'ff794209-eef1-406e-a31b-9f49b78edccd', 'f1111111-1111-1111-1111-111111111111', 1, 'Mike_4 Johnson', '{"name": "Mike_4 Johnson"}', 10, '2025-08-21T23:47:53.371810'),
('8571c71a-cc03-445c-946e-4643e199bd9b', 'ff794209-eef1-406e-a31b-9f49b78edccd', 'f1111111-1111-1111-1111-111111111111', 2, 'mjohnson.work_4@outlook.com', '{"email": "mjohnson.work_4@outlook.com"}', 10, '2025-08-21T23:47:53.371810'),
('14df21a2-0f83-42e1-a862-1febc9ee7970', 'ff794209-eef1-406e-a31b-9f49b78edccd', 'f1111111-1111-1111-1111-111111111111', 4, 'Pit Bull Mix', '{"dog_breed": "Pit Bull Mix"}', 5, '2025-08-21T23:47:53.371810'),
('a1c6804e-476d-4191-8b88-5824fb6ba9f7', 'ff794209-eef1-406e-a31b-9f49b78edccd', 'f1111111-1111-1111-1111-111111111111', 5, '2', '{"dog_age": "2"}', 15, '2025-08-21T23:47:53.371810'),
('b34dad88-4017-40d3-8512-c7f3c4951c51', 'ff794209-eef1-406e-a31b-9f49b78edccd', 'f1111111-1111-1111-1111-111111111111', 6, 'rarely', '{"behavior": "rarely"}', -10, '2025-08-21T23:47:53.371810'),
('2d847d76-1467-420b-8d7f-b96d3ceaf149', 'ff794209-eef1-406e-a31b-9f49b78edccd', 'f1111111-1111-1111-1111-111111111111', 7, '1', '{"walks_per_week": "1"}', 5, '2025-08-21T23:47:53.371810'),
('e7159c93-1920-429e-ae42-485ada9a41dc', 'ff794209-eef1-406e-a31b-9f49b78edccd', 'f1111111-1111-1111-1111-111111111111', 8, 'Dorchester', '{"address": "Dorchester"}', 20, '2025-08-21T23:47:53.371810'),
('39544d2c-b08b-4c12-8042-2e029c74ead9', 'ff794209-eef1-406e-a31b-9f49b78edccd', 'f1111111-1111-1111-1111-111111111111', 9, 'under_15', '{"budget": "under_15"}', 0, '2025-08-21T23:47:53.371810');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('17c2c185-6ba0-4511-a9a0-26171635cf6f', 'ff794209-eef1-406e-a31b-9f49b78edccd', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'unqualified', '{"name": "Mike_4 Johnson", "email": "mjohnson.work_4@outlook.com"}', 25, 0.25, false);


-- Lead 20: Maybe - Jennifer_4 Walsh
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('9da75cf8-dc3d-47b5-b223-1d901403e331', 'f1111111-1111-1111-1111-111111111111', 'sess_020_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-22T01:47:53.371854', '2025-08-22T02:07:53.371855', '2025-08-22T02:07:53.371855', 8, true, 60, 60, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0', '192.168.1.116', '{"device_type": "mobile", "completion_time": 29}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('c02b71e4-a9c8-4680-85f4-fc5c4717a938', '9da75cf8-dc3d-47b5-b223-1d901403e331', 'facebook', 'social', 'medford_pet_owners', 'pet walking services', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('9afa5267-4334-428a-b9ee-a30147d160be', '9da75cf8-dc3d-47b5-b223-1d901403e331', 'f1111111-1111-1111-1111-111111111111', 1, 'Jennifer_4 Walsh', '{"name": "Jennifer_4 Walsh"}', 10, '2025-08-22T01:47:53.371854'),
('ff957ca2-fdeb-49eb-bc31-3eb0101010b3', '9da75cf8-dc3d-47b5-b223-1d901403e331', 'f1111111-1111-1111-1111-111111111111', 2, 'jwalsh.home_4@gmail.com', '{"email": "jwalsh.home_4@gmail.com"}', 10, '2025-08-22T01:47:53.371854'),
('120a707c-b058-4140-9479-ce17c2102677', '9da75cf8-dc3d-47b5-b223-1d901403e331', 'f1111111-1111-1111-1111-111111111111', 4, 'Lab Mix', '{"dog_breed": "Lab Mix"}', 10, '2025-08-22T01:47:53.371854'),
('8bb644a5-0271-474e-9272-ee7309118964', '9da75cf8-dc3d-47b5-b223-1d901403e331', 'f1111111-1111-1111-1111-111111111111', 5, '6', '{"dog_age": "6"}', 15, '2025-08-22T01:47:53.371854'),
('f49efd2b-570b-4a38-88d1-0abc2337a576', '9da75cf8-dc3d-47b5-b223-1d901403e331', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-22T01:47:53.371854'),
('21c3eecc-2cf2-4868-af3d-639fceacedeb', '9da75cf8-dc3d-47b5-b223-1d901403e331', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-22T01:47:53.371854'),
('a76c6166-f84d-4099-a3a1-f0f8752f852f', '9da75cf8-dc3d-47b5-b223-1d901403e331', 'f1111111-1111-1111-1111-111111111111', 8, 'Medford Square area', '{"address": "Medford Square area"}', 20, '2025-08-22T01:47:53.371854');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('58df51d1-1b23-4017-8a9d-5234876718ed', '9da75cf8-dc3d-47b5-b223-1d901403e331', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "Jennifer_4 Walsh", "email": "jwalsh.home_4@gmail.com"}', 60, 0.60, true);


-- Lead 21: Qualified - Emily_5 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('ae9fefdf-4479-43bd-8610-ff4d048c5d83', 'f1111111-1111-1111-1111-111111111111', 'sess_021_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-17T05:47:53.371895', '2025-08-17T06:25:53.371896', '2025-08-17T06:25:53.371896', 7, true, 95, 95, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', '192.168.1.228', '{"device_type": "desktop", "completion_time": 38}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('fd206482-c199-465d-aa09-7616484fbdd9', 'ae9fefdf-4479-43bd-8610-ff4d048c5d83', 'google', 'cpc', 'premium_dog_walking', 'pet walking services', 'desktop', 'Edge', 'United States', 'Massachusetts', 'Arlington');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('e363f7a0-4b1f-4195-ab4e-50c30e42bfd4', 'ae9fefdf-4479-43bd-8610-ff4d048c5d83', 'f1111111-1111-1111-1111-111111111111', 1, 'Emily_5 Rodriguez', '{"name": "Emily_5 Rodriguez"}', 10, '2025-08-17T05:47:53.371895'),
('bbab2be0-c72a-4abf-ac80-a0db916a7e1d', 'ae9fefdf-4479-43bd-8610-ff4d048c5d83', 'f1111111-1111-1111-1111-111111111111', 2, 'emily.rodriguez_5@mit.edu', '{"email": "emily.rodriguez_5@mit.edu"}', 10, '2025-08-17T05:47:53.371895'),
('3397d8d4-f785-4a34-8c8f-39ff5cf59e49', 'ae9fefdf-4479-43bd-8610-ff4d048c5d83', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0192', '{"phone": "(617) 555-0192"}', 15, '2025-08-17T05:47:53.371895'),
('816e8b60-da0b-479a-b17b-0b9175299eab', 'ae9fefdf-4479-43bd-8610-ff4d048c5d83', 'f1111111-1111-1111-1111-111111111111', 4, 'German Shepherd', '{"dog_breed": "German Shepherd"}', 20, '2025-08-17T05:47:53.371895'),
('65abefb9-7415-4b85-a9dc-ab01df1284c7', 'ae9fefdf-4479-43bd-8610-ff4d048c5d83', 'f1111111-1111-1111-1111-111111111111', 5, '5', '{"dog_age": "5"}', 15, '2025-08-17T05:47:53.371895'),
('be346f3c-7833-4ee6-8e3d-9d5b30fe7797', 'ae9fefdf-4479-43bd-8610-ff4d048c5d83', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-17T05:47:53.371895'),
('42458d2c-fbb3-4f74-b661-fb8e10b2f842', 'ae9fefdf-4479-43bd-8610-ff4d048c5d83', 'f1111111-1111-1111-1111-111111111111', 7, '5_plus', '{"walks_per_week": "5_plus"}', 25, '2025-08-17T05:47:53.371895'),
('e7d26da4-6fc5-4d59-98e0-101cad0378ee', 'ae9fefdf-4479-43bd-8610-ff4d048c5d83', 'f1111111-1111-1111-1111-111111111111', 8, '1234 Mass Ave, Cambridge', '{"address": "1234 Mass Ave, Cambridge"}', 20, '2025-08-17T05:47:53.371895'),
('3b5946df-6018-4e17-8c62-9ce85b3ba6aa', 'ae9fefdf-4479-43bd-8610-ff4d048c5d83', 'f1111111-1111-1111-1111-111111111111', 9, '25_35', '{"budget": "25_35"}', 25, '2025-08-17T05:47:53.371895');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('8487342b-b5fb-410f-b1ca-6446120b4eea', 'ae9fefdf-4479-43bd-8610-ff4d048c5d83', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Emily_5 Rodriguez", "email": "emily.rodriguez_5@mit.edu", "phone": "(617) 555-0192"}', 95, 0.95, true);


-- Lead 22: Maybe - David_5 Park
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('750549bb-9528-4f67-8909-59d948359a43', 'f1111111-1111-1111-1111-111111111111', 'sess_022_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-18T03:47:53.371942', '2025-08-18T04:08:53.371942', '2025-08-18T04:08:53.371942', 6, true, 65, 65, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.168', '{"device_type": "mobile", "completion_time": 19}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('496acb31-397f-4c61-8b6f-4693b774a4bc', '750549bb-9528-4f67-8909-59d948359a43', 'facebook', 'social', 'local_dog_services', 'dog walking cambridge', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('547c375b-9833-477d-b4b4-1f0a04ce3d0a', '750549bb-9528-4f67-8909-59d948359a43', 'f1111111-1111-1111-1111-111111111111', 1, 'David_5 Park', '{"name": "David_5 Park"}', 10, '2025-08-18T03:47:53.371942'),
('1b251c1b-7912-4975-a32b-63f41fe23b69', '750549bb-9528-4f67-8909-59d948359a43', 'f1111111-1111-1111-1111-111111111111', 2, 'david.park_5@gmail.com', '{"email": "david.park_5@gmail.com"}', 10, '2025-08-18T03:47:53.371942'),
('015794ce-88eb-43d4-ac3b-e7167c98f1c3', '750549bb-9528-4f67-8909-59d948359a43', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0283', '{"phone": "(617) 555-0283"}', 15, '2025-08-18T03:47:53.371942'),
('eac57b22-0cec-48fa-8baa-cc9272f5200a', '750549bb-9528-4f67-8909-59d948359a43', 'f1111111-1111-1111-1111-111111111111', 4, 'Beagle', '{"dog_breed": "Beagle"}', 15, '2025-08-18T03:47:53.371942'),
('0f01977a-28b3-411e-a41f-031605ba1213', '750549bb-9528-4f67-8909-59d948359a43', 'f1111111-1111-1111-1111-111111111111', 5, '8', '{"dog_age": "8"}', 15, '2025-08-18T03:47:53.371942'),
('d58beb72-639f-4957-861c-00897d0cd88f', '750549bb-9528-4f67-8909-59d948359a43', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-18T03:47:53.371942'),
('935a16d7-01ed-48c4-a213-34f72c3a458a', '750549bb-9528-4f67-8909-59d948359a43', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-18T03:47:53.371942'),
('70948f48-8c70-4a1f-99f0-9b18a9b4d994', '750549bb-9528-4f67-8909-59d948359a43', 'f1111111-1111-1111-1111-111111111111', 8, 'Somerville near Davis Square', '{"address": "Somerville near Davis Square"}', 20, '2025-08-18T03:47:53.371942');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('77262767-6b45-4e1d-b917-fb0eb1e17344', '750549bb-9528-4f67-8909-59d948359a43', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "David_5 Park", "email": "david.park_5@gmail.com", "phone": "(617) 555-0283"}', 65, 0.65, true);


-- Lead 23: Qualified - Sarah_5 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('8d9d37c9-975a-4743-a6cd-3e9f348970ce', 'f1111111-1111-1111-1111-111111111111', 'sess_023_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-21T04:47:53.371989', '2025-08-21T05:28:53.371990', '2025-08-21T05:28:53.371990', 9, true, 88, 88, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.23', '{"device_type": "mobile", "completion_time": 27}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('bf314cbe-3a4e-4ba6-b1d9-1497fcd133ca', '8d9d37c9-975a-4743-a6cd-3e9f348970ce', 'google', 'cpc', 'harvard_students', 'professional dog walking', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('7c3da47f-9ef9-41c4-bb5c-97c2504f2cb9', '8d9d37c9-975a-4743-a6cd-3e9f348970ce', 'f1111111-1111-1111-1111-111111111111', 1, 'Sarah_5 Kim', '{"name": "Sarah_5 Kim"}', 10, '2025-08-21T04:47:53.371989'),
('3c8273e5-dee6-4fc7-afed-6d58eed44f36', '8d9d37c9-975a-4743-a6cd-3e9f348970ce', 'f1111111-1111-1111-1111-111111111111', 2, 'sarah.kim_5@harvard.edu', '{"email": "sarah.kim_5@harvard.edu"}', 10, '2025-08-21T04:47:53.371989'),
('cf82185d-d968-4d8b-8895-6e0ab560afc4', '8d9d37c9-975a-4743-a6cd-3e9f348970ce', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0374', '{"phone": "(617) 555-0374"}', 15, '2025-08-21T04:47:53.371989'),
('afb23f04-de1d-49ae-ae2e-e2e837f7e396', '8d9d37c9-975a-4743-a6cd-3e9f348970ce', 'f1111111-1111-1111-1111-111111111111', 4, 'Golden Retriever', '{"dog_breed": "Golden Retriever"}', 20, '2025-08-21T04:47:53.371989'),
('17e02891-d95d-4e0e-b191-bd12eab3acd6', '8d9d37c9-975a-4743-a6cd-3e9f348970ce', 'f1111111-1111-1111-1111-111111111111', 5, '3', '{"dog_age": "3"}', 15, '2025-08-21T04:47:53.371989'),
('5b3e5349-f7a5-4030-a785-217cc5691662', '8d9d37c9-975a-4743-a6cd-3e9f348970ce', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-21T04:47:53.371989'),
('9a62ffd8-10ad-4702-be68-0c4139ac1e90', '8d9d37c9-975a-4743-a6cd-3e9f348970ce', 'f1111111-1111-1111-1111-111111111111', 7, '3_4', '{"walks_per_week": "3_4"}', 20, '2025-08-21T04:47:53.371989'),
('53a72597-aedb-4517-a086-081c2322de1c', '8d9d37c9-975a-4743-a6cd-3e9f348970ce', 'f1111111-1111-1111-1111-111111111111', 8, 'Harvard Square area', '{"address": "Harvard Square area"}', 20, '2025-08-21T04:47:53.371989'),
('21b4374e-dc65-4988-bfb2-6f1b8d38fe21', '8d9d37c9-975a-4743-a6cd-3e9f348970ce', 'f1111111-1111-1111-1111-111111111111', 9, '20_30', '{"budget": "20_30"}', 20, '2025-08-21T04:47:53.371989');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('c37ccd01-65b2-45ad-bc6b-64b6cfe4e27e', '8d9d37c9-975a-4743-a6cd-3e9f348970ce', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Sarah_5 Kim", "email": "sarah.kim_5@harvard.edu", "phone": "(617) 555-0374"}', 88, 0.88, true);


-- Lead 24: Unqualified - Mike_5 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('bb389bc8-7167-4b4b-9ec6-cbd2573bc16e', 'f1111111-1111-1111-1111-111111111111', 'sess_024_unqualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-21T13:47:53.372038', '2025-08-21T14:32:53.372039', '2025-08-21T14:32:53.372039', 6, true, 25, 25, 'no', 'qualified', 'Thank you for your interest. We may not be the best fit, but please reach out if your needs change.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.213', '{"device_type": "desktop", "completion_time": 35}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('fe8dfbc3-d2cf-4b97-849a-7dfb398dce6d', 'bb389bc8-7167-4b4b-9ec6-cbd2573bc16e', 'organic', 'search', 'dog_walking_general', 'dog walking cambridge', 'desktop', 'Safari', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('0f595f9b-df0f-4920-882e-3b5e2789a844', 'bb389bc8-7167-4b4b-9ec6-cbd2573bc16e', 'f1111111-1111-1111-1111-111111111111', 1, 'Mike_5 Johnson', '{"name": "Mike_5 Johnson"}', 10, '2025-08-21T13:47:53.372038'),
('bf0d5431-e0f9-4831-8ae0-8d6fece0f31e', 'bb389bc8-7167-4b4b-9ec6-cbd2573bc16e', 'f1111111-1111-1111-1111-111111111111', 2, 'mjohnson.work_5@outlook.com', '{"email": "mjohnson.work_5@outlook.com"}', 10, '2025-08-21T13:47:53.372038'),
('b8c83bd8-e95d-4d1f-8226-48a8a636ceec', 'bb389bc8-7167-4b4b-9ec6-cbd2573bc16e', 'f1111111-1111-1111-1111-111111111111', 4, 'Pit Bull Mix', '{"dog_breed": "Pit Bull Mix"}', 5, '2025-08-21T13:47:53.372038'),
('cfc3a00f-0b2e-40e4-be8a-1ff0b33c416c', 'bb389bc8-7167-4b4b-9ec6-cbd2573bc16e', 'f1111111-1111-1111-1111-111111111111', 5, '2', '{"dog_age": "2"}', 15, '2025-08-21T13:47:53.372038'),
('ede4f8ee-3e81-44b9-8c9c-5e8bd5b9df1a', 'bb389bc8-7167-4b4b-9ec6-cbd2573bc16e', 'f1111111-1111-1111-1111-111111111111', 6, 'rarely', '{"behavior": "rarely"}', -10, '2025-08-21T13:47:53.372038'),
('f429fd0e-bb61-410d-b835-92bfe13462ab', 'bb389bc8-7167-4b4b-9ec6-cbd2573bc16e', 'f1111111-1111-1111-1111-111111111111', 7, '1', '{"walks_per_week": "1"}', 5, '2025-08-21T13:47:53.372038'),
('d684b3cd-9dd3-48ca-ba1b-22b90744981f', 'bb389bc8-7167-4b4b-9ec6-cbd2573bc16e', 'f1111111-1111-1111-1111-111111111111', 8, 'Dorchester', '{"address": "Dorchester"}', 20, '2025-08-21T13:47:53.372038'),
('a93e206c-6073-410a-9dad-22755410b735', 'bb389bc8-7167-4b4b-9ec6-cbd2573bc16e', 'f1111111-1111-1111-1111-111111111111', 9, 'under_15', '{"budget": "under_15"}', 0, '2025-08-21T13:47:53.372038');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('8dae39c3-9cc5-47c1-a454-a8b80a157d19', 'bb389bc8-7167-4b4b-9ec6-cbd2573bc16e', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'unqualified', '{"name": "Mike_5 Johnson", "email": "mjohnson.work_5@outlook.com"}', 25, 0.25, false);


-- Lead 25: Maybe - Jennifer_5 Walsh
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('b5c05317-5c39-4ff3-9efc-bb4d7a4474d8', 'f1111111-1111-1111-1111-111111111111', 'sess_025_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-24T11:47:53.372080', '2025-08-24T12:03:53.372081', '2025-08-24T12:03:53.372081', 9, true, 60, 60, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.159', '{"device_type": "mobile", "completion_time": 20}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('012789c8-5dda-45ac-930b-856e3c25697b', 'b5c05317-5c39-4ff3-9efc-bb4d7a4474d8', 'facebook', 'social', 'medford_pet_owners', 'local dog walker', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('0e4ae7e9-2218-45b5-bfc1-2276bc29babe', 'b5c05317-5c39-4ff3-9efc-bb4d7a4474d8', 'f1111111-1111-1111-1111-111111111111', 1, 'Jennifer_5 Walsh', '{"name": "Jennifer_5 Walsh"}', 10, '2025-08-24T11:47:53.372080'),
('763a3fec-1534-4147-96ba-48c995b74049', 'b5c05317-5c39-4ff3-9efc-bb4d7a4474d8', 'f1111111-1111-1111-1111-111111111111', 2, 'jwalsh.home_5@gmail.com', '{"email": "jwalsh.home_5@gmail.com"}', 10, '2025-08-24T11:47:53.372080'),
('e1f9e734-f2d5-47d6-a016-9dfef78f8ce9', 'b5c05317-5c39-4ff3-9efc-bb4d7a4474d8', 'f1111111-1111-1111-1111-111111111111', 4, 'Lab Mix', '{"dog_breed": "Lab Mix"}', 10, '2025-08-24T11:47:53.372080'),
('20d01c43-5b1c-4f79-b623-15dc32438aa8', 'b5c05317-5c39-4ff3-9efc-bb4d7a4474d8', 'f1111111-1111-1111-1111-111111111111', 5, '6', '{"dog_age": "6"}', 15, '2025-08-24T11:47:53.372080'),
('174e3ba0-b194-4b5e-9f62-966b88ddf891', 'b5c05317-5c39-4ff3-9efc-bb4d7a4474d8', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-24T11:47:53.372080'),
('5ceb9e39-291c-46ca-b3b2-e96b8b3a0d38', 'b5c05317-5c39-4ff3-9efc-bb4d7a4474d8', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-24T11:47:53.372080'),
('a83b926d-7ffc-4ae3-995e-9a50b46d080b', 'b5c05317-5c39-4ff3-9efc-bb4d7a4474d8', 'f1111111-1111-1111-1111-111111111111', 8, 'Medford Square area', '{"address": "Medford Square area"}', 20, '2025-08-24T11:47:53.372080');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('946ad28f-9f50-4e28-9633-f620cb150957', 'b5c05317-5c39-4ff3-9efc-bb4d7a4474d8', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "Jennifer_5 Walsh", "email": "jwalsh.home_5@gmail.com"}', 60, 0.60, true);


-- Lead 26: Qualified - Emily_6 Rodriguez
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('eb21ee76-971a-4a0f-a97a-c2870d32e91b', 'f1111111-1111-1111-1111-111111111111', 'sess_026_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-19T09:47:53.372119', '2025-08-19T10:08:53.372120', '2025-08-19T10:08:53.372120', 8, true, 95, 95, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.121', '{"device_type": "desktop", "completion_time": 24}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('4ea1eacc-d4f6-498c-afe4-de5ca25a726a', 'eb21ee76-971a-4a0f-a97a-c2870d32e91b', 'google', 'cpc', 'premium_dog_walking', 'pet walking services', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('b7af9178-c184-4cfa-8969-e31806acb6cc', 'eb21ee76-971a-4a0f-a97a-c2870d32e91b', 'f1111111-1111-1111-1111-111111111111', 1, 'Emily_6 Rodriguez', '{"name": "Emily_6 Rodriguez"}', 10, '2025-08-19T09:47:53.372119'),
('770b42f6-027b-4cf4-a586-bf2879710f05', 'eb21ee76-971a-4a0f-a97a-c2870d32e91b', 'f1111111-1111-1111-1111-111111111111', 2, 'emily.rodriguez_6@mit.edu', '{"email": "emily.rodriguez_6@mit.edu"}', 10, '2025-08-19T09:47:53.372119'),
('a92c5607-e0b0-44a4-93bf-1baf155828b3', 'eb21ee76-971a-4a0f-a97a-c2870d32e91b', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0192', '{"phone": "(617) 555-0192"}', 15, '2025-08-19T09:47:53.372119'),
('5646563f-6c6f-4be2-84c7-2b7e4f3beaf9', 'eb21ee76-971a-4a0f-a97a-c2870d32e91b', 'f1111111-1111-1111-1111-111111111111', 4, 'German Shepherd', '{"dog_breed": "German Shepherd"}', 20, '2025-08-19T09:47:53.372119'),
('a8a8817c-c58b-4abd-8121-293527babcaf', 'eb21ee76-971a-4a0f-a97a-c2870d32e91b', 'f1111111-1111-1111-1111-111111111111', 5, '5', '{"dog_age": "5"}', 15, '2025-08-19T09:47:53.372119'),
('46f23c10-848c-4605-98d0-5f2dc0ac9c06', 'eb21ee76-971a-4a0f-a97a-c2870d32e91b', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-19T09:47:53.372119'),
('cc52dcdd-5c41-4d39-9e60-08fcca53c7e1', 'eb21ee76-971a-4a0f-a97a-c2870d32e91b', 'f1111111-1111-1111-1111-111111111111', 7, '5_plus', '{"walks_per_week": "5_plus"}', 25, '2025-08-19T09:47:53.372119'),
('d05d9501-7396-4467-a128-b98598742509', 'eb21ee76-971a-4a0f-a97a-c2870d32e91b', 'f1111111-1111-1111-1111-111111111111', 8, '1234 Mass Ave, Cambridge', '{"address": "1234 Mass Ave, Cambridge"}', 20, '2025-08-19T09:47:53.372119'),
('67647f1a-3bd0-40ea-8fcd-8dbf47e53d8f', 'eb21ee76-971a-4a0f-a97a-c2870d32e91b', 'f1111111-1111-1111-1111-111111111111', 9, '25_35', '{"budget": "25_35"}', 25, '2025-08-19T09:47:53.372119');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('d9f1fb93-e999-4244-a361-2570c842f02c', 'eb21ee76-971a-4a0f-a97a-c2870d32e91b', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Emily_6 Rodriguez", "email": "emily.rodriguez_6@mit.edu", "phone": "(617) 555-0192"}', 95, 0.95, true);


-- Lead 27: Maybe - David_6 Park
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('3174a911-7391-4ff7-a8d8-1e4d775760b8', 'f1111111-1111-1111-1111-111111111111', 'sess_027_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-23T22:47:53.372165', '2025-08-23T23:15:53.372166', '2025-08-23T23:15:53.372166', 6, true, 65, 65, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.17', '{"device_type": "mobile", "completion_time": 33}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('7613f5c5-b426-4c3a-bc96-7603abbfb86b', '3174a911-7391-4ff7-a8d8-1e4d775760b8', 'facebook', 'social', 'local_dog_services', 'pet walking services', 'mobile', 'Chrome', 'United States', 'Massachusetts', 'Somerville');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('1b5457ee-9311-4ebd-a8c9-e19223a1fc1d', '3174a911-7391-4ff7-a8d8-1e4d775760b8', 'f1111111-1111-1111-1111-111111111111', 1, 'David_6 Park', '{"name": "David_6 Park"}', 10, '2025-08-23T22:47:53.372165'),
('e511f1d8-7531-47f5-82ac-486e08f2a575', '3174a911-7391-4ff7-a8d8-1e4d775760b8', 'f1111111-1111-1111-1111-111111111111', 2, 'david.park_6@gmail.com', '{"email": "david.park_6@gmail.com"}', 10, '2025-08-23T22:47:53.372165'),
('25541f6f-31db-4d52-9b28-66f9f8c853e8', '3174a911-7391-4ff7-a8d8-1e4d775760b8', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0283', '{"phone": "(617) 555-0283"}', 15, '2025-08-23T22:47:53.372165'),
('a87adaf9-b1b2-4514-9a2e-d9383cf96b87', '3174a911-7391-4ff7-a8d8-1e4d775760b8', 'f1111111-1111-1111-1111-111111111111', 4, 'Beagle', '{"dog_breed": "Beagle"}', 15, '2025-08-23T22:47:53.372165'),
('127df1bf-91ce-4bb6-a2ff-238f4dcd19fe', '3174a911-7391-4ff7-a8d8-1e4d775760b8', 'f1111111-1111-1111-1111-111111111111', 5, '8', '{"dog_age": "8"}', 15, '2025-08-23T22:47:53.372165'),
('aae79307-e244-4990-be85-fa2cb524f153', '3174a911-7391-4ff7-a8d8-1e4d775760b8', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-23T22:47:53.372165'),
('9cca1f9f-bdce-4b13-9d37-1604826b9739', '3174a911-7391-4ff7-a8d8-1e4d775760b8', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-23T22:47:53.372165'),
('5b378df2-6d60-4833-bf0a-572f523884e0', '3174a911-7391-4ff7-a8d8-1e4d775760b8', 'f1111111-1111-1111-1111-111111111111', 8, 'Somerville near Davis Square', '{"address": "Somerville near Davis Square"}', 20, '2025-08-23T22:47:53.372165');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('43732892-f749-4ea6-b08f-8a5b9401e86a', '3174a911-7391-4ff7-a8d8-1e4d775760b8', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "David_6 Park", "email": "david.park_6@gmail.com", "phone": "(617) 555-0283"}', 65, 0.65, true);


-- Lead 28: Qualified - Sarah_6 Kim
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('f45e7588-9446-4dac-983d-536c64e53221', 'f1111111-1111-1111-1111-111111111111', 'sess_028_qualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-21T20:47:53.372210', '2025-08-21T21:12:53.372211', '2025-08-21T21:12:53.372211', 8, true, 88, 88, 'yes', 'qualified', 'Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.32', '{"device_type": "mobile", "completion_time": 30}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('d7c05061-c24a-46d6-bc6b-167b0f56aafe', 'f45e7588-9446-4dac-983d-536c64e53221', 'google', 'cpc', 'harvard_students', 'dog walking cambridge', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Brookline');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('425343b9-d32b-4a08-86ff-28bda57662ee', 'f45e7588-9446-4dac-983d-536c64e53221', 'f1111111-1111-1111-1111-111111111111', 1, 'Sarah_6 Kim', '{"name": "Sarah_6 Kim"}', 10, '2025-08-21T20:47:53.372210'),
('72973e5c-b70c-4f6d-8c79-1a1f6e448cf2', 'f45e7588-9446-4dac-983d-536c64e53221', 'f1111111-1111-1111-1111-111111111111', 2, 'sarah.kim_6@harvard.edu', '{"email": "sarah.kim_6@harvard.edu"}', 10, '2025-08-21T20:47:53.372210'),
('8de4a0a7-9aed-48b8-a12d-43f39a3a87ea', 'f45e7588-9446-4dac-983d-536c64e53221', 'f1111111-1111-1111-1111-111111111111', 3, '(617) 555-0374', '{"phone": "(617) 555-0374"}', 15, '2025-08-21T20:47:53.372210'),
('640cd7b3-2458-4a4e-8c21-8632c08013c1', 'f45e7588-9446-4dac-983d-536c64e53221', 'f1111111-1111-1111-1111-111111111111', 4, 'Golden Retriever', '{"dog_breed": "Golden Retriever"}', 20, '2025-08-21T20:47:53.372210'),
('5a179da9-5071-45df-bad2-250249473f4f', 'f45e7588-9446-4dac-983d-536c64e53221', 'f1111111-1111-1111-1111-111111111111', 5, '3', '{"dog_age": "3"}', 15, '2025-08-21T20:47:53.372210'),
('29b2e159-e74f-453f-aff2-0fb7a2d8342c', 'f45e7588-9446-4dac-983d-536c64e53221', 'f1111111-1111-1111-1111-111111111111', 6, 'very_well', '{"behavior": "very_well"}', 25, '2025-08-21T20:47:53.372210'),
('30a30cdc-b22f-451b-8781-dbc2879f27eb', 'f45e7588-9446-4dac-983d-536c64e53221', 'f1111111-1111-1111-1111-111111111111', 7, '3_4', '{"walks_per_week": "3_4"}', 20, '2025-08-21T20:47:53.372210'),
('5f249726-03e5-4996-8689-43aad46ea7de', 'f45e7588-9446-4dac-983d-536c64e53221', 'f1111111-1111-1111-1111-111111111111', 8, 'Harvard Square area', '{"address": "Harvard Square area"}', 20, '2025-08-21T20:47:53.372210'),
('bb3868a2-7f4d-45cb-8ba1-57d93327f9fe', 'f45e7588-9446-4dac-983d-536c64e53221', 'f1111111-1111-1111-1111-111111111111', 9, '20_30', '{"budget": "20_30"}', 20, '2025-08-21T20:47:53.372210');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('f9513352-4011-4ec7-abbf-7dc52db50b02', 'f45e7588-9446-4dac-983d-536c64e53221', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'qualified', '{"name": "Sarah_6 Kim", "email": "sarah.kim_6@harvard.edu", "phone": "(617) 555-0374"}', 88, 0.88, true);


-- Lead 29: Unqualified - Mike_6 Johnson
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('54480a46-a221-4476-90f6-0c320756086f', 'f1111111-1111-1111-1111-111111111111', 'sess_029_unqualified', 'a1111111-1111-1111-1111-111111111111', '2025-08-17T20:47:53.372257', '2025-08-17T21:05:53.372257', '2025-08-17T21:05:53.372257', 9, true, 25, 25, 'no', 'qualified', 'Thank you for your interest. We may not be the best fit, but please reach out if your needs change.', 'active', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '192.168.1.155', '{"device_type": "desktop", "completion_time": 18}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('c396158e-6019-493f-adfb-a246f0ed8cc3', '54480a46-a221-4476-90f6-0c320756086f', 'organic', 'search', 'dog_walking_general', 'professional dog walking', 'desktop', 'Chrome', 'United States', 'Massachusetts', 'Cambridge');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('36d5652f-f501-4e0c-8613-1013cd67c678', '54480a46-a221-4476-90f6-0c320756086f', 'f1111111-1111-1111-1111-111111111111', 1, 'Mike_6 Johnson', '{"name": "Mike_6 Johnson"}', 10, '2025-08-17T20:47:53.372257'),
('fb7bf3bc-f1e1-4161-b363-ae501680eab3', '54480a46-a221-4476-90f6-0c320756086f', 'f1111111-1111-1111-1111-111111111111', 2, 'mjohnson.work_6@outlook.com', '{"email": "mjohnson.work_6@outlook.com"}', 10, '2025-08-17T20:47:53.372257'),
('8f988b7a-2a66-4e77-bfa7-6d47599ab6de', '54480a46-a221-4476-90f6-0c320756086f', 'f1111111-1111-1111-1111-111111111111', 4, 'Pit Bull Mix', '{"dog_breed": "Pit Bull Mix"}', 5, '2025-08-17T20:47:53.372257'),
('9ad472f8-67eb-483e-bc15-04beb15ba036', '54480a46-a221-4476-90f6-0c320756086f', 'f1111111-1111-1111-1111-111111111111', 5, '2', '{"dog_age": "2"}', 15, '2025-08-17T20:47:53.372257'),
('dd873f21-dc0e-4c0e-bb7c-bc03e984ea04', '54480a46-a221-4476-90f6-0c320756086f', 'f1111111-1111-1111-1111-111111111111', 6, 'rarely', '{"behavior": "rarely"}', -10, '2025-08-17T20:47:53.372257'),
('f816cfb3-9996-4b45-8150-a3b82f051152', '54480a46-a221-4476-90f6-0c320756086f', 'f1111111-1111-1111-1111-111111111111', 7, '1', '{"walks_per_week": "1"}', 5, '2025-08-17T20:47:53.372257'),
('8b87cad6-3d27-4dc8-8edc-76c5ba8ceaf6', '54480a46-a221-4476-90f6-0c320756086f', 'f1111111-1111-1111-1111-111111111111', 8, 'Dorchester', '{"address": "Dorchester"}', 20, '2025-08-17T20:47:53.372257'),
('be281cd3-a4af-42c5-a0f9-4cd706a8d4b0', '54480a46-a221-4476-90f6-0c320756086f', 'f1111111-1111-1111-1111-111111111111', 9, 'under_15', '{"budget": "under_15"}', 0, '2025-08-17T20:47:53.372257');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('fbe234b8-2911-4203-9154-71c994002c9a', '54480a46-a221-4476-90f6-0c320756086f', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'unqualified', '{"name": "Mike_6 Johnson", "email": "mjohnson.work_6@outlook.com"}', 25, 0.25, false);


-- Lead 30: Maybe - Jennifer_6 Walsh
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('ddfcceef-9142-40e6-ac78-d399147522fc', 'f1111111-1111-1111-1111-111111111111', 'sess_030_maybe', 'a1111111-1111-1111-1111-111111111111', '2025-08-18T23:47:53.372301', '2025-08-19T00:22:53.372301', '2025-08-19T00:22:53.372301', 6, true, 60, 60, 'maybe', 'qualified', 'Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.', 'active', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15', '192.168.1.24', '{"device_type": "mobile", "completion_time": 15}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('deb4964c-a787-461c-a6a2-9e66851d6be6', 'ddfcceef-9142-40e6-ac78-d399147522fc', 'facebook', 'social', 'medford_pet_owners', 'dog walking cambridge', 'mobile', 'Safari', 'United States', 'Massachusetts', 'Boston');


INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
('6ef27ddc-6081-4dad-97bf-2d16a3d987ef', 'ddfcceef-9142-40e6-ac78-d399147522fc', 'f1111111-1111-1111-1111-111111111111', 1, 'Jennifer_6 Walsh', '{"name": "Jennifer_6 Walsh"}', 10, '2025-08-18T23:47:53.372301'),
('22d1aa80-bbef-4508-bf00-629e240c301e', 'ddfcceef-9142-40e6-ac78-d399147522fc', 'f1111111-1111-1111-1111-111111111111', 2, 'jwalsh.home_6@gmail.com', '{"email": "jwalsh.home_6@gmail.com"}', 10, '2025-08-18T23:47:53.372301'),
('47b5155d-e3d8-457b-bd85-b09a29319006', 'ddfcceef-9142-40e6-ac78-d399147522fc', 'f1111111-1111-1111-1111-111111111111', 4, 'Lab Mix', '{"dog_breed": "Lab Mix"}', 10, '2025-08-18T23:47:53.372301'),
('6a27bec2-39a0-4c28-b5bf-0f44c4ff038e', 'ddfcceef-9142-40e6-ac78-d399147522fc', 'f1111111-1111-1111-1111-111111111111', 5, '6', '{"dog_age": "6"}', 15, '2025-08-18T23:47:53.372301'),
('a3f75658-151e-4ecc-a3fe-5dc5a2a0b457', 'ddfcceef-9142-40e6-ac78-d399147522fc', 'f1111111-1111-1111-1111-111111111111', 6, 'mostly_well', '{"behavior": "mostly_well"}', 15, '2025-08-18T23:47:53.372301'),
('ad6019f3-b7d5-46ef-81ab-53aa325ba6aa', 'ddfcceef-9142-40e6-ac78-d399147522fc', 'f1111111-1111-1111-1111-111111111111', 7, '2', '{"walks_per_week": "2"}', 10, '2025-08-18T23:47:53.372301'),
('61951f18-0d9a-4124-9da9-470f354c635c', 'ddfcceef-9142-40e6-ac78-d399147522fc', 'f1111111-1111-1111-1111-111111111111', 8, 'Medford Square area', '{"address": "Medford Square area"}', 20, '2025-08-18T23:47:53.372301');


INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('04cccc9a-e9da-4928-9985-e5501ab4eb79', 'ddfcceef-9142-40e6-ac78-d399147522fc', 'a1111111-1111-1111-1111-111111111111', 'f1111111-1111-1111-1111-111111111111', 'maybe', '{"name": "Jennifer_6 Walsh", "email": "jwalsh.home_6@gmail.com"}', 60, 0.60, true);


SELECT 'Generated 30 realistic lead sessions!' as status;
