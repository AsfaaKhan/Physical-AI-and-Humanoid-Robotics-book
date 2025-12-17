# Quickstart: Frontend ↔ Backend Chatbot Integration

## Prerequisites
- Node.js 18+ for Docusaurus frontend
- Python 3.11+ for FastAPI backend
- Access to Qdrant vector database
- Gemini API key (free tier)

## Setup Instructions

### 1. Backend Setup
```bash
cd backend
pip install fastapi uvicorn python-dotenv qdrant-client
# Configure environment variables (QDRANT_URL, GEMINI_API_KEY)
uvicorn src.main:app --reload
```

### 2. Frontend Setup
```bash
cd book
npm install
npm run start
```

### 3. Enable CORS in FastAPI
Add CORS middleware to your FastAPI application:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. Environment Variables
Create `.env` file in backend:
```
QDRANT_URL=your_qdrant_url
GEMINI_API_KEY=your_gemini_api_key
```

## API Endpoints

### Chat Endpoint
- **POST** `/api/chat`
- Request: `{"question": "string", "session_id": "string", "selected_text": "string"}`
- Response: `{"answer": "string", "sources": [...], "session_id": "string"}`

## Frontend Integration

### Chatbot Widget
The chatbot widget will be available on all pages via the Docusaurus theme integration. It appears as a floating button that expands to show the chat interface.

### Text Selection
Users can select text on any page and click the chatbot to ask questions about the selected content. The selected text will be automatically included as context.

## Development Workflow

1. Start backend: `cd backend && uvicorn src.main:app --reload`
2. Start frontend: `cd book && npm run start`
3. Access frontend at `http://localhost:3000`
4. Test chat functionality with the embedded widget

## Testing End-to-End

1. Verify backend API is accessible from frontend
2. Test basic question answering
3. Test selected text context feature
4. Test error handling and loading states
5. Verify source citations are displayed properly