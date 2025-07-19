import re
import structlog
from typing import Tuple, List

logger = structlog.get_logger()

# Crisis-related keywords that trigger immediate safety response
CRISIS_KEYWORDS = [
    'suicide', 'kill myself', 'end it all', 'not worth living',
    'self-harm', 'cut myself', 'hurt myself', 'overdose',
    'jump off', 'hang myself', 'want to die', 'better off dead',
    'end my life', 'take my own life', 'kill me', 'want to die',
    'pills to die', 'bridge jump', 'gun to head', 'rope around neck'
]

# Medical-related keywords that require redirection to professionals
MEDICAL_KEYWORDS = [
    'medication', 'prescription', 'dosage', 'pills',
    'antidepressant', 'diagnosis', 'diagnose', 'bipolar', 'schizophrenia',
    'psychiatrist appointment', 'therapy session', 'mental health diagnosis',
    'psychiatric medication', 'medical advice', 'doctor said',
    'hospital stay', 'psychiatric ward', 'mental health treatment'
]

# Violence-related keywords
VIOLENCE_KEYWORDS = [
    'hurt someone', 'hurt others', 'hurt them', 'hurt him', 'hurt her',
    'kill someone', 'kill others', 'kill them', 'kill him', 'kill her',
    'harm others', 'harm someone', 'violence', 'assault',
    'attack', 'rage against', 'destroy everything',
    'burn it down', 'revenge on', 'make them pay'
]

def check_safety(message: str) -> Tuple[bool, str]:
    """
    Check if a message triggers safety guardrails
    
    Args:
        message: User's input message
        
    Returns:
        Tuple of (is_safe: bool, safety_response: str)
        - is_safe: True if message is safe to process, False if guardrails triggered
        - safety_response: Empty string if safe, safety message if not safe
    """
    message_lower = message.lower().strip()
    
    # Remove common punctuation and normalize whitespace
    normalized_message = re.sub(r'[^\w\s]', ' ', message_lower)
    normalized_message = ' '.join(normalized_message.split())
    
    logger.info(
        "checking_message_safety",
        message_length=len(message),
        normalized_length=len(normalized_message)
    )
    
    # Check for crisis keywords
    crisis_detected = _check_keywords(normalized_message, CRISIS_KEYWORDS)
    if crisis_detected:
        safety_response = (
            "I'm not qualified to handle crisis situations. Please contact a mental health professional "
            "immediately or call a crisis helpline: 988 (US), 116 123 (UK), or your local emergency services. "
            "If you're in immediate danger, please call emergency services right away."
        )
        
        logger.warning(
            "crisis_keywords_detected",
            message_preview=message[:100] + "..." if len(message) > 100 else message,
            detected_keywords=crisis_detected
        )
        
        return False, safety_response
    
    # Check for violence keywords
    violence_detected = _check_keywords(normalized_message, VIOLENCE_KEYWORDS)
    if violence_detected:
        safety_response = (
            "I'm not qualified to help with thoughts of violence or harm towards others. "
            "Please contact a mental health professional immediately or call a crisis helpline: "
            "988 (US), 116 123 (UK), or your local emergency services."
        )
        
        logger.warning(
            "violence_keywords_detected",
            message_preview=message[:100] + "..." if len(message) > 100 else message,
            detected_keywords=violence_detected
        )
        
        return False, safety_response
    
    # Check for medical keywords
    medical_detected = _check_keywords(normalized_message, MEDICAL_KEYWORDS)
    if medical_detected:
        safety_response = (
            "I can't provide medical advice or guidance about medications and diagnoses. "
            "Please consult with a healthcare professional, psychiatrist, or your doctor about "
            "medical concerns. I'm here to support you with coping strategies and emotional support."
        )
        
        logger.info(
            "medical_keywords_detected",
            message_preview=message[:100] + "..." if len(message) > 100 else message,
            detected_keywords=medical_detected
        )
        
        return False, safety_response
    
    # Message passed all safety checks
    logger.info("message_passed_safety_checks")
    return True, ""

def _check_keywords(message: str, keyword_list: List[str]) -> List[str]:
    """
    Check if any keywords from the list are present in the message
    
    Args:
        message: Normalized message text
        keyword_list: List of keywords to check for
        
    Returns:
        List of detected keywords (empty if none found)
    """
    detected = []
    
    for keyword in keyword_list:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, message, re.IGNORECASE):
            detected.append(keyword)
    
    return detected

def is_appropriate_length(message: str) -> bool:
    """
    Check if message length is appropriate
    
    Args:
        message: User's input message
        
    Returns:
        True if length is appropriate, False otherwise
    """
    # Remove excessive whitespace
    cleaned_message = ' '.join(message.split())
    
    # Check length constraints
    if len(cleaned_message) < 1:
        return False
    if len(cleaned_message) > 1000:
        return False
    
    return True

def contains_spam_patterns(message: str) -> bool:
    """
    Check for common spam patterns
    
    Args:
        message: User's input message
        
    Returns:
        True if spam patterns detected, False otherwise
    """
    spam_patterns = [
        r'(.)\1{10,}',  # Repeated characters (10+ times)
        r'http[s]?://\S+',  # URLs
        r'\b\d{10,}\b',  # Long number sequences (phone numbers, etc.)
        r'\b[A-Z]{15,}\b',  # Excessive caps (15+ consecutive caps)
    ]
    
    for pattern in spam_patterns:
        if re.search(pattern, message, re.IGNORECASE):
            logger.warning(
                "spam_pattern_detected",
                pattern=pattern,
                message_preview=message[:50] + "..." if len(message) > 50 else message
            )
            return True
    
    return False

def validate_message_content(message: str) -> Tuple[bool, str]:
    """
    Comprehensive message validation including safety, length, and spam checks
    
    Args:
        message: User's input message
        
    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    # Check message length
    if not is_appropriate_length(message):
        return False, "Message must be between 1 and 1000 characters."
    
    # Check safety guardrails first (higher priority than spam)
    is_safe, safety_response = check_safety(message)
    if not is_safe:
        return False, safety_response
    
    # Check for spam patterns
    if contains_spam_patterns(message):
        return False, "Message contains inappropriate patterns. Please send a normal conversational message."
    
    return True, ""