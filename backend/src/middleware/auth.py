"""Authentication middleware for FastAPI."""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..utils.auth import verify_access_token
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class JWTBearer(HTTPBearer):
    """JWT Bearer token authentication middleware."""

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        """Validate the JWT token in the request."""
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme."
                )

            token = credentials.credentials
            token_data = verify_access_token(token)

            if token_data is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token."
                )

            # Add user info to request state
            request.state.user_id = token_data.get("sub")
            request.state.user_email = token_data.get("email")
            request.state.scopes = token_data.get("scopes", [])

            return token
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code."
            )


def get_current_user_id(request: Request) -> Optional[str]:
    """Get the current user ID from the request state."""
    return getattr(request.state, 'user_id', None)


def get_current_user_email(request: Request) -> Optional[str]:
    """Get the current user email from the request state."""
    return getattr(request.state, 'user_email', None)


# Additional middleware for role-based access control if needed
class RoleChecker:
    """Role-based access control middleware."""

    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, request: Request):
        user_roles = getattr(request.state, 'scopes', [])
        if not any(role in self.allowed_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )