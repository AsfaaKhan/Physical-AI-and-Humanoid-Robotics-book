"""Session-related database models for authentication system."""
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from ..database.database import Base
from typing import Optional
import uuid
from datetime import datetime


class UserSession(Base):
    """Session management for authenticated users, tracking active sessions."""

    __tablename__ = "user_sessions"

    session_id = Column(String(255), primary_key=True, index=True)
    user_id = Column(String(255), index=True, nullable=False)  # Reference to user
    token_hash = Column(String(255), nullable=False)  # Hashed session token for security
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_accessed = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    user_agent = Column(Text)  # Client information for security
    ip_address = Column(String(45))  # IP address for security tracking

    def __init__(self, session_id: str = None, user_id: str = None, token_hash: str = None, expires_at: datetime = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.user_id = user_id
        self.token_hash = token_hash
        self.expires_at = expires_at
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()