from pydantic import  BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class SourceReference(BaseModel):
    """Model for source references in agent responses"""
    url: str = Field(..., description="URL or path to the source")
    title: str = Field(..., description="Title of the source")
    content: str = Field(..., description="Relevant content snippet from the source")
    page_number: Optional[int] = None
    section: Optional[str] = None
    relevance_score: float = Field(..., ge=0, le=1, description="Relevance score of the source to the query")


class ChatRequest(BaseModel):
    """Model for chat requests from the frontend"""
    question: str = Field(..., description="The user's question about the book content")
    session_id: Optional[str] = None
    selected_text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}


class ChatResponse(BaseModel):
    """Model for chat responses from the backend"""
    answer: str = Field(..., description="The agent's response to the user's question")
    sources: List[SourceReference] = Field(default_factory=list, description="List of sources used to generate the response")
    session_id: str = Field(..., description="Session identifier for follow-up questions")
    timestamp: str = Field(..., description="ISO timestamp of the response")
    status: str = Field("success", description="Status of the response")
    confidence_score: Optional[float] = Field(None, ge=0, le=1, description="Confidence score of the response")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Performance metrics for the response")


class ErrorResponse(BaseModel):
    """Model for error responses"""
    error: str = Field(..., description="Error message")
    status: str = Field("error", description="Status of the response")
    details: Optional[Dict[str, Any]] = None