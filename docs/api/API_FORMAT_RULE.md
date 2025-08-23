# API Response Format Rule

## Standard JSON Response Format

**ALL API endpoints must return responses in this exact format:**

```json
{
  "success": <boolean>,
  "data": <object>,
  "message": <string>
}
```

## Examples

**Successful response:**
```json
{
  "success": true,
  "data": {
    "forms": [...],
    "totalCount": 25
  },
  "message": "Forms retrieved successfully"
}
```

**Error response:**
```json
{
  "success": false,
  "data": {},
  "message": "Failed to fetch forms: Invalid permissions"
}
```

## Implementation Notes

- This applies to ALL backend APIs (survey, admin, themes, analytics)
- Frontend API clients must expect and handle this format
- Legacy endpoints should be updated to follow this format
- Error handling should parse the `message` field for user feedback
- Success/failure logic should check the `success` boolean field

## Files to Update

When implementing Phase 3.3, ensure:
- `/backend/app/routes/admin_forms_api.py` uses this format
- `/backend/app/routes/admin_business_api.py` uses this format  
- Frontend admin API client expects this format
- All error handling uses the `message` field