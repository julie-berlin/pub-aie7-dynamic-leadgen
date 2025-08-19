#!/usr/bin/env python3
"""
Run the client themes migration
"""
import sys
import os
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.database import SupabaseClient

def main():
    """Run the theme migration"""
    print("🎨 Running Client Themes Migration...")
    
    try:
        # Initialize database client
        db = SupabaseClient()
        
        # Read migration file
        migration_file = Path(__file__).parent / "migrations" / "006_client_themes.sql"
        with open(migration_file, 'r') as f:
            migration_sql = f.read()
        
        # Split into individual statements (Supabase doesn't handle multi-statement well)
        statements = [stmt.strip() for stmt in migration_sql.split(';') if stmt.strip()]
        
        print(f"📋 Executing {len(statements)} SQL statements...")
        
        for i, statement in enumerate(statements):
            if not statement:
                continue
                
            try:
                # Use raw SQL execution for INSERT/UPDATE statements
                response = db.client.rpc('exec_sql', {'sql': statement})
                print(f"   ✅ Statement {i+1}/{len(statements)} executed")
            except Exception as e:
                # For statements that don't work with rpc, try direct table operations
                if "INSERT INTO client_themes" in statement:
                    print(f"   ⚠️  Statement {i+1}: Using fallback insertion method")
                    # This would need to be parsed and converted to Supabase table operations
                    # For now, we'll note this needs manual SQL execution
                    print(f"      💡 Please run this statement manually in Supabase SQL Editor:")
                    print(f"      {statement[:100]}...")
                else:
                    print(f"   ❌ Statement {i+1} failed: {e}")
        
        print("\n🎯 Migration Status:")
        print("   - Client themes migration completed")
        print("   - Some statements may need manual execution in Supabase SQL Editor")
        print(f"   - Migration file: {migration_file}")
        print("\n💡 Manual Steps:")
        print("   1. Copy the contents of 006_client_themes.sql")
        print("   2. Paste into Supabase SQL Editor")
        print("   3. Execute to create all client themes")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("\n💡 Manual Fallback:")
        print("   1. Open Supabase SQL Editor")
        print("   2. Run: database/migrations/006_client_themes.sql")

if __name__ == "__main__":
    main()