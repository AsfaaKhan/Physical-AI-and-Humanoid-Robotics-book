# Physical AI & Humanoid Robotics RAG Chatbot Backend

This is the backend service for the Physical AI & Humanoid Robotics RAG (Retrieval Augmented Generation) chatbot that uses Google's Gemini 2.0 Flash model for inference.

## Features

- **RAG System**: Uses vector embeddings and similarity search to find relevant book content
- **Gemini 2.0 Flash**: Free model for cost-effective inference
- **Document Ingestion**: API endpoints to add new documents to the knowledge base
- **Selected Text Mode**: Ability to answer questions only based on selected text
- **Citation Support**: Provides citations to specific book chapters/sections
- **Qdrant Vector Store**: Efficient vector similarity search
- **PostgreSQL Database**: For metadata storage

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   FastAPI        │───▶│   Qdrant        │
│   (Docusaurus)  │    │   Backend        │    │   Vector DB     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                       ┌──────────────────┐
                       │   PostgreSQL     │
                       │   (Neon)         │
                       └──────────────────┘
```

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (recommended)
- Google Gemini API Key (free tier available)

## Setup

### Environment Configuration

1. Create a `.env` file in the `chatbot-backend` directory:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/physical_ai_book
QDRANT_URL=https://your-cluster-url.qdrant.io  # Optional, for cloud
QDRANT_API_KEY=your_qdrant_api_key_here        # Optional, for cloud
QDRANT_HOST=localhost                          # For local development
QDRANT_PORT=6333
SECRET_KEY=your_secret_key_for_jwt_tokens
```

### Local Development

1. **Install dependencies:**
```bash
cd chatbot-backend
pip install -r requirements.txt
```

2. **Run with Docker Compose (recommended):**
```bash
docker-compose up --build
```

3. **Or run directly (requires separate Qdrant and PostgreSQL):**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints

- `POST /api/v1/ask` - Ask questions about the book
  - Request body: `{ "question": "string", "selected_text": "string", "use_selected_text_only": boolean }`
  - Response: `{ "answer": "string", "citations": [...], "context_used": "string", "confidence_estimate": number }`

- `POST /api/v1/embed` - Embed documents into the vector store
- `GET /api/v1/health` - Health check
- `GET /docs` - Interactive API documentation

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key (free tier available) | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `QDRANT_URL` | Qdrant cloud URL (or omit for local) | Optional |
| `QDRANT_API_KEY` | Qdrant API key (if using cloud) | Optional |
| `QDRANT_HOST` | Qdrant host | Yes (default: localhost) |
| `QDRANT_PORT` | Qdrant port | Yes (default: 6333) |
| `SECRET_KEY` | JWT secret key | Yes |

### How to Get API Keys

#### Google Gemini API Key (Required)
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click on "Get API Key"
4. Create a new API key
5. Use the free `gemini-2.0-flash` model

#### Neon PostgreSQL (Database)
1. Go to [Neon Console](https://neon.tech/)
2. Sign up or log in to your account
3. Create a new project
4. In the project dashboard, find your connection details
5. The connection string will be in the format: `postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname`

#### Qdrant (Vector Database)
For local development: No setup needed, Docker Compose will start a local instance
For cloud: Go to [Qdrant Cloud](https://qdrant.tech/) and create an account

## Usage

### Asking Questions

The chatbot can answer questions in two modes:

1. **Full RAG Mode**: Answers based on the entire book content
```json
{
  "question": "What is Physical AI?"
}
```

2. **Selected Text Mode**: Answers only based on selected text
```json
{
  "question": "What does this text say about robotics?",
  "selected_text": "Robotics is the interdisciplinary branch of engineering and science...",
  "use_selected_text_only": true
}
```

### Document Ingestion

To add new documents to the knowledge base:
```bash
curl -X POST http://localhost:8000/api/v1/embed \
  -H "Content-Type: application/json" \
  -d '{
    "sources": ["https://example.com/document.pdf"]
  }'
```

## Deployment

### To Render/Heroku/GCP/AWS

1. Set up environment variables in your deployment platform
2. Build and deploy the Docker image
3. Ensure Qdrant and PostgreSQL are accessible
4. Update the frontend to point to your deployed backend URL

### With Docker Compose (Production)

Update the docker-compose.yml for production settings and run:
```bash
docker-compose up -d
```

## Frontend Integration

The chatbot widget is designed to be integrated into the Docusaurus frontend. See the `book/src/components/ChatbotWidget` directory for the React component that connects to this backend.

## Error Handling

- All API endpoints return appropriate HTTP status codes
- Detailed error messages in response body
- Comprehensive logging for debugging
- Rate limiting to prevent abuse

## Security

- JWT-based authentication for protected endpoints
- Input validation on all endpoints
- CORS configured for secure cross-origin requests
- Secrets stored in environment variables

## Troubleshooting

### Common Issues

1. **"API Key not configured"**: Verify your `GEMINI_API_KEY` is set correctly
2. **Qdrant connection errors**: Check that Qdrant is running and accessible
3. **Database connection errors**: Verify your `DATABASE_URL` is correct
4. **Embedding errors**: Ensure documents are accessible and in supported formats

### Logs

Check application logs:
```bash
docker-compose logs backend
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.