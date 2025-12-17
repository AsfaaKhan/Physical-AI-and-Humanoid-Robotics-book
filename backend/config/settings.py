import os
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Configuration settings for the RAG system (ingestion and chatbot)."""

    def __init__(self):
        # Load environment variables with defaults
        self.COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
        self.QDRANT_URL = os.getenv("QDRANT_URL", "")
        self.QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
        self.BOOK_BASE_URL = os.getenv("BOOK_BASE_URL", "https://physical-ai-and-humanoid-robotics-book-p71goqgvj.vercel.app/")
        self.QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "rag_embedding_physical_ai_book")

        # Additional settings for chatbot API
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
        self.GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
        self.PORT = int(os.getenv("PORT", 5000))
        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

        # Authentication settings
        self.DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/rag_system")
        self.JWT_SECRET = os.getenv("JWT_SECRET", "")
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
        self.REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
        self.BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "")
        self.BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "")

    def validate(self) -> bool:
        """Validate that all required environment variables are set."""
        required_vars = [
            self.COHERE_API_KEY,
            self.QDRANT_URL,
            self.QDRANT_API_KEY
        ]

        return all(var for var in required_vars)


# Global settings instance
settings = Settings()