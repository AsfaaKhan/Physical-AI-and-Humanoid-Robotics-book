"""
RAG Agent API Service

This module implements a FastAPI service that provides a RAG (Retrieval-Augmented Generation)
agent for answering questions about book content using Gemini API and vector database retrieval.
"""
import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks # type: ignore
from pydantic import BaseModel # type: ignore
from contextlib import asynccontextmanager

from config.settings import settings
from src.rag_agent.rag_agent import get_rag_agent, AgentResponse
from src.utils import setup_logging

# Initialize logging
logger = setup_logging()

# Pydantic models for request/response
class QuestionRequest(BaseModel):
    """
    Request model for asking questions to the RAG agent.
    """
    question_text: str
    session_id: Optional[str] = None
    context_window: Optional[int] = 5
    top_k: Optional[int] = 5
    filters: Optional[Dict[str, Any]] = None


class SourceReference(BaseModel):
    """
    Model for source attribution in responses.
    """
    source_url: str
    page_title: str
    chunk_index: int
    relevance_score: float
    text_snippet: str


class AnswerResponse(BaseModel):
    """
    Response model containing the answer and metadata.
    """
    answer_text: str
    sources: List[SourceReference]
    confidence_score: float
    retrieval_time_ms: float
    generation_time_ms: float
    session_id: Optional[str] = None


class ConversationTurn(BaseModel):
    """
    Model representing a single exchange in a conversation.
    """
    turn_id: int
    question: str
    answer: str
    timestamp: str
    sources_used: List[SourceReference]


class ConversationSession(BaseModel):
    """
    Model for maintaining conversation state.
    """
    session_id: str
    conversation_history: List[ConversationTurn]
    created_at: str
    last_accessed: str
    max_history_length: int = 10


# In-memory session store (for development - should use Redis in production)
session_store: Dict[str, ConversationSession] = {}


def create_app():
    """
    Create and configure the FastAPI application.
    """
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup
        logger.info("Starting RAG Agent API Service...")
        # Validate required configurations
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not found in settings")
        if not settings.QDRANT_URL or not settings.QDRANT_API_KEY:
            logger.warning("QDRANT configuration not found in settings")

        yield

        # Shutdown
        logger.info("Shutting down RAG Agent API Service...")

    app = FastAPI(
        title="RAG Agent API Service",
        description="A RAG (Retrieval-Augmented Generation) agent for answering questions about book content",
        version="1.0.0",
        lifespan=lifespan
    )

    return app


app = create_app()


def get_session(session_id: Optional[str] = None) -> ConversationSession:
    """
    Get or create a conversation session.
    """
    if not session_id:
        # Create a new session
        import uuid
        session_id = str(uuid.uuid4())
        session = ConversationSession(
            session_id=session_id,
            conversation_history=[],
            created_at=datetime.now().isoformat(),
            last_accessed=datetime.now().isoformat()
        )
        session_store[session_id] = session
        return session

    # Get existing session or create new if not found
    if session_id not in session_store:
        session = ConversationSession(
            session_id=session_id,
            conversation_history=[],
            created_at=datetime.now().isoformat(),
            last_accessed=datetime.now().isoformat()
        )
        session_store[session_id] = session
        return session

    # Update last accessed time
    session_store[session_id].last_accessed = datetime.now().isoformat()
    return session_store[session_id]


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Endpoint to ask a question and get an answer from the RAG agent.
    """
    try:
        logger.info(f"Processing question: {request.question_text[:50]}...")

        # Retrieve conversation session
        session = get_session(request.session_id)

        # Prepare conversation history for context
        conversation_history = []
        if session.conversation_history:
            for turn in session.conversation_history[-request.context_window:]:
                conversation_history.append({
                    "question": turn.question,
                    "answer": turn.answer
                })

        # Get the RAG agent instance
        rag_agent = get_rag_agent()

        # Process the question using the RAG agent
        agent_response = rag_agent.ask(
            question=request.question_text,
            top_k=request.top_k,
            filters=request.filters,
            conversation_history=conversation_history
        )

        # Format sources for the response
        sources = []
        for source in agent_response.sources:
            sources.append(SourceReference(
                source_url=source['source_url'],
                page_title=source['page_title'],
                chunk_index=source['chunk_index'],
                relevance_score=source['relevance_score'],
                text_snippet=source['text_snippet']
            ))

        # Create response
        response = AnswerResponse(
            answer_text=agent_response.answer_text,
            sources=sources,
            confidence_score=agent_response.confidence_score,
            retrieval_time_ms=agent_response.retrieval_time_ms,
            generation_time_ms=agent_response.generation_time_ms,
            session_id=session.session_id
        )

        # Add to conversation history (limit history to prevent memory issues)
        conversation_turn = ConversationTurn(
            turn_id=len(session.conversation_history) + 1,
            question=request.question_text,
            answer=agent_response.answer_text,
            timestamp=datetime.now().isoformat(),
            sources_used=sources
        )

        session.conversation_history.append(conversation_turn)
        if len(session.conversation_history) > session.max_history_length:
            session.conversation_history = session.conversation_history[-session.max_history_length:]

        logger.info(f"Question processed successfully. Retrieval: {agent_response.retrieval_time_ms:.2f}ms, Generation: {agent_response.generation_time_ms:.2f}ms")
        return response

    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@app.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """
    Get information about a specific conversation session.
    """
    try:
        if session_id not in session_store:
            raise HTTPException(status_code=404, detail="Session not found")

        return session_store[session_id]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving session: {str(e)}")


@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """
    Clear a specific conversation session.
    """
    try:
        if session_id in session_store:
            del session_store[session_id]
            return {"message": f"Session {session_id} cleared successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error clearing session: {str(e)}")


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify service is running.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "RAG Agent API"
    }


if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        reload=True
    )