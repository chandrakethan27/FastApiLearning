# Lesson 7: Authentication with JWT Tokens

## The Big Picture — How Login Works in APIs

APIs don't have browser cookies/sessions like websites. Instead they use **tokens**.

### The Flow:
```
1. Client sends:  POST /login  { "username": "alice", "password": "secret" }
                      |
2. Server checks:  Is password correct?
                      |
          YES --------+-------- NO
           |                     |
3. Server creates            Return 401
   a JWT token               "Wrong credentials"
           |
4. Server returns:  { "access_token": "eyJhbG..." }
           |
5. Client saves the token
           |
6. For ALL future requests, client sends:
   Header:  Authorization: Bearer eyJhbG...
           |
7. Server reads token → knows who the user is → allows/denies access
```

## What is a JWT?

JWT = JSON Web Token. It's a string with 3 parts separated by dots:

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbGljZSIsImV4cCI6MTcxMn0.abc123signature
|---- header ----|  |--------- payload ---------|  |-- signature --|
```

- **Header**: algorithm used (HS256)
- **Payload**: the data (username, expiry time)
- **Signature**: proves the token wasn't tampered with (uses your SECRET_KEY)

Anyone can READ a JWT (it's just base64). But only YOUR server can CREATE valid ones
because only it knows the SECRET_KEY.

## Key Concepts

### 1. Password Hashing — Never store plain passwords!
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"])

hashed = pwd_context.hash("mypassword")       # → "$2b$12$xK3v..."
pwd_context.verify("mypassword", hashed)       # → True
pwd_context.verify("wrongpass", hashed)        # → False
```

### 2. Creating a JWT
```python
from jose import jwt
token = jwt.encode(
    {"sub": "alice", "exp": datetime + timedelta(minutes=30)},
    SECRET_KEY,
    algorithm="HS256"
)
```

### 3. OAuth2PasswordBearer — FastAPI's auth helper
```python
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
```
This tells FastAPI:
- "There's a login endpoint at /login"
- "Protected routes need a Bearer token in the Authorization header"
- It auto-adds the lock icon in /docs!

### 4. The Auth Dependency Chain
```
oauth2_scheme extracts token from header
        |
        v
get_current_user decodes the token, finds the user
        |
        v
Your route receives the verified user object
```

## Security Rules:
- NEVER store plain text passwords → always hash with bcrypt
- NEVER put secrets in code → use environment variables in production
- ALWAYS set token expiry → tokens should expire (30 min is common)
- The SECRET_KEY in this lesson is hardcoded for learning — never do this in production!

## Try It!
1. POST /register — create a user (password gets hashed)
2. POST /login — get a JWT token
3. Copy the token
4. GET /me — click the lock icon in /docs, paste the token → see your profile
5. Wait 30 min (or change EXPIRY_MINUTES to 1) → token expires, get 401
