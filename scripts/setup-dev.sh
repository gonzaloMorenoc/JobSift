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

# Detect OS for different sed syntax
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

# Universal Docker Compose function
get_docker_compose_cmd() {
    if command -v docker-compose &> /dev/null; then
        echo "docker-compose"
    elif docker compose version &> /dev/null 2>&1; then
        echo "docker compose"
    else
        echo "docker-compose"  # fallback
    fi
}

# Set the Docker Compose command globally
DOCKER_COMPOSE=$(get_docker_compose_cmd)

# Cross-platform sed function
safe_sed() {
    local pattern="$1"
    local replacement="$2"
    local file="$3"
    
    if [[ $(detect_os) == "macos" ]]; then
        sed -i '' "s|${pattern}|${replacement}|g" "$file"
    else
        sed -i "s|${pattern}|${replacement}|g" "$file"
    fi
}

# Error handling function
handle_error() {
    local exit_code=$1
    local line_number=$2
    echo -e "${RED}❌ Error occurred on line $line_number (exit code: $exit_code)${NC}"
    echo -e "${YELLOW}💡 Suggestions:${NC}"
    echo "1. Make sure Docker is running"
    echo "2. Check that you have Python 3.11+ installed"
    echo "3. Try running: make clean && make quickstart"
    echo "4. For Docker-only setup: make dev-docker"
    exit $exit_code
}

# Set up error trapping
trap 'handle_error $? $LINENO' ERR

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker Desktop and try again.${NC}"
    exit 1
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
    
    # Generate a secure secret key (cross-platform)
    if command -v python3 &> /dev/null; then
        SECRET_KEY=$(python3 -c "import secrets, string; print(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32)))" 2>/dev/null || echo "")
        if [[ -n "$SECRET_KEY" ]]; then
            safe_sed "your-super-secret-key-here-minimum-32-characters-long" "$SECRET_KEY" "backend/.env"
            echo -e "${GREEN}✅ Generated secure SECRET_KEY${NC}"
        fi
    elif command -v openssl &> /dev/null; then
        # Use openssl with safer character set
        SECRET_KEY=$(openssl rand -hex 16 2>/dev/null || echo "")  # 32 hex chars = 16 bytes
        if [[ -n "$SECRET_KEY" ]]; then
            safe_sed "your-super-secret-key-here-minimum-32-characters-long" "$SECRET_KEY" "backend/.env"
            echo -e "${GREEN}✅ Generated secure SECRET_KEY${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Neither Python3 nor OpenSSL found. Using default SECRET_KEY${NC}"
        echo -e "${YELLOW}⚠️  Please update SECRET_KEY in backend/.env for production${NC}"
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

# Generate package-lock.json if missing
echo -e "${BLUE}📦 Preparing frontend dependencies...${NC}"
chmod +x scripts/generate-lockfile.sh
./scripts/generate-lockfile.sh

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
        echo -e "${YELLOW}📋 Database logs:${NC}"
        $DOCKER_COMPOSE logs db
        exit 1
    fi
    echo -e "${YELLOW}⏳ Database not ready yet... (attempt $attempt/$max_attempts)${NC}"
    sleep 2
    ((attempt++))
done

echo -e "${GREEN}✅ Database is ready${NC}"

# Install backend dependencies (with better error handling)
if [[ -d "backend" ]] && command -v python3 &> /dev/null; then
    echo -e "${BLUE}🐍 Installing Python dependencies...${NC}"
    
    # Save current directory
    ORIGINAL_DIR=$(pwd)
    
    cd backend
    
    # Check Python version
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "unknown")
    echo -e "${BLUE}📍 Python version: $python_version${NC}"
    
    # Check if virtual environment exists
    if [[ ! -d "venv" ]]; then
        echo -e "${BLUE}📦 Creating Python virtual environment...${NC}"
        if ! python3 -m venv venv; then
            echo -e "${RED}❌ Failed to create virtual environment${NC}"
            echo -e "${YELLOW}💡 Try: python3 -m pip install --user virtualenv${NC}"
            cd "$ORIGINAL_DIR"
            exit 1
        fi
    fi
    
    # Activate virtual environment and install dependencies
    echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
    if ! source venv/bin/activate; then
        echo -e "${RED}❌ Failed to activate virtual environment${NC}"
        cd "$ORIGINAL_DIR"
        exit 1
    fi
    
    echo -e "${BLUE}📦 Upgrading pip...${NC}"
    if ! pip install --upgrade pip > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Failed to upgrade pip, continuing...${NC}"
    fi
    
    echo -e "${BLUE}📦 Installing requirements...${NC}"
    if ! pip install -r requirements.txt; then
        echo -e "${RED}❌ Failed to install Python dependencies${NC}"
        echo -e "${YELLOW}💡 Try: pip install -r requirements.txt --verbose${NC}"
        deactivate
        cd "$ORIGINAL_DIR"
        exit 1
    fi
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
    
    # Run database migrations
    echo -e "${BLUE}🔄 Running database migrations...${NC}"
    if ! alembic upgrade head; then
        echo -e "${RED}❌ Failed to run database migrations${NC}"
        echo -e "${YELLOW}💡 Check database connection and alembic configuration${NC}"
        deactivate
        cd "$ORIGINAL_DIR"
        exit 1
    fi
    echo -e "${GREEN}✅ Database migrations completed${NC}"
    
    # Seed database with demo data
    echo -e "${BLUE}🌱 Seeding database with demo data...${NC}"
    if ! python scripts/seed_data.py; then
        echo -e "${RED}❌ Failed to seed database${NC}"
        echo -e "${YELLOW}💡 Check scripts/seed_data.py and database connection${NC}"
        deactivate
        cd "$ORIGINAL_DIR"
        exit 1
    fi
    echo -e "${GREEN}✅ Database seeded with demo data${NC}"
    
    deactivate
    cd "$ORIGINAL_DIR"
else
    echo -e "${YELLOW}⚠️  Python3 not found or backend directory missing${NC}"
    echo -e "${YELLOW}💡 Using Docker-only setup...${NC}"
fi

# Install frontend dependencies (if running locally)
if [[ -d "frontend" ]] && command -v npm &> /dev/null; then
    echo -e "${BLUE}📦 Installing Node.js dependencies...${NC}"
    cd frontend
    if npm install > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Node.js dependencies installed${NC}"
    else
        echo -e "${YELLOW}⚠️  Failed to install Node.js dependencies${NC}"
        echo -e "${YELLOW}💡 Try: npm install --verbose${NC}"
    fi
    cd ..
else
    echo -e "${YELLOW}⚠️  npm not found or frontend directory missing${NC}"
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
echo "   Docker development: make dev-docker"
echo "   Local development: make dev"
echo "   Health check: make health"
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

# Optional: Open browser (cross-platform)
echo -e "${BLUE}🌐 Opening application in browser...${NC}"
case $(detect_os) in
    "macos")
        if command -v open &> /dev/null; then
            open http://localhost:5173 > /dev/null 2>&1 &
        fi
        ;;
    "linux")
        if command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:5173 > /dev/null 2>&1 &
        elif command -v firefox &> /dev/null; then
            firefox http://localhost:5173 > /dev/null 2>&1 &
        elif command -v chromium-browser &> /dev/null; then
            chromium-browser http://localhost:5173 > /dev/null 2>&1 &
        fi
        ;;
    *)
        echo "Please open http://localhost:5173 in your browser"
        ;;
esac

echo -e "${GREEN}Happy coding! 🚀${NC}"
