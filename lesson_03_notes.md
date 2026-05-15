# Lesson 3: Response Models, Status Codes & Error Handling

## Why Response Models?
Your database item might have a `password` or `internal_id` you don't want to expose.
Response models let you control EXACTLY what the client sees.

```python
class UserIn(BaseModel):    # what the client SENDS
    name: str
    email: str
    password: str

class UserOut(BaseModel):   # what the client GETS BACK
    name: str
    email: str
    # password is NOT here — it's hidden from the response!
```

## Key Concepts

### 1. response_model — filter your output
```python
@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    return user  # even though user has password, response_model strips it!
```
FastAPI automatically removes fields not in the response model.

### 2. Status Codes
HTTP status codes tell the client what happened:
- 200 = OK (default for GET)
- 201 = Created (use for POST that creates something)
- 204 = No Content (use for DELETE)
- 404 = Not Found
- 422 = Validation Error (FastAPI sends this automatically)

```python
@app.post("/users", status_code=201)  # returns 201 instead of 200
```

### 3. HTTPException — raise errors cleanly
```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return db[user_id]
```
- `raise`, not `return` — it stops execution immediately
- `detail` becomes the error message in the JSON response
- FastAPI catches it and sends the right HTTP status code

### 4. The Pattern: Input Model -> Process -> Output Model
```
Client sends JSON  -->  InputModel validates it
                            |
                        Your logic runs
                            |
                        OutputModel filters it  -->  Client gets clean JSON
```

## Try It!
1. POST /users — create a user WITH a password
2. Notice the response does NOT include the password (response_model filters it)
3. GET /users/999 — see the 404 error
4. DELETE /users/{id} — see the 204 status code
5. Check the /docs page — response models appear in the schema!
