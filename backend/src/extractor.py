"""
Extractor module for extracting clean textual content from URLs.
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from config.settings import settings
from src.utils import setup_logging, retry_with_backoff, clean_text, extract_title_from_html


logger = setup_logging()


@dataclass
class ContentChunk:
    """
    Represents a semantically coherent segment of extracted text with metadata.
    Based on data-model.md specifications.
    """
    id: str
    text_content: str
    source_url: str
    page_title: str
    chunk_index: int
    created_at: str
    metadata: Dict


def extract_text_from_urls(urls: List[str]) -> List[ContentChunk]:
    """
    Extract clean textual content from a list of URLs.

    Args:
        urls: List of URLs to extract content from

    Returns:
        List of ContentChunk objects with extracted content and metadata
    """
    content_chunks = []

    for idx, url in enumerate(urls):
        try:
            logger.info(f"Extracting content from {url}")

            # Fetch the page content
            response = retry_with_backoff(
                lambda: requests.get(url, timeout=30, headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; RAGBot/1.0; +http://example.com/bot)'
                })
            )

            if response.status_code != 200:
                logger.warning(f"Failed to fetch {url}: {response.status_code}")
                continue

            # Extract content
            page_title = extract_title_from_html(response.text) or "Untitled"
            text_content = _extract_main_content(response.text, url)

            if not text_content.strip():
                logger.warning(f"No content extracted from {url}")
                continue

            # Create ContentChunk
            from datetime import datetime
            import uuid

            chunk = ContentChunk(
                id=str(uuid.uuid4()),
                text_content=text_content,
                source_url=url,
                page_title=page_title,
                chunk_index=0,  # Will be updated when chunking is applied
                created_at=datetime.now().isoformat(),
                metadata={
                    "extracted_from": url,
                    "original_title": page_title,
                    "content_length": len(text_content)
                }
            )

            content_chunks.append(chunk)

            logger.info(f"Successfully extracted {len(text_content)} characters from {url}")

        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")
            continue

    return content_chunks


def _extract_main_content(html: str, url: str) -> str:
    """
    Extract main content from HTML, filtering out navigation, headers, footers, etc.

    Args:
        html: HTML content to extract from
        url: URL of the page (for logging)

    Returns:
        Clean text content
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Remove unwanted elements
    for tag in soup(['nav', 'header', 'footer', 'aside', 'script', 'style', 'noscript']):
        tag.decompose()

    # Remove elements with common class names for navigation/UI components
    for class_name in ['navbar', 'sidebar', 'toc', 'table-of-contents', 'menu', 'navigation', 'footer', 'header', 'advertisement', 'ads']:
        for tag in soup.find_all(class_=class_name):
            tag.decompose()

    # Look for main content areas in Docusaurus sites
    main_content = None

    # Try common selectors for Docusaurus content areas
    selectors = [
        'main div[class*="docItem"]',  # Docusaurus doc item
        'article',  # Standard article tag
        'main',  # Main content area
        'div[class*="markdown"]',  # Docusaurus markdown content
        'div[class*="container"]',  # General container
        'div[class*="content"]'  # General content area
    ]

    for selector in selectors:
        main_content = soup.select_one(selector)
        if main_content:
            break

    # If no specific selector worked, use the body
    if not main_content:
        main_content = soup.find('body')

    # Extract text from the main content
    if main_content:
        text = main_content.get_text(separator=' ')
    else:
        # Fallback: extract all text
        text = soup.get_text(separator=' ')

    # Clean the extracted text
    cleaned_text = clean_text(text)

    return cleaned_text


def extract_text_from_single_url(url: str) -> Optional[ContentChunk]:
    """
    Extract content from a single URL.

    Args:
        url: URL to extract content from

    Returns:
        ContentChunk object or None if extraction failed
    """
    chunks = extract_text_from_urls([url])
    return chunks[0] if chunks else None


def validate_clean_content(content: str, min_length: int = 50) -> bool:
    """
    Validate that extracted content is clean and meets minimum requirements.

    Args:
        content: Content to validate
        min_length: Minimum length of content

    Returns:
        True if content is valid, False otherwise
    """
    if not content or len(content) < min_length:
        return False

    # Check for excessive repetition (potential extraction error)
    words = content.split()
    if len(words) > 0:
        # If more than 30% of words are the same, it might be repetitive noise
        unique_words = set(words)
        if len(unique_words) / len(words) < 0.1:  # Less than 10% unique
            return False

    return True


if __name__ == "__main__":
    # Example usage
    test_urls = [settings.BOOK_BASE_URL]
    chunks = extract_text_from_urls(test_urls)
    print(f"Extracted {len(chunks)} content chunks")
    for chunk in chunks[:2]:  # Print first 2 chunks
        print(f"URL: {chunk.source_url}")
        print(f"Title: {chunk.page_title}")
        print(f"Content length: {len(chunk.text_content)}")
        print(f"Preview: {chunk.text_content[:200]}...")
        print("-" * 50)