import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"
    assert data["service"] == "therapist-bot-api"

def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Therapist Bot API"
    assert "endpoints" in data

@patch('app.services.llm_service.LLMService.generate_response')
@patch('app.services.llm_service.LLMService.validate_api_connection')
def test_respond_endpoint_normal_message(mock_validate, mock_generate, client, sample_messages):
    """Test the respond endpoint with a normal message"""
    # Mock the LLM service methods
    mock_validate.return_value = True
    mock_generate.return_value = "That sounds challenging. Can you tell me more about what specifically makes you feel anxious at work?"
    
    response = client.post("/respond", json={"message": sample_messages["normal"]})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "timestamp" in data
    assert len(data["response"]) > 0

def test_respond_endpoint_crisis_message(client, sample_messages):
    """Test the respond endpoint with a crisis message"""
    response = client.post("/respond", json={"message": sample_messages["crisis"]})
    assert response.status_code == 200
    data = response.json()
    assert "not qualified to handle crisis" in data["response"]
    assert "988" in data["response"]  # Crisis helpline number

def test_respond_endpoint_medical_message(client, sample_messages):
    """Test the respond endpoint with a medical advice request"""
    response = client.post("/respond", json={"message": sample_messages["medical"]})
    assert response.status_code == 200
    data = response.json()
    assert "can't provide medical advice" in data["response"].lower()

def test_respond_endpoint_empty_message(client, sample_messages):
    """Test the respond endpoint with an empty message"""
    response = client.post("/respond", json={"message": sample_messages["empty"]})
    assert response.status_code == 422  # Validation error

def test_respond_endpoint_too_long_message(client, sample_messages):
    """Test the respond endpoint with a message that's too long"""
    response = client.post("/respond", json={"message": sample_messages["too_long"]})
    assert response.status_code == 200
    data = response.json()
    assert "between 1 and 1000 characters" in data["response"]

def test_respond_endpoint_spam_message(client, sample_messages):
    """Test the respond endpoint with a spam-like message"""
    response = client.post("/respond", json={"message": sample_messages["spam"]})
    assert response.status_code == 200
    data = response.json()
    assert "inappropriate patterns" in data["response"]

def test_respond_endpoint_invalid_json(client):
    """Test the respond endpoint with invalid JSON"""
    response = client.post("/respond", json={"invalid": "field"})
    assert response.status_code == 422  # Validation error

def test_cors_headers(client):
    """Test that CORS headers are properly set"""
    response = client.options("/health")
    assert response.status_code == 200