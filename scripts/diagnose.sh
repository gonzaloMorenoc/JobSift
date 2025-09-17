#!/bin/bash

# JobSift Diagnostic Script
# This script helps identify setup issues

echo "🔍 JobSift Diagnostic Report"
echo "============================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# System Information
echo -e "\n${BLUE}🖥️  System Information${NC}"
echo "OS: $(uname -s) $(uname -r)"
echo "Architecture: $(uname -m)"

# Docker Information
echo -e "\n${BLUE}🐳 Docker Information${NC}"
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed"
    docker --version
    if docker info > /dev/null 2>&1; then
        echo "✅ Docker is running"
    else
        echo "❌ Docker is not running"
    fi
else
    echo "❌ Docker is not installed"
fi

# Docker Compose Information
echo -e "\n${BLUE}🔧 Docker Compose Information${NC}"
if command -v docker-compose &> /dev/null; then
    echo "✅ docker-compose is available"
    docker-compose --version
elif docker compose version &> /dev/null 2>&1; then
    echo "✅ docker compose is available"
    docker compose version
else
    echo "❌ Neither docker-compose nor docker compose is available"
fi

# Python Information
echo -e "\n${BLUE}🐍 Python Information${NC}"
if command -v python3 &> /dev/null; then
    echo "✅ Python3 is installed"
    python3 --version
    
    # Check if venv module is available
    if python3 -m venv --help > /dev/null 2>&1; then
        echo "✅ venv module is available"
    else
        echo "❌ venv module is not available"
    fi
    
    # Check pip
    if python3 -m pip --version > /dev/null 2>&1; then
        echo "✅ pip is available"
        python3 -m pip --version
    else
        echo "❌ pip is not available"
    fi
else
    echo "❌ Python3 is not installed"
fi

# Node.js Information
echo -e "\n${BLUE}📦 Node.js Information${NC}"
if command -v node &> /dev/null; then
    echo "✅ Node.js is installed"
    node --version
else
    echo "❌ Node.js is not installed"
fi

if command -v npm &> /dev/null; then
    echo "✅ npm is available"
    npm --version
else
    echo "❌ npm is not available"
fi

# Project Files
echo -e "\n${BLUE}📁 Project Files${NC}"
required_files=(
    "docker-compose.yml"
    "Makefile"
    "backend/.env.example"
    "frontend/.env.example"
    "backend/requirements.txt"
    "frontend/package.json"
)

all_files_present=true
for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
        all_files_present=false
    fi
done

# Environment files
echo -e "\n${BLUE}⚙️  Environment Files${NC}"
if [[ -f "backend/.env" ]]; then
    echo "✅ backend/.env exists"
    # Check if SECRET_KEY is set
    if grep -q "your-super-secret-key-here-minimum-32-characters-long" backend/.env; then
        echo "⚠️  SECRET_KEY needs to be updated"
    else
        echo "✅ SECRET_KEY appears to be set"
    fi
else
    echo "❌ backend/.env missing"
fi

if [[ -f "frontend/.env" ]]; then
    echo "✅ frontend/.env exists"
else
    echo "❌ frontend/.env missing"
fi

# Docker Containers Status
echo -e "\n${BLUE}🐳 Container Status${NC}"
if command -v docker &> /dev/null && docker info > /dev/null 2>&1; then
    DOCKER_COMPOSE="docker-compose"
    if ! command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE="docker compose"
    fi
    
    containers=$($DOCKER_COMPOSE ps -q 2>/dev/null || echo "")
    if [[ -n "$containers" ]]; then
        echo "Running containers:"
        $DOCKER_COMPOSE ps
    else
        echo "No containers running"
    fi
else
    echo "Cannot check container status (Docker not available)"
fi

# Port availability
echo -e "\n${BLUE}🔌 Port Availability${NC}"
ports=(5173 8000 5432)
for port in "${ports[@]}"; do
    if lsof -i :$port > /dev/null 2>&1; then
        process=$(lsof -i :$port | grep LISTEN | awk '{print $1}' | head -1)
        echo "⚠️  Port $port is in use by $process"
    else
        echo "✅ Port $port is available"
    fi
done

# Disk space
echo -e "\n${BLUE}💾 Disk Space${NC}"
df -h . | awk 'NR==2 {print "Available:", $4, "Used:", $5}'

# Recommendations
echo -e "\n${BLUE}💡 Recommendations${NC}"

if ! command -v docker &> /dev/null; then
    echo "📖 Install Docker Desktop: https://docs.docker.com/get-docker/"
fi

if ! command -v python3 &> /dev/null; then
    echo "🐍 Install Python 3.11+: https://www.python.org/downloads/"
fi

if ! command -v node &> /dev/null; then
    echo "📦 Install Node.js 18+: https://nodejs.org/"
fi

if [[ "$all_files_present" == false ]]; then
    echo "📁 Ensure you're in the correct project directory"
fi

echo -e "\n${BLUE}🚀 Quick Solutions${NC}"
echo "1. For Docker-only setup: make quickstart-simple"
echo "2. Clean start: make clean && make quickstart-simple"
echo "3. Manual setup: make setup && make dev-docker"
echo "4. View logs: make logs"

echo -e "\n${GREEN}✅ Diagnostic completed!${NC}"
