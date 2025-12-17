#!/usr/bin/env python3
"""
Main retrieval module for the RAG Pipeline Validation system.

This module provides the core functionality for:
- Accepting natural language queries
- Generating query embeddings using Cohere
- Performing vector similarity search against Qdrant
- Retrieving top-k relevant chunks with metadata
- Supporting optional metadata filtering
- Validating retrieval results for relevance and consistency
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import sys
import argparse

# Import the core retrieval components
from src.retrieval.query_processor import process_query
from src.retrieval.vector_search import search_similar_chunks
from src.retrieval.result_validator import validate_retrieval_result
from config.settings import settings


def main():
    """
    Main function to run the retrieval validation system.
    """
    parser = argparse.ArgumentParser(description='RAG Retrieval Validation System')
    parser.add_argument('--query', '-q', type=str, help='Natural language query to process')
    parser.add_argument('--top-k', type=int, default=5, help='Number of results to retrieve (default: 5)')
    parser.add_argument('--validate', action='store_true', help='Run validation on results')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger = logging.getLogger(__name__)

    # Validate configuration
    if not settings.validate():
        logger.error("Configuration validation failed. Please check your environment variables.")
        sys.exit(1)

    logger.info("RAG Retrieval Validation System initialized")

    if args.query:
        # Process the provided query
        logger.info(f"Processing query: {args.query}")

        try:
            result = process_query(
                query_text=args.query,
                top_k=args.top_k
            )

            print(f"\nQuery: {args.query}")
            print(f"Retrieved {len(result.retrieved_chunks)} chunks:")

            for i, chunk in enumerate(result.retrieved_chunks):
                print(f"\n{i+1}. Score: {chunk.relevance_score:.3f}")
                print(f"   Source: {chunk.source_url}")
                print(f"   Title: {chunk.page_title}")
                print(f"   Content Preview: {chunk.text_content[:200]}...")

            if args.validate:
                logger.info("Running validation on results...")
                validation_result = validate_retrieval_result(result)
                print(f"\nValidation Results:")
                print(f"  Precision: {validation_result.precision_score:.3f}")
                print(f"  Traceability: {validation_result.traceability_score:.3f}")
                print(f"  Consistency: {validation_result.consistency_score:.3f}")
                print(f"  Overall Quality: {validation_result.overall_quality:.3f}")

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            sys.exit(1)
    else:
        # Interactive mode
        print("\nRAG Retrieval Validation System")
        print("Enter queries to test the retrieval system (type 'quit' to exit)\n")

        while True:
            try:
                query = input("Enter query: ").strip()
                if query.lower() in ['quit', 'exit', 'q']:
                    break

                if not query:
                    continue

                result = process_query(query_text=query, top_k=args.top_k)

                print(f"\nRetrieved {len(result.retrieved_chunks)} chunks:")

                for i, chunk in enumerate(result.retrieved_chunks):
                    print(f"\n{i+1}. Score: {chunk.relevance_score:.3f}")
                    print(f"   Source: {chunk.source_url}")
                    print(f"   Title: {chunk.page_title}")
                    print(f"   Content Preview: {chunk.text_content[:200]}...")

                if args.validate:
                    validation_result = validate_retrieval_result(result)
                    print(f"\nValidation Results:")
                    print(f"  Precision: {validation_result.precision_score:.3f}")
                    print(f"  Traceability: {validation_result.traceability_score:.3f}")
                    print(f"  Consistency: {validation_result.consistency_score:.3f}")
                    print(f"  Overall Quality: {validation_result.overall_quality:.3f}")

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                logger.error(f"Error processing query: {str(e)}")
                continue

    logger.info("RAG Retrieval Validation System completed")


if __name__ == "__main__":
    main()