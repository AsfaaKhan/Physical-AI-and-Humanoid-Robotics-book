"""Personalization API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from src.database.database import get_db
from src.services.personalization import personalization_service
from src.services.user_profile import user_profile_service
from src.exceptions.auth_exceptions import UserNotFoundException
from src.middleware.auth import get_current_user_id
from pydantic import BaseModel


class PersonalizeContentRequest(BaseModel):
    """Request model for content personalization."""
    content: str
    content_type: str = "text"  # Could be "text", "code", "tutorial", etc.


class PersonalizeContentResponse(BaseModel):
    """Response model for personalized content."""
    original_content: str
    personalized_content: str
    user_background_applied: Dict[str, str]


class GetRecommendationsResponse(BaseModel):
    """Response model for personalization recommendations."""
    learning_path: str
    content_difficulty: str
    recommended_topics: list
    similar_users_count: int


# Create the router
personalization_router = APIRouter()


@personalization_router.post("/personalize", response_model=PersonalizeContentResponse)
async def personalize_content(
    request: PersonalizeContentRequest,
    request_obj: Request,
    db: Session = Depends(get_db)
) -> PersonalizeContentResponse:
    """Personalize content based on user's background information."""
    user_id = get_current_user_id(request_obj)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Get user background for personalization
    user_background = personalization_service.get_user_background_for_personalization(db, user_id)

    # Adapt content based on user background
    personalized_content = personalization_service.adapt_content_for_user(
        db, user_id, request.content
    )

    return PersonalizeContentResponse(
        original_content=request.content,
        personalized_content=personalized_content,
        user_background_applied=user_background
    )


@personalization_router.get("/recommendations", response_model=GetRecommendationsResponse)
async def get_recommendations(
    request_obj: Request,
    db: Session = Depends(get_db)
) -> GetRecommendationsResponse:
    """Get personalized recommendations based on user's background."""
    user_id = get_current_user_id(request_obj)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Get recommendations based on user background
    recommendations = personalization_service.get_personalization_recommendations(db, user_id)

    # Get similar users count
    similar_users = personalization_service.get_user_similarity_group(db, user_id)

    return GetRecommendationsResponse(
        learning_path=recommendations["learning_path"],
        content_difficulty=recommendations["content_difficulty"],
        recommended_topics=recommendations["recommended_topics"],
        similar_users_count=len(similar_users)
    )


@personalization_router.get("/stats")
async def get_personalization_stats(
    request_obj: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get personalization statistics for admin/analysis purposes."""
    # For now, only allow access for development purposes
    # In a real system, you'd have role-based access control here
    user_id = get_current_user_id(request_obj)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    stats = personalization_service.get_personalization_stats(db)

    return stats


@personalization_router.get("/user-background")
async def get_user_background(
    request_obj: Request,
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """Get the current user's background information used for personalization."""
    user_id = get_current_user_id(request_obj)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    background = personalization_service.get_user_background_for_personalization(db, user_id)

    return background