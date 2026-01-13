# Phase II Frontend - Next.js Todo Application

Next.js 14 frontend with TypeScript, JWT authentication, and task management.

## Setup Instructions

### Prerequisites

- Node.js 18 or higher
- npm, yarn, or pnpm package manager
- Backend API running on `http://localhost:8000`

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local if backend URL is different
   ```

### Running the Application

**Development mode** (with hot reload):
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

**Production build**:
```bash
npm run build
npm run start
```

The application will be available at `http://localhost:3000`

### Testing

Run tests:
```bash
npm test
# or
yarn test
```

Run tests in watch mode:
```bash
npm run test:watch
```

## Application Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout with navigation
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
│   │   └── AuthForm.tsx     # Reusable auth form
│   ├── lib/
│   │   ├── api.ts           # API client with auth headers
│   │   └── auth.ts          # Auth utilities
│   └── types/
│       ├── user.ts          # User TypeScript types
│       └── task.ts          # Task TypeScript types
├── tests/
│   ├── components/          # Component unit tests
│   └── integration/         # Integration tests
├── package.json
├── tsconfig.json
├── next.config.js
├── .env.local.example
└── README.md
```

## Features

### Authentication Flow

1. **Signup** (`/signup`):
   - User enters email and password (min 8 characters)
   - Frontend validates input and sends POST to `/api/v1/auth/signup`
   - Backend creates user and returns JWT token
   - Token stored in localStorage
   - User redirected to `/tasks`

2. **Login** (`/login`):
   - User enters email and password
   - Frontend sends POST to `/api/v1/auth/login`
   - Backend validates credentials and returns JWT token
   - Token stored in localStorage
   - User redirected to `/tasks`

3. **Authenticated Requests**:
   - All API requests to `/api/v1/tasks/*` include `Authorization: Bearer <token>` header
   - API client automatically injects token from localStorage
   - Unauthorized requests (401) redirect user to `/login`

### Task Management

1. **View Tasks** (`/tasks`):
   - Displays all tasks for authenticated user
   - Tasks sorted by creation date (newest first)
   - Shows task title, description, completion status

2. **Create Task**:
   - Form with title (required, max 100 chars) and description (optional, max 500 chars)
   - Real-time character count
   - Validation feedback
   - Task appears in list immediately after creation

3. **Update Task**:
   - Click edit button to enter edit mode
   - Modify title, description, or completion status
   - Changes saved via PATCH request
   - Task updates in list

4. **Toggle Completion**:
   - Checkbox to toggle task completion
   - Visual indicator for completed tasks
   - Updates via POST to `/api/v1/tasks/{id}/toggle`

5. **Delete Task**:
   - Delete button with confirmation
   - Removes task from list
   - Cannot be undone

## Component Architecture

### Client Components vs Server Components

- **Server Components** (default in Next.js 14 App Router):
  - Pages (`layout.tsx`, `page.tsx`)
  - Handles initial page render
  - Can fetch data on server

- **Client Components** (`'use client'` directive):
  - Interactive components (forms, buttons, inputs)
  - Components using React hooks (useState, useEffect)
  - Components accessing browser APIs (localStorage)

### API Client (`lib/api.ts`)

Centralized API client that:
- Handles all HTTP requests to backend
- Automatically injects JWT token from localStorage
- Handles error responses (400, 401, 403, 404, 500)
- Provides type-safe request/response handling

### Auth Utilities (`lib/auth.ts`)

Authentication helpers:
- `getToken()`: Retrieve JWT from localStorage
- `setToken(token)`: Store JWT in localStorage
- `removeToken()`: Clear JWT from localStorage
- `isAuthenticated()`: Check if user has valid token
- Token management abstracted from components

## API Integration

### Backend Endpoints

All endpoints use `NEXT_PUBLIC_API_URL` from environment variables.

**Authentication**:
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login

**Tasks** (require authentication):
- `GET /tasks` - List user's tasks
- `POST /tasks` - Create new task
- `PATCH /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `POST /tasks/{id}/toggle` - Toggle completion

### Error Handling

- **400 Bad Request**: Display validation errors to user
- **401 Unauthorized**: Redirect to login, clear token
- **403 Forbidden**: Show "Access denied" message
- **404 Not Found**: Show "Task not found" message
- **500 Server Error**: Show generic error message

## Development Guide

### Adding a New Page

1. Create page file in `src/app/your-page/page.tsx`
2. Export default React component
3. Add navigation link in `src/app/layout.tsx`

### Adding a New Component

1. Create component file in `src/components/YourComponent.tsx`
2. Add `'use client'` directive if using interactivity
3. Export component
4. Import and use in pages

### Making API Calls

```typescript
import { apiClient } from '@/lib/api';

// Example: Fetch tasks
const tasks = await apiClient.get('/tasks');

// Example: Create task
const newTask = await apiClient.post('/tasks', {
  title: 'Task title',
  description: 'Optional description'
});
```

### Managing Authentication

```typescript
import { getToken, setToken, removeToken, isAuthenticated } from '@/lib/auth';

// Check if authenticated
if (isAuthenticated()) {
  // User is logged in
}

// Store token after login
setToken(response.access_token);

// Clear token on logout
removeToken();
```

## Styling

This project uses inline styles for simplicity. You can add:
- **Tailwind CSS**: For utility-first styling
- **CSS Modules**: For scoped component styles
- **styled-components**: For CSS-in-JS

## Deployment

### Environment Variables

Set in production environment:
- `NEXT_PUBLIC_API_URL`: Backend API URL (e.g., `https://api.yourdomain.com/api/v1`)
- `NEXT_PUBLIC_APP_NAME`: Application name

### Build and Deploy

1. **Build production bundle**:
   ```bash
   npm run build
   ```

2. **Start production server**:
   ```bash
   npm run start
   ```

3. **Deploy to platforms**:
   - Vercel (recommended for Next.js)
   - Netlify
   - AWS Amplify
   - Docker container

### Production Considerations

1. **CORS**: Ensure backend allows requests from frontend domain
2. **HTTPS**: Use HTTPS in production for secure token transmission
3. **Environment Variables**: Never commit `.env.local` to git
4. **API URL**: Update `NEXT_PUBLIC_API_URL` to production backend
5. **Error Tracking**: Add error tracking (Sentry, etc.)
6. **Analytics**: Add analytics if needed

## Troubleshooting

### API Connection Errors

- Verify backend is running on `NEXT_PUBLIC_API_URL`
- Check CORS configuration in backend
- Ensure network connectivity

### Authentication Issues

- Check token is stored in localStorage
- Verify token format: `Bearer <token>`
- Check token expiration (24 hours by default)
- Clear localStorage and re-login if issues persist

### Build Errors

- Delete `.next` folder and rebuild
- Clear `node_modules` and reinstall dependencies
- Check TypeScript errors: `npm run build`

## Testing Strategy

### Component Tests

Test individual components in isolation:
- Rendering with different props
- User interactions (clicks, form submissions)
- Conditional rendering
- Error states

### Integration Tests

Test user flows:
- Signup → Login → View Tasks
- Create Task → Update Task → Delete Task
- Authentication required for protected pages
- Error handling and validation

## Browser Support

- Chrome (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Edge (last 2 versions)
