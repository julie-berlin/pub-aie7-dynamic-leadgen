#!/usr/bin/env python3
"""
Setup and test script for database population
Runs migrations, populates data, and tests the system
"""
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple

def run_command(command: List[str], description: str) -> Tuple[bool, str]:
    """Run a command and return success status and output"""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr or e.stdout}"
    except FileNotFoundError:
        return False, f"Command not found: {' '.join(command)}"

def main():
    """Setup database and run tests"""
    database_dir = Path(__file__).parent
    
    print("🚀 Setting up Database for Dynamic Survey System")
    print("="*60)
    
    # Check if we can run the test script
    test_script = database_dir / "test_database_population.py"
    if not test_script.exists():
        print("❌ Test script not found. Please ensure test_database_population.py exists.")
        return
    
    print("\n📋 Available files:")
    migration_files = [
        ("001_initial_schema.sql", "Database schema migration"),
        ("002_populate_example_data.sql", "Example data population"),
        ("001_rollback_schema.sql", "Schema rollback (optional)"),
        ("business_scenarios.md", "Business scenario documentation"),
        ("test_database_population.py", "Test script")
    ]
    
    for filename, description in migration_files:
        file_path = database_dir / filename
        status = "✅" if file_path.exists() else "❌"
        print(f"   {status} {filename} - {description}")
    
    print(f"\n💡 Manual Database Setup Required:")
    print(f"   1. Open your Supabase SQL Editor")
    print(f"   2. Run: {database_dir}/001_initial_schema.sql")
    print(f"   3. Run: {database_dir}/002_populate_example_data.sql")
    print(f"   4. Verify your .env file has:")
    print(f"      - SUPABASE_URL")
    print(f"      - SUPABASE_PUBLISHABLE_KEY") 
    print(f"      - SUPABASE_SECRET_KEY")
    
    print(f"\n🧪 Running Database Population Tests...")
    
    # Run the test script
    test_command = [sys.executable, str(test_script)]
    success, output = run_command(test_command, "Database population tests")
    
    if success:
        print(output)
    else:
        print(f"❌ Test execution failed:")
        print(output)
        print(f"\n💡 Troubleshooting:")
        print(f"   - Ensure database migrations have been run")
        print(f"   - Check your .env file configuration")
        print(f"   - Verify Supabase connection")
        return
    
    print(f"\n🎯 Next Steps:")
    print(f"   - Test the survey API endpoints with the populated form IDs")
    print(f"   - Use the business_scenarios.md file for context")
    print(f"   - Run specific business scenario tests as needed")
    
if __name__ == "__main__":
    main()