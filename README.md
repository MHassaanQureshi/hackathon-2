# Evolution of Todo - Multi-Phase Todo Application

A comprehensive todo application demonstrating evolution from CLI to full-stack web application with planned AI integration.

## Project Phases

### Phase I: CLI Application ✅ Complete
A command-line interface todo application with in-memory storage. See `todo/` directory.

### Phase II: Full-Stack Web Application ✅ Complete
A complete web-based todo application with JWT authentication and persistent storage.

**Stack**:
- **Backend**: FastAPI + SQLModel + Neon PostgreSQL
- **Frontend**: Next.js 14 + React 18 + TypeScript
- **Auth**: JWT tokens (24-hour expiration)
- **Database**: Neon PostgreSQL (serverless)

**Features**:
- 🔐 User authentication (signup, login)
- ✅ Full CRUD task management
- 👤 User-scoped data isolation
- 🎯 RESTful API design
- 📱 Responsive web interface

### Phase III: AI-Powered Features (Planned)
AI-powered task suggestions, chatbot interface, natural language processing.

### Phase IV: Microservices Architecture (Planned)
Event-driven microservices with Kafka, Dapr, Kubernetes.

### Phase V: Advanced Features (Planned)
Analytics, team collaboration, advanced integrations.

## Quick Start - Phase II

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL database (Neon DB recommended)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL and generate SECRET_KEY with:
openssl rand -hex 32

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend URL**: http://localhost:8000
**API Docs**: http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local

# Run frontend
npm run dev
```

**Frontend URL**: http://localhost:3000

## Architecture - Phase II

```
┌─────────────────────────┐
│   Next.js Frontend      │  http://localhost:3000
│  (React, TypeScript)    │
└──────────┬──────────────┘
           │ REST API + JWT
┌──────────▼──────────────┐
│    FastAPI Backend      │  http://localhost:8000
│  (Python, SQLModel)     │
└──────────┬──────────────┘
           │ asyncpg
┌──────────▼──────────────┐
│ Neon PostgreSQL         │
│ (Serverless Database)   │
└─────────────────────────┘
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/login` - Login user

### Tasks (Authenticated)
- `GET /api/v1/tasks` - Get all user tasks
- `POST /api/v1/tasks` - Create new task
- `PATCH /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task
- `POST /api/v1/tasks/{id}/toggle` - Toggle completion

## Project Structure

```
hackathon-2/
├── backend/                # Phase II - FastAPI backend
│   ├── app/
│   │   ├── models/        # SQLModel entities
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── api/           # API routes
│   │   ├── config.py      # Configuration
│   │   ├── database.py    # DB connection
│   │   └── main.py        # FastAPI app
│   ├── tests/             # Backend tests
│   └── README.md
├── frontend/              # Phase II - Next.js frontend
│   ├── src/
│   │   ├── app/          # Pages (App Router)
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities (API, auth)
│   │   └── types/        # TypeScript types
│   └── README.md
├── todo/                  # Phase I - CLI application
├── specs/                 # Feature specifications
├── history/               # PHRs and ADRs
└── .specify/              # SpecKit templates
```

## User Flows - Phase II

### 1. Sign Up & Login
1. Visit `/signup` and create account with email/password
2. Backend hashes password (bcrypt) and creates user
3. Receive JWT token (24-hour expiration)
4. Token stored in localStorage
5. Redirect to `/tasks` dashboard

### 2. Task Management
1. **Create**: Fill form with title (required, max 100 chars) and description (optional, max 500 chars)
2. **View**: See all your tasks sorted by creation date
3. **Update**: Click edit, modify details, save changes
4. **Complete**: Toggle checkbox to mark done/undone
5. **Delete**: Click delete button with confirmation

### 3. Data Isolation
- Each user sees only their own tasks
- Cross-user access attempts return 403 Forbidden
- JWT token validates identity on every request
- Database queries filter by user_id

## Features - Phase II

### Implemented ✅
- User registration and authentication
- JWT-based stateless auth
- Secure password hashing (bcrypt cost 12)
- Task CRUD operations
- User-scoped data isolation
- Input validation
- Error handling
- Responsive UI
- Real-time form validation
- Character counters
- Loading states
- Empty states

### Not Implemented ❌ (Future Phases)
- Password reset
- Email verification
- MFA
- Social login
- Task sharing
- Task categories/tags
- Due dates
- Notifications
- Real-time sync
- Offline mode
- AI features
- Analytics

## Testing

### Backend Tests
```bash
cd backend
pytest                    # Run all tests
pytest --cov=app          # With coverage
```

### Frontend Tests
```bash
cd frontend
npm test                  # Run tests
npm run test:watch        # Watch mode
```

## Development

### Adding Features
1. Update specs in `specs/<feature>/`
2. Implement backend (models, services, API)
3. Implement frontend (types, components, pages)
4. Add tests
5. Update documentation

### Code Quality
- Backend: FastAPI automatic validation, type hints
- Frontend: TypeScript strict mode, ESLint
- Testing: pytest (backend), Jest (frontend)
- Documentation: Inline comments, README files

## Deployment

### Backend
1. Set environment variables (DATABASE_URL, SECRET_KEY, FRONTEND_URL)
2. Use production ASGI server: `uvicorn app.main:app --workers 4`
3. Enable HTTPS (reverse proxy)
4. Use managed PostgreSQL (Neon DB)

### Frontend
1. Build: `npm run build`
2. Set NEXT_PUBLIC_API_URL to production backend
3. Deploy to Vercel/Netlify or custom server
4. Enable HTTPS

## Security

✅ **Implemented**:
- Password hashing (bcrypt cost 12)
- JWT token expiration (24 hours)
- Stateless authentication
- CORS configuration
- Input validation
- SQL injection prevention (ORM)
- User data isolation

⚠️ **Production Requirements**:
- Use HTTPS
- Strong SECRET_KEY (32+ bytes)
- Regular key rotation
- Rate limiting
- Security headers

## Performance

- Async database operations (asyncpg)
- Database indexes on email and user_id
- Stateless JWT (no DB lookup per request)
- Frontend optimistic updates
- Response time < 500ms

## Success Criteria - Phase II

All 17 success criteria met:
- ✅ SC-001 to SC-017 (see specs for details)
- ✅ Authentication under 30 seconds
- ✅ Task operations under 2 seconds
- ✅ Complete data isolation
- ✅ All CRUD operations functional
- ✅ No Phase I/III dependencies
- ✅ Architecture ready for future phases

## Documentation

- **Project**: This README
- **Backend**: `backend/README.md`
- **Frontend**: `frontend/README.md`
- **Specifications**: `specs/001-fullstack-web-app/`
- **API Docs**: http://localhost:8000/docs (when running)

## Troubleshooting

### Database Connection
- Check DATABASE_URL format
- Verify Neon DB credentials
- Test network connectivity

### Authentication Issues
- Verify SECRET_KEY is set
- Check token expiration
- Clear localStorage and re-login

### CORS Errors
- Verify FRONTEND_URL matches origin
- Check CORS middleware config
- Ensure backend allows frontend domain

## Contributing

This project follows Spec-Driven Development (SDD). See `.specify/memory/constitution.md` for governance rules.

## License

GIAIC Quarter 5 Hackathon 2 Project

## Support

For issues:
- Backend: See `backend/README.md`
- Frontend: See `frontend/README.md`
- Specifications: See `specs/001-fullstack-web-app/`
