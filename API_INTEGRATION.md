# RAG Chatbot API Integration Documentation

## Overview

This document describes the integration between the frontend Docusaurus application and the backend RAG (Retrieval-Augmented Generation) chatbot API. The system enables users to ask questions about book content and receive answers grounded in the source material with proper citations.

## Architecture

### Frontend Components
- **Docusaurus Website**: Static site built with Docusaurus, hosting the book content
- **Chatbot Widget**: React component embedded in the site for chat functionality
- **Context System**: React Context for state management
- **API Service**: Service layer for API communication

### Backend Components
- **FastAPI Server**: Backend API server
- **RAG Agent**: Core system that retrieves relevant content and generates responses
- **Vector Database**: Storage for book content embeddings
- **Gemini API**: Language model for response generation

## API Endpoints

### Chat Endpoint
- **URL**: `POST /api/chat`
- **Description**: Process user questions and return RAG-enhanced responses
- **Request Body**:
  ```json
  {
    "question": "string",
    "session_id": "string|null",
    "selected_text": "string|null",
    "metadata": "object"
  }
  ```
- **Response**:
  ```json
  {
    "answer": "string",
    "sources": [
      {
        "url": "string",
        "title": "string",
        "content": "string",
        "relevance_score": "number"
      }
    ],
    "session_id": "string",
    "timestamp": "string",
    "status": "string",
    "confidence_score": "number|null",
    "metrics": "object|null"
  }
  ```

### Health Check Endpoint
- **URL**: `GET /`
- **Description**: Verify API server health
- **Response**:
  ```json
  {
    "message": "RAG Chatbot API is running"
  }
  ```

## Frontend Integration

### Chatbot Widget
The chatbot widget is implemented as a React component that:
1. Manages local state using React Context
2. Communicates with the backend API via the ChatbotService
3. Handles user interactions and displays responses
4. Maintains conversation history with localStorage persistence

### State Management
- **ChatbotContext**: Provides global state management for the chat interface
- **Message Storage**: Uses localStorage to persist conversations across page refreshes
- **Session Management**: Maintains session IDs for conversation continuity

### API Service
The `ChatbotService` handles:
- API communication with retry logic
- Error handling and user feedback
- Request/response transformation
- Loading states and user feedback

## Backend Implementation

### RAG Agent
The RAG agent implements:
- Content retrieval from vector database
- Context-aware response generation using Gemini API
- Source attribution and confidence scoring
- Performance metrics tracking

### Data Models
- **ChatRequest**: Validates and structures incoming requests
- **ChatResponse**: Formats responses with sources and metadata
- **SourceReference**: Represents source citations for responses

## Environment Configuration

### Frontend Environment Variables
- `REACT_APP_CHATBOT_API_URL`: Backend API URL (defaults to `http://localhost:8000`)

### Backend Environment Variables
- `GEMINI_API_KEY`: API key for Google's Gemini service
- `GEMINI_MODEL_NAME`: Name of the Gemini model to use (defaults to `gemini-pro`)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS

## Error Handling

### Frontend Error Handling
- Network error detection with retry mechanism
- User-friendly error messages
- Graceful degradation when API is unavailable
- Input validation before sending requests

### Backend Error Handling
- Input validation with appropriate HTTP status codes
- Logging for debugging and monitoring
- Graceful handling of API service unavailability
- Session recovery mechanisms

## Performance Considerations

### Caching
- Conversation state cached in localStorage
- Vector database embeddings for efficient retrieval

### Loading States
- Typing indicators during response generation
- Pending message indicators for user input
- Smooth UI transitions during API calls

### Rate Limiting
- API rate limiting to prevent abuse
- Session-based tracking for conversation continuity

## Security Considerations

### Input Validation
- Frontend validation for user inputs
- Backend validation for all API requests
- Sanitization of potentially harmful content

### API Access
- Environment-based API URL configuration
- CORS configuration for frontend integration
- Secure handling of API keys

## Deployment

### Frontend Deployment
- Static site generation with Docusaurus
- GitHub Pages deployment configuration
- Environment-specific API URL configuration

### Backend Deployment
- FastAPI server deployment options
- Vector database configuration
- Gemini API key management

## Testing

### Unit Tests
- Individual component testing
- API service functionality testing
- Data model validation

### Integration Tests
- Frontend-backend communication
- End-to-end conversation flow
- Error condition handling

### Performance Tests
- Response time monitoring
- Load testing for concurrent users
- Memory usage optimization

## Maintenance Guide

### Common Issues
1. **API Connection Issues**:
   - Verify backend server is running
   - Check `REACT_APP_CHATBOT_API_URL` configuration
   - Ensure CORS settings are correct

2. **Empty Responses**:
   - Check vector database content
   - Verify Gemini API key validity
   - Review RAG agent configuration

3. **Session Problems**:
   - Clear localStorage if corrupted
   - Verify session ID handling
   - Check backend session management

### Monitoring
- API response times
- Error rates and types
- User engagement metrics
- Vector database performance

### Updating Dependencies
- Frontend: Update package.json dependencies
- Backend: Update requirements.txt
- Test compatibility after updates

## Development Workflow

### Local Development
1. Start backend: `uvicorn src.main:app --reload`
2. Start frontend: `cd book && npm start`
3. Access frontend at `http://localhost:3000`

### Testing Changes
1. Run unit tests for affected components
2. Test end-to-end functionality
3. Verify error handling
4. Check responsive design
5. Validate accessibility features

## Future Enhancements

### Planned Features
- Multi-language support
- Advanced conversation memory
- File upload for custom content
- Advanced analytics and insights

### Performance Improvements
- Streaming responses
- More efficient vector search
- Caching layer optimization
- Better error recovery

## Troubleshooting

### Debugging API Issues
1. Check browser network tab for request/response details
2. Verify backend logs for error messages
3. Test API endpoints directly with tools like curl or Postman
4. Confirm environment variable configuration

### Common Configuration Issues
- Mismatched API URLs between frontend and backend
- Incorrect CORS settings
- Missing or invalid API keys
- Database connection problems

## Contact and Support

For issues with this integration:
- Check the GitHub repository for existing issues
- Review the project documentation
- Contact the development team for support