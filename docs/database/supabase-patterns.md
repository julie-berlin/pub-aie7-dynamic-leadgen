# Supabase Database Patterns

## Overview

This document outlines the standardized patterns for database operations using Supabase client throughout the Dynamic Lead Gen application. All database operations have been migrated from psycopg2 to use consistent Supabase client patterns.

## Migration Summary

- **Migration Date**: August 23, 2025
- **Files Migrated**: 70+ database operations across 5+ API modules
- **Performance Impact**: From timeout issues to sub-second response times
- **Architecture**: Monolithic → Modular, Mixed patterns → Consistent patterns
- **Dependencies**: **psycopg2-binary completely removed** - 100% Supabase throughout application
- **LangChain Compatibility**: Confirmed working without psycopg2 dependency

## Standard Import Pattern

All files should use this consistent import pattern:

```python
from app.database import db
```

**❌ Deprecated patterns (removed):**
```python
from app.database import get_database_connection
from ..database import db  # Relative imports
```

## Database Client Usage

### Standard Query Pattern

All database operations follow this pattern:

```python
# SELECT operations
result = db.client.table("table_name")\
    .select("column1, column2")\
    .eq("filter_column", value)\
    .execute()

# INSERT operations  
result = db.client.table("table_name")\
    .insert(data_dict)\
    .execute()

# UPDATE operations
result = db.client.table("table_name")\
    .update(update_dict)\
    .eq("id", record_id)\
    .execute()

# DELETE operations
result = db.client.table("table_name")\
    .delete()\
    .eq("id", record_id)\
    .execute()
```

### Result Handling Patterns

#### Standard Result Checking

```python
# Check if data exists
if not result.data:
    # Handle no data case
    return error_response("Record not found", status_code=404)

# Get single record
record = result.data[0] if result.data else None

# Get multiple records with default
records = result.data or []
```

#### Safe Data Access

```python
# Safe access with defaults
record_value = result.data[0].get('field_name', 'default_value') if result.data else 'default_value'

# Conditional access
if result.data and len(result.data) > 0:
    record = result.data[0]
    field_value = record.get('field_name')
```

## Modular API Architecture

### Admin API Structure

The admin API has been modularized into focused modules:

```
app/routes/
├── admin_auth.py      # Authentication & JWT handling
├── admin_client.py    # Client settings & branding  
├── admin_team.py      # Team member management
├── admin_uploads.py   # File upload management
├── admin_leads.py     # Lead management & analytics
├── analytics_api.py   # Dashboard metrics & reporting
├── clients_api.py     # RESTful client operations
├── forms_api.py       # Form CRUD operations
├── themes_api.py      # Theme management
└── files_api.py       # File serving
```

Each module follows the same patterns:

1. **Consistent imports** from `app.database import db`
2. **Standardized error handling** using response helpers
3. **Row-level security** - client-scoped operations
4. **Consistent response format** via response helpers

### Response Format Standardization

All endpoints return consistent JSON responses:

```python
# Success response
{
    "success": true,
    "data": {...},
    "message": "Operation completed successfully",
    "_timestamp": "2025-08-23T00:47:20.092306",
    "_sanitized": true
}

# Error response  
{
    "success": false,
    "message": "Error description",
    "status_code": 400,
    "_timestamp": "2025-08-23T00:47:20.092306", 
    "_sanitized": true
}
```

## Security Patterns

### Client-Scoped Operations

All operations are automatically scoped to the authenticated client:

```python
@router.get("/forms")
async def list_forms(current_user: AdminUserResponse = Depends(get_current_admin_user)):
    # All queries automatically scoped to current_user.client_id
    result = db.client.table("forms")\
        .select("*")\
        .eq("client_id", current_user.client_id)\
        .execute()
```

### Row-Level Security

- Each client can only access their own data
- Cross-client access attempts return 404 (not 403 for security)
- System themes and shared resources handled appropriately

## Performance Optimizations

### Connection Pooling

The Supabase client uses built-in connection pooling:

```python
# Configuration in database.py
self.pool_size = config.pool_size
self.max_overflow = config.pool_max_overflow  
self.query_timeout = config.query_timeout
```

### Query Performance

- All queries use appropriate filters and indexes
- Pagination implemented where needed
- Response times optimized to <2 seconds (typically <1.2s)

## Error Handling

### Standard Error Pattern

```python
try:
    result = db.client.table("table_name").select("*").execute()
    
    if not result.data:
        return error_response("Record not found", status_code=404)
        
    return success_response(
        data=result.data[0],
        message="Record retrieved successfully"
    )
    
except Exception as e:
    logger.error(f"Database error: {e}")
    return error_response("Database operation failed", status_code=500)
```

### Logging

Consistent logging patterns for debugging:

```python
logger.info(f"Querying {table_name} for client {client_id}")
logger.error(f"Database operation failed: {e}")
logger.debug(f"Query result: {result.data}")
```

## Migration Checklist

When adding new database operations, ensure:

- [ ] Uses `from app.database import db` import
- [ ] Follows standard query patterns  
- [ ] Includes client_id scoping where appropriate
- [ ] Uses consistent result checking (`result.data or []`)
- [ ] Implements proper error handling
- [ ] Returns standardized response format
- [ ] Includes appropriate logging

## Troubleshooting

### Common Issues

1. **ImportError for AdminUserResponse**
   - **Solution**: Import from `app.routes.admin_auth import AdminUserResponse`

2. **AttributeError on database operations**
   - **Solution**: Ensure using `db.client.table()` pattern, not mixed patterns

3. **Timeout errors**
   - **Solution**: Check query filters and ensure indexes exist

4. **Empty result.data**
   - **Solution**: Use `result.data or []` pattern for safe access

### Debugging Tips

```python
# Enable query logging
logger.debug(f"Executing query: {query}")
logger.debug(f"Result: {result}")

# Check connection stats
stats = db.get_connection_stats()
logger.info(f"Connection stats: {stats}")
```

## Performance Benchmarks

After migration (August 2025):

- **Analytics dashboard**: 0.38 seconds
- **Clients endpoint**: 0.11 seconds  
- **Forms endpoint**: 1.12 seconds
- **Realtime analytics**: 0.21 seconds
- **Health endpoint**: 0.09 seconds

All endpoints meet the <2 second success criteria, with most under 0.4 seconds.