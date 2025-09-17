# JobSift Architecture Documentation

## Overview

JobSift is a modern full-stack web application for tracking job interviews. It follows a clean architecture pattern with clear separation between frontend, backend, and database layers.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Production Stack                        │
├─────────────────┬───────────────────┬───────────────────────────┤
│   React SPA     │    FastAPI        │     PostgreSQL            │
│   (Port 5173)   │    (Port 8000)    │     (Port 5432)           │
│                 │                   │                           │
│ • TypeScript    │ • Python 3.12     │ • JSONB Support          │
│ • Zustand       │ • SQLAlchemy 2.x   │ • Full-text Search       │
│ • TanStack Query│ • Alembic          │ • Robust Indexing        │
│ • React Router  │ • Pydantic         │ • Connection Pooling     │
│ • Tailwind CSS  │ • JWT Auth         │                          │
│ • shadcn/ui     │ • CORS Support     │                          │
└─────────────────┴───────────────────┴───────────────────────────┘
         │                    │                     │
         │                    │                     │
         └────────────────────┼─────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   External APIs   │
                    │                   │
                    │ • Google Calendar │
                    │ • SMTP Server     │
                    │ • ICS Export      │
                    └───────────────────┘
```

## Backend Architecture

### Layer Structure

```
app/
├── api/                 # API Layer (Controllers)
│   ├── deps.py         # Dependencies
│   └── v1/             # API Version 1
│       ├── auth.py     # Authentication endpoints
│       ├── interviews.py # Interview CRUD endpoints
│       ├── dashboard.py  # Dashboard & analytics
│       └── calendar.py   # Calendar integration
├── core/               # Core Configuration
│   ├── config.py       # Application settings
│   ├── database.py     # Database connection
│   └── security.py     # Security utilities
├── models/             # Data Models (ORM)
│   ├── user.py         # User model
│   ├── interview.py    # Interview model
│   └── calendar_event.py # Calendar event model
├── repositories/       # Data Access Layer
│   ├── base.py         # Base repository
│   ├── user.py         # User repository
│   └── interview.py    # Interview repository
├── services/           # Business Logic Layer
│   ├── auth.py         # Authentication service
│   ├── interview.py    # Interview service
│   ├── dashboard.py    # Dashboard service
│   └── calendar.py     # Calendar service
├── schemas/            # Request/Response Models
│   ├── user.py         # User schemas
│   ├── interview.py    # Interview schemas
│   └── dashboard.py    # Dashboard schemas
└── utils/              # Utilities
```

### Design Patterns

#### 1. Repository Pattern
- **Purpose**: Abstract data access logic
- **Implementation**: Base repository with generic CRUD operations
- **Benefits**: Testability, maintainability, database agnostic

```python
class BaseRepository(Generic[T]):
    def create(self, data: Dict[str, Any]) -> T
    def get_by_id(self, id: Any) -> Optional[T]
    def update(self, id: Any, data: Dict[str, Any]) -> Optional[T]
    def delete(self, id: Any) -> bool
```

#### 2. Service Layer Pattern
- **Purpose**: Encapsulate business logic
- **Implementation**: Services coordinate between repositories
- **Benefits**: Single responsibility, reusable business logic

```python
class InterviewService:
    def __init__(self, db: Session):
        self.interview_repo = InterviewRepository(db)
    
    def create_interview(self, user: User, data: InterviewCreate) -> Interview:
        # Business logic here
        return self.interview_repo.create_interview(...)
```

#### 3. Dependency Injection
- **Purpose**: Loose coupling between components
- **Implementation**: FastAPI's dependency system
- **Benefits**: Testability, flexibility

```python
@router.post("/interviews")
async def create_interview(
    interview_data: InterviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = InterviewService(db)
    return service.create_interview(current_user, interview_data)
```

## Frontend Architecture

### Component Structure

```
src/
├── components/         # Reusable UI Components
│   ├── ui/            # Base UI components (shadcn/ui)
│   ├── common/        # Common app components
│   └── layout/        # Layout components
├── features/          # Feature-based organization
│   ├── auth/          # Authentication feature
│   │   └── store/     # Auth state management
│   └── interviews/    # Interviews feature
│       └── store/     # Interview state management
├── pages/             # Page components
│   ├── auth/          # Authentication pages
│   ├── dashboard/     # Dashboard pages
│   └── interviews/    # Interview pages
├── lib/               # Utilities and configurations
│   ├── api.ts         # API client
│   ├── utils.ts       # Helper functions
│   └── i18n.ts        # Internationalization
├── types/             # TypeScript type definitions
└── styles/            # Global styles
```

### State Management Architecture

#### 1. Zustand Stores
- **Authentication State**: User session, login/logout
- **Interview State**: CRUD operations, filtering, pagination
- **UI State**: Loading states, error handling

#### 2. TanStack Query
- **Server State Management**: Caching, background updates
- **Optimistic Updates**: Immediate UI feedback
- **Error Handling**: Automatic retry and error states

#### 3. Form Management
- **React Hook Form**: Form validation and submission
- **Zod**: Runtime type validation
- **Integration**: Seamless API integration

## Database Design

### Entity Relationship Diagram

```
┌─────────────────┐     ┌─────────────────────┐     ┌─────────────────┐
│      Users      │     │     Interviews      │     │ Calendar Events │
├─────────────────┤     ├─────────────────────┤     ├─────────────────┤
│ id (UUID) PK    │────▶│ id (UUID) PK        │────▶│ id (UUID) PK    │
│ email           │     │ user_id (UUID) FK   │     │ interview_id FK │
│ password_hash   │     │ company_name        │     │ external_id     │
│ full_name       │     │ role_title          │     │ provider        │
│ locale          │     │ work_mode           │     │ event_title     │
│ is_verified     │     │ location            │     │ start_time      │
│ is_active       │     │ application_status  │     │ end_time        │
│ created_at      │     │ contact_info        │     │ is_synced       │
│ updated_at      │     │ salary_range        │     │ created_at      │
└─────────────────┘     │ notes               │     │ updated_at      │
                        │ interview_date      │     └─────────────────┘
                        │ created_at          │
                        │ updated_at          │
                        └─────────────────────┘
```

### Design Decisions

#### 1. UUID Primary Keys
- **Benefits**: Globally unique, security, distributed systems ready
- **Trade-offs**: Larger storage, no natural ordering

#### 2. JSONB for Flexible Data
- **Use Case**: Contact information, metadata
- **Benefits**: Schema flexibility, queryable
- **Performance**: Proper indexing for common queries

#### 3. Enum Types for Status
- **Implementation**: Python enums → PostgreSQL enums
- **Benefits**: Data integrity, clear domain model
- **Flexibility**: Easy to extend with migrations

## Security Architecture

### Authentication & Authorization

#### 1. JWT Token Strategy
- **Access Tokens**: Short-lived (30 min), stored in localStorage
- **Refresh Tokens**: Long-lived (30 days), HTTP-only cookies
- **Benefits**: Stateless, scalable, secure

#### 2. Password Security
- **Hashing**: bcrypt with salt
- **Minimum Requirements**: 6 characters (configurable)
- **Future**: Password complexity rules, breach checking

#### 3. CORS Configuration
- **Development**: Permissive for localhost
- **Production**: Strict origin control
- **Credentials**: Supported for cookie auth

### Data Protection

#### 1. Input Validation
- **Backend**: Pydantic models with validation
- **Frontend**: Zod schemas with runtime checking
- **SQL Injection**: SQLAlchemy ORM protection

#### 2. Rate Limiting
- **Implementation**: Nginx-based rate limiting
- **API Endpoints**: 10 requests/second
- **Auth Endpoints**: 5 requests/second (stricter)

#### 3. HTTPS Enforcement
- **Development**: HTTP acceptable
- **Production**: HTTPS required, HSTS headers
- **Certificates**: Automated with Let's Encrypt

## Performance Optimization

### Backend Performance

#### 1. Database Optimization
- **Connection Pooling**: SQLAlchemy pool (10 connections, 20 overflow)
- **Query Optimization**: Strategic indexes, N+1 query prevention
- **Caching**: Redis for session data (future enhancement)

#### 2. API Performance
- **Async Processing**: FastAPI async/await patterns
- **Pagination**: Limit/offset with defaults
- **Compression**: Gzip middleware enabled

### Frontend Performance

#### 1. Bundle Optimization
- **Code Splitting**: Route-based chunks
- **Tree Shaking**: Unused code elimination
- **Asset Optimization**: Vite's built-in optimizations

#### 2. Runtime Performance
- **State Management**: Minimal re-renders with Zustand
- **API Caching**: TanStack Query intelligent caching
- **Image Optimization**: WebP format, lazy loading

## Deployment Architecture

### Container Strategy

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Compose                       │
├─────────────────┬─────────────────┬─────────────────────┤
│   nginx         │   backend       │   frontend          │
│   (Port 80/443) │   (Port 8000)   │   (Port 5173)       │
│                 │                 │                     │
│ • Reverse Proxy │ • FastAPI App   │ • React Dev Server  │
│ • SSL Termination │ • Gunicorn     │ • Vite HMR         │
│ • Static Files  │ • Health Checks │ • Hot Reload       │
│ • Rate Limiting │                 │                     │
└─────────────────┴─────────────────┴─────────────────────┘
         │                │                │
         │                │                │
         └────────────────┼────────────────┘
                          │
      ┌─────────────────┬─┴─────────────────┬─────────────────┐
      │   postgres      │      redis        │    volumes      │
      │   (Port 5432)   │   (Port 6379)     │                 │
      │                 │                   │ • Database Data │
      │ • Primary DB    │ • Session Store   │ • Upload Files  │
      │ • Connection    │ • Cache Layer     │ • SSL Certs     │
      │   Pooling       │ • Background      │ • Logs          │
      │ • Backups       │   Jobs (Future)   │                 │
      └─────────────────┴───────────────────┴─────────────────┘
```

### Production Considerations

#### 1. Scalability
- **Horizontal Scaling**: Load balancer + multiple backend instances
- **Database**: Read replicas for analytics queries
- **CDN**: Static asset delivery (future)

#### 2. Monitoring & Observability
- **Health Checks**: Built-in endpoints for all services
- **Logging**: Structured JSON logs
- **Metrics**: Prometheus/Grafana setup (future)

#### 3. Backup & Recovery
- **Database Backups**: Automated PostgreSQL dumps
- **File Storage**: Volume persistence
- **Disaster Recovery**: Multi-zone deployment (production)

## API Design Principles

### RESTful API Design

#### 1. Resource-Based URLs
```
GET    /api/v1/interviews           # List interviews
POST   /api/v1/interviews           # Create interview
GET    /api/v1/interviews/{id}      # Get interview
PUT    /api/v1/interviews/{id}      # Update interview
DELETE /api/v1/interviews/{id}      # Delete interview
```

#### 2. HTTP Status Codes
- **200**: Success
- **201**: Created
- **204**: No Content (delete)
- **400**: Bad Request (validation)
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **422**: Unprocessable Entity
- **500**: Internal Server Error

#### 3. Response Format
```json
{
  "data": { ... },           // Actual response data
  "meta": {                  // Metadata
    "total": 100,
    "page": 1,
    "limit": 20
  },
  "links": {                 // Pagination links
    "self": "/api/v1/interviews?page=1",
    "next": "/api/v1/interviews?page=2"
  }
}
```

### Error Handling

#### 1. Consistent Error Format
```json
{
  "error": {
    "type": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

#### 2. Error Types
- **VALIDATION_ERROR**: Input validation failures
- **AUTHENTICATION_ERROR**: Auth failures
- **AUTHORIZATION_ERROR**: Permission denied
- **NOT_FOUND_ERROR**: Resource not found
- **INTERNAL_ERROR**: Server errors

## Testing Strategy

### Backend Testing

#### 1. Test Pyramid
- **Unit Tests**: Business logic, utilities (70%)
- **Integration Tests**: API endpoints, database (20%)
- **E2E Tests**: Full user workflows (10%)

#### 2. Test Categories
```python
# Unit Tests
def test_create_interview_service():
    # Test business logic in isolation

# Integration Tests  
def test_create_interview_endpoint():
    # Test API endpoint with database

# E2E Tests (Future)
def test_complete_interview_workflow():
    # Test full user journey
```

#### 3. Test Data Management
- **Fixtures**: Reusable test data
- **Factory Pattern**: Dynamic test object creation
- **Database**: Separate test database, auto-cleanup

### Frontend Testing

#### 1. Component Testing
- **Unit Tests**: Individual component logic
- **Integration Tests**: Component interactions
- **Visual Tests**: Storybook for UI components

#### 2. State Testing
- **Store Tests**: Zustand store logic
- **API Tests**: Mock API interactions
- **Form Tests**: Validation and submission

## Future Enhancements

### Phase 2 (v1.2)
- [ ] **Email Notifications**: Interview reminders, status updates
- [ ] **File Management**: Resume upload, job descriptions
- [ ] **Advanced Analytics**: Conversion funnels, time metrics
- [ ] **OAuth Integration**: Google, LinkedIn, Microsoft auth

### Phase 3 (v1.3)
- [ ] **Real-time Updates**: WebSocket notifications
- [ ] **Collaboration**: Share interviews with recruiters
- [ ] **API Integrations**: LinkedIn Jobs, Indeed API
- [ ] **Mobile App**: React Native application

### Phase 4 (v2.0)
- [ ] **AI Features**: Application insights, salary predictions
- [ ] **Enterprise Features**: Team management, reporting
- [ ] **Advanced Calendar**: Multiple calendar sync
- [ ] **Interview Preparation**: AI-powered practice questions

## Conclusion

JobSift's architecture is designed for scalability, maintainability, and developer productivity. The clean separation of concerns, modern technology stack, and comprehensive testing strategy provide a solid foundation for long-term growth and feature development.

Key architectural strengths:
- **Modularity**: Clear boundaries between layers
- **Testability**: Dependency injection and mocking support
- **Scalability**: Stateless design, database optimization
- **Security**: Modern authentication, input validation
- **Developer Experience**: Hot reload, type safety, automation

This architecture supports rapid feature development while maintaining code quality and system reliability.
