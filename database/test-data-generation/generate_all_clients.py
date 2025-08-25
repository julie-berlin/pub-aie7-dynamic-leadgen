#!/usr/bin/env python3
"""
Comprehensive Test Data Generator for Dynamic Surveys Platform

Generates realistic lead sessions for all 5 business clients:
1. Pawsome Dog Walking (Pet Services) - 30 leads
2. Metro Realty Group (Real Estate) - 30 leads  
3. TechSolve Consulting (Software Consulting) - 30 leads
4. FitLife Personal Training (Health & Fitness) - 30 leads
5. Sparkle Clean Solutions (Home Cleaning) - 30 leads

Total: 150 realistic leads with proper responses, tracking data, and outcomes.
"""

import uuid
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from client_personas import ALL_CLIENT_DATA

def generate_client_leads(client_name: str, num_leads: int = 30) -> str:
    """Generate SQL for lead sessions for a specific client."""
    
    client_data = ALL_CLIENT_DATA[client_name]
    personas = client_data['personas']
    questions = client_data['questions']
    client_id = client_data['client_id']
    form_id = client_data['form_id']
    
    sql_statements = []
    
    for i in range(num_leads):
        # Use personas cyclically and add variations
        base_persona = personas[i % len(personas)]
        
        # Create variations for each cycle
        variation_suffix = f"_{i // len(personas) + 1}" if i >= len(personas) else ""
        
        # Generate UUIDs
        session_uuid = str(uuid.uuid4())
        tracking_uuid = str(uuid.uuid4())
        outcome_uuid = str(uuid.uuid4())
        
        # Generate session_id string
        session_id = f"{client_name}_{i+1:03d}_{base_persona['lead_type']}"
        
        # Vary timestamps - calculate actual ISO timestamps
        days_ago = random.randint(0, 14)  # Spread over 2 weeks
        hours_ago = random.randint(1, 23)
        start_datetime = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
        complete_datetime = datetime.now() - timedelta(days=days_ago, hours=hours_ago-1, minutes=random.randint(15,45))
        
        start_time = f"'{start_datetime.isoformat()}'"
        complete_time = f"'{complete_datetime.isoformat()}'"
        
        # Vary the persona slightly for each iteration
        varied_name = base_persona['name']
        if variation_suffix:
            name_parts = base_persona['name'].split(' ')
            varied_name = f"{name_parts[0]}{variation_suffix} {name_parts[1]}"
        
        varied_email = base_persona['email']
        if variation_suffix and '@' in varied_email:
            local, domain = varied_email.split('@')
            varied_email = f"{local}{variation_suffix}@{domain}"
        
        # Generate lead session
        completed = 'true' if base_persona['lead_type'] != 'abandoned' else 'false'
        steps = random.randint(6, len(questions)) if base_persona['lead_type'] != 'abandoned' else random.randint(2, 4)
        
        completion_msg = get_completion_message(base_persona['lead_type'], client_name)
        
        # Map lead types to database values
        lead_status_mapping = {
            'qualified': 'yes',
            'maybe': 'maybe',
            'unqualified': 'no',
            'abandoned': 'unknown'
        }
        db_lead_status = lead_status_mapping.get(base_persona['lead_type'], 'unknown')
        
        sql_statements.append(f"""
-- Lead {i+1}: {base_persona['lead_type'].title()} - {varied_name} ({client_name.upper()})
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('{session_uuid}', '{form_id}', '{session_id}', '{client_id}', {start_time}, {complete_time}, {complete_time if base_persona['lead_type'] != 'abandoned' else 'NULL'}, {steps}, {completed}, {base_persona['score']}, {base_persona['score']}, '{db_lead_status}', 'qualified', '{completion_msg}', 'active', '{get_user_agent(base_persona.get('device', 'desktop'))}', '{get_ip_address()}', '{{"device_type": "{base_persona.get('device', 'desktop')}", "completion_time": {random.randint(10, 60)}}}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('{tracking_uuid}', '{session_uuid}', '{base_persona.get('utm_source', 'google')}', '{get_utm_medium(base_persona.get('utm_source', 'google'))}', '{base_persona.get('utm_campaign', f'{client_name}_general')}', '{get_utm_term(client_name)}', '{base_persona.get('device', 'desktop')}', '{get_browser(base_persona.get('device', 'desktop'))}', 'United States', 'Massachusetts', '{get_city()}');
""")
        
        # Generate responses for completed sessions
        if base_persona['lead_type'] != 'abandoned':
            response_sqls = []
            for q_num, field in questions.items():
                if field in base_persona and base_persona[field] is not None:
                    response_uuid = str(uuid.uuid4())
                    answer = base_persona[field]
                    if field == 'name':
                        answer = varied_name
                    elif field == 'email':
                        answer = varied_email
                    
                    # Escape single quotes in answer for SQL
                    escaped_answer = str(answer).replace("'", "''")
                    answer_data = json.dumps({field: answer}).replace("'", "''")
                    score = get_question_score(field, answer, client_name)
                    
                    response_sqls.append(f"('{response_uuid}', '{session_uuid}', '{form_id}', {q_num}, '{escaped_answer}', '{answer_data}', {score}, {start_time})")
            
            if response_sqls:
                sql_statements.append(f"""
INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
{',\n'.join(response_sqls)};
""")
        
        # Generate lead outcome for completed sessions (not abandoned)
        if base_persona['lead_type'] != 'abandoned':
            contact_info = {}
            if 'name' in base_persona:
                contact_info['name'] = varied_name
            if 'email' in base_persona:
                contact_info['email'] = varied_email
            if base_persona.get('phone'):
                contact_info['phone'] = base_persona['phone']
            
            # lead_outcomes mapping - abandoned gets None (no record created)
            final_status = None if base_persona['lead_type'] == 'abandoned' else base_persona['lead_type']
            
            if final_status:  # Only create outcome record if not abandoned
                sql_statements.append(f"""
INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent, converted, conversion_date, conversion_value, conversion_type) 
VALUES ('{outcome_uuid}', '{session_uuid}', '{client_id}', '{form_id}', '{final_status}', '{json.dumps(contact_info)}', {base_persona['score']}, {base_persona['score']/100:.2f}, {str(base_persona['lead_type'] != 'unqualified').lower()}, false, NULL, NULL, NULL);
""")
    
    return '\n'.join(sql_statements)

def get_completion_message(lead_type: str, client_name: str) -> str:
    """Generate client-specific completion messages."""
    
    client_messages = {
        'pawsome': {
            'qualified': "Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.",
            'maybe': "Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.",
            'unqualified': "Thank you for your interest. We may not be the best fit, but please reach out if your needs change.",
            'abandoned': ''
        },
        'metro_realty': {
            'qualified': "Excellent! Based on your responses, you are an ideal client for our real estate services. We will connect you with a specialist agent within 24 hours.",
            'maybe': "Thank you for your interest! We are reviewing your requirements to match you with the right agent. Expect to hear from us within 2-3 days.",
            'unqualified': "Thank you for your interest. While we may not be the best fit for your current needs, please reach out if your situation changes.",
            'abandoned': ''
        },
        'techsolve': {
            'qualified': "Perfect! Your technology challenges align well with our expertise. Our senior consultant will reach out within 24 hours to discuss your project.",
            'maybe': "Thanks for your inquiry! We are evaluating how we can best support your technology needs. Our team will be in touch within a few days.",
            'unqualified': "Thank you for considering TechSolve. While your current requirements may not align with our services, feel free to contact us in the future.",
            'abandoned': ''
        },
        'fitlife': {
            'qualified': "Great news! You are an excellent candidate for our personal training programs. We will contact you within 24 hours to schedule your consultation.",
            'maybe': "Thank you for your interest in FitLife! We are reviewing your fitness goals to create the best training plan. Expect to hear from us soon.",
            'unqualified': "Thank you for considering FitLife. While our current programs may not be the right fit, we wish you success in your fitness journey.",
            'abandoned': ''
        },
        'sparkle_clean': {
            'qualified': "Perfect! Your cleaning needs match our services perfectly. We will contact you within 24 hours to schedule your first appointment.",
            'maybe': "Thank you for your interest! We are reviewing your requirements to provide the best cleaning solution. We will be in touch soon.",
            'unqualified': "Thank you for considering Sparkle Clean. While we may not be able to accommodate your specific needs, feel free to reach out in the future.",
            'abandoned': ''
        }
    }
    
    return client_messages.get(client_name, {}).get(lead_type, '').replace("'", "''")

def get_utm_medium(source: str) -> str:
    """Map UTM source to appropriate medium."""
    mapping = {
        'google': 'cpc',
        'facebook': 'social',
        'instagram': 'social',
        'linkedin': 'social',
        'yelp': 'referral',
        'referral': 'referral',
        'organic': 'search',
        'email': 'email'
    }
    return mapping.get(source, 'referral')

def get_utm_term(client_name: str) -> str:
    """Generate client-appropriate search terms."""
    terms = {
        'pawsome': [
            'dog walker near me',
            'professional dog walking',
            'pet walking services',
            'dog walking cambridge',
            'local dog walker'
        ],
        'metro_realty': [
            'boston realtor',
            'cambridge real estate',
            'home buying agent',
            'property specialist',
            'real estate expert'
        ],
        'techsolve': [
            'IT consulting boston',
            'technology solutions',
            'digital transformation',
            'software consulting',
            'tech support services'
        ],
        'fitlife': [
            'personal trainer boston',
            'fitness coach',
            'weight loss trainer',
            'strength training',
            'personal fitness'
        ],
        'sparkle_clean': [
            'house cleaning service',
            'professional cleaners',
            'home cleaning boston',
            'cleaning service cambridge',
            'residential cleaning'
        ]
    }
    return random.choice(terms.get(client_name, ['general search']))

def get_city() -> str:
    """Generate realistic Boston metro area cities."""
    cities = ['Cambridge', 'Somerville', 'Arlington', 'Medford', 'Boston', 'Brookline', 'Newton', 'Lexington']
    return random.choice(cities)

def get_user_agent(device: str) -> str:
    """Generate realistic user agent strings."""
    agents = {
        'desktop': [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ],
        'mobile': [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0',
            'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
        ]
    }
    return random.choice(agents.get(device, agents['desktop']))

def get_browser(device: str) -> str:
    """Generate realistic browser names."""
    browsers = {
        'desktop': ['Chrome', 'Firefox', 'Safari', 'Edge'],
        'mobile': ['Safari', 'Chrome', 'Firefox']
    }
    return random.choice(browsers.get(device, browsers['desktop']))

def get_ip_address() -> str:
    """Generate realistic IP addresses."""
    return f"192.168.1.{random.randint(10, 250)}"

def get_question_score(field: str, answer: str, client_name: str) -> int:
    """Score responses based on field type and answer for specific client."""
    
    # Base scores for common fields
    base_scores = {
        'name': 10,
        'email': 10,
        'phone': 15
    }
    
    if field in base_scores:
        return base_scores[field]
    
    # Client-specific scoring
    client_scoring = {
        'pawsome': {
            'dog_breed': {'German Shepherd': 20, 'Golden Retriever': 20, 'Labrador': 15, 'Beagle': 15, 'Lab Mix': 10, 'Pit Bull Mix': 5},
            'behavior': {'very_well': 25, 'mostly_well': 15, 'rarely': -10},
            'walks_per_week': {'5_plus': 25, '3_4': 20, '2': 10, '1': 5},
            'budget': {'25_35': 25, '20_30': 20, '15_25': 15, 'under_15': 0}
        },
        'metro_realty': {
            'buy_or_sell': {'both': 25, 'sell': 20, 'buy': 15},
            'timeline': {'within_3_months': 25, '3_6_months': 20, '6_12_months': 10, 'just_browsing': 0},
            'price_range': {'$500k_plus': 20, '$300k_500k': 25, '$200k_300k': 15, 'under_200k': 5},
            'mortgage_status': {'cash': 25, 'pre_approved': 20, 'in_process': 15, 'planning_to_get': 10}
        },
        'techsolve': {
            'company_size': {'50_200_employees': 25, '10_50_employees': 20, 'under_10': 10},
            'budget_range': {'$100k_plus': 25, '$50k_100k': 20, '$25k_50k': 15, 'under_25k': 5},
            'timeline': {'within_3_months': 25, '3_6_months': 20, '6_12_months': 10, 'just_exploring': 0},
            'decision_maker': {'yes': 20, 'shared': 15, 'no': 5}
        },
        'fitlife': {
            'budget': {'$150_200': 25, '$100_150': 20, '$75_100': 15, 'under_75': 5},
            'timeline': {'asap': 25, 'within_month': 20, 'within_3_months': 10, 'just_exploring': 0},
            'commitment_level': {'4_sessions_week': 25, '3_sessions_week': 20, '2_sessions_week': 15, '1_session_week': 5},
            'motivation_level': {'very_motivated': 20, 'motivated': 15, 'somewhat_motivated': 10}
        },
        'sparkle_clean': {
            'budget': {'$150_plus': 25, '$100_150': 20, '$75_100': 15, 'under_75': 5},
            'frequency': {'weekly': 25, 'bi_weekly': 20, 'monthly': 15, 'one_time': 10},
            'timeline': {'within_week': 25, 'within_month': 20, 'within_3_months': 10, 'just_exploring': 0},
            'home_size': {'large_4plus_bed': 20, 'medium_2_3_bed': 15, 'small_1_bed': 10}
        }
    }
    
    client_scores = client_scoring.get(client_name, {})
    if field in client_scores:
        if isinstance(client_scores[field], dict):
            return client_scores[field].get(answer, 10)
        return client_scores[field]
    
    return 10  # Default score

def generate_all_clients_sql() -> str:
    """Generate SQL for all 5 clients."""
    all_sql = []
    
    # Header comment
    all_sql.append("""-- Comprehensive Test Data for Dynamic Surveys Platform
-- Generated realistic lead sessions for all 5 business clients
-- Total: 150 leads (30 per client) with complete tracking and outcomes
--
-- Clients included:
-- 1. Pawsome Dog Walking (Pet Services)
-- 2. Metro Realty Group (Real Estate) 
-- 3. TechSolve Consulting (Software Consulting)
-- 4. FitLife Personal Training (Health & Fitness)
-- 5. Sparkle Clean Solutions (Home Cleaning)

""")
    
    client_names = ['pawsome', 'metro_realty', 'techsolve', 'fitlife', 'sparkle_clean']
    
    for client_name in client_names:
        all_sql.append(f"""
-- ============================================================
-- {client_name.upper().replace('_', ' ')} CLIENT DATA (30 LEADS)
-- ============================================================
""")
        client_sql = generate_client_leads(client_name, 30)
        all_sql.append(client_sql)
    
    all_sql.append("""
-- ============================================================
-- DATA GENERATION COMPLETE
-- ============================================================
SELECT 'Generated 150 realistic lead sessions across 5 clients!' as status;
""")
    
    return '\n'.join(all_sql)

if __name__ == "__main__":
    print("-- Generating comprehensive test data for all clients...")
    print()
    
    sql = generate_all_clients_sql()
    print(sql)