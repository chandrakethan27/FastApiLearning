# Lesson 2: POST Requests & Pydantic Models

## The Problem
When a client sends data TO your API (e.g., creating a user), you need to:
1. Receive the data
2. Validate it (is email valid? is age a number?)
3. Convert it to the right types

FastAPI does ALL of this automatically using Pydantic models.

## Key Concepts

### 1. Pydantic BaseModel
```python
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True  # default value = optional field
```
- Define your data shape as a class
- Type hints ARE the validation rules
- Fields with defaults are optional
- Fields without defaults are required

### 2. Using it in a POST route
```python
@app.post("/items")
def create_item(item: Item):
    return item
```
- FastAPI sees `item: Item` and knows to read JSON from the request body
- It validates automatically — wrong types get a clear error response

### 3. What happens if validation fails?
Send `{"name": "Phone", "price": "not-a-number"}` and you get:
```json
{
  "detail": [
    {
      "type": "float_parsing",
      "loc": ["body", "price"],
      "msg": "Input should be a valid number"
    }
  ]
}
```
FastAPI returns a 422 error with EXACTLY what went wrong. You write zero validation code!

### 4. Optional fields with Optional/None
```python
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None  # can be missing or null
```

## Try It!
1. Go to http://127.0.0.1:8000/docs
2. Click on POST /items
3. Click "Try it out"
4. Edit the JSON body and click "Execute"
5. Try sending invalid data — see the automatic error messages!

## Key Takeaway
> In FastAPI, your Python type hints ARE your validation, your documentation,
> and your serialization — all at once. Write it once, get three things free.
