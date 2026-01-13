# Quickstart Guide: Phase II Full-Stack Web Application

**Feature**: 001-fullstack-web-app
**Date**: 2026-01-08
**Audience**: Developers implementing Phase II

## Overview

This guide provides the essential information to begin implementing Phase II. It includes setup instructions, directory structure, key workflows, and implementation checklist.

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL client (psql) for database verification
- Neon PostgreSQL database account and connection string
- Git (for version control)

## Project Structure

```
hackathon-2/
├── backend/                    # FastAPI backend application
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── api/               # API routes (endpoints)
│   │   │   ├── __init__.py
│   │   │   ├── auth.py        # /auth/signup, /auth/login
│   │   │   └── tasks.py       # /tasks endpoints
│   │   ├── services/          # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── auth.py        # User creation, authentication
│   │   │   └── tasks.py       # Task CRUD logic
│   │   ├── models/            # SQLModel database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py        # User model
│   │   │   └── task.py        # Task model
│   │   └── core/              # Cross-cutting concerns
│   │       ├── __init__.py
│   │       ├── config.py      # Environment configuration
│   │       ├── database.py    # DB session management
│   │       └── security.py    # JWT + password utilities
│   ├── tests/                 # Backend tests
│   │   ├── conftest.py        # Pytest fixtures
│   │   ├── test_auth.py       # Authentication tests
│   │   └── test_tasks.py      # Task CRUD tests
│   ├── alembic/               # Database migrations
│   │   ├── versions/          # Migration scripts
│   │   └── env.py             # Alembic config
│   ├── alembic.ini            # Alembic configuration file
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables (not committed)
│
├── frontend/                  # Next.js frontend application
│   ├── src/
│   │   ├── app/               # Next.js app router
│   │   │   ├── page.tsx       # Landing/login page
│   │   │   ├── signup/
│   │   │   │   └── page.tsx   # Signup page
│   │   │   └── tasks/
│   │   │       └── page.tsx   # Task list (protected)
│   │   ├── components/        # React components
│   │   │   ├── TaskList.tsx   # Task list display
│   │   │   ├── TaskItem.tsx   # Single task component
│   │   │   ├── TaskForm.tsx   # Create/edit form
│   │   │   └── AuthForm.tsx   # Login/signup form
│   │   ├── lib/               # Utilities
│   │   │   ├── api.ts         # API client class
│   │   │   ├── auth.ts        # Auth utilities
│   │   │   └── types.ts       # TypeScript interfaces
│   │   └── hooks/             # Custom hooks
│   │       ├── useAuth.tsx    # Authentication hook
│   │       └── useTasks.tsx   # Task operations hook
│   ├── tests/                 # Frontend tests
│   │   ├── components/        # Component tests
│   │   └── lib/               # Utility tests
│   ├── package.json           # Node dependencies
│   ├── tsconfig.json          # TypeScript configuration
│   ├── next.config.js         # Next.js configuration
│   └── .env.local             # Environment variables (not committed)
│
├── specs/                     # Feature specifications
│   └── 001-fullstack-web-app/
│       ├── spec.md            # Phase II specification
│       ├── plan.md            # This implementation plan
│       ├── research.md        # Technology decisions
│       ├── data-model.md      # Database schema
│       ├── quickstart.md      # This file
│       └── contracts/
│           └── openapi.yaml   # API contract
│
└── .specify/                  # Project governance
    ├── memory/
    │   └── constitution.md    # Project constitution
    └── templates/             # Document templates
```

## Quick Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql+asyncpg://user:password@host/database
JWT_SECRET=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
EOF

# Initialize database migrations
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Create users and tasks tables"

# Apply migrations
alembic upgrade head

# Run development server
uvicorn src.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env.local file
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_ENVIRONMENT=development
EOF

# Run development server
npm run dev
```

### 3. Verify Setup

```bash
# Test backend health
curl http://localhost:8000/api/v1/docs  # Should show OpenAPI docs

# Test frontend
open http://localhost:3000  # Should show landing page
```

## Implementation Workflow

### Phase Sequence

Implementation follows the Spec-Driven Development workflow:

1. ✅ **Constitution** → Established (see `.specify/memory/constitution.md`)
2. ✅ **Specification** → Complete (see `specs/001-fullstack-web-app/spec.md`)
3. ✅ **Planning** → Complete (see `specs/001-fullstack-web-app/plan.md`)
4. ⏳ **Tasks** → Next step (run `/sp.tasks` to generate task list)
5. ⏳ **Implementation** → Execute tasks in order (TDD approach)

### Development Approach

**Test-Driven Development (TDD)**: Red → Green → Refactor

1. **Red**: Write failing test for requirement
2. **Green**: Write minimal code to pass test
3. **Refactor**: Improve code while keeping tests green

### Task Execution Order

Tasks will be organized by user story priority:

1. **P1 Tasks**: User Registration and Authentication
   - Setup project structure
   - Implement database models
   - Implement authentication endpoints (/auth/signup, /auth/login)
   - Implement JWT utilities
   - Test authentication flow

2. **P2 Tasks**: Task Creation and Viewing
   - Implement task model
   - Implement GET /tasks and POST /tasks endpoints
   - Test task creation and listing
   - Verify user-scoped access

3. **P3 Tasks**: Task Management
   - Implement PATCH /tasks/{id} endpoint
   - Implement DELETE /tasks/{id} endpoint
   - Implement POST /tasks/{id}/toggle endpoint
   - Test update and delete operations
   - Verify authorization (403 Forbidden for other users' tasks)

4. **Frontend Tasks**: User Interface
   - Implement authentication pages (login, signup)
   - Implement task list page
   - Implement API client and hooks
   - Connect frontend to backend
   - E2E testing

## Key Implementation Guidelines

### Backend Guidelines

1. **Layered Architecture**:
   - Routes → Services → Data Access
   - No business logic in routes
   - No HTTP concerns in services

2. **Dependency Injection**:
   - Use FastAPI Depends for database sessions
   - Use Depends for JWT authentication
   - Makes testing easier (can mock dependencies)

3. **Error Handling**:
   - Raise HTTPException from routes
   - Use custom exception classes in services
   - Map exceptions to HTTP status codes in routes

4. **Database Sessions**:
   - Use async sessions for all operations
   - Always close sessions (use dependency injection)
   - Commit on success, rollback on error

5. **Security**:
   - Hash all passwords with bcrypt before storage
   - Validate JWT on every protected endpoint
   - Never log passwords or tokens
   - Filter tasks by user_id in all queries

### Frontend Guidelines

1. **Component Structure**:
   - Keep components focused (single responsibility)
   - Use TypeScript for type safety
   - Props interface for every component

2. **State Management**:
   - Use React hooks (useState, useEffect)
   - Custom hooks for API operations
   - Context for global state (auth)

3. **API Integration**:
   - Centralized API client class
   - Automatic token injection
   - Consistent error handling

4. **Error Handling**:
   - Display user-friendly error messages
   - Loading states for async operations
   - Retry mechanisms for transient failures

5. **Security**:
   - Store JWT in httpOnly cookie or secure localStorage
   - Clear token on logout
   - Redirect to login on 401 errors

## Testing Strategy

### Backend Tests

```bash
# Run all backend tests
cd backend
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run specific test function
pytest tests/test_auth.py::test_signup_success
```

**Test Categories**:
- **Unit Tests**: Test services and utilities in isolation
- **Integration Tests**: Test API endpoints with test database
- **Contract Tests**: Validate responses match OpenAPI schema

### Frontend Tests

```bash
# Run all frontend tests
cd frontend
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- TaskList.test.tsx
```

**Test Categories**:
- **Component Tests**: Test UI components with mocked data
- **Integration Tests**: Test component interactions
- **E2E Tests** (optional): Test full user workflows

## Common Commands

### Backend

```bash
# Start development server
uvicorn src.main:app --reload

# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Run tests
pytest

# Format code
black src tests

# Lint code
pylint src tests
```

### Frontend

```bash
# Start development server
npm run dev

# Build production bundle
npm run build

# Start production server
npm start

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

## Environment Variables Reference

### Backend (.env)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| DATABASE_URL | Yes | postgresql+asyncpg://... | Neon PostgreSQL connection string |
| JWT_SECRET | Yes | random-32-char-string | Secret key for JWT signing |
| JWT_ALGORITHM | Yes | HS256 | JWT signing algorithm |
| JWT_EXPIRATION_HOURS | No | 24 | Token expiration time (default: 24) |
| CORS_ORIGINS | Yes | http://localhost:3000 | Allowed CORS origins (comma-separated) |
| ENVIRONMENT | No | development | Current environment |

### Frontend (.env.local)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| NEXT_PUBLIC_API_URL | Yes | http://localhost:8000/api/v1 | Backend API base URL |
| NEXT_PUBLIC_ENVIRONMENT | No | development | Current environment |

## API Documentation

Once the backend is running, access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Troubleshooting

### Backend Issues

**Problem**: Database connection error
```
Solution: Verify DATABASE_URL in .env
Check: psql <DATABASE_URL> (should connect successfully)
```

**Problem**: Module not found errors
```
Solution: Ensure virtual environment is activated
Check: which python (should point to venv/bin/python)
Run: pip install -r requirements.txt
```

**Problem**: Migration errors
```
Solution: Check alembic/env.py configuration
Verify: Database user has CREATE TABLE permissions
Try: alembic downgrade -1 && alembic upgrade head
```

### Frontend Issues

**Problem**: API connection refused
```
Solution: Verify backend is running on port 8000
Check: curl http://localhost:8000/api/v1/docs
Verify: NEXT_PUBLIC_API_URL in .env.local
```

**Problem**: CORS errors
```
Solution: Verify CORS_ORIGINS in backend .env includes http://localhost:3000
Check: Browser console for specific CORS error
```

**Problem**: TypeScript errors
```
Solution: Run npm run type-check
Fix: Update types in lib/types.ts to match backend schemas
```

## Next Steps

1. **Generate Tasks**: Run `/sp.tasks` to create detailed task list
2. **Review Tasks**: Verify tasks cover all functional requirements
3. **Start Implementation**: Execute tasks in priority order (P1 → P2 → P3)
4. **Test Continuously**: Run tests after each task completion
5. **Commit Frequently**: Commit after each passing test

## Reference Documents

- **Specification**: `specs/001-fullstack-web-app/spec.md` - What to build
- **Implementation Plan**: `specs/001-fullstack-web-app/plan.md` - How to build it
- **Data Model**: `specs/001-fullstack-web-app/data-model.md` - Database schema
- **API Contract**: `specs/001-fullstack-web-app/contracts/openapi.yaml` - API specification
- **Research**: `specs/001-fullstack-web-app/research.md` - Technology decisions
- **Constitution**: `.specify/memory/constitution.md` - Project governance

## Success Criteria Checklist

Before considering Phase II complete, verify:

- [ ] All 40 functional requirements (FR-001 to FR-040) implemented
- [ ] All 17 success criteria (SC-001 to SC-017) met
- [ ] All API endpoints match OpenAPI contract
- [ ] All tests passing (backend + frontend)
- [ ] User-scoped data isolation verified (SC-004, SC-006)
- [ ] Authentication flow working (SC-001, SC-002)
- [ ] Task CRUD operations working (SC-009)
- [ ] Error handling complete (401, 403, 404, 400, 500)
- [ ] Performance requirements met (SC-005, SC-008)
- [ ] Phase isolation verified (FR-036 to FR-040)
- [ ] No Phase I or Phase III code present
- [ ] Documentation complete

## Support

For issues during implementation:

1. Review specification for requirement clarity
2. Check research.md for technology decisions
3. Verify against OpenAPI contract
4. Consult data-model.md for database questions
5. Create clarification request if spec is ambiguous
