#!/bin/bash

# JobSift System Health Check Script
# This script verifies that all components are working correctly

set -e

echo "🔍 Running JobSift system health checks..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running${NC}"
    exit 1
fi

# Check if services are up
echo -e "${BLUE}📊 Checking service status...${NC}"

services=("db" "backend" "frontend")
for service in "${services[@]}"; do
    if docker-compose ps -q $service > /dev/null 2>&1; then
        status=$(docker-compose ps $service | grep $service | awk '{print $3}')
        if [[ "$status" == "Up" ]]; then
            echo -e "${GREEN}✅ $service is running${NC}"
        else
            echo -e "${RED}❌ $service is not running (status: $status)${NC}"
        fi
    else
        echo -e "${RED}❌ $service container not found${NC}"
    fi
done

# Health check functions
check_database() {
    echo -e "${BLUE}🗄️  Checking database connection...${NC}"
    if docker-compose exec -T db pg_isready -U jobsift_user -d jobsift_db > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Database is healthy${NC}"
        
        # Check if tables exist
        table_count=$(docker-compose exec -T db psql -U jobsift_user -d jobsift_db -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';" | xargs)
        if [[ $table_count -gt 0 ]]; then
            echo -e "${GREEN}✅ Database tables exist ($table_count tables)${NC}"
        else
            echo -e "${YELLOW}⚠️  No tables found - run migrations${NC}"
        fi
        
        # Check if demo user exists
        user_count=$(docker-compose exec -T db psql -U jobsift_user -d jobsift_db -t -c "SELECT count(*) FROM users WHERE email = 'demo@jobsift.com';" 2>/dev/null | xargs || echo "0")
        if [[ $user_count -gt 0 ]]; then
            echo -e "${GREEN}✅ Demo user exists${NC}"
        else
            echo -e "${YELLOW}⚠️  Demo user not found - run seed script${NC}"
        fi
    else
        echo -e "${RED}❌ Database connection failed${NC}"
        return 1
    fi
}

check_backend() {
    echo -e "${BLUE}🔧 Checking backend API...${NC}"
    
    # Wait for backend to be ready
    max_attempts=30
    attempt=1
    while ! curl -s http://localhost:8000/health > /dev/null; do
        if [[ $attempt -eq $max_attempts ]]; then
            echo -e "${RED}❌ Backend API not responding after $max_attempts attempts${NC}"
            return 1
        fi
        echo -e "${YELLOW}⏳ Waiting for backend... (attempt $attempt/$max_attempts)${NC}"
        sleep 2
        ((attempt++))
    done
    
    # Test health endpoint
    health_response=$(curl -s http://localhost:8000/health)
    if echo "$health_response" | grep -q "ok"; then
        echo -e "${GREEN}✅ Backend health check passed${NC}"
    else
        echo -e "${RED}❌ Backend health check failed${NC}"
        return 1
    fi
    
    # Test API docs
    if curl -s http://localhost:8000/docs > /dev/null; then
        echo -e "${GREEN}✅ API documentation accessible${NC}"
    else
        echo -e "${YELLOW}⚠️  API documentation not accessible${NC}"
    fi
    
    # Test CORS headers
    cors_headers=$(curl -s -H "Origin: http://localhost:5173" -I http://localhost:8000/health | grep -i "access-control" || true)
    if [[ -n "$cors_headers" ]]; then
        echo -e "${GREEN}✅ CORS headers configured${NC}"
    else
        echo -e "${YELLOW}⚠️  CORS headers not found${NC}"
    fi
}

check_frontend() {
    echo -e "${BLUE}🖥️  Checking frontend application...${NC}"
    
    # Wait for frontend to be ready
    max_attempts=30
    attempt=1
    while ! curl -s http://localhost:5173 > /dev/null; do
        if [[ $attempt -eq $max_attempts ]]; then
            echo -e "${RED}❌ Frontend not responding after $max_attempts attempts${NC}"
            return 1
        fi
        echo -e "${YELLOW}⏳ Waiting for frontend... (attempt $attempt/$max_attempts)${NC}"
        sleep 2
        ((attempt++))
    done
    
    # Test if React app loads
    frontend_response=$(curl -s http://localhost:5173)
    if echo "$frontend_response" | grep -q "<!DOCTYPE html>"; then
        echo -e "${GREEN}✅ Frontend application loads${NC}"
    else
        echo -e "${RED}❌ Frontend application failed to load${NC}"
        return 1
    fi
    
    # Check if Vite dev server is running (in development)
    if echo "$frontend_response" | grep -q "vite"; then
        echo -e "${GREEN}✅ Vite dev server running${NC}"
    fi
}

check_integration() {
    echo -e "${BLUE}🔗 Checking API integration...${NC}"
    
    # Test login endpoint
    login_response=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
        -H "Content-Type: application/json" \
        -d '{"email":"demo@jobsift.com","password":"demo123456"}' || echo "error")
    
    if echo "$login_response" | grep -q "access_token"; then
        echo -e "${GREEN}✅ Login endpoint working${NC}"
        
        # Extract token for further tests
        access_token=$(echo "$login_response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
        
        # Test authenticated endpoint
        me_response=$(curl -s -H "Authorization: Bearer $access_token" http://localhost:8000/api/v1/auth/me || echo "error")
        
        if echo "$me_response" | grep -q "demo@jobsift.com"; then
            echo -e "${GREEN}✅ Authentication working${NC}"
        else
            echo -e "${YELLOW}⚠️  Authentication test failed${NC}"
        fi
        
        # Test dashboard endpoint
        dashboard_response=$(curl -s -H "Authorization: Bearer $access_token" http://localhost:8000/api/v1/dashboard/summary || echo "error")
        
        if echo "$dashboard_response" | grep -q "summary"; then
            echo -e "${GREEN}✅ Dashboard API working${NC}"
        else
            echo -e "${YELLOW}⚠️  Dashboard API test failed${NC}"
        fi
        
    else
        echo -e "${YELLOW}⚠️  Login endpoint test failed${NC}"
    fi
}

# Run all health checks
echo ""
check_database || exit 1
echo ""
check_backend || exit 1
echo ""
check_frontend || exit 1
echo ""
check_integration
echo ""

# Summary
echo -e "${GREEN}🎉 System health check completed!${NC}"
echo ""
echo -e "${BLUE}📋 Quick Access:${NC}"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo -e "${BLUE}🔑 Demo Login:${NC}"
echo "   Email: demo@jobsift.com"
echo "   Password: demo123456"
echo ""

# Optional: Open browser
if command -v open &> /dev/null; then
    echo -e "${BLUE}🌐 Opening application in browser...${NC}"
    open http://localhost:5173
elif command -v xdg-open &> /dev/null; then
    echo -e "${BLUE}🌐 Opening application in browser...${NC}"
    xdg-open http://localhost:5173
fi

echo -e "${GREEN}✨ JobSift is ready to use!${NC}"
