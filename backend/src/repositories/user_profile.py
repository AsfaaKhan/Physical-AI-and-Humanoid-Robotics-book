"""User profile repository for database operations."""
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from ..models.user import UserProfile, User
from ..exceptions.auth_exceptions import UserNotFoundException
from datetime import datetime


class UserProfileRepository:
    """Repository for user profile database operations."""

    @staticmethod
    def create_profile(db: Session, user_id: str, software_experience: str, programming_background: str, hardware_knowledge: str) -> UserProfile:
        """Create a new user profile in the database."""
        profile = UserProfile(
            user_id=user_id,
            software_experience=software_experience,
            programming_background=programming_background,
            hardware_knowledge=hardware_knowledge
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def get_profile_by_user_id(db: Session, user_id: str) -> Optional[UserProfile]:
        """Get user profile by user ID."""
        return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    @staticmethod
    def get_profile_with_user(db: Session, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile with associated user information."""
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None

        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

        result = {
            "user_id": user.user_id,
            "email": user.email,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            "is_verified": user.is_verified
        }

        if profile:
            result.update({
                "background": {
                    "software_experience": profile.software_experience,
                    "programming_background": profile.programming_background,
                    "hardware_knowledge": profile.hardware_knowledge
                },
                "profile_completed": profile.profile_completed,
                "profile_created_at": profile.created_at.isoformat() if profile.created_at else None,
                "profile_updated_at": profile.updated_at.isoformat() if profile.updated_at else None
            })

        return result

    @staticmethod
    def update_profile(db: Session, user_id: str, **updates) -> Optional[UserProfile]:
        """Update user profile with provided fields."""
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

        if not profile:
            return None

        # Update allowed fields
        allowed_fields = {
            'software_experience', 'programming_background', 'hardware_knowledge'
        }

        for field, value in updates.items():
            if field in allowed_fields and value is not None:
                setattr(profile, field, value)

        profile.updated_at = datetime.now()

        db.commit()
        db.refresh(profile)

        return profile

    @staticmethod
    def delete_profile(db: Session, user_id: str) -> bool:
        """Delete user profile from the database."""
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

        if not profile:
            return False

        db.delete(profile)
        db.commit()

        return True

    @staticmethod
    def get_users_by_background(db: Session,
                                software_experience: Optional[str] = None,
                                programming_background: Optional[str] = None,
                                hardware_knowledge: Optional[str] = None) -> List[UserProfile]:
        """Get user profiles filtered by background information."""
        query = db.query(UserProfile)

        if software_experience:
            query = query.filter(UserProfile.software_experience == software_experience)

        if programming_background:
            query = query.filter(UserProfile.programming_background == programming_background)

        if hardware_knowledge:
            query = query.filter(UserProfile.hardware_knowledge == hardware_knowledge)

        return query.all()

    @staticmethod
    def get_all_profiles(db: Session, skip: int = 0, limit: int = 100) -> List[UserProfile]:
        """Get all user profiles with pagination."""
        return db.query(UserProfile).offset(skip).limit(limit).all()

    @staticmethod
    def profile_exists(db: Session, user_id: str) -> bool:
        """Check if a user profile exists."""
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        return profile is not None

    @staticmethod
    def get_profile_stats(db: Session) -> Dict[str, Any]:
        """Get statistics about user profiles."""
        total_profiles = db.query(UserProfile).count()

        # Count by software experience
        from sqlalchemy import func
        software_exp_counts = db.query(
            UserProfile.software_experience,
            func.count(UserProfile.user_id)
        ).group_by(UserProfile.software_experience).all()

        # Count by programming background
        prog_back_counts = db.query(
            UserProfile.programming_background,
            func.count(UserProfile.user_id)
        ).group_by(UserProfile.programming_background).all()

        # Count by hardware knowledge
        hardware_know_counts = db.query(
            UserProfile.hardware_knowledge,
            func.count(UserProfile.user_id)
        ).group_by(UserProfile.hardware_knowledge).all()

        return {
            "total_profiles": total_profiles,
            "software_experience_distribution": dict(software_exp_counts),
            "programming_background_distribution": dict(prog_back_counts),
            "hardware_knowledge_distribution": dict(hardware_know_counts)
        }


# Global instance of the UserProfileRepository
user_profile_repository = UserProfileRepository()