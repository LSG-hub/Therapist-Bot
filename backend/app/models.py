from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MessageRequest(BaseModel):
    """Request model for incoming user messages"""
    message: str = Field(
        ..., 
        min_length=1, 
        max_length=1000,
        description="User's message to the therapist bot",
        example="I've been feeling really anxious about my upcoming presentation at work."
    )

class MessageResponse(BaseModel):
    """Response model for therapeutic responses"""
    response: str = Field(
        ...,
        description="Therapeutic response from the CBT assistant",
        example="It sounds like you're experiencing anticipatory anxiety about your presentation. That's quite common and understandable. Let's explore what specific thoughts are contributing to this anxiety. What's the worst thing you imagine could happen during your presentation?"
    )
    timestamp: str = Field(
        ...,
        description="ISO timestamp of when the response was generated",
        example="2025-01-19T10:30:00.000Z"
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Optional conversation identifier for session tracking",
        example="conv_abc123"
    )

class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str = Field(
        ...,
        description="Service health status",
        example="healthy"
    )
    timestamp: str = Field(
        ...,
        description="ISO timestamp of health check",
        example="2025-01-19T10:30:00.000Z"
    )
    version: str = Field(
        ...,
        description="API version",
        example="1.0.0"
    )
    service: str = Field(
        ...,
        description="Service name",
        example="therapist-bot-api"
    )

class ErrorResponse(BaseModel):
    """Response model for error responses"""
    error: str = Field(
        ...,
        description="Error message",
        example="I'm having trouble processing your message right now. Please try again in a moment."
    )
    timestamp: str = Field(
        ...,
        description="ISO timestamp of when the error occurred",
        example="2025-01-19T10:30:00.000Z"
    )
    request_id: Optional[str] = Field(
        None,
        description="Optional request identifier for debugging",
        example="req_xyz789"
    )