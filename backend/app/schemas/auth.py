"""
Authentication schemas.
Pydantic models for authentication request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """
    User registration request.

    Attributes:
        email: Valid email address
        password: Password (minimum 8 characters)
    """
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")


class LoginRequest(BaseModel):
    """
    User login request.

    Attributes:
        email: User email address
        password: User password
    """
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    """
    JWT token response.

    Attributes:
        access_token: JWT access token
        token_type: Token type (always "bearer")
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
