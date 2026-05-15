"""
Main app — creates the FastAPI instance and includes all routers.
This file is TINY. That's the point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, users, books

# Create all database tables
Base.metadata.create_all(bind=engine)

# Create the app
app = FastAPI(
    title="Bookstore API (Structured)",
    description="Lessons 1-10 combined into a production-ready project",
    version="2.0.0",
)

# CORS — allows frontend apps on other domains to call your API
# In production, replace ["*"] with your actual frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # e.g. ["https://your-frontend.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers — each one adds its routes to the app
app.include_router(auth.router)     # /auth/register, /auth/login
app.include_router(users.router)    # /users/me, /users/
app.include_router(books.router)    # /books/ (CRUD)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Bookstore API is running!"}
