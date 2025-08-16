# Frontend Integration Documentation

This directory contains essential files for frontend integration with the Dynamic Survey Platform backend.

## Files

### `typescript-types.ts`
Auto-generated TypeScript type definitions that match our Pydantic models. This file provides complete type safety between frontend and backend.

**⚠️ IMPORTANT: This file is auto-generated. Do not edit manually.**

## Keeping Types Synchronized

Whenever you make changes to the backend data schema (Pydantic models), you **must** regenerate the TypeScript types to maintain type safety.

### When to Regenerate Types

Run the type generation script whenever you:

1. **Add new Pydantic models** in any API module
2. **Modify existing Pydantic models** (add/remove/change fields)
3. **Change field types** in any model
4. **Update validation rules** that affect field types
5. **Add new API endpoints** with new request/response models

### How to Regenerate Types

From the project root directory:

```bash
# Use uv (recommended - ensures correct Python environment)
uv run python3 backend/generate_typescript_types.py

# Or with direct Python (ensure PYTHONPATH is set)
PYTHONPATH=/path/to/project/backend python3 backend/generate_typescript_types.py
```

This will:
- Generate `backend/survey-api-types.ts` with all current types
- Automatically copy the file to `docs/frontend-integration/typescript-types.ts`
- Create JSON schemas for additional tooling in `backend/survey-api-schemas.json`

### Type Generation Features

#### Phase 2 Support ✅
The type generator automatically includes Phase 2 API types when available:
- **Theme Management API**: Complete theming system types
- **Analytics API**: Event tracking and performance metrics
- **Admin API**: User management and client configuration

#### Generated Type Categories

1. **Core Enums**: `LeadStatus`, `AbandonmentStatus`, `CompletionType`, etc.
2. **Survey API Types**: Request/response models for form functionality
3. **Theme Management Types**: Theming and visual customization
4. **Analytics Types**: Event tracking and performance monitoring
5. **Admin Types**: User authentication and client management
6. **Utility Types**: Helper interfaces for frontend development
7. **API Client Interfaces**: Complete client implementations
8. **API Endpoints**: Centralized endpoint constants

#### Type Safety Features

- **Proper optional field handling**: Uses `field?:` syntax correctly
- **Literal type support**: Enum-like literal unions for constrained values
- **Email validation**: EmailStr fields become `string` in TypeScript
- **Complex type mapping**: Nested objects, arrays, and union types
- **Comprehensive documentation**: JSDoc comments from Pydantic field descriptions

### Integration with Frontend Projects

#### React/TypeScript Projects

```typescript
import { 
  StartSessionRequest, 
  SurveyApiClient,
  ThemeConfig,
  API_ENDPOINTS 
} from './types/survey-api';

// Type-safe API client implementation
const apiClient: SurveyApiClient = {
  async startSession(request: StartSessionRequest) {
    const response = await fetch(API_ENDPOINTS.START_SESSION, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    });
    return response.json();
  }
  // ... other methods
};
```

#### Validation and Error Handling

```typescript
import { ErrorResponse, LeadStatus } from './types/survey-api';

function isErrorResponse(data: any): data is ErrorResponse {
  return data && typeof data.error === 'string' && typeof data.message === 'string';
}

function isValidLeadStatus(status: string): status is LeadStatus {
  return ['unknown', 'yes', 'maybe', 'no'].includes(status);
}
```

### Development Workflow

1. **Make backend changes** to Pydantic models
2. **Test backend changes** with appropriate tests
3. **Regenerate types** using the command above
4. **Update frontend code** to use new types if needed
5. **Run frontend type checking** to catch any breaking changes
6. **Test integration** to ensure frontend-backend compatibility

### Automation Recommendations

Consider adding the type generation to your development workflow:

#### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit
cd backend
uv run python3 generate_typescript_types.py
git add ../docs/frontend-integration/typescript-types.ts
```

#### CI/CD Pipeline
```yaml
# In your GitHub Actions or similar
- name: Generate TypeScript Types
  run: |
    uv run python3 backend/generate_typescript_types.py
    git diff --exit-code docs/frontend-integration/typescript-types.ts || {
      echo "TypeScript types are out of date. Please regenerate."
      exit 1
    }
```

#### Package.json Scripts
```json
{
  "scripts": {
    "generate-types": "cd backend && uv run python3 generate_typescript_types.py",
    "check-types": "tsc --noEmit",
    "sync-types": "npm run generate-types && npm run check-types"
  }
}
```

## Phase 2 API Integration

The generated types include comprehensive Phase 2 support for advanced features:

### Theme System Integration
```typescript
import { ThemeConfig, ThemeApiClient, ClientThemeRequest } from './types/survey-api';

// Create custom themes
const newTheme: ClientThemeRequest = {
  name: "Brand Theme",
  description: "Corporate brand colors and fonts",
  theme_config: {
    name: "brand-theme",
    colors: {
      primary: "#007bff",
      primaryHover: "#0056b3",
      // ... complete color system
    },
    typography: {
      primary: "Inter, sans-serif",
      secondary: "Georgia, serif"
    }
  },
  is_default: true
};
```

### Analytics Integration
```typescript
import { EventTrackingRequest, AnalyticsApiClient } from './types/survey-api';

// Track user interactions
const trackingEvent: EventTrackingRequest = {
  session_id: "session-123",
  event_type: "question_answer",
  event_category: "interaction",
  event_action: "input",
  question_id: 1,
  step_number: 2,
  viewport_size: { width: 1920, height: 1080 },
  session_duration_ms: 45000
};
```

### Admin System Integration
```typescript
import { AdminUserRegister, AdminApiClient, ClientSettingsRequest } from './types/survey-api';

// User registration and management
const adminRegistration: AdminUserRegister = {
  email: "admin@company.com",
  password: "SecurePass123!",
  first_name: "Jane",
  last_name: "Smith",
  client_id: "client-uuid",
  role: "admin"
};

// Client branding configuration
const clientSettings: ClientSettingsRequest = {
  logo_url: "https://company.com/logo.png",
  brand_colors: {
    primary: "#007bff",
    secondary: "#6c757d"
  },
  white_label_enabled: true,
  custom_domain: "forms.company.com"
};
```

## Troubleshooting

### Common Issues

#### "Phase 2 Support: ❌ Not Available"
This means the Phase 2 API modules couldn't be imported. Check:
1. Are all dependencies installed? Run `uv sync`
2. Is the PYTHONPATH set correctly when running the generator?
3. Are there any import errors in the API modules?

#### "pydantic[email] not installed"
Install email validation support:
```bash
uv add "pydantic[email]"
```

#### Types seem outdated
Always regenerate after schema changes:
```bash
uv run python3 backend/generate_typescript_types.py
```

#### Import errors in generated types
This usually indicates:
1. Complex types that need manual mapping in the generator
2. Missing type imports in the generator script
3. Pydantic model issues that need resolution

### Getting Help

1. Check the generator script at `backend/generate_typescript_types.py`
2. Review the Pydantic models for any validation issues
3. Ensure all backend dependencies are properly installed
4. Test API modules individually to isolate import problems

## Best Practices

1. **Always regenerate types** after backend changes
2. **Use the generated types** consistently in frontend code
3. **Don't modify** the auto-generated file manually
4. **Version control** both the generator script and output file
5. **Test type safety** with `tsc --noEmit` in frontend projects
6. **Document breaking changes** when updating major API versions