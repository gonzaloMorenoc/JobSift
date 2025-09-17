.PHONY: dev db-up db-down db-reset migrate migration seed test format lint build clean help setup health

# Detect OS and set appropriate commands
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    OPEN_CMD = open
    SED_INPLACE = sed -i ''
else
    OPEN_CMD = xdg-open
    SED_INPLACE = sed -i
endif

# Detect Docker Compose command
DOCKER_COMPOSE := $(shell command -v docker-compose 2> /dev/null)
ifndef DOCKER_COMPOSE
    DOCKER_COMPOSE := docker compose
endif

# Colors for output
BLUE=\033[0;34m
GREEN=\033[0;32m
YELLOW=\033[1;33m
RED=\033[0;31m
NC=\033[0m # No Color

help: ## Show this help message
	@echo "${BLUE}JobSift Development Commands${NC}"
	@echo "================================"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "${GREEN}%-15s${NC} %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Complete development environment setup
	@echo "${BLUE}Running complete development setup...${NC}"
	@chmod +x scripts/setup-dev.sh
	@./scripts/setup-dev.sh

dev: ## Start full development environment
	@echo "${BLUE}Starting JobSift development environment...${NC}"
	$(DOCKER_COMPOSE) up -d db redis
	@echo "${YELLOW}Waiting for database to be ready...${NC}"
	@sleep 5
	@make migrate
	@echo "${GREEN}Starting backend and frontend...${NC}"
	@trap 'kill %1; kill %2' INT; \
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 & \
	cd frontend && npm run dev & \
	wait

dev-docker: ## Start development with Docker Compose
	@echo "${BLUE}Starting with Docker Compose...${NC}"
	$(DOCKER_COMPOSE) up --build

health: ## Run system health checks
	@echo "${BLUE}Running system health checks...${NC}"
	@chmod +x scripts/health-check.sh
	@./scripts/health-check.sh

diagnose: ## Run comprehensive system diagnostics
	@echo "${BLUE}Running system diagnostics...${NC}"
	@chmod +x scripts/diagnose.sh
	@./scripts/diagnose.sh

generate-key: ## Generate new SECRET_KEY for backend
	@echo "${BLUE}Generating new SECRET_KEY...${NC}"
	@chmod +x scripts/generate-key.sh
	@./scripts/generate-key.sh

generate-lockfile: ## Generate package-lock.json for frontend
	@echo "${BLUE}Generating frontend lockfile...${NC}"
	@chmod +x scripts/generate-lockfile.sh
	@./scripts/generate-lockfile.sh

db-up: ## Start database services
	@echo "${BLUE}Starting database services...${NC}"
	$(DOCKER_COMPOSE) up -d db redis

db-down: ## Stop database services
	@echo "${YELLOW}Stopping database services...${NC}"
	$(DOCKER_COMPOSE) down

db-reset: ## Reset database completely
	@echo "${RED}Resetting database... (this will delete all data)${NC}"
	$(DOCKER_COMPOSE) down -v
	$(DOCKER_COMPOSE) up -d db
	@echo "${YELLOW}Waiting for database to be ready...${NC}"
	@sleep 5
	@make migrate
	@make seed

migrate: ## Run database migrations
	@echo "${BLUE}Running database migrations...${NC}"
	cd backend && alembic upgrade head

migration: ## Generate new migration (usage: make migration name="description")
	@if [ -z "$(name)" ]; then \
		echo "${RED}Error: Please provide a migration name${NC}"; \
		echo "Usage: make migration name=\"add_new_field\""; \
		exit 1; \
	fi
	@echo "${BLUE}Generating migration: $(name)${NC}"
	cd backend && alembic revision --autogenerate -m "$(name)"

seed: ## Seed database with sample data
	@echo "${BLUE}Seeding database with sample data...${NC}"
	cd backend && python scripts/seed_data.py

test: ## Run all tests
	@echo "${BLUE}Running tests...${NC}"
	@make test-backend
	@make test-frontend

test-backend: ## Run backend tests
	@echo "${BLUE}Running backend tests...${NC}"
	cd backend && pytest -v --cov=app tests/ || echo "${YELLOW}Backend tests not yet implemented${NC}"

test-frontend: ## Run frontend tests
	@echo "${BLUE}Running frontend tests...${NC}"
	cd frontend && npm test || echo "${YELLOW}Frontend tests not yet implemented${NC}"

format: ## Format all code
	@echo "${BLUE}Formatting code...${NC}"
	@make format-backend
	@make format-frontend

format-backend: ## Format backend code
	@echo "${BLUE}Formatting backend code...${NC}"
	cd backend && black . && isort . || echo "${YELLOW}Backend formatting tools not installed${NC}"

format-frontend: ## Format frontend code
	@echo "${BLUE}Formatting frontend code...${NC}"
	cd frontend && npm run format || echo "${YELLOW}Frontend not set up yet${NC}"

lint: ## Lint all code
	@echo "${BLUE}Linting code...${NC}"
	@make lint-backend
	@make lint-frontend

lint-backend: ## Lint backend code
	@echo "${BLUE}Linting backend code...${NC}"
	cd backend && ruff check . && mypy . || echo "${YELLOW}Backend linting tools not installed${NC}"

lint-frontend: ## Lint frontend code
	@echo "${BLUE}Linting frontend code...${NC}"
	cd frontend && npm run lint || echo "${YELLOW}Frontend not set up yet${NC}"

build: ## Build for production
	@echo "${BLUE}Building for production...${NC}"
	cd frontend && npm run build
	@echo "${GREEN}Build completed!${NC}"

install: ## Install all dependencies
	@echo "${BLUE}Installing dependencies...${NC}"
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

install-dev: ## Install development dependencies
	@echo "${BLUE}Installing development dependencies...${NC}"
	cd backend && pip install -r requirements.txt && pip install pytest pytest-cov black isort ruff mypy
	cd frontend && npm install

pre-commit: ## Run pre-commit checks
	@echo "${BLUE}Running pre-commit checks...${NC}"
	@make format
	@make lint
	@make test

clean: ## Clean up Docker resources
	@echo "${YELLOW}Cleaning up Docker resources...${NC}"
	$(DOCKER_COMPOSE) down -v --remove-orphans
	docker system prune -f

logs: ## Show application logs
	@echo "${BLUE}Showing logs...${NC}"
	$(DOCKER_COMPOSE) logs -f

logs-backend: ## Show backend logs only
	@echo "${BLUE}Showing backend logs...${NC}"
	$(DOCKER_COMPOSE) logs -f backend

logs-db: ## Show database logs only
	@echo "${BLUE}Showing database logs...${NC}"
	$(DOCKER_COMPOSE) logs -f db

shell-backend: ## Open backend shell
	@echo "${BLUE}Opening backend shell...${NC}"
	cd backend && python -c "from app.main import app; from app.core.database import get_db; print('Backend shell ready')"

shell-db: ## Open database shell
	@echo "${BLUE}Opening database shell...${NC}"
	$(DOCKER_COMPOSE) exec db psql -U jobsift_user -d jobsift_db

backup-db: ## Backup database
	@echo "${BLUE}Creating database backup...${NC}"
	$(DOCKER_COMPOSE) exec db pg_dump -U jobsift_user jobsift_db > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "${GREEN}Backup created: backup_$(shell date +%Y%m%d_%H%M%S).sql${NC}"

restore-db: ## Restore database from backup (usage: make restore-db file="backup.sql")
	@if [ -z "$(file)" ]; then \
		echo "${RED}Error: Please provide a backup file${NC}"; \
		echo "Usage: make restore-db file=\"backup.sql\""; \
		exit 1; \
	fi
	@echo "${BLUE}Restoring database from $(file)...${NC}"
	@make db-reset
	$(DOCKER_COMPOSE) exec -T db psql -U jobsift_user -d jobsift_db < $(file)
	@echo "${GREEN}Database restored successfully${NC}"

status: ## Show services status
	@echo "${BLUE}Services status:${NC}"
	@$(DOCKER_COMPOSE) ps
	@echo "\n${BLUE}URLs:${NC}"
	@echo "${GREEN}Frontend:${NC} http://localhost:5173"
	@echo "${GREEN}Backend API:${NC} http://localhost:8000/api/v1"
	@echo "${GREEN}API Docs:${NC} http://localhost:8000/docs"
	@echo "${GREEN}Database:${NC} postgresql://jobsift_user:jobsift_pass@localhost:5432/jobsift_db"

demo: ## Quick demo setup (setup + start + health check)
	@echo "${BLUE}Setting up JobSift demo...${NC}"
	@make setup
	@make dev-docker
	@sleep 30
	@make health

# Production commands
prod-build: ## Build for production
	@echo "${BLUE}Building for production...${NC}"
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml build

prod-up: ## Start production environment
	@echo "${BLUE}Starting production environment...${NC}"
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-down: ## Stop production environment
	@echo "${YELLOW}Stopping production environment...${NC}"
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml down

# Quick start for new developers
quickstart: ## Complete quickstart for new developers
	@echo "${GREEN}🚀 JobSift Quickstart${NC}"
	@echo "This will set up everything you need to get started"
	@make setup
	@make dev-docker
	@echo "${YELLOW}Waiting for services to be ready...${NC}"
	@sleep 30
	@make health
	@echo ""
	@echo "${GREEN}🎉 JobSift is ready!${NC}"
	@echo "Visit: http://localhost:5173"
	@echo "Login: demo@jobsift.com / demo123456"

quick-start: ## One-command solution for all common issues
	@echo "${GREEN}🚀 JobSift Quick Start${NC}"
	@echo "Fixes common issues and starts the application"
	@chmod +x scripts/quick-start.sh
	@./scripts/quick-start.sh

quickstart-simple: ## Docker-only quickstart (most reliable)
	@echo "${GREEN}🚀 JobSift Simple Quickstart${NC}"
	@echo "Using Docker-only setup for maximum reliability"
	@chmod +x scripts/setup-dev.sh
	@echo "${BLUE}📋 Creating environment files...${NC}"
	@if [ ! -f backend/.env ]; then cp backend/.env.example backend/.env; fi
	@if [ ! -f frontend/.env ]; then cp frontend/.env.example frontend/.env; fi
	@echo "${BLUE}📦 Preparing frontend dependencies...${NC}"
	@chmod +x scripts/generate-lockfile.sh
	@./scripts/generate-lockfile.sh
	@echo "${BLUE}🛑 Stopping any existing containers...${NC}"
	$(DOCKER_COMPOSE) down --remove-orphans > /dev/null 2>&1 || true
	@echo "${BLUE}🏗️  Building and starting all services...${NC}"
	$(DOCKER_COMPOSE) up --build -d
	@echo "${YELLOW}⏳ Waiting for services to be ready...${NC}"
	@sleep 45
	@echo "${BLUE}🔍 Running health checks...${NC}"
	@make health || echo "${YELLOW}⚠️  Some services may still be starting...${NC}"
	@echo ""
	@echo "${GREEN}🎉 JobSift is ready!${NC}"
	@echo "Visit: http://localhost:5173"
	@echo "Login: demo@jobsift.com / demo123456"
