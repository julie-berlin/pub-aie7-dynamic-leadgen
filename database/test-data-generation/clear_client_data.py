#!/usr/bin/env python3
"""
Clear test data for a specific client
Usage: python3 clear_client_data.py <client_name>
"""

import sys
from client_personas import ALL_CLIENT_DATA

def generate_clear_sql(client_name: str) -> str:
    """Generate SQL to clear all data for a specific client."""
    
    if client_name not in ALL_CLIENT_DATA:
        raise ValueError(f"Unknown client: {client_name}. Available: {list(ALL_CLIENT_DATA.keys())}")
    
    client_data = ALL_CLIENT_DATA[client_name]
    client_id = client_data['client_id']
    form_id = client_data['form_id']
    
    business_names = {
        'pawsome': 'Pawsome Dog Walking',
        'metro_realty': 'Metro Realty Group', 
        'techsolve': 'TechSolve Consulting',
        'fitlife': 'FitLife Personal Training',
        'sparkle_clean': 'Sparkle Clean Solutions'
    }
    
    business_name = business_names.get(client_name, client_name.upper())
    
    return f"""-- Clear existing test data for {business_name}
-- Client ID: {client_id}
-- Form ID: {form_id}

-- Delete in correct order to respect foreign key constraints

-- 1. Delete lead outcomes first (references sessions)
DELETE FROM lead_outcomes 
WHERE client_id = '{client_id}' 
   OR form_id = '{form_id}';

-- 2. Delete responses (references sessions and forms)
DELETE FROM responses 
WHERE form_id = '{form_id}';

-- 3. Delete tracking data (references sessions)
DELETE FROM tracking_data 
WHERE session_id IN (
    SELECT id FROM lead_sessions 
    WHERE client_id = '{client_id}' 
       OR form_id = '{form_id}'
);

-- 4. Delete session snapshots (references sessions)
DELETE FROM session_snapshots 
WHERE session_id IN (
    SELECT id FROM lead_sessions 
    WHERE client_id = '{client_id}' 
       OR form_id = '{form_id}'
);

-- 5. Finally delete lead sessions
DELETE FROM lead_sessions 
WHERE client_id = '{client_id}' 
   OR form_id = '{form_id}';

SELECT 'Cleared all existing {business_name} test data!' as status;
"""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 clear_client_data.py <client_name>")
        print("Available clients:", list(ALL_CLIENT_DATA.keys()))
        sys.exit(1)
    
    client_name = sys.argv[1]
    
    try:
        print(generate_clear_sql(client_name))
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)