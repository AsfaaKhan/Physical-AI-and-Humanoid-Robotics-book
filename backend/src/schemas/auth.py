"""Authentication request/response schemas."""
from pydantic import BaseModel, EmailStr, validator
from typing import Dict, Any, Optional
from datetime import datetime


class SignupRequest(BaseModel):
    """Request schema for user signup."""
    email: EmailStr
    password: str
    background: Dict[str, str]  # Contains software_experience, programming_background, hardware_knowledge

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

    @validator('background')
    def validate_background(cls, v):
        required_fields = ['software_experience', 'programming_background', 'hardware_knowledge']
        for field in required_fields:
            if field not in v:
                raise ValueError(f'{field} is required in background')

        # Validate enum values
        software_exp_values = ['beginner', 'intermediate', 'expert']
        prog_back_values = ['none', 'basic', 'intermediate', 'advanced']
        hardware_know_values = ['none', 'basic', 'intermediate', 'advanced']

        if v.get('software_experience') not in software_exp_values:
            raise ValueError(f'software_experience must be one of {software_exp_values}')
        if v.get('programming_background') not in prog_back_values:
            raise ValueError(f'programming_background must be one of {prog_back_values}')
        if v.get('hardware_knowledge') not in hardware_know_values:
            raise ValueError(f'hardware_knowledge must be one of {hardware_know_values}')

        return v


class SigninRequest(BaseModel):
    """Request schema for user signin."""
    email: EmailStr
    password: str


class UpdateProfileRequest(BaseModel):
    """Request schema for profile updates."""
    background: Dict[str, str]

    @validator('background', pre=True)
    def validate_background_update(cls, v):
        if not v:
            return v

        # Allow partial updates, but validate the fields that are provided
        software_exp_values = ['beginner', 'intermediate', 'expert']
        prog_back_values = ['none', 'basic', 'intermediate', 'advanced']
        hardware_know_values = ['none', 'basic', 'intermediate', 'advanced']

        if 'software_experience' in v and v['software_experience'] not in software_exp_values:
            raise ValueError(f'software_experience must be one of {software_exp_values}')
        if 'programming_background' in v and v['programming_background'] not in prog_back_values:
            raise ValueError(f'programming_background must be one of {prog_back_values}')
        if 'hardware_knowledge' in v and v['hardware_knowledge'] not in hardware_know_values:
            raise ValueError(f'hardware_knowledge must be one of {hardware_know_values}')

        return v


class SignupResponse(BaseModel):
    """Response schema for user signup."""
    user_id: str
    email: str
    session_token: str
    profile_complete: bool
    background: Dict[str, str]


class SigninResponse(BaseModel):
    """Response schema for user signin."""
    user_id: str
    email: str
    session_token: str
    background: Optional[Dict[str, str]] = None


class ProfileResponse(BaseModel):
    """Response schema for user profile."""
    user_id: str
    email: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    background: Optional[Dict[str, str]] = None
    profile_completed: Optional[bool] = None
    profile_created_at: Optional[str] = None
    profile_updated_at: Optional[str] = None


class UpdateProfileResponse(BaseModel):
    """Response schema for profile updates."""
    user_id: str
    email: str
    background: Dict[str, str]
    updated_at: str


class SignoutResponse(BaseModel):
    """Response schema for signout."""
    message: str


class RefreshResponse(BaseModel):
    """Response schema for token refresh."""
    session_token: str