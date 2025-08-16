#!/usr/bin/env python3
"""
Run the theme customization columns migration (007)
Adds primary_color, secondary_color, and font_family columns to client_themes table
"""
import sys
import os
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.database import SupabaseClient

def main():
    """Run the theme customization migration"""
    print("🎨 Running Theme Customization Migration (007)...")
    print("   Adding primary_color, secondary_color, and font_family columns")
    
    try:
        # Initialize database client
        db = SupabaseClient()
        
        # Read migration file
        migration_file = Path(__file__).parent / "migrations" / "007_theme_customization_columns.sql"
        
        if not migration_file.exists():
            print(f"❌ Migration file not found: {migration_file}")
            return
        
        with open(migration_file, 'r') as f:
            migration_sql = f.read()
        
        print(f"📋 Migration file loaded: {migration_file.name}")
        
        # For complex migrations like this with functions and triggers,
        # it's safer to run manually in Supabase SQL Editor
        print("\n💡 Due to the complexity of this migration (functions, triggers, constraints),")
        print("   it's recommended to run this manually in Supabase SQL Editor.")
        
        print(f"\n📝 Manual Steps:")
        print(f"   1. Open Supabase SQL Editor")
        print(f"   2. Copy the contents of: {migration_file}")
        print(f"   3. Paste and execute the SQL")
        print(f"   4. Verify the migration completed successfully")
        
        print(f"\n🔍 What this migration does:")
        print(f"   ✅ Adds primary_color column to client_themes")
        print(f"   ✅ Adds secondary_color column to client_themes") 
        print(f"   ✅ Adds font_family column to client_themes")
        print(f"   ✅ Adds color format validation constraints")
        print(f"   ✅ Creates indexes for performance")
        print(f"   ✅ Migrates existing theme data to new columns")
        print(f"   ✅ Creates sync triggers for backwards compatibility")
        print(f"   ✅ Adds helper functions and views")
        
        # Try to test if we can connect to the database
        try:
            # Simple test to see if client_themes table exists
            result = db.client.table("client_themes").select("id").limit(1).execute()
            print(f"\n✅ Database connection successful")
            print(f"   Current client_themes table found with {len(result.data)} sample records")
        except Exception as e:
            print(f"\n⚠️  Database connection test failed: {e}")
        
        print(f"\n🎯 After running the migration, you'll be able to:")
        print(f"   • Query themes by color: SELECT * FROM client_themes WHERE primary_color = '#3B82F6'")
        print(f"   • Filter by font: SELECT * FROM client_themes WHERE font_family LIKE '%Inter%'")
        print(f"   • Use the theme_summary view for unified theme data")
        print(f"   • Create themes with: SELECT create_custom_theme(client_id, 'My Theme', 'Description', '#FF0000', '#00FF00')")
        
    except Exception as e:
        print(f"❌ Script failed: {e}")
        print(f"\n💡 Fallback:")
        print(f"   Run the SQL manually in Supabase SQL Editor")
        print(f"   File: database/migrations/007_theme_customization_columns.sql")

if __name__ == "__main__":
    main()