"""
Books router — full CRUD at /books/
Public: list and get. Protected: create, update, delete.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.services.book import (
    create_book, get_all_books, get_book, update_book, delete_book,
)
from app.models.user import User

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


# --- Public routes (no auth needed) ---

@router.get("/", response_model=list[BookResponse])
def list_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_books(db, skip=skip, limit=limit)


@router.get("/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# --- Protected routes (auth required) ---

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def add_book(
    data: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # must be logged in
):
    return create_book(db, data)


@router.patch("/{book_id}", response_model=BookResponse)
def edit_book(
    book_id: int,
    data: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = update_book(db, book_id, data)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not delete_book(db, book_id):
        raise HTTPException(status_code=404, detail="Book not found")
