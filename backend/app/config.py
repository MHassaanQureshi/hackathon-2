"""
Application configuration using Pydantic Settings.
Environment variables are loaded from .env file.
"""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    DATABASE_URL: str = Field(
        ...,
        description="PostgreSQL database URL with asyncpg driver"
    )

    # JWT Configuration
    SECRET_KEY: str = Field(
        ...,
        description="Secret key for JWT token generation"
    )
    ALGORITHM: str = Field(
        default="HS256",
        description="JWT signing algorithm"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=1440,  # 24 hours
        description="JWT token expiration time in minutes"
    )

    # CORS Configuration
    FRONTEND_URL: str = Field(
        default="http://localhost:3000",
        description="Frontend URL for CORS configuration"
    )

    # Application Configuration
    DEBUG: bool = Field(
        default=False,
        description="Debug mode"
    )
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
