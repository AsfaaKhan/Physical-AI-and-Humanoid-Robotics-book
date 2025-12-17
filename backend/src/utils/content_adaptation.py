"""Content adaptation utilities for personalization based on user background."""

from typing import Dict, Any, List, Optional, Union
from enum import Enum
from dataclasses import dataclass
from config.settings import settings


class ExperienceLevel(Enum):
    """Experience levels for different technical areas."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"
    NONE = "none"
    BASIC = "basic"
    ADVANCED = "advanced"


@dataclass
class ContentAdaptationConfig:
    """Configuration for content adaptation based on user background."""
    software_experience: ExperienceLevel
    programming_background: ExperienceLevel
    hardware_knowledge: ExperienceLevel


class ContentAdaptationEngine:
    """Engine for adapting content based on user background information."""

    def __init__(self):
        # Define adaptation rules for different experience levels
        self.adaptation_rules = {
            ExperienceLevel.BEGINNER: {
                "explanation_depth": "shallow",
                "example_complexity": "simple",
                "terminology_level": "basic",
                "prerequisite_assumption": "none",
                "content_pace": "slow",
                "visual_aids": "high",
                "interactivity": "high"
            },
            ExperienceLevel.INTERMEDIATE: {
                "explanation_depth": "moderate",
                "example_complexity": "moderate",
                "terminology_level": "intermediate",
                "prerequisite_assumption": "basic",
                "content_pace": "moderate",
                "visual_aids": "medium",
                "interactivity": "medium"
            },
            ExperienceLevel.EXPERT: {
                "explanation_depth": "deep",
                "example_complexity": "complex",
                "terminology_level": "advanced",
                "prerequisite_assumption": "advanced",
                "content_pace": "fast",
                "visual_aids": "low",
                "interactivity": "low"
            }
        }

    def adapt_content(self, content: str, config: ContentAdaptationConfig) -> Dict[str, Any]:
        """
        Adapt content based on user background configuration.

        Args:
            content: Original content to adapt
            config: User background configuration

        Returns:
            Dictionary containing adapted content and metadata
        """
        # Determine the primary experience level to guide adaptation
        primary_level = self._determine_primary_experience_level(config)

        # Get adaptation rules for the primary level
        rules = self.adaptation_rules.get(primary_level, self.adaptation_rules[ExperienceLevel.INTERMEDIATE])

        # Apply adaptation rules to content
        adapted_content = self._apply_adaptation_rules(content, rules, config)

        return {
            "original_content": content,
            "adapted_content": adapted_content,
            "adaptation_metadata": {
                "primary_experience_level": primary_level.value,
                "rules_applied": rules,
                "confidence": self._calculate_adaptation_confidence(config)
            }
        }

    def _determine_primary_experience_level(self, config: ContentAdaptationConfig) -> ExperienceLevel:
        """Determine the primary experience level from user background."""
        # Weight different experience areas based on content type
        # For now, we'll use a simple average approach
        levels = [config.software_experience, config.programming_background, config.hardware_knowledge]

        # Convert to numeric values for averaging
        level_values = []
        for level in levels:
            if level in [ExperienceLevel.BEGINNER, ExperienceLevel.NONE]:
                level_values.append(1)
            elif level in [ExperienceLevel.INTERMEDIATE, ExperienceLevel.BASIC]:
                level_values.append(2)
            elif level in [ExperienceLevel.EXPERT, ExperienceLevel.ADVANCED]:
                level_values.append(3)
            else:
                level_values.append(2)  # Default to intermediate

        avg_value = sum(level_values) / len(level_values)

        if avg_value <= 1.33:
            return ExperienceLevel.BEGINNER if config.software_experience == ExperienceLevel.BEGINNER else ExperienceLevel.NONE
        elif avg_value <= 2.33:
            return ExperienceLevel.INTERMEDIATE if config.software_experience in [ExperienceLevel.INTERMEDIATE, ExperienceLevel.BASIC] else ExperienceLevel.BASIC
        else:
            return ExperienceLevel.EXPERT if config.software_experience == ExperienceLevel.EXPERT else ExperienceLevel.ADVANCED

    def _apply_adaptation_rules(self, content: str, rules: Dict[str, Any], config: ContentAdaptationConfig) -> str:
        """Apply adaptation rules to the content."""
        adapted_content = content

        # Adjust content based on rules
        if rules["explanation_depth"] == "shallow":
            # Simplify explanations, remove complex details
            adapted_content = self._simplify_explanation(adapted_content)
        elif rules["explanation_depth"] == "deep":
            # Add more detailed explanations
            adapted_content = self._add_detailed_explanation(adapted_content)

        if rules["terminology_level"] == "basic":
            # Replace advanced terminology with simpler terms
            adapted_content = self._simplify_terminology(adapted_content)
        elif rules["terminology_level"] == "advanced":
            # Add more technical terminology
            adapted_content = self._add_advanced_terminology(adapted_content)

        if rules["example_complexity"] == "simple":
            # Use simpler examples
            adapted_content = self._simplify_examples(adapted_content)
        elif rules["example_complexity"] == "complex":
            # Use more complex examples
            adapted_content = self._add_complex_examples(adapted_content)

        return adapted_content

    def _simplify_explanation(self, content: str) -> str:
        """Simplify explanations for beginners."""
        # Remove advanced concepts, simplify language
        # This is a placeholder - in a real implementation, this would use NLP
        # or content templates to simplify content
        return content

    def _add_detailed_explanation(self, content: str) -> str:
        """Add detailed explanations for experts."""
        # Add more depth, technical details, and advanced concepts
        # This is a placeholder - in a real implementation, this would use NLP
        # or content templates to add detail
        return content

    def _simplify_terminology(self, content: str) -> str:
        """Replace advanced terminology with simpler terms."""
        # Replace complex terms with simpler equivalents
        # This is a placeholder - in a real implementation, this would use
        # a terminology mapping system
        return content

    def _add_advanced_terminology(self, content: str) -> str:
        """Add advanced terminology for experts."""
        # Add more technical terms and jargon
        # This is a placeholder - in a real implementation, this would use
        # a terminology mapping system
        return content

    def _simplify_examples(self, content: str) -> str:
        """Simplify examples for beginners."""
        # Replace complex examples with simpler ones
        # This is a placeholder - in a real implementation, this would use
        # example selection algorithms
        return content

    def _add_complex_examples(self, content: str) -> str:
        """Add complex examples for experts."""
        # Replace simple examples with more complex ones
        # This is a placeholder - in a real implementation, this would use
        # example selection algorithms
        return content

    def _calculate_adaptation_confidence(self, config: ContentAdaptationConfig) -> float:
        """Calculate confidence in the adaptation based on user data."""
        # For now, return a simple confidence based on completeness of data
        confidence = 1.0  # Assume complete data

        if config.software_experience == ExperienceLevel.BEGINNER:
            confidence *= 0.9
        elif config.software_experience == ExperienceLevel.INTERMEDIATE:
            confidence *= 1.0
        elif config.software_experience == ExperienceLevel.EXPERT:
            confidence *= 0.95

        return min(confidence, 1.0)


def adapt_content_for_user(content: str, user_background: Dict[str, str]) -> Dict[str, Any]:
    """
    Convenience function to adapt content for a specific user.

    Args:
        content: Original content to adapt
        user_background: Dictionary with user background data
                        Expected keys: software_experience, programming_background, hardware_knowledge

    Returns:
        Dictionary containing adapted content and metadata
    """
    # Create configuration from user background
    config = ContentAdaptationConfig(
        software_experience=ExperienceLevel(user_background.get('software_experience', 'intermediate')),
        programming_background=ExperienceLevel(user_background.get('programming_background', 'basic')),
        hardware_knowledge=ExperienceLevel(user_background.get('hardware_knowledge', 'basic'))
    )

    # Create and use adaptation engine
    engine = ContentAdaptationEngine()
    return engine.adapt_content(content, config)


def get_personalization_recommendations(user_background: Dict[str, str], available_content: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Get content recommendations based on user background.

    Args:
        user_background: User's background information
        available_content: List of available content items

    Returns:
        List of recommended content items with adaptation metadata
    """
    recommendations = []

    for content_item in available_content:
        adapted_result = adapt_content_for_user(content_item.get('content', ''), user_background)

        recommendations.append({
            'id': content_item.get('id'),
            'title': content_item.get('title'),
            'adapted_content': adapted_result['adapted_content'],
            'relevance_score': calculate_relevance_score(user_background, content_item),
            'adaptation_metadata': adapted_result['adaptation_metadata']
        })

    # Sort by relevance score
    recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
    return recommendations


def calculate_relevance_score(user_background: Dict[str, str], content_metadata: Dict[str, Any]) -> float:
    """
    Calculate relevance score for content based on user background.

    Args:
        user_background: User's background information
        content_metadata: Content metadata including tags, difficulty, etc.

    Returns:
        Relevance score between 0 and 1
    """
    # Calculate relevance based on experience match
    user_exp = user_background.get('software_experience', 'intermediate')
    content_level = content_metadata.get('difficulty', 'intermediate')

    # Simple matching algorithm
    if user_exp == content_level:
        base_score = 0.9
    elif (user_exp == 'beginner' and content_level in ['basic', 'intermediate']) or \
         (user_exp == 'intermediate' and content_level in ['beginner', 'basic', 'advanced']) or \
         (user_exp == 'expert' and content_level in ['intermediate', 'advanced']):
        base_score = 0.7
    else:
        base_score = 0.3

    # Consider content tags vs user interests (if available)
    content_tags = content_metadata.get('tags', [])
    user_interests = user_background.get('interests', [])

    if content_tags and user_interests:
        matching_tags = set(content_tags) & set(user_interests)
        tag_score = len(matching_tags) / len(set(content_tags) | set(user_interests))
        base_score = (base_score + tag_score) / 2

    return min(base_score, 1.0)


# Initialize the content adaptation engine
content_adaptation_engine = ContentAdaptationEngine()