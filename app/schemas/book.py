from pydantic import BaseModel
from typing import Optional


class BookCreate(BaseModel):
    title: str
    author: str
    pages: int = 0
    price: float = 0.0
    is_published: bool = True


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    pages: Optional[int] = None
    price: Optional[float] = None
    is_published: Optional[bool] = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    price: float
    is_published: bool

    model_config = {"from_attributes": True}
