from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None

class ItemRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    is_available: bool

    class Config:
        from_attributes = True
