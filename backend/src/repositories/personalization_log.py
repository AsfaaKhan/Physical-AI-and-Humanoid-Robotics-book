"""Repository for PersonalizationLog model operations."""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from backend.src.models.personalization_log import PersonalizationLog
from backend.src.models.user import User
from backend.src.utils.security import sanitize_input


class PersonalizationLogRepository:
    """Repository for PersonalizationLog database operations."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_log(self,
                   user_id: str,
                   event_type: str,
                   content_id: Optional[str] = None,
                   content_type: Optional[str] = None,
                   event_details: Optional[Dict[str, Any]] = None,
                   original_content_id: Optional[str] = None,
                   adapted_content_id: Optional[str] = None,
                   adaptation_strategy: Optional[str] = None,
                   user_background_snapshot: Optional[Dict[str, Any]] = None,
                   interaction_duration: Optional[float] = None,
                   interaction_type: Optional[str] = None,
                   satisfaction_score: Optional[int] = None,
                   feedback: Optional[str] = None,
                   processing_time: Optional[float] = None,
                   confidence_score: Optional[float] = None,
                   ip_address: Optional[str] = None,
                   user_agent: Optional[str] = None,
                   referrer: Optional[str] = None,
                   session_id: Optional[str] = None,
                   is_successful: bool = True,
                   is_test: bool = False) -> PersonalizationLog:
        """
        Create a new personalization log entry.

        Args:
            user_id: ID of the user
            event_type: Type of personalization event
            content_id: ID of the content that was personalized
            content_type: Type of content
            event_details: Additional event details as a dictionary
            original_content_id: Original content ID before personalization
            adapted_content_id: Adapted content ID
            adaptation_strategy: Strategy used for adaptation
            user_background_snapshot: Snapshot of user background as a dictionary
            interaction_duration: Time spent on content in seconds
            interaction_type: Type of interaction
            satisfaction_score: User satisfaction rating (1-5)
            feedback: User feedback text
            processing_time: Time taken to adapt content
            confidence_score: Confidence in personalization (0-1)
            ip_address: User's IP address
            user_agent: User agent string
            referrer: Referring URL
            session_id: Session identifier
            is_successful: Whether the personalization was successful
            is_test: Whether this is a test log

        Returns:
            Created PersonalizationLog instance
        """
        # Sanitize string inputs
        event_type = sanitize_input(event_type, max_length=100) if event_type else event_type
        content_id = sanitize_input(content_id, max_length=255) if content_id else content_id
        content_type = sanitize_input(content_type, max_length=100) if content_type else content_type
        original_content_id = sanitize_input(original_content_id, max_length=255) if original_content_id else original_content_id
        adapted_content_id = sanitize_input(adapted_content_id, max_length=255) if adapted_content_id else adapted_content_id
        adaptation_strategy = sanitize_input(adaptation_strategy, max_length=255) if adaptation_strategy else adaptation_strategy
        interaction_type = sanitize_input(interaction_type, max_length=100) if interaction_type else interaction_type
        feedback = sanitize_input(feedback) if feedback else feedback
        ip_address = sanitize_input(ip_address, max_length=45) if ip_address else ip_address
        user_agent = sanitize_input(user_agent) if user_agent else user_agent
        referrer = sanitize_input(referrer) if referrer else referrer
        session_id = sanitize_input(session_id, max_length=255) if session_id else session_id

        # Convert dictionaries to JSON strings
        import json
        event_details_json = json.dumps(event_details) if event_details else None
        user_background_snapshot_json = json.dumps(user_background_snapshot) if user_background_snapshot else None

        log_entry = PersonalizationLog(
            user_id=user_id,
            event_type=event_type,
            content_id=content_id,
            content_type=content_type,
            event_details=event_details_json,
            original_content_id=original_content_id,
            adapted_content_id=adapted_content_id,
            adaptation_strategy=adaptation_strategy,
            user_background_snapshot=user_background_snapshot_json,
            interaction_duration=interaction_duration,
            interaction_type=interaction_type,
            satisfaction_score=satisfaction_score,
            feedback=feedback,
            processing_time=processing_time,
            confidence_score=confidence_score,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer,
            session_id=session_id,
            is_successful=is_successful,
            is_test=is_test
        )

        self.db_session.add(log_entry)
        self.db_session.flush()  # Get the ID without committing
        return log_entry

    def get_log_by_id(self, log_id: str) -> Optional[PersonalizationLog]:
        """Get a personalization log by its ID."""
        return self.db_session.query(PersonalizationLog).filter(
            PersonalizationLog.id == log_id
        ).first()

    def get_logs_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> List[PersonalizationLog]:
        """Get personalization logs for a specific user."""
        return self.db_session.query(PersonalizationLog).filter(
            PersonalizationLog.user_id == user_id
        ).order_by(desc(PersonalizationLog.created_at)).offset(offset).limit(limit).all()

    def get_logs_by_event_type(self, event_type: str, limit: int = 100, offset: int = 0) -> List[PersonalizationLog]:
        """Get personalization logs by event type."""
        event_type = sanitize_input(event_type, max_length=100)
        return self.db_session.query(PersonalizationLog).filter(
            PersonalizationLog.event_type == event_type
        ).order_by(desc(PersonalizationLog.created_at)).offset(offset).limit(limit).all()

    def get_logs_by_content(self, content_id: str, limit: int = 100, offset: int = 0) -> List[PersonalizationLog]:
        """Get personalization logs for a specific content item."""
        content_id = sanitize_input(content_id, max_length=255)
        return self.db_session.query(PersonalizationLog).filter(
            PersonalizationLog.content_id == content_id
        ).order_by(desc(PersonalizationLog.created_at)).offset(offset).limit(limit).all()

    def get_logs_by_date_range(self, start_date: str, end_date: str, limit: int = 100, offset: int = 0) -> List[PersonalizationLog]:
        """Get personalization logs within a date range."""
        from sqlalchemy import and_
        from datetime import datetime

        start_dt = datetime.fromisoformat(start_date) if isinstance(start_date, str) else start_date
        end_dt = datetime.fromisoformat(end_date) if isinstance(end_date, str) else end_date

        return self.db_session.query(PersonalizationLog).filter(
            and_(
                PersonalizationLog.created_at >= start_dt,
                PersonalizationLog.created_at <= end_dt
            )
        ).order_by(desc(PersonalizationLog.created_at)).offset(offset).limit(limit).all()

    def get_logs_by_user_and_event_type(self, user_id: str, event_type: str, limit: int = 100, offset: int = 0) -> List[PersonalizationLog]:
        """Get personalization logs for a user by event type."""
        event_type = sanitize_input(event_type, max_length=100)
        return self.db_session.query(PersonalizationLog).filter(
            and_(
                PersonalizationLog.user_id == user_id,
                PersonalizationLog.event_type == event_type
            )
        ).order_by(desc(PersonalizationLog.created_at)).offset(offset).limit(limit).all()

    def get_satisfaction_stats_by_user(self, user_id: str) -> Dict[str, Any]:
        """Get satisfaction statistics for a user."""
        from sqlalchemy import func

        stats = self.db_session.query(
            func.avg(PersonalizationLog.satisfaction_score).label('avg_satisfaction'),
            func.count(PersonalizationLog.id).label('total_logs'),
            func.count(PersonalizationLog.satisfaction_score).label('rated_logs')
        ).filter(
            and_(
                PersonalizationLog.user_id == user_id,
                PersonalizationLog.satisfaction_score.isnot(None)
            )
        ).first()

        return {
            'avg_satisfaction': float(stats.avg_satisfaction) if stats.avg_satisfaction else None,
            'total_logs': stats.total_logs or 0,
            'rated_logs': stats.rated_logs or 0
        }

    def get_personalization_stats_by_content(self, content_id: str) -> Dict[str, Any]:
        """Get personalization statistics for a specific content item."""
        from sqlalchemy import func

        content_id = sanitize_input(content_id, max_length=255)
        stats = self.db_session.query(
            func.avg(PersonalizationLog.confidence_score).label('avg_confidence'),
            func.avg(PersonalizationLog.satisfaction_score).label('avg_satisfaction'),
            func.avg(PersonalizationLog.interaction_duration).label('avg_duration'),
            func.count(PersonalizationLog.id).label('total_views')
        ).filter(
            PersonalizationLog.content_id == content_id
        ).first()

        return {
            'avg_confidence': float(stats.avg_confidence) if stats.avg_confidence else None,
            'avg_satisfaction': float(stats.avg_satisfaction) if stats.avg_satisfaction else None,
            'avg_duration': float(stats.avg_duration) if stats.avg_duration else None,
            'total_views': stats.total_views or 0
        }

    def get_logs_by_adaptation_strategy(self, strategy: str, limit: int = 100, offset: int = 0) -> List[PersonalizationLog]:
        """Get personalization logs by adaptation strategy."""
        strategy = sanitize_input(strategy, max_length=255)
        return self.db_session.query(PersonalizationLog).filter(
            PersonalizationLog.adaptation_strategy == strategy
        ).order_by(desc(PersonalizationLog.created_at)).offset(offset).limit(limit).all()

    def get_successful_logs_count(self, user_id: str = None) -> int:
        """Get count of successful personalization logs."""
        query = self.db_session.query(PersonalizationLog)
        if user_id:
            query = query.filter(PersonalizationLog.user_id == user_id)
        query = query.filter(PersonalizationLog.is_successful == True)
        return query.count()

    def get_logs_with_feedback(self, user_id: str = None, limit: int = 100, offset: int = 0) -> List[PersonalizationLog]:
        """Get personalization logs that have user feedback."""
        query = self.db_session.query(PersonalizationLog).filter(
            PersonalizationLog.feedback.isnot(None)
        )
        if user_id:
            query = query.filter(PersonalizationLog.user_id == user_id)
        return query.order_by(desc(PersonalizationLog.created_at)).offset(offset).limit(limit).all()

    def delete_log(self, log_id: str) -> bool:
        """Delete a personalization log by ID."""
        log_entry = self.get_log_by_id(log_id)
        if log_entry:
            self.db_session.delete(log_entry)
            return True
        return False

    def bulk_create_logs(self, logs_data: List[Dict[str, Any]]) -> List[PersonalizationLog]:
        """Create multiple personalization logs at once."""
        log_entries = []
        for log_data in logs_data:
            log_entry = PersonalizationLog(**log_data)
            self.db_session.add(log_entry)
            log_entries.append(log_entry)

        self.db_session.flush()
        return log_entries

    def update_log(self, log_id: str, **kwargs) -> Optional[PersonalizationLog]:
        """Update a personalization log with the provided fields."""
        log_entry = self.get_log_by_id(log_id)
        if log_entry:
            for key, value in kwargs.items():
                if hasattr(log_entry, key):
                    if key in ['event_details', 'user_background_snapshot'] and isinstance(value, dict):
                        import json
                        value = json.dumps(value)
                    elif key in ['event_type', 'content_id', 'content_type', 'adaptation_strategy',
                                'interaction_type', 'feedback', 'ip_address', 'user_agent', 'referrer', 'session_id']:
                        value = sanitize_input(value)
                    setattr(log_entry, key, value)
            return log_entry
        return None