# FastAPI Learning — Zero to Production

A hands-on, conceptual guide to FastAPI covering every major topic from "Hello World" to deployment. Each lesson has a plain-English notes file and working code you can run immediately.

---

## Who This Is For

Beginners who know basic Python and want to build real APIs. No prior web framework experience needed.

---

## How This Repo Is Organized

```
FastApiLearning/
│
├── lesson_01_notes.md        # Concept notes for each lesson
├── lesson_02_notes.md
│   ...
├── lesson_10_notes.md
│
├── app_v2.py                 # Lessons 1–4 in one file (beginner, no DB)
├── database.py               # Lesson 5 helpers
├── models.py
├── schemas.py
├── crud.py
├── app_v3.py                 # Lesson 5 — SQLAlchemy database
├── app_v4.py                 # Lesson 6 — Async, background tasks, uploads
├── auth.py                   # Lesson 7 — JWT auth helpers
├── main.py                   # Lesson 7 app entry point
│
├── app/                      # Lesson 8+ — production project structure
│   ├── main.py               #   App factory
│   ├── config.py             #   Settings
│   ├── database.py           #   DB engine & session
│   ├── dependencies.py       #   Shared dependencies
│   ├── models/               #   SQLAlchemy models
│   ├── schemas/              #   Pydantic schemas
│   ├── routers/              #   APIRouter per feature
│   └── services/             #   Business logic layer
│
├── tests/                    # Lesson 9 — pytest test suite
├── Dockerfile                # Lesson 10 — containerization
├── Procfile                  # Lesson 10 — Heroku / Railway deploy
├── .env.example              # Environment variable template
└── requirements.txt          # All dependencies
```

---

## Lessons

| # | Notes File | Topic | Code File(s) |
|---|-----------|-------|-------------|
| 1 | `lesson_01_notes.md` | Hello FastAPI, GET, path & query params | `app_v2.py` |
| 2 | `lesson_02_notes.md` | POST requests & Pydantic models | `app_v2.py` |
| 3 | `lesson_03_notes.md` | Response models, status codes, HTTPException | `app_v2.py` |
| 4 | `lesson_04_notes.md` | Middleware & Dependency Injection | `app_v2.py` |
| 5 | `lesson_05_notes.md` | Real database with SQLAlchemy | `app_v3.py` + `database.py` `models.py` `schemas.py` `crud.py` |
| 6 | `lesson_06_notes.md` | Async, background tasks & file uploads | `app_v4.py` |
| 7 | `lesson_07_notes.md` | JWT authentication | `main.py` + `auth.py` |
| 8 | `lesson_08_notes.md` | APIRouter & production project structure | `app/` |
| 9 | `lesson_09_notes.md` | Testing with pytest & TestClient | `tests/` |
| 10 | `lesson_10_notes.md` | Deployment — Docker, Heroku, Railway | `Dockerfile` `Procfile` |

---

## Topics Covered

- **REST fundamentals** — GET, POST, PUT, DELETE, path params, query params
- **Pydantic** — request validation, response models, type safety
- **Error handling** — HTTPException, custom status codes
- **Dependency Injection** — reusable dependencies, shared logic
- **Middleware** — request/response lifecycle hooks, CORS
- **SQLAlchemy ORM** — models, sessions, CRUD operations with SQLite
- **Async Python** — `async def`, `await`, sync vs async comparison
- **Background Tasks** — fire-and-forget operations
- **File Uploads** — multipart/form-data, saving files
- **JWT Authentication** — password hashing, token creation, protected routes
- **Project Structure** — APIRouter, services, schemas, models separation
- **Testing** — pytest, TestClient, fixtures, test isolation
- **Deployment** — Docker, environment variables, cloud platforms

---

## Quick Start

**Prerequisites:** Python 3.10+

```bash
# 1. Clone the repo
git clone https://github.com/chandrakethan27/FastApiLearning.git
cd FastApiLearning

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run a lesson
# Lessons 1–4 (no database needed):
uvicorn app_v2:app --reload

# Lesson 5 (SQLAlchemy):
uvicorn app_v3:app --reload

# Lesson 6 (async + uploads):
uvicorn app_v4:app --reload

# Lesson 7 (JWT auth):
uvicorn main:app --reload

# Lessons 8–10 (full project):
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs** — FastAPI gives you interactive API docs for free.

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Suggested Learning Path

1. Read `lesson_01_notes.md` → run `app_v2.py` → hit the endpoints in `/docs`
2. Continue lesson by lesson in order
3. After lesson 7, switch to the `app/` folder and explore the structured project
4. Write your own routes as exercises after each lesson

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values before running the structured app:

```bash
cp .env.example .env
```

---

## License

MIT — use freely for learning and projects.
