#!/usr/bin/env python3
"""Update Pawsome form with custom theme in Supabase"""

import os
import json
from pathlib import Path

# Add backend to Python path
import sys
sys.path.append(str(Path(__file__).parent / "backend"))

from supabase import create_client

def main():
    # Database connection
    supabase = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    )
    
    # Read CSS file
    css_path = Path(__file__).parent / "frontend/form-app/src/styles/themes/pawsome.css"
    with open(css_path) as f:
        custom_css = f.read()
    
    # Theme configuration based on the CSS design
    theme_config = {
        "name": "pawsome",
        "colors": {
            "primary": "#4A9B8E",
            "primaryHover": "#3D8A7C",
            "primaryLight": "#E8F4F1", 
            "secondary": "#F4C430",
            "secondaryHover": "#E6B029",
            "secondaryLight": "#FFF8DC",
            "accent": "#8B4513",
            "text": "#2C3E50",
            "textLight": "#5A6C7D", 
            "textMuted": "#6B7280",
            "background": "#FFF8DC",
            "backgroundLight": "#F0F8F6",
            "border": "#D4E4E0",
            "error": "#ef4444",
            "success": "#10b981",
            "warning": "#f59e0b"
        },
        "typography": {
            "primary": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            "secondary": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
        },
        "spacing": {
            "section": "2rem",
            "element": "1rem",
            "page": "2rem", 
            "input": "0.75rem",
            "button": "0.875rem 2rem"
        },
        "borderRadius": "8px",
        "borderRadiusLg": "16px",
        "shadow": "0 4px 20px rgba(74, 155, 142, 0.1)",
        "shadowLg": "0 10px 15px -3px rgba(74, 155, 142, 0.2)",
        "logo_url": "/images/logos/Pawsome_Logo.png",
        "custom_css": custom_css
    }
    
    # Update the Pawsome form
    pawsome_form_id = "f1111111-1111-1111-1111-111111111111"
    
    result = supabase.table("forms").update({
        "theme_config": theme_config
    }).eq("id", pawsome_form_id).execute()
    
    if result.data:
        print("✅ Pawsome theme updated successfully!")
        print(f"Form ID: {pawsome_form_id}")
        print(f"Theme: {theme_config['name']}")
        print(f"Primary color: {theme_config['colors']['primary']}")
        print(f"Logo: {theme_config.get('logo_url', 'None')}")
    else:
        print("❌ Failed to update theme")

if __name__ == "__main__":
    main()