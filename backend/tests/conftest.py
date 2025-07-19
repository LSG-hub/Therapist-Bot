import pytest
from fastapi.testclient import TestClient
import os
from unittest.mock import patch

# Mock environment variables for testing
test_env = {
    "ANTHROPIC_API_KEY": "sk-ant-test-key-123456789",
    "DEBUG": "True",
    "HOST": "127.0.0.1",
    "PORT": "8000",
    "RATE_LIMIT_PER_MINUTE": "100",  # Higher limit for testing
    "LOG_LEVEL": "INFO"
}

@pytest.fixture(scope="session")
def mock_env():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, test_env):
        yield

@pytest.fixture
def client(mock_env):
    """Create test client with mocked environment"""
    from app.main import app
    return TestClient(app)

@pytest.fixture
def sample_messages():
    """Sample messages for testing"""
    return {
        "normal": "I've been feeling anxious about work lately.",
        "crisis": "I want to kill myself",
        "medical": "What medication should I take for depression?",
        "empty": "",
        "too_long": "a" * 1001,
        "spam": "AAAAAAAAAAAAAAAAAAAAAA"
    }