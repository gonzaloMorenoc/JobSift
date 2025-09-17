#!/bin/bash

# JobSift MVP Completeness Check
# This script verifies all required components are in place

echo "🔍 JobSift MVP Completeness Check"
echo "================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
total_checks=0
passed_checks=0
failed_checks=0

check_file() {
    total_checks=$((total_checks + 1))
    if [[ -f "$1" ]]; then
        echo -e "${GREEN}✅ $1${NC}"
        passed_checks=$((passed_checks + 1))
        return 0
    else
        echo -e "${RED}❌ $1 (missing)${NC}"
        failed_checks=$((failed_checks + 1))
        return 1
    fi
}

check_dir() {
    total_checks=$((total_checks + 1))
    if [[ -d "$1" ]]; then
        echo -e "${GREEN}✅ $1/ (directory)${NC}"
        passed_checks=$((passed_checks + 1))
        return 0
    else
        echo -e "${RED}❌ $1/ (directory missing)${NC}"
        failed_checks=$((failed_checks + 1))
        return 1
    fi
}

# Root files
echo -e "\n${BLUE}📁 Root Configuration Files${NC}"
check_file "README.md"
check_file "Makefile"
check_file "docker-compose.yml"
check_file ".gitignore"
check_file ".pre-commit-config.yaml"

# Backend structure
echo -e "\n${BLUE}🔧 Backend Structure${NC}"
check_dir "backend"
check_file "backend/Dockerfile"
check_file "backend/requirements.txt"
check_file "backend/requirements-dev.txt"
check_file "backend/pyproject.toml"
check_file "backend/.env.example"
check_file "backend/alembic.ini"

# Backend application
echo -e "\n${BLUE}🚀 Backend Application${NC}"
check_file "backend/app/__init__.py"
check_file "backend/app/main.py"

# Backend core
check_dir "backend/app/core"
check_file "backend/app/core/__init__.py"
check_file "backend/app/core/config.py"
check_file "backend/app/core/database.py"
check_file "backend/app/core/security.py"

# Backend models
check_dir "backend/app/models"
check_file "backend/app/models/__init__.py"
check_file "backend/app/models/user.py"
check_file "backend/app/models/interview.py"
check_file "backend/app/models/calendar_event.py"

# Backend repositories
check_dir "backend/app/repositories"
check_file "backend/app/repositories/__init__.py"
check_file "backend/app/repositories/base.py"
check_file "backend/app/repositories/user.py"
check_file "backend/app/repositories/interview.py"
check_file "backend/app/repositories/calendar_event.py"

# Backend services
check_dir "backend/app/services"
check_file "backend/app/services/__init__.py"
check_file "backend/app/services/auth.py"
check_file "backend/app/services/interview.py"
check_file "backend/app/services/dashboard.py"
check_file "backend/app/services/calendar.py"

# Backend schemas
check_dir "backend/app/schemas"
check_file "backend/app/schemas/__init__.py"
check_file "backend/app/schemas/user.py"
check_file "backend/app/schemas/interview.py"
check_file "backend/app/schemas/dashboard.py"
check_file "backend/app/schemas/calendar.py"

# Backend API
check_dir "backend/app/api"
check_file "backend/app/api/__init__.py"
check_file "backend/app/api/deps.py"
check_dir "backend/app/api/v1"
check_file "backend/app/api/v1/__init__.py"
check_file "backend/app/api/v1/auth.py"
check_file "backend/app/api/v1/interviews.py"
check_file "backend/app/api/v1/dashboard.py"
check_file "backend/app/api/v1/calendar.py"

# Backend migrations
check_dir "backend/alembic"
check_file "backend/alembic/env.py"
check_file "backend/alembic/script.py.mako"
check_dir "backend/alembic/versions"
check_file "backend/alembic/versions/001_initial_migration.py"

# Backend scripts
check_dir "backend/scripts"
check_file "backend/scripts/seed_data.py"

# Backend tests
check_dir "backend/tests"
check_file "backend/tests/conftest.py"
check_file "backend/tests/test_main.py"
check_file "backend/tests/test_auth.py"
check_file "backend/tests/test_interviews.py"
check_file "backend/tests/test_dashboard.py"
check_file "backend/pytest.ini"

# Frontend structure
echo -e "\n${BLUE}🎨 Frontend Structure${NC}"
check_dir "frontend"
check_file "frontend/Dockerfile"
check_file "frontend/package.json"
check_file "frontend/tsconfig.json"
check_file "frontend/tsconfig.node.json"
check_file "frontend/vite.config.ts"
check_file "frontend/tailwind.config.js"
check_file "frontend/postcss.config.js"
check_file "frontend/index.html"
check_file "frontend/.env.example"

# Frontend source
echo -e "\n${BLUE}⚛️ Frontend Application${NC}"
check_dir "frontend/src"
check_file "frontend/src/main.tsx"
check_file "frontend/src/App.tsx"
check_file "frontend/src/vite-env.d.ts"

# Frontend components
check_dir "frontend/src/components"
check_dir "frontend/src/components/ui"
check_file "frontend/src/components/ui/button.tsx"
check_file "frontend/src/components/ui/card.tsx"
check_file "frontend/src/components/ui/input.tsx"
check_file "frontend/src/components/ui/badge.tsx"
check_file "frontend/src/components/ui/alert.tsx"
check_file "frontend/src/components/ui/select.tsx"
check_file "frontend/src/components/ui/label.tsx"

check_dir "frontend/src/components/common"
check_file "frontend/src/components/common/LoadingSpinner.tsx"

check_dir "frontend/src/components/layout"
check_file "frontend/src/components/layout/Header.tsx"
check_file "frontend/src/components/layout/AppLayout.tsx"

# Frontend features
check_dir "frontend/src/features"
check_dir "frontend/src/features/auth"
check_dir "frontend/src/features/auth/store"
check_file "frontend/src/features/auth/store/authStore.ts"

check_dir "frontend/src/features/interviews"
check_dir "frontend/src/features/interviews/store"
check_file "frontend/src/features/interviews/store/interviewsStore.ts"

# Frontend pages
check_dir "frontend/src/pages"
check_dir "frontend/src/pages/auth"
check_file "frontend/src/pages/auth/LoginPage.tsx"
check_dir "frontend/src/pages/dashboard"
check_file "frontend/src/pages/dashboard/DashboardPage.tsx"

# Frontend lib
check_dir "frontend/src/lib"
check_file "frontend/src/lib/api.ts"
check_file "frontend/src/lib/constants.ts"
check_file "frontend/src/lib/utils.ts"
check_file "frontend/src/lib/i18n.ts"

# Frontend types
check_dir "frontend/src/types"
check_file "frontend/src/types/api.ts"
check_file "frontend/src/types/interview.ts"

# Frontend styles
check_dir "frontend/src/styles"
check_file "frontend/src/styles/globals.css"

# Frontend locales
check_dir "frontend/public"
check_dir "frontend/public/locales"
check_dir "frontend/public/locales/en"
check_file "frontend/public/locales/en/common.json"
check_dir "frontend/public/locales/es"
check_file "frontend/public/locales/es/common.json"

# Infrastructure
echo -e "\n${BLUE}🔧 Infrastructure${NC}"
check_dir "nginx"
check_file "nginx/default.conf"

check_dir "scripts"
check_file "scripts/init.sql"
check_file "scripts/setup-dev.sh"
check_file "scripts/health-check.sh"

# Documentation
echo -e "\n${BLUE}📚 Documentation${NC}"
check_dir "docs"
check_file "docs/ARCHITECTURE.md"

# Summary
echo -e "\n${BLUE}📊 Summary${NC}"
echo "================================="
echo -e "Total checks: $total_checks"
echo -e "${GREEN}Passed: $passed_checks${NC}"
echo -e "${RED}Failed: $failed_checks${NC}"

if [[ $failed_checks -eq 0 ]]; then
    echo -e "\n${GREEN}🎉 All components are in place! JobSift MVP is complete.${NC}"
    echo -e "\n${BLUE}Next steps:${NC}"
    echo "1. Run: chmod +x scripts/*.sh"
    echo "2. Run: make setup"
    echo "3. Run: make quickstart"
    exit 0
else
    echo -e "\n${YELLOW}⚠️ Some components are missing. Please check the failed items above.${NC}"
    exit 1
fi
