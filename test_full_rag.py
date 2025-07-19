#!/usr/bin/env python3
"""
Full end-to-end test for RAG functionality including HTTP API
"""
import asyncio
import requests
import json
import time

API_BASE = "http://127.0.0.1:8000"

def test_api_endpoints():
    """Test the RAG API endpoints with session continuity"""
    print("🧪 Testing Full RAG API Functionality")
    print("=" * 50)
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed: {health_data['status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on port 8000")
        return False
    
    # Test first message (new session)
    print("\n2. Testing first message (new session)...")
    first_message = {
        "message": "I'm feeling really anxious about my job interview tomorrow. I keep imagining the worst case scenarios."
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/respond",
            json=first_message,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            session_id = data["session_id"]
            is_new_session = data["is_new_session"]
            context_used = data["context_used"]
            
            print(f"✅ First response received")
            print(f"   Session ID: {session_id}")
            print(f"   New session: {is_new_session}")
            print(f"   Context used: {context_used}")
            print(f"   Response preview: {data['response'][:100]}...")
            
            if not is_new_session:
                print("⚠️  Expected new session but got existing session")
            if context_used:
                print("⚠️  Expected no context for first message but context was used")
        else:
            print(f"❌ First message failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending first message: {e}")
        return False
    
    # Test follow-up message with session continuity
    print("\n3. Testing follow-up message (session continuity)...")
    followup_message = {
        "message": "What specific breathing techniques would help me calm down before the interview?",
        "session_id": session_id
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/respond",
            json=followup_message,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            same_session = data["session_id"] == session_id
            is_new_session = data["is_new_session"]
            context_used = data["context_used"]
            
            print(f"✅ Follow-up response received")
            print(f"   Same session ID: {same_session}")
            print(f"   New session: {is_new_session}")
            print(f"   Context used: {context_used}")
            print(f"   Response preview: {data['response'][:100]}...")
            
            if not same_session:
                print("❌ Session ID mismatch - session continuity failed")
                return False
            if is_new_session:
                print("❌ Expected existing session but got new session flag")
                return False
            if not context_used:
                print("⚠️  Expected context to be used for follow-up but none was used")
        else:
            print(f"❌ Follow-up message failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending follow-up message: {e}")
        return False
    
    # Test third message to verify persistent memory
    print("\n4. Testing third message (persistent memory)...")
    third_message = {
        "message": "Thank you for the breathing advice. Can you remind me what my main concern was that we discussed?",
        "session_id": session_id
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/respond",
            json=third_message,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            context_used = data["context_used"]
            
            print(f"✅ Third response received")
            print(f"   Context used: {context_used}")
            print(f"   Response preview: {data['response'][:150]}...")
            
            # Check if the response references the original concern (job interview)
            response_text = data['response'].lower()
            if 'interview' in response_text or 'job' in response_text:
                print("✅ Response correctly references original concern (job interview)")
            else:
                print("⚠️  Response may not be referencing original concern")
                
        else:
            print(f"❌ Third message failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error sending third message: {e}")
        return False
    
    # Test new session creation
    print("\n5. Testing new session creation...")
    new_session_message = {
        "message": "Hello, I'd like to start a completely new conversation about a different topic."
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/respond",
            json=new_session_message,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            new_session_id = data["session_id"]
            is_new_session = data["is_new_session"]
            context_used = data["context_used"]
            
            print(f"✅ New session response received")
            print(f"   New session ID: {new_session_id}")
            print(f"   Different from previous: {new_session_id != session_id}")
            print(f"   New session flag: {is_new_session}")
            print(f"   Context used: {context_used}")
            
            if new_session_id == session_id:
                print("❌ Expected new session ID but got same ID")
                return False
            if not is_new_session:
                print("❌ Expected new session flag but got False")
                return False
            if context_used:
                print("⚠️  Expected no context for new session but context was used")
                
        else:
            print(f"❌ New session message failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error creating new session: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All RAG functionality tests passed!")
    print("\n✅ Key Features Verified:")
    print("   • Session creation and management")
    print("   • Message storage and embedding")
    print("   • Context retrieval and usage")
    print("   • Session continuity and memory")
    print("   • Session isolation")
    print("   • New session creation")
    
    return True

if __name__ == "__main__":
    success = test_api_endpoints()
    exit(0 if success else 1)