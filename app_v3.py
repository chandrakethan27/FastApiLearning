import asyncio
import time
from pathlib import Path

import httpx
from fastapi import FastAPI, UploadFile, BackgroundTasks, HTTPException

app = FastAPI(title="Lesson 6 — Async, Background Tasks & Uploads")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# ============================================================
# PART A: Sync vs Async
# ============================================================

# SYNC version — blocks the worker for 2 seconds
@app.get("/slow-sync")
def slow_sync():
    time.sleep(2)  # simulates a slow operation (blocks!)
    return {"message": "Sync done after 2 seconds", "type": "sync"}


# ASYNC version — frees the worker while "waiting"
@app.get("/slow-async")
async def slow_async():
    await asyncio.sleep(2)  # simulates waiting (non-blocking!)
    return {"message": "Async done after 2 seconds", "type": "async"}


# REAL async example — call an external API without blocking
@app.get("/external-api")
async def call_external_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/json")
        return {
            "status_code": response.status_code,
            "data": response.json(),
            "note": "This was fetched asynchronously — server stayed free while waiting!",
        }


# ============================================================
# PART B: Background Tasks
# ============================================================

# This function runs AFTER the response is sent to the client
def send_fake_email(to: str, subject: str):
    print(f"  [Background] Sending email to {to}...")
    time.sleep(3)  # simulate slow email sending
    print(f"  [Background] Email sent to {to}: '{subject}'")


def write_log(message: str):
    with open("app.log", "a") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {message}\n")
    print(f"  [Background] Log written: {message}")


@app.post("/notify")
def send_notification(
    email: str,
    message: str = "Welcome!",
    background_tasks: BackgroundTasks = None,
):
    # Queue background work — these run AFTER the response
    background_tasks.add_task(send_fake_email, email, message)
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    # Client gets this response IMMEDIATELY
    return {"status": "Notification queued!", "email": email}


# ============================================================
# PART C: File Uploads
# ============================================================

# Single file upload
@app.post("/upload")
async def upload_file(file: UploadFile):
    # Read file contents
    contents = await file.read()

    # Save to disk
    save_path = UPLOAD_DIR / file.filename
    with open(save_path, "wb") as f:
        f.write(contents)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents),
        "saved_to": str(save_path),
    }


# Multiple file upload
@app.post("/upload-many")
async def upload_multiple_files(files: list[UploadFile]):
    results = []
    for file in files:
        contents = await file.read()
        save_path = UPLOAD_DIR / file.filename
        with open(save_path, "wb") as f:
            f.write(contents)
        results.append({
            "filename": file.filename,
            "size_bytes": len(contents),
        })
    return {"uploaded": len(results), "files": results}


# Upload + background processing (combining lessons!)
@app.post("/upload-and-process")
async def upload_and_process(file: UploadFile, background_tasks: BackgroundTasks):
    contents = await file.read()
    save_path = UPLOAD_DIR / file.filename
    with open(save_path, "wb") as f:
        f.write(contents)

    # Process the file in the background (client doesn't wait)
    background_tasks.add_task(
        write_log, f"Processing file: {file.filename} ({len(contents)} bytes)"
    )

    return {
        "filename": file.filename,
        "status": "Uploaded! Processing in background.",
    }
