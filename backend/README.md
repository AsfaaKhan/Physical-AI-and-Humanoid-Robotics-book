# RAG Knowledge Ingestion Pipeline

This project implements a complete RAG (Retrieval-Augmented Generation) knowledge ingestion pipeline that extracts content from the deployed Docusaurus book website (https://physical-ai-and-humanoid-robotics-book-p71goqgvj.vercel.app/), chunks it for semantic retrieval, generates Cohere embeddings, and stores them in Qdrant Cloud with proper metadata for downstream RAG-based question answering.

## Features

- **Website Crawling**: Discovers all pages from the Docusaurus book website using both sitemap parsing and recursive crawling
- **Content Extraction**: Extracts clean textual content while filtering out navigation, headers, footers, and other UI components
- **Semantic Chunking**: Splits content into semantically coherent segments optimized for retrieval
- **Embedding Generation**: Creates vector embeddings using Cohere's multilingual models
- **Vector Storage**: Stores embeddings with metadata in Qdrant Cloud for efficient similarity search
- **Error Handling**: Implements comprehensive error handling with retries and logging

## Prerequisites

- Python 3.11+
- `uv` package manager
- Cohere API key
- Qdrant Cloud account and API credentials

## Setup

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies using uv:
   ```bash
   cd backend
   uv pip install -r requirements.txt
   # Or if using pyproject.toml directly:
   uv sync
   ```

4. Create a `.env` file with your configuration:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_cloud_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   BOOK_BASE_URL=https://physical-ai-and-humanoid-robotics-book-p71goqgvj.vercel.app/
   QDRANT_COLLECTION_NAME=rag_embedding_physical_ai_book
   ```

## Usage

### Run the Complete Pipeline

```bash
cd backend
python main.py
```

This will:
1. Discover all pages from the book website
2. Extract clean content from each page
3. Chunk content semantically
4. Generate embeddings using Cohere
5. Store embeddings in Qdrant with metadata

### Run Individual Components

You can also run individual components for testing or development:

```bash
# Test crawler functionality
python -m src.crawler

# Test extractor functionality
python -m src.extractor

# Test chunker functionality
python -m src.chunker

# Test embedder functionality
python -m src.embedder

# Test storage functionality
python -m src.storage
```

## Project Structure

```
backend/
├── main.py                    # Main ingestion pipeline orchestrator
├── pyproject.toml            # uv project configuration
├── requirements.txt          # Dependencies list
├── .env                     # Environment variables
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── config/
│   └── settings.py          # Configuration management
├── src/
│   ├── __init__.py
│   ├── crawler.py           # URL discovery and content fetching
│   ├── extractor.py         # Text extraction and cleaning
│   ├── chunker.py           # Text chunking logic
│   ├── embedder.py          # Embedding generation
│   └── storage.py           # Qdrant storage operations
└── tests/
    ├── __init__.py
    ├── test_crawler.py
    ├── test_extractor.py
    ├── test_chunker.py
    ├── test_embedder.py
    └── test_storage.py
```

## Testing

Run all tests using pytest:

```bash
cd backend
python -m pytest tests/ -v
```

Run specific test files:

```bash
python -m pytest tests/test_crawler.py -v
python -m pytest tests/test_extractor.py -v
```

## Configuration

The pipeline can be configured through environment variables in the `.env` file:

- `COHERE_API_KEY`: Your Cohere API key for generating embeddings
- `QDRANT_URL`: URL for your Qdrant Cloud instance
- `QDRANT_API_KEY`: API key for Qdrant Cloud
- `BOOK_BASE_URL`: Base URL of the book website to crawl (default: https://physical-ai-and-humanoid-robotics-book-p71goqgvj.vercel.app/)
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection (default: rag_embedding_physical_ai_book)

## Error Handling

The pipeline includes comprehensive error handling:
- Website unavailability: Retry with exponential backoff
- Rate limiting: Proper delays between requests
- Embedding failures: Log and continue with other chunks
- Qdrant storage failures: Batch operations with retry logic

## Performance

The pipeline is designed to process 100+ pages within 10 minutes with embeddings generated under 1 second per chunk. Performance may vary based on network conditions and API response times.

## License

This project is part of the Physical AI & Humanoid Robotics book project.