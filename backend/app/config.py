import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application configuration settings"""
    
    # API Configuration
    anthropic_api_key: str
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS Configuration
    allowed_origins: List[str] = ["*"]
    
    # Rate Limiting
    rate_limit_per_minute: int = 10
    
    # Logging
    log_level: str = "INFO"
    
    @field_validator("anthropic_api_key")
    @classmethod
    def validate_anthropic_api_key(cls, v):
        if not v:
            raise ValueError("ANTHROPIC_API_KEY is required")
        if not v.startswith("sk-ant-"):
            raise ValueError("Invalid Anthropic API key format")
        return v
    
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

# Global settings instance
settings = Settings()