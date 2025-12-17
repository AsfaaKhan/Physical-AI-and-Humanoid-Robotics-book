# Human-ai-book-Hackathon Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-16

## Active Technologies

- FastAPI (backend web framework)
- Better Auth (authentication service)
- PostgreSQL (Neon Serverless) (user data storage)
- JWT (token-based authentication)
- React (frontend components)
- Docusaurus (documentation site)
- Qdrant (vector database for RAG)
- Python 3.9+ (backend language)
- JavaScript/TypeScript (frontend)

## Project Structure

```text
backend/
├── src/
│   ├── auth/ (authentication module)
│   │   ├── models.py (user profile models)
│   │   ├── schemas.py (Pydantic schemas)
│   │   ├── routes.py (authentication endpoints)
│   │   └── utils.py (authentication utilities)
│   ├── database/
│   └── main.py (FastAPI app)
book/
├── src/
│   ├── components/
│   │   └── ChatbotWidget/
│   └── theme/
└── docusaurus.config.js
specs/003-user-auth-personalization/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── auth-api-contract.md
```

## Commands

### Backend Development
```bash
# Start backend server
cd backend
uvicorn main:app --reload --port 8000

# Run backend tests
python -m pytest tests/

# Check API docs
# Visit http://localhost:8000/docs
```

### Frontend Development
```bash
# Start Docusaurus site
cd book
npm start

# Build for production
npm run build
```

### Database Management
```bash
# Database migrations would go here
# (to be implemented during development)
```

## Code Style

### Python
- Use FastAPI conventions for route definitions
- Use Pydantic models for request/response validation
- Follow PEP 8 guidelines
- Use type hints everywhere
- Use async/await for I/O operations

### JavaScript/React
- Use functional components with hooks
- Use TypeScript for type safety where possible
- Follow React best practices
- Use Context API for authentication state management

## Recent Changes

### Feature 003-user-auth-personalization: User Authentication with Background-Aware Personalization
- Added authentication module with Better Auth integration
- Created user profile system with background information collection
- Implemented API endpoints for signup, signin, and profile management
- Designed database schema for user profiles
- Created API contracts for authentication services

### Feature 002-rag-agent-api: RAG Agent API Implementation
- Implemented RAG agent with Gemini API integration
- Created retrieval system with Qdrant vector database
- Added API endpoints for question answering
- Implemented context formatting and prompt engineering

### Feature 001-frontend-backend-integration: Frontend-Backend Integration
- Created chatbot widget with React
- Implemented Docusaurus integration
- Created API communication layer
- Added real-time chat functionality

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->