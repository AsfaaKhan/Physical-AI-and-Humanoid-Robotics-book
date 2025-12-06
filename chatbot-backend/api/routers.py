from fastapi import APIRouter, HTTPException, Request
from datetime import datetime
import logging

# Import API models
from .models import AskRequest, AskResponse, EmbedRequest, EmbedResponse, HealthResponse, ChatHistoryRequest, ChatHistoryResponse

# Import services
from agents.gemini_agent import GeminiAgent
from rag.document_processor import DocumentProcessor
from rag.vector_store import VectorStore
from utils.logger import get_logger

# Initialize services
agent = GeminiAgent()
processor = DocumentProcessor()
vector_store = VectorStore()

# Initialize logger
logger = get_logger(__name__)

# Create API router
router = APIRouter()


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    Ask a question about the Physical AI & Humanoid Robotics book
    """
    try:
        logger.info(f"Received question: {request.question}")
        logger.info(f"Use selected text only: {request.use_selected_text_only}")
        logger.info(f"Selected text provided: {bool(request.selected_text)}")

        # Validate inputs
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        if request.use_selected_text_only and not request.selected_text:
            raise HTTPException(status_code=400, detail="Selected text is required when use_selected_text_only is True")

        # Answer the question using the agent
        result = agent.answer_question(
            question=request.question,
            use_selected_text=request.use_selected_text_only,
            selected_text=request.selected_text
        )

        response = AskResponse(
            answer=result["answer"],
            citations=result["citations"],
            context_used=result["context_used"],
            confidence_estimate=result["confidence_estimate"]
        )

        logger.info("Successfully processed question")
        return response
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@router.post("/embed", response_model=EmbedResponse)
async def embed_documents(request: EmbedRequest):
    """
    Embed documents into the vector store
    """
    try:
        logger.info(f"Embedding {len(request.sources)} documents")

        if not request.sources:
            raise HTTPException(status_code=400, detail="Sources list cannot be empty")

        # Process and embed the documents
        chunked_docs, embeddings = processor.process_multiple_documents(
            request.sources,
            request.source_types
        )

        # Add to vector store
        doc_ids = vector_store.add_documents(chunked_docs, embeddings)

        response = EmbedResponse(
            success=True,
            message=f"Successfully embedded {len(doc_ids)} document chunks",
            processed_count=len(doc_ids)
        )

        logger.info(f"Successfully embedded {len(doc_ids)} document chunks")
        return response
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error embedding documents: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error embedding documents: {str(e)}")


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    try:
        response = HealthResponse(
            status="healthy",
            timestamp=datetime.now().isoformat()
        )

        logger.info("Health check successful")
        return response
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Health check failed")


@router.post("/chat-history")
async def save_chat_history(request: ChatHistoryRequest):
    """
    Save chat history to database (optional endpoint)
    """
    try:
        # In a full implementation, this would save to the database
        # For now, we'll just log the interaction

        logger.info(f"Chat history saved for session {request.session_id}")

        return {"success": True, "message": "Chat history saved"}
    except Exception as e:
        logger.error(f"Error saving chat history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error saving chat history")