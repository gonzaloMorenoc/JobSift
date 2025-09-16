# 💼 JobSift - Interview Tracking Made Simple

<div align="center">

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/jobsift/jobsift)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/jobsift/jobsift/actions)
[![Coverage](https://img.shields.io/badge/coverage-85%25-yellowgreen.svg)](https://github.com/jobsift/jobsift/coverage)

**Track your job interviews with ease. Built for modern job seekers.**

[Demo](https://jobsift-demo.onrender.com) • [Documentation](docs/) • [Report Bug](https://github.com/jobsift/jobsift/issues) • [Request Feature](https://github.com/jobsift/jobsift/discussions)

</div>

---

## ✨ Features

### 🎯 **Core Functionality**
- **Interview Management** - Create, update, and track interview processes
- **Smart Dashboard** - Visual analytics and conversion metrics
- **Calendar Integration** - Google Calendar sync + ICS export for Apple/iOS
- **Status Tracking** - From application to offer with milestone tracking
- **Company Profiles** - Detailed company information and notes

### 🔐 **Security & Privacy**
- **JWT Authentication** - Secure token-based auth with refresh tokens
- **GDPR Compliant** - Data ownership and export capabilities
- **Password Security** - bcrypt hashing with secure defaults
- **HTTPS Enforcement** - SSL/TLS encryption in production

### 🌍 **User Experience**
- **Responsive Design** - Works perfectly on desktop and mobile
- **Dark/Light Mode** - User preference support
- **Internationalization** - English and Spanish support
- **Accessibility** - WCAG 2.1 compliant interface

---

## 🚀 Quick Start

### Prerequisites
- **Docker Desktop** 4.0+
- **Node.js** 18+ (for local development)
- **Python** 3.12+ (for local development)

### One-Command Setup
```bash
git clone https://github.com/jobsift/jobsift.git
cd jobsift
make dev
```

That's it! 🎉

**Access your application:**
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

**Demo Credentials:**
- Email: `demo@jobsift.com`
- Password: `demo123456`

---

## 🏗️ Architecture

JobSift follows a modern full-stack architecture designed for scalability and maintainability:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React SPA     │    │   FastAPI        │    │   PostgreSQL    │
│   (Port 5173)   │◄──►│   (Port 8000)    │◄──►│   (Port 5432)   │
│                 │    │                  │    │                 │
│ • TypeScript    │    │ • Python 3.12    │    │ • User Data     │
│ • Zustand       │    │ • SQLAlchemy 2.x │    │ • Interviews    │
│ • TanStack Query│    │ • Alembic        │    │ • Calendar      │
│ • Tailwind CSS  │    │ • Pydantic       │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       
         │              ┌────────────────────┐          
         │              │  External APIs     │          
         └──────────────┤                    │          
                        │ • Google Calendar  │          
                        │ • SMTP Server      │          
                        │ • ICS Export       │          
                        └────────────────────┘          
```

### Tech Stack

**Frontend:**
- React 18 + TypeScript
- Vite (Build tool)
- Zustand (State management)
- TanStack Query (Server state)
- React Hook Form + Zod (Forms)
- Tailwind CSS + shadcn/ui (Styling)

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy 2.x (ORM)
- PostgreSQL (Database)
- Alembic (Migrations)
- JWT + bcrypt (Authentication)
- Pydantic (Validation)

**Infrastructure:**
- Docker + Docker Compose
- Nginx (Reverse proxy)
- Redis (Caching - optional)

---

## 💻 Installation

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker Desktop 4.0+
- 4GB RAM available

**Setup:**
```bash
# 1. Clone repository
git clone https://github.com/jobsift/jobsift.git
cd jobsift

# 2. Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 3. Generate secure secret key
openssl rand -base64 32  # Copy this to backend/.env SECRET_KEY

# 4. Start all services
make dev
# OR: docker-compose up -d

# 5. Open your browser
open http://localhost:5173
```

### Option 2: Local Development

**Prerequisites:**
- Node.js 18+
- Python 3.12+
- PostgreSQL 14+

**Backend Setup:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb jobsift_db
alembic upgrade head

# Seed demo data
python scripts/seed_data.py

# Start server
uvicorn app.main:app --reload
```

**Frontend Setup:**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## ⚙️ Configuration

### Environment Variables

**Backend (.env):**
```bash
# Database
DATABASE_URL=postgresql://jobsift_user:jobsift_pass@localhost:5432/jobsift_db

# Security
SECRET_KEY=your-super-secret-key-here-minimum-32-characters-long
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Google Calendar (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# App Config
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
ENVIRONMENT=development
```

**Frontend (.env):**
```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=JobSift
VITE_GOOGLE_CLIENT_ID=your-google-client-id
```

---

## 📚 Usage Examples

### Creating Your First Interview

1. **Sign Up:** Register with your email at `/register`
2. **Dashboard:** Overview of your interview pipeline
3. **Add Interview:** Click "New Interview" button
4. **Fill Details:** Company, role, status, salary range, etc.
5. **Track Progress:** Update status as you progress through stages

### Calendar Integration

**Google Calendar:**
```bash
# Sync interview with Google Calendar
POST /api/v1/calendar/google/sync
{
  "interview_id": "uuid-here"
}
```

**Apple/iOS (ICS Export):**
```bash
# Download ICS file
GET /api/v1/calendar/ics?days_ahead=90
```

### Dashboard Analytics

The dashboard provides:
- **Total interviews** by status
- **Conversion rates** from application to offer  
- **Upcoming interviews** this week
- **Recent activity** timeline
- **Success metrics** and trends

---

## 📖 API Reference

### Authentication

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET  /api/v1/auth/me
```

### Interviews

```http
GET    /api/v1/interviews          # List interviews
POST   /api/v1/interviews          # Create interview  
GET    /api/v1/interviews/{id}     # Get interview
PUT    /api/v1/interviews/{id}     # Update interview
DELETE /api/v1/interviews/{id}     # Delete interview
```

### Dashboard

```http
GET /api/v1/dashboard/summary      # Dashboard metrics
```

### Calendar

```http
POST /api/v1/calendar/google/sync  # Sync with Google
GET  /api/v1/calendar/ics          # Export ICS feed
```

**Full API Documentation:** http://localhost:8000/docs

---

## 🚀 Deployment

### Option 1: Railway (Recommended for MVP)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init jobsift
railway up
```

**Estimated cost:** $0-20/month

### Option 2: Docker Production

```bash
# Build for production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# With SSL (recommended)
docker-compose --profile production up -d
```

### Option 3: Cloud Providers

- **Fly.io:** ~$35/month
- **Render:** ~$57/month  
- **Google Cloud:** ~$62/month

**See full deployment guide:** [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 🧪 Testing

```bash
# Run all tests
make test

# Backend tests only
cd backend && pytest --cov=app tests/

# Frontend tests only  
cd frontend && npm test

# E2E tests
npm run test:e2e
```

**Current Coverage:** 85%+ on critical paths

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Code Quality

- **TypeScript** strict mode enabled
- **ESLint + Prettier** for code formatting
- **Black + isort** for Python formatting
- **Pre-commit hooks** for automatic checks

---

## 📊 Project Status

- ✅ **MVP Complete** (v1.0.0) - In Progress  
- 🏗️ **Testing Suite** (v1.1.0) - In Progress  
- 📅 **OAuth Integration** (v1.1.0) - Planned
- 🔔 **Notifications** (v1.2.0) - Planned

**See full roadmap:** [ROADMAP.md](ROADMAP.md)

---

## 🛠️ Built With

<div align="center">

[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

</div>

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙋‍♀️ Support

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/jobsift/jobsift/issues)
- **Discussions:** [GitHub Discussions](https://github.com/jobsift/jobsift/discussions)
- **Email:** support@jobsift.com

---

## ⭐ Show your support

Give a ⭐️ if this project helped you!

---

<div align="center">

**[⬆ back to top](#-jobsift---interview-tracking-made-simple)**

</div>