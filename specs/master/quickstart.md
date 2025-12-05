# Quickstart Guide: Physical AI & Humanoid Robotics Book + RAG System

## Overview

This guide will help you set up and run the Physical AI & Humanoid Robotics book with its integrated RAG (Retrieval-Augmented Generation) chatbot. The system consists of a Docusaurus-based book frontend and a FastAPI backend for the RAG functionality.

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.11 or higher)
- Git
- Access to OpenAI or Gemini API key
- Qdrant Cloud account (free tier)
- Neon Postgres account (free tier)

## Setting Up the Book Frontend

### 1. Clone the Repository

```bash
git clone <repository-url>
cd HUMAN-AI-BOOK-HACKATHON
```

### 2. Install Docusaurus Dependencies

```bash
cd book
npm install
```

### 3. Run the Development Server

```bash
npm run start
```

This will start the book at `http://localhost:3000`.

## Setting Up the RAG Backend

### 1. Navigate to Backend Directory

```bash
cd chatbot-backend
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `chatbot-backend` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
# OR for Gemini:
GEMINI_API_KEY=your_gemini_api_key_here

QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key

NEON_POSTGRES_URL=your_neon_postgres_connection_string

# Optional: Set your Docusaurus site URL for CORS
FRONTEND_URL=http://localhost:3000
```

### 4. Run the Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`.

## Initializing the RAG System

### 1. Index the Book Content

First, you need to extract and index the book content into the vector store:

```bash
# From the chatbot-backend directory
python -m app.rag.embed
```

This will:
- Extract text from the book markdown files
- Chunk the content into appropriate sizes
- Generate embeddings using the configured LLM
- Store the embeddings in Qdrant with metadata

### 2. Verify the Setup

Check the health of your API:

```bash
curl http://localhost:8000/health
```

## Testing the RAG Functionality

### 1. Test the Chat Endpoint

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "query": "What are the key components of ROS2?",
    "session_id": "test-session-123"
  }'
```

### 2. Test the Search Endpoint

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "query": "How does Gazebo simulate physics?",
    "top_k": 3
  }'
```

## Integrating the Chatbot with the Book

The chatbot UI components are already set up in the book's source directory. To connect the frontend to your backend:

1. Update the API configuration in `book/src/config/chatbot.js`:

```javascript
const CHATBOT_CONFIG = {
  API_BASE_URL: 'http://localhost:8000', // Update this to your backend URL
  API_KEY: 'your-api-key', // Consider how you want to handle API keys securely
  ENABLED: true,
};

export default CHATBOT_CONFIG;
```

2. The chatbot widget should now appear on all book pages.

## Deployment

### Deploying the Book to GitHub Pages

1. Update the `docusaurus.config.js` with your repository details:

```javascript
module.exports = {
  // ...
  url: 'https://your-username.github.io',
  baseUrl: '/your-repo-name/',
  organizationName: 'your-username',
  projectName: 'your-repo-name',
  // ...
};
```

2. Build the static site:

```bash
cd book
npm run build
```

3. Deploy using GitHub Actions or manually push to the `gh-pages` branch.

### Deploying the Backend

Deploy the FastAPI backend to a cloud provider like Railway, Render, or Fly.io:

1. Create an account on your preferred platform
2. Connect your GitHub repository
3. Set the environment variables in the platform's settings
4. Deploy the application

## Development Workflow

### Adding New Book Content

1. Create new markdown files in the appropriate module directory under `book/docs/`
2. Update `book/sidebars.js` to include the new content in the navigation
3. Rebuild the book: `npm run build` or restart the dev server
4. Re-index the content for the RAG system: `python -m app.rag.embed`

### Updating the RAG Index

When you add or modify book content, re-run the embedding process:

```bash
cd chatbot-backend
python -m app.rag.embed
```

This will update the vector store with the latest content.

## Troubleshooting

### Common Issues

1. **Backend not connecting to frontend**: Check CORS settings and ensure the API base URL is correctly configured.

2. **API rate limits**: If you encounter rate limiting, consider implementing caching or using a different API key.

3. **Slow responses**: Check your Qdrant and database connection speeds; consider optimizing your embedding chunk size.

4. **No results from RAG**: Verify that the book content has been properly indexed by running the embedding process.

### Useful Commands

```bash
# Check backend health
curl http://localhost:8000/health

# List all book documents available to RAG
curl -H "X-API-Key: your-api-key" http://localhost:8000/documents

# Test specific search
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"query": "your query here"}'
```

## Next Steps

1. Add your first book content to the `book/docs/` directory
2. Configure your API keys and deploy the backend
3. Index your content using the embedding script
4. Test the integration between frontend and backend
5. Customize the chatbot UI to match your book's theme