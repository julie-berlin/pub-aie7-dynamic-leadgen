#!/usr/bin/env python3
"""
Generate realistic lead sessions for demo purposes
"""

import uuid
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Client IDs from the database
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

# Pawsome Dog Walking personas and responses
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
        'phone': None,  # No phone provided
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

# Question mapping for Pawsome Dog Walking
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

def generate_lead_session(client_name: str, persona: Dict, num_leads: int = 30):
    """Generate SQL for lead sessions"""
    
    client_id = CLIENT_IDS[client_name]
    form_id = FORM_IDS[client_name]
    
    sql_statements = []
    
    for i in range(num_leads):
        # Use the personas cyclically and add variations
        base_persona = PAWSOME_PERSONAS[i % len(PAWSOME_PERSONAS)]
        
        # Create variations for each cycle
        variation_suffix = f"_{i // len(PAWSOME_PERSONAS) + 1}" if i >= len(PAWSOME_PERSONAS) else ""
        
        # Generate UUIDs
        session_uuid = str(uuid.uuid4())
        tracking_uuid = str(uuid.uuid4()) 
        outcome_uuid = str(uuid.uuid4())
        
        # Generate session_id string
        session_id = f"sess_{i+1:03d}_{base_persona['lead_type']}"
        
        # Vary timestamps - calculate actual ISO timestamps
        days_ago = random.randint(0, 7)
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
        completion_status = 'completed' if base_persona['lead_type'] != 'abandoned' else 'NULL'
        completed = 'true' if base_persona['lead_type'] != 'abandoned' else 'false'
        steps = random.randint(6, 9) if base_persona['lead_type'] != 'abandoned' else random.randint(2, 4)
        
        completion_msg = get_completion_message(base_persona['lead_type'])
        
        # Map lead types to database values
        lead_status_mapping = {
            'qualified': 'yes',
            'maybe': 'maybe', 
            'unqualified': 'no',
            'abandoned': 'unknown'
        }
        db_lead_status = lead_status_mapping.get(base_persona['lead_type'], 'unknown')
        
        sql_statements.append(f"""
-- Lead {i+1}: {base_persona['lead_type'].title()} - {varied_name}
INSERT INTO lead_sessions (id, form_id, session_id, client_id, started_at, last_updated, completed_at, step, completed, current_score, final_score, lead_status, completion_type, completion_message, abandonment_status, user_agent, ip_address, metadata) 
VALUES ('{session_uuid}', '{form_id}', '{session_id}', '{client_id}', {start_time}, {complete_time}, {complete_time if base_persona['lead_type'] != 'abandoned' else 'NULL'}, {steps}, {completed}, {base_persona['score']}, {base_persona['score']}, '{db_lead_status}', 'qualified', '{completion_msg}', 'active', '{get_user_agent(base_persona.get('device', 'desktop'))}', '{get_ip_address()}', '{{"device_type": "{base_persona.get('device', 'desktop')}", "completion_time": {random.randint(10, 60)}}}');

INSERT INTO tracking_data (id, session_id, utm_source, utm_medium, utm_campaign, utm_term, device_type, browser_name, country, region, city) 
VALUES ('{tracking_uuid}', '{session_uuid}', '{base_persona.get('utm_source', 'google')}', '{get_utm_medium(base_persona.get('utm_source', 'google'))}', '{base_persona.get('utm_campaign', 'dog_walking_general')}', '{get_utm_term(base_persona)}', '{base_persona.get('device', 'desktop')}', '{get_browser(base_persona.get('device', 'desktop'))}', 'United States', 'Massachusetts', '{get_city()}');
""")
        
        # Generate responses for completed sessions
        if base_persona['lead_type'] != 'abandoned':
            response_sqls = []
            for q_num, field in PAWSOME_QUESTIONS.items():
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
                    score = get_question_score(field, answer)
                    
                    response_sqls.append(f"('{response_uuid}', '{session_uuid}', '{form_id}', {q_num}, '{escaped_answer}', '{answer_data}', {score}, {start_time})")
            
            if response_sqls:
                sql_statements.append(f"""
INSERT INTO responses (id, session_id, form_id, question_id, answer, answer_data, score, created_at) VALUES 
{',\n'.join(response_sqls)};
""")
        
        # Generate lead outcome for completed sessions
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
INSERT INTO lead_outcomes (id, session_id, client_id, form_id, final_status, contact_info, lead_score, confidence_score, notification_sent) 
VALUES ('{outcome_uuid}', '{session_uuid}', '{client_id}', '{form_id}', '{final_status}', '{json.dumps(contact_info)}', {base_persona['score']}, {base_persona['score']/100:.2f}, {str(base_persona['lead_type'] != 'unqualified').lower()});
""")
    
    return '\n'.join(sql_statements)

def get_completion_message(lead_type: str) -> str:
    messages = {
        'qualified': "Thank you for your interest! You seem like a perfect fit for our dog walking services. We will contact you within 24 hours.",
        'maybe': "Thanks for your interest! We may be able to work something out based on your needs. We will be in touch soon.",
        'unqualified': "Thank you for your interest. We may not be the best fit, but please reach out if your needs change.",
        'abandoned': ''
    }
    return messages.get(lead_type, '').replace("'", "''")

def get_utm_medium(source: str) -> str:
    mapping = {
        'google': 'cpc',
        'facebook': 'social', 
        'organic': 'search',
        'email': 'email'
    }
    return mapping.get(source, 'referral')

def get_utm_term(persona: Dict) -> str:
    terms = [
        'dog walker near me',
        'professional dog walking',
        'pet walking services',
        'dog walking cambridge',
        'local dog walker'
    ]
    return random.choice(terms)

def get_city() -> str:
    cities = ['Cambridge', 'Somerville', 'Arlington', 'Medford', 'Boston', 'Brookline']
    return random.choice(cities)

def get_user_agent(device: str) -> str:
    agents = {
        'desktop': [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        ],
        'mobile': [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Android 12; Mobile; rv:104.0) Gecko/104.0'
        ]
    }
    return random.choice(agents.get(device, agents['desktop']))

def get_browser(device: str) -> str:
    browsers = {
        'desktop': ['Chrome', 'Firefox', 'Safari', 'Edge'],
        'mobile': ['Safari', 'Chrome', 'Firefox']
    }
    return random.choice(browsers.get(device, browsers['desktop']))

def get_ip_address() -> str:
    return f"192.168.1.{random.randint(10, 250)}"

def get_question_score(field: str, answer: str) -> int:
    """Score responses based on field type and answer"""
    scores = {
        'name': 10,
        'email': 10,
        'phone': 15,
        'dog_breed': {'German Shepherd': 20, 'Golden Retriever': 20, 'Labrador': 15, 'Beagle': 15, 'Lab Mix': 10, 'Pit Bull Mix': 5},
        'dog_age': 15,
        'behavior': {'very_well': 25, 'mostly_well': 15, 'rarely': -10},
        'walks_per_week': {'5_plus': 25, '3_4': 20, '2': 10, '1': 5},
        'address': 20,
        'budget': {'25_35': 25, '20_30': 20, '15_25': 15, 'under_15': 0}
    }
    
    if field in scores:
        if isinstance(scores[field], dict):
            return scores[field].get(answer, 10)
        return scores[field]
    return 10

if __name__ == "__main__":
    print("-- Generated realistic lead sessions for Pawsome Dog Walking")
    print("-- Run this script to generate 30 diverse leads")
    print()
    
    sql = generate_lead_session('pawsome', PAWSOME_PERSONAS, 30)
    print(sql)
    
    print()
    print("SELECT 'Generated 30 realistic lead sessions!' as status;")