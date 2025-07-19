# Therapist Bot - Implementation Plan

## 📋 Assignment Overview

Building a CBT (Cognitive Behavioral Therapy) therapist bot with FastAPI backend, React frontend, and dual AWS App Runner deployment strategies using Anthropic Claude API.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Client  │────│  FastAPI Server │────│  Anthropic API  │
│   (Frontend)    │    │   (Backend)     │    │   (Claude LLM)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │              ┌─────────────────┐
         └──────────────│   Static Files  │
                        │   (if needed)   │
                        └─────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (async, high-performance)
- **LLM Provider**: Anthropic Claude API
- **HTTP Client**: httpx (async)
- **Validation**: Pydantic models
- **Logging**: Python logging with structured format
- **Environment**: python-dotenv for config

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite (fast, modern)
- **Styling**: CSS Modules (avoiding Tailwind as requested)
- **HTTP Client**: fetch API
- **State Management**: React hooks (useState, useEffect)

### DevOps & Deployment
- **Containerization**: Docker (multi-stage builds)
- **Registry**: Amazon ECR
- **Deployment**: AWS App Runner (2 methods)
- **CI/CD**: GitHub Actions
- **Monitoring**: CloudWatch logs

## 📁 Directory Structure

```
therapist-bot/
├── README.md
├── claude_plan.md
├── assignment.md
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── models.py            # Pydantic models
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── llm_service.py   # Anthropic API integration
│   │   │   └── guardrails.py    # Safety checks
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── logging.py       # Structured logging
│   └── tests/
│       ├── __init__.py
│       ├── test_main.py
│       └── test_guardrails.py
│
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── index.html
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx
│   │   │   └── MessageBubble.tsx
│   │   ├── styles/
│   │   │   ├── App.module.css
│   │   │   └── ChatInterface.module.css
│   │   └── types/
│   │       └── api.ts
│   └── dist/                    # Build output
│
├── deployment/
│   ├── docker-compose.yml       # Local development
│   ├── apprunner.yaml          # App Runner config
│   └── github-actions/
│       ├── deploy-ecr.yml      # ECR + App Runner workflow
│       └── deploy-github.yml   # GitHub source workflow
│
└── docs/
    ├── setup.md
    ├── deployment.md
    └── api.md
```

## 🎯 Implementation Plan

### Phase 1: Core Backend (Day 1)
1. **Setup FastAPI project structure**
   - Initialize backend directory
   - Create requirements.txt with dependencies
   - Setup basic FastAPI app with health check

2. **Implement LLM Integration**
   - Create Anthropic API service
   - Design CBT therapist system prompt
   - Implement /respond endpoint

3. **Add Guardrails System**
   - Keyword detection for crisis situations
   - Response filtering and safety checks
   - Graceful fallback responses

### Phase 2: Frontend Development (Day 1-2)
1. **React App Setup**
   - Initialize Vite + React + TypeScript project
   - Create basic chat interface
   - Implement API communication

2. **UI/UX Design**
   - Clean, therapeutic-friendly design
   - Message bubbles for conversation flow
   - Loading states and error handling

### Phase 3: Containerization (Day 2)
1. **Docker Configuration**
   - Multi-stage Dockerfile for backend
   - Separate Dockerfile for frontend (if needed)
   - Docker Compose for local development

2. **Optimization**
   - Minimize image size
   - Security best practices
   - Health checks

### Phase 4: AWS Deployment (Day 2-3)
1. **Part A: ECR + App Runner**
   - Build and push Docker image to ECR
   - Create App Runner service from ECR image
   - Configure environment variables

2. **Part B: GitHub + App Runner**
   - Setup GitHub repository
   - Configure App Runner to build from source
   - Test direct deployment

### Phase 5: CI/CD & Monitoring (Day 3)
1. **GitHub Actions**
   - Automated Docker builds
   - ECR push workflow
   - App Runner deployment triggers

2. **Logging & Monitoring**
   - Structured request/response logging
   - CloudWatch integration
   - Error tracking

## 🔒 Security & Guardrails

### Prompt Engineering
```
System Prompt: "You are a warm, professional CBT therapist assistant. 
Your role is to:
- Provide supportive, evidence-based guidance
- Use CBT techniques like thought challenging and reframing
- Maintain professional boundaries
- NEVER diagnose or provide medical advice
- If someone mentions suicide, self-harm, or crisis: respond with 'I'm not qualified to handle this. Please talk to a professional immediately or call a crisis helpline.'"
```

### Guardrails Implementation
- **Keyword Detection**: suicide, kill, harm, die, hurt, pills, overdose
- **Response Filtering**: Medical advice detection
- **Rate Limiting**: Prevent API abuse
- **Input Validation**: Sanitize user inputs

## 🚀 Deployment Strategy

### Method 1: Docker + ECR + App Runner
1. Build Docker image locally
2. Push to Amazon ECR
3. Create App Runner service pointing to ECR
4. Configure auto-scaling and health checks

### Method 2: GitHub + App Runner
1. Push code to GitHub repository
2. Connect App Runner to GitHub
3. Configure build commands and runtime
4. Enable automatic deployments on push

## 📊 Success Metrics

### Functional Requirements
- ✅ `/respond` endpoint working
- ✅ CBT-style responses
- ✅ Guardrails preventing harmful advice
- ✅ Both deployment methods working

### Quality Metrics
- Response time < 3 seconds
- 99%+ uptime on App Runner
- Proper error handling
- Clean, maintainable code

## 🧪 Testing Strategy

### Backend Tests
- Unit tests for guardrails
- Integration tests for LLM service
- API endpoint testing
- Mock Anthropic API for testing

### Frontend Tests
- Component testing (if time permits)
- Manual UI testing
- Cross-browser compatibility

### Deployment Tests
- Health check endpoints
- Environment variable validation
- Service connectivity tests

## 📝 Documentation Plan

### README.md
- Quick start guide
- Local development setup
- Deployment instructions
- API documentation

### Technical Docs
- Architecture decisions
- Prompt engineering rationale
- Deployment troubleshooting
- Security considerations

## ⏱️ Timeline

**Day 1 (8 hours)**
- Backend development (4 hours)
- Frontend development (3 hours)
- Local testing (1 hour)

**Day 2 (6 hours)**
- Docker setup (2 hours)
- AWS ECR deployment (2 hours)
- GitHub deployment (2 hours)

**Day 3 (4 hours)**
- CI/CD setup (2 hours)
- Documentation (1 hour)
- Final testing (1 hour)

**Total: ~18 hours** (well within assignment scope)

## 🎁 Bonus Features

1. **Enhanced Frontend**: React-based chat interface
2. **GitHub Actions**: Automated deployments
3. **Structured Logging**: Request/response tracking with timestamps
4. **Health Monitoring**: Comprehensive health checks
5. **Error Handling**: Graceful degradation

This plan leverages modern development practices while meeting all assignment requirements efficiently.

---

## 🤖 Gemini's Feedback and Suggestions

This is a comprehensive and well-structured plan. The breakdown of phases, the technology stack, and the detailed directory structure are excellent. I will adopt this plan as the primary blueprint for the project, with a few minor refinements.

### Key Strengths Adopted

*   **TypeScript:** I agree that using TypeScript for the frontend is the best practice. We will proceed with a Vite + React + TypeScript setup.
*   **Detailed Testing:** The explicit strategy to mock the Anthropic API for backend tests is a crucial detail that we will implement.
*   **Structured Logging:** The `utils/logging.py` module is a good idea for maintaining clean and readable logs.

### Proposed Refinements

1.  **Styling Approach:** While CSS Modules provide excellent scoped styling, for the sake of rapid development and achieving a polished, modern UI quickly, I propose using a component library like **React-Bootstrap** or **MUI (Material-UI)**. This aligns with the goal of shipping a useful MVP fast and avoids building common components from scratch.

2.  **Directory Structure Simplification:** The proposed directory structure is very thorough. To maintain simplicity for this specific project scale, I suggest a slight consolidation:
    *   The `deployment/` and `docs/` directories can be merged into a comprehensive `README.md`. This centralizes all setup, deployment, and API documentation, which is often sufficient for a project of this size.
    *   Configuration files like `apprunner.yaml` can reside in the root of the `backend` directory, as they are specific to that part of the application.

### Final Plan

I will proceed by executing the plan laid out by Claude, incorporating the suggestions above. The core architecture, technology choices, and phased approach are sound. My next immediate step is to create the project's directory structure based on this refined plan.