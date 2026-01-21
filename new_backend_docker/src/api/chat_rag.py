"""
RAG Chat API - Real RAG-based chatbot
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.rag_service import RAGService
from rag.llm_generator import LLMGenerator

router = APIRouter()

# Initialize RAG service (will be initialized on startup)
rag_service = None
llm_generator = None

class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    top_k: int = 3

class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: List[Dict]
    context_used: bool
    model_used: str

def initialize_rag():
    """Initialize RAG service on startup"""
    global rag_service, llm_generator

    print("Initializing RAG chat service...")

    try:
        rag_service = RAGService()
        success = rag_service.initialize()

        llm_generator = LLMGenerator()

        if success:
            print("✅ RAG service initialized successfully!")
        else:
            print("⚠️ RAG service running in fallback mode")

    except Exception as e:
        print(f"❌ Error initializing RAG: {e}")
        rag_service = None
        llm_generator = None

# Initialize on module load
initialize_rag()

@router.post("/query", response_model=ChatResponse)
async def chat_query_rag(request: ChatRequest):
    """RAG-based chatbot with real content from the book"""

    try:
        # Check if RAG is available
        if rag_service and rag_service.is_initialized:
            # RAG mode - real content search
            print(f"[RAG] Processing: {request.question}")

            # Search for relevant content
            results = rag_service.search(request.question, top_k=request.top_k)

            # Get context
            context = rag_service.get_context_for_query(request.question, top_k=request.top_k)

            # Generate answer using LLM
            if llm_generator:
                answer = llm_generator.generate_answer(request.question, context)
            else:
                answer = f"Based on the textbook, here's relevant information: {context[:500]}..."

            # Format sources
            sources = rag_service.format_sources(results)

            return ChatResponse(
                session_id=request.session_id or str(uuid.uuid4()),
                answer=answer,
                sources=sources,
                context_used=True,
                model_used="RAG-Phi3-4k"
            )

        else:
            # Fallback mode - simple responses
            print(f"[Fallback] Processing: {request.question}")

            # Simple fallback answer
            answer = f"I understand you're asking about: {request.question}\n\nThe RAG system is still initializing. Please try again in a moment. The system is loading the textbook content to provide better answers."

            return ChatResponse(
                session_id=request.session_id or str(uuid.uuid4()),
                answer=answer,
                sources=[],
                context_used=False,
                model_used="fallback-init"
            )

    except Exception as e:
        print(f"Error in chat query: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your question: {str(e)}"
        )

@router.get("/status")
async def get_rag_status():
    """Get RAG service status"""
    return {
        "initialized": rag_service is not None and rag_service.is_initialized,
        "mode": "RAG" if (rag_service and rag_service.is_initialized) else "fallback",
        "chunks_indexed": len(rag_service.vector_store.chunks) if (rag_service and rag_service.is_initialized) else 0
    }
