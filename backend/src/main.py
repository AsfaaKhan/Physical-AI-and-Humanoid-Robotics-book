from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.chat_api import app as chat_router
from src.api.v1.auth import auth_router
from src.api.v1.personalization import personalization_router
from config.settings import settings

# Create the main FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="API for the RAG chatbot integration between frontend and backend",
    version="1.0.0"
)

# Configure CORS middleware to allow Docusaurus frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # Use configured allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chat API router
app.include_router(chat_router, prefix="", tags=["chat"])

# Include the auth API router
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])

# Include the personalization API router
app.include_router(personalization_router, prefix="/api/v1/personalization", tags=["personalization"])

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "RAG Chatbot API with Authentication"}

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)