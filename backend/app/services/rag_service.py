"""
RAG (Retrieval Augmented Generation) service for context-aware therapeutic responses.
"""
from .embedding_service import EmbeddingService
from .session_service import SessionService
from .llm_service import LLMService
import structlog
from typing import List, Dict, Optional, Tuple

logger = structlog.get_logger(__name__)

class RAGService:
    """Orchestrates RAG functionality for context-aware therapeutic conversations."""
    
    def __init__(self, llm_service=None):
        self.embedding_service = EmbeddingService()
        self.session_service = SessionService(embedding_service=self.embedding_service)
        self.llm_service = llm_service  # Will be injected from main.py
    
    async def generate_rag_response(self, user_message: str, session_id: Optional[str] = None) -> Dict:
        """Generate a context-aware therapeutic response using RAG."""
        try:
            # Create new session if none provided
            if not session_id:
                session_id = self.session_service.create_session()
                is_new_session = True
                logger.info("Created new session for RAG response", session_id=session_id)
            else:
                is_new_session = False
                # Verify session exists
                session = self.session_service.get_session(session_id)
                if not session:
                    logger.warning("Session not found, creating new one", requested_session_id=session_id)
                    session_id = self.session_service.create_session()
                    is_new_session = True
            
            # Store user message first
            user_message_id = self.session_service.store_message(
                session_id=session_id,
                content=user_message,
                message_type="user"
            )
            
            if not user_message_id:
                raise Exception("Failed to store user message")
            
            # Retrieve relevant conversation context
            context_items = []
            if not is_new_session:
                context_items = self.embedding_service.retrieve_relevant_context(
                    session_id=session_id,
                    query=user_message,
                    n_results=5
                )
            
            # Build enhanced therapeutic prompt
            enhanced_prompt = self._build_therapeutic_prompt(user_message, context_items, is_new_session)
            
            # Generate response with Claude
            llm_response = await self.llm_service.generate_response(enhanced_prompt)
            
            # Store therapist response
            therapist_message_id = self.session_service.store_message(
                session_id=session_id,
                content=llm_response,
                message_type="therapist"
            )
            
            # Extract and store any therapeutic insights
            await self._extract_and_store_insights(session_id, user_message, llm_response)
            
            logger.info("Generated RAG response", 
                       session_id=session_id,
                       user_message_length=len(user_message),
                       response_length=len(llm_response),
                       context_items_used=len(context_items),
                       is_new_session=is_new_session)
            
            return {
                "response": llm_response,
                "session_id": session_id,
                "context_used": len(context_items) > 0,
                "context_items_count": len(context_items),
                "is_new_session": is_new_session,
                "user_message_id": user_message_id,
                "therapist_message_id": therapist_message_id
            }
            
        except Exception as e:
            logger.error("Failed to generate RAG response", 
                        session_id=session_id, 
                        user_message_length=len(user_message) if user_message else 0,
                        error=str(e))
            raise
    
    def _build_therapeutic_prompt(self, user_message: str, context_items: List[Dict], is_new_session: bool) -> str:
        """Build an enhanced therapeutic prompt with conversation context."""
        
        # Base therapeutic system prompt
        base_prompt = """You are Alex, a warm, empathetic CBT (Cognitive Behavioral Therapy) assistant. You provide supportive, evidence-based therapeutic guidance while maintaining professional boundaries.

Your therapeutic approach:
- Use CBT techniques: thought challenging, behavioral activation, cognitive restructuring
- Ask gentle, open-ended questions to explore thoughts and feelings
- Provide supportive reframes for negative thinking patterns
- Keep responses concise (150-300 words) but compassionate
- Remember you're an AI assistant, not a licensed therapist

CRITICAL SAFETY RULES:
- For crisis situations (suicide, self-harm, violence): "I'm not qualified to handle crisis situations. Please contact a mental health professional immediately or call a crisis helpline: 988 (US), 116 123 (UK), or your local emergency services."
- Never diagnose mental health conditions
- Never provide medical advice or medication recommendations
- Redirect medical questions to healthcare professionals"""
        
        # Add conversation context if available
        if context_items and not is_new_session:
            context_text = "\n".join([
                f"- {item['message_type'].title()}: {item['content'][:200]}{'...' if len(item['content']) > 200 else ''}"
                for item in context_items[:3]  # Use top 3 most relevant items
            ])
            
            context_prompt = f"""
PREVIOUS CONVERSATION CONTEXT:
{context_text}

This shows relevant parts of your ongoing conversation with this person. Use this context to:
- Reference previous topics when therapeutically relevant
- Build on earlier insights and progress
- Maintain therapeutic continuity and rapport
- Avoid repeating the same questions or advice
- Show that you remember and care about their journey"""
        else:
            context_prompt = "\nThis is the beginning of your conversation with this person."
        
        # Current message
        current_message_prompt = f"""
CURRENT MESSAGE: {user_message}

Provide therapeutic guidance that demonstrates continuity while offering fresh, helpful CBT support. Be warm, empathetic, and professionally boundaried."""
        
        return base_prompt + context_prompt + current_message_prompt
    
    async def _extract_and_store_insights(self, session_id: str, user_message: str, therapist_response: str):
        """Extract and store therapeutic insights from the conversation."""
        try:
            # Simple keyword-based insight extraction
            # In a production system, this could use more sophisticated NLP
            
            insights_to_store = []
            
            # Detect emotional themes
            emotional_keywords = {
                "anxiety": ["anxious", "worried", "nervous", "panic", "stress"],
                "depression": ["sad", "depressed", "hopeless", "empty", "down"],
                "anger": ["angry", "mad", "frustrated", "irritated", "furious"],
                "fear": ["scared", "afraid", "fearful", "terrified", "phobia"]
            }
            
            user_lower = user_message.lower()
            for emotion, keywords in emotional_keywords.items():
                if any(keyword in user_lower for keyword in keywords):
                    insights_to_store.append({
                        "type": "emotion",
                        "content": f"User expressed {emotion} in conversation",
                        "confidence": 0.7
                    })
            
            # Detect coping strategies mentioned
            coping_keywords = ["breathing", "meditation", "exercise", "journal", "therapy", "support"]
            if any(keyword in user_lower for keyword in coping_keywords):
                insights_to_store.append({
                    "type": "coping_strategy",
                    "content": "User mentioned or discussed coping strategies",
                    "confidence": 0.8
                })
            
            # Store insights
            for insight in insights_to_store:
                self.session_service.add_session_insight(
                    session_id=session_id,
                    insight_type=insight["type"],
                    content=insight["content"],
                    confidence_score=insight["confidence"]
                )
            
            if insights_to_store:
                logger.info("Stored therapeutic insights", 
                           session_id=session_id, 
                           insights_count=len(insights_to_store))
                           
        except Exception as e:
            logger.error("Failed to extract insights", session_id=session_id, error=str(e))
            # Don't raise - insights are supplementary
    
    def get_session_summary(self, session_id: str) -> Dict:
        """Get a comprehensive summary of a therapy session."""
        try:
            # Get session stats
            stats = self.session_service.get_session_stats(session_id)
            
            # Get recent insights
            insights = self.session_service.get_session_insights(session_id)
            
            # Get recent context
            context = self.session_service.get_session_context(session_id, limit=5)
            
            return {
                "session_stats": stats,
                "recent_insights": insights[:5],  # Last 5 insights
                "recent_messages": context[-5:] if context else [],  # Last 5 messages
                "total_context_items": len(context)
            }
            
        except Exception as e:
            logger.error("Failed to get session summary", session_id=session_id, error=str(e))
            return {}