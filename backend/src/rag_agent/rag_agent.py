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
            conversation_history: Optional[List[Dict[str, str]]] = None,
            selected_text: Optional[str] = None) -> AgentResponse:
        """
        Process a question using RAG methodology.

        Args:
            question: The question to answer
            top_k: Number of chunks to retrieve from vector database
            filters: Optional metadata filters for targeted retrieval
            conversation_history: Optional conversation history for context
            selected_text: Optional text that was selected by the user for higher priority context

        Returns:
            AgentResponse containing the answer and metadata
        """
        logger.info(f"Processing question with RAG agent: {question[:50]}...")

        # Measure retrieval time
        retrieval_start = time.time()

        # Implement response priority logic:
        # 1. If user selected text → Explain selected text only
        # 2. Else if user asked a question → Use embeddings search
        # 3. Else → Normal chatbot response (this is handled by the embedding search as fallback)

        # Mode 1: Selected text explanation
        if selected_text:
            logger.info("Processing in 'selected text explanation' mode")
            is_explain_query = True

            # For selected text explanation, we'll use the selected text as primary context
            # but still search for related content to enhance the explanation
            retrieval_result = process_query(
                query_text=question,
                top_k=top_k,
                filters=filters
            )
            retrieval_duration = (time.time() - retrieval_start) * 1000

            # Prepare context for the LLM, prioritizing the selected text
            context_text = self._format_context_for_explanation(retrieval_result, selected_text)

        # Mode 2: Question answering using embeddings search
        else:
            logger.info("Processing in 'embedding-based question answering' mode")
            is_explain_query = False

            try:
                retrieval_result = process_query(
                    query_text=question,
                    top_k=top_k,
                    filters=filters
                )
                retrieval_duration = (time.time() - retrieval_start) * 1000
            except Exception as e:
                logger.error(f"Error during retrieval: {str(e)}")
                raise

            # Check if we have relevant results and if they actually answer the question
            if not retrieval_result.retrieved_chunks:
                # No relevant content found in embeddings
                context_text = "No relevant information was found in the book content."
            else:
                # Check if the retrieved content as a whole addresses the specific question
                question_lower = question.lower()
                content_addresses_question = False

                # Check each chunk to see if any of them address the specific question
                for chunk in retrieval_result.retrieved_chunks:
                    chunk_content = chunk.text_content.lower()
                    if self._content_addresses_question(question_lower, chunk_content):
                        content_addresses_question = True
                        break

                if not content_addresses_question:
                    # Even though chunks were retrieved, none address the specific question
                    context_text = "No relevant information was found in the book content."
                else:
                    # Prepare context for the LLM
                    context_text = self._format_context(retrieval_result)

        # Prepare the prompt for the LLM
        prompt = self._construct_prompt(
            question=question,
            context=context_text,
            conversation_history=conversation_history,
            selected_text=selected_text,
            is_explain_query=is_explain_query
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

    def _format_context_for_explanation(self, retrieval_result: RetrievalResult, selected_text: str) -> str:
        """
        Format context specifically for explaining selected text.

        Args:
            retrieval_result: The result from the retrieval process
            selected_text: The text that was selected by the user

        Returns:
            Formatted context string with selected text prioritized
        """
        context_parts = [
            f"USER SELECTED TEXT (HIGHEST PRIORITY):",
            f"Content: {selected_text}",
            f"",
            f"Additional context from the knowledge base:"
        ]

        if retrieval_result.retrieved_chunks:
            for i, chunk in enumerate(retrieval_result.retrieved_chunks, 1):
                context_parts.append(f"\n{i}. Source: {chunk.source_url}")
                context_parts.append(f"   Title: {chunk.page_title}")
                context_parts.append(f"   Content: {chunk.text_content}")
                context_parts.append(f"   Relevance Score: {chunk.relevance_score:.3f}")
        else:
            context_parts.append("\nNo additional context was found in the knowledge base.")

        return "\n".join(context_parts)

    def _construct_prompt(self,
                         question: str,
                         context: str,
                         conversation_history: Optional[List[Dict[str, str]]] = None,
                         selected_text: Optional[str] = None,
                         is_explain_query: bool = False) -> str:
        """
        Construct the prompt for the LLM with context and conversation history.

        Args:
            question: The user's question
            context: The retrieved context
            conversation_history: Optional conversation history
            selected_text: Optional text that was selected by the user
            is_explain_query: Whether this is an explain-type query

        Returns:
            Formatted prompt string
        """
        # Check if no relevant content was found in the embeddings
        no_relevant_content = "No relevant information was found in the book content." in context

        if is_explain_query and selected_text:
            # Special prompt for explaining selected text
            prompt_parts = [
                "You are an AI assistant that explains text content in simple language.",
                "IMPORTANT: Your explanation should be based on the provided context and the selected text.",
                "Focus on explaining the selected text in simple, clear language with optional examples.",
                "Do NOT include unrelated information that is not relevant to explaining the selected text.",
                "Provide a clear explanation with simple language and examples if helpful.",
                "\nUSER SELECTED TEXT TO EXPLAIN:",
                selected_text,
                "\nADDITIONAL CONTEXT FROM KNOWLEDGE BASE:",
                context,
                "\nINSTRUCTIONS:",
                "1. Explain ONLY the selected text in simple language",
                "2. Use the additional context to enhance the explanation if relevant",
                "3. Keep your explanation clear, concise, and reader-friendly",
                "4. Do NOT add unrelated content or information not relevant to the selected text",
                "5. Include an example if it would help clarify the explanation",
                "6. Focus on clarity and simplicity",
                "\nQUESTION/REQUEST:",
                question
            ]
        elif no_relevant_content:
            # Special case: no relevant content found in embeddings
            prompt_parts = [
                "You are an AI assistant that can only answer questions based on the provided book content.",
                "IMPORTANT: You must NOT make up or hallucinate any information.",
                "If the book content does not contain information to answer the question, respond with:",
                '"This topic is not covered in the book yet."',
                "\nCONTEXT:",
                context,  # This will be "No relevant information was found in the book content."
                "\nINSTRUCTIONS:",
                "1. Do NOT attempt to answer the question based on your general knowledge",
                "2. Do NOT make up information that is not in the provided context",
                "3. Respond with exactly: 'This topic is not covered in the book yet.'",
                "4. Do NOT provide any other information or explanation",
                "\nQUESTION:",
                question
            ]
        else:
            # Standard prompt for regular questions
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
                "7. Cite chapter/section name if available in the context",
                "\nQUESTION:",
                question
            ]

        # Add conversation history if provided
        if conversation_history:
            if is_explain_query:
                prompt_parts.insert(6, "\nPREVIOUS CONVERSATION:")
                for turn in conversation_history[-3:]:  # Use last 3 turns for context
                    prompt_parts.insert(7, f"Q: {turn['question']}")
                    prompt_parts.insert(8, f"A: {turn['answer']}")
                    prompt_parts.insert(9, "")
            else:
                prompt_parts.insert(5, "\nPREVIOUS CONVERSATION:")
                for turn in conversation_history[-3:]:  # Use last 3 turns for context
                    prompt_parts.insert(6, f"Q: {turn['question']}")
                    prompt_parts.insert(7, f"A: {turn['answer']}")
                    prompt_parts.insert(8, "")

        return "\n".join(prompt_parts)

    def _content_addresses_question(self, question_lower: str, content_lower: str) -> bool:
        """
        Determine if the content addresses the specific question.
        This method checks if the retrieved content contains sufficient information
        to answer the specific question asked.

        Args:
            question_lower: The question in lowercase
            content_lower: The content chunk in lowercase

        Returns:
            True if content addresses the question, False otherwise
        """
        import re

        # For definition-type questions (what is/are, define, explain),
        # check if the content provides a clear definition/explanation of the main subject
        definition_indicators = ['what is', 'what are', 'define', 'explain', 'meaning of', 'definition of']

        # Check if this is a definition request
        is_definition_request = any(indicator in question_lower for indicator in definition_indicators)

        if is_definition_request:
            # Extract the main subject being defined (e.g., "ROS2 node" from "What is a ROS2 node?")
            # Look for patterns like "what is [the] [a/an] <subject>"
            pattern = r'(?:what is|what are|define|explain)\s+(?:the\s+)?(?:a\s+|an\s+)?(.+?)(?:\?|$)'
            match = re.search(pattern, question_lower)

            if match:
                subject = match.group(1).strip()
                # Check if the subject appears in the content with definition-like phrases
                # Look for definition patterns in the content
                definition_patterns = [
                    f'{subject}.*is',  # "ROS2 node is..."
                    f'{subject}.*are', # "ROS2 nodes are..."
                    f'{subject}.*refers to', # "ROS2 node refers to..."
                    f'{subject}.*means', # "ROS2 node means..."
                    f'defin', # Contains "defin" (definition, define, etc.)
                ]

                content_has_definition = any(re.search(pattern, content_lower) for pattern in definition_patterns)

                return content_has_definition

        # For other types of questions, use a simpler keyword match approach
        # Extract key terms from the question (excluding common words)
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'what', 'how', 'why', 'where', 'when', 'who', 'which', 'that', 'this', 'these', 'those'}

        # Extract meaningful words from question
        question_words = re.findall(r'\b\w+\b', question_lower)
        meaningful_words = [word for word in question_words if word not in common_words and len(word) > 2]

        if not meaningful_words:
            return True  # If no meaningful words, assume it's addressed

        # Check if key terms from the question appear in the content
        content_addressed = any(term in content_lower for term in meaningful_words if len(term) > 2)

        return content_addressed

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