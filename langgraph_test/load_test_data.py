#!/usr/bin/env python3
"""Load test data into SQLite database."""

import sqlite3
import os
from pathlib import Path

def load_test_data():
    """Load test data from SQL file into database."""
    
    # Get paths
    db_path = "test_survey.db"
    sql_file = Path(__file__).parent / "database" / "test_data.sql"
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ Removed existing database: {db_path}")
    
    # Create new database and load schema
    from database.sqlite_db import SQLiteDatabase
    db = SQLiteDatabase(db_path)
    print("✅ Created new database with schema")
    
    # Load test data
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(sql_file, 'r') as f:
        sql_content = f.read()
        
    # Execute all SQL statements
    for statement in sql_content.split(';'):
        statement = statement.strip()
        if statement:
            try:
                cursor.execute(statement)
                conn.commit()
            except sqlite3.IntegrityError as e:
                print(f"⚠️ Skipping duplicate: {e}")
            except Exception as e:
                print(f"❌ Error executing statement: {e}")
                print(f"Statement: {statement[:100]}...")
    
    # Verify data loaded
    cursor.execute("SELECT COUNT(*) FROM clients")
    client_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM forms")
    form_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM form_questions")
    question_count = cursor.fetchone()[0]
    
    print(f"\n📊 Data loaded successfully:")
    print(f"  - Clients: {client_count}")
    print(f"  - Forms: {form_count}")
    print(f"  - Questions: {question_count}")
    
    # Show available forms
    cursor.execute("SELECT id, title FROM forms")
    forms = cursor.fetchall()
    print(f"\n📋 Available test forms:")
    for form_id, title in forms:
        print(f"  - {form_id}: {title}")
    
    conn.close()
    print(f"\n✅ Test data loaded into {db_path}")

if __name__ == "__main__":
    load_test_data()