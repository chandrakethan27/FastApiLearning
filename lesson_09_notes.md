# Lesson 9: Testing Your FastAPI App

## Why Test?
- Catch bugs BEFORE they reach users
- Refactor with confidence — if tests pass, nothing broke
- Tests ARE documentation — they show how the API is supposed to behave

## Key Concepts

### 1. TestClient — FastAPI's built-in test helper
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
```
- No server needed! TestClient simulates requests in-memory
- Same interface as requests/httpx — `.get()`, `.post()`, `.json()`, etc.

### 2. Test Database — Don't pollute real data!
We create a SEPARATE test database (test.db) so tests don't mess with real data.
After all tests run, we can throw it away.

```python
# Override the get_db dependency to use the test database
app.dependency_overrides[get_db] = get_test_db
```
This is the power of dependency injection — swap the real DB for a test DB
with ONE line!

### 3. Fixtures — Reusable test setup
```python
@pytest.fixture
def client():
    # setup: create tables
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # teardown: drop tables (clean slate for next test)
    Base.metadata.drop_all(bind=engine)
```
- `@pytest.fixture` = a function that provides something tests need
- `yield` = "give this to the test, then run cleanup after"
- Each test gets a fresh database!

### 4. What to test (the testing pyramid)

```
         /  E2E  \          ← Few: full user flows
        /----------\
       / Integration \      ← Some: routes + DB together
      /----------------\
     /    Unit Tests     \  ← Many: individual functions
    /______________________\
```

In this lesson we write **integration tests** — they hit the actual routes
with a real (test) database.

### 5. Test naming convention
```python
def test_<what>_<expected_behavior>():
    # test_register_success
    # test_register_duplicate_fails
    # test_get_book_not_found_returns_404
```

### 6. The AAA Pattern
Every test follows: **Arrange → Act → Assert**
```python
def test_create_book(client):
    # ARRANGE: prepare data
    book_data = {"title": "Dune", "author": "Herbert", "price": 14.99}

    # ACT: make the request
    response = client.post("/books/", json=book_data)

    # ASSERT: check the result
    assert response.status_code == 201
    assert response.json()["title"] == "Dune"
```

## Running Tests
```bash
python -m pytest tests/ -v
```
- `-v` = verbose (shows each test name and pass/fail)
- `-v --tb=short` = shorter error tracebacks
- `tests/test_books.py` = run only book tests
- `tests/test_books.py::test_create_book` = run ONE specific test

## Try It!
1. Run: `python -m pytest tests/ -v`
2. Watch all tests pass (green!)
3. Break something in the code — run tests again, see them fail (red!)
4. Fix it — tests pass again. That's the workflow!
