# Implementation Plan: Phase II - Full-Stack Web Application

**Branch**: `001-fullstack-web-app` | **Date**: 2026-01-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-fullstack-web-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a full-stack web application with JWT-authenticated task management system. The backend uses FastAPI + SQLModel with Neon PostgreSQL for persistence, exposing a REST API at `/api/v1`. The frontend uses Next.js with server-side rendering and API route handlers. Users can register, authenticate, and perform full CRUD operations on their personal tasks with complete data isolation enforced at the database and API layers.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x + Node.js 18+ (frontend)
**Primary Dependencies**: FastAPI 0.104+, SQLModel 0.0.14+, python-jose[cryptography] (JWT), bcrypt (password hashing), Next.js 14+, React 18+
**Storage**: Neon PostgreSQL (serverless, managed, PostgreSQL 16 compatible)
**Testing**: pytest + pytest-asyncio (backend), Jest + React Testing Library (frontend)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge - last 2 versions), Linux/Windows/macOS servers for backend
**Project Type**: Web application (separate backend and frontend)
**Performance Goals**: <500ms API response time, <2s task creation round-trip, <5s authentication flow
**Constraints**: <200ms validation errors, stateless authentication (JWT only), complete user data isolation
**Scale/Scope**: 100+ users with 1000 tasks each, 8 REST API endpoints, 5-7 frontend pages/components

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Spec-Driven Development**: ✅ PASS
- Feature specification approved in `specs/001-fullstack-web-app/spec.md`
- Implementation plan (this document) created before coding
- Task list will be generated via `/sp.tasks` command after plan approval

**Agent Behavior Rules**: ✅ PASS
- No manual coding - all implementation will be agent-generated
- No feature invention - scope strictly limited to spec requirements (FR-001 through FR-040)
- No deviation - implementation follows approved spec and plan exactly
- Refinement at spec level - any ambiguities resolved via spec updates, not code interpretation

**Phase Governance**: ✅ PASS
- Phase II scope strictly enforced (web application with authentication and task CRUD)
- No Phase I (CLI) features in Phase II implementation (FR-040)
- No Phase III (AI/chatbot) features in Phase II implementation (FR-036, FR-037, FR-038)
- No Phase IV/V (Kubernetes, Kafka, Dapr) in Phase II implementation (FR-039)
- Architecture designed to support future phases without requiring Phase II refactoring

**Technology Constraints**: ✅ PASS
- Backend: Python + FastAPI + SQLModel (constitution-mandated)
- Database: Neon DB (PostgreSQL-compatible, constitution-mandated)
- Frontend: Next.js (constitution-mandated)
- No unauthorized technology introductions

**Quality Principles**: ✅ PASS
- Clean architecture: Models → Services → API layers clearly separated
- Stateless services: JWT-based authentication, no server-side sessions (FR-007)
- Clear separation of concerns: Auth, tasks, database each have dedicated modules
- Cloud-native readiness: Environment-based configuration, containerization-ready structure

## Project Structure

### Documentation (this feature)

```text
specs/001-fullstack-web-app/
├── spec.md              # Feature specification (approved)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: Technology and architecture research
├── data-model.md        # Phase 1: Database schema and entity relationships
├── quickstart.md        # Phase 1: Setup and development guide
├── contracts/           # Phase 1: API contract specifications
│   ├── auth-api.md      # Authentication endpoints (signup, login)
│   └── tasks-api.md     # Task CRUD endpoints
└── tasks.md             # Phase 2: Actionable task list (via /sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and environment variables
│   ├── database.py          # Database connection and session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User SQLModel (id, email, hashed_password, timestamps)
│   │   └── task.py          # Task SQLModel (id, user_id, title, description, completed, timestamps)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py          # Pydantic schemas for auth requests/responses
│   │   └── task.py          # Pydantic schemas for task requests/responses
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication service (password hashing, JWT generation/validation)
│   │   └── task.py          # Task service (CRUD operations with user isolation)
│   └── api/
│       ├── __init__.py
│       ├── deps.py          # Dependency injection (get_db, get_current_user)
│       └── v1/
│           ├── __init__.py
│           ├── auth.py      # Auth routes (/api/v1/auth/signup, /api/v1/auth/login)
│           └── tasks.py     # Task routes (/api/v1/tasks, /api/v1/tasks/{id}, etc.)
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures (test database, test client, test users)
│   ├── test_auth.py         # Authentication endpoint tests
│   └── test_tasks.py        # Task endpoint tests
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
└── README.md                # Backend setup and API documentation

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home/landing page
│   │   ├── signup/
│   │   │   └── page.tsx     # User registration page
│   │   ├── login/
│   │   │   └── page.tsx     # User login page
│   │   └── tasks/
│   │       └── page.tsx     # Task management dashboard
│   ├── components/
│   │   ├── TaskList.tsx     # Task list component
│   │   ├── TaskForm.tsx     # Task creation/edit form
│   │   ├── TaskItem.tsx     # Individual task item
│   │   └── AuthForm.tsx     # Reusable auth form component
│   ├── lib/
│   │   ├── api.ts           # API client with auth headers
│   │   └── auth.ts          # Auth utilities (token storage, user context)
│   └── types/
│       ├── user.ts          # User TypeScript types
│       └── task.ts          # Task TypeScript types
├── public/                  # Static assets
├── tests/
│   ├── components/          # Component unit tests
│   └── integration/         # Integration tests
├── package.json             # Node dependencies
├── tsconfig.json            # TypeScript configuration
├── next.config.js           # Next.js configuration
├── .env.local.example       # Environment variable template
└── README.md                # Frontend setup and development guide

# Root level (repository)
.
├── backend/                 # Backend directory (see above)
├── frontend/                # Frontend directory (see above)
├── todo/                    # Phase I CLI (preserved, not modified)
├── tests/                   # Phase I tests (preserved, not modified)
├── specs/                   # All feature specifications
├── history/                 # PHRs and ADRs
├── .specify/                # SpecKit Plus templates
├── README.md                # Project overview and phase navigation
└── CLAUDE.md                # Agent instructions
```

**Structure Decision**: Web application architecture with separate `backend/` and `frontend/` directories. This separation ensures:

1. **Clear phase boundaries**: Phase I CLI code in `todo/` remains untouched, Phase II web code in dedicated directories
2. **Independent deployment**: Backend and frontend can be deployed separately
3. **Technology isolation**: Python dependencies don't conflict with Node.js dependencies
4. **Clean architecture**: Each directory follows its ecosystem's conventions (FastAPI backend structure, Next.js app directory structure)
5. **Future extensibility**: Phase III AI features can be added without restructuring Phase II code

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations detected. All complexity is justified by requirements:
- Separate backend/frontend: Required for web architecture (FR-027, constitution-mandated Next.js)
- JWT authentication: Required for stateless auth (FR-007, SC-010)
- SQLModel ORM: Constitution-mandated, prevents SQL injection vulnerabilities
- Service layer: Required for clean architecture (constitution quality principle)

## Phase 0: Research and Discovery

### Technology Stack Validation

**Backend Stack**:
- **FastAPI 0.104+**: Constitution-mandated, provides async support, automatic OpenAPI documentation, dependency injection
- **SQLModel 0.0.14+**: Constitution-mandated, combines SQLAlchemy and Pydantic for type-safe database operations
- **python-jose[cryptography]**: JWT implementation (RS256/HS256 algorithms)
- **passlib[bcrypt]**: Password hashing with bcrypt algorithm (industry standard)
- **asyncpg**: Async PostgreSQL driver for SQLModel
- **alembic**: Database migrations (schema evolution)

**Frontend Stack**:
- **Next.js 14+**: Constitution-mandated, provides App Router, server components, API routes
- **React 18+**: Required by Next.js, provides component architecture
- **TypeScript 5.x**: Type safety for frontend code
- **Tailwind CSS**: Utility-first CSS framework (optional, can use alternative)
- **Axios or Fetch API**: HTTP client for API communication

**Database**:
- **Neon PostgreSQL**: Constitution-mandated, serverless, PostgreSQL 16 compatible, automatic scaling

### Architecture Patterns

**Backend Architecture** (Clean Architecture):
```
┌─────────────────────────────────────────┐
│         FastAPI Application             │
│  (main.py - ASGI entry point)           │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         API Layer (Routes)              │
│  /api/v1/auth/* - Authentication        │
│  /api/v1/tasks/* - Task management      │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│       Service Layer (Business Logic)    │
│  auth.py - Password hashing, JWT        │
│  task.py - CRUD operations, isolation   │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│       Data Layer (Models)               │
│  User model - SQLModel ORM              │
│  Task model - SQLModel ORM              │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Database (Neon PostgreSQL)      │
│  users table - User data                │
│  tasks table - Task data                │
└─────────────────────────────────────────┘
```

**Frontend Architecture** (Next.js App Router):
```
┌─────────────────────────────────────────┐
│         Next.js Application             │
│  (app/ directory - React components)    │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Pages (Server Components)       │
│  /signup - User registration UI         │
│  /login - User authentication UI        │
│  /tasks - Task management dashboard     │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Components (Client Components)     │
│  TaskList - Display tasks               │
│  TaskForm - Create/edit tasks           │
│  TaskItem - Individual task UI          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│       API Client Library (lib/)         │
│  api.ts - HTTP client with auth         │
│  auth.ts - Token storage, user context  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Backend REST API                │
│  (FastAPI endpoints)                    │
└─────────────────────────────────────────┘
```

### Authentication Flow

**JWT Token Structure**:
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

**Signup Flow**:
1. User submits email + password via frontend form
2. Frontend sends POST request to `/api/v1/auth/signup`
3. Backend validates email format, checks uniqueness
4. Backend hashes password with bcrypt (cost factor 12)
5. Backend creates User record in database
6. Backend generates JWT token (24-hour expiration)
7. Backend returns `{access_token, token_type}` response
8. Frontend stores token in localStorage/sessionStorage
9. Frontend redirects to `/tasks` page

**Login Flow**:
1. User submits email + password via frontend form
2. Frontend sends POST request to `/api/v1/auth/login`
3. Backend retrieves User by email
4. Backend verifies password hash
5. Backend generates JWT token (24-hour expiration)
6. Backend returns `{access_token, token_type}` response
7. Frontend stores token in localStorage/sessionStorage
8. Frontend redirects to `/tasks` page

**Authenticated Request Flow**:
1. Frontend includes token in Authorization header: `Bearer <token>`
2. Backend dependency `get_current_user` extracts token
3. Backend validates JWT signature and expiration
4. Backend decodes token and retrieves user_id
5. Backend query verifies user exists
6. Backend injects User object into route handler
7. Route handler performs operation with user context

### Data Isolation Strategy

**Database-Level Isolation**:
- Foreign key constraint: `tasks.user_id` references `users.id` with ON DELETE CASCADE
- All task queries include `WHERE user_id = :current_user_id` filter
- Database indexes on `user_id` column for query performance

**Service-Level Isolation**:
- Task service methods accept `user_id` parameter (from JWT token)
- All CRUD operations automatically scope to user_id
- Get/Update/Delete operations validate ownership before execution
- Unauthorized access attempts return 403 Forbidden

**API-Level Isolation**:
- `get_current_user` dependency extracts user from JWT token
- All task endpoints depend on `get_current_user`
- User object passed to service layer for automatic filtering
- No endpoint accepts user_id as input parameter (always from token)

### Error Handling Strategy

**HTTP Status Codes**:
- `200 OK`: Successful retrieval or update
- `201 Created`: Successful creation (signup, task creation)
- `400 Bad Request`: Validation errors (invalid email, title too long)
- `401 Unauthorized`: Missing/invalid/expired JWT token
- `403 Forbidden`: Valid token but insufficient permissions (accessing other user's task)
- `404 Not Found`: Resource doesn't exist (task not found)
- `500 Internal Server Error`: Unexpected server errors (database connection failure)

**Error Response Format**:
```json
{
  "detail": "User-friendly error message",
  "errors": [  // Optional, for validation errors
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

**Exception Handling**:
- FastAPI exception handlers for HTTPException
- Database exceptions wrapped in HTTPException
- Validation errors from Pydantic automatically converted to 400 responses
- Unhandled exceptions caught and logged, return 500 with generic message

## Phase 1: Design and Contracts

### Data Model Design

**User Model** (`app/models/user.py`):
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user", cascade_delete=True)
```

**Task Model** (`app/models/task.py`):
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: User = Relationship(back_populates="tasks")
```

**Database Schema** (PostgreSQL DDL):
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_id_created_at ON tasks(user_id, created_at DESC);
```

### API Contract Specifications

See `specs/001-fullstack-web-app/contracts/auth-api.md` and `specs/001-fullstack-web-app/contracts/tasks-api.md` for detailed API specifications.

**Authentication Endpoints Summary**:

1. **POST `/api/v1/auth/signup`**
   - Request: `{email: string, password: string}`
   - Response: `{access_token: string, token_type: "bearer"}`
   - Errors: 400 (validation), 409 (email exists)

2. **POST `/api/v1/auth/login`**
   - Request: `{email: string, password: string}`
   - Response: `{access_token: string, token_type: "bearer"}`
   - Errors: 400 (validation), 401 (invalid credentials)

**Task Endpoints Summary**:

3. **GET `/api/v1/tasks`**
   - Headers: `Authorization: Bearer <token>`
   - Response: `[{id, user_id, title, description, completed, created_at, updated_at}, ...]`
   - Errors: 401 (unauthorized)

4. **POST `/api/v1/tasks`**
   - Headers: `Authorization: Bearer <token>`
   - Request: `{title: string, description?: string}`
   - Response: `{id, user_id, title, description, completed, created_at, updated_at}`
   - Errors: 400 (validation), 401 (unauthorized)

5. **PATCH `/api/v1/tasks/{id}`**
   - Headers: `Authorization: Bearer <token>`
   - Request: `{title?: string, description?: string, completed?: boolean}`
   - Response: `{id, user_id, title, description, completed, created_at, updated_at}`
   - Errors: 400 (validation), 401 (unauthorized), 403 (forbidden), 404 (not found)

6. **DELETE `/api/v1/tasks/{id}`**
   - Headers: `Authorization: Bearer <token>`
   - Response: 204 No Content
   - Errors: 401 (unauthorized), 403 (forbidden), 404 (not found)

7. **POST `/api/v1/tasks/{id}/toggle`**
   - Headers: `Authorization: Bearer <token>`
   - Response: `{id, user_id, title, description, completed, created_at, updated_at}`
   - Errors: 401 (unauthorized), 403 (forbidden), 404 (not found)

### Configuration Management

**Backend Environment Variables** (`.env`):
```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host/dbname

# JWT Configuration
SECRET_KEY=<generated-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours

# CORS
FRONTEND_URL=http://localhost:3000

# Application
DEBUG=true
LOG_LEVEL=INFO
```

**Frontend Environment Variables** (`.env.local`):
```env
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Application
NEXT_PUBLIC_APP_NAME=Todo App
```

### Testing Strategy

**Backend Testing** (pytest):
- **Unit Tests**: Service layer logic (password hashing, JWT generation, task CRUD)
- **Integration Tests**: API endpoints with test database
- **Contract Tests**: Request/response schema validation
- **Fixtures**: Test database, test client, authenticated test users

**Frontend Testing** (Jest + React Testing Library):
- **Component Tests**: TaskList, TaskForm, TaskItem rendering and interaction
- **Integration Tests**: Page-level tests with mocked API responses
- **E2E Tests** (optional): Playwright tests for critical user flows

**Test Data Strategy**:
- Test database created/destroyed per test session
- Fixtures create test users with known credentials
- Each test creates its own tasks for isolation
- Cleanup handled by database teardown

## Phase 2: Implementation Strategy

Implementation will follow Red-Green-Refactor TDD methodology:

1. **Backend Setup**: Project structure, dependencies, configuration
2. **Database Layer**: Models, migrations, database connection
3. **Authentication Service**: Password hashing, JWT generation/validation
4. **Authentication API**: Signup and login endpoints with tests
5. **Task Service**: CRUD operations with user isolation
6. **Task API**: Task endpoints with tests
7. **Frontend Setup**: Project structure, dependencies, configuration
8. **Frontend Auth**: Signup, login pages, token storage, auth context
9. **Frontend Tasks**: Task dashboard, list, form, item components
10. **Integration Testing**: End-to-end user flows
11. **Documentation**: API documentation, setup guides, deployment instructions

Each step delivers tested, working functionality before proceeding to the next.

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Neon PostgreSQL connection issues | High - app won't function | Medium | Test connection early, provide clear error messages, document connection string format |
| JWT token expiration handling | Medium - user experience | Medium | Implement token refresh mechanism or clear error messages with re-login prompt |
| CORS configuration errors | High - frontend can't communicate | Medium | Document CORS setup, test cross-origin requests early |
| Password hashing performance | Low - slow signup/login | Low | Use appropriate bcrypt cost factor (12), consider caching strategies |
| Data isolation bugs | Critical - security vulnerability | Low | Comprehensive tests for cross-user access attempts, code review of all queries |
| Database migration conflicts | Medium - deployment issues | Low | Use Alembic for version control, test migrations on staging database |

## Success Metrics

- All 8 API endpoints implemented and tested (100% coverage)
- All 40 functional requirements (FR-001 through FR-040) satisfied
- All 17 success criteria (SC-001 through SC-017) met
- <500ms API response time for 95th percentile
- Zero cross-user data access in security testing
- 100% test pass rate for backend (pytest) and frontend (Jest)
- Complete API documentation with examples
- Deployment-ready configuration for backend and frontend

## Next Steps

1. **Approve this plan**: Review and approve this implementation plan
2. **Generate tasks**: Run `/sp.tasks` to create actionable task list from this plan
3. **Begin implementation**: Execute tasks in order with TDD methodology
4. **Create PHRs**: Document progress with Prompt History Records
5. **Suggest ADRs**: Identify architectural decisions requiring documentation
