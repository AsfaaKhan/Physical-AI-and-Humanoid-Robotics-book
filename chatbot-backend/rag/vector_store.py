from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from typing import List, Dict, Any, Optional
from utils.config import settings
import logging
import uuid

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self):
        # Initialize Qdrant client based on configuration
        if settings.QDRANT_URL:
            # Use cloud instance
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
                prefer_grpc=True
            )
        else:
            # Use local instance
            self.client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT
            )

        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """
        Ensure the collection exists in Qdrant with proper configuration
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(
                collection.name == self.collection_name
                for collection in collections.collections
            )

            if not collection_exists:
                # Create collection with appropriate vector size for embeddings
                # Using 768 dimensions for sentence-transformers/all-MiniLM-L6-v2
                # Change to 1536 if using OpenAI embeddings
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=384,  # Size for sentence-transformers/all-MiniLM-L6-v2
                        distance=Distance.COSINE
                    )
                )

                # Create payload index for metadata
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="metadata",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {str(e)}")
            raise

    def add_documents(self, documents: List[Dict[str, Any]], embeddings: List[List[float]]):
        """
        Add documents with their embeddings to the vector store
        """
        try:
            # Prepare points for Qdrant
            points = []
            for doc, embedding in zip(documents, embeddings):
                point_id = str(uuid.uuid4())

                points.append(
                    models.PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload={
                            "content": doc.get("content", ""),
                            "metadata": doc.get("metadata", {}),
                            "document_id": doc.get("document_id", ""),
                            "chunk_index": doc.get("chunk_index", 0)
                        }
                    )
                )

            # Upload points to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
                wait=True
            )

            logger.info(f"Added {len(points)} documents to vector store")
            return [point.id for point in points]  # Return the IDs of added points
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise

    def similarity_search(self, query_embedding: List[float], k: int = 5, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Perform similarity search in the vector store
        """
        try:
            # Prepare filters if provided
            qdrant_filters = None
            if filters:
                filter_conditions = []
                for key, value in filters.items():
                    filter_conditions.append(
                        models.FieldCondition(
                            key=f"metadata.{key}",
                            match=models.MatchValue(value=value)
                        )
                    )

                if filter_conditions:
                    qdrant_filters = models.Filter(
                        must=filter_conditions
                    )

            # Perform search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=k,
                query_filter=qdrant_filters,
                with_payload=True,
                with_vectors=False
            )

            # Format results
            documents = []
            for result in results:
                documents.append({
                    "id": result.id,
                    "content": result.payload["content"],
                    "metadata": result.payload["metadata"],
                    "document_id": result.payload.get("document_id", ""),
                    "chunk_index": result.payload.get("chunk_index", 0),
                    "score": result.score
                })

            return documents
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            raise

    def delete_collection(self):
        """
        Delete the entire collection (useful for re-indexing)
        """
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            logger.info(f"Deleted Qdrant collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            raise

    def get_collection_info(self):
        """
        Get information about the collection
        """
        try:
            collection_info = self.client.get_collection(collection_name=self.collection_name)
            return {
                "vectors_count": collection_info.vectors_count,
                "indexed_vectors_count": collection_info.indexed_vectors_count,
                "points_count": collection_info.points_count
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            raise

    def delete_points(self, point_ids: List[str]):
        """
        Delete specific points from the collection
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=point_ids
                )
            )
            logger.info(f"Deleted {len(point_ids)} points from vector store")
        except Exception as e:
            logger.error(f"Error deleting points from vector store: {str(e)}")
            raise