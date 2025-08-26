-- Clear existing test data for Pawsome Dog Walking
-- Client ID: a1111111-1111-1111-1111-111111111111
-- Form ID: f1111111-1111-1111-1111-111111111111

-- Delete in correct order to respect foreign key constraints

-- 1. Delete lead outcomes first (references sessions)
DELETE FROM lead_outcomes 
WHERE client_id = 'a1111111-1111-1111-1111-111111111111' 
   OR form_id = 'f1111111-1111-1111-1111-111111111111';

-- 2. Delete responses (references sessions and forms)
DELETE FROM responses 
WHERE form_id = 'f1111111-1111-1111-1111-111111111111';

-- 3. Delete tracking data (references sessions)
DELETE FROM tracking_data 
WHERE session_id IN (
    SELECT id FROM lead_sessions 
    WHERE client_id = 'a1111111-1111-1111-1111-111111111111' 
       OR form_id = 'f1111111-1111-1111-1111-111111111111'
);

-- 4. Delete session snapshots (references sessions)
DELETE FROM session_snapshots 
WHERE session_id IN (
    SELECT id FROM lead_sessions 
    WHERE client_id = 'a1111111-1111-1111-1111-111111111111' 
       OR form_id = 'f1111111-1111-1111-1111-111111111111'
);

-- 5. Finally delete lead sessions
DELETE FROM lead_sessions 
WHERE client_id = 'a1111111-1111-1111-1111-111111111111' 
   OR form_id = 'f1111111-1111-1111-1111-111111111111';

SELECT 'Cleared all existing Pawsome test data!' as status;