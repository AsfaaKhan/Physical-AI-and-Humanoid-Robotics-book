"""User profile service for managing user background information."""
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from ..models.user import User
from ..exceptions.auth_exceptions import UserNotFoundException
from ..repositories.user_profile import user_profile_repository
from ..utils.validation import validate_background_information


class UserProfileService:
    """Service for managing user profiles and background information."""

    @staticmethod
    def create_profile(db: Session, user_id: str, software_experience: str, programming_background: str, hardware_knowledge: str) -> 'UserProfile':
        """Create a new user profile with background information."""
        # Check if user exists
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise UserNotFoundException(user_id)

        # Validate background information
        background_data = {
            'software_experience': software_experience,
            'programming_background': programming_background,
            'hardware_knowledge': hardware_knowledge
        }
        validation_errors = validate_background_information(background_data)
        if validation_errors:
            from exceptions.auth_exceptions import InvalidInputException
            raise InvalidInputException(field="background", reason="; ".join(validation_errors))

        # Create profile using repository
        return user_profile_repository.create_profile(
            db, user_id, software_experience, programming_background, hardware_knowledge
        )

    @staticmethod
    def get_profile(db: Session, user_id: str) -> Optional['UserProfile']:
        """Get user profile by user ID."""
        return user_profile_repository.get_profile_by_user_id(db, user_id)

    @staticmethod
    def update_profile(db: Session, user_id: str, **updates) -> Optional['UserProfile']:
        """Update user profile with provided fields."""
        # Validate background information if provided
        if updates:
            validation_errors = validate_background_information(updates)
            if validation_errors:
                from exceptions.auth_exceptions import InvalidInputException
                raise InvalidInputException(field="background", reason="; ".join(validation_errors))

        return user_profile_repository.update_profile(db, user_id, **updates)

    @staticmethod
    def get_profile_with_user(db: Session, user_id: str) -> Dict[str, Any]:
        """Get user profile with associated user information."""
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise UserNotFoundException(user_id)

        profile_data = user_profile_repository.get_profile_with_user(db, user_id)

        if not profile_data:
            # User exists but profile doesn't, return user data with empty background
            return {
                "user_id": user.user_id,
                "email": user.email,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
                "is_verified": user.is_verified
            }

        return profile_data

    @staticmethod
    def delete_profile(db: Session, user_id: str) -> bool:
        """Delete user profile (does not delete the user account)."""
        return user_profile_repository.delete_profile(db, user_id)

    @staticmethod
    def validate_background_data(background_data: Dict[str, Any]) -> bool:
        """Validate background information data."""
        validation_errors = validate_background_information(background_data)
        return len(validation_errors) == 0

    @staticmethod
    def get_users_by_background(db: Session, software_experience: Optional[str] = None,
                                programming_background: Optional[str] = None,
                                hardware_knowledge: Optional[str] = None) -> list:
        """Get users filtered by background information."""
        return user_profile_repository.get_users_by_background(
            db, software_experience, programming_background, hardware_knowledge
        )


# Global instance of the UserProfileService
user_profile_service = UserProfileService()