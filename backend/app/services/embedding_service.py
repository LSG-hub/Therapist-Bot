"""
Embedding service using ChromaDB for session-isolated vector storage.
"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import structlog
from typing import List, Dict, Optional
import os
import uuid

logger = structlog.get_logger(__name__)

class EmbeddingService:
    """Manages vector embeddings with session-based isolation using ChromaDB."""
    
    def __init__(self):
        self.model_name = "all-MiniLM-L6-v2"  # Fast, lightweight model
        self.chroma_data_path = "./chroma_data"
        self.model = None
        self.chroma_client = None
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize sentence transformer and ChromaDB client."""
        try:
            # Initialize sentence transformer model
            logger.info("Loading sentence transformer model", model=self.model_name)
            self.model = SentenceTransformer(self.model_name)
            
            # Initialize ChromaDB client with persistent storage
            logger.info("Initializing ChromaDB client", data_path=self.chroma_data_path)
            self.chroma_client = chromadb.PersistentClient(
                path=self.chroma_data_path,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            logger.info("Embedding service initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize embedding service", error=str(e))
            raise
    
    def create_session_collection(self, session_id: str) -> bool:
        """Create a new vector collection for a chat session."""
        try:
            collection_name = f"session_{session_id.replace('-', '_')}"
            
            # Check if collection already exists
            try:
                existing_collection = self.chroma_client.get_collection(collection_name)
                logger.info("Session collection already exists", session_id=session_id)
                return True
            except Exception:
                # Collection doesn't exist, create new one
                pass
            
            collection = self.chroma_client.create_collection(
                name=collection_name,
                metadata={"session_id": session_id, "created_at": str(uuid.uuid4())}
            )
            
            logger.info("Created new session collection", session_id=session_id, collection=collection_name)
            return True
            
        except Exception as e:
            logger.error("Failed to create session collection", session_id=session_id, error=str(e))
            return False
    
    def add_message_embedding(self, session_id: str, message: str, message_id: str, message_type: str) -> Optional[str]:
        """Add a message embedding to the session's vector collection."""
        try:
            collection_name = f"session_{session_id.replace('-', '_')}"
            
            # Get or create collection
            try:
                collection = self.chroma_client.get_collection(collection_name)
            except Exception:
                # Create collection if it doesn't exist
                if not self.create_session_collection(session_id):
                    return None
                collection = self.chroma_client.get_collection(collection_name)
            
            # Generate embedding
            embedding = self.model.encode([message])[0].tolist()
            
            # Create unique embedding ID
            embedding_id = f"{message_type}_{message_id}"
            
            # Add to collection
            collection.add(
                embeddings=[embedding],
                documents=[message],
                metadatas=[{
                    "message_id": message_id,
                    "message_type": message_type,
                    "session_id": session_id
                }],
                ids=[embedding_id]
            )
            
            logger.info("Added message embedding", 
                       session_id=session_id, 
                       message_type=message_type,
                       embedding_id=embedding_id)
            
            return embedding_id
            
        except Exception as e:
            logger.error("Failed to add message embedding", 
                        session_id=session_id, 
                        message_id=message_id, 
                        error=str(e))
            return None
    
    def retrieve_relevant_context(self, session_id: str, query: str, n_results: int = 5) -> List[Dict]:
        """Retrieve relevant conversation context using semantic search."""
        try:
            collection_name = f"session_{session_id.replace('-', '_')}"
            
            # Get collection
            try:
                collection = self.chroma_client.get_collection(collection_name)
            except Exception:
                logger.info("No collection found for session", session_id=session_id)
                return []
            
            # Generate query embedding
            query_embedding = self.model.encode([query])[0].tolist()
            
            # Search for similar messages
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=min(n_results, collection.count()),
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            context_items = []
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    context_items.append({
                        "content": doc,
                        "message_type": metadata.get("message_type", "unknown"),
                        "message_id": metadata.get("message_id", ""),
                        "similarity_score": 1 - distance,  # Convert distance to similarity
                        "rank": i + 1
                    })
            
            logger.info("Retrieved relevant context", 
                       session_id=session_id, 
                       query_length=len(query),
                       results_count=len(context_items))
            
            return context_items
            
        except Exception as e:
            logger.error("Failed to retrieve relevant context", 
                        session_id=session_id, 
                        error=str(e))
            return []
    
    def get_session_message_count(self, session_id: str) -> int:
        """Get the total number of messages in a session collection."""
        try:
            collection_name = f"session_{session_id.replace('-', '_')}"
            collection = self.chroma_client.get_collection(collection_name)
            return collection.count()
        except Exception:
            return 0
        except Exception as e:
            logger.error("Failed to get session message count", session_id=session_id, error=str(e))
            return 0
    
    def delete_session_collection(self, session_id: str) -> bool:
        """Delete a session's vector collection (for privacy compliance)."""
        try:
            collection_name = f"session_{session_id.replace('-', '_')}"
            self.chroma_client.delete_collection(collection_name)
            logger.info("Deleted session collection", session_id=session_id)
            return True
        except Exception:
            logger.info("Session collection not found for deletion", session_id=session_id)
            return True  # Consider it successful if already doesn't exist
        except Exception as e:
            logger.error("Failed to delete session collection", session_id=session_id, error=str(e))
            return False