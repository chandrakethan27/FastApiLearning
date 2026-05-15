from pydantic import BaseModel
from typing import Optional


# --- What the client SENDS when creating a book ---
class BookCreate(BaseModel):
    title: str
    author: str
    pages: int = 0
    price: float = 0.0
    is_published: bool = True


# --- What the client SENDS when updating (all fields optional) ---
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    pages: Optional[int] = None
    price: Optional[float] = None
    is_published: Optional[bool] = None


# --- What the client GETS BACK (includes the id from the database) ---
class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    pages: int
    price: float
    is_published: bool

    model_config = {"from_attributes": True}
    # ^ This tells Pydantic: "you can read data from SQLAlchemy model attributes"
    #   Without this, Pydantic can't convert a DB object to a response
