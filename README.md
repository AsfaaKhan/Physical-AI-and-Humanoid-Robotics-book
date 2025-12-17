# Physical AI & Humanoid Robotics RAG Chatbot

A comprehensive RAG (Retrieval-Augmented Generation) chatbot system for the Physical AI & Humanoid Robotics book, featuring Google's Gemini 2.0 Flash model and Qdrant vector database.

## Features

- **RAG-powered Q&A**: Ask questions about the Physical AI & Humanoid Robotics book content
- **Selected Text Mode**: Answer questions using only selected text context
- **Citation Support**: View sources for all answers provided
- **Docusaurus Integration**: Seamless integration with Docusaurus documentation site
- **Full Stack**: Complete backend (FastAPI) and frontend (React) solution

## Architecture

### Backend Components
- **FastAPI**: Modern Python web framework for the API
- **Google Gemini 2.0 Flash**: Lightweight model for efficient question answering
- **Qdrant**: Vector database for semantic document retrieval
- **Sentence Transformers**: Embedding generation for document indexing
- **PostgreSQL (Neon)**: Metadata storage and chat history

### Frontend Components
- **Docusaurus**: Documentation site framework
- **React Widget**: Interactive chatbot interface
- **Text Selection**: Context-aware question answering

## Setup

### Backend Setup

1. Install Python dependencies:
```bash
cd chatbot-backend
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```env
GEMINI_API_KEY=your-gemini-api-key
QDRANT_URL=your-qdrant-url # or leave empty for local
QDRANT_API_KEY=your-qdrant-api-key
DATABASE_URL=your-postgres-connection-string
```

3. Start the backend server:
```bash
cd chatbot-backend
uvicorn main:app --reload
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd book
npm install
```

2. Start the Docusaurus development server:
```bash
npm run start
```

## API Endpoints

- `POST /api/v1/ask` - Ask questions about the book
- `POST /api/v1/embed` - Embed documents into the vector store
- `GET /api/v1/health` - Health check endpoint

### Ask Endpoint Request Format

```json
{
  "question": "Your question here",
  "selected_text": "Selected text context (optional)",
  "use_selected_text_only": true/false
}
```

### Response Format

```json
{
  "answer": "Generated answer",
  "citations": ["Source citations"],
  "context_used": "Context used for answering",
  "confidence_estimate": 0.8
}
```

## System Components

### RAG Pipeline
1. **Document Processing**: PDF, text, and URL document loading
2. **Text Splitting**: Chunking documents with overlap
3. **Embedding Generation**: Creating vector representations
4. **Vector Storage**: Storing embeddings in Qdrant
5. **Retrieval**: Semantic search for relevant documents
6. **Generation**: Answer generation using Gemini model

### Frontend Widget
- Persistent chat interface
- Text selection detection
- Context-aware responses
- Citation display
- Responsive design

## Environment Variables

Required configuration in `chatbot-backend/.env`:

```env
# Gemini API Configuration
GEMINI_API_KEY=your-api-key
GEMINI_MODEL=gemini-2.0-flash

# Qdrant Configuration
QDRANT_URL=your-qdrant-url
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=physical_ai_docs

# Database Configuration
DATABASE_URL=your-postgres-url

# Application Configuration
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

## Development

### Running Tests

```bash
# Backend tests
cd chatbot-backend
python -m pytest tests/

# System integration test
python system_test.py
```

### Building for Production

```bash
# Build backend Docker image
cd chatbot-backend
docker build -t rag-chatbot-backend .

# Build Docusaurus site
cd book
npm run build
```

## Troubleshooting

### Common Issues

1. **API Key Issues**: Ensure GEMINI_API_KEY and QDRANT_API_KEY are properly set
2. **Connection Issues**: Verify Qdrant and PostgreSQL connection strings
3. **CORS Issues**: Check ALLOWED_ORIGINS in configuration
4. **Embedding Issues**: Ensure proper sentence transformer model loading

### Debugging

Enable DEBUG mode in the environment variables for detailed logging.

## Security

- API keys are loaded from environment variables
- Rate limiting is implemented
- Input validation is performed on all endpoints
- CORS is configured (configure properly for production)

## License

This project is part of the Physical AI & Humanoid Robotics book implementation.