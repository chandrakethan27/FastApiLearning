from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    pages = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    is_published = Column(Boolean, default=True)
