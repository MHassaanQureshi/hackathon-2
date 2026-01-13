# Phase II Backend - FastAPI Todo Application

FastAPI backend with JWT authentication and SQLModel + Neon PostgreSQL persistence.

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Neon PostgreSQL database (or local PostgreSQL instance)
- pip or poetry for dependency management

### Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration values
   ```

4. **Generate SECRET_KEY** (if not already set):
   ```bash
   openssl rand -hex 32
   # Copy the output to SECRET_KEY in .env
   ```

### Running the Application

**Development mode** (with auto-reload):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the application is running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Authentication Endpoints

#### POST `/api/v1/auth/signup`
Register a new user account.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Success Response (201 Created)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid email format or password too short
- `409 Conflict`: Email already registered

#### POST `/api/v1/auth/login`
Authenticate existing user.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Success Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid email format
- `401 Unauthorized`: Invalid email or password

### Task Endpoints

All task endpoints require authentication via `Authorization: Bearer <token>` header.

#### GET `/api/v1/tasks`
Retrieve all tasks for the authenticated user.

**Success Response (200 OK)**:
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Complete project",
    "description": "Finish Phase II implementation",
    "completed": false,
    "created_at": "2026-01-08T12:00:00Z",
    "updated_at": "2026-01-08T12:00:00Z"
  }
]
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid token

#### POST `/api/v1/tasks`
Create a new task.

**Request Body**:
```json
{
  "title": "Task title (max 100 characters)",
  "description": "Optional description (max 500 characters)"
}
```

**Success Response (201 Created)**:
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "created_at": "2026-01-08T12:00:00Z",
  "updated_at": "2026-01-08T12:00:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Title missing, too long, or validation failed
- `401 Unauthorized`: Missing or invalid token

#### PATCH `/api/v1/tasks/{id}`
Update an existing task.

**Request Body** (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Success Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2026-01-08T12:00:00Z",
  "updated_at": "2026-01-08T12:30:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Validation failed
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Task belongs to another user
- `404 Not Found`: Task does not exist

#### DELETE `/api/v1/tasks/{id}`
Delete a task.

**Success Response (204 No Content)**:
No response body.

**Error Responses**:
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Task belongs to another user
- `404 Not Found`: Task does not exist

#### POST `/api/v1/tasks/{id}/toggle`
Toggle task completion status.

**Success Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Task title",
  "description": "Task description",
  "completed": true,
  "created_at": "2026-01-08T12:00:00Z",
  "updated_at": "2026-01-08T12:30:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Task belongs to another user
- `404 Not Found`: Task does not exist

## Testing

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_auth.py
```

## Architecture

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and environment variables
│   ├── database.py          # Database connection and session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User SQLModel
│   │   └── task.py          # Task SQLModel
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py          # Auth request/response schemas
│   │   └── task.py          # Task request/response schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication service
│   │   └── task.py          # Task service
│   └── api/
│       ├── __init__.py
│       ├── deps.py          # Dependency injection
│       └── v1/
│           ├── __init__.py
│           ├── auth.py      # Auth routes
│           └── tasks.py     # Task routes
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py         # Authentication tests
│   └── test_tasks.py        # Task tests
├── requirements.txt
├── .env.example
└── README.md
```

### Clean Architecture

The application follows clean architecture principles with clear separation of concerns:

1. **Models Layer** (`app/models/`): SQLModel database entities
2. **Services Layer** (`app/services/`): Business logic (password hashing, JWT, CRUD operations)
3. **API Layer** (`app/api/`): REST endpoints and request/response handling
4. **Configuration** (`app/config.py`): Environment-based configuration
5. **Database** (`app/database.py`): Database connection and session management

### Authentication Flow

1. User signs up or logs in via `/api/v1/auth/signup` or `/api/v1/auth/login`
2. Backend hashes password (bcrypt cost 12), creates/verifies user, generates JWT
3. JWT contains `sub` (user_id), `email`, `exp` (expiration), `iat` (issued at)
4. Frontend stores JWT in localStorage
5. All task endpoints require `Authorization: Bearer <token>` header
6. `get_current_user` dependency validates JWT, extracts user_id, queries user
7. Services enforce user-scoped data access (users see only their own tasks)

### Data Isolation

- **Database Level**: Foreign key `tasks.user_id` references `users.id` with CASCADE
- **Service Level**: All task queries filter by `user_id` from authenticated user
- **API Level**: `get_current_user` dependency extracts user from JWT token
- Cross-user access attempts return `403 Forbidden`

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Tasks Table

```sql
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

## Deployment

### Environment Variables

Ensure the following environment variables are set in production:

- `DATABASE_URL`: Neon PostgreSQL connection string
- `SECRET_KEY`: Secure random key (generate with `openssl rand -hex 32`)
- `ALGORITHM`: `HS256` (recommended)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 1440 = 24 hours)
- `FRONTEND_URL`: Frontend URL for CORS (e.g., `https://yourdomain.com`)
- `DEBUG`: `false` in production
- `LOG_LEVEL`: `INFO` or `WARNING` in production

### Production Considerations

1. **HTTPS**: Enforce HTTPS at the infrastructure level (reverse proxy, load balancer)
2. **CORS**: Set `FRONTEND_URL` to your actual frontend domain
3. **Database**: Use Neon PostgreSQL or managed PostgreSQL instance
4. **Secret Key**: Generate a new secure key, never use the example value
5. **Workers**: Use multiple Uvicorn workers for production (`--workers 4`)
6. **Monitoring**: Add logging and monitoring for API endpoints
7. **Rate Limiting**: Consider adding rate limiting middleware for production

## Troubleshooting

### Database Connection Errors

- Verify `DATABASE_URL` format: `postgresql+asyncpg://user:password@host:port/dbname`
- Check Neon PostgreSQL connection string and credentials
- Ensure database is accessible from your network

### JWT Token Errors

- Verify `SECRET_KEY` is set and matches across restarts
- Check token expiration time is reasonable
- Ensure Authorization header format: `Bearer <token>`

### CORS Errors

- Verify `FRONTEND_URL` matches your frontend origin exactly
- Check CORS middleware configuration in `app/main.py`
- Ensure preflight requests (OPTIONS) are handled correctly
