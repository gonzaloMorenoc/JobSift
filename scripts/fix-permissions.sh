#!/bin/bash

# JobSift - Fix permissions and verify setup
# This script ensures all files have correct permissions

echo "🔧 Fixing file permissions for JobSift..."

# Make scripts executable
chmod +x scripts/*.sh
chmod +x scripts/*.py

# Verify permissions
echo "✅ Script permissions fixed"

# Quick verification
echo "🔍 Verifying setup..."

# Check for required files
required_files=(
    "docker-compose.yml"
    "Makefile"
    "scripts/setup-dev.sh"
    "scripts/health-check.sh"
    "scripts/install-deps.sh"
    "backend/.env.example"
    "frontend/.env.example"
)

missing_files=()

for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        missing_files+=("$file")
    fi
done

if [[ ${#missing_files[@]} -eq 0 ]]; then
    echo "✅ All required files present"
else
    echo "❌ Missing files:"
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
    exit 1
fi

echo "🎉 Setup verification complete!"
echo ""
echo "Next steps:"
echo "1. Run: make setup"
echo "2. Run: make quickstart"
