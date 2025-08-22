-- Test data for standalone LangGraph testing

-- Insert test client (Pawsome Dog Walking)
INSERT INTO clients (
    id, name, business_name, email, owner_name,
    business_type, industry, background, goals, target_audience
) VALUES (
    'c1111111-1111-1111-1111-111111111111',
    'Pawsome Dog Walking',
    'Pawsome Dog Walking LLC',
    'contact@pawsomedogwalking.com',
    'Sarah Johnson',
    'Pet Services',
    'Pet Care',
    'Premier dog walking service in Austin since 2019. We provide daily walks, pet sitting, and dog training services.',
    'Expand client base by 30% in the next quarter',
    'Busy professionals and elderly pet owners in Austin metro area'
);

-- Insert test form
INSERT INTO forms (
    id, client_id, title, description,
    lead_scoring_threshold_yes, lead_scoring_threshold_maybe,
    max_questions, min_questions_before_fail,
    completion_message_template, unqualified_message
) VALUES (
    'f1111111-1111-1111-1111-111111111111',
    'c1111111-1111-1111-1111-111111111111',
    'Dog Walking Service Inquiry',
    'Lead generation form for Pawsome Dog Walking services',
    75,
    40,
    8,
    4,
    'Thank you {name}! Based on your needs, we can definitely help. Expect a call within 24 hours.',
    'Thank you for your interest. We may not be the perfect fit, but we appreciate your time.'
);

-- Insert form questions for dog walking service
INSERT INTO form_questions (id, form_id, question_id, question_order, question_text, question_type, is_required, scoring_rubric, category) VALUES
('q1', 'f1111111-1111-1111-1111-111111111111', 1, 1, 'What is your name?', 'text', 1, '{"max_score": 0}', 'contact'),
('q2', 'f1111111-1111-1111-1111-111111111111', 2, 2, 'What is your email address?', 'email', 1, '{"max_score": 0}', 'contact'),
('q3', 'f1111111-1111-1111-1111-111111111111', 3, 3, 'What is your phone number?', 'phone', 0, '{"max_score": 5}', 'contact'),
('q4', 'f1111111-1111-1111-1111-111111111111', 4, 4, 'Where are you located? (Address or neighborhood)', 'text', 1, '{"max_score": 10, "positive_keywords": ["austin", "downtown", "south congress"]}', 'location'),
('q5', 'f1111111-1111-1111-1111-111111111111', 5, 5, 'How many dogs do you have?', 'number', 1, '{"max_score": 10, "positive_keywords": ["1", "2", "3"]}', 'service'),
('q6', 'f1111111-1111-1111-1111-111111111111', 6, 6, 'What breed(s) are your dogs?', 'text', 0, '{"max_score": 5}', 'service'),
('q7', 'f1111111-1111-1111-1111-111111111111', 7, 7, 'How often do you need dog walking services?', 'text', 1, '{"max_score": 15, "positive_keywords": ["daily", "every day", "5 days", "weekdays"]}', 'frequency'),
('q8', 'f1111111-1111-1111-1111-111111111111', 8, 8, 'When would you like to start?', 'text', 1, '{"max_score": 20, "positive_keywords": ["immediately", "asap", "this week", "tomorrow"]}', 'urgency'),
('q9', 'f1111111-1111-1111-1111-111111111111', 9, 9, 'What is your budget range per walk?', 'text', 0, '{"max_score": 15, "positive_keywords": ["$30", "$40", "$50", "flexible"]}', 'budget'),
('q10', 'f1111111-1111-1111-1111-111111111111', 10, 10, 'Any special requirements for your dogs?', 'text', 0, '{"max_score": 5}', 'special');

-- Insert test client 2 (Real Estate)
INSERT INTO clients (
    id, name, business_name, email, owner_name,
    business_type, industry, background, goals, target_audience
) VALUES (
    'c2222222-2222-2222-2222-222222222222',
    'Metro Realty Group',
    'Metro Realty Group Inc',
    'leads@metrorealtygroup.com',
    'Michael Chen',
    'Real Estate',
    'Real Estate',
    'Full-service real estate brokerage specializing in residential properties in the metro area.',
    'Generate 50 qualified buyer leads per month',
    'First-time homebuyers and investors looking for properties'
);

-- Insert form for real estate
INSERT INTO forms (
    id, client_id, title, description,
    lead_scoring_threshold_yes, lead_scoring_threshold_maybe,
    max_questions, min_questions_before_fail
) VALUES (
    'f2222222-2222-2222-2222-222222222222',
    'c2222222-2222-2222-2222-222222222222',
    'Home Buying Interest Form',
    'Qualify potential home buyers',
    80,
    50,
    10,
    4
);

-- Insert questions for real estate
INSERT INTO form_questions (id, form_id, question_id, question_order, question_text, question_type, is_required, scoring_rubric, category) VALUES
('r1', 'f2222222-2222-2222-2222-222222222222', 1, 1, 'What is your name?', 'text', 1, '{"max_score": 0}', 'contact'),
('r2', 'f2222222-2222-2222-2222-222222222222', 2, 2, 'What is your email?', 'email', 1, '{"max_score": 0}', 'contact'),
('r3', 'f2222222-2222-2222-2222-222222222222', 3, 3, 'Are you pre-approved for a mortgage?', 'text', 1, '{"max_score": 25, "positive_keywords": ["yes", "approved", "have financing"]}', 'qualification'),
('r4', 'f2222222-2222-2222-2222-222222222222', 4, 4, 'What is your budget range?', 'text', 1, '{"max_score": 20, "positive_keywords": ["500k", "600k", "700k", "800k", "million"]}', 'budget'),
('r5', 'f2222222-2222-2222-2222-222222222222', 5, 5, 'When are you looking to buy?', 'text', 1, '{"max_score": 25, "positive_keywords": ["immediately", "this month", "30 days", "asap"]}', 'timeline'),
('r6', 'f2222222-2222-2222-2222-222222222222', 6, 6, 'What areas are you interested in?', 'text', 1, '{"max_score": 10}', 'location'),
('r7', 'f2222222-2222-2222-2222-222222222222', 7, 7, 'How many bedrooms do you need?', 'text', 0, '{"max_score": 5}', 'preferences'),
('r8', 'f2222222-2222-2222-2222-222222222222', 8, 8, 'Are you working with another agent?', 'text', 1, '{"max_score": 15, "negative_keywords": ["yes", "already have", "signed with"]}', 'competition');