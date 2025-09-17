#!/bin/bash

# JobSift Quick Fix & Start Script
# This script fixes common issues and starts the application

set -e

echo "🔧 JobSift Quick Fix & Start"
echo "============================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Fix permissions
echo -e "${BLUE}🔧 Fixing script permissions...${NC}"
chmod +x scripts/*.sh 2>/dev/null || true

# Create environment files
echo -e "${BLUE}📋 Setting up environment files...${NC}"
if [[ ! -f "backend/.env" ]]; then
    if [[ -f "backend/.env.example" ]]; then
        cp backend/.env.example backend/.env
        echo -e "${GREEN}✅ Created backend/.env${NC}"
    else
        echo -e "${RED}❌ backend/.env.example not found${NC}"
        exit 1
    fi
fi

if [[ ! -f "frontend/.env" ]]; then
    if [[ -f "frontend/.env.example" ]]; then
        cp frontend/.env.example frontend/.env
        echo -e "${GREEN}✅ Created frontend/.env${NC}"
    else
        echo -e "${RED}❌ frontend/.env.example not found${NC}"
        exit 1
    fi
fi

# Generate SECRET_KEY
echo -e "${BLUE}🔑 Generating SECRET_KEY...${NC}"
./scripts/generate-key.sh

# Generate package-lock.json
echo -e "${BLUE}📦 Preparing frontend dependencies...${NC}"
./scripts/generate-lockfile.sh

# Stop any existing containers
echo -e "${BLUE}🛑 Cleaning up existing containers...${NC}"
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

$DOCKER_COMPOSE down --remove-orphans -v > /dev/null 2>&1 || true

# Start fresh
echo -e "${BLUE}🏗️  Building and starting all services...${NC}"
$DOCKER_COMPOSE up --build -d

echo -e "${YELLOW}⏳ Waiting for services to start...${NC}"
sleep 30

# Quick health check
echo -e "${BLUE}🔍 Quick health check...${NC}"
backend_ready=false
frontend_ready=false

# Check backend
for i in {1..10}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        backend_ready=true
        break
    fi
    sleep 3
done

# Check frontend
for i in {1..10}; do
    if curl -s http://localhost:5173 > /dev/null 2>&1; then
        frontend_ready=true
        break
    fi
    sleep 3
done

# Results
echo ""
echo -e "${BLUE}📊 Status Report:${NC}"
if [[ "$backend_ready" == true ]]; then
    echo -e "${GREEN}✅ Backend: Ready (http://localhost:8000)${NC}"
else
    echo -e "${YELLOW}⚠️  Backend: Starting... (may take a few more minutes)${NC}"
fi

if [[ "$frontend_ready" == true ]]; then
    echo -e "${GREEN}✅ Frontend: Ready (http://localhost:5173)${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend: Starting... (may take a few more minutes)${NC}"
fi

echo ""
echo -e "${GREEN}🎉 JobSift Quick Start Complete!${NC}"
echo ""
echo -e "${BLUE}🌐 Access URLs:${NC}"
echo "   • Frontend: http://localhost:5173"
echo "   • Backend API: http://localhost:8000"
echo "   • API Docs: http://localhost:8000/docs"
echo ""
echo -e "${BLUE}🔑 Demo Login:${NC}"
echo "   • Email: demo@jobsift.com"
echo "   • Password: demo123456"
echo ""
echo -e "${BLUE}📋 Useful Commands:${NC}"
echo "   • Check status: make status"
echo "   • View logs: make logs"
echo "   • Full health check: make health"
echo "   • Restart: make clean && ./scripts/quick-start.sh"

# Open browser if available
if command -v open &> /dev/null; then
    echo -e "${BLUE}🌐 Opening browser...${NC}"
    open http://localhost:5173 > /dev/null 2>&1 &
elif command -v xdg-open &> /dev/null; then
    echo -e "${BLUE}🌐 Opening browser...${NC}"
    xdg-open http://localhost:5173 > /dev/null 2>&1 &
fi

echo -e "${GREEN}🚀 Happy coding!${NC}"
