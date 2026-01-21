"""
FastAPI Backend for Physical AI & Humanoid Robotics Textbook
Main application entry point with RAG chatbot and auth endpoints
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

app = FastAPI(
    title="Physical AI Textbook API",
    description="RAG chatbot and personalization services for Physical AI textbook",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://hackathon1-physical-ai-humanoid-book.vercel.app",
        "https://*.vercel.app",
        "*"  # Allow all for maximum compatibility
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "physical-ai-textbook-api",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Physical AI Textbook API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/test-rag")
async def test_rag():
    """Test RAG service directly"""
    try:
        from src.services.rag_service import RAGService
        rag = RAGService()
        result = rag.answer_question("What is ROS 2?", top_k=2)
        return {"status": "success", "answer": result["answer"][:200]}
    except Exception as e:
        import traceback
        return {"status": "error", "message": str(e), "trace": traceback.format_exc()}

# Import routers
from src.api import chat_rag, auth

# Register routers - Using RAG version for real content search
app.include_router(chat_rag.router, prefix="/api/chat", tags=["chat"])
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])

# Other bonus routers placeholders
# from src.api import personalization, translation
# app.include_router(personalization.router, prefix="/api/personalize", tags=["personalization"])
# app.include_router(translation.router, prefix="/api/translate", tags=["translation"])
