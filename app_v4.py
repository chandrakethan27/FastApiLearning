from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth import (
    users_db,
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    UserRegister,
    UserProfile,
    TokenResponse,
)

app = FastAPI(title="Lesson 7 — JWT Authentication")


# ============================================================
# PUBLIC ROUTES — no token needed
# ============================================================

@app.get("/")
def home():
    return {"message": "Welcome! Register at /register, login at /login"}


# --- Register a new user ---
@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    # Check if username already exists
    if user.username in users_db:
        raise HTTPException(
            status_code=400,
            detail="Username already taken",
        )

    # Hash the password and store
    users_db[user.username] = {
        "username": user.username,
        "hashed_password": hash_password(user.password),
        "role": "user",
    }

    return {"message": f"User '{user.username}' registered successfully!"}


# --- Login and get a JWT token ---
# OAuth2PasswordRequestForm is a special FastAPI form that expects
# 'username' and 'password' as form fields (not JSON!)
@app.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Find the user
    user = users_db.get(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Wrong username or password")

    # Verify password
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Wrong username or password")

    # Create JWT token — "sub" (subject) is the standard claim for the user identity
    token = create_access_token(data={"sub": user["username"]})

    return {"access_token": token, "token_type": "bearer"}


# ============================================================
# PROTECTED ROUTES — token required!
# ============================================================

# get_current_user dependency:
#   1. reads the Authorization header
#   2. decodes the JWT
#   3. returns the user dict
# If anything fails → automatic 401 error

@app.get("/me", response_model=UserProfile)
def get_my_profile(current_user: dict = Depends(get_current_user)):
    return current_user


@app.get("/me/secret")
def get_secret_data(current_user: dict = Depends(get_current_user)):
    return {
        "user": current_user["username"],
        "secret": "The answer to everything is 42.",
        "message": "Only authenticated users can see this!",
    }


# --- Admin-only route (role check on top of auth) ---
def require_admin(current_user: dict = Depends(get_current_user)):
    """Dependency that chains on get_current_user and checks the role."""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


@app.get("/admin/users")
def list_all_users(admin: dict = Depends(require_admin)):
    return {
        "admin": admin["username"],
        "users": [
            {"username": u["username"], "role": u["role"]}
            for u in users_db.values()
        ],
    }


# --- Utility: make yourself admin (for testing) ---
@app.post("/make-admin/{username}")
def make_admin(username: str, current_user: dict = Depends(get_current_user)):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[username]["role"] = "admin"
    return {"message": f"'{username}' is now an admin!"}
