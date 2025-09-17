# JobSift Scripts

This directory contains utility scripts for setting up and managing the JobSift development environment.

## Scripts Overview

### Setup Scripts

- **`setup-dev.sh`** - Main development environment setup script
  - Creates environment files from examples
  - Generates secure SECRET_KEY
  - Sets up database and installs dependencies
  - Cross-platform compatible (macOS/Linux)

- **`install-deps.sh`** - Universal dependency installer
  - Automatically installs Python 3.11+, Node.js, and checks Docker
  - Supports macOS (with Homebrew) and Linux (apt/yum/dnf)

- **`fix-permissions.sh`** - Fix file permissions and verify setup
  - Makes all scripts executable
  - Verifies required files exist

### Development Scripts

- **`health-check.sh`** - System health verification
  - Checks all services (database, backend, frontend)
  - Tests API endpoints and authentication
  - Verifies complete system functionality

- **`generate-secret.py`** - Secure SECRET_KEY generator
  - Generates cryptographically secure secret keys
  - Can update .env files automatically

- **`check-completeness.sh`** - MVP completeness verification
  - Comprehensive check of all required files
  - Verifies project structure integrity

### Database Scripts

- **`init.sql`** - Database initialization
  - Creates required extensions
  - Sets up initial database structure

## Quick Start

For first-time setup:

```bash
# 1. Fix permissions
chmod +x scripts/fix-permissions.sh
./scripts/fix-permissions.sh

# 2. Install dependencies (optional)
./scripts/install-deps.sh

# 3. Setup development environment
make setup

# 4. Start the application
make quickstart
```

## Platform Compatibility

All scripts are designed to work on:
- **macOS** (with Homebrew)
- **Linux** (Ubuntu/Debian, RHEL/CentOS/Fedora)
- **Windows** (via WSL)

Scripts automatically detect the operating system and use appropriate commands for each platform.

## Environment Variables

The setup scripts will create `.env` files from examples and generate secure secret keys automatically. Manual configuration is only needed for:

- Email settings (SMTP)
- Google Calendar integration
- Production environment variables

## Troubleshooting

If you encounter issues:

1. Run `./scripts/health-check.sh` to diagnose problems
2. Check Docker is running: `docker info`
3. Verify permissions: `./scripts/fix-permissions.sh`
4. Review logs: `make logs`

For platform-specific issues, ensure you have the required dependencies installed for your operating system.
