import re
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel, EmailStr, field_validator

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    # Standard response shape across all endpoints
    success: bool = True
    message: str
    data: Optional[T] = None


class UserRegisterRequest(BaseModel):
    # Registration input schema
    full_name: str
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        # Convert email to lowercase and remove spaces
        return v.strip().lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        # Ensure password has at least 8 chars, 1 uppercase, 1 lowercase, 1 number, and 1 special char
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserLoginRequest(BaseModel):
    # Login input schema
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()
