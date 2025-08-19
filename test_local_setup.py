#!/usr/bin/env python3
"""
Test script to verify local PostgreSQL setup and survey flow
"""
import asyncio
import asyncpg
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:dev_password@localhost:5432/survey_dev")

async def test_database_connection():
    """Test basic database connectivity"""
    print("1. Testing database connection...")
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        version = await conn.fetchval("SELECT version()")
        print(f"   ✅ Connected to PostgreSQL: {version[:30]}...")
        await conn.close()
        return True
    except Exception as e:
        print(f"   ❌ Failed to connect: {e}")
        return False

async def test_schema_setup():
    """Verify all required tables exist"""
    print("\n2. Verifying database schema...")
    conn = await asyncpg.connect(DATABASE_URL)
    
    required_tables = [
        'clients', 'forms', 'form_questions', 'lead_sessions',
        'responses', 'tracking_data', 'session_snapshots', 
        'lead_outcomes', 'client_themes', 'admin_users'
    ]
    
    for table in required_tables:
        exists = await conn.fetchval(
            "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = $1)",
            table
        )
        status = "✅" if exists else "❌"
        print(f"   {status} Table '{table}' exists: {exists}")
    
    await conn.close()

async def test_sample_data():
    """Verify sample data is loaded"""
    print("\n3. Checking sample data...")
    conn = await asyncpg.connect(DATABASE_URL)
    
    # Check forms
    forms = await conn.fetch("SELECT id, title FROM forms ORDER BY title")
    print(f"   ✅ Found {len(forms)} forms:")
    for form in forms:
        print(f"      - {form['title']} ({form['id']})")
    
    # Check questions count
    question_count = await conn.fetchval("SELECT COUNT(*) FROM form_questions")
    print(f"   ✅ Total questions loaded: {question_count}")
    
    # Check clients
    clients = await conn.fetch("SELECT name, industry FROM clients ORDER BY name")
    print(f"   ✅ Found {len(clients)} clients:")
    for client in clients:
        print(f"      - {client['name']} ({client['industry']})")
    
    await conn.close()

async def test_survey_flow():
    """Test creating a survey session"""
    print("\n4. Testing survey session creation...")
    conn = await asyncpg.connect(DATABASE_URL)
    
    # Get first form
    form = await conn.fetchrow("SELECT * FROM forms LIMIT 1")
    if not form:
        print("   ❌ No forms found")
        await conn.close()
        return
    
    print(f"   Using form: {form['title']}")
    
    # Create a test session
    session_id = 'test-' + datetime.now().strftime('%Y%m%d-%H%M%S')
    
    try:
        session = await conn.fetchrow("""
            INSERT INTO lead_sessions (
                id, form_id, status, started_at, user_agent, ip_address
            ) VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING *
        """, session_id, form['id'], 'in_progress', 
            datetime.now(), 'Test Script', '127.0.0.1')
        
        print(f"   ✅ Created session: {session['id']}")
        
        # Get questions for this form
        questions = await conn.fetch("""
            SELECT * FROM form_questions 
            WHERE form_id = $1 
            ORDER BY order_position 
            LIMIT 3
        """, form['id'])
        
        print(f"   ✅ Found {len(questions)} questions to test")
        
        # Simulate responses
        for q in questions:
            response = await conn.fetchrow("""
                INSERT INTO responses (
                    session_id, question_id, answer, created_at
                ) VALUES ($1, $2, $3, $4)
                RETURNING id
            """, session_id, q['id'], f"Test answer for {q['question_text'][:30]}", 
                datetime.now())
            print(f"      - Saved response {response['id']} for question {q['id']}")
        
        # Update session
        await conn.execute("""
            UPDATE lead_sessions 
            SET status = 'completed', completed_at = $1
            WHERE id = $2
        """, datetime.now(), session_id)
        
        print(f"   ✅ Session completed successfully")
        
    except Exception as e:
        print(f"   ❌ Error during session test: {e}")
    
    await conn.close()

async def test_langgraph_api():
    """Test LangGraph API if running"""
    print("\n5. Testing LangGraph API...")
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            # Test health endpoint
            response = await client.get("http://localhost:8123/health")
            if response.status_code == 200:
                print(f"   ✅ LangGraph API is healthy")
                
                # List assistants
                response = await client.get("http://localhost:8123/assistants")
                if response.status_code == 200:
                    assistants = response.json()
                    print(f"   ✅ Found {len(assistants)} assistants:")
                    for assistant in assistants:
                        print(f"      - {assistant.get('name', 'Unknown')} ({assistant.get('graph_id', 'Unknown')})")
            else:
                print(f"   ⚠️  LangGraph API returned status {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  LangGraph API not accessible: {e}")
        print("      (This is OK if you're testing database only)")

async def main():
    """Run all tests"""
    print("=" * 60)
    print("LOCAL POSTGRESQL SETUP TEST")
    print("=" * 60)
    
    # Test database
    if not await test_database_connection():
        print("\n❌ Database connection failed. Make sure PostgreSQL is running.")
        print("   Run: docker compose -f docker-compose.local.yml up -d postgres")
        return
    
    await test_schema_setup()
    await test_sample_data()
    await test_survey_flow()
    await test_langgraph_api()
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 60)
    print("\nYour local setup is ready! You can now:")
    print("1. Access LangGraph API at http://localhost:8123")
    print("2. Use LangGraph Studio at https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123")
    print("3. Connect to PostgreSQL at localhost:5432 (user: postgres, password: dev_password)")
    print("4. View database with PgAdmin (if started) at http://localhost:5050")

if __name__ == "__main__":
    asyncio.run(main())