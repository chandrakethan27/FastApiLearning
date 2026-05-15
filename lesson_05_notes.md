# Lesson 5: Real Database with SQLAlchemy

## Why a Database?
So far we used `fake_db = []` — data disappears when the server restarts.
Now we'll use SQLite (a file-based database) with SQLAlchemy (Python's most popular ORM).

## What is an ORM?
ORM = Object Relational Mapper. Instead of writing raw SQL:
```sql
INSERT INTO books (title, author, pages) VALUES ('Dune', 'Frank Herbert', 412);
```
You write Python:
```python
book = Book(title="Dune", author="Frank Herbert", pages=412)
db.add(book)
db.commit()
```
The ORM translates Python objects <-> database rows.

## Project Structure (real-world pattern!)
```
FastApiLearning/
    main.py          <-- still our main app (lessons 1-4)
    database.py      <-- NEW: database connection setup
    models.py        <-- NEW: database table definitions
    schemas.py       <-- NEW: Pydantic models (request/response shapes)
    crud.py          <-- NEW: database operations (Create, Read, Update, Delete)
    app_v2.py        <-- NEW: clean FastAPI app using the database
```

## Why separate files?
| File | Purpose | Analogy |
|------|---------|---------|
| database.py | How to connect | The power cable |
| models.py | Table structure | The blueprint |
| schemas.py | API data shapes | The form you fill out |
| crud.py | DB operations | The warehouse worker |
| app_v2.py | Routes + glue | The front desk |

## Key Concepts

### 1. database.py — Engine + Session
- **Engine** = the connection to the database file
- **SessionLocal** = a factory that creates database sessions
- **Base** = parent class for all your table models

### 2. models.py — Table as a Python class
```python
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
```
Each class = a table. Each attribute = a column.

### 3. schemas.py — Pydantic models (NOT the same as DB models!)
- **BookCreate** — what the client sends (no id, the DB generates that)
- **BookResponse** — what the client gets back (includes id)
- DB models = table shape. Pydantic schemas = API shape.

### 4. crud.py — Keep DB logic separate
```python
def create_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    return db_book
```

### 5. Depends(get_db) — The DB Session Dependency
```python
def get_db():
    db = SessionLocal()
    try:
        yield db      # give the session to the route
    finally:
        db.close()    # always close when done
```
`yield` makes this a generator — FastAPI calls it, gets the session,
runs your route, then the `finally` block cleans up. No leaked connections!

## Try It!
1. Run: uvicorn app_v2:app --reload --port 8001
2. Open: http://127.0.0.1:8001/docs
3. POST /books — create some books
4. GET /books — see them listed
5. Restart the server — data is STILL THERE (it's in books.db file!)

## The Big Picture
```
Client Request
    |
    v
app_v2.py (route) --> Depends(get_db) gives a DB session
    |
    v
schemas.py validates the input (Pydantic)
    |
    v
crud.py does the database work (SQLAlchemy)
    |
    v
models.py defines the table structure
    |
    v
database.py manages the connection
    |
    v
books.db (SQLite file on disk)
```
