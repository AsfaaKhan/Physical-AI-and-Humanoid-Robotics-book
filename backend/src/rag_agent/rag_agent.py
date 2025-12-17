"""
RAG Agent Implementation

This module implements the core RAG agent that combines retrieval capabilities
with Gemini API for question answering.
"""
import logging
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

import google.generativeai as genai

from src.retrieval.query_processor import process_query, RetrievalResult
from src.retrieval.result_validator import calculate_precision_score
from config.settings import settings
from src.utils import setup_logging

logger = setup_logging()


@dataclass
class AgentResponse:
    """
    Represents the response from the RAG agent.
    """
    answer_text: str
    sources: List[Dict[str, Any]]
    confidence_score: float
    retrieval_time_ms: float
    generation_time_ms: float
    total_time_ms: float


class RAGAgent:
    """
    RAG (Retrieval-Augmented Generation) Agent that combines vector database
    retrieval with Gemini API for question answering.
    """

    def __init__(self):
        """
        Initialize the RAG agent with required configurations.
        """
        # Configure Gemini API
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in settings")

        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Initialize the generative model
        self.model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL_NAME,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 2048,
            }
        )

        logger.info("RAG Agent initialized successfully")

    def ask(self,
            question: str,
            top_k: int = 5,
            filters: Optional[Dict[str, Any]] = None,
            conversation_history: Optional[List[Dict[str, str]]] = None) -> AgentResponse:
        """
        Process a question using RAG methodology.

        Args:
            question: The question to answer
            top_k: Number of chunks to retrieve from vector database
            filters: Optional metadata filters for targeted retrieval
            conversation_history: Optional conversation history for context

        Returns:
            AgentResponse containing the answer and metadata
        """
        logger.info(f"Processing question with RAG agent: {question[:50]}...")

        # Measure retrieval time
        retrieval_start = time.time()
        try:
            # Retrieve relevant content from vector database
            retrieval_result = process_query(
                query_text=question,
                top_k=top_k,
                filters=filters
            )
            retrieval_duration = (time.time() - retrieval_start) * 1000
        except Exception as e:
            logger.error(f"Error during retrieval: {str(e)}")
            raise

        # Prepare context for the LLM
        context_text = self._format_context(retrieval_result)

        # Prepare the prompt for the LLM
        prompt = self._construct_prompt(
            question=question,
            context=context_text,
            conversation_history=conversation_history
        )

        # Measure generation time
        generation_start = time.time()
        try:
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            generation_duration = (time.time() - generation_start) * 1000

            if response.text:
                answer_text = response.text
            else:
                logger.warning("Gemini returned empty response")
                answer_text = "I couldn't generate a response based on the available information."
        except Exception as e:
            logger.error(f"Error during generation: {str(e)}")
            answer_text = "Sorry, I encountered an error while processing your question."

        # Calculate confidence score based on retrieval quality
        confidence_score = self._calculate_confidence_score(retrieval_result)

        # Format sources
        sources = []
        for chunk in retrieval_result.retrieved_chunks:
            sources.append({
                'source_url': chunk.source_url,
                'page_title': chunk.page_title,
                'chunk_index': chunk.chunk_index,
                'relevance_score': chunk.relevance_score,
                'text_snippet': chunk.text_content[:200] + "..." if len(chunk.text_content) > 200 else chunk.text_content
            })

        total_duration = retrieval_duration + generation_duration

        # Create and return response
        agent_response = AgentResponse(
            answer_text=answer_text,
            sources=sources,
            confidence_score=confidence_score,
            retrieval_time_ms=retrieval_duration,
            generation_time_ms=generation_duration,
            total_time_ms=total_duration
        )

        logger.info(f"Question processed. Retrieval: {retrieval_duration:.2f}ms, Generation: {generation_duration:.2f}ms, Total: {total_duration:.2f}ms")
        return agent_response

    def _format_context(self, retrieval_result: RetrievalResult) -> str:
        """
        Format the retrieved content into a context string for the LLM.

        Args:
            retrieval_result: The result from the retrieval process

        Returns:
            Formatted context string
        """
        if not retrieval_result.retrieved_chunks:
            return "No relevant information was found in the knowledge base."

        context_parts = ["Relevant information from the knowledge base:"]

        for i, chunk in enumerate(retrieval_result.retrieved_chunks, 1):
            context_parts.append(f"\n{i}. Source: {chunk.source_url}")
            context_parts.append(f"   Title: {chunk.page_title}")
            context_parts.append(f"   Content: {chunk.text_content}")
            context_parts.append(f"   Relevance Score: {chunk.relevance_score:.3f}")

        return "\n".join(context_parts)

    def _construct_prompt(self,
                         question: str,
                         context: str,
                         conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Construct the prompt for the LLM with context and conversation history.

        Args:
            question: The user's question
            context: The retrieved context
            conversation_history: Optional conversation history

        Returns:
            Formatted prompt string
        """
        prompt_parts = [
            "You are an AI assistant that answers questions based ONLY on the provided context.",
            "IMPORTANT: Your responses must be grounded in the provided context and should not include information not present in the context.",
            "Do NOT make up information, facts, or sources that are not in the provided context.",
            "Always provide source attribution when referencing specific information.",
            "If the context doesn't contain relevant information to answer the question, clearly state that you cannot answer based on the provided information.",
            "\nCONTEXT:",
            context,
            "\nINSTRUCTIONS:",
            "1. Answer the question based ONLY on the provided context",
            "2. If the context doesn't contain relevant information, say so clearly",
            "3. Provide source attribution for information referenced in your answer",
            "4. Keep your answer concise and focused",
            "5. Do NOT provide information that is not explicitly stated in the context",
            "6. Quote or paraphrase information directly from the context when possible",
            "\nQUESTION:",
            question
        ]

        # Add conversation history if provided
        if conversation_history:
            prompt_parts.insert(5, "\nPREVIOUS CONVERSATION:")
            for turn in conversation_history[-3:]:  # Use last 3 turns for context
                prompt_parts.insert(6, f"Q: {turn['question']}")
                prompt_parts.insert(7, f"A: {turn['answer']}")
            prompt_parts.insert(8, "")

        return "\n".join(prompt_parts)

    def _calculate_confidence_score(self, retrieval_result: RetrievalResult) -> float:
        """
        Calculate a confidence score based on retrieval quality metrics.

        Args:
            retrieval_result: The result from the retrieval process

        Returns:
            Confidence score between 0.0 and 1.0
        """
        if not retrieval_result.retrieved_chunks:
            return 0.0

        # Calculate precision score (this uses relevance scores as proxy)
        precision_score = calculate_precision_score(retrieval_result)

        # Calculate average relevance score
        avg_relevance = sum([chunk.relevance_score for chunk in retrieval_result.retrieved_chunks]) / len(retrieval_result.retrieved_chunks)

        # Combine metrics for overall confidence
        # Weight precision score higher as it represents quality of retrieved content
        confidence = (precision_score * 0.7) + (avg_relevance * 0.3)

        return min(1.0, max(0.0, confidence))  # Ensure score is between 0 and 1


# Global instance of the RAG agent
rag_agent = None


def get_rag_agent():
    """
    Get or create the RAG agent instance.
    """
    global rag_agent
    if rag_agent is None:
        try:
            rag_agent = RAGAgent()
        except Exception as e:
            logger.error(f"Failed to initialize RAG agent: {str(e)}")
            raise
    return rag_agent