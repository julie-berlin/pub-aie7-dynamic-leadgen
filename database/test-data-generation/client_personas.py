"""
Client personas and form data for comprehensive test data generation.
Contains realistic personas for all 5 business types with appropriate responses.
"""

# Client and Form ID mappings
CLIENT_IDS = {
    'pawsome': 'a1111111-1111-1111-1111-111111111111',
    'metro_realty': 'a2222222-2222-2222-2222-222222222222', 
    'techsolve': 'a3333333-3333-3333-3333-333333333333',
    'fitlife': 'a4444444-4444-4444-4444-444444444444',
    'sparkle_clean': 'a5555555-5555-5555-5555-555555555555'
}

FORM_IDS = {
    'pawsome': 'f1111111-1111-1111-1111-111111111111',
    'metro_realty': 'f2222222-2222-2222-2222-222222222222',
    'techsolve': 'f3333333-3333-3333-3333-333333333333', 
    'fitlife': 'f4444444-4444-4444-4444-444444444444',
    'sparkle_clean': 'f5555555-5555-5555-5555-555555555555'
}

# ==== PAWSOME DOG WALKING PERSONAS ====
PAWSOME_PERSONAS = [
    {
        'name': 'Emily Rodriguez',
        'email': 'emily.rodriguez@mit.edu',
        'phone': '(617) 555-0192',
        'dog_breed': 'German Shepherd',
        'dog_age': '5',
        'behavior': 'very_well',
        'walks_per_week': '5_plus',
        'address': '1234 Mass Ave, Cambridge',
        'budget': '25_35',
        'lead_type': 'qualified',
        'score': 95,
        'utm_source': 'google',
        'utm_campaign': 'premium_dog_walking',
        'device': 'desktop'
    },
    {
        'name': 'David Park',
        'email': 'david.park@gmail.com', 
        'phone': '(617) 555-0283',
        'dog_breed': 'Beagle',
        'dog_age': '8',
        'behavior': 'mostly_well',
        'walks_per_week': '2',
        'address': 'Somerville near Davis Square',
        'lead_type': 'maybe',
        'score': 65,
        'utm_source': 'facebook',
        'utm_campaign': 'local_dog_services',
        'device': 'mobile'
    },
    {
        'name': 'Sarah Kim',
        'email': 'sarah.kim@harvard.edu',
        'phone': '(617) 555-0374',
        'dog_breed': 'Golden Retriever',
        'dog_age': '3',
        'behavior': 'very_well',
        'walks_per_week': '3_4',
        'address': 'Harvard Square area',
        'budget': '20_30',
        'lead_type': 'qualified',
        'score': 88,
        'utm_source': 'google',
        'utm_campaign': 'harvard_students',
        'device': 'mobile'
    },
    {
        'name': 'Mike Johnson',
        'email': 'mjohnson.work@outlook.com',
        'phone': None,
        'dog_breed': 'Pit Bull Mix',
        'dog_age': '2',
        'behavior': 'rarely',
        'walks_per_week': '1',
        'address': 'Dorchester',
        'budget': 'under_15',
        'lead_type': 'unqualified',
        'score': 25,
        'utm_source': 'organic',
        'device': 'desktop'
    },
    {
        'name': 'Jennifer Walsh',
        'email': 'jwalsh.home@gmail.com',
        'dog_breed': 'Lab Mix',
        'dog_age': '6', 
        'behavior': 'mostly_well',
        'walks_per_week': '2',
        'address': 'Medford Square area',
        'lead_type': 'maybe',
        'score': 60,
        'utm_source': 'facebook',
        'utm_campaign': 'medford_pet_owners',
        'device': 'mobile'
    }
]

PAWSOME_QUESTIONS = {
    1: 'name',
    2: 'email',
    3: 'phone',
    4: 'dog_breed',
    5: 'dog_age',
    6: 'behavior',
    7: 'walks_per_week',
    8: 'address',
    9: 'budget'
}

# ==== METRO REALTY GROUP PERSONAS ====
METRO_REALTY_PERSONAS = [
    {
        'name': 'Jessica Chen',
        'email': 'jessica.chen@techcorp.com',
        'phone': '(617) 555-1234',
        'buy_or_sell': 'buy',
        'timeline': 'within_3_months',
        'mortgage_status': 'pre_approved',
        'price_range': '$500k_plus',
        'areas': 'boston_cambridge',
        'first_time_buyer': 'no',
        'bedrooms': '3_bedrooms',
        'worked_with_realtor': 'no',
        'urgency': 'high',
        'lead_type': 'qualified',
        'score': 90,
        'utm_source': 'google',
        'utm_campaign': 'luxury_homes_boston',
        'device': 'desktop'
    },
    {
        'name': 'Mark Thompson',
        'email': 'mark.thompson@startup.io',
        'phone': '(857) 555-5678',
        'buy_or_sell': 'both',
        'timeline': '3_6_months',
        'mortgage_status': 'in_process',
        'price_range': '$300k_500k',
        'areas': 'brookline_newton',
        'first_time_buyer': 'yes',
        'bedrooms': '2_bedrooms',
        'worked_with_realtor': 'yes',
        'urgency': 'medium',
        'lead_type': 'qualified',
        'score': 85,
        'utm_source': 'facebook',
        'utm_campaign': 'first_time_buyers',
        'device': 'mobile'
    },
    {
        'name': 'Amanda Rodriguez',
        'email': 'arodriguez@lawfirm.com',
        'phone': '(617) 555-9012',
        'buy_or_sell': 'sell',
        'timeline': 'within_3_months',
        'mortgage_status': 'cash',
        'price_range': '$500k_plus',
        'areas': 'boston_cambridge',
        'first_time_buyer': 'no',
        'bedrooms': '4_bedrooms',
        'worked_with_realtor': 'no',
        'urgency': 'high',
        'lead_type': 'qualified',
        'score': 92,
        'utm_source': 'referral',
        'utm_campaign': 'luxury_sellers',
        'device': 'desktop'
    },
    {
        'name': 'Kevin O\'Brien',
        'email': 'kevin.obrien@email.com',
        'phone': '(508) 555-3456',
        'buy_or_sell': 'buy',
        'timeline': 'just_browsing',
        'mortgage_status': 'planning_to_get',
        'price_range': 'under_200k',
        'areas': 'other_metro',
        'first_time_buyer': 'yes',
        'bedrooms': '1_bedroom',
        'worked_with_realtor': 'no',
        'urgency': 'low',
        'lead_type': 'unqualified',
        'score': 35,
        'utm_source': 'organic',
        'utm_campaign': 'general_search',
        'device': 'mobile'
    },
    {
        'name': 'Lisa Martinez',
        'email': 'lisa.martinez@hospital.org',
        'phone': '(781) 555-7890',
        'buy_or_sell': 'buy',
        'timeline': '6_12_months',
        'mortgage_status': 'in_process',
        'price_range': '$200k_300k',
        'areas': 'other_metro',
        'first_time_buyer': 'yes',
        'bedrooms': '2_bedrooms',
        'worked_with_realtor': 'yes',
        'urgency': 'medium',
        'lead_type': 'maybe',
        'score': 65,
        'utm_source': 'google',
        'utm_campaign': 'affordable_homes',
        'device': 'desktop'
    }
]

METRO_REALTY_QUESTIONS = {
    1: 'name',
    2: 'email', 
    3: 'phone',
    4: 'buy_or_sell',
    5: 'timeline',
    6: 'mortgage_status',
    7: 'price_range',
    8: 'areas',
    9: 'first_time_buyer',
    10: 'bedrooms',
    11: 'worked_with_realtor',
    12: 'urgency'
}

# ==== TECHSOLVE CONSULTING PERSONAS ====
TECHSOLVE_PERSONAS = [
    {
        'name': 'Robert Kim',
        'email': 'robert.kim@enterprise.com',
        'phone': '(617) 555-2468',
        'company_size': '50_200_employees',
        'tech_challenges': 'legacy_systems',
        'budget_range': '$50k_100k',
        'timeline': 'within_3_months',
        'current_setup': 'mixed_cloud_onprem',
        'decision_maker': 'yes',
        'industry': 'manufacturing',
        'previous_consulting': 'yes_good',
        'urgency': 'high',
        'meeting_availability': 'within_week',
        'primary_goal': 'digital_transformation',
        'lead_type': 'qualified',
        'score': 92,
        'utm_source': 'linkedin',
        'utm_campaign': 'enterprise_solutions',
        'device': 'desktop'
    },
    {
        'name': 'Patricia Davis',
        'email': 'p.davis@retailchain.com',
        'phone': '(857) 555-1357',
        'company_size': '10_50_employees',
        'tech_challenges': 'data_management',
        'budget_range': '$25k_50k',
        'timeline': '3_6_months',
        'current_setup': 'mostly_cloud',
        'decision_maker': 'shared',
        'industry': 'retail',
        'previous_consulting': 'no',
        'urgency': 'medium',
        'meeting_availability': 'next_month',
        'primary_goal': 'process_automation',
        'lead_type': 'qualified',
        'score': 78,
        'utm_source': 'google',
        'utm_campaign': 'small_business_tech',
        'device': 'desktop'
    },
    {
        'name': 'James Wilson',
        'email': 'james.wilson@nonprofit.org',
        'phone': '(617) 555-8024',
        'company_size': 'under_10',
        'tech_challenges': 'security',
        'budget_range': 'under_25k',
        'timeline': '6_12_months',
        'current_setup': 'mostly_onprem',
        'decision_maker': 'no',
        'industry': 'nonprofit',
        'previous_consulting': 'yes_mixed',
        'urgency': 'low',
        'meeting_availability': 'more_than_month',
        'primary_goal': 'cost_reduction',
        'lead_type': 'maybe',
        'score': 45,
        'utm_source': 'organic',
        'utm_campaign': 'nonprofit_solutions',
        'device': 'mobile'
    },
    {
        'name': 'Michelle Brown',
        'email': 'mbrown@startup.co',
        'phone': None,
        'company_size': 'under_10',
        'tech_challenges': 'scaling',
        'budget_range': 'under_25k',
        'timeline': 'just_exploring',
        'current_setup': 'all_cloud',
        'decision_maker': 'yes',
        'industry': 'technology',
        'previous_consulting': 'no',
        'urgency': 'low',
        'meeting_availability': 'more_than_month',
        'primary_goal': 'cost_reduction',
        'lead_type': 'unqualified',
        'score': 30,
        'utm_source': 'organic',
        'utm_campaign': 'startup_resources',
        'device': 'mobile'
    },
    {
        'name': 'Thomas Anderson',
        'email': 'tanderson@midcorp.com',
        'phone': '(508) 555-4680',
        'company_size': '10_50_employees',
        'tech_challenges': 'integration',
        'budget_range': '$25k_50k',
        'timeline': '3_6_months',
        'current_setup': 'mixed_cloud_onprem',
        'decision_maker': 'shared',
        'industry': 'healthcare',
        'previous_consulting': 'yes_good',
        'urgency': 'medium',
        'meeting_availability': 'within_month',
        'primary_goal': 'digital_transformation',
        'lead_type': 'maybe',
        'score': 68,
        'utm_source': 'referral',
        'utm_campaign': 'healthcare_tech',
        'device': 'desktop'
    }
]

TECHSOLVE_QUESTIONS = {
    1: 'name',
    2: 'email',
    3: 'phone', 
    4: 'company_size',
    5: 'tech_challenges',
    6: 'budget_range',
    7: 'timeline',
    8: 'current_setup',
    9: 'decision_maker',
    10: 'industry',
    11: 'previous_consulting'
}

# ==== FITLIFE PERSONAL TRAINING PERSONAS ====
FITLIFE_PERSONAS = [
    {
        'name': 'Rachel Green',
        'email': 'rachel.green@consulting.com',
        'phone': '(617) 555-3691',
        'fitness_goals': 'weight_loss',
        'experience_level': 'beginner',
        'availability': 'mornings',
        'preferred_location': 'gym',
        'budget': '$100_150',
        'health_conditions': 'none',
        'timeline': 'asap',
        'motivation_level': 'very_motivated',
        'training_type': 'one_on_one',
        'commitment_level': '3_sessions_week',
        'lead_type': 'qualified',
        'score': 88,
        'utm_source': 'instagram',
        'utm_campaign': 'transformation_stories',
        'device': 'mobile'
    },
    {
        'name': 'Steve Rogers',
        'email': 'steve.rogers@military.gov',
        'phone': '(857) 555-7410',
        'fitness_goals': 'strength_building',
        'experience_level': 'intermediate',
        'availability': 'evenings',
        'preferred_location': 'home',
        'budget': '$150_200',
        'health_conditions': 'minor_injury',
        'timeline': 'within_month',
        'motivation_level': 'very_motivated',
        'training_type': 'one_on_one',
        'commitment_level': '4_sessions_week',
        'lead_type': 'qualified',
        'score': 92,
        'utm_source': 'google',
        'utm_campaign': 'strength_training',
        'device': 'desktop'
    },
    {
        'name': 'Monica Bellucci',
        'email': 'monica.bellucci@fashion.com',
        'phone': '(617) 555-8520',
        'fitness_goals': 'general_fitness',
        'experience_level': 'intermediate',
        'availability': 'flexible',
        'preferred_location': 'gym',
        'budget': '$75_100',
        'health_conditions': 'none',
        'timeline': 'within_month',
        'motivation_level': 'motivated',
        'training_type': 'small_group',
        'commitment_level': '2_sessions_week',
        'lead_type': 'maybe',
        'score': 65,
        'utm_source': 'facebook',
        'utm_campaign': 'group_fitness',
        'device': 'mobile'
    },
    {
        'name': 'Peter Parker',
        'email': 'peter.parker@university.edu',
        'phone': '(617) 555-9630',
        'fitness_goals': 'athletic_performance',
        'experience_level': 'advanced',
        'availability': 'afternoons',
        'preferred_location': 'gym',
        'budget': 'under_75',
        'health_conditions': 'none',
        'timeline': 'just_exploring',
        'motivation_level': 'somewhat_motivated',
        'training_type': 'small_group',
        'commitment_level': '1_session_week',
        'lead_type': 'unqualified',
        'score': 35,
        'utm_source': 'organic',
        'utm_campaign': 'student_fitness',
        'device': 'mobile'
    },
    {
        'name': 'Diana Prince',
        'email': 'diana.prince@embassy.gov',
        'phone': '(781) 555-1470',
        'fitness_goals': 'martial_arts',
        'experience_level': 'advanced',
        'availability': 'evenings',
        'preferred_location': 'home',
        'budget': '$100_150',
        'health_conditions': 'none',
        'timeline': 'within_month',
        'motivation_level': 'motivated',
        'training_type': 'one_on_one',
        'commitment_level': '2_sessions_week',
        'lead_type': 'maybe',
        'score': 70,
        'utm_source': 'referral',
        'utm_campaign': 'specialized_training',
        'device': 'desktop'
    }
]

FITLIFE_QUESTIONS = {
    1: 'name',
    2: 'email',
    3: 'phone',
    4: 'fitness_goals',
    5: 'experience_level',
    6: 'availability',
    7: 'preferred_location',
    8: 'budget',
    9: 'health_conditions',
    10: 'timeline'
}

# ==== SPARKLE CLEAN SOLUTIONS PERSONAS ====
SPARKLE_CLEAN_PERSONAS = [
    {
        'name': 'Helen Smith',
        'email': 'helen.smith@lawfirm.com',
        'phone': '(617) 555-2580',
        'service_type': 'regular_cleaning',
        'home_size': 'large_4plus_bed',
        'frequency': 'weekly',
        'special_requirements': 'pet_friendly',
        'budget': '$150_plus',
        'location': 'cambridge',
        'timeline': 'within_week',
        'home_access': 'key_provided',
        'priority_areas': 'kitchen_bathrooms',
        'lead_type': 'qualified',
        'score': 90,
        'utm_source': 'google',
        'utm_campaign': 'luxury_home_cleaning',
        'device': 'desktop'
    },
    {
        'name': 'Carlos Rodriguez',
        'email': 'carlos.rodriguez@tech.com',
        'phone': '(857) 555-3691',
        'service_type': 'deep_cleaning',
        'home_size': 'medium_2_3_bed',
        'frequency': 'one_time',
        'special_requirements': 'eco_friendly',
        'budget': '$100_150',
        'location': 'somerville',
        'timeline': 'within_month',
        'home_access': 'present_during',
        'priority_areas': 'whole_house',
        'lead_type': 'qualified',
        'score': 82,
        'utm_source': 'yelp',
        'utm_campaign': 'deep_clean_specialists',
        'device': 'mobile'
    },
    {
        'name': 'Betty Johnson',
        'email': 'betty.johnson@email.com',
        'phone': '(617) 555-4702',
        'service_type': 'regular_cleaning',
        'home_size': 'small_1_bed',
        'frequency': 'bi_weekly',
        'special_requirements': 'none',
        'budget': '$75_100',
        'location': 'boston',
        'timeline': 'within_month',
        'home_access': 'key_provided',
        'priority_areas': 'bathroom_bedroom',
        'lead_type': 'maybe',
        'score': 65,
        'utm_source': 'facebook',
        'utm_campaign': 'apartment_cleaning',
        'device': 'desktop'
    },
    {
        'name': 'Gary Wilson',
        'email': 'gary.wilson@startup.co',
        'phone': None,
        'service_type': 'regular_cleaning',
        'home_size': 'small_1_bed',
        'frequency': 'monthly',
        'special_requirements': 'none',
        'budget': 'under_75',
        'location': 'other',
        'timeline': 'just_exploring',
        'home_access': 'present_during',
        'priority_areas': 'kitchen_bathrooms',
        'lead_type': 'unqualified',
        'score': 30,
        'utm_source': 'organic',
        'utm_campaign': 'budget_cleaning',
        'device': 'mobile'
    },
    {
        'name': 'Maria Santos',
        'email': 'maria.santos@hospital.org',
        'phone': '(781) 555-5813',
        'service_type': 'move_in_out',
        'home_size': 'medium_2_3_bed',
        'frequency': 'one_time',
        'special_requirements': 'eco_friendly',
        'budget': '$100_150',
        'location': 'brookline',
        'timeline': 'within_month',
        'home_access': 'present_during',
        'priority_areas': 'whole_house',
        'lead_type': 'maybe',
        'score': 70,
        'utm_source': 'referral',
        'utm_campaign': 'move_cleaning',
        'device': 'desktop'
    }
]

SPARKLE_CLEAN_QUESTIONS = {
    1: 'name',
    2: 'email',
    3: 'phone',
    4: 'service_type',
    5: 'home_size',
    6: 'frequency',
    7: 'special_requirements',
    8: 'budget',
    9: 'location'
}

# Combine all personas for easy access
ALL_CLIENT_DATA = {
    'pawsome': {
        'personas': PAWSOME_PERSONAS,
        'questions': PAWSOME_QUESTIONS,
        'client_id': CLIENT_IDS['pawsome'],
        'form_id': FORM_IDS['pawsome']
    },
    'metro_realty': {
        'personas': METRO_REALTY_PERSONAS,
        'questions': METRO_REALTY_QUESTIONS,
        'client_id': CLIENT_IDS['metro_realty'],
        'form_id': FORM_IDS['metro_realty']
    },
    'techsolve': {
        'personas': TECHSOLVE_PERSONAS,
        'questions': TECHSOLVE_QUESTIONS,
        'client_id': CLIENT_IDS['techsolve'],
        'form_id': FORM_IDS['techsolve']
    },
    'fitlife': {
        'personas': FITLIFE_PERSONAS,
        'questions': FITLIFE_QUESTIONS,
        'client_id': CLIENT_IDS['fitlife'],
        'form_id': FORM_IDS['fitlife']
    },
    'sparkle_clean': {
        'personas': SPARKLE_CLEAN_PERSONAS,
        'questions': SPARKLE_CLEAN_QUESTIONS,
        'client_id': CLIENT_IDS['sparkle_clean'],
        'form_id': FORM_IDS['sparkle_clean']
    }
}