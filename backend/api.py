"""
Entry point for Hugging Face Spaces deployment.
This file imports the FastAPI app from app.main
"""
from app.main import app

# This is the ASGI application that Hugging Face will use
__all__ = ["app"]
