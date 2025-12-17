"""User-related database models for authentication system."""
from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from ..database.database import Base
from typing import Optional
import uuid
from datetime import datetime


class User(Base):
    """Core user entity managed by Better Auth but referenced in our system for profile data."""

    __tablename__ = "users"

    user_id = Column(String(255), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_verified = Column(Boolean, default=False)

    def __init__(self, user_id: str = None, email: str = None):
        self.user_id = user_id or str(uuid.uuid4())
        self.email = email
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


class UserProfile(Base):
    """Extended user profile containing background information for personalization."""

    __tablename__ = "user_profiles"

    user_id = Column(String(255), primary_key=True, index=True)
    software_experience = Column(String(20), nullable=False)  # enum: ["beginner", "intermediate", "expert"]
    programming_background = Column(String(20), nullable=False)  # enum: ["none", "basic", "intermediate", "advanced"]
    hardware_knowledge = Column(String(20), nullable=False)  # enum: ["none", "basic", "intermediate", "advanced"]
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    profile_completed = Column(Boolean, default=False)

    def __init__(self, user_id: str, software_experience: str, programming_background: str, hardware_knowledge: str):
        self.user_id = user_id
        self.software_experience = software_experience
        self.programming_background = programming_background
        self.hardware_knowledge = hardware_knowledge
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        # Check if all required background fields are provided to set profile_completed
        if (software_experience and programming_background and hardware_knowledge):
            self.profile_completed = True