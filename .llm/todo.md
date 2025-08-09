# Task 1, Phase 4: Update Supabase Authentication

## Overview
Migrate from current authentication method to new public key authentication method for Supabase integration.

## Implementation Tasks

- [x] Research current Supabase authentication setup
  - Examine `src/database.py` to understand current implementation
  - Document current authentication flow and dependencies
  - Identify all files that use Supabase authentication

**FINDINGS:**

**Current Authentication Implementation:**
- Uses legacy JWT-based service key authentication in `src/database.py:25`
- Client initialization: `create_client(self.url, self.service_key)`
- Environment variables: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY`
- **Status**: Currently working (✅ DB connected) but marked for migration in `.env` comment

**Authentication Flow:**
1. `SupabaseClient.__init__()` reads environment variables (lines 17-19)
2. Validates all required keys are present (lines 21-22)
3. Creates client using service key for backend operations (line 25)
4. Test connection uses simple table query (lines 30-31)
5. Has error detection for "Legacy API keys are disabled" (lines 35-37)

**Files Using Supabase Authentication:**
- `src/database.py` - Main client wrapper (singleton instance `db`)
- `src/api/main.py:58` - Health check imports `from database import db`
- `src/flow_engine.py:19` - LangGraph integration imports `from database import db`
- `notebooks/enhanced_lead_funnel.ipynb:61` - Notebook imports `from database import db`

**Dependencies & Impact:**
- All database operations go through singleton `db` instance
- API endpoints rely on database for session management
- LangGraph flow uses database for real-time persistence
- Test connection detects legacy key deprecation automatically
- No direct Supabase client usage outside of `src/database.py` wrapper

- [ ] Research new public key authentication method
  - Review Supabase documentation for new authentication patterns
  - Understand migration requirements and breaking changes
  - Document security improvements and compliance benefits

- [ ] Create test cases for authentication functionality
  - Add tests for database connection with current method
  - Add tests for key authentication operations (read, write)
  - Tests should initially pass with current auth, fail with new auth

- [ ] Update environment variable configuration
  - Add new authentication environment variables to `.env`
  - Update environment variable documentation in DEVELOPMENT_PLAN.md
  - Maintain backward compatibility during transition

- [ ] Update Supabase client initialization
  - Modify `src/database.py` to use new public key authentication
  - Implement proper error handling and fallback mechanisms
  - Ensure existing function signatures remain unchanged

- [ ] Update database utility functions
  - Modify any authentication-specific utility functions
  - Update connection testing and validation methods
  - Ensure all database operations work with new auth method

- [ ] Test database connection and operations
  - Run connection tests: `uv run python3 -c "from src.database import db; print('✅ DB connected' if db.test_connection() else '❌ DB issue')"`
  - Test all CRUD operations on existing tables
  - Verify session management still works correctly

- [ ] Test integration with LangGraph flow
  - Run the enhanced_lead_funnel.ipynb notebook
  - Verify all database saves during form flow work correctly
  - Test session state persistence and retrieval

- [ ] Test API backend integration
  - Start API server: `uv run uvicorn src.api.main:app --reload`
  - Test all API endpoints that use database
  - Verify session management endpoints work correctly

- [ ] Update security and error handling
  - Review security implications of new authentication method
  - Update error messages to not expose authentication details
  - Implement proper connection retry logic

- [ ] Clean up deprecated authentication code
  - Remove old authentication method code
  - Update any configuration files or documentation
  - Remove unused environment variables

- [ ] Update documentation and development commands
  - Update DEVELOPMENT_PLAN.md with new authentication status
  - Update any README or setup instructions
  - Update development command examples if needed

## Success Criteria
- [ ] All database operations work with new authentication
- [ ] Existing notebooks and API continue to function
- [ ] Security compliance improved
- [ ] No degradation in functionality or performance
- [ ] Clean migration with no deprecated code remaining

## Testing Commands
```bash
# Test database connection
uv run python3 -c "from src.database import db; print('✅ DB connected' if db.test_connection() else '❌ DB issue')"

# Test API backend
uv run uvicorn src.api.main:app --reload

# Test notebook functionality
uv run jupyter notebook enhanced_lead_funnel.ipynb
```