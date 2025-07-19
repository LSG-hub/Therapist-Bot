import pytest
from app.services.guardrails import (
    check_safety, 
    validate_message_content, 
    is_appropriate_length, 
    contains_spam_patterns
)

class TestGuardrails:
    """Test suite for the guardrails system"""
    
    def test_check_safety_normal_message(self):
        """Test that normal messages pass safety checks"""
        message = "I've been feeling anxious about my job interview tomorrow."
        is_safe, response = check_safety(message)
        assert is_safe == True
        assert response == ""
    
    def test_check_safety_crisis_keywords(self):
        """Test that crisis keywords trigger safety response"""
        crisis_messages = [
            "I want to kill myself",
            "I'm thinking about suicide",
            "I want to end it all",
            "I'm better off dead",
            "I want to hurt myself"
        ]
        
        for message in crisis_messages:
            is_safe, response = check_safety(message)
            assert is_safe == False
            assert "not qualified to handle crisis" in response
            assert "988" in response or "emergency services" in response
    
    def test_check_safety_violence_keywords(self):
        """Test that violence keywords trigger safety response"""
        violence_messages = [
            "I want to hurt someone",
            "I'm going to kill someone",
            "I want to attack my boss"
        ]
        
        for message in violence_messages:
            is_safe, response = check_safety(message)
            assert is_safe == False
            assert "not qualified" in response
            assert "violence" in response or "harm towards others" in response
    
    def test_check_safety_medical_keywords(self):
        """Test that medical keywords trigger appropriate response"""
        medical_messages = [
            "What medication should I take?",
            "Can you diagnose my depression?",
            "Should I increase my antidepressant dosage?",
            "I think I have bipolar disorder"
        ]
        
        for message in medical_messages:
            is_safe, response = check_safety(message)
            assert is_safe == False
            assert "can't provide medical advice" in response
            assert "healthcare professional" in response
    
    def test_is_appropriate_length(self):
        """Test message length validation"""
        # Empty message
        assert is_appropriate_length("") == False
        
        # Normal message
        assert is_appropriate_length("Hello, I need help.") == True
        
        # Very long message (over 1000 chars)
        long_message = "a" * 1001
        assert is_appropriate_length(long_message) == False
        
        # Exactly 1000 chars should be OK
        exact_message = "a" * 1000
        assert is_appropriate_length(exact_message) == True
    
    def test_contains_spam_patterns(self):
        """Test spam pattern detection"""
        # Normal message
        assert contains_spam_patterns("I need help with anxiety") == False
        
        # Repeated characters
        assert contains_spam_patterns("AAAAAAAAAAAAAA") == True
        
        # URLs
        assert contains_spam_patterns("Check out http://spam.com") == True
        assert contains_spam_patterns("Visit https://malicious.site") == True
        
        # Long number sequences
        assert contains_spam_patterns("Call me at 1234567890123") == True
        
        # Excessive caps (15+ consecutive caps)
        assert contains_spam_patterns("AAAAAAAAAAAAAAAAAA") == True
    
    def test_validate_message_content_comprehensive(self):
        """Test comprehensive message validation"""
        # Valid message
        is_valid, error = validate_message_content("I'm feeling stressed about work")
        assert is_valid == True
        assert error == ""
        
        # Empty message
        is_valid, error = validate_message_content("")
        assert is_valid == False
        assert "between 1 and 1000 characters" in error
        
        # Too long message
        is_valid, error = validate_message_content("a" * 1001)
        assert is_valid == False
        assert "between 1 and 1000 characters" in error
        
        # Spam message
        is_valid, error = validate_message_content("AAAAAAAAAAAAAA")
        assert is_valid == False
        assert "inappropriate patterns" in error
        
        # Crisis message
        is_valid, error = validate_message_content("I want to kill myself")
        assert is_valid == False
        assert "not qualified to handle crisis" in error
        
        # Medical message
        is_valid, error = validate_message_content("What medication should I take?")
        assert is_valid == False
        assert "can't provide medical advice" in error
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Message with punctuation and special chars
        message_with_punct = "I'm feeling really, really bad!!! What should I do???"
        is_safe, response = check_safety(message_with_punct)
        assert is_safe == True
        
        # Mixed case crisis keyword
        mixed_case = "I Want To KILL myself"
        is_safe, response = check_safety(mixed_case)
        assert is_safe == False
        
        # Partial matches should not trigger (word boundaries)
        partial_match = "I'm skilled at my job"  # contains "kill" but not as whole word
        is_safe, response = check_safety(partial_match)
        assert is_safe == True
        
        # Whitespace handling
        whitespace_message = "  I need help  "
        is_valid, error = validate_message_content(whitespace_message)
        assert is_valid == True