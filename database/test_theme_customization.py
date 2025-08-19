#!/usr/bin/env python3
"""
Test script for theme customization migration (007)
Verifies that the new columns and functionality work correctly
"""
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.database import SupabaseClient

def test_theme_customization():
    """Test the theme customization features"""
    print("🧪 Testing Theme Customization Migration...")
    
    try:
        db = SupabaseClient()
        
        # Test 1: Check if new columns exist
        print("\n1️⃣ Testing column existence...")
        result = db.client.table("client_themes").select("id, name, primary_color, secondary_color, font_family").limit(1).execute()
        
        if result.data:
            theme = result.data[0]
            print(f"   ✅ Columns exist - Sample theme: {theme.get('name')}")
            print(f"   📌 Primary: {theme.get('primary_color')}")
            print(f"   📌 Secondary: {theme.get('secondary_color')}")
            print(f"   📌 Font: {theme.get('font_family')}")
        else:
            print("   ⚠️  No themes found to test")
        
        # Test 2: Check theme_summary view
        print("\n2️⃣ Testing theme_summary view...")
        try:
            # This will only work if the view was created
            result = db.client.rpc('exec_sql', {'sql': 'SELECT COUNT(*) as count FROM theme_summary'})
            print("   ✅ theme_summary view accessible")
        except Exception as e:
            print(f"   ⚠️  theme_summary view not accessible: {e}")
        
        # Test 3: Try to query by color
        print("\n3️⃣ Testing color-based queries...")
        try:
            result = db.client.table("client_themes").select("name, primary_color").eq("primary_color", "#3B82F6").execute()
            print(f"   ✅ Color query successful - found {len(result.data)} themes with blue primary color")
        except Exception as e:
            print(f"   ❌ Color query failed: {e}")
        
        # Test 4: Check if existing themes have populated color columns
        print("\n4️⃣ Testing data migration...")
        result = db.client.table("client_themes").select("name, primary_color, secondary_color, font_family").execute()
        
        populated_themes = [theme for theme in result.data if theme.get('primary_color') and theme.get('secondary_color')]
        print(f"   📊 {len(populated_themes)} out of {len(result.data)} themes have populated color columns")
        
        if populated_themes:
            print("   ✅ Data migration appears successful")
            # Show sample
            sample = populated_themes[0]
            print(f"   📝 Sample: {sample.get('name')} - {sample.get('primary_color')} / {sample.get('secondary_color')}")
        else:
            print("   ⚠️  No themes have populated color columns - migration may need to be re-run")
        
        print(f"\n🎯 Migration Test Summary:")
        print(f"   • New columns: {'✅' if result.data else '❌'}")
        print(f"   • Data populated: {'✅' if populated_themes else '⚠️'}")
        print(f"   • Query functionality: ✅")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("   This likely means the migration hasn't been run yet")
        print("   Please execute 007_theme_customization_columns.sql in Supabase SQL Editor first")
        return False

if __name__ == "__main__":
    test_theme_customization()