"""Session management utilities for authentication system."""
from sqlalchemy.orm import Session
from ..models.user import User, UserProfile
from ..models.session import UserSession
from typing import Optional, Dict, Any
import hashlib
import secrets
from datetime import datetime, timedelta
from config.settings import settings
from ..repositories.session import session_repository


class SessionManager:
    """Manages user sessions including creation, validation, and cleanup."""

    @staticmethod
    def create_session(db: Session, user_id: str, expires_in_minutes: int = None) -> tuple:
        """Create a new user session."""
        if expires_in_minutes is None:
            expires_in_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

        # Generate a secure session token
        session_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(session_token.encode()).hexdigest()

        # Calculate expiration time
        expires_at = datetime.now() + timedelta(minutes=expires_in_minutes)

        # Create session using repository
        session = session_repository.create_session(db, user_id, token_hash, expires_at)

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