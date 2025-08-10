-- Migration 002: Populate Example Data for 5 Business Scenarios
-- This script populates comprehensive test data for the dynamic survey system
-- Safe to run multiple times - uses ON CONFLICT DO NOTHING
-- ==== CLEAR EXISTING TEST DATA (Optional) ====
-- Uncomment these lines if you want to reset all test data
-- DELETE FROM responses WHERE session_id IN (SELECT session_id FROM lead_sessions WHERE form_id IN (SELECT id FROM forms WHERE client_id IN (SELECT id FROM clients WHERE email LIKE '%@jkwb.mozmail.com')));
-- DELETE FROM tracking_data WHERE session_id IN (SELECT session_id FROM lead_sessions WHERE form_id IN (SELECT id FROM forms WHERE client_id IN (SELECT id FROM clients WHERE email LIKE '%@jkwb.mozmail.com')));
-- DELETE FROM lead_sessions WHERE form_id IN (SELECT id FROM forms WHERE client_id IN (SELECT id FROM clients WHERE email LIKE '%@jkwb.mozmail.com'));
-- DELETE FROM form_questions WHERE form_id IN (SELECT id FROM forms WHERE client_id IN (SELECT id FROM clients WHERE email LIKE '%@jkwb.mozmail.com'));
-- DELETE FROM forms WHERE client_id IN (SELECT id FROM clients WHERE email LIKE '%@jkwb.mozmail.com');
-- DELETE FROM clients WHERE email LIKE '%@jkwb.mozmail.com';
-- ==== INSERT CLIENTS ====
-- 1. Dog Walking Service
INSERT INTO
    clients (
        id,
        name,
        business_name,
        email,
        owner_name,
        business_type,
        industry,
        address,
        phone,
        website,
        background,
        goals,
        target_audience
    )
VALUES
    (
        'a1111111-1111-1111-1111-111111111111' :: uuid,
        'Pawsome Dog Walking Services',
        'Pawsome Dog Walking',
        'pawsome@jkwb.mozmail.com',
        'Darlene Demo',
        'dog walking service',
        'Pet Services',
        '243 School Street, Somerville, MA 02144',
        '(617) 555-WALK',
        'www.pawsomedogwalking.com',
        'I am a recent college graduate (Psychology) who loves dogs. I grew up with several family dogs and always loved playing with them and hiking, jogging, swimming. I started this service because there are many busy people near me who may not have the time to walk their dog every day. Walking a dog enriches them and keeps them happy and calm.',
        'I want to find clients that live nearby and have well-behaved dogs to be walked several times per week. If a dog gets along well with other dogs then I can walk several at once which is best for profit. I would like to learn about the client expectations and preferences through the questions.',
        'Dog owners in urban areas who need regular walking services for well-behaved, vaccinated dogs'
    ) ON CONFLICT (email) DO NOTHING;

-- 2. Real Estate Agent
INSERT INTO
    clients (
        id,
        name,
        business_name,
        email,
        owner_name,
        business_type,
        industry,
        address,
        phone,
        website,
        background,
        goals,
        target_audience
    )
VALUES
    (
        'a2222222-2222-2222-2222-222222222222' :: uuid,
        'Metro Realty Group LLC',
        'Metro Realty Group',
        'metrorealty@jkwb.mozmail.com',
        'Michael Thompson',
        'real estate agency',
        'Real Estate',
        '500 Boylston Street, Boston, MA 02116',
        '(617) 555-HOME',
        'www.metrorealtygroup.com',
        'With over 15 years of experience in the Boston metropolitan real estate market, I specialize in helping families find their dream homes and investors identify profitable opportunities. Our team has closed over $250M in transactions and maintains a 98% client satisfaction rate.',
        'I am looking for serious buyers and sellers who are ready to make a move within the next 3-6 months. Ideal clients have realistic expectations about the market, are pre-approved for financing or have sellable property, and value professional guidance through the complex real estate process.',
        'Home buyers and sellers in the Greater Boston area with realistic timelines and budgets, particularly first-time buyers and families looking to upgrade'
    ) ON CONFLICT (email) DO NOTHING;

-- 3. Software Consulting Company
INSERT INTO
    clients (
        id,
        name,
        business_name,
        email,
        owner_name,
        business_type,
        industry,
        address,
        phone,
        website,
        background,
        goals,
        target_audience
    )
VALUES
    (
        'a3333333-3333-3333-3333-333333333333' :: uuid,
        'TechSolve Consulting Inc.',
        'TechSolve Consulting',
        'techsolve@jkwb.mozmail.com',
        'Sarah Chen',
        'software consulting',
        'Technology Consulting',
        '1 Cambridge Center, Cambridge, MA 02142',
        '(617) 555-TECH',
        'www.techsolveconsulting.com',
        'We are a boutique consulting firm specializing in digital transformation for SMBs. Our team of 25 consultants has expertise in cloud migration, custom software development, and process automation. We have successfully delivered 200+ projects ranging from $20K to $2M.',
        'We seek established businesses with $1M+ annual revenue who recognize the need for digital transformation. Ideal clients have allocated budget for technology improvements, have clear pain points in their current processes, and understand that meaningful change requires investment in both technology and training.',
        'Small to medium businesses (10-500 employees) in healthcare, finance, and manufacturing sectors looking to modernize their technology infrastructure'
    ) ON CONFLICT (email) DO NOTHING;

-- 4. Personal Fitness Trainer
INSERT INTO
    clients (
        id,
        name,
        business_name,
        email,
        owner_name,
        business_type,
        industry,
        address,
        phone,
        website,
        background,
        goals,
        target_audience
    )
VALUES
    (
        'a4444444-4444-4444-4444-444444444444' :: uuid,
        'FitLife Personal Training Studio',
        'FitLife Personal Training',
        'fitlife@jkwb.mozmail.com',
        'Jason Martinez',
        'personal training',
        'Health & Fitness',
        '789 Commonwealth Ave, Boston, MA 02215',
        '(617) 555-FITT',
        'www.fitlifeboston.com',
        'As a certified personal trainer with specializations in strength training, nutrition, and corrective exercise, I have helped over 300 clients achieve their fitness goals. My studio offers one-on-one training, small group sessions, and nutritional coaching in a supportive, non-intimidating environment.',
        'I am looking for committed individuals who are ready to invest in their health and fitness. Ideal clients have specific goals (weight loss, muscle gain, athletic performance), can commit to at least 2-3 sessions per week, understand that results require consistency, and view personal training as an investment in their long-term health.',
        'Busy professionals, post-rehab clients, and individuals serious about making lasting lifestyle changes, ages 25-55'
    ) ON CONFLICT (email) DO NOTHING;

-- 5. Home Cleaning Service
INSERT INTO
    clients (
        id,
        name,
        business_name,
        email,
        owner_name,
        business_type,
        industry,
        address,
        phone,
        website,
        background,
        goals,
        target_audience
    )
VALUES
    (
        'a5555555-5555-5555-5555-555555555555' :: uuid,
        'Sparkle Clean Solutions LLC',
        'Sparkle Clean Solutions',
        'sparkleclean@jkwb.mozmail.com',
        'Maria Rodriguez',
        'home cleaning service',
        'Home Services',
        '321 Harvard Street, Brookline, MA 02446',
        '(617) 555-CLEAN',
        'www.sparklecleansolutions.com',
        'Family-owned and operated for 10 years, we provide eco-friendly residential cleaning services throughout Greater Boston. Our team of 15 bonded and insured professionals has maintained a 4.9-star rating across 2000+ homes. We specialize in regular maintenance cleaning, deep cleaning, and move-in/move-out services.',
        'We seek busy professionals and families who value their time and want reliable, consistent cleaning services. Ideal clients need regular weekly or bi-weekly cleaning, have homes between 1500-4000 sq ft, appreciate eco-friendly products, and are looking for a long-term relationship with a trusted service provider.',
        'Dual-income households, busy professionals, and families with children in suburban Boston who prioritize cleanliness but lack time for regular housekeeping'
    ) ON CONFLICT (email) DO NOTHING;

-- ==== INSERT FORMS ====
-- 1. Dog Walking Form
INSERT INTO
    forms (
        id,
        client_id,
        title,
        description,
        lead_scoring_threshold_yes,
        lead_scoring_threshold_maybe,
        max_questions,
        min_questions_before_fail,
        completion_message_template,
        unqualified_message
    )
VALUES
    (
        'f1111111-1111-1111-1111-111111111111' :: uuid,
        'a1111111-1111-1111-1111-111111111111' :: uuid,
        'Dog Walking Service Interest Form',
        'Let us know about your dog and walking needs so we can provide the best service!',
        75,
        45,
        10,
        4,
        'Thank you {name}! We would love to walk {dog_name}. We will contact you within 24 hours to schedule a meet-and-greet.',
        'Thank you for your interest. Unfortunately, we may not be the right fit for your needs at this time.'
    ) ON CONFLICT (id) DO NOTHING;

-- 2. Real Estate Form
INSERT INTO
    forms (
        id,
        client_id,
        title,
        description,
        lead_scoring_threshold_yes,
        lead_scoring_threshold_maybe,
        max_questions,
        min_questions_before_fail,
        completion_message_template,
        unqualified_message
    )
VALUES
    (
        'f2222222-2222-2222-2222-222222222222' :: uuid,
        'a2222222-2222-2222-2222-222222222222' :: uuid,
        'Real Estate Consultation Request',
        'Tell us about your real estate goals and let us help you achieve them!',
        80,
        50,
        12,
        4,
        'Excellent {name}! Your {property_type} search in {location} is our priority. A specialist will call you within 2 hours to discuss your needs.',
        'Thank you for your interest. We recommend exploring online resources for your real estate questions at this time.'
    ) ON CONFLICT (id) DO NOTHING;

-- 3. Software Consulting Form
INSERT INTO
    forms (
        id,
        client_id,
        title,
        description,
        lead_scoring_threshold_yes,
        lead_scoring_threshold_maybe,
        max_questions,
        min_questions_before_fail,
        completion_message_template,
        unqualified_message
    )
VALUES
    (
        'f3333333-3333-3333-3333-333333333333' :: uuid,
        'a3333333-3333-3333-3333-333333333333' :: uuid,
        'Digital Transformation Assessment',
        'Discover how technology can transform your business operations and drive growth.',
        85,
        55,
        11,
        5,
        'Thank you {name}! Based on your {industry} needs, we have identified several opportunities to improve your {pain_point}. Our senior consultant will contact you within 24 hours.',
        'Thank you for your interest. We recommend starting with our free resources library for your technology needs.'
    ) ON CONFLICT (id) DO NOTHING;

-- 4. Personal Training Form
INSERT INTO
    forms (
        id,
        client_id,
        title,
        description,
        lead_scoring_threshold_yes,
        lead_scoring_threshold_maybe,
        max_questions,
        min_questions_before_fail,
        completion_message_template,
        unqualified_message
    )
VALUES
    (
        'f4444444-4444-4444-4444-444444444444' :: uuid,
        'a4444444-4444-4444-4444-444444444444' :: uuid,
        'Personal Training Consultation',
        'Start your fitness journey with a personalized training program designed for your goals!',
        75,
        45,
        10,
        4,
        'Awesome {name}! Your {goal} is absolutely achievable. We will call you today to schedule your free fitness assessment.',
        'Thank you for your interest in fitness. We encourage you to explore our online workout resources.'
    ) ON CONFLICT (id) DO NOTHING;

-- 5. Home Cleaning Form
INSERT INTO
    forms (
        id,
        client_id,
        title,
        description,
        lead_scoring_threshold_yes,
        lead_scoring_threshold_maybe,
        max_questions,
        min_questions_before_fail,
        completion_message_template,
        unqualified_message
    )
VALUES
    (
        'f5555555-5555-5555-5555-555555555555' :: uuid,
        'a5555555-5555-5555-5555-555555555555' :: uuid,
        'Home Cleaning Service Quote',
        'Get a customized cleaning plan that fits your home and schedule perfectly!',
        80,
        50,
        9,
        4,
        'Perfect {name}! We can definitely help with your {frequency} cleaning needs for your {home_size} home. Expect our call within 4 hours to finalize details.',
        'Thank you for considering our services. Your needs may be better served by other providers in your area.'
    ) ON CONFLICT (id) DO NOTHING;

-- ==== INSERT FORM QUESTIONS ====
-- 1. Dog Walking Service Questions (10 questions)
INSERT INTO
    form_questions (
        form_id,
        question_id,
        question_order,
        question_text,
        question_type,
        options,
        is_required,
        scoring_rubric,
        category
    )
VALUES
    -- Contact & Basic Info
    (
        'f1111111-1111-1111-1111-111111111111' :: uuid,
        1,
        1,
        'What is your name?',
        'text',
        NULL,
        true,
        NULL,
        'contact'
    ),
    (
        'f1111111-1111-1111-1111-111111111111' :: uuid,
        2,
        2,
        'What is your dog''s name and breed?',
        'text',
        NULL,
        false,
        '+5 points for providing dog info',
        'basic_info'
    ),
    -- Qualification Questions
    (
        'f1111111-1111-1111-1111-111111111111' :: uuid,
        3,
        3,
        'Where do you live (nearest intersection or neighborhood)?',
        'text',
        NULL,
        true,
        '+30 if within 2 miles, +20 if 2-5 miles, +10 if 5-10 miles, -20 if over 10 miles',
        'qualification'
    ),
    (
        'f1111111-1111-1111-1111-111111111111' :: uuid,
        4,
        4,
        'How often do you need dog walking services?',
        'select',
        '["Daily (5+ times/week)", "Regular (3-4 times/week)", "Occasional (1-2 times/week)", "As needed"]' :: jsonb,
        true,
        '+25 for daily, +20 for regular, +10 for occasional, +5 for as needed',
        'qualification'
    ),
    (
        'f1111111-1111-1111-1111-111111111111' :: uuid,
        5,
        5,
        'Is your dog up to date on all vaccinations including rabies?',
        'boolean',
        NULL,
        true,
        '+20 if yes, -50 if no (disqualifying)',
        'qualification'
    ),
    (
        'f1111111-1111-1111-1111-111111111111' :: uuid,
        6,
        6,
        'Can your dog be walked with other dogs?',
        'select',
        '["Yes, loves other dogs", "Yes, but prefers small groups", "No, needs individual walks", "Not sure"]' :: jsonb,
        false,
        '+15 for loves others, +10 for small groups, +5 for individual, +5 for not sure',
        'compatibility'
    ),
    -- Engagement Questions
    (
        'f1111111-1111-1111-1111-111111111111' :: uuid,
        7,
        7,
        'What time of day works best for walks?',
        'select',
        '["Early morning (6-9am)", "Mid-morning (9am-12pm)", "Afternoon (12-3pm)", "Late afternoon (3-6pm)", "Flexible"]' :: jsonb,
        false,
        '+5 for any answer',
        'engagement'
    ),
    (
        'f1111111-1111-1111-1111-111111111111' :: uuid,
        8,
        8,
        'Does your dog have any special needs or behaviors we should know about?',
        'textarea',
        NULL,
        false,
        '+5 for providing information',
        'engagement'
    ),
    -- Contact completion
    (
        'f1111111-1111-1111-1111-111111111111' :: uuid,
        9,
        9,
        'What is your email address?',
        'email',
        NULL,
        true,
        NULL,
        'contact'
    ),
    (
        'f1111111-1111-1111-1111-111111111111' :: uuid,
        10,
        10,
        'What is the best phone number to reach you?',
        'phone',
        NULL,
        true,
        NULL,
        'contact'
    ) ON CONFLICT (form_id, question_id) DO NOTHING;

-- 2. Real Estate Agent Questions (12 questions)
INSERT INTO
    form_questions (
        form_id,
        question_id,
        question_order,
        question_text,
        question_type,
        options,
        is_required,
        scoring_rubric,
        category
    )
VALUES
    -- Initial Qualification
    (
        'f2222222-2222-2222-2222-222222222222' :: uuid,
        1,
        1,
        'Are you looking to buy or sell property?',
        'select',
        '["Buy", "Sell", "Both", "Just researching"]' :: jsonb,
        true,
        '+10 for buy/sell/both, -20 for just researching',
        'qualification'
    ),
    (
        'f2222222-2222-2222-2222-222222222222' :: uuid,
        2,
        2,
        'What is your timeline for making a move?',
        'select',
        '["Immediate (within 30 days)", "Soon (1-3 months)", "Planning (3-6 months)", "Future (6+ months)", "Just browsing"]' :: jsonb,
        true,
        '+30 for immediate, +25 for soon, +15 for planning, +5 for future, -30 for browsing',
        'qualification'
    ),
    -- Financial Qualification
    (
        'f2222222-2222-2222-2222-222222222222' :: uuid,
        3,
        3,
        'What is your budget range? (For buyers)',
        'select',
        '["Under $300K", "$300K-$500K", "$500K-$750K", "$750K-$1M", "Over $1M", "Not applicable (selling only)"]' :: jsonb,
        false,
        '+5 for under 300K, +15 for 300-500K, +20 for 500-750K, +25 for 750K-1M, +30 for over 1M',
        'qualification'
    ),
    (
        'f2222222-2222-2222-2222-222222222222' :: uuid,
        4,
        4,
        'Are you pre-approved for a mortgage? (For buyers)',
        'select',
        '["Yes, fully pre-approved", "In process", "Planning to apply", "Cash buyer", "Not yet", "Not applicable (selling only)"]' :: jsonb,
        false,
        '+25 for pre-approved, +15 for in process, +10 for planning, +30 for cash, +5 for not yet',
        'qualification'
    ),
    -- Property Details
    (
        'f2222222-2222-2222-2222-222222222222' :: uuid,
        5,
        5,
        'What type of property are you interested in?',
        'select',
        '["Single family home", "Condo", "Multi-family", "Commercial", "Land", "Any"]' :: jsonb,
        false,
        '+5 for any selection',
        'basic_info'
    ),
    (
        'f2222222-2222-2222-2222-222222222222' :: uuid,
        6,
        6,
        'Which areas are you considering?',
        'text',
        NULL,
        true,
        '+10 for specific areas, +5 for general region',
        'basic_info'
    ),
    -- Engagement Questions
    (
        'f2222222-2222-2222-2222-222222222222' :: uuid,
        7,
        7,
        'What is most important to you in this transaction?',
        'textarea',
        NULL,
        false,
        '+5 for detailed response',
        'engagement'
    ),
    (
        'f2222222-2222-2222-2222-222222222222' :: uuid,
        8,
        8,
        'Have you worked with a real estate agent before?',
        'select',
        '["Yes, great experience", "Yes, okay experience", "Yes, poor experience", "No, first time", "Currently have an agent"]' :: jsonb,
        false,
        '+10 for no agent, +5 for poor/okay experience, +3 for great experience, -20 for current agent',
        'engagement'
    ),
    -- Contact Information
    (
        'f2222222-2222-2222-2222-222222222222' :: uuid,
        9,
        9,
        'What is your full name?',
        'text',
        NULL,
        true,
        NULL,
        'contact'
    ),
    (
        'f2222222-2222-2222-2222-222222222222' :: uuid,
        10,
        10,
        'What is your email address?',
        'email',
        NULL,
        true,
        NULL,
        'contact'
    ),
    (
        'f2222222-2222-2222-2222-222222222222' :: uuid,
        11,
        11,
        'What is your phone number?',
        'phone',
        NULL,
        true,
        NULL,
        'contact'
    ),
    (
        'f2222222-2222-2222-2222-222222222222' :: uuid,
        12,
        12,
        'Preferred contact method and best time to call?',
        'text',
        NULL,
        false,
        NULL,
        'contact'
    ) ON CONFLICT (form_id, question_id) DO NOTHING;

-- 3. Software Consulting Questions (11 questions)
INSERT INTO
    form_questions (
        form_id,
        question_id,
        question_order,
        question_text,
        question_type,
        options,
        is_required,
        scoring_rubric,
        category
    )
VALUES
    -- Company Qualification
    (
        'f3333333-3333-3333-3333-333333333333' :: uuid,
        1,
        1,
        'What is your company name and industry?',
        'text',
        NULL,
        true,
        '+5 for providing details',
        'basic_info'
    ),
    (
        'f3333333-3333-3333-3333-333333333333' :: uuid,
        2,
        2,
        'What is your company''s approximate annual revenue?',
        'select',
        '["Under $500K", "$500K-$1M", "$1M-$5M", "$5M-$20M", "$20M-$50M", "Over $50M"]' :: jsonb,
        true,
        '+5 for under 500K, +10 for 500K-1M, +20 for 1M-5M, +30 for 5M-20M, +25 for 20M-50M, +20 for over 50M',
        'qualification'
    ),
    (
        'f3333333-3333-3333-3333-333333333333' :: uuid,
        3,
        3,
        'How many employees does your company have?',
        'select',
        '["1-10", "11-50", "51-200", "201-500", "500+"]' :: jsonb,
        false,
        '+10 for 1-10, +20 for 11-50, +25 for 51-200, +20 for 201-500, +15 for 500+',
        'qualification'
    ),
    -- Project Details
    (
        'f3333333-3333-3333-3333-333333333333' :: uuid,
        4,
        4,
        'What technology challenges are you facing?',
        'textarea',
        NULL,
        true,
        '+10 for specific challenges, +5 for general issues',
        'qualification'
    ),
    (
        'f3333333-3333-3333-3333-333333333333' :: uuid,
        5,
        5,
        'What is your estimated project budget?',
        'select',
        '["Under $10K", "$10K-$25K", "$25K-$50K", "$50K-$100K", "$100K-$250K", "Over $250K", "Not determined"]' :: jsonb,
        true,
        '-10 for under 10K, +10 for 10-25K, +20 for 25-50K, +30 for 50-100K, +35 for 100-250K, +40 for over 250K, +5 for not determined',
        'qualification'
    ),
    (
        'f3333333-3333-3333-3333-333333333333' :: uuid,
        6,
        6,
        'When do you need to start this project?',
        'select',
        '["Immediately", "Within 1 month", "1-3 months", "3-6 months", "6+ months", "Just exploring"]' :: jsonb,
        true,
        '+30 for immediately, +25 for 1 month, +20 for 1-3 months, +10 for 3-6 months, +5 for 6+ months, -20 for exploring',
        'qualification'
    ),
    -- Decision Making
    (
        'f3333333-3333-3333-3333-333333333333' :: uuid,
        7,
        7,
        'What is your role in the decision-making process?',
        'select',
        '["Final decision maker", "Key influencer", "Researching for team", "End user", "Other"]' :: jsonb,
        true,
        '+25 for decision maker, +20 for influencer, +10 for researching, +5 for end user, +5 for other',
        'qualification'
    ),
    -- Engagement
    (
        'f3333333-3333-3333-3333-333333333333' :: uuid,
        8,
        8,
        'Have you worked with consultants before?',
        'select',
        '["Yes, successfully", "Yes, with mixed results", "No, first time", "Currently working with another firm"]' :: jsonb,
        false,
        '+10 for first time, +8 for mixed results, +5 for successfully, -15 for current firm',
        'engagement'
    ),
    -- Contact Information
    (
        'f3333333-3333-3333-3333-333333333333' :: uuid,
        9,
        9,
        'Your full name and title?',
        'text',
        NULL,
        true,
        NULL,
        'contact'
    ),
    (
        'f3333333-3333-3333-3333-333333333333' :: uuid,
        10,
        10,
        'Your business email address?',
        'email',
        NULL,
        true,
        NULL,
        'contact'
    ),
    (
        'f3333333-3333-3333-3333-333333333333' :: uuid,
        11,
        11,
        'Best phone number for business hours?',
        'phone',
        NULL,
        true,
        NULL,
        'contact'
    ) ON CONFLICT (form_id, question_id) DO NOTHING;

-- 4. Personal Training Questions (10 questions)
INSERT INTO
    form_questions (
        form_id,
        question_id,
        question_order,
        question_text,
        question_type,
        options,
        is_required,
        scoring_rubric,
        category
    )
VALUES
    -- Goals and Commitment
    (
        'f4444444-4444-4444-4444-444444444444' :: uuid,
        1,
        1,
        'What are your primary fitness goals?',
        'select',
        '["Weight loss", "Muscle gain", "Athletic performance", "General health", "Rehabilitation", "Not sure yet"]' :: jsonb,
        true,
        '+20 for specific goals, +10 for general health, +5 for not sure',
        'qualification'
    ),
    (
        'f4444444-4444-4444-4444-444444444444' :: uuid,
        2,
        2,
        'How many days per week can you commit to training?',
        'select',
        '["1 day", "2 days", "3 days", "4 days", "5+ days"]' :: jsonb,
        true,
        '+5 for 1 day, +10 for 2 days, +20 for 3 days, +25 for 4 days, +30 for 5+ days',
        'qualification'
    ),
    (
        'f4444444-4444-4444-4444-444444444444' :: uuid,
        3,
        3,
        'What is your budget for personal training per month?',
        'select',
        '["Under $200", "$200-$400", "$400-$600", "$600-$800", "Over $800"]' :: jsonb,
        true,
        '+5 for under 200, +10 for 200-400, +20 for 400-600, +25 for 600-800, +30 for over 800',
        'qualification'
    ),
    -- Health and Experience
    (
        'f4444444-4444-4444-4444-444444444444' :: uuid,
        4,
        4,
        'Do you have any injuries or health conditions?',
        'textarea',
        NULL,
        false,
        '+5 for disclosure, enables proper program design',
        'health'
    ),
    (
        'f4444444-4444-4444-4444-444444444444' :: uuid,
        5,
        5,
        'What is your current activity level?',
        'select',
        '["Sedentary", "Lightly active", "Moderately active", "Very active", "Athlete"]' :: jsonb,
        false,
        '+5 for any level - helps with program design',
        'basic_info'
    ),
    (
        'f4444444-4444-4444-4444-444444444444' :: uuid,
        6,
        6,
        'Have you worked with a personal trainer before?',
        'select',
        '["Yes, great results", "Yes, some results", "Yes, no results", "No, never"]' :: jsonb,
        false,
        '+10 for never, +8 for no results, +5 for some results, +3 for great results',
        'engagement'
    ),
    -- Logistics
    (
        'f4444444-4444-4444-4444-444444444444' :: uuid,
        7,
        7,
        'What time of day works best for training?',
        'select',
        '["Early morning (5-8am)", "Morning (8-11am)", "Lunch (11am-2pm)", "Afternoon (2-5pm)", "Evening (5-8pm)", "Flexible"]' :: jsonb,
        false,
        '+5 for any selection',
        'logistics'
    ),
    -- Contact Information
    (
        'f4444444-4444-4444-4444-444444444444' :: uuid,
        8,
        8,
        'Your full name?',
        'text',
        NULL,
        true,
        NULL,
        'contact'
    ),
    (
        'f4444444-4444-4444-4444-444444444444' :: uuid,
        9,
        9,
        'Your email address?',
        'email',
        NULL,
        true,
        NULL,
        'contact'
    ),
    (
        'f4444444-4444-4444-4444-444444444444' :: uuid,
        10,
        10,
        'Your phone number?',
        'phone',
        NULL,
        true,
        NULL,
        'contact'
    ) ON CONFLICT (form_id, question_id) DO NOTHING;

-- 5. Home Cleaning Service Questions (9 questions)
INSERT INTO
    form_questions (
        form_id,
        question_id,
        question_order,
        question_text,
        question_type,
        options,
        is_required,
        scoring_rubric,
        category
    )
VALUES
    -- Property Details
    (
        'f5555555-5555-5555-5555-555555555555' :: uuid,
        1,
        1,
        'What is the size of your home?',
        'select',
        '["Under 1000 sq ft", "1000-1500 sq ft", "1500-2000 sq ft", "2000-3000 sq ft", "3000-4000 sq ft", "Over 4000 sq ft"]' :: jsonb,
        true,
        '+5 for under 1000, +10 for 1000-1500, +15 for 1500-2000, +25 for 2000-3000, +30 for 3000-4000, +25 for over 4000',
        'qualification'
    ),
    (
        'f5555555-5555-5555-5555-555555555555' :: uuid,
        2,
        2,
        'How many bedrooms and bathrooms?',
        'text',
        NULL,
        true,
        '+5 for providing details',
        'basic_info'
    ),
    -- Service Requirements
    (
        'f5555555-5555-5555-5555-555555555555' :: uuid,
        3,
        3,
        'How often would you like cleaning service?',
        'select',
        '["Weekly", "Bi-weekly", "Monthly", "One-time deep clean", "Move-in/out"]' :: jsonb,
        true,
        '+30 for weekly, +25 for bi-weekly, +15 for monthly, +5 for one-time, +10 for move',
        'qualification'
    ),
    (
        'f5555555-5555-5555-5555-555555555555' :: uuid,
        4,
        4,
        'What is your budget per cleaning?',
        'select',
        '["Under $100", "$100-$150", "$150-$200", "$200-$250", "Over $250"]' :: jsonb,
        true,
        '+5 for under 100, +15 for 100-150, +25 for 150-200, +30 for 200-250, +35 for over 250',
        'qualification'
    ),
    (
        'f5555555-5555-5555-5555-555555555555' :: uuid,
        5,
        5,
        'What is your location (city/neighborhood)?',
        'text',
        NULL,
        true,
        '+20 if within service area, +10 if adjacent area, -20 if outside area',
        'qualification'
    ),
    -- Special Requirements
    (
        'f5555555-5555-5555-5555-555555555555' :: uuid,
        6,
        6,
        'Do you have pets?',
        'select',
        '["No pets", "Cat(s)", "Dog(s)", "Both cats and dogs", "Other pets"]' :: jsonb,
        false,
        '+5 for any answer - helps prepare team',
        'basic_info'
    ),
    (
        'f5555555-5555-5555-5555-555555555555' :: uuid,
        7,
        7,
        'Any special cleaning requirements or areas of focus?',
        'textarea',
        NULL,
        false,
        '+5 for providing details',
        'engagement'
    ),
    -- Contact Information
    (
        'f5555555-5555-5555-5555-555555555555' :: uuid,
        8,
        8,
        'Your full name?',
        'text',
        NULL,
        true,
        NULL,
        'contact'
    ),
    (
        'f5555555-5555-5555-5555-555555555555' :: uuid,
        9,
        9,
        'Your email and phone number?',
        'text',
        NULL,
        true,
        NULL,
        'contact'
    ) ON CONFLICT (form_id, question_id) DO NOTHING;

-- ==== VERIFICATION QUERIES ====
-- Verify data population
SELECT
    'Data Population Summary:' as info;

SELECT
    'Clients: ' || COUNT(*) as count
FROM
    clients
WHERE
    email LIKE '%@jkwb.mozmail.com';

SELECT
    'Forms: ' || COUNT(*) as count
FROM
    forms
WHERE
    client_id IN (
        SELECT
            id
        FROM
            clients
        WHERE
            email LIKE '%@jkwb.mozmail.com'
    );

SELECT
    'Questions: ' || COUNT(*) as count
FROM
    form_questions
WHERE
    form_id IN (
        SELECT
            id
        FROM
            forms
        WHERE
            client_id IN (
                SELECT
                    id
                FROM
                    clients
                WHERE
                    email LIKE '%@jkwb.mozmail.com'
            )
    );

-- Show summary by business
SELECT
    c.business_name,
    f.title as form_title,
    COUNT(fq.id) as question_count,
    f.lead_scoring_threshold_yes as yes_threshold,
    f.lead_scoring_threshold_maybe as maybe_threshold
FROM
    clients c
    JOIN forms f ON f.client_id = c.id
    LEFT JOIN form_questions fq ON fq.form_id = f.id
WHERE
    c.email LIKE '%@jkwb.mozmail.com'
GROUP BY
    c.business_name,
    f.title,
    f.lead_scoring_threshold_yes,
    f.lead_scoring_threshold_maybe
ORDER BY
    c.business_name;