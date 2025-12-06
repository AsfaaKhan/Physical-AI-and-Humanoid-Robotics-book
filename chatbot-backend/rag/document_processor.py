from typing import List, Dict, Any, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredURLLoader,
    BSHTMLLoader
)
from sentence_transformers import SentenceTransformer
from utils.config import settings
import logging
import requests
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class DocumentProcessor:
    def __init__(self):
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
        )

        # Initialize sentence transformer model for embeddings
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def load_document(self, source: str, source_type: str = "auto") -> List[Dict[str, Any]]:
        """
        Load a document from various sources
        """
        try:
            # Determine source type if not specified
            if source_type == "auto":
                if source.startswith(('http://', 'https://')):
                    source_type = "url"
                elif source.endswith('.pdf'):
                    source_type = "pdf"
                elif source.endswith(('.txt', '.md', '.py', '.js', '.html', '.css')):
                    source_type = "text"
                else:
                    source_type = "text"

            # Validate URL format if source_type is url
            if source_type == "url":
                parsed = urlparse(source)
                if not all([parsed.scheme, parsed.netloc]):
                    raise ValueError(f"Invalid URL format: {source}")

                # Check if URL is accessible
                try:
                    response = requests.head(source, timeout=10)
                    if response.status_code >= 400:
                        logger.warning(f"URL may not be accessible: {source} (status: {response.status_code})")
                except requests.RequestException as e:
                    logger.warning(f"Could not validate URL {source}: {str(e)}")

            # Load document based on type
            raw_docs = []
            if source_type == "url":
                loader = UnstructuredURLLoader(urls=[source])
                raw_docs = loader.load()
            elif source_type == "pdf":
                loader = PyPDFLoader(source)
                raw_docs = loader.load()
            elif source_type == "text":
                if source.endswith('.html'):
                    loader = BSHTMLLoader(source)
                    raw_docs = loader.load()
                else:
                    loader = TextLoader(source, encoding='utf-8')
                    raw_docs = loader.load()
            else:
                raise ValueError(f"Unsupported source type: {source_type}")

            # Convert to the format expected by our system
            documents = []
            for i, doc in enumerate(raw_docs):
                documents.append({
                    "content": doc.page_content,
                    "metadata": {
                        **doc.metadata,
                        "source": source,
                        "source_type": source_type,
                        "chunk_index": i
                    }
                })

            logger.info(f"Loaded {len(documents)} documents from {source}")
            return documents
        except Exception as e:
            logger.error(f"Error loading document from {source}: {str(e)}")
            raise

    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Split documents into chunks
        """
        try:
            chunked_docs = []
            for doc in documents:
                content = doc["content"]
                metadata = doc["metadata"]

                # Split the content
                splits = self.text_splitter.split_text(content)

                for i, split in enumerate(splits):
                    chunked_docs.append({
                        "content": split,
                        "metadata": {**metadata, "chunk_index": i}
                    })

            logger.info(f"Chunked {len(documents)} documents into {len(chunked_docs)} chunks")
            return chunked_docs
        except Exception as e:
            logger.error(f"Error chunking documents: {str(e)}")
            raise

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using sentence transformer model
        """
        try:
            # Generate embeddings using sentence transformer
            embeddings = self.embedding_model.encode(texts).tolist()
            logger.info(f"Generated embeddings for {len(texts)} text chunks")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def process_document(self, source: str, source_type: str = "auto") -> Tuple[List[Dict[str, Any]], List[List[float]]]:
        """
        Complete processing pipeline: load, chunk, and embed documents
        """
        try:
            # Load documents
            raw_docs = self.load_document(source, source_type)

            # Chunk documents
            chunked_docs = self.chunk_documents(raw_docs)

            # Extract text content for embedding
            texts = [doc["content"] for doc in chunked_docs]

            # Generate embeddings
            embeddings = self.generate_embeddings(texts)

            return chunked_docs, embeddings
        except Exception as e:
            logger.error(f"Error processing document {source}: {str(e)}")
            raise

    def process_multiple_documents(self, sources: List[str], source_types: List[str] = None) -> Tuple[List[Dict[str, Any]], List[List[float]]]:
        """
        Process multiple documents and combine them
        """
        try:
            all_chunked_docs = []
            all_embeddings = []

            for i, source in enumerate(sources):
                source_type = source_types[i] if source_types and i < len(source_types) else "auto"

                chunked_docs, embeddings = self.process_document(source, source_type)

                all_chunked_docs.extend(chunked_docs)
                all_embeddings.extend(embeddings)

            logger.info(f"Processed {len(sources)} sources into {len(all_chunked_docs)} total chunks")
            return all_chunked_docs, all_embeddings
        except Exception as e:
            logger.error(f"Error processing multiple documents: {str(e)}")
            raise