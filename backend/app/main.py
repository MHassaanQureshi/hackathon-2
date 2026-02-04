"""
FastAPI application entry point.
Initializes app, configures CORS, registers routes.
"""
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import create_db_and_tables, close_db
from app.api.v1 import api_router

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="Phase II - Full-Stack Web Application with JWT Authentication",
    version="2.0.0",
    debug=settings.DEBUG
)

# Configure JSON response to use aliases (camelCase for frontend)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse as FastAPIJSONResponse

class JSONResponse(FastAPIJSONResponse):
    def render(self, content) -> bytes:
        return super().render(
            jsonable_encoder(content, by_alias=True)
        )

app.router.default_response_class = JSONResponse

# Configure CORS
# Allow all origins in development for easier testing
# In production, restrict to specific frontend URL
origins = [settings.FRONTEND_URL]
if settings.DEBUG:
    origins.extend([
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Create database tables on application startup."""
    try:
        logger.info("Starting application...")
        await create_db_and_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


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


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


# Register API v1 router
app.include_router(api_router, prefix="/api/v1")
