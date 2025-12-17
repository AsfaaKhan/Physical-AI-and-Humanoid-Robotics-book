#!/usr/bin/env python3
"""
Test script to debug Qdrant connection issues
"""

import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), "backend"))

from config.settings import settings
from src.retrieval.vector_search import validate_qdrant_connection, initialize_qdrant_client

def test_qdrant_connection():
    print("Testing Qdrant connection...")
    print(f"QDRANT_URL: {settings.QDRANT_URL}")
    print(f"QDRANT_COLLECTION_NAME: {settings.QDRANT_COLLECTION_NAME}")

    # Validate settings
    if not settings.validate():
        print("ERROR: Required environment variables are missing!")
        return False

    print("Environment variables are set correctly.")

    # Test connection
    try:
        success = validate_qdrant_connection()
        if success:
            print("SUCCESS: Qdrant connection is working!")
        else:
            print("ERROR: Qdrant connection failed or collection not found!")
            return False
    except Exception as e:
        print(f"ERROR: Exception during Qdrant connection test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    # Try to initialize client and search with a dummy query
    try:
        client = initialize_qdrant_client()
        print("Successfully initialized Qdrant client.")

        # Try to search with a dummy query using query_points (without specifying vector name)
        response = client.query_points(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query=[0.1] * 1024,  # Use same dimension as Cohere embeddings
            limit=1
        )
        results = response.points  # Access the points from the response
        print(f"Query executed successfully, found {len(results)} results.")

    except Exception as e:
        print(f"ERROR: Exception during search test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    success = test_qdrant_connection()
    if success:
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nTests failed!")
        sys.exit(1)