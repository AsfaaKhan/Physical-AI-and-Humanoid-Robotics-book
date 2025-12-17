"""Logging utilities for authentication system."""
import logging
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from config.settings import settings


def setup_logging():
    """Set up logging configuration for the authentication system."""
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Create error handler
    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(error_handler)

    # Set specific loggers to appropriate levels
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)  # Reduce SQLAlchemy noise
    logging.getLogger('urllib3').setLevel(logging.WARNING)  # Reduce urllib3 noise
    logging.getLogger('httpx').setLevel(logging.WARNING)  # Reduce httpx noise

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    return logging.getLogger(name)


def log_auth_event(
    event_type: str,
    user_id: Optional[str] = None,
    email: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    success: bool = True,
    details: Optional[Dict[str, Any]] = None
) -> None:
    """Log authentication-related events."""
    logger = get_logger('auth')

    event_data = {
        'event_type': event_type,
        'user_id': user_id,
        'email': email,
        'timestamp': datetime.utcnow().isoformat(),
        'ip_address': ip_address,
        'user_agent': user_agent,
        'success': success,
        'details': details or {}
    }

    log_message = f"AUTH_EVENT: {event_type} - User: {email or user_id} - Success: {success}"

    if success:
        logger.info(log_message, extra=event_data)
    else:
        logger.warning(log_message, extra=event_data)


def log_security_event(
    event_type: str,
    user_id: Optional[str] = None,
    email: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    severity: str = 'medium',
    details: Optional[Dict[str, Any]] = None
) -> None:
    """Log security-related events."""
    logger = get_logger('security')

    event_data = {
        'event_type': event_type,
        'user_id': user_id,
        'email': email,
        'timestamp': datetime.utcnow().isoformat(),
        'ip_address': ip_address,
        'user_agent': user_agent,
        'severity': severity,
        'details': details or {}
    }

    log_message = f"SECURITY_EVENT: {event_type} - Severity: {severity} - User: {email or user_id}"

    if severity.lower() == 'high' or severity.lower() == 'critical':
        logger.error(log_message, extra=event_data)
    elif severity.lower() == 'low':
        logger.info(log_message, extra=event_data)
    else:
        logger.warning(log_message, extra=event_data)


def log_personalization_event(
    event_type: str,
    user_id: str,
    content_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> None:
    """Log personalization-related events."""
    logger = get_logger('personalization')

    event_data = {
        'event_type': event_type,
        'user_id': user_id,
        'content_id': content_id,
        'timestamp': datetime.utcnow().isoformat(),
        'ip_address': ip_address,
        'details': details or {}
    }

    log_message = f"PERSONALIZATION_EVENT: {event_type} - User: {user_id} - Content: {content_id}"

    logger.info(log_message, extra=event_data)


def log_database_operation(
    operation: str,
    table_name: str,
    user_id: Optional[str] = None,
    success: bool = True,
    duration_ms: Optional[float] = None,
    details: Optional[Dict[str, Any]] = None
) -> None:
    """Log database operations."""
    logger = get_logger('database')

    event_data = {
        'operation': operation,
        'table_name': table_name,
        'user_id': user_id,
        'timestamp': datetime.utcnow().isoformat(),
        'success': success,
        'duration_ms': duration_ms,
        'details': details or {}
    }

    log_message = f"DB_OPERATION: {operation} on {table_name} - Success: {success}"
    if duration_ms:
        log_message += f" - Duration: {duration_ms}ms"

    if success:
        logger.debug(log_message, extra=event_data)
    else:
        logger.warning(log_message, extra=event_data)


def log_rate_limit_event(
    endpoint: str,
    user_id: Optional[str] = None,
    email: Optional[str] = None,
    ip_address: Optional[str] = None,
    limit: int = 0,
    window_size: int = 60
) -> None:
    """Log rate limit events."""
    logger = get_logger('rate_limit')

    event_data = {
        'endpoint': endpoint,
        'user_id': user_id,
        'email': email,
        'ip_address': ip_address,
        'timestamp': datetime.utcnow().isoformat(),
        'limit': limit,
        'window_size': window_size
    }

    user_info = email or user_id or "Unknown"
    ip_info = ip_address or "Unknown"
    log_message = f"RATE_LIMIT: {endpoint} - User: {user_info} - IP: {ip_info}"

    logger.warning(log_message, extra=event_data)


def log_error(exception: Exception, context: str = "", extra_data: Optional[Dict[str, Any]] = None) -> None:
    """Log an error with context."""
    logger = get_logger('errors')

    event_data = {
        'context': context,
        'exception_type': type(exception).__name__,
        'timestamp': datetime.utcnow().isoformat(),
        'extra_data': extra_data or {}
    }

    log_message = f"ERROR: {context} - {type(exception).__name__}: {str(exception)}"

    logger.error(log_message, extra=event_data, exc_info=True)


def log_performance_metric(
    metric_name: str,
    value: float,
    unit: str = "",
    user_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> None:
    """Log performance metrics."""
    logger = get_logger('performance')

    event_data = {
        'metric_name': metric_name,
        'value': value,
        'unit': unit,
        'user_id': user_id,
        'timestamp': datetime.utcnow().isoformat(),
        'details': details or {}
    }

    log_message = f"PERFORMANCE: {metric_name} = {value}{unit} - User: {user_id}"

    logger.info(log_message, extra=event_data)


# Initialize logging when module is imported
setup_logging()