#!/usr/bin/env python3
"""
Test script to verify that question tracking is working correctly.
This tests the fix for the recurring question repetition bug.

Usage:
    python test_question_tracking.py
"""

import requests
import json
import time
from typing import List, Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
FORM_ID = "f1111111-1111-1111-1111-111111111111"  # Pawsome Dog Walking

def test_question_tracking():
    """Test that questions don't repeat across multiple submissions."""
    
    print("=" * 60)
    print("QUESTION TRACKING TEST")
    print("=" * 60)
    
    # Track all question IDs we've seen
    all_seen_questions: List[int] = []
    session_cookies = None
    
    # Step 1: Start a new session
    print("\n1. Starting new session...")
    response = requests.post(
        f"{BASE_URL}/api/survey/start",
        json={
            "form_id": FORM_ID,
            "utm_source": "test",
            "utm_campaign": "question_tracking_test"
        }
    )
    
    if response.status_code != 200:
        print(f"❌ Failed to start session: {response.status_code}")
        print(response.text)
        return False
    
    session_cookies = response.cookies
    data = response.json()['data']
    
    # Check first set of questions
    first_questions = data['step']['questions']
    first_question_ids = [q.get('id') for q in first_questions if q.get('id') is not None]
    
    print(f"✅ Session started")
    print(f"   Questions received: {len(first_questions)}")
    print(f"   Question IDs: {first_question_ids}")
    
    if not first_question_ids:
        print("❌ ERROR: Questions don't have IDs!")
        return False
    
    all_seen_questions.extend(first_question_ids)
    
    # Step 2: Submit responses to first set
    print("\n2. Submitting responses to first set...")
    responses = []
    for q in first_questions:
        if q.get('id'):
            responses.append({
                "question_id": q['id'],
                "answer": "Test answer for question " + str(q['id'])
            })
    
    response = requests.post(
        f"{BASE_URL}/api/survey/step",
        json={"responses": responses},
        cookies=session_cookies
    )
    
    if response.status_code != 200:
        print(f"❌ Failed to submit responses: {response.status_code}")
        print(response.text)
        return False
    
    data = response.json()['data']
    
    # Check if complete or got more questions
    if data.get('isComplete'):
        print("✅ Form completed after first submission")
        return True
    
    # Check second set of questions
    second_questions = data['nextStep']['questions']
    second_question_ids = [q.get('id') for q in second_questions if q.get('id') is not None]
    
    print(f"✅ Responses submitted")
    print(f"   Questions received: {len(second_questions)}")
    print(f"   Question IDs: {second_question_ids}")
    
    # CRITICAL CHECK: No questions should repeat
    repeated_questions = set(second_question_ids) & set(first_question_ids)
    if repeated_questions:
        print(f"\n❌ ERROR: Questions are repeating!")
        print(f"   Repeated question IDs: {repeated_questions}")
        print(f"   First set had: {first_question_ids}")
        print(f"   Second set has: {second_question_ids}")
        return False
    else:
        print(f"✅ No repeated questions - fix is working!")
    
    all_seen_questions.extend(second_question_ids)
    
    # Step 3: Submit responses to second set
    print("\n3. Submitting responses to second set...")
    responses = []
    for q in second_questions:
        if q.get('id'):
            responses.append({
                "question_id": q['id'],
                "answer": "Test answer for question " + str(q['id'])
            })
    
    response = requests.post(
        f"{BASE_URL}/api/survey/step",
        json={"responses": responses},
        cookies=session_cookies
    )
    
    if response.status_code != 200:
        print(f"❌ Failed to submit responses: {response.status_code}")
        print(response.text)
        return False
    
    data = response.json()['data']
    
    # Check if complete or got more questions
    if data.get('isComplete'):
        print("✅ Form completed after second submission")
        print(f"   Total unique questions asked: {len(set(all_seen_questions))}")
        return True
    
    # Check third set of questions
    third_questions = data['nextStep']['questions']
    third_question_ids = [q.get('id') for q in third_questions if q.get('id') is not None]
    
    print(f"✅ Responses submitted")
    print(f"   Questions received: {len(third_questions)}")
    print(f"   Question IDs: {third_question_ids}")
    
    # CRITICAL CHECK: No questions should repeat from any previous set
    repeated_questions = set(third_question_ids) & set(all_seen_questions)
    if repeated_questions:
        print(f"\n❌ ERROR: Questions are repeating!")
        print(f"   Repeated question IDs: {repeated_questions}")
        print(f"   All previous questions: {all_seen_questions}")
        print(f"   Third set has: {third_question_ids}")
        return False
    else:
        print(f"✅ No repeated questions across all sets - fix is working!")
    
    print(f"\n✅ TEST PASSED: Question tracking is working correctly")
    print(f"   Total unique questions shown: {len(set(all_seen_questions + third_question_ids))}")
    
    return True

def check_logs():
    """Check backend logs for tracking messages."""
    print("\n" + "=" * 60)
    print("LOG CHECK")
    print("=" * 60)
    print("\nTo verify the fix is working, check backend logs for:")
    print("  🔥 QUESTION TRACKING: Already asked question IDs: [...]")
    print("  🔥 QUESTION TRACKING: Added question ID X to asked_questions")
    print("  🔥 QUESTION TRACKING: Loaded X available questions")
    print("\nRun: docker-compose logs backend | grep '🔥 QUESTION TRACKING'")

if __name__ == "__main__":
    try:
        success = test_question_tracking()
        check_logs()
        
        if success:
            print("\n✅ All tests passed!")
            exit(0)
        else:
            print("\n❌ Tests failed - question repetition bug may have returned")
            exit(1)
            
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)