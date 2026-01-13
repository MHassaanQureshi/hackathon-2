# Research & Technology Decisions: Phase II Full-Stack Web Application

**Feature**: 001-fullstack-web-app
**Date**: 2026-01-08
**Status**: Completed

## Purpose

This document consolidates technology choices, best practices, and architectural patterns researched for Phase II implementation. All decisions are made in accordance with the project constitution and Phase II specification requirements.

## Technology Stack Decisions

### Backend Framework: FastAPI

**Decision**: Use FastAPI 0.100+ with Python 3.11+

**Rationale**:
- Mandated by project constitution (Section IV: Technology Constraints)
- Native async/await support for high-performance I/O operations
- Automatic OpenAPI documentation generation for API contract validation
- Built-in request/response validation using Pydantic models
- Excellent ecosystem support for JWT authentication and database integration

**Alternatives Considered**:
- Flask: Considered but rejected - lacks native async support and type safety
- Django: Considered but rejected - too heavyweight for Phase II scope, includes features outside requirements (admin panel, ORM migration complexity)

**Best Practices**:
- Use dependency injection for database sessions and authentication
- Implement middleware for CORS and JWT validation
- Structure as layered architecture: routes → services → data access
- Use Pydantic schemas for request/response validation
- Enable automatic interactive API documentation at `/docs`

### ORM: SQLModel

**Decision**: Use SQLModel 0.0.14+ with type hints

**Rationale**:
- Mandated by project constitution
- Combines Pydantic validation with SQLAlchemy ORM capabilities
- Type-safe database operations with full IDE autocomplete support
- Simplifies schema definition with single model for DB and API
- Native support for async operations with async sessions

**Alternatives Considered**:
- Raw SQLAlchemy: Considered but rejected - more verbose, lacks Pydantic integration
- Django ORM: Not applicable (Django framework not selected)

**Best Practices**:
- Define models with SQLModel.table=True for database tables
- Use Pydantic models (SQLModel without table=True) for API schemas
- Implement relationship loading strategies (selectinload for N+1 prevention)
- Use async sessions for all database operations
- Implement proper connection pooling for Neon PostgreSQL

### Database: Neon PostgreSQL

**Decision**: Use Neon serverless PostgreSQL

**Rationale**:
- Mandated by project constitution and specification
- Serverless architecture with automatic scaling
- PostgreSQL compatibility ensures feature parity with traditional PostgreSQL
- Built-in connection pooling reduces overhead
- Generous free tier for development and Phase II requirements

**Configuration**:
- Connection string via environment variable: `DATABASE_URL`
- Use asyncpg driver for async PostgreSQL operations
- Enable SSL mode for secure connections
- Connection pool size: 5-10 for Phase II (single-user to small team)

**Best Practices**:
- Use database migrations for schema management (Alembic)
- Implement proper error handling for connection failures
- Use indexes on foreign keys (user_id in tasks table)
- Enable query logging in development for debugging

### Authentication: JWT (JSON Web Tokens)

**Decision**: Use python-jose 3.3+ with passlib 1.7+ for JWT and password hashing

**Rationale**:
- Stateless authentication required by specification (FR-007)
- Industry-standard approach for REST API authentication
- No server-side session storage needed (aligns with cloud-native principles)
- Cross-origin support for separate frontend/backend architecture

**Implementation Details**:
- Algorithm: HS256 (symmetric key signing)
- Token expiration: 24 hours (configurable via environment)
- Password hashing: bcrypt with cost factor 12
- Token payload: user_id, email, expiration timestamp

**Alternatives Considered**:
- Session-based auth: Rejected - violates stateless requirement (FR-007)
- OAuth2 with external providers: Out of scope for Phase II
- API keys: Considered but rejected - less secure, no expiration mechanism

**Best Practices**:
- Store JWT secret in environment variables, never in code
- Validate token signature, expiration, and structure on every request
- Use HTTPBearer security scheme with FastAPI dependencies
- Implement token refresh mechanism for future phases (not Phase II)
- Never log tokens or passwords

### Frontend Framework: Next.js

**Decision**: Use Next.js 14+ with React 18+ and TypeScript 5+

**Rationale**:
- Mandated by project constitution
- Server-side rendering (SSR) capabilities for improved performance
- Built-in routing with file-based structure
- TypeScript support for type-safe API integration
- Excellent developer experience with hot reload

**Project Structure**:
- App Router (Next.js 13+ architecture)
- API client layer for backend communication
- Component-based UI architecture
- Environment-based configuration for backend URL

**Best Practices**:
- Use client components for interactive UI (task list, forms)
- Implement proper error boundaries for error handling
- Store JWT token in httpOnly cookies or secure localStorage
- Use React hooks for state management (useState, useEffect)
- Implement loading and error states for all API calls

### API Client: Fetch API with TypeScript

**Decision**: Use native Fetch API with TypeScript types

**Rationale**:
- Built into modern browsers (no additional dependency)
- Promise-based async interface aligns with async/await
- Simple integration with Next.js and React
- Easy to wrap in custom API client class for centralized config

**Alternatives Considered**:
- Axios: Considered but rejected - adds dependency, native fetch sufficient for Phase II
- React Query: Out of scope - adds complexity, Phase II doesn't need advanced caching

**Best Practices**:
- Create centralized API client class with base URL and auth headers
- Implement request/response interceptors for JWT token injection
- Handle common HTTP errors (401, 403, 404, 500) globally
- Use TypeScript interfaces matching backend schemas
- Implement proper timeout handling

## Architecture Patterns

### Layered Architecture (Backend)

**Pattern**: Three-layer architecture with clear separation

**Layers**:
1. **API Layer** (routes): HTTP request/response handling, validation
2. **Service Layer** (services): Business logic, authorization checks
3. **Data Access Layer** (models): Database operations, queries

**Rationale**:
- Aligns with clean architecture principle (Constitution V)
- Clear separation of concerns
- Testable in isolation (unit tests per layer)
- Easy to modify one layer without affecting others

**Implementation**:
```
backend/src/
├── api/           # FastAPI routers (endpoints)
│   ├── auth.py    # POST /auth/signup, /auth/login
│   └── tasks.py   # CRUD endpoints for tasks
├── services/      # Business logic
│   ├── auth.py    # User creation, password verification, token generation
│   └── tasks.py   # Task CRUD logic, ownership validation
├── models/        # SQLModel definitions
│   ├── user.py    # User table model
│   └── task.py    # Task table model
└── core/          # Cross-cutting concerns
    ├── config.py  # Environment configuration
    ├── database.py # DB session management
    └── security.py # JWT utilities, password hashing
```

### Component-Based Architecture (Frontend)

**Pattern**: React component hierarchy with shared components

**Structure**:
```
frontend/src/
├── app/              # Next.js app router
│   ├── page.tsx      # Landing/login page
│   ├── signup/
│   │   └── page.tsx  # Signup page
│   └── tasks/
│       └── page.tsx  # Task list page (protected)
├── components/       # Reusable UI components
│   ├── TaskList.tsx  # Display list of tasks
│   ├── TaskItem.tsx  # Individual task display/edit
│   ├── TaskForm.tsx  # Create/edit task form
│   └── AuthForm.tsx  # Login/signup form
├── lib/              # Utilities and API client
│   ├── api.ts        # API client class
│   ├── auth.ts       # Auth utilities (token storage)
│   └── types.ts      # TypeScript interfaces
└── hooks/            # Custom React hooks
    ├── useAuth.tsx   # Authentication state hook
    └── useTasks.tsx  # Task operations hook
```

**Rationale**:
- Reusable components reduce duplication
- Clear separation between pages (routing) and components (UI)
- Custom hooks encapsulate API logic and state management
- Type-safe interfaces ensure frontend-backend contract compliance

## Error Handling Strategy

### Backend Error Handling

**Strategy**: Centralized exception handling with HTTPException

**Implementation**:
- Use FastAPI HTTPException for all API errors
- Custom exception classes for domain errors (InvalidCredentials, TaskNotFound, UnauthorizedAccess)
- Global exception handler for unexpected errors (500)
- Structured error responses with consistent format

**Error Response Format**:
```json
{
  "detail": "User-friendly error message",
  "error_code": "INVALID_CREDENTIALS",
  "field_errors": {  // Optional, for validation errors
    "title": "Title must be 100 characters or less"
  }
}
```

**Best Practices**:
- Map domain exceptions to appropriate HTTP status codes
- Never expose stack traces or internal details in production
- Log all errors with context (user_id, request_id) for debugging
- Implement request ID tracking for error correlation

### Frontend Error Handling

**Strategy**: Error boundaries + inline error states

**Implementation**:
- React Error Boundary for catastrophic errors
- Per-component error state for API failures
- Toast notifications for user-friendly feedback
- Retry mechanisms for transient failures

**Best Practices**:
- Display specific error messages from backend
- Implement loading states to prevent double-submissions
- Clear errors when user retries action
- Graceful degradation for non-critical failures

## Security Considerations

### Password Security

**Requirements**:
- Hash all passwords with bcrypt (cost factor 12)
- Never log passwords or password hashes
- Validate password strength on frontend and backend
- Minimum 8 characters (per specification assumptions)

### JWT Security

**Requirements**:
- Sign tokens with strong secret (32+ character random string)
- Rotate secrets periodically (operational concern, not Phase II)
- Validate signature, expiration, and structure on every request
- Never include sensitive data in JWT payload (email is acceptable, password is not)

### CORS Configuration

**Requirements**:
- Allow specific frontend origin only (not wildcard *)
- Enable credentials (cookies, auth headers)
- Restrict allowed methods to required set (GET, POST, PATCH, DELETE)
- Implement CORS middleware in FastAPI

### SQL Injection Prevention

**Mitigation**:
- Use parameterized queries via SQLModel/SQLAlchemy (automatic protection)
- Never construct raw SQL with string interpolation
- Validate all input data types and formats

## Environment Configuration

### Backend Environment Variables

Required environment variables for backend:
```
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
JWT_SECRET=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
ENVIRONMENT=development|production
```

**Best Practices**:
- Use .env files for development (never commit to git)
- Use platform-specific secrets management in production
- Validate required variables at startup
- Provide sensible defaults for non-sensitive values

### Frontend Environment Variables

Required environment variables for frontend:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development|production
```

**Best Practices**:
- Prefix with NEXT_PUBLIC_ for browser-accessible variables
- Never expose backend secrets in frontend env
- Use different values per environment (dev, staging, prod)

## Database Schema Design

### Migration Strategy

**Tool**: Alembic (SQLAlchemy migration tool)

**Workflow**:
1. Define models in SQLModel
2. Generate migration from models: `alembic revision --autogenerate -m "description"`
3. Review and adjust migration file
4. Apply migration: `alembic upgrade head`
5. Commit migration file to version control

**Best Practices**:
- Always review auto-generated migrations
- Test migrations on development database first
- Implement rollback scripts for all migrations
- Use semantic migration naming (001_create_users, 002_create_tasks)

### Index Strategy

**Indexes Required**:
- tasks.user_id: B-tree index for fast user-scoped queries
- users.email: Unique index for email uniqueness and fast lookup

**Rationale**:
- user_id index critical for SC-005 (500ms response time)
- Supports WHERE user_id = ? filtering in all task queries
- Email index enables fast authentication lookups

## Testing Strategy

### Backend Testing

**Framework**: pytest with pytest-asyncio

**Test Levels**:
1. **Unit Tests**: Test services and utilities in isolation
2. **Integration Tests**: Test API endpoints with test database
3. **Contract Tests**: Validate API responses match OpenAPI schema

**Best Practices**:
- Use in-memory SQLite for unit tests (fast)
- Use dedicated test PostgreSQL database for integration tests
- Mock external dependencies (database in unit tests)
- Test authentication and authorization for all protected endpoints
- Test all error cases (401, 403, 404, 400, 500)

### Frontend Testing

**Framework**: Jest with React Testing Library

**Test Levels**:
1. **Component Tests**: Test UI components in isolation
2. **Integration Tests**: Test component interactions
3. **E2E Tests** (optional Phase II): Test full user flows

**Best Practices**:
- Mock API calls in component tests
- Test user interactions (click, input, submit)
- Test loading and error states
- Use data-testid attributes for stable selectors

## Deployment Considerations

### Backend Deployment

**Target**: Cloud platform with Python support (Render, Vercel Functions, AWS Lambda)

**Requirements**:
- Python 3.11+ runtime
- Environment variable support
- PostgreSQL connectivity to Neon
- HTTPS enforcement

**Build Process**:
1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `alembic upgrade head`
3. Start server: `uvicorn main:app --host 0.0.0.0 --port 8000`

### Frontend Deployment

**Target**: Vercel (optimal for Next.js) or Netlify

**Requirements**:
- Node.js 18+ runtime
- Environment variable support
- Static site generation + API routes support
- HTTPS enforcement

**Build Process**:
1. Install dependencies: `npm install`
2. Build production assets: `npm run build`
3. Start server: `npm start` (or use platform's automatic deployment)

## Performance Optimization

### Database Query Optimization

**Strategies**:
- Use selectinload for N+1 query prevention
- Implement pagination for task lists (future enhancement)
- Use database indexes on frequently queried fields
- Connection pooling for reduced connection overhead

### Frontend Performance

**Strategies**:
- Code splitting with Next.js dynamic imports (future enhancement)
- Optimize images with Next.js Image component
- Minimize bundle size (avoid unnecessary dependencies)
- Implement client-side caching for task list (future enhancement)

## Phase Isolation Compliance

### Excluded Technologies (per FR-036 to FR-040)

**NOT Included in Phase II**:
- AI/NLP libraries (transformers, spaCy, NLTK)
- OpenAI SDK or API integration
- Chatbot frameworks
- MCP (Model Context Protocol) tools
- Kafka message broker
- Dapr distributed runtime
- Kubernetes orchestration
- Any natural language processing

**Enforcement**:
- No dependencies on excluded libraries in requirements.txt or package.json
- No placeholder code for future AI features
- No stub endpoints for chatbot integration
- Clear architectural boundaries for future phase integration

### Future Phase Readiness (per SC-016)

**Architecture Decisions for Phase III+ Compatibility**:
- Use RESTful API design (can be extended with new endpoints)
- Stateless authentication (supports scaling to distributed systems)
- Service layer separation (can be extracted to microservices)
- Environment-based configuration (supports multi-environment deployment)
- Database schema designed for extensibility (additional tables can be added)

## Risk Mitigation

### Database Connection Failures

**Risk**: Neon database connection loss during operation

**Mitigation**:
- Implement connection retry logic with exponential backoff
- Use connection pooling to minimize connection churn
- Return 503 Service Unavailable with retry-after header
- Log connection failures for operational monitoring

### Token Expiration

**Risk**: JWT token expires during active user session

**Mitigation**:
- Set reasonable expiration (24 hours per spec assumptions)
- Return 401 Unauthorized with clear error message
- Redirect user to login page on frontend
- Future enhancement: Implement refresh tokens (Phase III+)

### Concurrent Task Updates

**Risk**: Same user updates task from multiple tabs/devices

**Mitigation**:
- Use database-level locking or optimistic concurrency (future enhancement)
- Phase II: Last write wins (acceptable for single-user scenario)
- Include updated_at timestamp in responses for conflict detection

## Summary

All technology decisions align with:
- Project constitution requirements (FastAPI, SQLModel, Next.js, Neon PostgreSQL)
- Phase II specification (JWT auth, REST API, user-scoped data)
- Phase isolation requirements (no AI, MCP, Kafka, Kubernetes)
- Quality principles (clean architecture, stateless services, separation of concerns)

The architecture is designed for:
- Independent development and testing of frontend/backend
- Horizontal scalability for future phases
- Clear separation of concerns for maintainability
- Type safety across the full stack
- Testability at all levels

All unknowns from Technical Context have been resolved. Ready to proceed to Phase 1 (data model and contracts).
