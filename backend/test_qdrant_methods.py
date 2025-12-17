#!/usr/bin/env python3
"""
Test script to check available QdrantClient methods
"""

import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), "backend"))

from qdrant_client import QdrantClient
from config.settings import settings

def check_qdrant_methods():
    print("Checking QdrantClient methods...")

    # Initialize a client (without connecting to avoid network calls)
    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        prefer_grpc=False
    )

    # List all methods that contain 'search' or 'query'
    methods = [method for method in dir(client) if not method.startswith('_')]
    search_methods = [method for method in methods if 'search' in method.lower() or 'query' in method.lower() or 'retrieve' in method.lower()]

    print(f"All available methods: {methods}")
    print(f"\nMethods related to search/query/retrieve: {search_methods}")

    # Check the version and see if we need to use a different method
    import qdrant_client
    print(f"\nQdrant client version: {qdrant_client.__version__}")

if __name__ == "__main__":
    check_qdrant_methods()