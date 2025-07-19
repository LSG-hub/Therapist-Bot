from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog
from datetime import datetime
import os
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from .models import MessageRequest, MessageResponse
from .services.llm_service import LLMService
from .services.guardrails import validate_message_content
from .services.rag_service import RAGService
from .database.connection import init_database
from .config import settings

# Load environment variables
load_dotenv()

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(20),  # INFO level
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Initialize services
llm_service = None
rag_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global llm_service, rag_service
    logger.info("Starting Therapist Bot API")
    
    # Initialize database
    try:
        init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise
    
    # Initialize LLM service
    llm_service = LLMService(settings.anthropic_api_key)
    logger.info("LLM service initialized")
    
    # Test API connection
    is_connected = await llm_service.validate_api_connection()
    if not is_connected:
        logger.error("Failed to validate Anthropic API connection")
        raise ValueError("Cannot connect to Anthropic API")
    
    logger.info("Anthropic API connection validated")
    
    # Initialize RAG service
    try:
        rag_service = RAGService(llm_service=llm_service)
        logger.info("RAG service initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize RAG service", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Therapist Bot API")

# Create FastAPI app
app = FastAPI(
    title="Therapist Bot API",
    description="A CBT-focused therapeutic chatbot powered by Claude Sonnet 4",
    version="1.0.0",
    lifespan=lifespan
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Setup rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.utcnow()
    
    # Log request
    logger.info(
        "request_started",
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else "unknown"
    )
    
    response = await call_next(request)
    
    # Log response
    duration = (datetime.utcnow() - start_time).total_seconds()
    logger.info(
        "request_completed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        duration_seconds=duration
    )
    
    return response

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "service": "therapist-bot-api"
    }

@app.post("/respond", response_model=MessageResponse)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def respond_to_message(message_request: MessageRequest, request: Request):
    """
    Main endpoint for therapeutic conversations with RAG-enhanced context awareness.
    Processes user messages through safety guardrails and generates CBT-focused responses.
    """
    user_message = message_request.message.strip()
    session_id = message_request.session_id
    
    # Log the incoming request (without full message content for privacy)
    logger.info(
        "message_received",
        message_length=len(user_message),
        session_id=session_id,
        has_session=session_id is not None,
        client_ip=request.client.host if request.client else "unknown"
    )
    
    try:
        # Validate message content and check safety guardrails
        is_valid, validation_response = validate_message_content(user_message)
        
        if not is_valid:
            logger.warning(
                "message_validation_failed",
                message_preview=user_message[:50] + "..." if len(user_message) > 50 else user_message,
                validation_response=validation_response,
                session_id=session_id
            )
            
            # For safety responses, create a simple response without RAG
            return MessageResponse(
                response=validation_response,
                timestamp=datetime.utcnow().isoformat(),
                session_id=session_id or "safety_response",
                context_used=False,
                is_new_session=False
            )
        
        # Generate therapeutic response using RAG service
        if not rag_service:
            logger.error("RAG service not initialized")
            raise HTTPException(status_code=500, detail="Service temporarily unavailable")
        
        rag_response = await rag_service.generate_rag_response(user_message, session_id)
        
        # Log successful response (without content for privacy)
        logger.info(
            "rag_response_generated",
            response_length=len(rag_response["response"]),
            user_message_length=len(user_message),
            session_id=rag_response["session_id"],
            context_used=rag_response["context_used"],
            is_new_session=rag_response["is_new_session"]
        )
        
        return MessageResponse(
            response=rag_response["response"],
            timestamp=datetime.utcnow().isoformat(),
            session_id=rag_response["session_id"],
            context_used=rag_response["context_used"],
            is_new_session=rag_response["is_new_session"]
        )
        
    except Exception as e:
        logger.error(
            "error_processing_message",
            error_type=type(e).__name__,
            error_message=str(e),
            session_id=session_id
        )
        
        # Return graceful error response
        raise HTTPException(
            status_code=500,
            detail="I'm having trouble processing your message right now. Please try again in a moment."
        )

@app.get("/")
async def root():
    """Root endpoint with basic API information"""
    return {
        "message": "Therapist Bot API",
        "description": "A CBT-focused therapeutic chatbot",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "respond": "/respond (POST)",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )