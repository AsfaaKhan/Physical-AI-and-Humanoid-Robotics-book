from google.generativeai import GenerativeModel, configure, embedding
from typing import List, Dict, Any, Optional
from utils.config import settings
from rag.retriever import Retriever
import logging

logger = logging.getLogger(__name__)

# Configure the Google Generative AI library
configure(api_key=settings.GEMINI_API_KEY)


class GeminiAgent:
    def __init__(self):
        # Initialize the Gemini model
        self.model = GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            system_instruction="""
            You are an expert assistant for the Physical AI & Humanoid Robotics book.
            Your purpose is to answer questions based only on the provided context from the book.

            Rules:
            1. ONLY answer from the provided context/chunks
            2. If the answer is not in the context, respond with: "This information is not found in the book."
            3. Always cite the specific chapter/section when providing information
            4. Maintain a technical but approachable tone suitable for robotics & AI education
            5. Do not hallucinate or invent content
            6. Refuse to provide information about harmful or unsafe robotics applications
            7. Be helpful but stick strictly to book content
            """
        )

        self.retriever = Retriever()

    def answer_from_context(self, question: str, context: str, selected_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Answer a question using the provided context with Gemini
        """
        try:
            # Prepare the prompt with book-specific instructions
            if selected_text:
                prompt = f"""
                You are an expert assistant for the Physical AI & Humanoid Robotics book.
                Answer the user's question based ONLY on the following selected text:
                {selected_text}

                If the answer is not in the selected text, respond with: "This information is not found in the selected text."

                Question: {question}
                """
            else:
                prompt = f"""
                You are an expert assistant for the Physical AI & Humanoid Robotics book.
                Answer the user's question based ONLY on the provided context from the book.
                If the answer is not in the context, respond with: "This information is not found in the book."
                Always cite the specific chapter/section when providing information.
                Maintain a technical but approachable tone suitable for robotics & AI education.

                Book Context:
                {context}

                Question: {question}
                """

            # Generate response using Gemini
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.3,  # Lower temperature for more consistent, factual responses
                    "max_output_tokens": 1000
                }
            )

            answer = response.text

            # Calculate a basic confidence estimate based on response characteristics
            confidence_estimate = self._calculate_confidence(answer, context if not selected_text else selected_text)

            return {
                "answer": answer,
                "confidence_estimate": confidence_estimate
            }
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise

    def _calculate_confidence(self, answer: str, context: str) -> float:
        """
        Calculate a basic confidence estimate based on response characteristics
        """
        # Simple heuristic: if the answer contains phrases indicating lack of information, lower confidence
        low_confidence_phrases = [
            "not found in the book",
            "not found in the selected text",
            "no information",
            "not mentioned",
            "not provided"
        ]

        answer_lower = answer.lower()
        for phrase in low_confidence_phrases:
            if phrase in answer_lower:
                return 0.1  # Very low confidence

        # If we have substantial context and a detailed answer, higher confidence
        if len(context) > 100 and len(answer) > 50:
            return 0.8
        elif len(context) > 50:
            return 0.6
        else:
            return 0.4

    def answer_question(self, question: str, use_selected_text: bool = False, selected_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Main method to answer a question using RAG
        """
        try:
            if use_selected_text and selected_text:
                # Use only the selected text for answering
                context = selected_text
                citations = [{"content": selected_text[:200] + "..." if len(selected_text) > 200 else selected_text,
                             "source": "selected_text",
                             "score": 1.0,
                             "metadata": {"source": "selected_text"}}]

                result = self.answer_from_context(question, context, selected_text=selected_text)
            else:
                # Use full RAG approach
                if self.retriever:
                    formatted_context, full_docs = self.retriever.retrieve_and_format(question, k=5)
                    citations = self.retriever.get_citations(full_docs)
                    result = self.answer_from_context(question, formatted_context)
                else:
                    # Fallback if retriever is not available
                    result = self.answer_from_context(question, "No context available.")

            return {
                "answer": result["answer"],
                "citations": citations,
                "context_used": selected_text if use_selected_text and selected_text else (formatted_context if 'formatted_context' in locals() else "No context"),
                "confidence_estimate": result["confidence_estimate"]
            }
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            raise

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Gemini
        """
        try:
            embeddings = []
            for text in texts:
                # Generate embedding for the text
                embedding_result = embedding(text)
                embeddings.append(embedding_result)

            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise