"""
Crawler module for discovering all book pages from the Docusaurus website.
"""

import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time
import logging
from typing import List, Set
from config.settings import settings
from src.utils import setup_logging, retry_with_backoff, normalize_url


logger = setup_logging()


def get_all_urls() -> List[str]:
    """
    Discover and return all public URLs from the Docusaurus book website.

    This function uses both sitemap parsing and recursive crawling to
    identify all available pages.

    Returns:
        List of all discovered URLs
    """
    logger.info(f"Starting URL discovery from {settings.BOOK_BASE_URL}")

    # Get URLs from sitemap first
    sitemap_urls = _get_urls_from_sitemap()
    logger.info(f"Found {len(sitemap_urls)} URLs from sitemap")

    # Get URLs from recursive crawling
    crawled_urls = _crawl_website()
    logger.info(f"Found {len(crawled_urls)} URLs from crawling")

    # Combine and deduplicate
    all_urls = list(set(sitemap_urls + crawled_urls))
    logger.info(f"Total unique URLs discovered: {len(all_urls)}")

    return all_urls


def _get_urls_from_sitemap() -> List[str]:
    """
    Parse the sitemap.xml to extract all URLs.

    Returns:
        List of URLs from sitemap
    """
    sitemap_url = urljoin(settings.BOOK_BASE_URL, "sitemap.xml")
    logger.info(f"Fetching sitemap from {sitemap_url}")

    try:
        response = retry_with_backoff(
            lambda: requests.get(sitemap_url, timeout=30)
        )

        if response.status_code != 200:
            logger.warning(f"Sitemap not found or inaccessible: {sitemap_url}")
            return []

        soup = BeautifulSoup(response.content, 'xml')
        urls = []

        # Look for <url><loc> elements in sitemap
        for loc in soup.find_all('loc'):
            url = loc.text.strip()
            if url and url.startswith(settings.BOOK_BASE_URL):
                urls.append(url)

        # Handle sitemap index files (sitemap of sitemaps)
        for sitemap_elem in soup.find_all('sitemap'):
            loc_elem = sitemap_elem.find('loc')
            if loc_elem:
                nested_sitemap_url = loc_elem.text.strip()
                if nested_sitemap_url:
                    nested_urls = _get_nested_sitemap_urls(nested_sitemap_url)
                    urls.extend(nested_urls)

        return urls

    except Exception as e:
        logger.warning(f"Error fetching sitemap: {str(e)}")
        return []


def _get_nested_sitemap_urls(sitemap_url: str) -> List[str]:
    """
    Get URLs from a nested sitemap.

    Args:
        sitemap_url: URL of the nested sitemap

    Returns:
        List of URLs from nested sitemap
    """
    try:
        response = requests.get(sitemap_url, timeout=30)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.content, 'xml')
        urls = []

        for loc in soup.find_all('loc'):
            url = loc.text.strip()
            if url and url.startswith(settings.BOOK_BASE_URL):
                urls.append(url)

        return urls

    except Exception as e:
        logger.warning(f"Error fetching nested sitemap {sitemap_url}: {str(e)}")
        return []


def _crawl_website(max_depth: int = 2, max_pages: int = 100) -> List[str]:
    """
    Recursively crawl the website to discover all pages.

    Args:
        max_depth: Maximum depth to crawl
        max_pages: Maximum number of pages to crawl

    Returns:
        List of discovered URLs
    """
    visited_urls: Set[str] = set()
    urls_to_visit: List[str] = [settings.BOOK_BASE_URL]

    while urls_to_visit and len(visited_urls) < max_pages:
        current_url = urls_to_visit.pop(0)

        # Skip if already visited or not in the same domain
        if (current_url in visited_urls or
            not current_url.startswith(settings.BOOK_BASE_URL)):
            continue

        try:
            logger.info(f"Crawling: {current_url}")

            response = retry_with_backoff(
                lambda: requests.get(current_url, timeout=30)
            )

            if response.status_code != 200:
                logger.warning(f"Failed to fetch {current_url}: {response.status_code}")
                continue

            visited_urls.add(current_url)

            # Parse links from the page
            soup = BeautifulSoup(response.content, 'html.parser')

            for link in soup.find_all('a', href=True):
                href = link['href']

                # Convert relative URLs to absolute
                absolute_url = normalize_url(settings.BOOK_BASE_URL, href)

                # Only add URLs from the same domain and not already visited
                if (absolute_url.startswith(settings.BOOK_BASE_URL) and
                    absolute_url not in visited_urls and
                    len(visited_urls) < max_pages):
                    urls_to_visit.append(absolute_url)

            # Be respectful - add delay between requests
            time.sleep(0.5)

        except Exception as e:
            logger.error(f"Error crawling {current_url}: {str(e)}")
            continue

    return list(visited_urls)


def validate_urls(urls: List[str]) -> List[str]:
    """
    Validate a list of URLs to ensure they are accessible.

    Args:
        urls: List of URLs to validate

    Returns:
        List of URLs that are accessible
    """
    valid_urls = []

    for url in urls:
        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                valid_urls.append(url)
            else:
                logger.warning(f"URL not accessible (status {response.status_code}): {url}")
        except Exception as e:
            logger.warning(f"Error validating URL {url}: {str(e)}")

    return valid_urls


if __name__ == "__main__":
    # Example usage
    all_urls = get_all_urls()
    print(f"Discovered {len(all_urls)} URLs")
    for url in all_urls[:10]:  # Print first 10 URLs
        print(url)