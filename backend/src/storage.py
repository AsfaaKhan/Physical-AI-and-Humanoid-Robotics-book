"""
Storage module for managing vector storage in Qdrant Cloud.
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
import logging
from config.settings import settings
from src.utils import setup_logging


logger = setup_logging()


def create_collection(collection_name: str = None) -> bool:
    """
    Create a Qdrant collection for storing embeddings.

    Args:
        collection_name: Name of the collection to create (uses default if None)

    Returns:
        True if collection was created successfully, False otherwise
    """
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME

    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        prefer_grpc=False  # Using HTTP for better compatibility
    )

    try:
        # Check if collection already exists
        collections = client.get_collections()
        existing_collection_names = [c.name for c in collections.collections]

        if collection_name in existing_collection_names:
            logger.info(f"Collection '{collection_name}' already exists")
            return True

        # Create collection with appropriate vector configuration
        # Using Cohere's multilingual model dimension (1024)
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1024,  # Dimension of Cohere embeddings
                distance=models.Distance.COSINE  # Cosine similarity for semantic search
            )
        )

        logger.info(f"Successfully created collection '{collection_name}' with 1024-dimensional vectors")
        return True

    except Exception as e:
        logger.error(f"Error creating collection '{collection_name}': {str(e)}")
        return False


def save_chunks_to_qdrant(chunks: List[Dict], collection_name: str = None) -> bool:
    """
    Save content chunks with embeddings to Qdrant collection.

    Args:
        chunks: List of dictionaries containing chunk data with embeddings
               Each dict should have: id, vector, text_content, source_url, page_title, chunk_index, metadata
        collection_name: Name of the collection to save to (uses default if None)

    Returns:
        True if chunks were saved successfully, False otherwise
    """
    if not chunks:
        logger.warning("No chunks to save to Qdrant")
        return True

    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME

    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        prefer_grpc=False
    )

    try:
        # Prepare points for insertion
        points = []
        for chunk in chunks:
            # Validate required fields
            required_fields = ['id', 'vector', 'text_content', 'source_url', 'page_title', 'chunk_index']
            for field in required_fields:
                if field not in chunk:
                    raise ValueError(f"Missing required field '{field}' in chunk data")

            point = models.PointStruct(
                id=chunk['id'],
                vector=chunk['vector'],
                payload={
                    'text_content': chunk['text_content'],
                    'source_url': chunk['source_url'],
                    'page_title': chunk['page_title'],
                    'chunk_index': chunk['chunk_index'],
                    'metadata': chunk.get('metadata', {}),
                    'created_at': chunk.get('created_at', '')
                }
            )
            points.append(point)

        # Upload points in batches
        batch_size = 64  # Reasonable batch size for Qdrant
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            client.upsert(
                collection_name=collection_name,
                points=batch
            )
            logger.info(f"Uploaded batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1} to Qdrant")

        logger.info(f"Successfully saved {len(chunks)} chunks to collection '{collection_name}'")
        return True

    except Exception as e:
        logger.error(f"Error saving chunks to Qdrant: {str(e)}")
        return False


def search_in_qdrant(query_vector: List[float], collection_name: str = None, limit: int = 10) -> List[Dict]:
    """
    Search for similar content in Qdrant collection.

    Args:
        query_vector: Vector to search for similar items
        collection_name: Name of the collection to search (uses default if None)
        limit: Maximum number of results to return

    Returns:
        List of similar content with scores
    """
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME

    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        prefer_grpc=False
    )

    try:
        results = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit
        )

        search_results = []
        for result in results:
            search_results.append({
                'id': result.id,
                'text_content': result.payload.get('text_content', ''),
                'source_url': result.payload.get('source_url', ''),
                'page_title': result.payload.get('page_title', ''),
                'chunk_index': result.payload.get('chunk_index', 0),
                'metadata': result.payload.get('metadata', {}),
                'score': result.score
            })

        return search_results

    except Exception as e:
        logger.error(f"Error searching in Qdrant: {str(e)}")
        return []


def validate_metadata_storage(chunks: List[Dict]) -> bool:
    """
    Validate that all required metadata is properly stored.

    Args:
        chunks: List of chunk dictionaries to validate

    Returns:
        True if all metadata is properly structured, False otherwise
    """
    required_metadata = ['text_content', 'source_url', 'page_title', 'chunk_index', 'metadata']

    for i, chunk in enumerate(chunks):
        for field in required_metadata:
            if field not in chunk:
                logger.error(f"Chunk {i} missing required field: {field}")
                return False

        # Validate that the vector exists and has proper dimensions
        if 'vector' not in chunk or not chunk['vector']:
            logger.error(f"Chunk {i} missing vector data")
            return False

        # Validate that the ID is present
        if 'id' not in chunk or not chunk['id']:
            logger.error(f"Chunk {i} missing ID")
            return False

    logger.info(f"Successfully validated metadata for {len(chunks)} chunks")
    return True


def batch_save_to_qdrant(chunks: List[Dict], collection_name: str = None, batch_size: int = 64) -> bool:
    """
    Save chunks to Qdrant in batches for better performance.

    Args:
        chunks: List of dictionaries containing chunk data with embeddings
        collection_name: Name of the collection to save to (uses default if None)
        batch_size: Number of chunks to process in each batch

    Returns:
        True if all chunks were saved successfully, False otherwise
    """
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME

    success_count = 0
    total_chunks = len(chunks)

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        if save_chunks_to_qdrant(batch, collection_name):
            success_count += len(batch)
            logger.info(f"Successfully saved batch {i//batch_size + 1} ({len(batch)} chunks)")
        else:
            logger.error(f"Failed to save batch {i//batch_size + 1}")
            return False

    logger.info(f"Successfully saved {success_count}/{total_chunks} chunks to Qdrant")
    return success_count == total_chunks


def check_collection_exists(collection_name: str = None) -> bool:
    """
    Check if a collection exists in Qdrant.

    Args:
        collection_name: Name of the collection to check (uses default if None)

    Returns:
        True if collection exists, False otherwise
    """
    if collection_name is None:
        collection_name = settings.QDRANT_COLLECTION_NAME

    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        prefer_grpc=False
    )

    try:
        collections = client.get_collections()
        existing_collection_names = [c.name for c in collections.collections]
        return collection_name in existing_collection_names
    except Exception as e:
        logger.error(f"Error checking collection existence: {str(e)}")
        return False


if __name__ == "__main__":
    # Example usage
    # Note: This would require valid Qdrant credentials to run successfully
    print("Storage module for Qdrant operations")
    print(f"Default collection name: {settings.QDRANT_COLLECTION_NAME}")
    print(f"Qdrant URL: {settings.QDRANT_URL}")