"""
Vector Search Module for RAG Retrieval Validation

This module handles:
- Vector similarity search against Qdrant
- Top-k retrieval with metadata
- Metadata filtering capabilities
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.http import models

from config.settings import settings
from src.utils import setup_logging


logger = setup_logging()


def initialize_qdrant_client() -> QdrantClient:
    """
    Initialize and return a Qdrant client instance.

    Returns:
        QdrantClient instance configured with settings
    """
    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        prefer_grpc=False  # Using HTTP for better compatibility
    )
    return client


def search_similar_chunks(
    query_embedding: List[float],
    top_k: int = 5,
    filters: Optional[Dict[str, Any]] = None,
    min_score: Optional[float] = None
) -> List[Dict[str, Any]]:
    """
    Perform vector similarity search in Qdrant to find similar content chunks.

    Args:
        query_embedding: Query embedding vector to search for similar items
        top_k: Number of similar chunks to retrieve
        filters: Optional metadata filters to apply during search
        min_score: Minimum similarity score threshold

    Returns:
        List of dictionaries containing chunk data with similarity scores
    """
    logger.info(f"Searching for {top_k} similar chunks in collection '{settings.QDRANT_COLLECTION_NAME}'")

    client = initialize_qdrant_client()

    try:
        # Build Qdrant filter if filters are provided
        qdrant_filter = None
        if filters:
            qdrant_filter = build_qdrant_filter(filters)
            logger.debug(f"Applying filter: {qdrant_filter}")

        # Perform the search using query_points method
        response = client.query_points(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query=query_embedding,
            limit=top_k,
            query_filter=qdrant_filter,
            score_threshold=min_score  # Apply minimum score threshold if specified
        )
        results = response.points  # Extract points from the response

        # Process and return results
        chunks_data = []
        for result in results:
            chunk_data = {
                'id': result.id,
                'text_content': getattr(result.payload, 'get', lambda x, y: '')('text_content', '') if hasattr(result, 'payload') and result.payload else '',
                'source_url': getattr(result.payload, 'get', lambda x, y: '')('source_url', '') if hasattr(result, 'payload') and result.payload else '',
                'page_title': getattr(result.payload, 'get', lambda x, y: '')('page_title', '') if hasattr(result, 'payload') and result.payload else '',
                'chunk_index': getattr(result.payload, 'get', lambda x, y: 0)('chunk_index', 0) if hasattr(result, 'payload') and result.payload else 0,
                'score': getattr(result, 'score', 0),
                'metadata': getattr(result.payload, 'get', lambda x, y: {})('metadata', {}) if hasattr(result, 'payload') and result.payload else {},
                'created_at': getattr(result.payload, 'get', lambda x, y: '')('created_at', '') if hasattr(result, 'payload') and result.payload else ''
            }
            chunks_data.append(chunk_data)

        logger.info(f"Found {len(chunks_data)} similar chunks")
        return chunks_data

    except Exception as e:
        logger.error(f"Error performing vector search: {str(e)}")
        raise


def build_qdrant_filter(filters: Dict[str, Any]) -> models.Filter:
    """
    Build a Qdrant filter from the provided metadata filters.

    Args:
        filters: Dictionary of metadata filters to apply

    Returns:
        Qdrant Filter object
    """
    conditions = []

    for field_name, field_value in filters.items():
        if isinstance(field_value, list):
            # Handle list of values (e.g., multiple URLs or modules)
            condition = models.FieldCondition(
                key=field_name,
                match=models.MatchAny(any=field_value)
            )
        elif isinstance(field_value, str):
            # Handle single string value
            condition = models.FieldCondition(
                key=field_name,
                match=models.MatchValue(value=field_value)
            )
        elif isinstance(field_value, (int, float)):
            # Handle numeric values
            condition = models.FieldCondition(
                key=field_name,
                range=models.Range(gte=field_value, lte=field_value)
            )
        else:
            # Default to MatchValue for other types
            condition = models.FieldCondition(
                key=field_name,
                match=models.MatchValue(value=field_value)
            )

        conditions.append(condition)

    # Combine all conditions with AND logic
    qdrant_filter = models.Filter(must=conditions)
    return qdrant_filter


def apply_metadata_filters_to_search(
    query_embedding: List[float],
    top_k: int = 5,
    filters: Optional[Dict[str, Any]] = None,
    min_score: Optional[float] = None
) -> List[Dict[str, Any]]:
    """
    Perform vector similarity search with metadata filters applied.

    Args:
        query_embedding: Query embedding vector to search for similar items
        top_k: Number of similar chunks to retrieve
        filters: Optional metadata filters to apply during search
        min_score: Minimum similarity score threshold

    Returns:
        List of dictionaries containing chunk data with similarity scores
    """
    logger.info(f"Searching with metadata filters: {filters}")

    return search_similar_chunks(
        query_embedding=query_embedding,
        top_k=top_k,
        filters=filters,
        min_score=min_score
    )


def apply_metadata_filters(
    chunks_data: List[Dict[str, Any]],
    filters: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Apply metadata filters to the retrieved chunks (alternative to server-side filtering).

    Args:
        chunks_data: List of chunk data dictionaries
        filters: Metadata filters to apply

    Returns:
        Filtered list of chunk data
    """
    if not filters:
        return chunks_data

    filtered_chunks = []
    for chunk in chunks_data:
        include_chunk = True

        for field_name, field_value in filters.items():
            chunk_value = chunk.get('metadata', {}).get(field_name) or chunk.get(field_name)

            if isinstance(field_value, list):
                # Check if chunk value is in the list of allowed values
                if chunk_value not in field_value:
                    include_chunk = False
                    break
            elif chunk_value != field_value:
                # Exact match for single values
                include_chunk = False
                break

        if include_chunk:
            filtered_chunks.append(chunk)

    logger.debug(f"Applied metadata filters: {len(chunks_data)} -> {len(filtered_chunks)} chunks")
    return filtered_chunks


def get_collection_stats(collection_name: str = None) -> Dict[str, Any]:
    """
    Get statistics about the collection including number of points and other metrics.

    Args:
        collection_name: Name of the collection to get stats for (uses default if None)

    Returns:
        Dictionary with collection statistics
    """
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME

    client = initialize_qdrant_client()

    try:
        collection_info = client.get_collection(collection_name)
        return {
            'points_count': collection_info.points_count,
            'indexed_vectors_count': getattr(collection_info, 'indexed_vectors_count', 'N/A'),
            'config': collection_info.config.dict() if hasattr(collection_info, 'config') else 'N/A'
        }
    except Exception as e:
        logger.error(f"Error getting collection stats: {str(e)}")
        return {}


def validate_qdrant_connection() -> bool:
    """
    Validate that we can connect to Qdrant and access the collection.

    Returns:
        True if connection is successful, False otherwise
    """
    try:
        client = initialize_qdrant_client()
        collections = client.get_collections()
        collection_names = [c.name for c in collections.collections]

        if settings.QDRANT_COLLECTION_NAME in collection_names:
            logger.info(f"Successfully connected to Qdrant and found collection '{settings.QDRANT_COLLECTION_NAME}'")
            return True
        else:
            logger.warning(f"Collection '{settings.QDRANT_COLLECTION_NAME}' not found in Qdrant")
            return False

    except Exception as e:
        logger.error(f"Error validating Qdrant connection: {str(e)}")
        return False


def search_by_url(url: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search for chunks specifically from a given URL.

    Args:
        url: Source URL to search for
        top_k: Number of results to retrieve

    Returns:
        List of chunks from the specified URL
    """
    filters = {'source_url': url}
    qdrant_filter = build_qdrant_filter(filters)

    client = initialize_qdrant_client()

    try:
        response = client.query_points(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query=[0.0] * 1024,  # Dummy vector, using filter only
            limit=top_k,
            query_filter=qdrant_filter
        )
        results = response.points  # Extract points from the response

        # Since we're using a dummy vector, we'll need to do a semantic search with URL filter
        # So we'll get all chunks from the URL and then rerank them based on semantic similarity

        # For now, return chunks from the URL
        chunks_data = []
        for result in results:
            chunk_data = {
                'id': result.id,
                'text_content': getattr(result.payload, 'get', lambda x, y: '')('text_content', '') if hasattr(result, 'payload') and result.payload else '',
                'source_url': getattr(result.payload, 'get', lambda x, y: '')('source_url', '') if hasattr(result, 'payload') and result.payload else '',
                'page_title': getattr(result.payload, 'get', lambda x, y: '')('page_title', '') if hasattr(result, 'payload') and result.payload else '',
                'chunk_index': getattr(result.payload, 'get', lambda x, y: 0)('chunk_index', 0) if hasattr(result, 'payload') and result.payload else 0,
                'score': getattr(result, 'score', 0),
                'metadata': getattr(result.payload, 'get', lambda x, y: {})('metadata', {}) if hasattr(result, 'payload') and result.payload else {},
                'created_at': getattr(result.payload, 'get', lambda x, y: '')('created_at', '') if hasattr(result, 'payload') and result.payload else ''
            }
            chunks_data.append(chunk_data)

        return chunks_data

    except Exception as e:
        logger.error(f"Error searching by URL: {str(e)}")
        raise


def search_by_page_title(title: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search for chunks from a page with a specific title.

    Args:
        title: Page title to search for
        top_k: Number of results to retrieve

    Returns:
        List of chunks from pages with the specified title
    """
    filters = {'page_title': title}
    qdrant_filter = build_qdrant_filter(filters)

    client = initialize_qdrant_client()

    try:
        response = client.query_points(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query=[0.0] * 1024,  # Dummy vector, using filter only
            limit=top_k,
            query_filter=qdrant_filter
        )
        results = response.points  # Extract points from the response

        chunks_data = []
        for result in results:
            chunk_data = {
                'id': result.id,
                'text_content': getattr(result.payload, 'get', lambda x, y: '')('text_content', '') if hasattr(result, 'payload') and result.payload else '',
                'source_url': getattr(result.payload, 'get', lambda x, y: '')('source_url', '') if hasattr(result, 'payload') and result.payload else '',
                'page_title': getattr(result.payload, 'get', lambda x, y: '')('page_title', '') if hasattr(result, 'payload') and result.payload else '',
                'chunk_index': getattr(result.payload, 'get', lambda x, y: 0)('chunk_index', 0) if hasattr(result, 'payload') and result.payload else 0,
                'score': getattr(result, 'score', 0),
                'metadata': getattr(result.payload, 'get', lambda x, y: {})('metadata', {}) if hasattr(result, 'payload') and result.payload else {},
                'created_at': getattr(result.payload, 'get', lambda x, y: '')('created_at', '') if hasattr(result, 'payload') and result.payload else ''
            }
            chunks_data.append(chunk_data)

        return chunks_data

    except Exception as e:
        logger.error(f"Error searching by page title: {str(e)}")
        raise


if __name__ == "__main__":
    # Example usage
    # This would require actual embeddings to work properly
    print("Vector search module - requires valid embeddings and Qdrant connection to test")