#!/usr/bin/env python3
"""Test runner for LangGraph survey flow with tool integration."""

import os
import sys
import json
import logging
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
        
        # Process responses in batches
        response_index = 0
        while response_index < len(responses):
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
                if response_index < len(responses):
                    response = responses[response_index]
                    # Match response to question
                    current_responses.append({
                        "question_id": q['id'],
                        "question_text": q['text'],
                        "phrased_question": q['text'],
                        "answer": response['answer'],
                        "step": step_count
                    })
                    print(f"   A: {response['answer']}")
                    response_index += 1
            
            if not current_responses:
                print("   ⚠️ No responses available for these questions")
                break
            
            # Update state with responses
            state["pending_responses"] = current_responses
            
            # Process responses
            print(f"\n🤖 Processing responses...")
            state = run_survey_sync(state)
            
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
            lead_status = state.get("lead_status", "continue")
            if lead_status != "continue":
                print(f"\n🎯 Lead Status Determined: {lead_status.upper()}")
                break
            
            # Check for completion
            if state.get("completed"):
                break
        
        # Final results
        print(f"\n{'='*60}")
        print(f"📈 FINAL RESULTS")
        print(f"{'='*60}")
        
        final_score = state.get("lead_intelligence", {}).get("current_score", 0)
        lead_status = state.get("lead_status", "unknown")
        completion_message = state.get("completion_message", "No message generated")
        
        print(f"📊 Final Score: {final_score}/100")
        if tool_boost > 0:
            print(f"   - Base Score: {final_score - tool_boost}")
            print(f"   - Tool Boost: +{tool_boost}")
        
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
            "tool_boost": tool_boost,
            "lead_status": lead_status,
            "completion_message": completion_message,
            "tool_results": all_tool_results
        }
        
        self.test_results.append(result)
        return result
    
    def run_all_tests(self):
        """Run all test scenarios."""
        
        # Test Scenario 1: High-quality lead with tool validation
        scenario1_responses = [
            {"answer": "John Smith"},
            {"answer": "john.smith@email.com"},
            {"answer": "512-555-1234"},
            {"answer": "123 Main St, Downtown Austin, TX"},
            {"answer": "2"},
            {"answer": "Golden Retriever and Labrador"},
            {"answer": "Daily walks needed, 5 days a week"},
            {"answer": "Need to start immediately, my work schedule changed"},
            {"answer": "$40 per walk is fine"},
            {"answer": "The Lab needs gentle handling, he's older"}
        ]
        
        self.run_test_scenario(
            "High-Quality Lead (Downtown Austin)",
            "f1111111-1111-1111-1111-111111111111",
            scenario1_responses
        )
        
        # Test Scenario 2: Maybe lead - far location
        scenario2_responses = [
            {"answer": "Mary Johnson"},
            {"answer": "mary@email.com"},
            {"answer": ""},  # No phone
            {"answer": "Round Rock, TX"},  # Far from Austin
            {"answer": "1"},
            {"answer": "Poodle"},
            {"answer": "Maybe 2-3 times per week"},
            {"answer": "Next month possibly"},
            {"answer": "$25 if possible"},
            {"answer": "No special needs"}
        ]
        
        self.run_test_scenario(
            "Maybe Lead (Round Rock - Distance Challenge)",
            "f1111111-1111-1111-1111-111111111111",
            scenario2_responses
        )
        
        # Test Scenario 3: Unqualified lead
        scenario3_responses = [
            {"answer": "Bob Wilson"},
            {"answer": "bob@test.com"},
            {"answer": ""},
            {"answer": "Houston, TX"},  # Wrong city
            {"answer": "0"},  # No dogs!
            {"answer": "None yet"},
            {"answer": "Not sure"},
            {"answer": "Just browsing"},
            {"answer": "Not sure about budget"},
            {"answer": "N/A"}
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
            print(f"  - Score: {result['final_score']}/100")
            print(f"  - Tool Boost: +{result['tool_boost']}")
            print(f"  - Steps: {result['steps']}")
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"test_results_{timestamp}.json"
        
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
    
    if args.scenario == "all":
        runner.run_all_tests()
    else:
        # Run individual scenario
        if args.scenario == "high":
            responses = [
                {"answer": "Sarah Williams"},
                {"answer": "sarah@email.com"},
                {"answer": "512-555-9999"},
                {"answer": "456 Congress Ave, Austin, TX"},
                {"answer": "3"},
                {"answer": "All small breeds"},
                {"answer": "Every weekday please"},
                {"answer": "Starting tomorrow if possible"},
                {"answer": "$50 per walk"},
                {"answer": "They love treats!"}
            ]
            runner.run_test_scenario("High Quality Lead", 
                                   "f1111111-1111-1111-1111-111111111111",
                                   responses)
    
    print("\n✅ Test run complete!")

if __name__ == "__main__":
    main()