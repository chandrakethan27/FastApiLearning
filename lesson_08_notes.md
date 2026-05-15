# Lesson 8: APIRouter & Real Project Structure

## The Problem
Right now all our routes are in one file. That works for learning, but real apps
have dozens or hundreds of endpoints. Imagine 50 routes in one file — nightmare!

## The Solution: APIRouter
APIRouter lets you split routes into separate files by topic, then plug them
into the main app. Think of it like Blueprints in Flask.

```
# Without Router (everything in one file):
app_v4.py → /register, /login, /me, /books, /upload, /search, /products...

# With Routers (organized by feature):
main app
  ├── routers/auth.py     → /auth/register, /auth/login
  ├── routers/books.py    → /books/, /books/{id}
  ├── routers/uploads.py  → /uploads/, /uploads/{id}
  └── routers/users.py    → /users/me, /users/{id}
```

## How APIRouter Works

### 1. Create a router in a separate file
```python
# routers/books.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/books",       # all routes start with /books
    tags=["Books"],        # grouped in /docs under "Books"
)

@router.get("/")           # this becomes GET /books/
def list_books():
    return [...]

@router.post("/")          # this becomes POST /books/
def create_book():
    return [...]
```

### 2. Plug it into the main app
```python
# main.py
from routers import books

app = FastAPI()
app.include_router(books.router)
```

That's it! The router's routes are now part of the app.

## Key Parameters

| Parameter | What it does | Example |
|-----------|-------------|---------|
| `prefix` | URL prefix for all routes | `prefix="/books"` → `/books/...` |
| `tags` | Groups in Swagger docs | `tags=["Books"]` |
| `dependencies` | Auth/checks for ALL routes in this router | `dependencies=[Depends(get_current_user)]` |

## Project Structure (production-ready pattern)

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py           # app creation, router includes, startup
│   ├── config.py         # settings, environment variables
│   ├── database.py       # DB engine, session, base
│   ├── models/           # SQLAlchemy table definitions
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── book.py
│   ├── schemas/          # Pydantic request/response models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── book.py
│   ├── routers/          # route handlers, grouped by feature
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── books.py
│   ├── services/         # business logic (not in routes!)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── book.py
│   └── dependencies.py   # shared dependencies (get_db, get_current_user)
├── requirements.txt
└── .env
```

## Why This Structure?
- **Routers** → handle HTTP (request in, response out)
- **Services** → business logic (validation rules, calculations)
- **Models** → database tables
- **Schemas** → API data shapes

Each layer only knows about the layer below it. Routes don't touch the DB directly,
they call services. Services don't know about HTTP, they work with plain data.

## Try It!
1. Run: uvicorn app.main:app --reload --port 8004
2. Open /docs — routes are grouped by tags (Auth, Books, Users)
3. The exact same functionality, but organized properly
4. Look at each file — notice how small and focused they are
