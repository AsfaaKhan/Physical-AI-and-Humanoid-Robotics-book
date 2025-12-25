from fastapi import APIRouter, HTTPException 
from typing import Optional, Dict, Any
import uuid
from datetime import datetime
import logging

# Import Pydantic models from the models module
from pydantic import BaseModel, Field # type: ignore
from typing import List, Optional
from src.models.chat_models import ChatRequest, ChatResponse, SourceReference, ErrorResponse

# Import the RAG agent
from src.rag_agent.rag_agent import get_rag_agent, AgentResponse


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the API router
app = APIRouter()


@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Send a question to the RAG agent
    Processes user questions and returns answers grounded in book content with source references
    """
    try:
        # Validate input
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        # Generate a new session ID if none provided
        session_id = request.session_id or str(uuid.uuid4())

        # Get the RAG agent instance
        rag_agent = get_rag_agent()

        # Process the question using the RAG agent
        agent_response = rag_agent.ask(
            question=request.question,
            filters=request.metadata or {},  # Use metadata for filtering if provided
            conversation_history=None,  # For now, not using conversation history
            selected_text=request.selected_text  # Pass selected text for higher priority context
        )

        # Convert the agent response to the API response format
        sources = []
        for source in agent_response.sources:
            sources.append(SourceReference(
                url=source.get('source_url', ''),
                title=source.get('page_title', ''),
                content=source.get('text_snippet', ''),
                relevance_score=source.get('relevance_score', 0.0)
            ))

        response = ChatResponse(
            answer=agent_response.answer_text,
            sources=sources,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            status="success",
            confidence_score=agent_response.confidence_score,
            metrics={
                'retrieval_time_ms': agent_response.retrieval_time_ms,
                'generation_time_ms': agent_response.generation_time_ms,
                'total_time_ms': agent_response.total_time_ms
            }
        )

        logger.info(f"Processed question: '{request.question[:50]}...', Session: {session_id}")
        return response

    except HTTPException:
        # Re-raise HTTP exceptions (like 400) to preserve status codes
        raise
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error occurred")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)