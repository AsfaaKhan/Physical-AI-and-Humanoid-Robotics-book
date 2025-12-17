"""Personalization service for content adaptation based on user background."""
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from ..models.user import UserProfile
from ..repositories.user_profile import user_profile_repository
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class PersonalizationService:
    """Service for personalizing content based on user background information."""

    @staticmethod
    def get_user_background_for_personalization(db: Session, user_id: str) -> Dict[str, Any]:
        """Get user background information formatted for personalization."""
        profile = user_profile_repository.get_profile_by_user_id(db, user_id)

        if not profile:
            # Return default values if no profile exists
            return {
                "software_experience": "beginner",
                "programming_background": "none",
                "hardware_knowledge": "none"
            }

        return {
            "software_experience": profile.software_experience,
            "programming_background": profile.programming_background,
            "hardware_knowledge": profile.hardware_knowledge
        }

    @staticmethod
    def adapt_content_for_user(db: Session, user_id: str, content: str) -> str:
        """Adapt content based on user's background information."""
        user_background = PersonalizationService.get_user_background_for_personalization(db, user_id)

        # Apply content adaptation based on user background
        adapted_content = content

        # Adjust complexity based on software experience
        if user_background["software_experience"] == "beginner":
            adapted_content = PersonalizationService._simplify_content(adapted_content)
        elif user_background["software_experience"] == "expert":
            adapted_content = PersonalizationService._enhance_content(adapted_content)

        # Adjust technical depth based on programming background
        if user_background["programming_background"] in ["none", "basic"]:
            adapted_content = PersonalizationService._reduce_technical_jargon(adapted_content)
        elif user_background["programming_background"] in ["intermediate", "advanced"]:
            adapted_content = PersonalizationService._add_technical_details(adapted_content)

        # Adjust hardware-related content based on hardware knowledge
        if user_background["hardware_knowledge"] in ["none", "basic"]:
            adapted_content = PersonalizationService._simplify_hardware_content(adapted_content)
        elif user_background["hardware_knowledge"] in ["intermediate", "advanced"]:
            adapted_content = PersonalizationService._add_hardware_details(adapted_content)

        return adapted_content

    @staticmethod
    def _simplify_content(content: str) -> str:
        """Simplify content for beginners."""
        # Add more explanations and simpler examples
        simplified = content.replace("advanced concept", "concept")
        simplified = simplified.replace("complex implementation", "implementation")
        # Add beginner-friendly explanations
        return f"[Beginner-friendly explanation] {simplified}"

    @staticmethod
    def _enhance_content(content: str) -> str:
        """Enhance content for experts."""
        # Add more depth and advanced examples
        enhanced = content.replace("basic approach", "advanced approach")
        # Add expert-level insights
        return f"[Expert insight] {enhanced}"

    @staticmethod
    def _reduce_technical_jargon(content: str) -> str:
        """Reduce technical jargon for users with basic programming background."""
        # Replace technical terms with simpler explanations
        jargon_reduced = content.replace("asynchronous", "non-blocking")
        jargon_reduced = jargon_reduced.replace("polymorphism", "the ability to use the same interface for different underlying data types")
        return jargon_reduced

    @staticmethod
    def _add_technical_details(content: str) -> str:
        """Add technical details for users with advanced programming background."""
        # Add technical specifics
        detailed = f"{content} [Technical detail: This implementation uses best practices for performance and security.]"
        return detailed

    @staticmethod
    def _simplify_hardware_content(content: str) -> str:
        """Simplify hardware-related content."""
        # Replace complex hardware terms
        simplified_hw = content.replace("field-programmable gate array", "programmable hardware chip")
        return simplified_hw

    @staticmethod
    def _add_hardware_details(content: str) -> str:
        """Add hardware details for advanced users."""
        # Add hardware-specific information
        detailed_hw = f"{content} [Hardware specification: Compatible with ARM64 architecture, minimum 2GB RAM recommended.]"
        return detailed_hw

    @staticmethod
    def get_personalization_recommendations(db: Session, user_id: str) -> Dict[str, Any]:
        """Get personalized recommendations based on user background."""
        user_background = PersonalizationService.get_user_background_for_personalization(db, user_id)

        recommendations = {
            "learning_path": PersonalizationService._get_learning_path(user_background),
            "content_difficulty": PersonalizationService._get_content_difficulty(user_background),
            "recommended_topics": PersonalizationService._get_recommended_topics(user_background)
        }

        return recommendations

    @staticmethod
    def _get_learning_path(user_background: Dict[str, Any]) -> str:
        """Determine the appropriate learning path."""
        if user_background["software_experience"] == "beginner":
            return "foundations_first"
        elif user_background["programming_background"] in ["none", "basic"]:
            return "programming_focused"
        elif user_background["hardware_knowledge"] in ["none", "basic"]:
            return "hardware_introduction"
        else:
            return "advanced_concepts"

    @staticmethod
    def _get_content_difficulty(user_background: Dict[str, Any]) -> str:
        """Determine appropriate content difficulty."""
        exp_level = user_background["software_experience"]
        if exp_level == "beginner":
            return "basic"
        elif exp_level == "intermediate":
            return "intermediate"
        else:
            return "advanced"

    @staticmethod
    def _get_recommended_topics(user_background: Dict[str, Any]) -> List[str]:
        """Get recommended topics based on user background."""
        topics = []

        if user_background["software_experience"] == "beginner":
            topics.extend(["fundamentals", "basic_concepts"])
        if user_background["programming_background"] in ["none", "basic"]:
            topics.append("programming_introduction")
        if user_background["hardware_knowledge"] in ["none", "basic"]:
            topics.append("hardware_basics")

        return topics

    @staticmethod
    def get_user_similarity_group(db: Session, user_id: str) -> List[str]:
        """Get other users with similar background for comparison."""
        user_profile = user_profile_repository.get_profile_by_user_id(db, user_id)
        if not user_profile:
            return []

        # Find users with similar backgrounds
        similar_users = user_profile_repository.get_users_by_background(
            db,
            software_experience=user_profile.software_experience,
            programming_background=user_profile.programming_background,
            hardware_knowledge=user_profile.hardware_knowledge
        )

        # Return user IDs of similar users (excluding the current user)
        similar_user_ids = [profile.user_id for profile in similar_users if profile.user_id != user_id]

        return similar_user_ids

    @staticmethod
    def get_personalization_stats(db: Session) -> Dict[str, Any]:
        """Get statistics about personalization usage."""
        profile_stats = user_profile_repository.get_profile_stats(db)

        return {
            "total_users_with_profiles": profile_stats["total_profiles"],
            "software_experience_distribution": profile_stats["software_experience_distribution"],
            "programming_background_distribution": profile_stats["programming_background_distribution"],
            "hardware_knowledge_distribution": profile_stats["hardware_knowledge_distribution"]
        }


# Global instance of the PersonalizationService
personalization_service = PersonalizationService()