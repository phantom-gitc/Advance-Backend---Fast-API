from sqlmodel import SQLModel, Field
from typing import Optional

class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    price: float
    is_available: bool = Field(default=True)
