from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class AskRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None
    use_selected_text_only: bool = False
    history: Optional[List[Dict[str, str]]] = []


class AskResponse(BaseModel):
    answer: str
    citations: List[Dict[str, Any]]
    context_used: str
    confidence_estimate: float


class EmbedRequest(BaseModel):
    sources: List[str]
    source_types: Optional[List[str]] = None


class EmbedResponse(BaseModel):
    success: bool
    message: str
    processed_count: int


class HealthResponse(BaseModel):
    status: str
    timestamp: str


class ChatHistoryRequest(BaseModel):
    session_id: str
    user_input: str
    agent_response: str
    citations: List[Dict[str, Any]]


class ChatHistoryResponse(BaseModel):
    success: bool
    message: str