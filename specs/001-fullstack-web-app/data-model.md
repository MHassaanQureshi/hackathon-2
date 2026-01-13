# Data Model: Phase II Full-Stack Web Application

**Feature**: 001-fullstack-web-app
**Date**: 2026-01-08
**Status**: Final

## Overview

This document defines the data model for Phase II, including database entities, relationships, validation rules, and state transitions. The model is derived from the Phase II specification (Key Entities section) and aligned with functional requirements FR-001 through FR-022.

## Entities

### User Entity

**Purpose**: Represents a registered application user with authentication credentials

**Database Table**: `users`

**Fields**:

| Field Name  | Type      | Constraints                                      | Description                          |
|-------------|-----------|--------------------------------------------------|--------------------------------------|
| id          | UUID      | PRIMARY KEY, NOT NULL, DEFAULT gen_random_uuid() | Unique user identifier               |
| email       | String    | UNIQUE, NOT NULL, MAX 255                        | User's email address (login ID)      |
| password    | String    | NOT NULL, MAX 255                                | Bcrypt hashed password               |
| created_at  | Timestamp | NOT NULL, DEFAULT CURRENT_TIMESTAMP              | Account creation timestamp           |
| updated_at  | Timestamp | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE   | Last update timestamp                |

**Validation Rules**:
- **FR-002**: Email must match RFC 5322 email format regex
- **FR-002**: Email must be unique across all users (database constraint)
- **FR-003**: Password must be hashed with bcrypt before storage (never plaintext)
- Minimum password length: 8 characters (validated before hashing)
- Email and password are required fields (cannot be null or empty)

**Indexes**:
- Primary key index on `id` (automatic)
- Unique index on `email` (for fast authentication lookups and uniqueness enforcement)

**Relationships**:
- One user has many tasks (1:N relationship)
- User deletion should cascade to delete all associated tasks (referential integrity)

**State Diagram**: N/A (users have no state transitions in Phase II)

---

### Task Entity

**Purpose**: Represents a todo item owned by a user

**Database Table**: `tasks`

**Fields**:

| Field Name  | Type      | Constraints                                      | Description                          |
|-------------|-----------|--------------------------------------------------|--------------------------------------|
| id          | UUID      | PRIMARY KEY, NOT NULL, DEFAULT gen_random_uuid() | Unique task identifier               |
| user_id     | UUID      | FOREIGN KEY (users.id), NOT NULL, INDEX          | Owner user ID                        |
| title       | String    | NOT NULL, MAX 100                                | Task title                           |
| description | String    | NULLABLE, MAX 500                                | Optional task description            |
| completed   | Boolean   | NOT NULL, DEFAULT FALSE                          | Completion status                    |
| created_at  | Timestamp | NOT NULL, DEFAULT CURRENT_TIMESTAMP              | Task creation timestamp              |
| updated_at  | Timestamp | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE   | Last update timestamp                |

**Validation Rules**:
- **FR-009**: Title is required (not null, not empty string, not only whitespace)
- **FR-009**: Title maximum 100 characters
- **FR-010**: Description is optional (nullable)
- **FR-010**: Description maximum 500 characters (when provided)
- **FR-022**: Completed defaults to false on task creation
- **FR-012**: Every task must be associated with a valid user (foreign key constraint)

**Indexes**:
- Primary key index on `id` (automatic)
- Index on `user_id` (for fast user-scoped queries - critical for SC-005 performance requirement)
- Composite index on `(user_id, created_at DESC)` for efficient sorted retrieval

**Relationships**:
- Many tasks belong to one user (N:1 relationship)
- Foreign key `user_id` references `users.id`
- ON DELETE CASCADE: When user is deleted, all their tasks are deleted

**State Diagram**:

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  [Initial State]                                    │
│  completed = false                                  │
│  (created via POST /api/v1/tasks)                   │
│                                                     │
└─────────────┬───────────────────────────────────────┘
              │
              │ POST /api/v1/tasks/{id}/toggle
              ├──────────────────────────────────────┐
              │                                      │
              v                                      v
    ┌──────────────────┐                  ┌──────────────────┐
    │  INCOMPLETE      │                  │   COMPLETED      │
    │  completed=false │◄─────────────────│  completed=true  │
    └──────────────────┘                  └──────────────────┘
              ▲         POST /tasks/{id}/toggle      │
              │         or PATCH /tasks/{id}         │
              └──────────────────────────────────────┘

Notes:
- Toggle endpoint flips completed status
- PATCH endpoint can explicitly set completed to true or false
- DELETE endpoint removes task from any state (no state restrictions)
```

## Relationships Diagram

```
┌─────────────────────────────────────┐
│            User                     │
│  ─────────────────────────────────  │
│  id: UUID (PK)                      │
│  email: String (UNIQUE)             │
│  password: String (hashed)          │
│  created_at: Timestamp              │
│  updated_at: Timestamp              │
└──────────────┬──────────────────────┘
               │
               │ 1
               │
               │ owns
               │
               │ N
               │
┌──────────────▼──────────────────────┐
│            Task                     │
│  ─────────────────────────────────  │
│  id: UUID (PK)                      │
│  user_id: UUID (FK → users.id)      │
│  title: String (100 max)            │
│  description: String (500 max)      │
│  completed: Boolean (default false) │
│  created_at: Timestamp              │
│  updated_at: Timestamp              │
└─────────────────────────────────────┘
```

**Relationship Rules**:
- **FR-012**: Each task MUST have exactly one owner (user_id NOT NULL)
- **FR-013**: Users can only retrieve their own tasks (enforced by services layer)
- **FR-015**: Users can only delete their own tasks (enforced by services layer)
- **FR-017**: Tasks belonging to other users are inaccessible (403 Forbidden if attempted)
- **FR-019**: Foreign key constraint ensures referential integrity (tasks cannot reference non-existent users)

## Data Access Patterns

### Common Queries

1. **Authenticate User** (Login):
   ```sql
   SELECT id, email, password, created_at, updated_at
   FROM users
   WHERE email = ?
   ```
   - Used by: POST /api/v1/auth/login
   - Index: email (unique index)
   - Expected: Single row or none

2. **Create User** (Signup):
   ```sql
   INSERT INTO users (id, email, password, created_at, updated_at)
   VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
   ```
   - Used by: POST /api/v1/auth/signup
   - Constraint: Email uniqueness check (raises error if duplicate)

3. **List User Tasks**:
   ```sql
   SELECT id, user_id, title, description, completed, created_at, updated_at
   FROM tasks
   WHERE user_id = ?
   ORDER BY created_at DESC
   ```
   - Used by: GET /api/v1/tasks
   - Index: user_id + created_at (composite)
   - Expected: Multiple rows (0 to N)

4. **Get Single Task**:
   ```sql
   SELECT id, user_id, title, description, completed, created_at, updated_at
   FROM tasks
   WHERE id = ? AND user_id = ?
   ```
   - Used by: PATCH /api/v1/tasks/{id}, DELETE /api/v1/tasks/{id}
   - Index: Primary key (id) + user_id filter
   - Expected: Single row or none (none = 404)

5. **Create Task**:
   ```sql
   INSERT INTO tasks (id, user_id, title, description, completed, created_at, updated_at)
   VALUES (?, ?, ?, ?, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
   ```
   - Used by: POST /api/v1/tasks
   - Constraint: Foreign key validates user_id exists

6. **Update Task**:
   ```sql
   UPDATE tasks
   SET title = ?, description = ?, completed = ?, updated_at = CURRENT_TIMESTAMP
   WHERE id = ? AND user_id = ?
   ```
   - Used by: PATCH /api/v1/tasks/{id}, POST /api/v1/tasks/{id}/toggle
   - Expected: 1 row updated or 0 (0 = 404 or 403)

7. **Delete Task**:
   ```sql
   DELETE FROM tasks
   WHERE id = ? AND user_id = ?
   ```
   - Used by: DELETE /api/v1/tasks/{id}
   - Expected: 1 row deleted or 0 (0 = 404 or 403)

### Performance Considerations

- **SC-005**: All queries must complete within 500ms
- User-scoped queries (tasks by user_id) are optimized with index
- Email lookup (authentication) is optimized with unique index
- No N+1 query issues (no nested relationships loaded in Phase II)
- Connection pooling reduces query overhead

## Validation Summary

### User Validation

| Rule | Validation Point | Error Response |
|------|------------------|----------------|
| Email format | API layer (Pydantic) | 400 Bad Request with field error |
| Email uniqueness | Database constraint | 400 Bad Request "Email already registered" |
| Password length | API layer (Pydantic) | 400 Bad Request with field error |
| Password hashing | Service layer (before DB) | N/A (internal operation) |

### Task Validation

| Rule | Validation Point | Error Response |
|------|------------------|----------------|
| Title required | API layer (Pydantic) | 400 Bad Request "Title required" |
| Title max 100 chars | API layer (Pydantic) | 400 Bad Request "Title too long" |
| Description max 500 chars | API layer (Pydantic) | 400 Bad Request "Description too long" |
| User ownership | Service layer | 403 Forbidden "Not authorized" |
| Task exists | Database query result | 404 Not Found "Task not found" |

## Migration Scripts

### Initial Migration (001_create_users_and_tasks.py)

```python
"""Create users and tasks tables

Revision ID: 001
Create Date: 2026-01-08
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )

    # Create index on email
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.String(500), nullable=True),
        sa.Column('completed', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )

    # Create indexes on tasks
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('ix_tasks_user_id_created_at', 'tasks', ['user_id', sa.text('created_at DESC')])

def downgrade():
    op.drop_table('tasks')
    op.drop_table('users')
```

## Extensibility for Future Phases

### Phase III+ Considerations

While maintaining Phase II isolation, the data model is designed for extension:

- **Task Categories/Tags** (Future): Additional tables can be added without modifying existing schema
- **Task Sharing** (Future): Junction table (task_shares) can be added for many-to-many user-task relationships
- **Task Attachments** (Future): New attachments table with foreign key to tasks.id
- **User Profiles** (Future): Additional fields can be added to users table or separate profiles table

**Important**: No placeholders or stub fields for future features in Phase II schema. Extensions happen in future migrations only.

## Compliance Matrix

| Requirement | Compliance |
|-------------|------------|
| FR-001: Allow signup | ✓ Users table supports email + password |
| FR-002: Unique emails | ✓ Unique constraint on email field |
| FR-003: Hash passwords | ✓ Password field stores bcrypt hash |
| FR-008: Create tasks | ✓ Tasks table with title + description |
| FR-009: Title validation | ✓ Title NOT NULL, max 100 chars |
| FR-010: Description validation | ✓ Description nullable, max 500 chars |
| FR-011: Unique IDs | ✓ UUID primary keys for both tables |
| FR-012: User association | ✓ user_id foreign key on tasks |
| FR-018: Persist data | ✓ PostgreSQL via Neon |
| FR-019: Referential integrity | ✓ Foreign key constraint with CASCADE |
| FR-020: Creation timestamps | ✓ created_at on both tables |
| FR-021: Update timestamps | ✓ updated_at on both tables |
| FR-022: Default completed | ✓ completed defaults to false |

## Summary

The data model consists of two entities (User, Task) with a 1:N relationship. All validation rules from FR-001 through FR-022 are enforced through database constraints, API validation, or service layer authorization checks. The model supports all Phase II functional requirements while maintaining extensibility for future phases without requiring schema changes to existing tables.
