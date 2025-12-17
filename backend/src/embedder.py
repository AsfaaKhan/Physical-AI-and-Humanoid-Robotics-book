"""
Embedder module for generating vector embeddings using Cohere models.
"""

import cohere
from typing import List, Dict, Any
import logging
from config.settings import settings
from src.utils import setup_logging


logger = setup_logging()


def embed(texts: List[str], model: str = "embed-multilingual-v3.0") -> List[List[float]]:
    """
    Generate vector embeddings for a list of texts using Cohere.

    Args:
        texts: List of texts to embed
        model: Cohere embedding model to use

    Returns:
        List of embedding vectors (each vector is a list of floats)
    """
    if not texts:
        return []

    # Initialize Cohere client
    co = cohere.Client(settings.COHERE_API_KEY)

    try:
        logger.info(f"Generating embeddings for {len(texts)} texts using model {model}")

        # Generate embeddings
        response = co.embed(
            texts=texts,
            model=model,
            input_type="search_document"  # Appropriate for document search
        )

        embeddings = response.embeddings
        logger.info(f"Successfully generated {len(embeddings)} embeddings")

        # Validate that all embeddings have the same dimension
        if embeddings:
            first_dim = len(embeddings[0])
            for i, emb in enumerate(embeddings):
                if len(emb) != first_dim:
                    raise ValueError(f"Embedding {i} has different dimension ({len(emb)}) than expected ({first_dim})")

        return embeddings

    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise


def embed_single_text(text: str, model: str = "embed-multilingual-v3.0") -> List[float]:
    """
    Generate vector embedding for a single text.

    Args:
        text: Text to embed
        model: Cohere embedding model to use

    Returns:
        Embedding vector (list of floats)
    """
    embeddings = embed([text], model)
    return embeddings[0] if embeddings else []


def validate_embeddings(embeddings: List[List[float]], expected_dimension: int = None) -> bool:
    """
    Validate that embeddings have consistent dimensions.

    Args:
        embeddings: List of embedding vectors to validate
        expected_dimension: Expected dimension of embeddings (optional)

    Returns:
        True if all embeddings have consistent dimensions, False otherwise
    """
    if not embeddings:
        return True

    first_dim = len(embeddings[0])

    # Check if expected dimension is provided and matches
    if expected_dimension and first_dim != expected_dimension:
        logger.error(f"Embedding dimension {first_dim} does not match expected {expected_dimension}")
        return False

    # Check that all embeddings have the same dimension
    for i, emb in enumerate(embeddings):
        if len(emb) != first_dim:
            logger.error(f"Embedding {i} has different dimension ({len(emb)}) than expected ({first_dim})")
            return False

    logger.info(f"All {len(embeddings)} embeddings have consistent dimension of {first_dim}")
    return True


def get_embedding_model_info(model: str = "embed-multilingual-v3.0") -> Dict[str, Any]:
    """
    Get information about the embedding model.

    Args:
        model: Cohere embedding model name

    Returns:
        Dictionary with model information
    """
    # Common Cohere embedding models and their dimensions
    model_info = {
        "embed-multilingual-v3.0": {
            "dimension": 1024,
            "type": "multilingual",
            "recommended_use": "multilingual content, semantic search"
        },
        "embed-english-v3.0": {
            "dimension": 1024,
            "type": "english",
            "recommended_use": "english content, semantic search"
        }
    }

    return model_info.get(model, {
        "dimension": 1024,  # Default assumption
        "type": "unknown",
        "recommended_use": "general purpose"
    })


def batch_embed(texts: List[str], batch_size: int = 96, model: str = "embed-multilingual-v3.0") -> List[List[float]]:
    """
    Generate embeddings in batches to handle large lists of texts.

    Args:
        texts: List of texts to embed
        batch_size: Number of texts to process in each batch
        model: Cohere embedding model to use

    Returns:
        List of embedding vectors
    """
    if not texts:
        return []

    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        logger.info(f"Processing batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")

        batch_embeddings = embed(batch, model)
        all_embeddings.extend(batch_embeddings)

    return all_embeddings


if __name__ == "__main__":
    # Example usage
    sample_texts = [
        "Artificial Intelligence is a wonderful field.",
        "Machine Learning is a subset of AI.",
        "Deep Learning uses neural networks with multiple layers."
    ]

    try:
        embeddings = batch_embed(sample_texts)
        print(f"Generated {len(embeddings)} embeddings")
        print(f"Each embedding has {len(embeddings[0]) if embeddings else 0} dimensions")
        print(f"First embedding preview: {embeddings[0][:5]}...")  # Show first 5 values
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set your COHERE_API_KEY in the .env file")