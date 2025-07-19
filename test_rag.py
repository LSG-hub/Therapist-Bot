#!/usr/bin/env python3
"""
Simple test script for RAG functionality
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.append('backend')

async def test_rag():
    """Test RAG service initialization and basic functionality"""
    try:
        print("Testing RAG service initialization...")
        
        # Import services
        from backend.app.services.rag_service import RAGService
        from backend.app.services.llm_service import LLMService
        from backend.app.database.connection import init_database
        from backend.app.config import settings
        
        # Initialize database
        print("Initializing database...")
        init_database()
        print("✅ Database initialized")
        
        # Initialize LLM service
        print("Initializing LLM service...")
        llm_service = LLMService(settings.anthropic_api_key)
        print("✅ LLM service initialized")
        
        # Test API connection
        print("Testing API connection...")
        is_connected = await llm_service.validate_api_connection()
        if not is_connected:
            raise ValueError("Cannot connect to Anthropic API")
        print("✅ API connection validated")
        
        # Initialize RAG service
        print("Initializing RAG service...")
        rag_service = RAGService(llm_service=llm_service)
        print("✅ RAG service initialized")
        
        # Test RAG response
        print("Testing RAG response generation...")
        test_message = "I feel anxious about my job interview tomorrow"
        
        response = await rag_service.generate_rag_response(test_message)
        
        print("✅ RAG response generated successfully!")
        print(f"Session ID: {response['session_id']}")
        print(f"Is new session: {response['is_new_session']}")
        print(f"Context used: {response['context_used']}")
        print(f"Response length: {len(response['response'])} characters")
        print(f"Response preview: {response['response'][:100]}...")
        
        # Test with session continuity
        print("\nTesting session continuity...")
        follow_up_message = "What techniques can I use to manage this anxiety?"
        
        response2 = await rag_service.generate_rag_response(
            follow_up_message, 
            session_id=response['session_id']
        )
        
        print("✅ Follow-up response generated successfully!")
        print(f"Session ID: {response2['session_id']}")
        print(f"Is new session: {response2['is_new_session']}")
        print(f"Context used: {response2['context_used']}")
        print(f"Response length: {len(response2['response'])} characters")
        print(f"Response preview: {response2['response'][:100]}...")
        
        print("\n🎉 All RAG tests passed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_rag())
    sys.exit(0 if success else 1)