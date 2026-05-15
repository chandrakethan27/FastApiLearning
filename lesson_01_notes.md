# Lesson 1: Hello FastAPI

## What is FastAPI?
- A modern Python web framework for building APIs
- Built on top of Starlette (for web) and Pydantic (for data validation)
- Automatic interactive API docs (Swagger UI + ReDoc)
- Type hints drive everything — validation, docs, editor support

## Key Concepts in This Lesson

### 1. Creating an app
```python
app = FastAPI()
```
This creates your application instance. Everything attaches to this.

### 2. Routes (aka endpoints)
```python
@app.get("/")
```
This decorator says: "when someone visits `/` with a GET request, run this function."

### 3. HTTP Methods
- GET    -> Read data      (e.g., fetch a user profile)
- POST   -> Create data    (e.g., register a new user)
- PUT    -> Update data    (e.g., edit a profile)
- DELETE -> Remove data    (e.g., delete an account)

### 4. Running the server
```bash
uvicorn main:app --reload
```
- `main` = the file name (main.py)
- `app`  = the FastAPI instance variable
- `--reload` = auto-restart when you save changes (dev only)

## Try It!
1. Run: `uvicorn main:app --reload`
2. Open: http://127.0.0.1:8000
3. Open: http://127.0.0.1:8000/docs  (interactive Swagger UI!)
4. Open: http://127.0.0.1:8000/redoc (alternative docs)

## What to Notice
- The JSON response `{"message": "Hello, FastAPI!"}` — FastAPI auto-converts dicts to JSON
- The `/docs` page lets you test your API right in the browser
- The `/items/42` endpoint shows how URL parameters work
- Change `42` to any number and see it reflected in the response
