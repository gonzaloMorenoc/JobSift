#!/bin/bash

# Script to generate package-lock.json if missing

echo "📦 Checking frontend dependencies..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if we're in the right directory
if [[ ! -f "frontend/package.json" ]]; then
    echo "❌ frontend/package.json not found. Run this from the project root."
    exit 1
fi

cd frontend

# Check if package-lock.json exists
if [[ -f "package-lock.json" ]]; then
    echo -e "${GREEN}✅ package-lock.json already exists${NC}"
    exit 0
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo -e "${YELLOW}⚠️  npm not found. Cannot generate package-lock.json${NC}"
    echo "The Docker build will use npm install instead"
    exit 0
fi

echo -e "${BLUE}📦 Generating package-lock.json...${NC}"

# Clean install to generate package-lock.json
if npm install > /dev/null 2>&1; then
    echo -e "${GREEN}✅ package-lock.json generated successfully${NC}"
    echo -e "${BLUE}📋 Node modules installed in frontend/node_modules${NC}"
else
    echo -e "${YELLOW}⚠️  Failed to generate package-lock.json${NC}"
    echo "Docker build will still work with npm install"
fi

cd ..
