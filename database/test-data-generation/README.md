# Test Data Generation for Dynamic Surveys Platform

This folder contains scripts to generate realistic test data for all 5 business clients in the platform.

## Overview

The test data generation creates **150 realistic lead sessions** across 5 different business types:

1. **Pawsome Dog Walking** (Pet Services) - 30 leads
2. **Metro Realty Group** (Real Estate) - 30 leads  
3. **TechSolve Consulting** (Software Consulting) - 30 leads
4. **FitLife Personal Training** (Health & Fitness) - 30 leads
5. **Sparkle Clean Solutions** (Home Cleaning) - 30 leads

## Files

### `client_personas.py`
Contains realistic personas and form field mappings for all 5 clients:
- **Personas**: Realistic customer profiles with appropriate responses for each business type
- **Form Questions**: Question ID to field mappings for each client's form
- **Lead Types**: qualified, maybe, unqualified, abandoned leads for realistic conversion rates

### `generate_all_clients.py`
Main script that generates SQL for all clients:
- Creates complete lead sessions with proper timestamps
- Generates responses, tracking data, and lead outcomes
- Handles database constraints correctly
- Produces realistic UTM tracking and device data

### `generate_leads.py` (Legacy)
Original script for Pawsome Dog Walking only - kept for reference.

## Usage

### Generate All Clients (Recommended)
```bash
cd database/test-data-generation
./generate_all.sh
```

This creates individual SQL files for each client, making it easy to:
- Add more leads to specific clients
- Modify individual client data  
- Test specific business scenarios
- Execute clients independently

### Generate Individual Client Data
```bash
# Individual client files
python3 generate_pawsome.py > ../pawsome_leads.sql
python3 generate_metro_realty.py > ../metro_realty_leads.sql
python3 generate_techsolve.py > ../techsolve_leads.sql
python3 generate_fitlife.py > ../fitlife_leads.sql
python3 generate_sparkle_clean.py > ../sparkle_clean_leads.sql
```

### Combine All Files (Optional)
```bash
cat ../pawsome_leads.sql ../metro_realty_leads.sql ../techsolve_leads.sql ../fitlife_leads.sql ../sparkle_clean_leads.sql > ../all_clients_leads.sql
```

## Data Characteristics

### Lead Distribution
- **Qualified Leads** (~40%): High-scoring leads ready for immediate follow-up
- **Maybe Leads** (~30%): Medium-scoring leads requiring nurturing  
- **Unqualified Leads** (~20%): Low-scoring leads that don't meet criteria
- **Abandoned Leads** (~10%): Incomplete sessions for testing abandonment flows

### Realistic Elements
- **Timestamps**: Spread over 2 weeks with realistic session durations
- **Contact Info**: Business-appropriate names, emails, and phone numbers
- **Responses**: Industry-specific answers that align with business needs
- **UTM Tracking**: Realistic marketing campaign attribution
- **Devices**: Mix of desktop/mobile usage patterns
- **Scoring**: Business-specific scoring rubrics for lead qualification

### Database Compliance
- **Proper UUID Formats**: All IDs are valid UUIDs
- **Constraint Compliance**: Respects all database CHECK constraints
- **Foreign Key Relationships**: Correct references between tables
- **JSONB Data**: Properly formatted contact_info and metadata fields

## Database Tables Populated

1. **lead_sessions**: Main session records with scoring and status
2. **tracking_data**: UTM parameters and device information
3. **responses**: Individual question/answer pairs with timestamps
4. **lead_outcomes**: Final lead classification and contact information

## Execution

After generating the SQL file, execute it against your Supabase database:

1. **Generate**: `python3 generate_all_clients.py > test_data.sql`
2. **Review**: Check the generated SQL for correctness
3. **Execute**: Run the SQL against your database
4. **Verify**: Check admin pages to confirm data loaded correctly

## Demo Benefits

This comprehensive dataset enables:
- **Complete Admin Interface Demo**: All pages populated with realistic data
- **Lead Management Testing**: Conversion tracking, filtering, and analytics
- **Multi-Client Scenarios**: Different business types and use cases
- **Performance Testing**: Realistic data volumes for UI testing
- **Analytics Validation**: Proper data for reporting and insights

## Customization

To modify the data generation:

1. **Add Personas**: Edit `client_personas.py` to add more customer profiles
2. **Adjust Volumes**: Change `num_leads` parameter in generation calls
3. **Modify Scoring**: Update scoring logic in `get_question_score()`
4. **Time Ranges**: Adjust timestamp generation for different date ranges
5. **UTM Campaigns**: Add more marketing campaign variations

## Notes

- All generated data is **fictional** and safe for demo purposes
- Lead scoring reflects realistic business qualification criteria  
- Conversion tracking fields are initialized as unconverted (ready for admin updates)
- Data generation is **deterministic** for consistent results across runs