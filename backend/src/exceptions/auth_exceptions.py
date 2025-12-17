"""Custom exceptions for authentication system."""
from fastapi import HTTPException, status
from typing import Dict, Any, Optional


class AuthException(HTTPException):
    """Base authentication exception."""

    def __init__(self, detail: str, status_code: int = status.HTTP_401_UNAUTHORIZED, error_code: Optional[str] = None):
        super().__init__(
            status_code=status_code,
            detail={
                "error": {
                    "code": error_code or "AUTH_ERROR",
                    "message": detail,
                    "details": {}
                }
            }
        )
        self.error_code = error_code


class UserNotFoundException(AuthException):
    """Exception raised when user is not found."""

    def __init__(self, user_id: str = None):
        detail = f"User not found"
        if user_id:
            detail = f"User with ID {user_id} not found"
        super().__init__(
            detail=detail,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="USER_NOT_FOUND"
        )


class EmailAlreadyExistsException(AuthException):
    """Exception raised when email already exists."""

    def __init__(self, email: str):
        super().__init__(
            detail=f"Email {email} already registered",
            status_code=status.HTTP_409_CONFLICT,
            error_code="EMAIL_EXISTS"
        )


class InvalidCredentialsException(AuthException):
    """Exception raised when credentials are invalid."""

    def __init__(self):
        super().__init__(
            detail="Invalid credentials",
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="INVALID_CREDENTIALS"
        )


class InvalidTokenException(AuthException):
    """Exception raised when token is invalid or expired."""

    def __init__(self):
        super().__init__(
            detail="Invalid or expired token",
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="INVALID_TOKEN"
        )


class InsufficientPermissionsException(AuthException):
    """Exception raised when user doesn't have sufficient permissions."""

    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="INSUFFICIENT_PERMISSIONS"
        )


class PasswordValidationException(AuthException):
    """Exception raised when password validation fails."""

    def __init__(self, detail: str = "Password does not meet requirements"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="INVALID_PASSWORD"
        )


class ProfileIncompleteException(AuthException):
    """Exception raised when user profile is incomplete."""

    def __init__(self, detail: str = "User profile is incomplete"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="PROFILE_INCOMPLETE"
        )


class RateLimitExceededException(AuthException):
    """Exception raised when rate limit is exceeded."""

    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMITED"
        )


class InvalidInputException(AuthException):
    """Exception raised when input validation fails."""

    def __init__(self, field: str = None, reason: str = None):
        detail = "Invalid input data"
        error_details = {}

        if field:
            error_details["field"] = field
        if reason:
            error_details["reason"] = reason

        super().__init__(
            detail={
                "error": {
                    "code": "INVALID_INPUT",
                    "message": detail,
                    "details": error_details
                }
            },
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="INVALID_INPUT"
        )


def create_error_response(error_code: str, message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create a standardized error response."""
    error_response = {
        "error": {
            "code": error_code,
            "message": message,
            "details": details or {}
        }
    }
    return error_response