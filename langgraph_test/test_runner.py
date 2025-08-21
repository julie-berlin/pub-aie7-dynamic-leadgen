#!/usr/bin/env python3
"""Test runner for LangGraph survey flow with tool integration."""

import os
import sys
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import graph components
from graph.simplified_survey_graph import run_survey_sync
from database.sqlite_db import db

class SurveyTestRunner:
    """Test runner for survey graph."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.test_results = []
        
        # Use unique database for this test run to avoid conflicts
        self.db_name = f"test_survey_{uuid.uuid4().hex[:8]}.db"
        
        # Update database instance to use our unique name
        from database.sqlite_db import SQLiteDatabase
        import database.sqlite_db as db_module
        db_module.db = SQLiteDatabase(self.db_name)
        
        # Copy test data to our unique database
        self._setup_test_database()
    
    def _setup_test_database(self):
        """Setup test database with data."""
        try:
            # Load test data SQL and execute it
            import sqlite3
            from pathlib import Path
            
            sql_file = Path(__file__).parent / "database" / "test_data.sql"
            
            if sql_file.exists():
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                
                with open(sql_file, 'r') as f:
                    sql_content = f.read()
                
                # Execute SQL statements
                for statement in sql_content.split(';'):
                    statement = statement.strip()
                    if statement:
                        try:
                            cursor.execute(statement)
                        except sqlite3.IntegrityError:
                            pass  # Ignore duplicates
                
                conn.commit()
                conn.close()
                print(f"✅ Setup test database: {self.db_name}")
            else:
                print(f"⚠️ Test data file not found: {sql_file}")
                
        except Exception as e:
            print(f"❌ Failed to setup test database: {e}")
    
    def cleanup(self):
        """Clean up test database."""
        try:
            if os.path.exists(self.db_name):
                os.remove(self.db_name)
                print(f"🧹 Cleaned up test database: {self.db_name}")
        except Exception as e:
            print(f"⚠️ Failed to cleanup database: {e}")
    
    def run_test_scenario(self, scenario_name: str, form_id: str, responses: List[Dict]) -> Dict[str, Any]:
        """Run a single test scenario."""
        print(f"\n{'='*60}")
        print(f"🧪 TEST SCENARIO: {scenario_name}")
        print(f"{'='*60}")
        
        # Initialize state
        initial_state = {
            "core": {
                "form_id": form_id,
                "client_id": None
            },
            "pending_responses": []
        }
        
        # Run initial graph to get first questions
        print("\n📋 STEP 1: Starting survey...")
        state = run_survey_sync(initial_state)
        
        step_count = 1
        total_score = 0
        tool_boost = 0
        all_tool_results = []
        
        # Process responses until survey is complete
        max_iterations = 20  # Safety limit
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            step_count += 1
            
            # Get current questions from state
            frontend_response = state.get("frontend_response", {})
            questions = frontend_response.get("questions", [])
            
            if not questions:
                print(f"\n⚠️ No questions available at step {step_count}")
                break
            
            print(f"\n📋 STEP {step_count}: Received {len(questions)} questions")
            
            # Display questions
            for q in questions:
                print(f"   Q{q['id']}: {q['text']}")
            
            # Prepare responses for current questions
            current_responses = []
            for q in questions:
                # Match response by question ID
                answer = self._get_answer_by_question_id(q['id'], responses)
                if answer:
                    current_responses.append({
                        "question_id": q['id'],
                        "question_text": q['text'],
                        "phrased_question": q['text'],
                        "answer": answer,
                        "step": step_count
                    })
                    print(f"   A: {answer}")
                else:
                    print(f"   A: [No answer for Q{q['id']}]")
            
            if not current_responses:
                print("   ⚠️ No responses available for these questions")
                break
            
            # Create a minimal state update with just the new responses
            # Preserve existing state structure but only update pending_responses
            response_state = {
                "core": state.get("core", {}),
                "question_strategy": state.get("question_strategy", {}), 
                "lead_intelligence": state.get("lead_intelligence", {}),
                "pending_responses": current_responses,
                "metadata": state.get("metadata", {}),
                "error_log": state.get("error_log", []),
                "operation_log": state.get("operation_log", [])
            }
            
            # Process responses
            print(f"\n🤖 Processing responses...")
            state = run_survey_sync(response_state)
            
            # Check for tool usage
            if state.get("tool_results"):
                print(f"\n🔧 TOOLS EXECUTED:")
                for tool_name, result in state["tool_results"].items():
                    all_tool_results.append(result)
                    if result.get("success"):
                        print(f"   ✅ {tool_name.upper()}:")
                        if tool_name == "tavily":
                            print(f"      Query: {result.get('query', '')}")
                            print(f"      Score Boost: +{result.get('score_boost', 0)} points")
                            tool_boost += result.get('score_boost', 0)
                        elif tool_name == "maps":
                            print(f"      Distance: {result.get('distance', 'N/A')}")
                            print(f"      In Service Area: {result.get('in_service_area', False)}")
                            print(f"      Score Boost: +{result.get('score_boost', 0)} points")
                            tool_boost += result.get('score_boost', 0)
            
            # Check score
            lead_intel = state.get("lead_intelligence", {})
            current_score = lead_intel.get("current_score", 0)
            if current_score != total_score:
                print(f"\n📊 Score Update: {total_score} → {current_score}")
                total_score = current_score
            
            # Check if complete
            lead_status = state.get("lead_status", "unknown")
            completed = state.get("completed", False)
            route_decision = state.get("route_decision", "continue")
            
            print(f"\n🎯 Current Status: {lead_status.upper()} | Route: {route_decision} | Completed: {completed}")
            
            # Break if survey is complete
            if completed or route_decision == "end":
                print(f"\n🎯 Survey Complete! Final Status: {lead_status.upper()}")
                break
            
            # Continue to next round if route_decision is "continue"
            if route_decision == "continue":
                if lead_status == "unknown":
                    print(f"\n↻ Continuing survey (need more data to classify)...")
                elif lead_status == "maybe":
                    print(f"\n↻ Continuing survey (maybe lead - gathering more info to determine yes/no)...")
                else:
                    print(f"\n↻ Continuing survey ({lead_status} lead)...")
                continue
            else:
                # Safety break
                print(f"\n⚠️ Unexpected state - breaking loop")
                break
        
        # Final results
        print(f"\n{'='*60}")
        print(f"📈 FINAL RESULTS")
        print(f"{'='*60}")
        
        final_score = state.get("lead_intelligence", {}).get("current_score", 0)
        lead_status = state.get("lead_status", "unknown")
        completion_message = state.get("completion_message", "No message generated")
        
        # Get score breakdown
        llm_adjustment = state.get("llm_score_adjustment", 0)
        
        print(f"📊 Final Score: {final_score}/100")
        if tool_boost > 0 or llm_adjustment != 0:
            base_score = final_score - tool_boost - llm_adjustment
            print(f"   - Base Score: {base_score}")
            if tool_boost > 0:
                print(f"   - Tool Boost: +{tool_boost}")
            if llm_adjustment != 0:
                print(f"   - LLM Adjustment: {llm_adjustment:+d}")
                # Show adjustment reason if available
                adjustments = state.get("lead_intelligence", {}).get("last_classification", {}).get("score_adjustments", {})
                if adjustments.get("adjustment_reason"):
                    print(f"     Reason: {adjustments['adjustment_reason']}")
        
        print(f"🎯 Lead Status: {lead_status.upper()}")
        print(f"📝 Steps Taken: {step_count}")
        
        # Display completion message prominently
        print(f"\n{'='*60}")
        print(f"💬 COMPLETION MESSAGE TO USER:")
        print(f"{'='*60}")
        print(f"\n{completion_message}\n")
        print(f"{'='*60}")
        
        # Store results
        result = {
            "scenario": scenario_name,
            "form_id": form_id,
            "steps": step_count,
            "final_score": final_score,
            "base_score": final_score - tool_boost - llm_adjustment,
            "tool_boost": tool_boost,
            "llm_adjustment": llm_adjustment,
            "llm_adjustment_reason": adjustments.get("adjustment_reason", "") if 'adjustments' in locals() else "",
            "lead_status": lead_status,
            "completion_message": completion_message,
            "tool_results": all_tool_results
        }
        
        self.test_results.append(result)
        return result
    
    def _get_answer_by_question_id(self, question_id, all_responses):
        """Get answer for a specific question ID."""
        for response in all_responses:
            if response.get('question_id') == question_id:
                return response.get('answer')
        return None
    
    def run_all_tests(self):
        """Run all test scenarios."""
        
        # Test Scenario 1: High-quality lead with tool validation
        scenario1_responses = [
            {"question_id": 1, "answer": "John Smith"},
            {"question_id": 2, "answer": "john.smith@email.com"},
            {"question_id": 3, "answer": "512-555-1234"},
            {"question_id": 4, "answer": "123 Main St, Downtown Austin, TX"},
            {"question_id": 5, "answer": "2"},
            {"question_id": 6, "answer": "Golden Retriever and Labrador"},
            {"question_id": 7, "answer": "Daily walks needed, 5 days a week"},
            {"question_id": 8, "answer": "Need to start immediately, my work schedule changed"},
            {"question_id": 9, "answer": "$40 per walk is fine"},
            {"question_id": 10, "answer": "The Lab needs gentle handling, he's older"}
        ]
        
        self.run_test_scenario(
            "High-Quality Lead (Downtown Austin)",
            "f1111111-1111-1111-1111-111111111111",
            scenario1_responses
        )
        
        # Test Scenario 2: Maybe lead - far location
        scenario2_responses = [
            {"question_id": 1, "answer": "Mary Johnson"},
            {"question_id": 2, "answer": "mary@email.com"},
            {"question_id": 3, "answer": ""},  # No phone
            {"question_id": 4, "answer": "Round Rock, TX"},  # Far from Austin
            {"question_id": 5, "answer": "1"},
            {"question_id": 6, "answer": "Poodle"},
            {"question_id": 7, "answer": "Maybe 2-3 times per week"},
            {"question_id": 8, "answer": "Next month possibly"},
            {"question_id": 9, "answer": "$25 if possible"},
            {"question_id": 10, "answer": "No special needs"}
        ]
        
        self.run_test_scenario(
            "Maybe Lead (Round Rock - Distance Challenge)",
            "f1111111-1111-1111-1111-111111111111",
            scenario2_responses
        )
        
        # Test Scenario 3: Unqualified lead
        scenario3_responses = [
            {"question_id": 1, "answer": "Bob Wilson"},
            {"question_id": 2, "answer": "bob@test.com"},
            {"question_id": 3, "answer": ""},
            {"question_id": 4, "answer": "Houston, TX"},  # Wrong city
            {"question_id": 5, "answer": "0"},  # No dogs!
            {"question_id": 6, "answer": "None yet"},
            {"question_id": 7, "answer": "Not sure"},
            {"question_id": 8, "answer": "Just browsing"},
            {"question_id": 9, "answer": "Not sure about budget"},
            {"question_id": 10, "answer": "N/A"}
        ]
        
        self.run_test_scenario(
            "Unqualified Lead (Wrong City, No Dogs)",
            "f1111111-1111-1111-1111-111111111111",
            scenario3_responses
        )
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary."""
        print(f"\n{'='*60}")
        print(f"📊 TEST SUMMARY")
        print(f"{'='*60}")
        
        for result in self.test_results:
            print(f"\n{result['scenario']}:")
            print(f"  - Status: {result['lead_status'].upper()}")
            print(f"  - Final Score: {result['final_score']}/100")
            print(f"    - Base: {result['base_score']}")
            if result['tool_boost'] > 0:
                print(f"    - Tool Boost: +{result['tool_boost']}")
            if result['llm_adjustment'] != 0:
                print(f"    - LLM Adjustment: {result['llm_adjustment']:+d}")
            print(f"  - Steps: {result['steps']}")
        
        # Save results to file in results directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"results/test_results_{timestamp}.json"
        
        # Ensure results directory exists
        os.makedirs("results", exist_ok=True)
        
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"\n✅ Results saved to: {results_file}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test LangGraph Survey Flow")
    parser.add_argument("--scenario", choices=["high", "maybe", "low", "all"], 
                       default="all", help="Which scenario to run")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--load-data", action="store_true", help="Load test data first")
    
    args = parser.parse_args()
    
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: No LLM API keys found!")
        print("Please set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
        sys.exit(1)
    
    # Optional: Check for tool API keys
    if not os.getenv("TAVILY_API_KEY"):
        print("⚠️ Warning: TAVILY_API_KEY not set - will use mock Tavily responses")
    
    if not os.getenv("GOOGLE_MAPS_API_KEY"):
        print("⚠️ Warning: GOOGLE_MAPS_API_KEY not set - will use mock Maps responses")
    
    # Load test data if requested
    if args.load_data:
        from load_test_data import load_test_data
        load_test_data()
    
    # Check if database exists
    if not os.path.exists("test_survey.db"):
        print("❌ Database not found! Run with --load-data flag first")
        sys.exit(1)
    
    # Run tests
    print("\n🚀 Starting LangGraph Survey Test Runner")
    print(f"   LangSmith Tracing: {'Enabled' if os.getenv('LANGCHAIN_TRACING_V2') else 'Disabled'}")
    
    runner = SurveyTestRunner(verbose=args.verbose)
    
    try:
        if args.scenario == "all":
            runner.run_all_tests()
        else:
            # Run individual scenario
            if args.scenario == "high":
                responses = [
                    {"question_id": 1, "answer": "Sarah Williams"},
                    {"question_id": 2, "answer": "sarah@email.com"},
                    {"question_id": 3, "answer": "512-555-9999"},
                    {"question_id": 4, "answer": "456 Congress Ave, Austin, TX"},
                    {"question_id": 5, "answer": "3"},
                    {"question_id": 6, "answer": "All small breeds"},
                    {"question_id": 7, "answer": "Every weekday please"},
                    {"question_id": 8, "answer": "Starting tomorrow if possible"},
                    {"question_id": 9, "answer": "$50 per walk"},
                    {"question_id": 10, "answer": "They love treats!"}
                ]
                runner.run_test_scenario("High Quality Lead", 
                                       "f1111111-1111-1111-1111-111111111111",
                                       responses)
        
        print("\n✅ Test run complete!")
        
    finally:
        # Always cleanup the test database
        runner.cleanup()

if __name__ == "__main__":
    main()