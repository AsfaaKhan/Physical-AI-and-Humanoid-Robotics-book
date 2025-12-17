"""User session service for managing user sessions."""
from sqlalchemy.orm import Session
from typing import Optional
from models.session import UserSession
from repositories.session import session_repository
from utils.auth import create_access_token, create_refresh_token
from datetime import timedelta, datetime
import secrets
import hashlib
from config.settings import settings


class UserSessionService:
    """Service for managing user sessions."""

    @staticmethod
    def create_session(db: Session, user_id: str, expires_in_minutes: Optional[int] = None) -> tuple:
        """Create a new user session and return both the session and token."""
        if expires_in_minutes is None:
            expires_in_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

        # Generate a secure session token
        session_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(session_token.encode()).hexdigest()

        # Calculate expiration time
        expires_at = datetime.now() + timedelta(minutes=expires_in_minutes)

        # Create session using repository
        session = session_repository.create_session(
            db, user_id, token_hash, expires_at
        )

        return session, session_token

    @staticmethod
    def validate_session(db: Session, session_token: str) -> Optional[UserSession]:
        """Validate a session token and return the session if valid."""
        if not session_token:
            return None

        # Hash the provided token to compare with stored hash
        token_hash = hashlib.sha256(session_token.encode()).hexdigest()

        # Validate session using repository
        return session_repository.validate_session(db, token_hash)

    @staticmethod
    def delete_session(db: Session, session_token: str) -> bool:
        """Delete a user session."""
        if not session_token:
            return False

        token_hash = hashlib.sha256(session_token.encode()).hexdigest()

        return session_repository.delete_session(db, token_hash)

    @staticmethod
    def cleanup_expired_sessions(db: Session) -> int:
        """Remove all expired sessions from the database."""
        return session_repository.cleanup_expired_sessions(db)

    @staticmethod
    def get_session_by_user_id(db: Session, user_id: str) -> list:
        """Get all sessions for a specific user."""
        return session_repository.get_sessions_by_user_id(db, user_id)

    @staticmethod
    def revoke_all_user_sessions(db: Session, user_id: str) -> int:
        """Revoke all sessions for a specific user."""
        return session_repository.delete_sessions_by_user_id(db, user_id)

    @staticmethod
    def extend_session(db: Session, session_token: str, additional_minutes: int = None) -> bool:
        """Extend an existing session."""
        if additional_minutes is None:
            additional_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

        if not session_token:
            return False

        token_hash = hashlib.sha256(session_token.encode()).hexdigest()

        # Calculate new expiration time
        new_expires_at = datetime.now() + timedelta(minutes=additional_minutes)

        return session_repository.update_session_expiration(db, token_hash, new_expires_at)


# Global instance of the UserSessionService
user_session_service = UserSessionService()