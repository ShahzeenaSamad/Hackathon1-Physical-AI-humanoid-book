"""
FastAPI Backend for Physical AI & Humanoid Robotics Textbook
Main application entry point with RAG chatbot and auth endpoints
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

# --- Logger Configuration ---
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/backend.log", level="INFO", rotation="10 MB", retention="7 days")
# ---

app = FastAPI(
    title="Physical AI Textbook API",
    description="RAG chatbot and personalization services for Physical AI textbook",
    version="1.0.0"
)

# --- Middleware ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Logs incoming HTTP requests."""
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# --- Exception Handler ---
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Catches and logs unhandled exceptions, returning a generic 500 error."""
    logger.error(f"Unhandled exception for request {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )
# ---

# CORS configuration for frontend - UPDATED FOR HUGGING FACE AND VERCEL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://shahzeenasamad-physical-ai-frontend.vercel.app",  # Deployed frontend
        "https://*.vercel.app",  # Allow any Vercel subdomain
        "https://*.hf.space",    # Allow Hugging Face Spaces
        "*",  # Allow all origins for maximum compatibility
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

# Import routers
from src.api import chat_mock

# Register routers - Using MOCK version for demo
app.include_router(chat_mock.router, prefix="/api/chat", tags=["chat"])

# Other routes
@app.get("/api/chapters")
async def get_chapters():
    return [{"id": "ch1", "title": "Introduction to Physical AI", "module": "Module 1"}]

@app.get("/api/modules")
async def get_modules():
    return [{"id": "mod1", "title": "Module 1: ROS 2 Fundamentals"}]