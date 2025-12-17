"""
Chunker module for splitting content into semantically coherent segments.
"""

import re
from typing import List, Dict, Any
from dataclasses import dataclass
from src.extractor import ContentChunk
import logging
from src.utils import setup_logging


logger = setup_logging()


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    """
    Split text into semantically coherent chunks with overlap.

    Args:
        text: Text to chunk
        chunk_size: Target size of each chunk (in characters)
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if not text or len(text) <= chunk_size:
        return [text] if text else []

    chunks = []
    start = 0

    while start < len(text):
        # Determine the end position
        end = start + chunk_size

        # If we're near the end, take the rest
        if end >= len(text):
            chunks.append(text[start:])
            break

        # Try to break at sentence boundary
        chunk = text[start:end]
        sentence_end = re.search(r'[.!?]+\s+', chunk[::-1])

        if sentence_end:
            # Found a sentence boundary, adjust the end position
            break_pos = len(chunk) - sentence_end.start()
            actual_end = start + break_pos
            chunks.append(text[start:actual_end])
            start = actual_end - overlap
        else:
            # No sentence boundary found, try paragraph boundary
            paragraph_end = chunk.rfind('\n\n')
            if paragraph_end != -1 and paragraph_end > chunk_size // 2:
                actual_end = start + paragraph_end + 2
                chunks.append(text[start:actual_end])
                start = actual_end - overlap
            else:
                # No good boundary found, just take the chunk
                chunks.append(text[start:end])
                start = end - overlap

        # Ensure we make progress to avoid infinite loops
        if start <= chunks[-1].start if hasattr(chunks[-1], 'start') else start <= len(chunks[-1]) + start - chunk_size:
            start += 1

    # Filter out empty chunks and clean them up
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    return chunks


def chunk_content_chunks(content_chunks: List[ContentChunk], chunk_size: int = 800, overlap: int = 100) -> List[ContentChunk]:
    """
    Chunk a list of ContentChunk objects into smaller pieces.

    Args:
        content_chunks: List of ContentChunk objects to chunk
        chunk_size: Target size of each chunk (in characters)
        overlap: Number of characters to overlap between chunks

    Returns:
        List of chunked ContentChunk objects
    """
    chunked_content = []

    for original_chunk in content_chunks:
        text_chunks = chunk_text(original_chunk.text_content, chunk_size, overlap)

        for idx, text_chunk in enumerate(text_chunks):
            # Create a new ContentChunk for each text chunk
            chunked_chunk = ContentChunk(
                id=f"{original_chunk.id}_chunk_{idx}",
                text_content=text_chunk,
                source_url=original_chunk.source_url,
                page_title=original_chunk.page_title,
                chunk_index=idx,
                created_at=original_chunk.created_at,
                metadata={
                    **original_chunk.metadata,
                    "original_chunk_id": original_chunk.id,
                    "chunk_index": idx,
                    "total_chunks": len(text_chunks),
                    "is_chunked": True
                }
            )
            chunked_content.append(chunked_chunk)

    logger.info(f"Chunked {len(content_chunks)} content chunks into {len(chunked_content)} smaller chunks")
    return chunked_content


def validate_chunk_coherence(chunks: List[str], min_chunk_size: int = 50) -> Dict[str, Any]:
    """
    Validate that chunks maintain semantic coherence.

    Args:
        chunks: List of text chunks to validate
        min_chunk_size: Minimum size for a valid chunk

    Returns:
        Dictionary with validation results
    """
    results = {
        "total_chunks": len(chunks),
        "valid_chunks": 0,
        "invalid_chunks": 0,
        "avg_chunk_size": 0,
        "coherence_score": 0.0,
        "boundary_preservation": 0.0
    }

    if not chunks:
        return results

    valid_chunks = 0
    total_size = 0
    good_boundaries = 0

    for chunk in chunks:
        total_size += len(chunk)
        if len(chunk) >= min_chunk_size:
            valid_chunks += 1

        # Check if chunk ends with sentence/paragraph boundary
        if chunk.endswith(('.', '!', '?', '\n')):
            good_boundaries += 1

    results["valid_chunks"] = valid_chunks
    results["invalid_chunks"] = len(chunks) - valid_chunks
    results["avg_chunk_size"] = total_size / len(chunks) if chunks else 0
    results["coherence_score"] = valid_chunks / len(chunks) if chunks else 0
    results["boundary_preservation"] = good_boundaries / len(chunks) if chunks else 0

    return results


def recursive_chunk_by_tokens(text: str, max_tokens: int = 256, overlap_tokens: int = 32) -> List[str]:
    """
    Recursively chunk text based on token-like units (approximate).

    Args:
        text: Text to chunk
        max_tokens: Maximum tokens per chunk (approximate)
        overlap_tokens: Overlapping tokens between chunks (approximate)

    Returns:
        List of text chunks
    """
    # Approximate tokenization: assume 1 token = 4 characters
    approx_char_per_token = 4
    chunk_size_chars = max_tokens * approx_char_per_token
    overlap_chars = overlap_tokens * approx_char_per_token

    return chunk_text(text, chunk_size=chunk_size_chars, overlap=overlap_chars)


def preserve_section_boundaries(text: str, max_chunk_size: int = 800) -> List[str]:
    """
    Split text while preserving section boundaries (headings, etc.).

    Args:
        text: Text to chunk
        max_chunk_size: Maximum size of each chunk

    Returns:
        List of text chunks that respect section boundaries
    """
    # Split by common section markers (headings, etc.)
    section_pattern = r'(\n#{1,6}\s[^\n]*\n|\n={1,6}\s[^\n]*\n|\n\w+.*\n-{3,}\n)'
    sections = re.split(section_pattern, text)

    chunks = []
    current_chunk = ""

    for section in sections:
        # If adding this section would exceed the limit
        if len(current_chunk) + len(section) > max_chunk_size and current_chunk:
            # Add the current chunk to results
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            # Start a new chunk with the current section
            current_chunk = section
        else:
            # Add the section to the current chunk
            current_chunk += section

    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def validate_boundary_preservation(chunks: List[str], original_text: str) -> Dict[str, Any]:
    """
    Validate that chunks preserve paragraph and section boundaries appropriately.

    Args:
        chunks: List of text chunks to validate
        original_text: Original text that was chunked

    Returns:
        Dictionary with validation results
    """
    results = {
        "total_chunks": len(chunks),
        "boundary_preserved_chunks": 0,
        "boundary_preservation_rate": 0.0,
        "details": []
    }

    if not chunks:
        return results

    # Count chunks that end with sentence or paragraph boundaries
    boundary_preserved = 0

    for chunk in chunks:
        chunk_stripped = chunk.strip()
        if not chunk_stripped:
            continue

        # Check if chunk ends with sentence-ending punctuation followed by space/newline
        ends_with_sentence = bool(re.search(r'[.!?]\s*$', chunk))
        # Check if chunk ends with paragraph boundary (double newline)
        ends_with_paragraph = chunk.endswith('\n\n') or chunk.endswith('\n\r\n')

        is_boundary_preserved = ends_with_sentence or ends_with_paragraph

        results["details"].append({
            "chunk_length": len(chunk),
            "ends_with_sentence": ends_with_sentence,
            "ends_with_paragraph": ends_with_paragraph,
            "boundary_preserved": is_boundary_preserved
        })

        if is_boundary_preserved:
            boundary_preserved += 1

    results["boundary_preserved_chunks"] = boundary_preserved
    results["boundary_preservation_rate"] = boundary_preserved / len(chunks) if chunks else 0

    return results


if __name__ == "__main__":
    # Example usage
    sample_text = """
    # Introduction to AI
    Artificial Intelligence (AI) is a branch of computer science that aims to create software or machines that exhibit human-like intelligence. This can include learning from experience, understanding natural language, solving problems, and recognizing patterns.

    AI can be categorized into different types based on their capabilities and functionalities. The most common categorization includes narrow AI, general AI, and super AI.

    ## Machine Learning
    Machine Learning is a subset of AI that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. It focuses on the development of computer programs that can access data and use it to learn for themselves.

    The process of learning begins with observations or data, such as examples, direct experience, or instruction, in order to look for patterns in data and make better decisions in the future based on the examples that we provide.

    ## Deep Learning
    Deep Learning is a subset of machine learning that uses neural networks with many layers. These neural networks attempt to simulate the behavior of the human brain, though far from matching its ability. This enables the system to process data and create patterns for use in decision making.
    """

    chunks = chunk_text(sample_text, chunk_size=150, overlap=20)
    print(f"Created {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {len(chunk)} chars - '{chunk[:50]}...'")
        print()