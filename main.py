from fastapi import FastAPI, HTTPException, status, Depends, Header, Request
from pydantic import BaseModel
from typing import Optional
import time

# Create the app
app = FastAPI()


# ============================================================
# LESSON 4: Middleware — runs on EVERY request
# ============================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"  {request.method} {request.url.path} - {response.status_code} - {duration:.3f}s")
    return response


# ============================================================
# LESSON 1: GET requests, path params, query params
# ============================================================

@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item number {item_id}"}


# Try: http://127.0.0.1:8000/search?q=python&limit=5
@app.get("/search")
def search(q: str, limit: int = 10):
    return {"query": q, "limit": limit, "results": [f"Result {i} for '{q}'" for i in range(1, limit + 1)]}


# ============================================================
# LESSON 2: POST requests & Pydantic models
# ============================================================

# Step 1: Define your data shape with a Pydantic model
class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None  # optional — can be missing or null
    in_stock: bool = True              # optional — defaults to True


# Step 2: Use it in a POST route — FastAPI reads + validates the JSON body
@app.post("/items")
def create_item(item: Item):
    return {"message": f"Item '{item.name}' created!", "item": item}


# Step 3: Combine path params + body — both at once!
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "updated": item}


# In-memory storage to make it more realistic
fake_db: list[dict] = []


@app.post("/items/save")
def save_item(item: Item):
    item_dict = item.model_dump()  # convert Pydantic model -> dict
    fake_db.append(item_dict)
    return {"message": "Saved!", "total_items": len(fake_db), "item": item_dict}


@app.get("/items/all")
def get_all_items():
    return {"items": fake_db, "count": len(fake_db)}


# ============================================================
# LESSON 3: Response Models, Status Codes & Error Handling
# ============================================================

# --- Response Models: control what the client sees ---

# What the client SENDS (includes password)
class UserIn(BaseModel):
    name: str
    email: str
    password: str


# What the client GETS BACK (password is hidden!)
class UserOut(BaseModel):
    id: int
    name: str
    email: str


# Fake user database
users_db: dict[int, dict] = {}
user_id_counter = 0


# response_model=UserOut ensures password is NEVER sent back
@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserIn):
    global user_id_counter
    user_id_counter += 1
    user_data = {"id": user_id_counter, **user.model_dump()}
    users_db[user_id_counter] = user_data
    return user_data  # has password, but response_model strips it!


# --- HTTPException: raise clean errors ---

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return users_db[user_id]


@app.get("/users", response_model=list[UserOut])
def list_users():
    return list(users_db.values())


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    del users_db[user_id]
    # 204 = no content, so we return nothing


# ============================================================
# LESSON 4: Dependencies — reusable logic injected into routes
# ============================================================

# --- Dependency 1: Shared pagination logic ---
def common_pagination(skip: int = 0, limit: int = 10):
    """Instead of writing skip/limit in every route, define it once."""
    return {"skip": skip, "limit": limit}


# Fake product data
products_db = [
    {"id": i, "name": f"Product {i}", "price": round(9.99 * i, 2)}
    for i in range(1, 21)  # 20 products
]


@app.get("/products")
def list_products(pagination: dict = Depends(common_pagination)):
    skip = pagination["skip"]
    limit = pagination["limit"]
    return {
        "products": products_db[skip: skip + limit],
        "pagination": pagination,
        "total": len(products_db),
    }


# --- Dependency 2: Simple auth check ---
def get_current_user(token: str = Header()):
    """Check the 'token' header. If invalid, the route never runs."""
    if token != "secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )
    return {"username": "Alice", "role": "admin"}


@app.get("/protected")
def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Welcome {user['username']}! You have {user['role']} access."}


@app.get("/protected/dashboard")
def dashboard(user: dict = Depends(get_current_user)):
    return {
        "user": user["username"],
        "stats": {"total_products": len(products_db), "total_users": len(users_db)},
    }
