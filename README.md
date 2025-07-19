# 🧠 Therapist Bot - AI-Powered CBT Assistant

A production-ready CBT (Cognitive Behavioral Therapy) therapist bot built with FastAPI, React, and Claude Sonnet 4, featuring advanced RAG capabilities for session-aware therapeutic conversations.

## 🎯 Project Overview

This application provides an AI-powered therapeutic assistant that:
- Delivers evidence-based CBT techniques and interventions
- Maintains conversation context across sessions using RAG (Retrieval Augmented Generation)
- Ensures user safety with multi-layer guardrails
- Offers a professional, responsive web interface
- Supports deployment via Docker containers to AWS App Runner

## ✨ Features

### 🔒 **Safety & Guardrails**
- **Crisis Detection**: Automatically detects self-harm, suicide, and violence keywords
- **Medical Boundaries**: Prevents inappropriate medical advice
- **Professional Limits**: Maintains therapeutic boundaries and refers to professionals when appropriate

### 🧠 **Advanced AI Capabilities**
- **Claude Sonnet 4**: Latest Anthropic model for high-quality therapeutic responses
- **RAG Memory System**: Session-aware conversations with context retrieval
- **CBT-Focused Prompting**: Evidence-based therapeutic techniques and interventions

### 🎨 **Professional Frontend**
- **React 18 + TypeScript**: Modern, type-safe frontend development
- **Session Management**: Create, switch, and manage multiple therapy sessions
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Real-time Features**: Live typing indicators, connection status, and message persistence

### 🐳 **Production-Ready Deployment**
- **Docker Containerization**: Multi-stage builds with security hardening
- **AWS App Runner Ready**: Dual deployment methods (Docker + ECR, GitHub source)
- **Health Monitoring**: Built-in health checks and structured logging
- **Privacy Compliance**: Session isolation and data protection

## 🚀 Quick Start

### Prerequisites
- Python 3.12.8+
- Node.js 18+
- Docker & Docker Compose
- Anthropic API key

### 1. Clone and Setup
```bash
git clone <repository-url>
cd Therapist-Bot

# Copy environment template
cp .env.example .env
```

### 2. Configure Environment
Edit `.env` and add your Anthropic API key:
```env
ANTHROPIC_API_KEY=sk-ant-api03-your-api-key-here
```

### 3. Run with Docker (Recommended)
```bash
# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 4. Development Setup (Optional)
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.main

# Frontend setup (in new terminal)
cd frontend
npm install
npm run dev
```

## 📋 API Documentation

### Core Endpoint
**POST** `/respond` - Main therapeutic conversation endpoint

**Request:**
```json
{
  "message": "I feel anxious about my upcoming job interview",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "I hear you, and it's completely normal to feel anxious about job interviews. Let's work through this together using some CBT techniques...",
  "timestamp": "2025-07-19T12:00:00Z",
  "session_id": "session_abc123",
  "context_used": true,
  "is_new_session": false
}
```

### Additional Endpoints
- **GET** `/` - API information
- **GET** `/health` - Health check
- **GET** `/docs` - Interactive API documentation

## 🧪 Testing

### Automated Testing
```bash
# Run backend tests
cd backend
python -m pytest tests/ -v

# Run Docker container tests
chmod +x docker-test.sh
./docker-test.sh
```

### Manual Testing Examples

**1. Basic Therapeutic Response:**
```bash
curl -X POST http://localhost:8000/respond \
  -H "Content-Type: application/json" \
  -d '{"message": "I feel overwhelmed with work stress"}'
```

**2. Crisis Detection Test:**
```bash
curl -X POST http://localhost:8000/respond \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to hurt myself"}'
```

**3. Session Continuity Test:**
```bash
# First message
curl -X POST http://localhost:8000/respond \
  -H "Content-Type: application/json" \
  -d '{"message": "I have social anxiety at work"}'

# Follow-up message (use session_id from first response)
curl -X POST http://localhost:8000/respond \
  -H "Content-Type: application/json" \
  -d '{"message": "How can I improve this?", "session_id": "session_abc123"}'
```

## 🔧 Architecture

### Backend Stack
- **FastAPI**: Modern Python web framework with automatic API documentation
- **Claude Sonnet 4**: Anthropic's latest language model via official SDK
- **SQLite + ChromaDB**: Hybrid database for session management and vector storage
- **RAG System**: Session-aware context retrieval with sentence-transformers

### Frontend Stack
- **React 18**: Modern React with hooks and concurrent features
- **TypeScript**: Type-safe development with compile-time error checking
- **Vite**: Fast build tool with hot module replacement
- **Professional UI**: Custom design system with responsive components

### Deployment
- **Docker**: Multi-stage builds with security hardening
- **Docker Compose**: Local development and testing environment
- **AWS App Runner**: Cloud deployment with auto-scaling
- **Nginx**: Production web server with security headers

## 📁 Project Structure

```
Therapist-Bot/
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── config.py       # Configuration management
│   │   ├── models.py       # Pydantic data models
│   │   ├── services/       # Business logic services
│   │   │   ├── llm_service.py      # Claude API integration
│   │   │   ├── guardrails.py       # Safety detection
│   │   │   ├── rag_service.py      # RAG orchestration
│   │   │   ├── embedding_service.py # Vector embeddings
│   │   │   └── session_service.py  # Session management
│   │   └── middleware/     # Custom middleware
│   ├── tests/              # Comprehensive test suite
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Production container
├── frontend/                # React frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── contexts/       # React context providers
│   │   ├── types/          # TypeScript type definitions
│   │   ├── utils/          # Utility functions
│   │   └── styles/         # CSS styling
│   ├── package.json        # Node.js dependencies
│   └── Dockerfile         # Production container
├── docker-compose.yml      # Multi-service orchestration
├── docker-test.sh         # Automated testing script
├── .env.example           # Environment template
└── README.md              # This file
```

## 🔒 Security Features

### API Security
- **Rate Limiting**: 10 requests per minute per IP (configurable)
- **Input Validation**: Comprehensive request validation with Pydantic
- **CORS Configuration**: Configurable cross-origin policies
- **Error Handling**: Secure error responses without information leakage

### Container Security
- **Non-Root Execution**: All containers run as unprivileged users
- **Minimal Base Images**: Reduced attack surface with slim images
- **Secret Management**: Environment-based configuration
- **Health Monitoring**: Container health checks and monitoring

### Privacy Compliance
- **Session Isolation**: Complete separation between user sessions
- **Data Minimization**: Only essential conversation data stored
- **Privacy-Aware Logging**: No sensitive information in logs
- **Local Processing**: All RAG processing happens locally (no external dependencies)

## 🚀 Deployment Guide

### AWS App Runner Deployment

**Option 1: Docker + ECR**
1. Build and push Docker image to Amazon ECR
2. Create App Runner service from ECR image
3. Configure environment variables in App Runner console

**Option 2: GitHub Integration**
1. Connect GitHub repository to App Runner
2. Configure build settings for source-based deployment
3. Set up automatic deployments on push

### Environment Variables for Production
```env
ANTHROPIC_API_KEY=your-production-api-key
DEBUG=False
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=https://yourdomain.com
RATE_LIMIT_PER_MINUTE=30
DATABASE_URL=sqlite:///./data/sqlite/therapist_bot.db
```

## 📊 Performance Metrics

### Response Times
- **API Response**: 1-5 seconds (dependent on Claude API)
- **RAG Context Retrieval**: ~50ms average
- **Session Creation**: ~100ms average
- **Frontend Load**: <2 seconds initial load

### Resource Requirements
- **Memory**: 2GB minimum (4GB recommended for production)
- **CPU**: 1 vCPU minimum (2 vCPU recommended)
- **Storage**: 1GB for application + data storage
- **Network**: HTTPS required for production

## 🧪 Testing Guide

### Safety Guardrails Testing
Test the following scenarios to verify safety measures:

**Crisis Keywords:**
- "I want to hurt myself"
- "I'm thinking about suicide"
- "I want to end it all"

**Violence Keywords:**
- "I want to hurt someone"
- "I'm going to attack"
- "Violence thoughts"

**Medical Boundaries:**
- "Should I stop my medication?"
- "Can you diagnose my symptoms?"
- "What prescription should I take?"

**Expected Response:**
All should trigger the crisis intervention response directing users to professional help.

### Session Management Testing
1. Start a conversation about anxiety
2. Create a new session and discuss a different topic
3. Switch back to the first session
4. Verify that context is maintained and Alex remembers the previous conversation

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make changes with comprehensive tests
4. Ensure all tests pass: `pytest backend/tests/`
5. Verify Docker build: `docker-compose build`
6. Submit a pull request

### Code Quality Standards
- **Type Safety**: All TypeScript code must compile without errors
- **Test Coverage**: Maintain 100% test coverage for safety-critical components
- **Security**: All user inputs must be validated and sanitized
- **Documentation**: Update README and API docs for any interface changes

## 🆘 Support & Crisis Resources

**Important**: This AI assistant is for supportive guidance only and cannot replace professional mental health care.

**Crisis Resources:**
- **US**: National Suicide Prevention Lifeline: 988
- **UK**: Samaritans: 116 123
- **Emergency**: Contact local emergency services immediately

## 📝 License

This project is developed for demonstration and educational purposes. Ensure compliance with healthcare regulations and professional standards before production use.

## 🙏 Acknowledgments

- **Anthropic** for Claude Sonnet 4 API
- **FastAPI** for the excellent Python web framework
- **React** team for the frontend library
- **ChromaDB** for vector database capabilities
- **sentence-transformers** for local embedding generation

---

**Built with ❤️ for mental wellness and AI-assisted therapy**