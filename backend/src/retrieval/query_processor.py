"""
Query Processor Module for RAG Retrieval Validation

This module handles:
- Processing natural language queries
- Generating query embeddings using Cohere
- Managing the query processing pipeline
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import cohere
from qdrant_client import QdrantClient

from config.settings import settings
from src.retrieval.vector_search import search_similar_chunks
from src.utils import setup_logging


logger = setup_logging()


@dataclass
class QueryRequest:
    """
    Represents a natural language query with optional metadata filters and retrieval parameters.
    Based on data-model.md specifications.
    """
    query_text: str
    top_k: int = 5
    min_score: Optional[float] = None
    filters: Optional[Dict[str, Any]] = None
    query_embedding: Optional[List[float]] = None
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


@dataclass
class ContentChunk:
    """
    Retrieved text content with associated metadata.
    Based on data-model.md specifications.
    """
    id: str
    text_content: str
    source_url: str
    page_title: str
    chunk_index: int
    relevance_score: float
    metadata: Dict[str, Any]


@dataclass
class RetrievalResult:
    """
    Contains relevant content chunks with similarity scores, metadata, and source information.
    Based on data-model.md specifications.
    """
    query_request: QueryRequest
    retrieved_chunks: List[ContentChunk]
    relevance_scores: List[float]
    retrieval_time_ms: float
    total_candidates: int
    metadata_filters_applied: Dict[str, Any]
    validation_metrics: Dict[str, float]


def process_query(query_text: str, top_k: int = 5, filters: Optional[Dict[str, Any]] = None, min_score: Optional[float] = None) -> RetrievalResult:
    """
    Process a natural language query and return relevant chunks from the vector store.

    Args:
        query_text: Natural language query to process
        top_k: Number of results to retrieve (default: 5)
        filters: Optional metadata filters to apply (default: None)
        min_score: Minimum similarity score threshold (default: None)

    Returns:
        RetrievalResult containing relevant chunks with metadata
    """
    logger.info(f"Processing query: {query_text[:50]}...")

    # Validate inputs
    if not query_text or len(query_text.strip()) == 0:
        raise ValueError("Query text cannot be empty")

    if top_k <= 0 or top_k > 100:
        raise ValueError("top_k must be between 1 and 100")

    if min_score is not None and (min_score < 0.0 or min_score > 1.0):
        raise ValueError("min_score must be between 0.0 and 1.0 if specified")

    # Create query request object
    query_request = QueryRequest(
        query_text=query_text,
        top_k=top_k,
        min_score=min_score,
        filters=filters
    )

    # Generate query embedding
    logger.debug("Generating query embedding...")
    query_embedding = generate_query_embedding(query_text)
    query_request.query_embedding = query_embedding

    # Perform similarity search
    logger.debug(f"Performing similarity search with top_k={top_k}...")
    search_start_time = datetime.now()

    chunks_data = search_similar_chunks(
        query_embedding=query_embedding,
        top_k=top_k,
        filters=filters,
        min_score=min_score
    )

    search_duration = (datetime.now() - search_start_time).total_seconds() * 1000  # Convert to milliseconds

    # Convert raw search results to ContentChunk objects
    retrieved_chunks = []
    relevance_scores = []

    for chunk_data in chunks_data:
        chunk = ContentChunk(
            id=chunk_data.get('id'),
            text_content=chunk_data.get('text_content', ''),
            source_url=chunk_data.get('source_url', ''),
            page_title=chunk_data.get('page_title', ''),
            chunk_index=chunk_data.get('chunk_index', 0),
            relevance_score=chunk_data.get('score', 0.0),
            metadata=chunk_data.get('metadata', {})
        )
        retrieved_chunks.append(chunk)
        relevance_scores.append(chunk.relevance_score)

    # Create and return retrieval result
    result = RetrievalResult(
        query_request=query_request,
        retrieved_chunks=retrieved_chunks,
        relevance_scores=relevance_scores,
        retrieval_time_ms=search_duration,
        total_candidates=len(chunks_data),  # This would need to be updated to reflect total candidates considered
        metadata_filters_applied=filters or {},
        validation_metrics={}  # Will be populated by validation functions
    )

    logger.info(f"Retrieved {len(retrieved_chunks)} chunks in {search_duration:.2f}ms")
    return result


def generate_query_embedding(query_text: str) -> List[float]:
    """
    Generate embedding for the query text using Cohere.

    Args:
        query_text: Text to generate embedding for

    Returns:
        List of floats representing the embedding vector
    """
    # Initialize Cohere client
    from config.settings import settings
    co = cohere.Client(settings.COHERE_API_KEY)

    try:
        # Generate embedding using the same model as ingestion pipeline
        response = co.embed(
            texts=[query_text],
            model="embed-multilingual-v3.0",  # Same as ingestion pipeline
            input_type="search_query"  # Specify this is a search query (not document)
        )

        # Extract the embedding (should be a 1024-dimensional vector)
        embeddings = response.embeddings
        if len(embeddings) == 0:
            raise ValueError("No embeddings returned from Cohere API")

        query_embedding = embeddings[0]
        logger.debug(f"Generated {len(query_embedding)}-dimensional embedding for query")

        return query_embedding

    except Exception as e:
        logger.error(f"Error generating query embedding: {str(e)}")
        raise


def process_query_with_filters(query_text: str, filters: Dict[str, Any], top_k: int = 5) -> RetrievalResult:
    """
    Process a query with specific metadata filters applied.

    Args:
        query_text: Natural language query to process
        filters: Metadata filters to apply during retrieval
        top_k: Number of results to retrieve

    Returns:
        RetrievalResult with filtered results
    """
    return process_query(query_text, top_k=top_k, filters=filters)


if __name__ == "__main__":
    # Example usage
    sample_query = "What is Physical AI?"
    result = process_query(sample_query, top_k=3)
    print(f"Query: {sample_query}")
    print(f"Retrieved {len(result.retrieved_chunks)} chunks:")
    for i, chunk in enumerate(result.retrieved_chunks):
        print(f"  {i+1}. Score: {chunk.relevance_score:.3f}, Source: {chunk.source_url[:50]}...")