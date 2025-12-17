"""Validation utilities for authentication system."""
from typing import Dict, Any, List
from ..exceptions.auth_exceptions import InvalidInputException


def validate_background_information(background_data: Dict[str, Any]) -> List[str]:
    """
    Validate background information data and return a list of validation errors.

    Args:
        background_data: Dictionary containing background information

    Returns:
        List of validation error messages. Empty list if all validations pass.
    """
    errors = []

    # Define valid values for each field
    valid_software_experience = ['beginner', 'intermediate', 'expert']
    valid_programming_background = ['none', 'basic', 'intermediate', 'advanced']
    valid_hardware_knowledge = ['none', 'basic', 'intermediate', 'advanced']

    # Check required fields exist
    required_fields = ['software_experience', 'programming_background', 'hardware_knowledge']
    for field in required_fields:
        if field not in background_data:
            errors.append(f"Missing required field: {field}")

    # Validate each field if present
    if 'software_experience' in background_data:
        value = background_data['software_experience']
        if value not in valid_software_experience:
            errors.append(f"software_experience must be one of {valid_software_experience}, got: {value}")

    if 'programming_background' in background_data:
        value = background_data['programming_background']
        if value not in valid_programming_background:
            errors.append(f"programming_background must be one of {valid_programming_background}, got: {value}")

    if 'hardware_knowledge' in background_data:
        value = background_data['hardware_knowledge']
        if value not in valid_hardware_knowledge:
            errors.append(f"hardware_knowledge must be one of {valid_hardware_knowledge}, got: {value}")

    return errors


def validate_email_format(email: str) -> bool:
    """
    Validate email format using basic checks.

    Args:
        email: Email string to validate

    Returns:
        True if email format is valid, False otherwise.
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password_strength(password: str) -> List[str]:
    """
    Validate password strength and return a list of validation errors.

    Args:
        password: Password string to validate

    Returns:
        List of validation error messages. Empty list if all validations pass.
    """
    errors = []

    # Check minimum length
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")

    # Check for at least one uppercase letter
    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")

    # Check for at least one lowercase letter
    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")

    # Check for at least one digit
    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one digit")

    # Check for at least one special character
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        errors.append("Password must contain at least one special character")

    return errors


def validate_user_registration_data(email: str, password: str, background: Dict[str, Any]) -> None:
    """
    Validate complete user registration data and raise exception if invalid.

    Args:
        email: User email
        password: User password
        background: Background information

    Raises:
        InvalidInputException: If validation fails
    """
    errors = []

    # Validate email
    if not email:
        errors.append("Email is required")
    elif not validate_email_format(email):
        errors.append("Invalid email format")

    # Validate password
    password_errors = validate_password_strength(password)
    errors.extend(password_errors)

    # Validate background information
    background_errors = validate_background_information(background)
    errors.extend(background_errors)

    # Raise exception if any errors found
    if errors:
        raise InvalidInputException(
            field="registration_data",
            reason="; ".join(errors)
        )


def validate_profile_update_data(background: Dict[str, Any]) -> None:
    """
    Validate profile update data and raise exception if invalid.

    Args:
        background: Background information for update (can be partial)

    Raises:
        InvalidInputException: If validation fails
    """
    errors = []

    # If no background data provided, nothing to validate
    if not background:
        return

    # Define valid values for each field
    valid_software_experience = ['beginner', 'intermediate', 'expert']
    valid_programming_background = ['none', 'basic', 'intermediate', 'advanced']
    valid_hardware_knowledge = ['none', 'basic', 'intermediate', 'advanced']

    # Validate each field if present
    if 'software_experience' in background:
        value = background['software_experience']
        if value not in valid_software_experience:
            errors.append(f"software_experience must be one of {valid_software_experience}, got: {value}")

    if 'programming_background' in background:
        value = background['programming_background']
        if value not in valid_programming_background:
            errors.append(f"programming_background must be one of {valid_programming_background}, got: {value}")

    if 'hardware_knowledge' in background:
        value = background['hardware_knowledge']
        if value not in valid_hardware_knowledge:
            errors.append(f"hardware_knowledge must be one of {hardware_knowledge}, got: {value}")

    # Raise exception if any errors found
    if errors:
        raise InvalidInputException(
            field="background_data",
            reason="; ".join(errors)
        )


def is_valid_software_experience(value: str) -> bool:
    """Check if software experience value is valid."""
    valid_values = ['beginner', 'intermediate', 'expert']
    return value in valid_values


def is_valid_programming_background(value: str) -> bool:
    """Check if programming background value is valid."""
    valid_values = ['none', 'basic', 'intermediate', 'advanced']
    return value in valid_values


def is_valid_hardware_knowledge(value: str) -> bool:
    """Check if hardware knowledge value is valid."""
    valid_values = ['none', 'basic', 'intermediate', 'advanced']
    return value in valid_values