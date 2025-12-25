"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from src.database.database import get_db
from src.models.user import User, UserProfile
from src.models.session import UserSession
from src.database.session_manager import SessionManager
from src.utils.auth import create_access_token, create_refresh_token, verify_password, hash_password
from src.exceptions.auth_exceptions import (
    UserNotFoundException,
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    InvalidInputException
)
from src.services.user_profile import user_profile_service
from src.services.better_auth import better_auth_client
from src.schemas.auth import SignupRequest, SigninRequest, UpdateProfileRequest, SignupResponse, SigninResponse, SignoutResponse, RefreshResponse, ProfileResponse, UpdateProfileResponse
from datetime import datetime, timedelta
import uuid
import re


# Create the router
auth_router = APIRouter()


@auth_router.post("/auth/signup", status_code=status.HTTP_201_CREATED, response_model=SignupResponse)
async def signup(request: SignupRequest, db: Session = Depends(get_db)) -> SignupResponse:
    """Register a new user with background information."""
    # Check if user already exists in Better Auth first
    try:
        # Check if user exists in our system
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            # User already exists in our database
            raise EmailAlreadyExistsException(request.email)

        # Try to get user from Better Auth service to check if they already exist there
        # If user exists in Better Auth but not in our DB, we can link them
        # But for signup, we'll create in Better Auth first
        better_auth_response = better_auth_client.create_user(
            email=request.email,
            password=request.password,
            user_data={"name": request.email.split("@")[0]}  # Extract name from email as default
        )

        # Use the user ID from Better Auth
        user_id = better_auth_response.get("id")

        # Check if user already exists in our database (using the Better Auth user ID)
        existing_user_by_id = db.query(User).filter(User.user_id == user_id).first()
        if existing_user_by_id:
            # User already exists, shouldn't happen during signup but just in case
            raise EmailAlreadyExistsException(request.email)

        # Create user in our system to store additional profile data
        user = User(user_id=user_id, email=request.email)
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create user profile with background information using the service
        profile = user_profile_service.create_profile(
            db,
            user_id=user_id,
            software_experience=request.background['software_experience'],
            programming_background=request.background['programming_background'],
            hardware_knowledge=request.background['hardware_knowledge']
        )

        # Create access token
        access_token_expires = timedelta(minutes=30)  # Use settings value in real implementation
        access_token = create_access_token(
            data={"sub": user_id, "email": user.email},
            expires_delta=access_token_expires
        )

        # Create session
        session, session_token = SessionManager.create_session(db, user_id)

        return {
            "user_id": user_id,
            "email": user.email,
            "session_token": session_token,  # In real implementation, you might return the access_token
            "profile_complete": True,
            "background": {
                "software_experience": profile.software_experience,
                "programming_background": profile.programming_background,
                "hardware_knowledge": profile.hardware_knowledge
            }
        }
    except EmailAlreadyExistsException:
        raise
    except Exception as e:
        # Rollback transaction on error
        db.rollback()
        raise e


@auth_router.post("/auth/signin", response_model=SigninResponse)
async def signin(request: SigninRequest, db: Session = Depends(get_db)) -> SigninResponse:
    """Authenticate existing user."""
    try:
        # Verify credentials with Better Auth service
        better_auth_response = better_auth_client.verify_user_password(
            email=request.email,
            password=request.password
        )

        if not better_auth_response or "user" not in better_auth_response:
            raise InvalidCredentialsException()

        user_data = better_auth_response["user"]
        user_id = user_data["id"]
        email = user_data["email"]

        # Find user in our system by Better Auth user ID
        user = db.query(User).filter(User.user_id == user_id).first()

        if user:
            # User exists, update lastLoginAt
            user.last_login_at = datetime.utcnow()
            db.commit()
            db.refresh(user)

            # Get user profile using the service
            profile = user_profile_service.get_profile(db, user.user_id)
        else:
            # User does not exist in our system, create user record as fallback
            user = User(user_id=user_id, email=email)
            db.add(user)
            db.commit()
            db.refresh(user)

            # User is new to our system, profile may not exist yet
            profile = user_profile_service.get_profile(db, user.user_id)

        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.user_id, "email": user.email},
            expires_delta=access_token_expires
        )

        # Create session
        session, session_token = SessionManager.create_session(db, user.user_id)

        result = {
            "user_id": user.user_id,
            "email": user.email,
            "session_token": session_token,  # In real implementation, you might return the access_token
        }

        if profile:
            result["background"] = {
                "software_experience": profile.software_experience,
                "programming_background": profile.programming_background,
                "hardware_knowledge": profile.hardware_knowledge
            }

        return result
    except Exception as e:
        # Rollback transaction on error
        db.rollback()
        raise e


@auth_router.post("/auth/signout", response_model=SignoutResponse)
async def signout(request: Request, db: Session = Depends(get_db)) -> SignoutResponse:
    """End current user session."""
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Get token from authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )

    token = auth_header[7:]  # Remove "Bearer " prefix

    # Delete the session
    success = SessionManager.delete_session(db, token)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )

    return {"message": "Successfully signed out"}


@auth_router.get("/auth/profile", response_model=ProfileResponse)
async def get_profile(request: Request, db: Session = Depends(get_db)) -> ProfileResponse:
    """Get current user profile."""
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Get user profile with user info using the service
    result = user_profile_service.get_profile_with_user(db, user_id)

    return result


@auth_router.put("/auth/profile", response_model=UpdateProfileResponse)
async def update_profile(
    request: UpdateProfileRequest,
    request_obj: Request,
    db: Session = Depends(get_db)
) -> UpdateProfileResponse:
    """Update user profile including background information."""
    user_id = getattr(request_obj.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Update profile using the service
    profile = user_profile_service.update_profile(
        db,
        user_id,
        **request.background
    )

    if not profile:
        raise UserNotFoundException(user_id)

    # Get user info for response
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise UserNotFoundException(user_id)

    return {
        "user_id": user.user_id,
        "email": user.email,
        "background": {
            "software_experience": profile.software_experience,
            "programming_background": profile.programming_background,
            "hardware_knowledge": profile.hardware_knowledge
        },
        "updated_at": profile.updated_at.isoformat()
    }


@auth_router.post("/auth/refresh", response_model=RefreshResponse)
async def refresh_token(request: Request, db: Session = Depends(get_db)) -> RefreshResponse:
    """Refresh authentication token."""
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Create new access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user_id, "email": getattr(request.state, 'user_email', None)},
        expires_delta=access_token_expires
    )

    return {"session_token": access_token}