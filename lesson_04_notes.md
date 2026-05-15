# Lesson 4: Dependency Injection & Middleware

## Two separate concepts in this lesson:
1. **Middleware** — code that wraps EVERY request (see main.py lines 14-20)
2. **Dependencies** — reusable functions injected into SPECIFIC routes

---

## PART A: Middleware (main.py lines 14-20)

Middleware sits between the client and your routes. It runs on EVERY request,
no matter which endpoint is hit.

### Code in main.py:
```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()                # BEFORE the route runs
    response = await call_next(request) # actually run the route
    duration = time.time() - start      # AFTER the route runs
    print(f"  {request.method} {request.url.path} - {response.status_code} - {duration:.3f}s")
    return response
```

### How it works:
1. A request comes in (any URL, any method)
2. `start = time.time()` — record the start time
3. `await call_next(request)` — this actually runs your route function
4. After the route finishes, calculate how long it took
5. Print a log line to the terminal

### Where to see it:
Look at your TERMINAL (where uvicorn is running). Every request prints:
```
  GET /products - 200 - 0.003s
  GET /protected - 401 - 0.001s
```

### Common uses for middleware:
- Request/response logging (what we built)
- CORS headers (allow cross-origin requests)
- Rate limiting
- Adding custom headers to every response

---

## PART B: Dependency Injection (Depends)

## What is Dependency Injection (DI)?
Instead of repeating the same logic in every route (auth checks, DB connections,
pagination), you extract it into a function and FastAPI "injects" it automatically.

Think of it like: "before running this route, run THIS function first and give me the result."

## Key Concepts

### 1. Basic Dependency — Shared Logic
```python
def common_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items")
def list_items(pagination: dict = Depends(common_pagination)):
    # pagination = {"skip": 0, "limit": 10}
```
- `Depends(func)` tells FastAPI: "call this function, pass its return value here"
- The dependency's parameters show up in the docs too!

### 2. Auth Dependency — Protect Routes
```python
def get_current_user(token: str = Header()):
    if token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user": "Alice"}

@app.get("/protected")
def secret_stuff(user: dict = Depends(get_current_user)):
    return {"message": f"Hello {user['user']}"}
```
- If the dependency raises an exception, the route NEVER runs
- Perfect for auth, permissions, rate limiting

### 3. Middleware — Runs on EVERY Request
```python
@app.middleware("http")
async def log_requests(request, call_next):
    # BEFORE the route runs
    start = time.time()
    response = await call_next(request)  # run the actual route
    # AFTER the route runs
    duration = time.time() - start
    print(f"{request.method} {request.url.path} - {duration:.3f}s")
    return response
```
- Middleware wraps ALL routes — no need to add it per-endpoint
- Great for logging, CORS, timing, adding headers

### 4. Dependencies vs Middleware
| | Dependencies | Middleware |
|---|---|---|
| Scope | Per-route (you choose) | ALL routes |
| Access | Function params + return | Raw request/response |
| Use for | Auth, DB, pagination | Logging, CORS, timing |

## The Mental Model
```
Request comes in
    |
    v
  Middleware (before) — logging, timing start
    |
    v
  Dependencies resolve — auth check, get DB, parse pagination
    |
    v
  Your route function runs
    |
    v
  Middleware (after) — add headers, log duration
    |
    v
Response goes out
```

## Try It!
1. GET /protected — fails with 401 (no token)
2. GET /protected with header `token: secret-token` — works!
3. GET /products?skip=5&limit=3 — pagination via dependency
4. Watch your terminal — middleware logs every request with timing
