# Phase 1 Plan: Therapist Bot Implementation

## 🎯 Combined Approach Overview

This plan synthesizes the best elements from both Claude's comprehensive architecture and Gemini's pragmatic MVP approach. We prioritize rapid development while maintaining production-ready standards.

## 🏗️ Final Architecture Decision

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   React Frontend    │────│   FastAPI Backend   │────│   Anthropic API     │
│   + React-Bootstrap │    │   + Guardrails      │    │   (Claude Sonnet 4) │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
         │                           │
         │                  ┌─────────────────────┐
         └──────────────────│   Request Logging   │
                            │   + Health Checks   │
                            └─────────────────────┘
```

## 🛠️ Final Technology Stack

### Backend

- **Framework**: FastAPI (async, high-performance)
- **LLM Provider**: Anthropic Claude API
- **HTTP Client**: httpx (async)
- **Validation**: Pydantic v2 models
- **Logging**: Python structlog
- **Rate Limiting**: slowapi
- **Environment**: python-dotenv
- **Testing**: pytest + httpx test client

### Frontend

- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: React-Bootstrap (rapid development)
- **HTTP Client**: fetch API
- **State Management**: React Context + hooks
- **Icons**: React-Bootstrap-Icons

### DevOps

- **Containerization**: Docker (multi-stage builds)
- **Registry**: Amazon ECR
- **Deployment**: AWS App Runner (dual methods)
- **CI/CD**: GitHub Actions
- **Monitoring**: CloudWatch

## 📁 Simplified Directory Structure

```
therapist-bot/
├── README.md                    # Comprehensive setup & deployment guide
├── .env.example                # Environment variables template
├── docker-compose.yml          # Local development
│
├── backend/
│   ├── Dockerfile
│   ├── apprunner.yaml          # App Runner configuration
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI entry point + CORS
│   │   ├── config.py           # Configuration management
│   │   ├── models.py           # Pydantic request/response models
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── llm_service.py  # Anthropic API integration
│   │   │   ├── guardrails.py   # Safety checks & keyword detection
│   │   │   └── logging.py      # Structured logging utility
│   │   └── middleware/
│   │       ├── __init__.py
│   │       └── rate_limit.py   # Rate limiting middleware
│   └── tests/
│       ├── __init__.py
│       ├── test_main.py        # API endpoint tests
│       ├── test_guardrails.py  # Safety checks tests
│       └── conftest.py         # Test configuration
│
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── index.html
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── components/
│       │   ├── ChatInterface.tsx    # Main chat UI
│       │   ├── MessageList.tsx      # Message history display
│       │   ├── MessageInput.tsx     # User input component
│       │   └── LoadingIndicator.tsx # Typing indicator
│       ├── hooks/
│       │   └── useChat.ts          # Chat state management
│       ├── types/
│       │   └── api.ts              # TypeScript interfaces
│       └── utils/
│           └── api.ts              # API communication utilities
│
└── .github/
    └── workflows/
        ├── deploy-ecr.yml          # Docker + ECR + App Runner
        └── deploy-github.yml       # GitHub source deployment
```

## 🎯 Implementation Phases

### Phase 1A: Backend Core (4 hours)

#### 1.1 Project Setup (30 min)

```bash
# Initialize backend structure
mkdir -p backend/app/services backend/app/middleware backend/tests
cd backend
```

#### 1.2 Dependencies (requirements.txt)

```
fastapi
uvicorn[standard]
anthropic
httpx
pydantic
python-dotenv
structlog
slowapi
pytest
pytest-asyncio
```

**Note**: Working in your existing venv with latest compatible versions. The latest Anthropic SDK will support **Claude Sonnet 4** with enhanced reasoning capabilities.

#### 1.3 Core FastAPI App (1 hour)

- **File**: `backend/app/main.py`
- **Features**:
  - Basic FastAPI setup with CORS
  - Health check endpoint (`/health`)
  - Request logging middleware
  - Rate limiting setup

#### 1.4 Configuration Management (30 min)

- **File**: `backend/app/config.py`
- **Features**:
  - Environment variable loading
  - Anthropic API key validation
  - App configuration class

#### 1.5 Pydantic Models (30 min)

- **File**: `backend/app/models.py`
- **Models**:
  ```python
  class MessageRequest(BaseModel):
      message: str = Field(..., min_length=1, max_length=1000)

  class MessageResponse(BaseModel):
      response: str
      timestamp: datetime
      conversation_id: Optional[str] = None
  ```

#### 1.6 LLM Service (1 hour)

- **File**: `backend/app/services/llm_service.py`
- **Features**:
  - Anthropic API integration
  - CBT-focused system prompt
  - Error handling and retries
  - Response validation

#### 1.7 Guardrails System (1 hour)

- **File**: `backend/app/services/guardrails.py`
- **Features**:
  - Crisis keyword detection
  - Medical advice filtering
  - Safety response generation
  - Logging of flagged content

### Phase 1B: Frontend Core (3 hours)

#### 1.8 React Setup (45 min)

```bash
# Initialize frontend
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install react-bootstrap bootstrap react-bootstrap-icons
```

#### 1.9 TypeScript Interfaces (15 min)

- **File**: `frontend/src/types/api.ts`
- **Interfaces**:
  ```typescript
  interface Message {
    id: string;
    content: string;
    timestamp: Date;
    type: 'user' | 'therapist';
    isError?: boolean;
  }

  interface ApiResponse {
    response: string;
    timestamp: string;
    conversation_id?: string;
  }
  ```

#### 1.10 API Utilities (30 min)

- **File**: `frontend/src/utils/api.ts`
- **Features**:
  - API endpoint configuration
  - Request/response handling
  - Error management

#### 1.11 Chat Hook (45 min)

- **File**: `frontend/src/hooks/useChat.ts`
- **Features**:
  - Message state management
  - Send message functionality
  - Loading states
  - Error handling

#### 1.12 UI Components (45 min)

- **ChatInterface.tsx**: Main container with React-Bootstrap layout
- **MessageList.tsx**: Scrollable message history
- **MessageInput.tsx**: Input form with send button
- **LoadingIndicator.tsx**: Typing indicator

### Phase 1C: Integration & Testing (1 hour)

#### 1.13 Local Development Setup (30 min)

- **File**: `docker-compose.yml`
- **Features**:
  - Backend service configuration
  - Environment variable mounting
  - Port mapping (backend: 8000, frontend: 5173)

#### 1.14 Basic Testing (30 min)

- API endpoint tests
- Guardrails functionality tests
- Frontend-backend integration test

## 🔒 Enhanced Security & Guardrails

### CBT Therapist System Prompt

```
You are a warm, empathetic CBT (Cognitive Behavioral Therapy) assistant named Alex. 

Your therapeutic approach:
- Use evidence-based CBT techniques (thought challenging, behavioral activation, cognitive restructuring)
- Ask gentle, open-ended questions to help users explore thoughts and feelings
- Provide supportive reframes for negative thinking patterns
- Keep responses concise (150-300 words) but compassionate
- Maintain professional boundaries - you're an AI assistant, not a licensed therapist

CRITICAL SAFETY RULES:
- If someone mentions suicide, self-harm, violence, or crisis situations: "I'm not qualified to handle crisis situations. Please contact a mental health professional immediately or call a crisis helpline: 988 (US), 116 123 (UK), or your local emergency services."
- Never diagnose mental health conditions
- Never provide medical advice or medication recommendations
- For medical questions, redirect to healthcare professionals
- If unsure about safety, err on the side of caution

Remember: Your role is to provide supportive guidance using CBT principles while ensuring user safety.
```

### Advanced Guardrails

```python
CRISIS_KEYWORDS = [
    'suicide', 'kill myself', 'end it all', 'not worth living',
    'self-harm', 'cut myself', 'hurt myself', 'overdose',
    'jump off', 'hang myself', 'want to die', 'better off dead'
]

MEDICAL_KEYWORDS = [
    'medication', 'prescription', 'dosage', 'pills',
    'antidepressant', 'diagnosis', 'bipolar', 'schizophrenia'
]

def check_safety(message: str) -> tuple[bool, str]:
    """Returns (is_safe, safety_response)"""
    message_lower = message.lower()
  
    for keyword in CRISIS_KEYWORDS:
        if keyword in message_lower:
            return False, "I'm not qualified to handle crisis situations. Please contact a mental health professional immediately or call a crisis helpline."
  
    for keyword in MEDICAL_KEYWORDS:
        if keyword in message_lower:
            return False, "I can't provide medical advice. Please consult with a healthcare professional about medical concerns."
  
    return True, ""
```

## 📊 Success Criteria for Phase 1

### Backend Requirements ✅

- [ ] FastAPI server running on port 8000
- [ ] `/respond` endpoint accepting POST requests
- [ ] Anthropic API integration working
- [ ] Guardrails detecting crisis keywords
- [ ] Health check endpoint responding
- [ ] Request/response logging implemented

### Frontend Requirements ✅

- [ ] React app running on port 5173
- [ ] Chat interface with React-Bootstrap styling
- [ ] Message input and display working
- [ ] API communication established
- [ ] Loading states and error handling
- [ ] TypeScript compilation without errors

### Integration Requirements ✅

- [ ] Frontend can send messages to backend
- [ ] Backend responses display in frontend
- [ ] Guardrails trigger appropriate responses
- [ ] Local development with docker-compose
- [ ] No CORS issues between frontend/backend

## 🧪 Testing Strategy

### Backend Tests

```python
def test_respond_endpoint():
    """Test normal therapeutic response"""
    response = client.post("/respond", json={"message": "I feel anxious"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_crisis_detection():
    """Test guardrails for crisis situations"""
    response = client.post("/respond", json={"message": "I want to hurt myself"})
    assert "not qualified to handle" in response.json()["response"]

def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
```

### Frontend Tests

- Manual testing of chat interface
- API integration verification
- Error state handling
- Responsive design check

## ⏱️ Timeline Estimation

**Total Phase 1: 8 hours**

- Backend Core: 4 hours
- Frontend Core: 3 hours
- Integration & Testing: 1 hour

**Deliverables**:

- Working local development environment
- Functional chat interface
- Basic CBT responses from Anthropic API
- Safety guardrails operational
- Ready for containerization (Phase 2)

## 🚀 Ready for Review

This plan combines:

- **Claude's comprehensive approach**: Production-ready architecture, security, testing
- **Gemini's pragmatic focus**: Simplified structure, React-Bootstrap, rapid development
- **Balanced timeline**: Achievable 8-hour Phase 1 with clear deliverables

The result is a professional MVP foundation that can be quickly extended with deployment and CI/CD in subsequent phases.

---

## 🧠 Phase 1C: RAG Implementation (4-6 hours)

### Overview
Implement Retrieval Augmented Generation (RAG) to transform the therapist bot from a stateless system into a sophisticated therapeutic companion with session-based memory and context awareness.

### Architecture Decision

**Database Stack:**
- **Primary Database**: SQLite (zero-setup, ACID compliant)
- **Vector Database**: ChromaDB (local embeddings, session isolation)
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2 (local, fast)

### Database Schema

```sql
-- Chat Sessions Table
CREATE TABLE chat_sessions (
    session_id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_metadata JSON,
    total_messages INTEGER DEFAULT 0
);

-- Messages Table
CREATE TABLE messages (
    message_id TEXT PRIMARY KEY,
    session_id TEXT REFERENCES chat_sessions(session_id),
    content TEXT NOT NULL,
    message_type TEXT CHECK (message_type IN ('user', 'therapist')),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    embedding_id TEXT,
    token_count INTEGER
);

-- Session Insights for Therapeutic Continuity
CREATE TABLE session_insights (
    insight_id TEXT PRIMARY KEY,
    session_id TEXT REFERENCES chat_sessions(session_id),
    insight_type TEXT, -- 'theme', 'trigger', 'progress', 'goal', 'emotion'
    content TEXT,
    confidence_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Implementation Plan

#### Phase 1C.1: Database & ORM Setup (1-2 hours)

**Dependencies to Add:**
```
sqlalchemy
chromadb
sentence-transformers
numpy
```

**Files to Create:**
- `backend/app/database/models.py` - SQLAlchemy models
- `backend/app/database/connection.py` - Database connection
- `backend/app/services/embedding_service.py` - Vector embeddings
- `backend/app/services/rag_service.py` - RAG orchestration
- `backend/app/services/session_service.py` - Session management

#### Phase 1C.2: RAG Service Development (2-3 hours)

**Key Components:**

1. **Session Management**
```python
class SessionService:
    def create_session(self) -> str:
        """Create new chat session with unique ID"""
    
    def get_session_context(self, session_id: str, limit: int = 10) -> List[str]:
        """Retrieve recent conversation context"""
    
    def store_message(self, session_id: str, content: str, msg_type: str):
        """Store message with embedding"""
```

2. **Embedding Service**
```python
class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client = chromadb.Client()
    
    def create_session_collection(self, session_id: str):
        """Create isolated vector collection per session"""
    
    def add_message_embedding(self, session_id: str, message: str, message_id: str):
        """Add message embedding to session collection"""
    
    def retrieve_relevant_context(self, session_id: str, query: str, n_results: int = 5) -> List[str]:
        """Semantic search within session"""
```

3. **RAG Service Integration**
```python
class RAGService:
    def __init__(self, embedding_service, session_service, llm_service):
        self.embedding_service = embedding_service
        self.session_service = session_service
        self.llm_service = llm_service
    
    def generate_rag_response(self, session_id: str, user_message: str) -> str:
        """Generate context-aware therapeutic response"""
        
        # 1. Retrieve relevant conversation context
        context = self.embedding_service.retrieve_relevant_context(session_id, user_message)
        
        # 2. Build enhanced prompt with context
        enhanced_prompt = self.build_therapeutic_prompt(user_message, context)
        
        # 3. Generate response with Claude
        response = await self.llm_service.generate_response(enhanced_prompt)
        
        # 4. Store both user message and response
        self.session_service.store_message(session_id, user_message, 'user')
        self.session_service.store_message(session_id, response, 'therapist')
        
        return response
```

#### Phase 1C.3: Enhanced Prompt Engineering (1-2 hours)

**RAG-Enhanced System Prompt:**
```python
def build_therapeutic_prompt(self, user_message: str, session_context: List[str]) -> str:
    context_text = "\n".join([f"- {ctx}" for ctx in session_context]) if session_context else "This is the beginning of our conversation."
    
    return f"""You are Alex, a warm, empathetic CBT therapist assistant. You are having an ongoing conversation with this person.

CONVERSATION HISTORY:
{context_text}

CURRENT MESSAGE: {user_message}

As their CBT assistant, provide therapeutic guidance that:
- Builds on previous conversation themes and insights
- References earlier topics when therapeutically relevant
- Maintains conversation continuity and therapeutic rapport
- Uses CBT techniques appropriate for their ongoing journey
- Shows you remember and care about their progress

Respond in a way that demonstrates therapeutic continuity while providing fresh, helpful CBT guidance."""
```

### Frontend Integration

#### Updated API Types
```typescript
export interface SessionInfo {
  sessionId: string;
  createdAt: string;
  messageCount: number;
}

export interface MessageRequest {
  message: string;
  sessionId?: string;  // Optional for new sessions
}

export interface MessageResponse {
  response: string;
  timestamp: string;
  sessionId: string;     // Always returned
  contextUsed: boolean;  // Indicates if RAG was used
}
```

#### Updated Chat Hook
```typescript
export const useChat = () => {
  const [sessionId, setSessionId] = useState<string | null>(null);
  
  const startNewSession = () => {
    setSessionId(null);
    setState(prev => ({ ...prev, messages: [] }));
  };
  
  const sendMessage = async (content: string) => {
    // Include sessionId in request
    const response = await apiClient.sendMessage(content, sessionId);
    
    // Update sessionId if this was a new session
    if (!sessionId) {
      setSessionId(response.sessionId);
    }
    
    // Rest of the logic...
  };
};
```

### Benefits of RAG Implementation

**1. Therapeutic Continuity**
- "I remember you mentioned feeling anxious about presentations last week. How did that meeting go?"
- References to previous coping strategies and their effectiveness
- Builds therapeutic relationship over time

**2. Personalized Interventions**
- Context-aware CBT technique selection
- Tailored responses based on user's specific triggers and patterns
- Progressive therapeutic goals based on session history

**3. Privacy & Security**
- Complete session isolation (no cross-contamination)
- Local database storage (no external data sharing)
- Session-specific vector collections in ChromaDB

**4. Enhanced User Experience**
- More natural, flowing conversations
- Demonstrates AI "memory" and care
- Reduces repetitive explanations from users

### Success Metrics

**Technical:**
- ✅ Session creation and management working
- ✅ Vector embeddings stored per session
- ✅ Context retrieval functioning (semantic search)
- ✅ Enhanced prompts improving response quality

**Therapeutic:**
- ✅ Responses reference previous conversation points
- ✅ Therapeutic continuity maintained across messages
- ✅ Context-appropriate CBT interventions
- ✅ Progressive therapeutic relationship building

### Testing Strategy

**Unit Tests:**
- Session creation and isolation
- Embedding generation and retrieval
- Database operations and data integrity

**Integration Tests:**
- Full RAG pipeline (message → context → response)
- Session-based conversation flows
- Cross-session isolation verification

**User Experience Tests:**
- Conversation continuity across multiple messages
- Therapeutic relevance of contextual responses
- Session management (new session, clear history)

---

## 📊 Updated Timeline

**Total Phase 1 (including RAG): 14-16 hours**
- Backend Core: 4 hours ✅
- Frontend Core: 3 hours ✅
- Integration & Testing: 1 hour ✅
- **RAG Implementation: 4-6 hours** 🔄

**Deliverables After RAG**:
- Session-aware therapeutic conversations
- Context-rich CBT guidance
- Personalized user experiences
- Scalable database architecture
- Privacy-compliant session isolation

The RAG implementation will elevate the therapist bot from a simple Q&A system to a sophisticated therapeutic companion that maintains meaningful conversation continuity while respecting privacy boundaries.

**Next Steps After RAG Completion**:

1. ✅ Create project structure
2. ✅ Implement backend core
3. ✅ Build React frontend
4. ✅ Integrate and test locally
5. 🔄 Implement RAG for session continuity
6. Prepare for Phase 2 (Containerization & Deployment)
