from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, HTTPException
import os

def get_rate_limit_key(request: Request):
    """
    Generate rate limiting key based on client IP
    In production, you might want to use user ID or API key
    """
    return get_remote_address(request)

def setup_rate_limiting(app):
    """Setup rate limiting for the FastAPI app"""
    
    # Get rate limit from environment or default to 10/minute
    rate_limit = os.getenv("RATE_LIMIT_PER_MINUTE", "10")
    
    # Create limiter instance
    limiter = Limiter(key_func=get_rate_limit_key)
    app.state.limiter = limiter
    
    # Add rate limit exceeded handler
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
    
    return limiter

async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Custom handler for rate limit exceeded errors"""
    return HTTPException(
        status_code=429,
        detail={
            "error": "Rate limit exceeded. Please slow down and try again later.",
            "retry_after": exc.retry_after if hasattr(exc, 'retry_after') else 60
        }
    )