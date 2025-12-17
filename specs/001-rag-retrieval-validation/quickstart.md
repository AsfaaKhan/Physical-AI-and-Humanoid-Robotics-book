# Quickstart: Vector Retrieval and RAG Pipeline Validation

## Overview
Quick setup guide to run the retrieval validation system for the RAG pipeline.

## Prerequisites
- Python 3.11 or higher
- Access to the backend/ directory with existing ingestion pipeline
- Cohere API key (same as used for ingestion)
- Qdrant Cloud credentials (same as used for ingestion)
- The book embeddings must already be stored in Qdrant from the ingestion pipeline

## Setup Instructions

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Verify Dependencies
Ensure the following dependencies are available (they should already exist from the ingestion pipeline):
```bash
pip install cohere qdrant-client python-dotenv pytest
```

### 3. Environment Configuration
The retrieval system will use the same environment variables as the ingestion pipeline:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=rag_embedding_physical_ai_book
```

### 4. Run the Retrieval Validation
```bash
# Run a single query for validation
python -c "from src.retrieval.query_processor import process_query; result = process_query('your query here'); print(result)"

# Or run the validation script with sample queries
python retrieval.py --validate
```

## Usage Examples

### Basic Query
```python
from src.retrieval.query_processor import process_query

# Simple query
result = process_query("What is ROS2?")
print(f"Found {len(result.retrieved_chunks)} relevant chunks")
for chunk in result.retrieved_chunks:
    print(f"Score: {chunk.relevance_score}, URL: {chunk.source_url}")
    print(f"Content: {chunk.text_content[:200]}...")
```

### Query with Metadata Filtering
```python
from src.retrieval.query_processor import process_query_with_filters

# Query with URL filtering
filters = {"source_url": {"$contains": "ros2"}}
result = process_query_with_filters("ROS2 basics", filters, top_k=3)
```

### Validation Testing
```python
from src.retrieval.result_validator import validate_retrieval

# Validate retrieval quality
validation_result = validate_retrieval(query_text="What is physical AI?",
                                    expected_sources=["intro", "what-is-physical-ai"])
print(f"Validation score: {validation_result.overall_quality}")
```

## Expected Output
- Query results with relevance scores (0.0-1.0)
- Source URLs for traceability
- Performance metrics (latency, precision)
- Validation scores confirming quality

## Development Commands

### Run Tests
```bash
# Run all retrieval tests
python -m pytest tests/test_retrieval.py

# Run specific test
python -m pytest tests/test_query_processor.py
```

### Validation Testing
```bash
# Run comprehensive validation suite
python -m pytest tests/ -k "validation"
```

## Troubleshooting

### Common Issues:
1. **No Results**: Verify Qdrant collection has embeddings from ingestion pipeline
2. **API Key Errors**: Check Cohere and Qdrant API keys are correct
3. **Connection Issues**: Verify Qdrant URL and network connectivity

### Verify Setup:
```bash
# Test Cohere connection
python -c "import cohere; client = cohere.Client(os.getenv('COHERE_API_KEY')); print('Cohere connection OK')"

# Test Qdrant connection
python -c "from qdrant_client import QdrantClient; client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY')); print('Qdrant connection OK')"

# Verify collection exists
python -c "from qdrant_client import QdrantClient; client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY')); print('Collections:', client.get_collections())"
```