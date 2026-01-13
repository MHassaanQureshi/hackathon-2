"""
API v1 router.
Aggregates all v1 endpoints under /api/v1 prefix.
"""
from fastapi import APIRouter
from app.api.v1 import auth, tasks

# Create main v1 router
api_router = APIRouter()

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
