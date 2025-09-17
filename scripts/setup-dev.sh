#!/bin/bash

# JobSift Development Setup Script
# Run this script to set up your development environment

set -e

echo "🚀 Setting up JobSift development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker Desktop and try again.${NC}"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  docker-compose not found, trying docker compose...${NC}"
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo -e "${BLUE}📋 Checking requirements...${NC}"

# Check if required files exist
required_files=(
    "backend/.env.example"
    "frontend/.env.example"
    "docker-compose.yml"
)

for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo -e "${RED}❌ Required file $file not found${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ All required files found${NC}"

# Create environment files if they don't exist
echo -e "${BLUE}📝 Setting up environment files...${NC}"

if [[ ! -f "backend/.env" ]]; then
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✅ Created backend/.env from example${NC}"
    
    # Generate a secure secret key
    if command -v openssl &> /dev/null; then
        SECRET_KEY=$(openssl rand -base64 32)
        # Replace the placeholder secret key in the .env file
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/your-super-secret-key-here-minimum-32-characters-long/$SECRET_KEY/" backend/.env
        else
            # Linux
            sed -i "s/your-super-secret-key-here-minimum-32-characters-long/$SECRET_KEY/" backend/.env
        fi
        echo -e "${GREEN}✅ Generated secure SECRET_KEY${NC}"
    else
        echo -e "${YELLOW}⚠️  OpenSSL not found. Please manually update SECRET_KEY in backend/.env${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  backend/.env already exists, skipping...${NC}"
fi

if [[ ! -f "frontend/.env" ]]; then
    cp frontend/.env.example frontend/.env
    echo -e "${GREEN}✅ Created frontend/.env from example${NC}"
else
    echo -e "${YELLOW}⚠️  frontend/.env already exists, skipping...${NC}"
fi

# Stop any existing containers
echo -e "${BLUE}🛑 Stopping any existing containers...${NC}"
$DOCKER_COMPOSE down --remove-orphans > /dev/null 2>&1 || true

# Build and start the database
echo -e "${BLUE}🗄️  Starting PostgreSQL database...${NC}"
$DOCKER_COMPOSE up -d db

# Wait for database to be ready
echo -e "${YELLOW}⏳ Waiting for database to be ready...${NC}"
sleep 10

# Check if database is ready
max_attempts=30
attempt=1
while ! $DOCKER_COMPOSE exec -T db pg_isready -U jobsift_user -d jobsift_db > /dev/null 2>&1; do
    if [[ $attempt -eq $max_attempts ]]; then
        echo -e "${RED}❌ Database failed to start after $max_attempts attempts${NC}"
        $DOCKER_COMPOSE logs db
        exit 1
    fi
    echo -e "${YELLOW}⏳ Database not ready yet... (attempt $attempt/$max_attempts)${NC}"
    sleep 2
    ((attempt++))
done

echo -e "${GREEN}✅ Database is ready${NC}"

# Install backend dependencies (if running locally)
if [[ -d "backend" ]] && command -v python3 &> /dev/null; then
    echo -e "${BLUE}🐍 Installing Python dependencies...${NC}"
    cd backend
    
    # Check if virtual environment exists
    if [[ ! -d "venv" ]]; then
        echo -e "${BLUE}📦 Creating Python virtual environment...${NC}"
        python3 -m venv venv
    fi
    
    # Activate virtual environment and install dependencies
    source venv/bin/activate
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt > /dev/null 2>&1
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
    
    # Run database migrations
    echo -e "${BLUE}🔄 Running database migrations...${NC}"
    alembic upgrade head
    echo -e "${GREEN}✅ Database migrations completed${NC}"
    
    # Seed database with demo data
    echo -e "${BLUE}🌱 Seeding database with demo data...${NC}"
    python scripts/seed_data.py
    echo -e "${GREEN}✅ Database seeded with demo data${NC}"
    
    deactivate
    cd ..
fi

# Install frontend dependencies (if running locally)
if [[ -d "frontend" ]] && command -v npm &> /dev/null; then
    echo -e "${BLUE}📦 Installing Node.js dependencies...${NC}"
    cd frontend
    npm install > /dev/null 2>&1
    echo -e "${GREEN}✅ Node.js dependencies installed${NC}"
    cd ..
fi

# Final setup message
echo ""
echo -e "${GREEN}🎉 JobSift development environment is ready!${NC}"
echo ""
echo -e "${BLUE}📝 Demo Credentials:${NC}"
echo "   Email: demo@jobsift.com"
echo "   Password: demo123456"
echo ""
echo -e "${BLUE}🚀 To start the application:${NC}"
echo "   Local development: make dev"
echo "   Docker development: make dev-docker"
echo ""
echo -e "${BLUE}🌐 URLs:${NC}"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Database: postgresql://jobsift_user:jobsift_pass@localhost:5432/jobsift_db"
echo ""
echo -e "${BLUE}📚 Useful commands:${NC}"
echo "   make help          - Show all available commands"
echo "   make test          - Run tests"
echo "   make format        - Format code"
echo "   make seed          - Re-seed database"
echo "   make logs          - Show application logs"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
