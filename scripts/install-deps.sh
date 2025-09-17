#!/bin/bash

# Universal dependency installer for JobSift
# Works on macOS, Linux, and Windows (WSL)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📦 Installing JobSift dependencies...${NC}"

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
echo -e "${BLUE}🖥️  Detected OS: $OS${NC}"

# Install Python 3.11+ if not available
install_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${YELLOW}⚠️  Python3 not found, attempting to install...${NC}"
        
        case $OS in
            "macos")
                if command -v brew &> /dev/null; then
                    brew install python@3.11
                else
                    echo -e "${RED}❌ Homebrew not found. Please install Python 3.11+ manually${NC}"
                    echo "Visit: https://www.python.org/downloads/"
                    exit 1
                fi
                ;;
            "linux")
                if command -v apt-get &> /dev/null; then
                    sudo apt-get update
                    sudo apt-get install -y python3.11 python3.11-venv python3-pip
                elif command -v yum &> /dev/null; then
                    sudo yum install -y python3.11 python3-pip
                elif command -v dnf &> /dev/null; then
                    sudo dnf install -y python3.11 python3-pip
                else
                    echo -e "${RED}❌ Package manager not found. Please install Python 3.11+ manually${NC}"
                    exit 1
                fi
                ;;
            *)
                echo -e "${RED}❌ Unsupported OS for automatic Python installation${NC}"
                exit 1
                ;;
        esac
    else
        echo -e "${GREEN}✅ Python3 found${NC}"
    fi
}

# Install Node.js if not available
install_node() {
    if ! command -v npm &> /dev/null; then
        echo -e "${YELLOW}⚠️  Node.js not found, attempting to install...${NC}"
        
        case $OS in
            "macos")
                if command -v brew &> /dev/null; then
                    brew install node
                else
                    echo -e "${RED}❌ Homebrew not found. Please install Node.js 18+ manually${NC}"
                    echo "Visit: https://nodejs.org/"
                    exit 1
                fi
                ;;
            "linux")
                curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
                sudo apt-get install -y nodejs
                ;;
            *)
                echo -e "${RED}❌ Unsupported OS for automatic Node.js installation${NC}"
                exit 1
                ;;
        esac
    else
        echo -e "${GREEN}✅ Node.js found${NC}"
    fi
}

# Install Docker if not available
install_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}⚠️  Docker not found${NC}"
        echo -e "${BLUE}📖 Please install Docker Desktop:${NC}"
        case $OS in
            "macos")
                echo "  Download from: https://docs.docker.com/desktop/mac/install/"
                ;;
            "linux")
                echo "  Run: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"
                ;;
            "windows")
                echo "  Download from: https://docs.docker.com/desktop/windows/install/"
                ;;
        esac
        exit 1
    else
        echo -e "${GREEN}✅ Docker found${NC}"
    fi
}

# Main installation
install_python
install_node
install_docker

echo -e "${GREEN}🎉 All dependencies installed successfully!${NC}"
echo -e "${BLUE}📝 Next steps:${NC}"
echo "1. Run: make setup"
echo "2. Run: make quickstart"
