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

- [x] Research new public key authentication method
  - Review Supabase documentation for new authentication patterns
  - Understand migration requirements and breaking changes
  - Document security improvements and compliance benefits

**FINDINGS:**

**New Authentication System (Available Now, Required by Q2/Q3 2025):**

**1. New API Key Types:**
- **Publishable Key** (`sb_publishable_...`) - Replaces `SUPABASE_ANON_KEY`
- **Secret Key** (`sb_secret_...`) - Replaces `SUPABASE_SERVICE_KEY`
- Multiple secret keys can be created per project
- Single publishable key per project (like anon key)

**2. JWT Signing Keys System:**
- **Legacy**: Single shared JWT secret (symmetric HS256)
- **New**: Asymmetric keys (RS256, ES256) or improved shared secrets
- **Benefits**: Local JWT validation, zero-downtime rotation, enhanced security
- **Timeline**: New projects use asymmetric JWTs by default from October 1, 2025

**3. Migration Timeline:**
- **Current Status**: Legacy keys still working, new keys available as opt-in
- **Deadline**: Legacy API keys disabled November 1, 2025
- **No Action Required Until**: At least November 1, 2025
- **Python Client**: supabase-py supports both systems during transition

**4. Security Improvements:**
- Zero-downtime key rotation without forcing user sign-outs
- Better security compliance framework alignment
- Improved performance with local JWT validation
- Enhanced reliability and reduced dependency on central services

**5. Breaking Changes & Compatibility:**
- Secret keys cannot be used in browser environments (same as service keys)
- Some third-party integrations may need updates
- Edge Functions and database type generation may need adjustments
- Realtime connections may have 24-hour session limitations

**6. Migration Requirements:**
- Update client libraries to latest versions
- Replace environment variables: `SUPABASE_ANON_KEY` → `SUPABASE_PUBLISHABLE_KEY`
- Replace `SUPABASE_SERVICE_KEY` → `SUPABASE_SECRET_KEY`
- Update JWT verification logic to use new signing keys
- Test authentication flows with new keys

- [x] Create test cases for authentication functionality
  - Add tests for database connection with current method
  - Add tests for key authentication operations (read, write)
  - Tests should initially pass with current auth, fail with new auth

**IMPLEMENTATION:**

**Test Structure Created:**
- `tests/` - New test directory with comprehensive test suite
- `tests/conftest.py` - Shared fixtures for legacy/new auth environment variables
- `pytest.ini` - Test configuration with custom markers and async support
- Added `pytest` and `pytest-asyncio` dependencies to `pyproject.toml`

**Test Coverage:**
- `test_database_legacy_auth.py` - 10 tests for current authentication (ALL PASSING ✅)
  - Environment variable validation and format checking
  - Client initialization and singleton behavior
  - Connection testing with error detection for "Legacy API keys disabled"
  - CRUD operations (create/read clients, sessions, responses)
  - Connection state management and error handling

- `test_database_new_auth.py` - Tests for new authentication (PROPERLY SKIPPED until implementation)
  - New key format validation (publishable/secret keys)
  - Client initialization with new environment variables
  - Connection and CRUD operations with new auth system
  - Authentication transition and error handling scenarios

- `test_integration_auth.py` - Real database connection tests
  - Legacy auth integration test (PASSES with real DB connection ✅)
  - New auth integration tests (skipped until implementation)
  - Migration compatibility and error recovery tests

**Test Results:**
- **Legacy Authentication**: 10/10 tests passing, real DB connection working
- **New Authentication**: Tests properly skipped with clear implementation markers
- **Key Validation**: Both legacy JWT and new key formats validated correctly
- **Error Detection**: "Legacy API keys disabled" error properly handled

- [x] Update environment variable configuration
  - Add new authentication environment variables to `.env`
  - Update environment variable documentation in DEVELOPMENT_PLAN.md
  - Maintain backward compatibility during transition

**IMPLEMENTATION:**

**Environment Variables Updated:**
- `.env` - New keys added and organized (PUBLISHABLE_KEY, SECRET_KEY)
- `.env.sample` - Updated to reflect new key structure
- Legacy keys retained with deprecation comment for backward compatibility
- Google Maps API key added (empty) for future enhancements

**Documentation Updates:**
- `DEVELOPMENT_PLAN.md` - Updated Environment Variables Status section
  - Clear labeling of new vs legacy authentication systems
  - Migration timeline documented (November 1, 2025 deadline)
  - Backward compatibility status noted
  - Authentication migration status section added

**Key Organization:**
- **New keys first**: SUPABASE_PUBLISHABLE_KEY, SUPABASE_SECRET_KEY
- **Legacy keys deprecated**: SUPABASE_ANON_KEY, SUPABASE_SERVICE_KEY
- Clear deprecation comment: "the below env vars are deprecated"
- Maintained environment integrity during transition period

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