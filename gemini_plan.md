# Therapist Bot: Plan & Architecture

This document outlines the plan, architecture, and technologies for building the Therapist Bot application as per the assignment requirements.

## 1. Project Overview

The goal is to build a simple, yet robust, LLM-powered "Therapist Bot". The application will consist of a Python-based backend API and a modern web frontend. The project will be fully containerized and deployed to AWS, fulfilling all core and bonus requirements of the assignment.

- **Backend:** A FastAPI application providing a `/respond` endpoint.
- **Frontend:** A React-based single-page application for user interaction.
- **LLM:** Anthropic's API will be used to generate therapeutic responses.
- **Deployment:** The application will be deployed to AWS App Runner using two distinct methods: via a Docker container from ECR and directly from a GitHub source repository.

## 2. Architecture

The application will follow a decoupled frontend-backend architecture.

- **Frontend (Client-Side):** A React application built with Vite. It will provide the user interface for the chat, manage the conversation state, and communicate with the backend via RESTful API calls.
- **Backend (Server-Side):** A FastAPI application written in Python. It will expose a single API endpoint (`POST /respond`) that accepts a user's message. Its responsibilities include:
    1.  Receiving the request.
    2.  Applying safety guardrails (checking for red-flag keywords).
    3.  Constructing the prompt and calling the Anthropic API.
    4.  Logging the request/response pair with a timestamp.
    5.  Returning the LLM's response to the frontend.
- **Containerization:** The backend application will be containerized using Docker, ensuring a consistent and portable runtime environment.

## 3. Tools & Technologies

| Area                | Technology / Tool                               | Justification                                                                 |
| ------------------- | ----------------------------------------------- | ----------------------------------------------------------------------------- |
| **Backend**         | Python, FastAPI                                 | Meets the assignment's core requirement. FastAPI is modern and high-performance. |
| **Frontend**        | React.js, Vite                                  | A modern, industry-standard choice for building dynamic UIs. Vite for fast dev. |
| **Styling**         | Bootstrap CSS                                   | A reliable and popular CSS framework that avoids the requested `TailwindCSS`. |
| **LLM Integration** | Anthropic Python SDK                            | The specified LLM provider. The official SDK ensures reliable integration.     |
| **Containerization**| Docker                                          | Required for deployment and ensures environment consistency.                  |
| **Deployment**      | AWS App Runner, AWS ECR                         | The specified deployment platform as per the assignment.                      |
| **CI/CD**           | GitHub Actions                                  | To automate the Docker build and push to ECR, fulfilling a bonus requirement. |

## 4. Proposed Directory Structure

A monorepo structure will be used to keep the frontend and backend code organized within a single GitHub repository.

```
/Therapist-Bot/
|-- .github/
|   |-- workflows/
|       |-- deploy-to-ecr.yml      # GitHub Action for bonus task
|-- backend/
|   |-- app/
|   |   |-- __init__.py
|   |   |-- main.py                # FastAPI app, endpoints, logging
|   |   |-- services/
|   |   |   |-- __init__.py
|   |   |   |-- llm_service.py       # Logic for Anthropic API interaction
|   |   |   |-- guardrails.py        # Red-flag keyword detection
|   |   |-- models/
|   |   |   |-- __init__.py
|   |   |   |-- api_models.py        # Pydantic models for API
|   |-- tests/
|   |   |-- test_main.py             # Unit tests for the API
|   |-- .env.example             # Example for environment variables
|   |-- Dockerfile               # Dockerfile for the backend
|   |-- requirements.txt         # Python dependencies
|-- frontend/
|   |-- public/
|   |-- src/
|   |   |-- components/
|   |   |   |-- ChatWindow.jsx
|   |   |-- App.jsx
|   |   |-- index.css
|   |   |-- main.jsx
|   |-- .gitignore
|   |-- index.html
|   |-- package.json
|   |-- vite.config.js
|-- .gitignore                   # Root gitignore
|-- gemini_plan.md               # This file
|-- README.md                    # Setup, deployment, and usage instructions
```

## 5. Development & Deployment Plan

The project will be executed in the following phases:

1.  **Phase 1: Backend Development (FastAPI)**
    -   Initialize the project with the defined directory structure.
    -   Implement the `/respond` endpoint in `main.py`.
    -   Create Pydantic models for robust request and response handling.
    -   Implement the `guardrails.py` service to filter for sensitive keywords.
    -   Implement the `llm_service.py` to handle prompt construction and interaction with the Anthropic API.
    -   Add request/response logging with timestamps.
    -   Write unit tests to verify guardrail and endpoint functionality.

2.  **Phase 2: Frontend Development (React)**
    -   Scaffold the React application using Vite.
    -   Build the UI components, including the chat window and message input box.
    -   Implement state management to handle the conversation history.
    -   Integrate with the backend API to send user messages and display responses.
    -   Style the application with Bootstrap for a clean, responsive layout.

3.  **Phase 3: Containerization & Deployment**
    -   Write a multi-stage `Dockerfile` for the backend to create a lightweight and secure production image.
    -   **Deployment A (ECR):**
        -   Build the Docker image.
        -   Push the image to Amazon ECR.
        -   Deploy to AWS App Runner from the ECR image.
    -   **Deployment B (GitHub):**
        -   Push the complete source code to a new GitHub repository.
        -   Configure AWS App Runner to build and deploy directly from the GitHub repository.
    -   **Bonus CI/CD:** Create the GitHub Actions workflow to automatically build and push the Docker image to ECR upon a push to the `main` branch.

4.  **Phase 4: Documentation**
    -   Create a comprehensive `README.md` file.
    -   It will include clear, step-by-step instructions for:
        -   Setting up the local development environment.
        -   Configuring required environment variables (like `ANTHROPIC_API_KEY`).
        -   Running the application locally.
        -   Executing both deployment methods.

---

## Claude's Feedback & Enhancements

After reviewing Gemini's comprehensive plan, here are my observations and suggested improvements:

### 🎯 Strengths in Gemini's Plan
1. **Clear Architecture**: The decoupled frontend-backend approach is solid
2. **Monorepo Structure**: Smart choice for keeping everything organized
3. **Bootstrap CSS**: Good alternative to Tailwind as requested
4. **Phase-based Development**: Logical progression from backend to deployment

### 🚀 Suggested Enhancements & Additions

#### 1. Enhanced Prompt Engineering Strategy
```python
# More sophisticated CBT-focused system prompt
SYSTEM_PROMPT = """You are a warm, empathetic CBT (Cognitive Behavioral Therapy) assistant. 
Your responses should:
- Use CBT techniques like thought challenging, behavioral activation, and cognitive restructuring
- Ask open-ended questions to help users explore their thoughts and feelings
- Provide gentle reframes for negative thinking patterns
- Maintain professional boundaries - you're an assistant, not a licensed therapist
- Be concise but compassionate (150-300 words max)

CRITICAL SAFETY RULES:
- If user mentions suicide, self-harm, violence, or crisis: "I'm not qualified to handle this. Please contact a mental health professional immediately or call a crisis helpline."
- Never diagnose mental health conditions
- Never provide medical advice or medication recommendations
- Redirect medical questions to healthcare professionals"""
```

#### 2. Advanced Guardrails Implementation
```python
# Expanded crisis detection keywords
CRISIS_KEYWORDS = [
    'suicide', 'kill myself', 'end it all', 'not worth living',
    'self-harm', 'cut myself', 'hurt myself', 'overdose',
    'pills', 'jump off', 'hang myself', 'die', 'death'
]

MEDICAL_KEYWORDS = [
    'medication', 'prescription', 'dosage', 'symptoms',
    'diagnosis', 'disorder', 'therapy', 'psychiatrist'
]
```

#### 3. Enhanced Directory Structure
Additions to Gemini's structure:
```
/Therapist-Bot/
|-- deployment/
|   |-- apprunner.yaml          # App Runner configuration
|   |-- docker-compose.yml      # Local development
|-- docs/
|   |-- api.md                  # API documentation
|   |-- deployment.md           # Deployment guide
|-- backend/
|   |-- app/
|   |   |-- middleware/
|   |   |   |-- cors.py         # CORS configuration
|   |   |   |-- logging.py      # Request logging middleware
|   |   |-- utils/
|   |   |   |-- validators.py   # Input validation utilities
|   |   |-- config.py           # Application configuration
```

#### 4. TypeScript for Frontend
**Recommendation**: Use TypeScript instead of JavaScript for better type safety:
```typescript
// Enhanced type definitions
interface TherapyMessage {
  id: string;
  content: string;
  timestamp: Date;
  type: 'user' | 'therapist';
  isError?: boolean;
}

interface ApiResponse {
  response: string;
  timestamp: string;
  conversationId?: string;
}
```

#### 5. Production-Ready Features

**A. Rate Limiting & Security**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/respond")
@limiter.limit("10/minute")  # Prevent abuse
async def respond_endpoint(request: Request, message: MessageRequest):
    # Implementation
```

**B. Health Checks & Monitoring**
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/metrics")
async def metrics():
    # Basic metrics for monitoring
    return {"requests_processed": request_counter}
```

#### 6. Enhanced Deployment Strategy

**Docker Optimization**:
```dockerfile
# Multi-stage build for smaller images
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**GitHub Actions Enhancement**:
```yaml
# Additional workflow for automated testing
name: Test and Deploy
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest tests/
```

#### 7. Advanced Logging Strategy
```python
import structlog
from datetime import datetime

logger = structlog.get_logger()

async def log_conversation(user_message: str, bot_response: str, user_id: str = None):
    logger.info(
        "conversation_logged",
        timestamp=datetime.utcnow().isoformat(),
        user_message=user_message[:100] + "..." if len(user_message) > 100 else user_message,
        response_length=len(bot_response),
        user_id=user_id or "anonymous",
        guardrail_triggered=check_for_crisis_keywords(user_message)
    )
```

#### 8. Frontend Enhancements

**State Management with Context**:
```typescript
// Better state management for conversation history
const ConversationContext = createContext();

const useConversation = () => {
  const [messages, setMessages] = useState<TherapyMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  
  const sendMessage = async (content: string) => {
    // Enhanced message handling with optimistic updates
  };
  
  return { messages, sendMessage, isLoading };
};
```

### 🎨 UI/UX Improvements
1. **Typing Indicators**: Show when the therapist is "thinking"
2. **Message Timestamps**: Display conversation timing
3. **Conversation Persistence**: Save chat history in localStorage
4. **Accessibility**: ARIA labels and keyboard navigation
5. **Mobile Responsive**: Ensure great mobile experience

### 📊 Testing Strategy Enhancement
```python
# Comprehensive test coverage
def test_crisis_detection():
    assert detect_crisis("I want to hurt myself") == True
    assert detect_crisis("I'm feeling sad") == False

def test_response_quality():
    # Test that responses follow CBT principles
    response = generate_response("I always fail at everything")
    assert "cognitive distortion" in response.lower() or "reframe" in response.lower()
```

### 🔐 Security Best Practices
1. **Environment Variables**: Secure API key management
2. **Input Sanitization**: Prevent injection attacks
3. **HTTPS Only**: Force secure connections in production
4. **CORS Configuration**: Proper cross-origin setup

### 📈 Monitoring & Analytics
```python
# CloudWatch integration for AWS deployment
import boto3

cloudwatch = boto3.client('cloudwatch')

def log_metric(metric_name: str, value: float):
    cloudwatch.put_metric_data(
        Namespace='TherapistBot',
        MetricData=[{
            'MetricName': metric_name,
            'Value': value,
            'Unit': 'Count'
        }]
    )
```

### 🎯 Conclusion
Gemini's plan provides an excellent foundation. These enhancements add:
- Production-ready security and monitoring
- Better user experience with TypeScript and advanced state management
- Comprehensive testing and deployment strategies
- Professional-grade CBT prompt engineering

The combined approach ensures we deliver not just a working prototype, but a production-ready application that demonstrates industry best practices.
