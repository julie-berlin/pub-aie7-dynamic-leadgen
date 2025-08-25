#!/bin/bash

# Generate individual SQL files for each client
echo "Generating test data for all 5 clients..."

python3 generate_pawsome.py > ../pawsome_leads.sql
echo "✓ Generated Pawsome Dog Walking leads (30)"

python3 generate_metro_realty.py > ../metro_realty_leads.sql  
echo "✓ Generated Metro Realty Group leads (30)"

python3 generate_techsolve.py > ../techsolve_leads.sql
echo "✓ Generated TechSolve Consulting leads (30)"

python3 generate_fitlife.py > ../fitlife_leads.sql
echo "✓ Generated FitLife Personal Training leads (30)"

python3 generate_sparkle_clean.py > ../sparkle_clean_leads.sql
echo "✓ Generated Sparkle Clean Solutions leads (30)"

echo ""
echo "Generated 5 SQL files with 150 total leads!"
echo "Files created in database/ folder:"
echo "  - pawsome_leads.sql"
echo "  - metro_realty_leads.sql" 
echo "  - techsolve_leads.sql"
echo "  - fitlife_leads.sql"
echo "  - sparkle_clean_leads.sql"
echo ""
echo "To execute all at once:"
echo "cat ../pawsome_leads.sql ../metro_realty_leads.sql ../techsolve_leads.sql ../fitlife_leads.sql ../sparkle_clean_leads.sql > ../all_clients_leads.sql"