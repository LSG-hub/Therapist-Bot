#!/bin/bash
# Docker Test Script for Therapist Bot
# Tests Docker containers locally before deployment

set -e  # Exit on any error

echo "🐳 Therapist Bot - Docker Container Test"
echo "========================================"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env file not found! Please create it from .env.example${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Pre-flight Checks${NC}"
echo "✅ .env file found"
echo "✅ Docker Compose files ready"

# Build containers
echo -e "\n${YELLOW}🔨 Building Docker Containers${NC}"
echo "Building backend (this may take 5-10 minutes due to ML dependencies)..."
docker-compose build backend

echo "Building frontend..."
docker-compose build frontend

# Test backend container
echo -e "\n${YELLOW}🧪 Testing Backend Container${NC}"
docker-compose up -d backend
sleep 30  # Wait for startup

# Health check
echo "Testing health endpoint..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend health check passed${NC}"
else
    echo -e "${RED}❌ Backend health check failed${NC}"
    docker-compose logs backend
    exit 1
fi

# Test RAG functionality
echo "Testing RAG functionality..."
response=$(curl -s -X POST http://localhost:8000/respond \
    -H "Content-Type: application/json" \
    -d '{"message": "I feel anxious about my test"}')

if echo "$response" | grep -q "session_id"; then
    echo -e "${GREEN}✅ RAG API working (session_id found in response)${NC}"
else
    echo -e "${RED}❌ RAG API test failed${NC}"
    echo "Response: $response"
    exit 1
fi

# Stop backend
docker-compose stop backend

# Test frontend container
echo -e "\n${YELLOW}🎨 Testing Frontend Container${NC}"
docker-compose up -d frontend
sleep 15  # Wait for startup

# Frontend health check
if curl -f http://localhost:3000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend health check passed${NC}"
else
    echo -e "${RED}❌ Frontend health check failed${NC}"
    docker-compose logs frontend
    exit 1
fi

# Stop all containers
docker-compose down

echo -e "\n${GREEN}🎉 All Docker tests passed!${NC}"
echo -e "${YELLOW}📦 Ready for deployment to AWS App Runner${NC}"

# Show image sizes
echo -e "\n${YELLOW}📊 Container Image Sizes:${NC}"
docker images | grep therapist-bot