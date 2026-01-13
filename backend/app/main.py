"""
FastAPI application entry point.
Initializes app, configures CORS, registers routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_db_and_tables, close_db
from app.api.v1 import api_router


# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="Phase II - Full-Stack Web Application with JWT Authentication",
    version="2.0.0",
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Create database tables on application startup."""
    await create_db_and_tables()


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on application shutdown."""
    await close_db()


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Todo API - Phase II",
        "version": "2.0.0",
        "status": "running"
    }


# Register API v1 router
app.include_router(api_router, prefix="/api/v1")
