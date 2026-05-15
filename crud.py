from sqlalchemy.orm import Session
from models import Book
from schemas import BookCreate, BookUpdate


def create_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)  # reload from DB to get the auto-generated id
    return db_book


def get_all_books(db: Session, skip: int = 0, limit: int = 100) -> list[Book]:
    return db.query(Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()


def update_book(db: Session, book_id: int, book_update: BookUpdate) -> Book | None:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return None
    # Only update fields that were actually provided (not None)
    update_data = book_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return False
    db.delete(db_book)
    db.commit()
    return True
