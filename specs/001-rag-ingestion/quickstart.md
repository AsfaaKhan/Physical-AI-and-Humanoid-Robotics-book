# Quickstart: RAG Knowledge Ingestion Pipeline

## Overview
Quick setup guide to run the RAG knowledge ingestion pipeline for the Physical AI and Humanoid Robotics book.

## Prerequisites
- Python 3.11 or higher
- `uv` package manager installed
- Cohere API key
- Qdrant Cloud account and API credentials

## Setup Instructions

### 1. Clone and Navigate to Backend
```bash
# If you haven't already, create the backend directory
mkdir backend && cd backend
```

### 2. Install uv Package Manager (if not already installed)
```bash
pip install uv
# Or using other methods: https://github.com/astral-sh/uv
```

### 3. Create Project Structure
```bash
cd backend
uv init
```

### 4. Set up Environment Variables
Create a `.env` file in the backend directory:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
BOOK_BASE_URL=https://physical-ai-and-humanoid-robotics-book-p71goqgvj.vercel.app/
QDRANT_COLLECTION_NAME=rag_embedding_physical_ai_book
```

### 5. Install Dependencies
```bash
uv pip install requests beautifulsoup4 cohere qdrant-client python-dotenv
```

Or create a `requirements.txt` file:
```txt
requests==2.31.0
beautifulsoup4==4.12.2
cohere==4.4.3
qdrant-client==1.9.1
python-dotenv==1.0.0
pytest==8.0.0
```

### 6. Run the Ingestion Pipeline
```bash
# From the backend directory
python main.py
```

## Development Commands

### Run Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_crawler.py
```

### Environment Setup Check
```bash
# Verify all required environment variables are set
python -c "import os; [print(f'{k}: {v}') for k,v in os.environ.items() if k in ['COHERE_API_KEY', 'QDRANT_URL', 'QDRANT_API_KEY']]"
```

## Expected Output
- All pages from the book website will be crawled
- Content will be extracted and cleaned
- Text will be chunked into semantic segments
- Embeddings will be generated using Cohere
- Data will be stored in Qdrant collection: `rag_embedding_physical_ai_book`

## Troubleshooting

### Common Issues:
1. **API Key Errors**: Verify your Cohere and Qdrant API keys are correct
2. **Connection Issues**: Check your internet connection and firewall settings
3. **Rate Limiting**: The pipeline includes delays to respect website rate limits

### Verify Setup:
```bash
# Test Cohere connection
python -c "import cohere; client = cohere.Client(os.getenv('COHERE_API_KEY')); print('Cohere connection OK')"

# Test Qdrant connection
python -c "from qdrant_client import QdrantClient; client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY')); print('Qdrant connection OK')"
```