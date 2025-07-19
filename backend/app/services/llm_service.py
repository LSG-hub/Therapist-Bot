import asyncio
from anthropic import AsyncAnthropic
import structlog
from typing import Optional

logger = structlog.get_logger()

class LLMService:
    """Service for interacting with Anthropic's Claude API"""
    
    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"  # Latest Claude Sonnet model
        self.max_tokens = 1000
        self.temperature = 0.7
        
        # CBT-focused system prompt
        self.system_prompt = """You are Alex, a warm, empathetic CBT (Cognitive Behavioral Therapy) assistant. 

Your therapeutic approach:
- Use evidence-based CBT techniques like thought challenging, behavioral activation, and cognitive restructuring
- Ask gentle, open-ended questions to help users explore their thoughts and feelings
- Provide supportive reframes for negative thinking patterns and cognitive distortions
- Keep responses concise (150-300 words) but compassionate and therapeutic
- Maintain professional boundaries - you're an AI assistant, not a licensed therapist
- Use a conversational, supportive tone that feels natural and caring

CBT Techniques to use:
- Thought challenging: Help identify and examine negative thought patterns
- Cognitive restructuring: Guide users to develop more balanced perspectives
- Behavioral activation: Suggest small, manageable actions when appropriate
- Psychoeducation: Briefly explain relevant CBT concepts when helpful

CRITICAL SAFETY RULES:
- If someone mentions suicide, self-harm, violence, or crisis situations: "I'm not qualified to handle crisis situations. Please contact a mental health professional immediately or call a crisis helpline: 988 (US), 116 123 (UK), or your local emergency services."
- Never diagnose mental health conditions
- Never provide medical advice or medication recommendations
- For medical questions, redirect to healthcare professionals
- If unsure about safety, err on the side of caution

Remember: Your role is to provide supportive guidance using CBT principles while ensuring user safety. Focus on being helpful, warm, and therapeutically oriented."""

    async def generate_response(self, user_message: str, conversation_history: Optional[list] = None) -> str:
        """
        Generate a therapeutic response using Claude Sonnet 4
        
        Args:
            user_message: The user's input message
            conversation_history: Optional previous conversation context
            
        Returns:
            Therapeutic response string
        """
        try:
            # Prepare messages for the API
            messages = []
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            logger.info(
                "sending_request_to_anthropic",
                model=self.model,
                message_count=len(messages),
                user_message_length=len(user_message)
            )
            
            # Make API call to Anthropic
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=self.system_prompt,
                messages=messages
            )
            
            # Extract response text
            if response.content and len(response.content) > 0:
                therapeutic_response = response.content[0].text
                
                logger.info(
                    "received_response_from_anthropic",
                    response_length=len(therapeutic_response),
                    usage_input_tokens=response.usage.input_tokens,
                    usage_output_tokens=response.usage.output_tokens
                )
                
                return therapeutic_response
            else:
                logger.error("empty_response_from_anthropic")
                return "I'm having trouble formulating a response right now. Could you please rephrase your message?"
                
        except Exception as e:
            logger.error(
                "error_calling_anthropic_api",
                error_type=type(e).__name__,
                error_message=str(e)
            )
            
            # Return graceful fallback response
            return "I apologize, but I'm experiencing some technical difficulties right now. Please try again in a moment, or if this persists, consider speaking with a human therapist."
    
    async def validate_api_connection(self) -> bool:
        """
        Validate that the API connection is working
        
        Returns:
            True if connection is valid, False otherwise
        """
        try:
            # Send a simple test message
            test_response = await self.client.messages.create(
                model=self.model,
                max_tokens=50,
                temperature=0.1,
                system="You are a helpful assistant. Respond with exactly: 'Connection test successful'",
                messages=[{
                    "role": "user",
                    "content": "Test connection"
                }]
            )
            
            if test_response.content and len(test_response.content) > 0:
                response_text = test_response.content[0].text
                logger.info("api_connection_validated", response=response_text)
                return True
            else:
                logger.error("api_connection_validation_failed_empty_response")
                return False
                
        except Exception as e:
            logger.error(
                "api_connection_validation_failed",
                error_type=type(e).__name__,
                error_message=str(e)
            )
            return False