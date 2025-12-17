"""User session repository for database operations."""
from sqlalchemy.orm import Session
from typing import Optional, List
from ..models.session import UserSession
from datetime import datetime


class SessionRepository:
    """Repository for user session database operations."""

    @staticmethod
    def create_session(db: Session, user_id: str, token_hash: str, expires_at: datetime) -> UserSession:
        """Create a new user session in the database."""
        session = UserSession(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_session_by_token_hash(db: Session, token_hash: str) -> Optional[UserSession]:
        """Get user session by token hash."""
        return db.query(UserSession).filter(UserSession.token_hash == token_hash).first()

    @staticmethod
    def get_session_by_user_id(db: Session, user_id: str) -> List[UserSession]:
        """Get all sessions for a specific user."""
        return db.query(UserSession).filter(UserSession.user_id == user_id).all()

    @staticmethod
    def validate_session(db: Session, token_hash: str) -> Optional[UserSession]:
        """Validate a session token hash and return the session if valid."""
        session = db.query(UserSession).filter(
            UserSession.token_hash == token_hash,
            UserSession.expires_at > datetime.now()
        ).first()

        if session:
            # Update last accessed time
            session.last_accessed = datetime.now()
            db.commit()
            return session

        return None

    @staticmethod
    def update_session_expiration(db: Session, token_hash: str, new_expires_at: datetime) -> bool:
        """Update session expiration time."""
        session = db.query(UserSession).filter(UserSession.token_hash == token_hash).first()

        if not session:
            return False

        session.expires_at = new_expires_at
        session.last_accessed = datetime.now()
        db.commit()

        return True

    @staticmethod
    def delete_session(db: Session, token_hash: str) -> bool:
        """Delete a user session by token hash."""
        session = db.query(UserSession).filter(UserSession.token_hash == token_hash).first()

        if not session:
            return False

        db.delete(session)
        db.commit()
        return True

    @staticmethod
    def delete_sessions_by_user_id(db: Session, user_id: str) -> int:
        """Delete all sessions for a specific user."""
        sessions = db.query(UserSession).filter(UserSession.user_id == user_id).all()
        count = len(sessions)

        for session in sessions:
            db.delete(session)

        db.commit()
        return count

    @staticmethod
    def cleanup_expired_sessions(db: Session) -> int:
        """Remove all expired sessions from the database."""
        expired_sessions = db.query(UserSession).filter(
            UserSession.expires_at <= datetime.now()
        ).all()

        count = len(expired_sessions)

        for session in expired_sessions:
            db.delete(session)

        db.commit()
        return count

    @staticmethod
    def get_active_sessions_count(db: Session) -> int:
        """Get the count of all active (non-expired) sessions."""
        active_sessions_count = db.query(UserSession).filter(
            UserSession.expires_at > datetime.now()
        ).count()

        return active_sessions_count

    @staticmethod
    def get_sessions_by_user_and_date_range(db: Session, user_id: str, start_date: datetime, end_date: datetime) -> List[UserSession]:
        """Get sessions for a user within a specific date range."""
        return db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.created_at >= start_date,
            UserSession.created_at <= end_date
        ).all()


# Global instance of the SessionRepository
session_repository = SessionRepository()