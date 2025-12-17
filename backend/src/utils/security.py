"""Security utilities for input sanitization and validation."""
import re
import html
from typing import Union, List, Dict, Any, Optional
from bleach import clean as bleach_clean
import unicodedata
from config.settings import settings


def sanitize_input(input_str: str, max_length: int = 1000) -> str:
    """
    Sanitize input string to prevent XSS and other injection attacks.

    Args:
        input_str: Input string to sanitize
        max_length: Maximum allowed length for the string

    Returns:
        Sanitized string
    """
    if not input_str:
        return input_str

    # Limit length
    if len(input_str) > max_length:
        input_str = input_str[:max_length]

    # Normalize Unicode characters
    input_str = unicodedata.normalize('NFKD', input_str)

    # Remove null bytes and other dangerous characters
    input_str = input_str.replace('\0', '')

    # Remove or encode potentially dangerous characters
    # This includes control characters except tab, newline, and carriage return
    input_str = ''.join(char for char in input_str if ord(char) >= 32 or char in '\t\n\r')

    # HTML encode dangerous characters
    input_str = html.escape(input_str)

    return input_str


def sanitize_email(email: str) -> str:
    """
    Sanitize email address input.

    Args:
        email: Email address to sanitize

    Returns:
        Sanitized email address
    """
    if not email:
        return email

    # Basic email validation and sanitization
    email = email.strip().lower()

    # Remove potentially dangerous characters
    email = re.sub(r'[^\w\-\.\+@]', '', email)

    return email


def sanitize_password(password: str) -> str:
    """
    Sanitize password input (basic sanitization, validation should be done separately).

    Args:
        password: Password to sanitize

    Returns:
        Sanitized password
    """
    if not password:
        return password

    # Remove null bytes and normalize
    password = password.replace('\0', '')
    password = unicodedata.normalize('NFKD', password)

    # Only allow printable ASCII characters
    password = ''.join(char for char in password if 32 <= ord(char) <= 126)

    return password


def sanitize_username(username: str) -> str:
    """
    Sanitize username input.

    Args:
        username: Username to sanitize

    Returns:
        Sanitized username
    """
    if not username:
        return username

    # Remove dangerous characters, allow alphanumeric and some common symbols
    username = re.sub(r'[^\w\-.]', '', username)

    # Limit length
    username = username[:50]

    return username


def sanitize_background_field(field_value: str) -> str:
    """
    Sanitize a background field value (software_experience, programming_background, hardware_knowledge).

    Args:
        field_value: Field value to sanitize

    Returns:
        Sanitized field value
    """
    if not field_value:
        return field_value

    # Convert to lowercase and strip whitespace
    field_value = field_value.strip().lower()

    # Only allow alphanumeric and underscore/hyphen
    field_value = re.sub(r'[^\w\-]', '', field_value)

    # Limit length
    field_value = field_value[:20]

    return field_value


def validate_and_sanitize_background_data(background_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate and sanitize background data.

    Args:
        background_data: Background data dictionary

    Returns:
        Sanitized background data dictionary

    Raises:
        ValueError: If invalid values are provided
    """
    if not isinstance(background_data, dict):
        raise ValueError("Background data must be a dictionary")

    valid_software_experience = ['beginner', 'intermediate', 'expert']
    valid_programming_background = ['none', 'basic', 'intermediate', 'advanced']
    valid_hardware_knowledge = ['none', 'basic', 'intermediate', 'advanced']

    sanitized_data = {}

    # Validate and sanitize software experience
    software_exp = background_data.get('software_experience', '').strip().lower()
    if software_exp not in valid_software_experience:
        raise ValueError(f"software_experience must be one of {valid_software_experience}")
    sanitized_data['software_experience'] = software_exp

    # Validate and sanitize programming background
    prog_back = background_data.get('programming_background', '').strip().lower()
    if prog_back not in valid_programming_background:
        raise ValueError(f"programming_background must be one of {valid_programming_background}")
    sanitized_data['programming_background'] = prog_back

    # Validate and sanitize hardware knowledge
    hardware_know = background_data.get('hardware_knowledge', '').strip().lower()
    if hardware_know not in valid_hardware_knowledge:
        raise ValueError(f"hardware_knowledge must be one of {valid_hardware_knowledge}")
    sanitized_data['hardware_knowledge'] = hardware_know

    return sanitized_data


def sanitize_json_input(json_data: Dict[str, Any], max_depth: int = 5) -> Dict[str, Any]:
    """
    Recursively sanitize JSON input to prevent deep nesting and injection.

    Args:
        json_data: JSON data to sanitize
        max_depth: Maximum allowed nesting depth

    Returns:
        Sanitized JSON data
    """
    def _sanitize_recursive(obj, depth=0):
        if depth > max_depth:
            raise ValueError(f"JSON exceeds maximum allowed depth of {max_depth}")

        if isinstance(obj, str):
            return sanitize_input(obj)
        elif isinstance(obj, dict):
            sanitized_dict = {}
            for key, value in obj.items():
                # Sanitize the key
                sanitized_key = sanitize_input(str(key), max_length=100)
                # Sanitize the value
                sanitized_dict[sanitized_key] = _sanitize_recursive(value, depth + 1)
            return sanitized_dict
        elif isinstance(obj, list):
            return [_sanitize_recursive(item, depth + 1) for item in obj]
        else:
            # For non-string, non-container types, return as-is
            return obj

    return _sanitize_recursive(json_data)


def is_safe_redirect_url(target: str, allowed_hosts: List[str]) -> bool:
    """
    Check if a redirect URL is safe to use.

    Args:
        target: Target URL to check
        allowed_hosts: List of allowed hostnames

    Returns:
        True if the URL is safe, False otherwise
    """
    if not target:
        return False

    # Check if it's a relative URL
    if target.startswith('/'):
        return True

    # Parse the URL to check host
    try:
        from urllib.parse import urlparse
        parsed = urlparse(target)

        # Only allow http and https schemes
        if parsed.scheme not in ['http', 'https']:
            return False

        # Check if host is in allowed list
        return parsed.hostname in allowed_hosts
    except Exception:
        return False


def sanitize_sql_like_pattern(pattern: str) -> str:
    """
    Sanitize a string that will be used in a SQL LIKE clause to prevent wildcards abuse.

    Args:
        pattern: Pattern to sanitize

    Returns:
        Sanitized pattern
    """
    if not pattern:
        return pattern

    # Escape SQL LIKE wildcards
    pattern = pattern.replace('\\', '\\\\')  # Escape backslashes first
    pattern = pattern.replace('%', '\\%')    # Escape percent
    pattern = pattern.replace('_', '\\_')    # Escape underscore

    return pattern


def validate_ip_address(ip_address: str) -> bool:
    """
    Validate if the provided string is a valid IP address.

    Args:
        ip_address: IP address string to validate

    Returns:
        True if valid, False otherwise
    """
    if not ip_address:
        return False

    # Check for IPv4
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ipv4_pattern, ip_address):
        parts = ip_address.split('.')
        for part in parts:
            if int(part) > 255:
                return False
        return True

    # Check for IPv6 (simplified)
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::1$|^::$'
    if re.match(ipv6_pattern, ip_address):
        return True

    return False


def sanitize_user_agent(user_agent: str) -> str:
    """
    Sanitize user agent string.

    Args:
        user_agent: User agent string to sanitize

    Returns:
        Sanitized user agent
    """
    if not user_agent:
        return user_agent

    # Limit length
    user_agent = user_agent[:500]

    # Remove null bytes and normalize
    user_agent = user_agent.replace('\0', '')
    user_agent = unicodedata.normalize('NFKD', user_agent)

    # Only allow printable characters
    user_agent = ''.join(char for char in user_agent if 32 <= ord(char) <= 126)

    return user_agent


def validate_content_type(content_type: str) -> bool:
    """
    Validate if the content type is safe and allowed.

    Args:
        content_type: Content type string to validate

    Returns:
        True if valid, False otherwise
    """
    if not content_type:
        return False

    # Define allowed content types
    allowed_types = [
        'text/plain',
        'text/html',
        'application/json',
        'application/xml',
        'text/markdown',
        'text/md',
        'text/x-markdown'
    ]

    # Normalize and check
    content_type = content_type.strip().lower()

    for allowed_type in allowed_types:
        if content_type.startswith(allowed_type):
            return True

    return False


def sanitize_content(content: str, content_type: str = 'text/plain') -> str:
    """
    Sanitize content based on its type.

    Args:
        content: Content to sanitize
        content_type: Type of content

    Returns:
        Sanitized content
    """
    if not content:
        return content

    if content_type == 'text/html':
        # Use bleach to sanitize HTML content
        allowed_tags = ['p', 'br', 'strong', 'em', 'b', 'i', 'u', 'ol', 'ul', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'pre']
        allowed_attributes = {'a': ['href', 'title'], 'img': ['src', 'alt', 'title']}
        return bleach_clean(content, tags=allowed_tags, attributes=allowed_attributes)
    else:
        # For other content types, use basic sanitization
        return sanitize_input(content)