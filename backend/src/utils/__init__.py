"""Utils package combining authentication and general utilities."""

# Import authentication utilities
from .logging import setup_logging as auth_setup_logging, get_logger, log_auth_event, log_security_event, log_personalization_event, log_database_operation, log_rate_limit_event, log_error, log_performance_metric

# Import general RAG utilities from the helpers module
from .helpers import (
    setup_logging as rag_setup_logging,
    retry_with_backoff,
    normalize_url,
    clean_text,
    extract_title_from_html,
    sanitize_text,
    truncate_text,
    calculate_similarity_score,
    validate_json_serializable,
    merge_dicts,
    deep_merge_dicts,
    flatten_dict,
    extract_keys_with_prefix,
    time_it,
    batch_process,
    get_memory_usage,
    create_progress_bar,
    format_timestamp
)

# For setup_logging, we'll use the RAG version as it's more general purpose
setup_logging = rag_setup_logging

__all__ = [
    # Authentication utilities
    "auth_setup_logging",
    "get_logger",
    "log_auth_event",
    "log_security_event",
    "log_personalization_event",
    "log_database_operation",
    "log_rate_limit_event",
    "log_error",
    "log_performance_metric",

    # General utilities
    "setup_logging",
    "retry_with_backoff",
    "normalize_url",
    "clean_text",
    "extract_title_from_html",
    "sanitize_text",
    "truncate_text",
    "calculate_similarity_score",
    "validate_json_serializable",
    "merge_dicts",
    "deep_merge_dicts",
    "flatten_dict",
    "extract_keys_with_prefix",
    "time_it",
    "batch_process",
    "get_memory_usage",
    "create_progress_bar",
    "format_timestamp"
]