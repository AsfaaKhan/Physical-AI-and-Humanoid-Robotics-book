"""Simplified Better Auth integration service for development."""
from typing import Dict, Any, Optional
from config.settings import settings
import logging
import hashlib

logger = logging.getLogger(__name__)


class SimpleBetterAuthClient:
    """Simplified synchronous client for Better Auth service (development version)."""

    def __init__(self):
        self.base_url = settings.BETTER_AUTH_URL
        self.secret = settings.BETTER_AUTH_SECRET

    def create_user(self, email: str, password: str, user_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new user in Better Auth (simplified for development)."""
        if not self.base_url or not self.secret:
            # In development, simulate the API call
            logger.info(f"Better Auth not configured, simulating user creation for {email}")
            user_id = f"dev_{email.split('@')[0]}_{abs(hash(email)) % 10000}"
            return {
                "id": user_id,
                "email": email,
                "emailVerified": True,
                "createdAt": "2025-12-16T22:50:00.000Z",
                "updatedAt": "2025-12-16T22:50:00.000Z"
            }

        # In production, this would make actual API calls
        # For now, we return an error to indicate that proper configuration is needed
        raise Exception("Better Auth service not configured for production use")

    def verify_user_password(self, email: str, password: str) -> Dict[str, Any]:
        """Verify user credentials with Better Auth (simplified for development)."""
        if not self.base_url or not self.secret:
            # In development, simulate the API call
            logger.info(f"Better Auth not configured, simulating user verification for {email}")
            user_id = f"dev_{email.split('@')[0]}_{abs(hash(email)) % 10000}"
            return {
                "user": {
                    "id": user_id,
                    "email": email,
                    "emailVerified": True,
                    "createdAt": "2025-12-16T22:50:00.000Z",
                    "updatedAt": "2025-12-16T22:50:00.000Z"
                },
                "session": {
                    "id": f"session_{abs(hash(email)) % 10000}",
                    "userId": user_id,
                    "expiresAt": "2025-12-17T22:50:00.000Z"
                }
            }

        # In production, this would make actual API calls
        raise Exception("Better Auth service not configured for production use")

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information from Better Auth (simplified for development)."""
        if not self.base_url or not self.secret:
            # In development, simulate the API call
            logger.info(f"Better Auth not configured, simulating user retrieval for {user_id}")
            return {
                "id": user_id,
                "email": f"user_{user_id}@example.com",
                "emailVerified": True,
                "createdAt": "2025-12-16T22:50:00.000Z",
                "updatedAt": "2025-12-16T22:50:00.000Z"
            }

        # In production, this would make actual API calls
        raise Exception("Better Auth service not configured for production use")

    def revoke_session(self, session_id: str) -> bool:
        """Revoke a user session in Better Auth (simplified for development)."""
        if not self.base_url or not self.secret:
            # In development, simulate the API call
            logger.info(f"Better Auth not configured, simulating session revocation for {session_id}")
            return True

        # In production, this would make actual API calls
        raise Exception("Better Auth service not configured for production use")

    def sign_out(self, user_id: str) -> bool:
        """Sign out user from Better Auth (simplified for development)."""
        if not self.base_url or not self.secret:
            # In development, simulate the API call
            logger.info(f"Better Auth not configured, simulating sign out for {user_id}")
            return True

        # In production, this would make actual API calls
        raise Exception("Better Auth service not configured for production use")


# Global instance of the SimpleBetterAuthClient
better_auth_client = SimpleBetterAuthClient()