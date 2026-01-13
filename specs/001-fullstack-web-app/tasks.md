---
description: "Task list for Phase II - Full-Stack Web Application implementation"
---

# Tasks: Phase II - Full-Stack Web Application

**Input**: Design documents from `/specs/001-fullstack-web-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Tests are included in this implementation as comprehensive testing is required for authentication security and data isolation (FR-004, FR-005, FR-006, FR-017, SC-004, SC-006, SC-007).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` for source code, `backend/tests/` for tests
- **Frontend**: `frontend/src/` for source code, `frontend/tests/` for tests
- Paths shown below follow the web application structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend directory structure per plan.md (backend/app/, backend/app/models/, backend/app/schemas/, backend/app/services/, backend/app/api/, backend/app/api/v1/, backend/tests/)
- [ ] T002 Create backend/requirements.txt with dependencies: fastapi>=0.104.0, sqlmodel>=0.0.14, python-jose[cryptography], passlib[bcrypt], uvicorn[standard], asyncpg, pytest, pytest-asyncio, httpx
- [ ] T003 [P] Create backend/.env.example with template variables: DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, FRONTEND_URL, DEBUG, LOG_LEVEL
- [ ] T004 [P] Create backend/README.md with setup instructions and API documentation structure
- [ ] T005 Create frontend directory structure per plan.md (frontend/src/app/, frontend/src/components/, frontend/src/lib/, frontend/src/types/, frontend/tests/)
- [ ] T006 Initialize Next.js 14+ project in frontend/ with TypeScript and App Router configuration
- [ ] T007 [P] Create frontend/.env.local.example with template variables: NEXT_PUBLIC_API_URL, NEXT_PUBLIC_APP_NAME
- [ ] T008 [P] Create frontend/README.md with setup instructions and development guide

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 Create backend/app/__init__.py (empty, marks app as Python package)
- [ ] T010 Create backend/app/config.py with Pydantic Settings class for environment variables (DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, FRONTEND_URL, per plan.md Phase 1)
- [ ] T011 Create backend/app/database.py with async SQLModel engine, session factory, and get_db dependency (using asyncpg driver per plan.md Phase 0)
- [ ] T012 Create backend/app/models/__init__.py (empty, marks models as package)
- [ ] T013 Create backend/app/schemas/__init__.py (empty, marks schemas as package)
- [ ] T014 Create backend/app/services/__init__.py (empty, marks services as package)
- [ ] T015 Create backend/app/api/__init__.py (empty, marks api as package)
- [ ] T016 Create backend/app/api/v1/__init__.py with APIRouter setup for /api/v1 base path (per FR-027)
- [ ] T017 Create backend/app/main.py with FastAPI application initialization, CORS middleware for FRONTEND_URL, and /api/v1 router registration
- [ ] T018 Create backend/tests/__init__.py (empty, marks tests as package)
- [ ] T019 Create backend/tests/conftest.py with pytest fixtures: test_db (in-memory SQLite or test PostgreSQL), test_client (TestClient), test_engine, async_session_maker
- [ ] T020 Create frontend/src/types/user.ts with User interface (id, email, createdAt, updatedAt per plan.md Phase 1 data model)
- [ ] T021 Create frontend/src/types/task.ts with Task interface (id, userId, title, description, completed, createdAt, updatedAt per plan.md Phase 1 data model)
- [ ] T022 Create frontend/src/lib/api.ts with base API client using fetch, Authorization header injection, error handling (per plan.md Phase 0 frontend architecture)
- [ ] T023 Create frontend/src/lib/auth.ts with token storage utilities (localStorage), getToken, setToken, removeToken, isAuthenticated (per plan.md Phase 0 authentication flow)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to sign up with email/password, log in, receive JWT tokens, and gain authenticated access to the application

**Independent Test**: Sign up with various email/password combinations, verify token issuance, log in with those credentials, confirm token validity

**Spec Reference**: spec.md lines 10-24 (User Story 1), FR-001 through FR-007, SC-001, SC-002, SC-007, SC-010

### Backend Models for User Story 1

- [ ] T024 [P] [US1] Create backend/app/models/user.py with User SQLModel class (id, email unique/indexed, hashed_password, created_at, updated_at, tasks relationship per plan.md Phase 1 data model lines 359-376)

### Backend Services for User Story 1

- [ ] T025 [US1] Create backend/app/services/auth.py with password hashing functions (hash_password using bcrypt cost 12, verify_password), JWT generation (create_access_token with HS256, 24hr expiration per plan.md Phase 0 lines 266-274), JWT validation (decode_token, verify expiration)
- [ ] T026 [US1] Create backend/app/schemas/auth.py with Pydantic schemas: SignupRequest (email EmailStr, password str min 8 chars), LoginRequest (email, password), TokenResponse (access_token, token_type="bearer" per FR-004)

### Backend API for User Story 1

- [ ] T027 [US1] Create backend/app/api/deps.py with get_db dependency (yields async session), get_current_user dependency (extracts JWT from Authorization header, validates token, queries User by ID from token.sub, returns User or raises 401 per plan.md Phase 0 lines 297-304)
- [ ] T028 [US1] Create backend/app/api/v1/auth.py with POST /api/v1/auth/signup endpoint (validates email uniqueness per FR-002, hashes password per FR-003, creates User, returns JWT per FR-004, handles 400 validation/409 conflict per plan.md Phase 1 lines 433-436)
- [ ] T029 [US1] Create backend/app/api/v1/auth.py with POST /api/v1/auth/login endpoint (retrieves User by email, verifies password per plan.md Phase 0 lines 287-295, returns JWT, handles 401 invalid credentials per plan.md Phase 1 lines 438-441)
- [ ] T030 [US1] Register auth router in backend/app/api/v1/__init__.py and verify /api/v1 prefix in backend/app/main.py

### Backend Database Setup for User Story 1

- [ ] T031 [US1] Create database initialization script in backend/app/database.py with create_db_and_tables function that uses SQLModel.metadata.create_all for User table (per plan.md Phase 1 lines 400-410)
- [ ] T032 [US1] Update backend/app/main.py startup event to call create_db_and_tables for table creation on application start

### Backend Tests for User Story 1

- [ ] T033 [P] [US1] Create backend/tests/test_auth.py with test_signup_success (valid email/password, expects 201, JWT token returned, User created in DB)
- [ ] T034 [P] [US1] Create backend/tests/test_auth.py with test_signup_duplicate_email (signup twice with same email, expects 409 conflict per spec.md acceptance scenario 4 line 23)
- [ ] T035 [P] [US1] Create backend/tests/test_auth.py with test_signup_invalid_email (malformed email, expects 400 validation error per edge case line 64)
- [ ] T036 [P] [US1] Create backend/tests/test_auth.py with test_login_success (existing user, correct credentials, expects 200, JWT token per spec.md acceptance scenario 2 line 21)
- [ ] T037 [P] [US1] Create backend/tests/test_auth.py with test_login_invalid_credentials (wrong password, expects 401 per spec.md acceptance scenario 3 line 22)
- [ ] T038 [P] [US1] Create backend/tests/test_auth.py with test_login_nonexistent_user (email not registered, expects 401)
- [ ] T039 [P] [US1] Create backend/tests/test_auth.py with test_jwt_token_structure (verify token contains sub=user_id, email, exp, iat per plan.md Phase 0 lines 266-274)
- [ ] T040 [P] [US1] Create backend/tests/test_auth.py with test_jwt_token_expiration (verify expired token raises 401 per FR-006)
- [ ] T041 [P] [US1] Create backend/tests/test_auth.py with test_get_current_user_valid_token (valid JWT, returns User object)
- [ ] T042 [P] [US1] Create backend/tests/test_auth.py with test_get_current_user_invalid_token (forged/manipulated JWT, expects 401 per edge case line 70)
- [ ] T043 [P] [US1] Create backend/tests/test_auth.py with test_get_current_user_missing_token (no Authorization header, expects 401 per FR-006)

### Frontend Components for User Story 1

- [ ] T044 [P] [US1] Create frontend/src/components/AuthForm.tsx reusable form component with email/password fields, submit button, error display, loading state (per plan.md Phase 0 lines 239-249)
- [ ] T045 [US1] Create frontend/src/app/signup/page.tsx with signup page using AuthForm, calling POST /api/v1/auth/signup via api.ts, storing token via auth.ts setToken, redirecting to /tasks on success (per plan.md Phase 0 lines 276-285)
- [ ] T046 [US1] Create frontend/src/app/login/page.tsx with login page using AuthForm, calling POST /api/v1/auth/login via api.ts, storing token via auth.ts setToken, redirecting to /tasks on success (per plan.md Phase 0 lines 287-295)
- [ ] T047 [US1] Create frontend/src/app/layout.tsx with root layout, navigation links to /signup, /login, /tasks, and conditional display based on auth.ts isAuthenticated
- [ ] T048 [US1] Create frontend/src/app/page.tsx home page with welcome message and links to signup/login

### Frontend Tests for User Story 1

- [ ] T049 [P] [US1] Create frontend/tests/components/AuthForm.test.tsx with test_renders_email_password_fields, test_handles_form_submission, test_displays_error_message
- [ ] T050 [P] [US1] Create frontend/tests/integration/auth.test.tsx with test_signup_flow (fill form, submit, mock API success, verify token stored, verify redirect)
- [ ] T051 [P] [US1] Create frontend/tests/integration/auth.test.tsx with test_login_flow (fill form, submit, mock API success, verify token stored, verify redirect)
- [ ] T052 [P] [US1] Create frontend/tests/integration/auth.test.tsx with test_signup_error_handling (mock API 400/409 errors, verify error display)
- [ ] T053 [P] [US1] Create frontend/tests/integration/auth.test.tsx with test_login_error_handling (mock API 401 error, verify error display)

**Checkpoint**: At this point, User Story 1 should be fully functional - users can sign up, log in, receive JWT tokens, and authentication is tested end-to-end

---

## Phase 4: User Story 2 - Task Creation and Viewing (Priority: P2)

**Goal**: Enable authenticated users to create new tasks (title + optional description) and view their personal task list with complete data isolation

**Independent Test**: Authenticate a user, create multiple tasks with various titles/descriptions, verify all created tasks appear in the user's task list with correct data, confirm user-scoped isolation

**Spec Reference**: spec.md lines 27-41 (User Story 2), FR-008 through FR-013, FR-017, SC-003, SC-004, SC-006

### Backend Models for User Story 2

- [ ] T054 [P] [US2] Create backend/app/models/task.py with Task SQLModel class (id, user_id foreign key to users.id with CASCADE, title max 100, description optional max 500, completed default False, created_at, updated_at, user relationship per plan.md Phase 1 data model lines 378-397)

### Backend Services for User Story 2

- [ ] T055 [US2] Create backend/app/services/task.py with create_task function (accepts user_id, title, description, creates Task with user_id, returns Task per FR-012)
- [ ] T056 [US2] Create backend/app/services/task.py with get_user_tasks function (accepts user_id, queries tasks WHERE user_id=user_id ORDER BY created_at DESC, returns List[Task] per FR-013 and spec.md acceptance scenario 2 line 38)
- [ ] T057 [US2] Create backend/app/schemas/task.py with Pydantic schemas: TaskCreate (title str max 100 required, description optional str max 500 per FR-009, FR-010), TaskResponse (id, user_id, title, description, completed, created_at, updated_at per plan.md Phase 1 lines 443-470)

### Backend API for User Story 2

- [ ] T058 [US2] Create backend/app/api/v1/tasks.py with GET /api/v1/tasks endpoint (depends on get_current_user, calls get_user_tasks with current_user.id, returns List[TaskResponse], handles 401 per FR-031 and plan.md Phase 1 lines 445-448)
- [ ] T059 [US2] Create backend/app/api/v1/tasks.py with POST /api/v1/tasks endpoint (depends on get_current_user, validates TaskCreate schema, calls create_task with current_user.id, returns 201 TaskResponse per FR-032 and plan.md Phase 1 lines 450-454)
- [ ] T060 [US2] Register tasks router in backend/app/api/v1/__init__.py and verify /api/v1 prefix in backend/app/main.py

### Backend Database Setup for User Story 2

- [ ] T061 [US2] Update backend/app/database.py create_db_and_tables to include Task table creation with foreign key to users (per plan.md Phase 1 lines 412-425)

### Backend Tests for User Story 2

- [ ] T062 [P] [US2] Create backend/tests/conftest.py fixture for authenticated_user (creates test user, returns user + JWT token for authenticated requests)
- [ ] T063 [P] [US2] Create backend/tests/test_tasks.py with test_create_task_success (authenticated user, valid title/description, expects 201, Task created with correct user_id per spec.md acceptance scenario 1 line 37)
- [ ] T064 [P] [US2] Create backend/tests/test_tasks.py with test_create_task_title_too_long (title > 100 chars, expects 400 validation error per spec.md acceptance scenario 3 line 39)
- [ ] T065 [P] [US2] Create backend/tests/test_tasks.py with test_create_task_empty_title (empty/whitespace title, expects 400 per edge case line 67)
- [ ] T066 [P] [US2] Create backend/tests/test_tasks.py with test_create_task_description_too_long (description > 500 chars, expects 400 per edge case line 71)
- [ ] T067 [P] [US2] Create backend/tests/test_tasks.py with test_create_task_unauthenticated (no JWT token, expects 401 per spec.md acceptance scenario 4 line 40)
- [ ] T068 [P] [US2] Create backend/tests/test_tasks.py with test_get_tasks_success (authenticated user with tasks, expects 200, returns only user's tasks sorted by created_at DESC per spec.md acceptance scenario 2 line 38)
- [ ] T069 [P] [US2] Create backend/tests/test_tasks.py with test_get_tasks_empty (authenticated user with no tasks, expects 200, returns empty list)
- [ ] T070 [P] [US2] Create backend/tests/test_tasks.py with test_get_tasks_data_isolation (create two users with tasks, verify each user only sees their own tasks per FR-017, SC-004, SC-006)
- [ ] T071 [P] [US2] Create backend/tests/test_tasks.py with test_get_tasks_unauthenticated (no JWT token, expects 401 per spec.md acceptance scenario 4 line 40)

### Frontend Components for User Story 2

- [ ] T072 [P] [US2] Create frontend/src/components/TaskForm.tsx with form for title (required, max 100), description (optional, max 500), submit button, validation, error display (per plan.md Phase 0 lines 239-249)
- [ ] T073 [P] [US2] Create frontend/src/components/TaskItem.tsx with display for single task (title, description, completed status, created date)
- [ ] T074 [US2] Create frontend/src/components/TaskList.tsx with list rendering of TaskItem components, empty state message, loading state (per plan.md Phase 0 lines 239-249)
- [ ] T075 [US2] Create frontend/src/app/tasks/page.tsx with task dashboard: TaskForm for creation, TaskList for display, fetches GET /api/v1/tasks on mount, handles POST /api/v1/tasks on form submit, requires authentication (redirect to /login if no token per plan.md Phase 0 lines 297-304)

### Frontend Tests for User Story 2

- [ ] T076 [P] [US2] Create frontend/tests/components/TaskForm.test.tsx with test_renders_title_description_fields, test_validates_title_required, test_validates_title_max_length, test_handles_form_submission
- [ ] T077 [P] [US2] Create frontend/tests/components/TaskItem.test.tsx with test_renders_task_data, test_displays_completion_status
- [ ] T078 [P] [US2] Create frontend/tests/components/TaskList.test.tsx with test_renders_multiple_tasks, test_displays_empty_state, test_displays_loading_state
- [ ] T079 [P] [US2] Create frontend/tests/integration/tasks.test.tsx with test_create_task_flow (authenticated, fill form, submit, mock API 201, verify task appears in list)
- [ ] T080 [P] [US2] Create frontend/tests/integration/tasks.test.tsx with test_view_tasks_flow (authenticated, mock API returns tasks, verify all tasks displayed)
- [ ] T081 [P] [US2] Create frontend/tests/integration/tasks.test.tsx with test_tasks_page_requires_auth (no token, verify redirect to /login)
- [ ] T082 [P] [US2] Create frontend/tests/integration/tasks.test.tsx with test_create_task_validation_errors (title too long, mock API 400, verify error display)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can authenticate, create tasks, and view their personal task list with data isolation enforced

---

## Phase 5: User Story 3 - Task Management (Priority: P3)

**Goal**: Enable authenticated users to update task details (title, description, completion status), toggle completion, and delete tasks they own

**Independent Test**: Create a task, update title/description/completion, verify changes persist, toggle completion multiple times, delete task and confirm removal, attempt to modify another user's task and verify 403 Forbidden

**Spec Reference**: spec.md lines 44-59 (User Story 3), FR-014 through FR-017, SC-006, SC-009

### Backend Services for User Story 3

- [ ] T083 [US3] Create backend/app/services/task.py with get_task_by_id function (accepts task_id, user_id, queries task by ID and user_id, returns Task or None for ownership validation per plan.md Phase 0 lines 313-317)
- [ ] T084 [US3] Create backend/app/services/task.py with update_task function (accepts task_id, user_id, update data dict, validates ownership via get_task_by_id, updates fields, returns updated Task or raises 403/404 per FR-014, FR-017)
- [ ] T085 [US3] Create backend/app/services/task.py with delete_task function (accepts task_id, user_id, validates ownership via get_task_by_id, deletes task, returns success or raises 403/404 per FR-015, FR-017)
- [ ] T086 [US3] Create backend/app/services/task.py with toggle_task_completion function (accepts task_id, user_id, validates ownership, toggles completed boolean, returns updated Task per FR-016)
- [ ] T087 [US3] Create backend/app/schemas/task.py with TaskUpdate Pydantic schema (title optional str max 100, description optional str max 500, completed optional bool per plan.md Phase 1 lines 456-460)

### Backend API for User Story 3

- [ ] T088 [US3] Create backend/app/api/v1/tasks.py with PATCH /api/v1/tasks/{id} endpoint (depends on get_current_user, validates TaskUpdate schema, calls update_task with current_user.id, returns 200 TaskResponse, handles 400/401/403/404 per FR-033 and plan.md Phase 1 lines 456-460)
- [ ] T089 [US3] Create backend/app/api/v1/tasks.py with DELETE /api/v1/tasks/{id} endpoint (depends on get_current_user, calls delete_task with current_user.id, returns 204 No Content, handles 401/403/404 per FR-034 and plan.md Phase 1 lines 462-465)
- [ ] T090 [US3] Create backend/app/api/v1/tasks.py with POST /api/v1/tasks/{id}/toggle endpoint (depends on get_current_user, calls toggle_task_completion with current_user.id, returns 200 TaskResponse, handles 401/403/404 per FR-035 and plan.md Phase 1 lines 467-470)

### Backend Tests for User Story 3

- [ ] T091 [P] [US3] Create backend/tests/test_tasks.py with test_update_task_success (authenticated user updates own task title/description, expects 200, changes persisted per spec.md acceptance scenario 1 line 54)
- [ ] T092 [P] [US3] Create backend/tests/test_tasks.py with test_update_task_completion_status (authenticated user updates completed field, expects 200, status changed per spec.md acceptance scenario 2 line 55)
- [ ] T093 [P] [US3] Create backend/tests/test_tasks.py with test_update_task_not_found (update non-existent task ID, expects 404 per spec.md acceptance scenario 5 line 58)
- [ ] T094 [P] [US3] Create backend/tests/test_tasks.py with test_update_task_forbidden (user A tries to update user B's task, expects 403 per spec.md acceptance scenario 4 line 57, FR-017, SC-006)
- [ ] T095 [P] [US3] Create backend/tests/test_tasks.py with test_update_task_unauthenticated (no JWT token, expects 401)
- [ ] T096 [P] [US3] Create backend/tests/test_tasks.py with test_delete_task_success (authenticated user deletes own task, expects 204, task removed from database per spec.md acceptance scenario 3 line 56)
- [ ] T097 [P] [US3] Create backend/tests/test_tasks.py with test_delete_task_not_found (delete non-existent task ID, expects 404)
- [ ] T098 [P] [US3] Create backend/tests/test_tasks.py with test_delete_task_forbidden (user A tries to delete user B's task, expects 403 per spec.md acceptance scenario 4 line 57, FR-017, SC-006)
- [ ] T099 [P] [US3] Create backend/tests/test_tasks.py with test_delete_task_unauthenticated (no JWT token, expects 401)
- [ ] T100 [P] [US3] Create backend/tests/test_tasks.py with test_toggle_task_completion_success (toggle task from incomplete to complete, expects 200, completed=true per FR-016)
- [ ] T101 [P] [US3] Create backend/tests/test_tasks.py with test_toggle_task_completion_multiple_times (toggle twice, verify returns to original state)
- [ ] T102 [P] [US3] Create backend/tests/test_tasks.py with test_toggle_task_forbidden (user A tries to toggle user B's task, expects 403)
- [ ] T103 [P] [US3] Create backend/tests/test_tasks.py with test_toggle_task_not_found (toggle non-existent task, expects 404)

### Frontend Components for User Story 3

- [ ] T104 [US3] Update frontend/src/components/TaskItem.tsx to add edit button (opens inline edit mode with TaskForm pre-filled), delete button (with confirmation), toggle completion checkbox (per plan.md Phase 0 lines 239-249)
- [ ] T105 [US3] Update frontend/src/components/TaskForm.tsx to support edit mode (pre-fill with existing task data, PATCH instead of POST)
- [ ] T106 [US3] Update frontend/src/app/tasks/page.tsx to handle PATCH /api/v1/tasks/{id} for updates, DELETE /api/v1/tasks/{id} for deletion, POST /api/v1/tasks/{id}/toggle for completion toggle

### Frontend Tests for User Story 3

- [ ] T107 [P] [US3] Update frontend/tests/components/TaskItem.test.tsx with test_renders_edit_delete_buttons, test_handles_edit_click, test_handles_delete_click_with_confirmation, test_handles_toggle_completion
- [ ] T108 [P] [US3] Update frontend/tests/components/TaskForm.test.tsx with test_edit_mode_prefills_data, test_edit_mode_submits_patch
- [ ] T109 [P] [US3] Create frontend/tests/integration/tasks-management.test.tsx with test_update_task_flow (edit task, change title/description, submit, mock API 200, verify changes reflected)
- [ ] T110 [P] [US3] Create frontend/tests/integration/tasks-management.test.tsx with test_delete_task_flow (click delete, confirm, mock API 204, verify task removed from list)
- [ ] T111 [P] [US3] Create frontend/tests/integration/tasks-management.test.tsx with test_toggle_completion_flow (click checkbox, mock API 200, verify completed state updated)
- [ ] T112 [P] [US3] Create frontend/tests/integration/tasks-management.test.tsx with test_update_task_error_handling (mock API 403/404, verify error display)

**Checkpoint**: All user stories should now be independently functional - users can authenticate, create, view, update, toggle, and delete their tasks with complete data isolation

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, documentation, and deployment readiness

- [ ] T113 [P] Add error logging to backend/app/services/auth.py and backend/app/services/task.py for debugging (per plan.md Phase 1 lines 349-353)
- [ ] T114 [P] Add request/response logging middleware to backend/app/main.py for API audit trail
- [ ] T115 [P] Create backend/app/main.py exception handlers for HTTPException, database exceptions, and unhandled exceptions with user-friendly messages (per plan.md Phase 0 lines 349-353)
- [ ] T116 [P] Update backend/README.md with complete API documentation: all endpoints, request/response examples, authentication flow, error codes (per SC-017)
- [ ] T117 [P] Update frontend/README.md with development guide: setup instructions, environment variables, component architecture, testing guide
- [ ] T118 [P] Create root README.md with project overview, Phase II description, setup instructions for backend and frontend, links to backend/frontend READMEs
- [ ] T119 Verify backend database connection with Neon PostgreSQL (test connection string, create tables, insert test data per plan.md Phase 1 lines 474-490)
- [ ] T120 Verify CORS configuration in backend/app/main.py allows requests from FRONTEND_URL (per plan.md Phase 0 risk line 544)
- [ ] T121 Run all backend tests with pytest (verify 100% pass rate per SC-017)
- [ ] T122 Run all frontend tests with Jest (verify 100% pass rate)
- [ ] T123 Manual end-to-end test: signup → login → create tasks → view tasks → update task → toggle completion → delete task (verify all user flows work per SC-001, SC-002, SC-003, SC-009)
- [ ] T124 Manual security test: create two users, attempt cross-user task access via API (verify 403 Forbidden per SC-004, SC-006)
- [ ] T125 Manual performance test: measure API response times for all endpoints (verify <500ms per SC-005)
- [ ] T126 [P] Add frontend loading states and error boundaries for better UX
- [ ] T127 [P] Add frontend form validation feedback (real-time title length counter, description length counter)
- [ ] T128 Verify no Phase I (CLI) dependencies in Phase II code (per FR-040, SC-014)
- [ ] T129 Verify no Phase III+ (AI, chatbot, MCP, Kafka, Kubernetes, Dapr) features in Phase II code (per FR-036, FR-037, FR-038, FR-039, SC-015)
- [ ] T130 Document deployment instructions in backend/README.md and frontend/README.md (environment setup, database migrations, running in production)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (Phase 3): Can start after Foundational - No dependencies on other stories
  - User Story 2 (Phase 4): Can start after Foundational - No dependencies on other stories (independently testable)
  - User Story 3 (Phase 5): Can start after Foundational - No dependencies on other stories (independently testable)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Requires User model from US1 but tasks functionality is independent
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Requires Task model from US2 but management operations are independent

### Within Each User Story

- Backend models before services
- Services before API endpoints
- API endpoints before frontend components
- Backend tests can run in parallel (marked [P])
- Frontend tests can run in parallel (marked [P])
- Database setup must complete before API tests

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004, T007, T008)
- All Foundational package creation tasks can run in parallel (T009-T018, T020-T023)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Within User Story 1: Backend model (T024) and backend service (T025, T026) are independent until API layer
- Within User Story 1: All backend tests (T033-T043) can run in parallel
- Within User Story 1: Frontend components (T044, T045, T046, T047, T048) can be developed in parallel
- Within User Story 1: All frontend tests (T049-T053) can run in parallel
- Within User Story 2: Backend model (T054), service (T055, T056, T057) are independent until API layer
- Within User Story 2: All backend tests (T063-T071) can run in parallel
- Within User Story 2: Frontend components (T072, T073, T074) can be developed in parallel
- Within User Story 2: All frontend tests (T076-T082) can run in parallel
- Within User Story 3: All service functions (T083-T087) can be developed in parallel
- Within User Story 3: All backend tests (T091-T103) can run in parallel
- Within User Story 3: All frontend tests (T107-T112) can run in parallel
- All Polish tasks marked [P] can run in parallel (T113-T118, T126-T127)

---

## Parallel Example: User Story 1 Backend Tests

```bash
# Launch all backend tests for User Story 1 together:
Task T033: "test_signup_success"
Task T034: "test_signup_duplicate_email"
Task T035: "test_signup_invalid_email"
Task T036: "test_login_success"
Task T037: "test_login_invalid_credentials"
Task T038: "test_login_nonexistent_user"
Task T039: "test_jwt_token_structure"
Task T040: "test_jwt_token_expiration"
Task T041: "test_get_current_user_valid_token"
Task T042: "test_get_current_user_invalid_token"
Task T043: "test_get_current_user_missing_token"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T008)
2. Complete Phase 2: Foundational (T009-T023) - CRITICAL: blocks all stories
3. Complete Phase 3: User Story 1 (T024-T053)
4. **STOP and VALIDATE**: Run all US1 tests, manually test signup/login flows
5. Deploy/demo if ready - authentication is fully functional

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP - authentication works!)
3. Add User Story 2 → Test independently → Deploy/Demo (Users can create and view tasks!)
4. Add User Story 3 → Test independently → Deploy/Demo (Full CRUD functionality!)
5. Complete Polish phase → Final deployment (Production-ready!)
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T023)
2. Once Foundational is done:
   - Developer A: User Story 1 (T024-T053)
   - Developer B: User Story 2 (T054-T082) - can start backend model/service/API in parallel
   - Developer C: User Story 3 (T083-T112) - can start once US2 Task model exists
3. Stories complete and integrate independently
4. Team completes Polish together (T113-T130)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label (US1, US2, US3) maps task to specific user story for traceability
- Each user story should be independently completable and testable
- All backend tests must pass before considering a user story complete
- All frontend tests must pass before considering a user story complete
- Commit after each task or logical group of tasks
- Stop at any checkpoint to validate story independently
- Authentication (US1) is required for US2 and US3, but US2 and US3 are independent of each other
- Data isolation is critical: all tests verify users cannot access other users' tasks (FR-017, SC-004, SC-006)
- Performance testing should verify <500ms API response times (SC-005)
- No Phase I (CLI) code should be modified (FR-040)
- No Phase III+ features should be introduced (FR-036, FR-037, FR-038, FR-039)
