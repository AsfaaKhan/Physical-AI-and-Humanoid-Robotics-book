#!/usr/bin/env python3
"""
Main ingestion pipeline for RAG Knowledge Ingestion Pipeline for Docusaurus Book.

This script orchestrates the complete pipeline:
1. get_all_urls - Discover all book pages
2. extract_text_from_urls - Extract clean content
3. chunk_text - Split content into semantic chunks
4. embed - Generate Cohere embeddings
5. create_collection - Set up Qdrant collection
6. save_chunks_to_qdrant - Store embeddings with metadata
"""

import logging
import time
import uuid
from datetime import datetime
from typing import List, Dict, Any
import sys

# Import all required modules
from config.settings import settings
from src.crawler import get_all_urls
from src.extractor import extract_text_from_urls, ContentChunk
from src.chunker import chunk_content_chunks, validate_boundary_preservation
from src.embedder import batch_embed, validate_embeddings
from src.storage import create_collection, save_chunks_to_qdrant, validate_metadata_storage
from src.utils import setup_logging


def main():
    """
    Main function that orchestrates the complete RAG ingestion pipeline.
    """
    logger = setup_logging("INFO")
    logger.info("Starting RAG Knowledge Ingestion Pipeline")

    # Validate settings
    if not settings.validate():
        logger.error("Configuration validation failed. Please check your environment variables.")
        sys.exit(1)

    try:
        # Step 1: Get all URLs from the book website
        logger.info("Step 1: Discovering all book pages...")
        urls = get_all_urls()
        logger.info(f"Discovered {len(urls)} URLs")

        if not urls:
            logger.error("No URLs found. Exiting.")
            return

        # Step 2: Extract text content from all URLs
        logger.info("Step 2: Extracting content from URLs...")
        content_chunks = extract_text_from_urls(urls)
        logger.info(f"Extracted {len(content_chunks)} content chunks")

        if not content_chunks:
            logger.error("No content extracted. Exiting.")
            return

        # Step 3: Chunk the content for better semantic retrieval
        logger.info("Step 3: Chunking content...")
        chunked_content = chunk_content_chunks(content_chunks, chunk_size=800, overlap=100)
        logger.info(f"Chunked into {len(chunked_content)} smaller chunks")

        # Validate chunk boundary preservation
        chunk_texts = [chunk.text_content for chunk in chunked_content]
        original_text = " ".join([cc.text_content for cc in content_chunks])
        boundary_validation = validate_boundary_preservation(chunk_texts, original_text)
        logger.info(f"Boundary preservation rate: {boundary_validation['boundary_preservation_rate']:.2%}")

        # Step 4: Prepare texts for embedding
        texts_to_embed = [chunk.text_content for chunk in chunked_content]

        # Step 5: Generate embeddings using Cohere
        logger.info("Step 4: Generating embeddings...")
        embeddings = batch_embed(texts_to_embed, batch_size=96)
        logger.info(f"Generated {len(embeddings)} embeddings")

        if not validate_embeddings(embeddings, expected_dimension=1024):
            logger.error("Embedding validation failed. Dimensions inconsistent.")
            return

        # Step 6: Prepare chunks with embeddings for storage
        processed_chunks = []
        for i, chunk in enumerate(chunked_content):
            if i < len(embeddings):  # Safety check
                processed_chunk = {
                    'id': str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{chunk.id}_{i}")),
                    'vector': embeddings[i],
                    'text_content': chunk.text_content,
                    'source_url': chunk.source_url,
                    'page_title': chunk.page_title,
                    'chunk_index': chunk.chunk_index,
                    'created_at': datetime.now().isoformat(),
                    'metadata': {
                        **chunk.metadata,
                        'processed_at': datetime.now().isoformat(),
                        'original_chunk_id': chunk.id
                    }
                }
                processed_chunks.append(processed_chunk)

        # Validate metadata storage structure
        if not validate_metadata_storage(processed_chunks):
            logger.error("Metadata validation failed.")
            return

        # Step 7: Create Qdrant collection
        logger.info("Step 5: Creating Qdrant collection...")
        if not create_collection(settings.QDRANT_COLLECTION_NAME):
            logger.error("Failed to create Qdrant collection.")
            return

        # Step 8: Save chunks to Qdrant
        logger.info("Step 6: Saving chunks to Qdrant...")
        if not save_chunks_to_qdrant(processed_chunks, settings.QDRANT_COLLECTION_NAME):
            logger.error("Failed to save chunks to Qdrant.")
            return

        logger.info(f"Pipeline completed successfully! Saved {len(processed_chunks)} chunks to collection '{settings.QDRANT_COLLECTION_NAME}'")

    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}")
        sys.exit(1)


def get_all_urls():
    """
    Get all URLs from the Docusaurus book website.
    """
    from src.crawler import get_all_urls as crawler_get_all_urls
    return crawler_get_all_urls()


def extract_text_from_urls(urls: List[str]):
    """
    Extract text from the provided URLs.
    """
    from src.extractor import extract_text_from_urls as extractor_extract
    return extractor_extract(urls)


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100):
    """
    Chunk the provided text.
    """
    from src.chunker import chunk_text as chunker_chunk_text
    return chunker_chunk_text(text, chunk_size, overlap)


def embed(texts: List[str]):
    """
    Generate embeddings for the provided texts.
    """
    from src.embedder import embed as embedder_embed
    return embedder_embed(texts)


def create_collection(collection_name: str = None):
    """
    Create a Qdrant collection.
    """
    from src.storage import create_collection as storage_create_collection
    return storage_create_collection(collection_name)


def save_chunks_to_qdrant(chunks: List[Dict], collection_name: str = None):
    """
    Save chunks to Qdrant.
    """
    from src.storage import save_chunks_to_qdrant as storage_save_chunks
    return storage_save_chunks(chunks, collection_name)


if __name__ == "__main__":
    main()