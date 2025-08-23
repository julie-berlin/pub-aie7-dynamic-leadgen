"""
Mock Authentication for Testing

IMPORTANT: This file should ONLY be used during development/testing.
Remove or disable before production deployment.
"""

from datetime import datetime
from app.routes.admin_auth import AdminUserResponse

# Test client ID that matches existing test data
TEST_CLIENT_ID = "a1111111-1111-1111-1111-111111111111"  # Pawsome Dog Walking

async def get_mock_admin_user() -> AdminUserResponse:
    """
    Mock admin user for testing without authentication.
    
    WARNING: This bypasses all security. REMOVE IN PRODUCTION!
    """
    return AdminUserResponse(
        id="mock-admin-user-id",
        client_id=TEST_CLIENT_ID,
        email="test@example.com",
        first_name="Test",
        last_name="Admin",
        role="admin",
        permissions=["read", "write", "delete"],
        is_active=True,
        email_verified=True,
        last_login_at=None,
        login_count=0,
        created_at=datetime.now()
    )