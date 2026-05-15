# Lesson 6: Async, Background Tasks & File Uploads

## Part A: Async — What and Why?

### The Problem
Imagine your API needs to call an external service (weather API, payment gateway).
With sync code, the server WAITS and can't handle other requests:

```
Request 1: calls weather API... waiting 2 seconds... done
Request 2: has to wait for Request 1 to finish first!
```

With async, the server handles other work while waiting:

```
Request 1: calls weather API... waiting...
Request 2: starts immediately! No waiting!
Request 1: ...weather API responds, done
```

### Sync vs Async in FastAPI
```python
# SYNC — blocks the worker while waiting
@app.get("/sync")
def sync_route():
    result = slow_network_call()  # blocks!
    return result

# ASYNC — frees the worker while waiting
@app.get("/async")
async def async_route():
    result = await slow_network_call()  # frees the worker!
    return result
```

### When to use which?
| Use `def` (sync) when... | Use `async def` when... |
|---------------------------|--------------------------|
| CPU-bound work | I/O-bound work (network, file, DB) |
| Simple DB queries | Calling external APIs |
| Quick operations | Using async libraries (httpx, aiofiles) |

### Rule of thumb:
- If you don't use `await` inside, just use `def` — it's simpler
- FastAPI handles both just fine
- Don't mix: never call sync blocking code inside `async def`

---

## Part B: Background Tasks

### The Problem
Client uploads a file → you need to send a confirmation email.
Should the client wait for the email to send? NO! Send it in the background.

```python
from fastapi import BackgroundTasks

def send_email(to: str, subject: str):
    time.sleep(3)  # pretend this takes time
    print(f"Email sent to {to}: {subject}")

@app.post("/register")
def register(background_tasks: BackgroundTasks):
    # ... create user ...
    background_tasks.add_task(send_email, "user@mail.com", "Welcome!")
    return {"message": "Registered!"}  # returns IMMEDIATELY
    # email sends in the background after response
```

- `add_task(function, arg1, arg2)` — queues it to run AFTER the response
- Client gets instant response, slow work happens behind the scenes
- Perfect for: emails, notifications, log writing, cleanup

---

## Part C: File Uploads

### Single file
```python
from fastapi import UploadFile

@app.post("/upload")
async def upload(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```

### Multiple files
```python
@app.post("/upload-many")
async def upload_many(files: list[UploadFile]):
    return [{"name": f.filename} for f in files]
```

### UploadFile properties:
- `file.filename` — original file name
- `file.content_type` — MIME type (image/png, text/csv, etc.)
- `file.size` — file size in bytes
- `await file.read()` — read the full content
- `await file.read(1024)` — read in chunks (for large files)

---

## Try It!
1. GET /slow-sync and GET /slow-async — both take 2s, but async frees the server
2. POST /notify — returns instantly, check terminal 3s later for the "email"
3. POST /upload — upload any file, see its info
4. POST /upload-many — upload multiple files at once
5. GET /external-api — see async HTTP call to a real API
