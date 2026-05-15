"""
conftest.py — shared fixtures for ALL test files.
pytest auto-discovers this file; no need to import it.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.dependencies import get_db
from app.main import app

# --- Test database (separate from your real app_structured.db!) ---
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def get_test_db():
    """Same as get_db, but uses the test database."""
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


# Override the real DB dependency with the test DB
app.dependency_overrides[get_db] = get_test_db


@pytest.fixture()
def client():
    """
    Gives each test a fresh TestClient with empty tables.
    After the test, tables are dropped — clean slate!
    """
    # SETUP: create all tables
    Base.metadata.create_all(bind=test_engine)

    yield TestClient(app)

    # TEARDOWN: drop all tables (fresh for next test)
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def auth_headers(client):
    """
    Registers a user and returns auth headers.
    Use this when a test needs a logged-in user.
    """
    # Register
    client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpass123",
    })

    # Login
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpass123",
    })
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
