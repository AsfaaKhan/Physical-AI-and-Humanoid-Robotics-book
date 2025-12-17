"""
Utility Functions for RAG Retrieval Validation

This module provides:
- Logging setup
- Helper functions for validation
- Utility functions for inspection
"""

import logging
import time
from typing import Any, Dict, List, Optional
from datetime import datetime


def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    Set up logging configuration.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("rag_retrieval")
    logger.setLevel(getattr(logging, level.upper()))

    # Avoid adding multiple handlers if logger already exists
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def retry_with_backoff(func, max_retries: int = 3, backoff_factor: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Retry a function with exponential backoff.

    Args:
        func: Function to retry
        max_retries: Maximum number of retry attempts
        backoff_factor: Factor for exponential backoff
        exceptions: Tuple of exceptions that trigger retries

    Returns:
        Result of the function if successful

    Raises:
        The last exception if all retries fail
    """
    for attempt in range(max_retries + 1):
        try:
            return func()
        except exceptions as e:
            if attempt == max_retries:
                raise e

            wait_time = backoff_factor * (2 ** attempt)
            time.sleep(wait_time)

    return None  # This line should never be reached


def format_timestamp(timestamp: str) -> str:
    """
    Format a timestamp string for display.

    Args:
        timestamp: ISO format timestamp string

    Returns:
        Formatted timestamp string
    """
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return timestamp


def calculate_similarity_score(text1: str, text2: str) -> float:
    """
    Calculate a basic similarity score between two text strings.
    This is a simplified implementation - in production, use more sophisticated methods.

    Args:
        text1: First text string
        text2: Second text string

    Returns:
        Similarity score between 0.0 and 1.0
    """
    if not text1 or not text2:
        return 0.0

    # Simple word overlap ratio as a basic similarity measure
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = words1.intersection(words2)
    union = words1.union(words2)

    if not union:
        return 0.0

    # Jaccard similarity coefficient
    similarity = len(intersection) / len(union)
    return min(1.0, max(0.0, similarity))


def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing potentially problematic characters.

    Args:
        text: Text to sanitize

    Returns:
        Sanitized text
    """
    if not text:
        return text

    # Remove or replace problematic characters
    sanitized = text.replace('\x00', '')  # Null bytes
    sanitized = sanitized.replace('\r\n', '\n')  # Normalize line endings
    sanitized = sanitized.replace('\r', '\n')  # Normalize line endings

    return sanitized


def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to a maximum length with ellipsis.

    Args:
        text: Text to truncate
        max_length: Maximum length (default: 200)

    Returns:
        Truncated text with ellipsis if truncated
    """
    if not text or len(text) <= max_length:
        return text

    return text[:max_length - 3] + "..."


def validate_json_serializable(obj: Any) -> bool:
    """
    Validate if an object is JSON serializable.

    Args:
        obj: Object to validate

    Returns:
        True if JSON serializable, False otherwise
    """
    import json

    try:
        json.dumps(obj)
        return True
    except (TypeError, ValueError):
        return False


def merge_dicts(dict1: Dict, dict2: Dict, overwrite: bool = True) -> Dict:
    """
    Merge two dictionaries with options for handling conflicts.

    Args:
        dict1: First dictionary
        dict2: Second dictionary to merge
        overwrite: Whether to overwrite values from dict1 with dict2 (default: True)

    Returns:
        Merged dictionary
    """
    merged = dict1.copy()

    for key, value in dict2.items():
        if key in merged and not overwrite:
            continue  # Skip if key exists and overwrite is False
        merged[key] = value

    return merged


def deep_merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Deep merge two dictionaries, merging nested dictionaries recursively.

    Args:
        dict1: First dictionary
        dict2: Second dictionary to merge

    Returns:
        Deep merged dictionary
    """
    import copy

    result = copy.deepcopy(dict1)

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value

    return result


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """
    Flatten a nested dictionary with a separator.

    Args:
        d: Dictionary to flatten
        parent_key: Parent key prefix (used in recursion)
        sep: Separator for nested keys (default: '.')

    Returns:
        Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def extract_keys_with_prefix(data: Dict, prefix: str) -> Dict:
    """
    Extract all keys from a dictionary that start with a given prefix.

    Args:
        data: Dictionary to extract keys from
        prefix: Prefix to match

    Returns:
        Dictionary with only keys that start with the prefix
    """
    return {k: v for k, v in data.items() if k.startswith(prefix)}


def time_it(func):
    """
    Decorator to time function execution.

    Args:
        func: Function to time

    Returns:
        Wrapped function that logs execution time
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper


def batch_process(items: List[Any], batch_size: int, process_func) -> List[Any]:
    """
    Process items in batches.

    Args:
        items: List of items to process
        batch_size: Size of each batch
        process_func: Function to apply to each batch

    Returns:
        List of results from processing each batch
    """
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_result = process_func(batch)
        results.extend(batch_result)
    return results


def get_memory_usage() -> Dict[str, Any]:
    """
    Get current memory usage information.

    Returns:
        Dictionary with memory usage information
    """
    try:
        import psutil # type: ignore
        import os

        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()

        return {
            'rss_bytes': mem_info.rss,  # Resident Set Size
            'vms_bytes': mem_info.vms,  # Virtual Memory Size
            'rss_mb': round(mem_info.rss / 1024 / 1024, 2),
            'vms_mb': round(mem_info.vms / 1024 / 1024, 2),
        }
    except ImportError:
        return {'error': 'psutil not available'}


def clean_text(text: str) -> str:
    """
    Clean and normalize text content by removing extra whitespace and special characters.

    Args:
        text: Raw text to clean

    Returns:
        Cleaned text
    """
    if not text:
        return text

    # Replace multiple whitespaces with single space
    import re
    cleaned = re.sub(r'\s+', ' ', text)

    # Remove leading/trailing whitespace
    cleaned = cleaned.strip()

    # Remove control characters but keep basic punctuation
    cleaned = ''.join(char for char in cleaned if ord(char) >= 32 or char in '\n\r\t')

    return cleaned


def extract_title_from_html(html_content: str) -> str:
    """
    Extract title from HTML content.

    Args:
        html_content: HTML content to extract title from

    Returns:
        Extracted title or empty string if not found
    """
    from bs4 import BeautifulSoup

    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Try multiple methods to find the title
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()

        # Look for h1 as a potential title
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()

        # Look for meta property="og:title"
        og_title = soup.find('meta', property='og:title')
        if og_title:
            return og_title.get('content', '').strip()

        # Look for meta name="title"
        meta_title = soup.find('meta', attrs={'name': 'title'})
        if meta_title:
            return meta_title.get('content', '').strip()

        return ''
    except Exception:
        return ''


def normalize_url(base_url: str, relative_url: str) -> str:
    """
    Normalize a relative URL against a base URL.

    Args:
        base_url: Base URL to resolve against
        relative_url: Relative URL to normalize

    Returns:
        Normalized absolute URL
    """
    from urllib.parse import urljoin

    # Use urljoin to properly resolve relative URLs against the base
    normalized = urljoin(base_url, relative_url.strip())
    return normalized


def create_progress_bar(current: int, total: int, bar_length: int = 50) -> str:
    """
    Create a text-based progress bar.

    Args:
        current: Current progress value
        total: Total value
        bar_length: Length of the progress bar (default: 50)

    Returns:
        Progress bar string
    """
    if total <= 0:
        return ""

    percent = float(current) / total
    filled_length = int(round(bar_length * percent))
    bar = '=' * filled_length + '-' * (bar_length - filled_length)

    return f"[{bar}] {current}/{total} ({percent * 100:.1f}%)"


if __name__ == "__main__":
    # Example usage of utility functions
    logger = setup_logging()
    logger.info("Utils module loaded successfully")

    # Test similarity function
    sim = calculate_similarity_score("hello world", "hello there")
    print(f"Similarity: {sim}")

    # Test truncation
    long_text = "This is a very long text that will be truncated for display purposes."
    truncated = truncate_text(long_text, 30)
    print(f"Truncated: {truncated}")