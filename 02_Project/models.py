from pydantic import BaseModel, Field


class MenuItem(BaseModel):
    id: str
    name: str
    description: str
    category: str
    price: float
    is_veg: bool
    is_available: bool
    rating: float = Field(ge=0, le=5)


class MenuResponse(BaseModel):
    status: str = "success"
    count: int
    items: list[MenuItem]
