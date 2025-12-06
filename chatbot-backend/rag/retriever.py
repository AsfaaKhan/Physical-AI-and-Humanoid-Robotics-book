from typing import List, Dict, Any, Optional
from .vector_store import VectorStore
from .document_processor import DocumentProcessor
from utils.config import settings
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)


class Retriever:
    def __init__(self):
        self.vector_store = VectorStore()
        self.document_processor = DocumentProcessor()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def get_relevant_documents(self, query: str, k: int = 5, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a given query
        """
        try:
            # Generate embedding for the query using sentence transformer
            query_embedding = self.embedding_model.encode([query]).tolist()[0]

            # Perform similarity search
            relevant_docs = self.vector_store.similarity_search(
                query_embedding=query_embedding,
                k=k,
                filters=filters
            )

            return relevant_docs
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise

    def format_documents(self, docs: List[Dict[str, Any]], max_length: int = 500) -> str:
        """
        Format retrieved documents into a string for the LLM
        """
        formatted = []
        for i, doc in enumerate(docs):
            content = doc["content"]
            if len(content) > max_length:
                content = content[:max_length] + "..."

            source = doc["metadata"].get("source", "Unknown")
            formatted.append(f"Document {i+1}: {content}\nSource: {source}\nScore: {doc['score']:.3f}\n")

        return "\n".join(formatted)

    def retrieve_and_format(self, query: str, k: int = 5, filters: Optional[Dict] = None, max_length: int = 500) -> tuple:
        """
        Retrieve documents and format them for LLM consumption
        """
        try:
            relevant_docs = self.get_relevant_documents(query, k, filters)
            formatted_context = self.format_documents(relevant_docs, max_length)
            return formatted_context, relevant_docs
        except Exception as e:
            logger.error(f"Error retrieving and formatting documents: {str(e)}")
            raise

    def get_citations(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract citations from retrieved documents
        """
        citations = []
        for doc in docs:
            citation = {
                "content": doc["content"][:200] + "..." if len(doc["content"]) > 200 else doc["content"],
                "source": doc["metadata"].get("source", "Unknown"),
                "score": doc["score"],
                "metadata": doc["metadata"]
            }
            citations.append(citation)

        return citations

    def search_by_selected_text(self, selected_text: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search specifically in the context of selected text only
        """
        try:
            # Generate embedding for the selected text using sentence transformer
            selected_text_embedding = self.embedding_model.encode([selected_text]).tolist()[0]

            # Perform similarity search
            relevant_docs = self.vector_store.similarity_search(
                query_embedding=selected_text_embedding,
                k=k
            )

            return relevant_docs
        except Exception as e:
            logger.error(f"Error searching by selected text: {str(e)}")
            raise