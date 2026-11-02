from typing import Optional
from pydantic import BaseModel, field_validator


class UserUpdateRequest(BaseModel):
    # Regular users can only update allowed fields like full_name
    full_name: Optional[str] = None


class AdminUserUpdateRequest(BaseModel):
    # Admins can update full_name, role, or active status
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ("user", "admin"):
            raise ValueError("Role must be 'user' or 'admin'")
        return v
