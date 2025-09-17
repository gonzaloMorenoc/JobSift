#!/bin/bash

# Simple script to generate and set SECRET_KEY

echo "🔑 Generating SECRET_KEY for JobSift..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if backend/.env exists
if [[ ! -f "backend/.env" ]]; then
    echo -e "${YELLOW}⚠️  backend/.env not found, creating from example...${NC}"
    if [[ -f "backend/.env.example" ]]; then
        cp backend/.env.example backend/.env
        echo -e "${GREEN}✅ Created backend/.env${NC}"
    else
        echo "❌ backend/.env.example not found"
        exit 1
    fi
fi

# Generate SECRET_KEY
SECRET_KEY=""

# Try Python first
if command -v python3 &> /dev/null; then
    SECRET_KEY=$(python3 -c "import secrets, string; print(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32)))" 2>/dev/null || echo "")
fi

# Try OpenSSL if Python failed
if [[ -z "$SECRET_KEY" ]] && command -v openssl &> /dev/null; then
    SECRET_KEY=$(openssl rand -hex 16 2>/dev/null || echo "")
fi

# Fallback: manual generation
if [[ -z "$SECRET_KEY" ]]; then
    SECRET_KEY="JobSift$(date +%s)$(echo $RANDOM | md5sum | head -c 16)"
fi

if [[ -n "$SECRET_KEY" ]]; then
    # Update the .env file
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|your-super-secret-key-here-minimum-32-characters-long|$SECRET_KEY|g" backend/.env
    else
        # Linux
        sed -i "s|your-super-secret-key-here-minimum-32-characters-long|$SECRET_KEY|g" backend/.env
    fi
    
    echo -e "${GREEN}✅ SECRET_KEY generated and updated in backend/.env${NC}"
    echo -e "${BLUE}🔑 Generated key: ${SECRET_KEY:0:8}...${NC}"
else
    echo "❌ Failed to generate SECRET_KEY"
    exit 1
fi

echo -e "${GREEN}🎉 Ready to start JobSift!${NC}"
