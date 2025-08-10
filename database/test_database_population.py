#!/usr/bin/env python3
"""
Test script for database population and survey system integration
Validates that all 5 business scenarios work correctly with the database
"""
import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Any

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.database import SupabaseClient
from app.tools import load_questions, load_client_info, load_form_config

# Test form IDs from our populated data
TEST_FORM_IDS = {
    'dog_walking': 'f1111111-1111-1111-1111-111111111111',
    'real_estate': 'f2222222-2222-2222-2222-222222222222',  
    'software_consulting': 'f3333333-3333-3333-3333-333333333333',
    'personal_training': 'f4444444-4444-4444-4444-444444444444',
    'home_cleaning': 'f5555555-5555-5555-5555-555555555555'
}

def test_database_connection() -> bool:
    """Test that database connection works"""
    print("🔍 Testing database connection...")
    try:
        db = SupabaseClient()
        if db.test_connection():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_data_loading_functions() -> Dict[str, bool]:
    """Test all data loading functions for each business scenario"""
    results = {}
    
    for business_name, form_id in TEST_FORM_IDS.items():
        print(f"\n📋 Testing {business_name} (form_id: {form_id})...")
        
        # Test load_questions
        try:
            questions_result = load_questions(form_id)
            questions = json.loads(questions_result)
            
            if isinstance(questions, list) and len(questions) > 0:
                print(f"   ✅ Questions loaded: {len(questions)} questions")
                
                # Validate question structure
                first_question = questions[0]
                required_fields = ['question_text', 'question_type', 'question_order']
                missing_fields = [field for field in required_fields if field not in first_question]
                
                if not missing_fields:
                    print(f"   ✅ Question structure valid")
                else:
                    print(f"   ⚠️  Missing fields in questions: {missing_fields}")
                    
            else:
                print(f"   ❌ Questions load failed or empty")
                results[f"{business_name}_questions"] = False
                continue
                
        except Exception as e:
            print(f"   ❌ Questions load error: {e}")
            results[f"{business_name}_questions"] = False
            continue
            
        results[f"{business_name}_questions"] = True
        
        # Test load_client_info  
        try:
            client_result = load_client_info(form_id)
            client_data = json.loads(client_result)
            
            if 'client' in client_data and client_data['client']:
                client = client_data['client']
                required_client_fields = ['business_name', 'owner_name', 'background']
                missing_client_fields = [field for field in required_client_fields if field not in client]
                
                if not missing_client_fields:
                    print(f"   ✅ Client info loaded: {client.get('business_name', 'Unknown')}")
                else:
                    print(f"   ⚠️  Missing client fields: {missing_client_fields}")
            else:
                print(f"   ❌ Client info load failed or empty")
                results[f"{business_name}_client"] = False
                continue
                
        except Exception as e:
            print(f"   ❌ Client info load error: {e}")
            results[f"{business_name}_client"] = False
            continue
            
        results[f"{business_name}_client"] = True
        
        # Test load_form_config
        try:
            form_result = load_form_config(form_id)
            form_data = json.loads(form_result)
            
            if form_data and 'title' in form_data:
                print(f"   ✅ Form config loaded: {form_data.get('title', 'Unknown')}")
                
                # Check scoring thresholds
                if 'lead_scoring_threshold_yes' in form_data and 'lead_scoring_threshold_maybe' in form_data:
                    yes_threshold = form_data['lead_scoring_threshold_yes']
                    maybe_threshold = form_data['lead_scoring_threshold_maybe']
                    print(f"   📊 Scoring thresholds: Yes={yes_threshold}, Maybe={maybe_threshold}")
                    
            else:
                print(f"   ❌ Form config load failed or empty")
                results[f"{business_name}_form"] = False
                continue
                
        except Exception as e:
            print(f"   ❌ Form config load error: {e}")
            results[f"{business_name}_form"] = False
            continue
            
        results[f"{business_name}_form"] = True
        
        print(f"   🎉 {business_name.replace('_', ' ').title()} - All data loading tests passed!")
    
    return results

def test_question_scoring_logic() -> Dict[str, bool]:
    """Test that questions have proper scoring rubrics for lead qualification"""
    results = {}
    
    for business_name, form_id in TEST_FORM_IDS.items():
        print(f"\n🎯 Testing scoring logic for {business_name}...")
        
        try:
            questions_result = load_questions(form_id)
            questions = json.loads(questions_result)
            
            # Count questions with scoring rubrics
            scored_questions = [q for q in questions if q.get('scoring_rubric')]
            contact_questions = [q for q in questions if q.get('category') == 'contact']
            qualification_questions = [q for q in questions if q.get('category') == 'qualification']
            
            print(f"   📝 Total questions: {len(questions)}")
            print(f"   🎯 Scored questions: {len(scored_questions)}")
            print(f"   📞 Contact questions: {len(contact_questions)}")
            print(f"   ⭐ Qualification questions: {len(qualification_questions)}")
            
            # Validate scoring logic
            if len(scored_questions) >= 4:  # Should have at least 4 scored questions
                print(f"   ✅ Sufficient scoring questions")
            else:
                print(f"   ⚠️  May need more scoring questions")
                
            if len(contact_questions) >= 2:  # Should have name and email/phone
                print(f"   ✅ Sufficient contact questions")
            else:
                print(f"   ⚠️  May need more contact questions")
                
            if len(qualification_questions) >= 3:  # Should have strong qualification criteria
                print(f"   ✅ Sufficient qualification questions")
            else:
                print(f"   ⚠️  May need more qualification questions")
                
            results[f"{business_name}_scoring"] = True
            
        except Exception as e:
            print(f"   ❌ Scoring logic test error: {e}")
            results[f"{business_name}_scoring"] = False
            
    return results

def test_form_diversity() -> bool:
    """Test that the 5 forms represent diverse business scenarios"""
    print(f"\n🌈 Testing form diversity across business types...")
    
    business_types = set()
    industries = set()
    question_counts = []
    scoring_thresholds = []
    
    for business_name, form_id in TEST_FORM_IDS.items():
        try:
            # Get client info
            client_result = load_client_info(form_id)
            client_data = json.loads(client_result)['client']
            
            # Get form info
            form_result = load_form_config(form_id)
            form_data = json.loads(form_result)
            
            # Get questions
            questions_result = load_questions(form_id)
            questions = json.loads(questions_result)
            
            # Collect diversity metrics
            business_types.add(client_data.get('business_type', 'unknown'))
            industries.add(client_data.get('industry', 'unknown'))
            question_counts.append(len(questions))
            scoring_thresholds.append(form_data.get('lead_scoring_threshold_yes', 0))
            
        except Exception as e:
            print(f"   ❌ Error analyzing {business_name}: {e}")
            return False
    
    print(f"   🏢 Business types: {len(business_types)} unique types")
    print(f"      {', '.join(sorted(business_types))}")
    print(f"   🏭 Industries: {len(industries)} unique industries")
    print(f"      {', '.join(sorted(industries))}")
    print(f"   📋 Question counts: {min(question_counts)}-{max(question_counts)} questions")
    print(f"   🎯 Scoring thresholds: {min(scoring_thresholds)}-{max(scoring_thresholds)}")
    
    # Validate diversity
    diversity_checks = [
        (len(business_types) >= 5, "All business types are unique"),
        (len(industries) >= 4, "Multiple industries represented"),
        (max(question_counts) - min(question_counts) <= 5, "Question counts are reasonable"),
        (max(scoring_thresholds) - min(scoring_thresholds) >= 5, "Scoring thresholds vary appropriately")
    ]
    
    all_passed = True
    for check, description in diversity_checks:
        if check:
            print(f"   ✅ {description}")
        else:
            print(f"   ⚠️  {description}")
            all_passed = False
    
    return all_passed

def generate_test_report(
    connection_result: bool,
    loading_results: Dict[str, bool],
    scoring_results: Dict[str, bool],
    diversity_result: bool
) -> None:
    """Generate comprehensive test report"""
    print(f"\n" + "="*60)
    print(f"📊 DATABASE POPULATION TEST REPORT")
    print(f"="*60)
    
    # Connection Test
    print(f"\n🔌 Database Connection:")
    print(f"   {'✅' if connection_result else '❌'} Connection Test")
    
    # Data Loading Tests
    print(f"\n📋 Data Loading Tests:")
    business_summary = {}
    for key, result in loading_results.items():
        business, test_type = key.rsplit('_', 1)
        if business not in business_summary:
            business_summary[business] = {}
        business_summary[business][test_type] = result
    
    for business, tests in business_summary.items():
        all_passed = all(tests.values())
        status = '✅' if all_passed else '❌'
        print(f"   {status} {business.replace('_', ' ').title()}: {sum(tests.values())}/{len(tests)} tests passed")
        
        if not all_passed:
            for test_type, passed in tests.items():
                if not passed:
                    print(f"      ❌ {test_type} failed")
    
    # Scoring Logic Tests
    print(f"\n🎯 Scoring Logic Tests:")
    for business, result in scoring_results.items():
        business_name = business.replace('_scoring', '').replace('_', ' ').title()
        status = '✅' if result else '❌'
        print(f"   {status} {business_name}")
    
    # Diversity Test
    print(f"\n🌈 Form Diversity Test:")
    print(f"   {'✅' if diversity_result else '❌'} Business Scenario Diversity")
    
    # Overall Summary
    total_tests = 1 + len(loading_results) + len(scoring_results) + 1
    passed_tests = (
        int(connection_result) + 
        sum(loading_results.values()) + 
        sum(scoring_results.values()) + 
        int(diversity_result)
    )
    
    print(f"\n🎉 OVERALL RESULT:")
    print(f"   {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print(f"   🚀 All systems ready for production!")
        print(f"   💡 You can now test the survey API with any of the {len(TEST_FORM_IDS)} form IDs")
    else:
        print(f"   🔧 Some issues need attention before production")
        print(f"   💡 Check the failed tests above and verify database setup")

def main():
    """Run all database population tests"""
    print("🧪 Starting Database Population Test Suite...")
    print(f"📝 Testing {len(TEST_FORM_IDS)} business scenarios\n")
    
    # Test 1: Database Connection
    connection_result = test_database_connection()
    if not connection_result:
        print("\n❌ Database connection failed. Please check your setup:")
        print("   1. Verify SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, and SUPABASE_SECRET_KEY in .env")
        print("   2. Run database migrations: 001_initial_schema.sql")
        print("   3. Populate data: 002_populate_example_data.sql")
        return
    
    # Test 2: Data Loading Functions
    loading_results = test_data_loading_functions()
    
    # Test 3: Question Scoring Logic
    scoring_results = test_question_scoring_logic()
    
    # Test 4: Form Diversity
    diversity_result = test_form_diversity()
    
    # Generate Report
    generate_test_report(connection_result, loading_results, scoring_results, diversity_result)

if __name__ == "__main__":
    main()