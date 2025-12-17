"""Database model for tracking personalization events and user interactions."""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional
import uuid
from backend.src.database.database import Base


class PersonalizationLog(Base):
    """Model for tracking personalization events and user interactions."""

    __tablename__ = "personalization_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    content_id = Column(String(255), nullable=True, index=True)  # ID of the content that was personalized
    content_type = Column(String(100), nullable=True)  # Type of content (article, video, etc.)

    # Event details
    event_type = Column(String(100), nullable=False)  # 'content_view', 'recommendation_shown', 'content_interaction', etc.
    event_details = Column(Text, nullable=True)  # JSON string with additional event details

    # Personalization details
    original_content_id = Column(String(255), nullable=True)  # Original content before personalization
    adapted_content_id = Column(String(255), nullable=True)  # Adapted content ID
    adaptation_strategy = Column(String(255), nullable=True)  # Strategy used for adaptation
    user_background_snapshot = Column(Text, nullable=True)  # JSON snapshot of user background at time of personalization

    # Interaction data
    interaction_duration = Column(Float, nullable=True)  # Time spent on personalized content in seconds
    interaction_type = Column(String(100), nullable=True)  # 'view', 'click', 'scroll', 'time_spent', etc.
    satisfaction_score = Column(Integer, nullable=True)  # User satisfaction rating (1-5)
    feedback = Column(Text, nullable=True)  # User feedback text

    # Performance metrics
    processing_time = Column(Float, nullable=True)  # Time taken to adapt content in seconds
    confidence_score = Column(Float, nullable=True)  # Confidence in personalization (0-1)

    # Metadata
    ip_address = Column(String(45), nullable=True)  # User's IP address
    user_agent = Column(Text, nullable=True)  # User agent string
    referrer = Column(Text, nullable=True)  # Referring URL
    session_id = Column(String(255), nullable=True)  # Session identifier

    # Flags
    is_successful = Column(Boolean, default=True)  # Whether the personalization was successful
    is_test = Column(Boolean, default=False)  # Whether this is a test log

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="personalization_logs")

    def __repr__(self):
        return f"<PersonalizationLog(id='{self.id}', user_id='{self.user_id}', event_type='{self.event_type}', created_at='{self.created_at}')>"

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content_id': self.content_id,
            'content_type': self.content_type,
            'event_type': self.event_type,
            'event_details': self.event_details,
            'original_content_id': self.original_content_id,
            'adapted_content_id': self.adapted_content_id,
            'adaptation_strategy': self.adaptation_strategy,
            'user_background_snapshot': self.user_background_snapshot,
            'interaction_duration': self.interaction_duration,
            'interaction_type': self.interaction_type,
            'satisfaction_score': self.satisfaction_score,
            'feedback': self.feedback,
            'processing_time': self.processing_time,
            'confidence_score': self.confidence_score,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'referrer': self.referrer,
            'session_id': self.session_id,
            'is_successful': self.is_successful,
            'is_test': self.is_test,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }