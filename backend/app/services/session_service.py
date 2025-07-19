"""
Session management service for handling chat sessions and conversation context.
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..database.models import ChatSession, Message, SessionInsight
from ..database.connection import get_database
import structlog
from typing import List, Optional, Dict
import uuid
from datetime import datetime

logger = structlog.get_logger(__name__)

class SessionService:
    """Manages chat sessions and conversation history."""
    
    def __init__(self, embedding_service=None):
        self.embedding_service = embedding_service
    
    def create_session(self, metadata: Optional[Dict] = None) -> str:
        """Create a new chat session and return the session ID."""
        try:
            session_id = str(uuid.uuid4())
            
            # Create database session
            db = next(get_database())
            try:
                new_session = ChatSession(
                    session_id=session_id,
                    session_metadata=metadata or {}
                )
                db.add(new_session)
                db.commit()
                
                # Create corresponding vector collection
                if self.embedding_service:
                    self.embedding_service.create_session_collection(session_id)
                
                logger.info("Created new chat session", session_id=session_id)
                return session_id
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error("Failed to create session", error=str(e))
            raise
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get session information by session ID."""
        try:
            db = next(get_database())
            try:
                session = db.query(ChatSession).filter(
                    ChatSession.session_id == session_id
                ).first()
                return session
            finally:
                db.close()
        except Exception as e:
            logger.error("Failed to get session", session_id=session_id, error=str(e))
            return None
    
    def store_message(self, session_id: str, content: str, message_type: str, token_count: Optional[int] = None) -> Optional[str]:
        """Store a message in both database and vector store."""
        try:
            message_id = str(uuid.uuid4())
            
            # Store in database
            db = next(get_database())
            try:
                # Create message record
                new_message = Message(
                    message_id=message_id,
                    session_id=session_id,
                    content=content,
                    message_type=message_type,
                    token_count=token_count
                )
                
                # Update session activity and message count
                session = db.query(ChatSession).filter(
                    ChatSession.session_id == session_id
                ).first()
                
                if session:
                    session.last_activity = datetime.utcnow()
                    session.total_messages = session.total_messages + 1
                
                db.add(new_message)
                db.commit()
                
                # Store in vector database
                if self.embedding_service:
                    embedding_id = self.embedding_service.add_message_embedding(
                        session_id, content, message_id, message_type
                    )
                    if embedding_id:
                        # Update message with embedding ID
                        new_message.embedding_id = embedding_id
                        db.commit()
                
                logger.info("Stored message", 
                           session_id=session_id, 
                           message_id=message_id, 
                           message_type=message_type,
                           content_length=len(content))
                
                return message_id
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error("Failed to store message", 
                        session_id=session_id, 
                        message_type=message_type, 
                        error=str(e))
            return None
    
    def get_session_context(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Get recent conversation context for a session."""
        try:
            db = next(get_database())
            try:
                messages = db.query(Message).filter(
                    Message.session_id == session_id
                ).order_by(desc(Message.timestamp)).limit(limit).all()
                
                # Convert to context format (reverse to chronological order)
                context = []
                for message in reversed(messages):
                    context.append({
                        "content": message.content,
                        "type": message.message_type,
                        "timestamp": message.timestamp.isoformat() if message.timestamp else None,
                        "message_id": message.message_id
                    })
                
                logger.info("Retrieved session context", 
                           session_id=session_id, 
                           message_count=len(context))
                
                return context
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error("Failed to get session context", session_id=session_id, error=str(e))
            return []
    
    def add_session_insight(self, session_id: str, insight_type: str, content: str, confidence_score: Optional[float] = None) -> Optional[str]:
        """Add a therapeutic insight to the session."""
        try:
            insight_id = str(uuid.uuid4())
            
            db = next(get_database())
            try:
                insight = SessionInsight(
                    insight_id=insight_id,
                    session_id=session_id,
                    insight_type=insight_type,
                    content=content,
                    confidence_score=confidence_score
                )
                
                db.add(insight)
                db.commit()
                
                logger.info("Added session insight", 
                           session_id=session_id, 
                           insight_type=insight_type,
                           insight_id=insight_id)
                
                return insight_id
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error("Failed to add session insight", 
                        session_id=session_id, 
                        insight_type=insight_type, 
                        error=str(e))
            return None
    
    def get_session_insights(self, session_id: str, insight_type: Optional[str] = None) -> List[Dict]:
        """Get therapeutic insights for a session."""
        try:
            db = next(get_database())
            try:
                query = db.query(SessionInsight).filter(
                    SessionInsight.session_id == session_id
                )
                
                if insight_type:
                    query = query.filter(SessionInsight.insight_type == insight_type)
                
                insights = query.order_by(desc(SessionInsight.created_at)).all()
                
                # Convert to response format
                result = []
                for insight in insights:
                    result.append({
                        "insight_id": insight.insight_id,
                        "type": insight.insight_type,
                        "content": insight.content,
                        "confidence_score": insight.confidence_score,
                        "created_at": insight.created_at.isoformat() if insight.created_at else None
                    })
                
                logger.info("Retrieved session insights", 
                           session_id=session_id, 
                           insight_type=insight_type,
                           count=len(result))
                
                return result
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error("Failed to get session insights", 
                        session_id=session_id, 
                        insight_type=insight_type, 
                        error=str(e))
            return []
    
    def get_session_stats(self, session_id: str) -> Dict:
        """Get statistical information about a session."""
        try:
            db = next(get_database())
            try:
                session = db.query(ChatSession).filter(
                    ChatSession.session_id == session_id
                ).first()
                
                if not session:
                    return {}
                
                message_count = db.query(Message).filter(
                    Message.session_id == session_id
                ).count()
                
                user_messages = db.query(Message).filter(
                    Message.session_id == session_id,
                    Message.message_type == "user"
                ).count()
                
                therapist_messages = db.query(Message).filter(
                    Message.session_id == session_id,
                    Message.message_type == "therapist"
                ).count()
                
                insights_count = db.query(SessionInsight).filter(
                    SessionInsight.session_id == session_id
                ).count()
                
                return {
                    "session_id": session_id,
                    "created_at": session.created_at.isoformat() if session.created_at else None,
                    "last_activity": session.last_activity.isoformat() if session.last_activity else None,
                    "total_messages": message_count,
                    "user_messages": user_messages,
                    "therapist_messages": therapist_messages,
                    "insights_count": insights_count,
                    "metadata": session.session_metadata
                }
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error("Failed to get session stats", session_id=session_id, error=str(e))
            return {}
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session and all associated data (for privacy compliance)."""
        try:
            db = next(get_database())
            try:
                # Delete from database (cascades to messages and insights)
                session = db.query(ChatSession).filter(
                    ChatSession.session_id == session_id
                ).first()
                
                if session:
                    db.delete(session)
                    db.commit()
                
                # Delete from vector store
                if self.embedding_service:
                    self.embedding_service.delete_session_collection(session_id)
                
                logger.info("Deleted session", session_id=session_id)
                return True
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error("Failed to delete session", session_id=session_id, error=str(e))
            return False